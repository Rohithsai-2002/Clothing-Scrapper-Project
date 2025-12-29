import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "offers.db"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            store TEXT,
            item_id TEXT,
            title TEXT,
            url TEXT,
            last_price REAL,
            raw JSON,
            PRIMARY KEY(store, item_id)
        )
        """
    )
    conn.commit()
    conn.close()

def get_item(store, item_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT last_price, raw FROM items WHERE store=? AND item_id=?", (store, item_id))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"last_price": row[0], "raw": row[1]}

def upsert_item(store, item_id, title, url, last_price, raw_json):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "REPLACE INTO items (store, item_id, title, url, last_price, raw) VALUES (?,?,?,?,?,?)",
        (store, item_id, title, url, last_price, raw_json),
    )
    conn.commit()
    conn.close()
