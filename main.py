import os, sys
from db import ensure_table, is_seen, mark_seen
from scraper import fetch_items
from filter import is_interesting
from notifier import send_notification

def run():
    feed_url = os.environ.get("RSS_FEED_URL", "https://rss.app/feeds/8ZEez9pneLj9S3q2.xml")
    print("🐾 Kitten Watch starting...")
    ensure_table()
    items = fetch_items(feed_url)
    print(f"  Fetched {len(items)} items from feed")
    new_count = matched_count = 0
    for item in items:
        if is_seen(item.guid):
            continue
        new_count += 1
        print(f"  New item: {item.title!r}")
        if is_interesting(item):
            matched_count += 1
            print("  ✅ Matched — sending notification")
            try:
                send_notification(item)
            except Exception as e:
                print(f"  ❌ Failed to send: {e}", file=sys.stderr)
        mark_seen(item.guid)
    print(f"  Done. {new_count} new item(s), {matched_count} notification(s) sent.")

if __name__ == "__main__":
    run()
