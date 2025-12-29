import importlib
import requests
from bs4 import BeautifulSoup
import json

def fetch_html(url, timeout=15):
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def parse_price(text: str):
    if not text:
        return None
    # crude number extraction
    s = text.replace(',', '').strip()
    num = ''
    for ch in s:
        if ch.isdigit() or ch == '.':
            num += ch
        elif num:
            break
    try:
        return float(num) if num else None
    except ValueError:
        return None

def parse_listings(html: str, selectors: dict):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for el in soup.select(selectors["item"]):
        title_el = el.select_one(selectors.get("title", ""))
        price_el = el.select_one(selectors.get("price", ""))
        orig_el = el.select_one(selectors.get("original_price", ""))
        sizes_el = el.select_one(selectors.get("sizes", ""))

        title = title_el.get_text(strip=True) if title_el else ""
        price = parse_price(price_el.get_text()) if price_el else None
        original = parse_price(orig_el.get_text()) if orig_el else None
        sizes = sizes_el.get_text(separator=",", strip=True) if sizes_el else ""
        link_el = el.select_one("a")
        url = link_el["href"] if link_el and link_el.has_attr("href") else ""

        items.append({
            "title": title,
            "price": price,
            "original_price": original,
            "sizes": sizes,
            "url": url,
        })
    return items

def load_store_module(module_path: str):
    # store modules can provide custom fetching or parsing if needed
    try:
        return importlib.import_module(module_path)
    except Exception:
        return None
