import os, sys
from dotenv import load_dotenv
load_dotenv(override=True)
from db import ensure_table, is_seen, mark_seen
from scraper import fetch_items
from filter import is_interesting
from notifier import send_digest

def run():
    feed_url = os.environ.get("RSS_FEED_URL", "https://rss.app/feeds/8ZEez9pneLj9S3q2.xml")
    print("🐾 Kitten Watch starting...")
    ensure_table()
    items = fetch_items(feed_url)
    print(f"  Fetched {len(items)} items from feed")
    matched = []
    for item in items:
        if is_seen(item.guid):
            continue
        print(f"  New item: {item.title!r}")
        if is_interesting(item):
            print("  ✅ Matched")
            matched.append(item)
        mark_seen(item.guid)
    if matched:
        try:
            send_digest(matched)
        except Exception as e:
            print(f"  ❌ Failed to send digest: {e}", file=sys.stderr)
    print(f"  Done. {len(matched)} match(es).")

if __name__ == "__main__":
    run()
