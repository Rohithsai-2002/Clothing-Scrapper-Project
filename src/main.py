import yaml
from pathlib import Path
from src import scraper
from src import db
from src import emailer
import json


def load_config(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def matches_size(item, cfg_filters):
    title = item.get("title", "").lower()
    sizes = item.get("sizes", "").lower()
    shirt_size = cfg_filters.get("shirt_size", "xxl").lower()
    trouser_size = cfg_filters.get("trouser_size", "40").lower()

    if shirt_size in title or shirt_size in sizes:
        if "shirt" in title or "shirt" in sizes:
            return True
    if trouser_size in title or trouser_size in sizes:
        if "trouser" in title or "trouser" in sizes or "pants" in title:
            return True
    return False


def detect_offer(item):
    # consider it an offer if original_price exists and price < original_price
    price = item.get("price")
    orig = item.get("original_price")
    title = item.get("title", "").lower()
    if price and orig and price < orig:
        return True
    if "sale" in title or "offer" in title or "% off" in title:
        return True
    return False


def item_id_from(item):
    # create a simple stable id from title+url
    return (item.get("url") or item.get("title", "")).strip()


def run_once(config_path: str = "config.yaml"):
    cfg = load_config(Path(config_path))
    smtp = cfg.get("smtp", {})
    filters = cfg.get("filters", {})

    db.init_db()

    messages = []

    for store in cfg.get("stores", []):
        name = store.get("name")
        module = store.get("module")
        base = store.get("base_url", "")
        path = store.get("listings_path", "")
        selectors = store.get("selectors", {})

        url = base.rstrip("/") + path
        
        # Try custom module first (allows mock stores to skip fetching)
        store_mod = scraper.load_store_module(module) if module else None
        items = None
        html = None
        
        if store_mod and hasattr(store_mod, "adapt_items"):
            print(f"Loading {name} (custom module)")
            items = store_mod.adapt_items(html, selectors)
        
        # If custom module didn't provide items, fetch and parse HTML
        if not items:
            print(f"Fetching {name}: {url}")
            try:
                html = scraper.fetch_html(url)
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                continue

        if not items:
            items = scraper.parse_listings(html, selectors)

        for it in items:
            if not matches_size(it, filters):
                continue
            offer = detect_offer(it)
            if not offer:
                # user also requested alerts on price drops
                pass

            iid = item_id_from(it)
            prev = db.get_item(name, iid)
            prev_price = prev.get("last_price") if prev else None
            price = it.get("price")

            notify = False
            reason = None
            if offer and prev is None:
                notify = True
                reason = "New offer"
            elif price and prev_price and price < prev_price:
                notify = True
                reason = f"Price dropped {prev_price} -> {price}"

            if notify:
                messages.append(f"Store: {name}\nTitle: {it.get('title')}\nPrice: {price}\nURL: {it.get('url')}\nReason: {reason}\n")
            # upsert item record
            db.upsert_item(name, iid, it.get("title"), it.get("url"), price or prev_price or 0.0, json.dumps(it))

    if messages:
        body = "\n\n".join(messages)
        subject = "Clothing offers / price drop alert"
        print("Sending email with", len(messages), "alerts")
    else:
        body = "No new deals or price drops found at this time.\n\nFilters:\n  Shirt size: XXL\n  Trouser size: 40\n\nThe scraper will continue checking every hour."
        subject = "Clothing Notifier - Status Check (No New Deals)"
        print("Sending status email (no new alerts)")
    
    try:
        emailer.send_email(subject, body, smtp)
        print("✓ Email sent successfully!")
    except Exception as e:
        print(f"✗ Email failed: {e}")
        print(f"  (Make sure SMTP credentials in config.yaml are correct)")


if __name__ == "__main__":
    run_once()
