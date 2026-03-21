import os, sys, yaml
from dotenv import load_dotenv
load_dotenv(override=True)
from db import ensure_table, is_seen, mark_seen
from scraper import fetch_items
from filter import is_interesting
from notifier import send_digest

def load_sources() -> list[dict]:
    with open("sources.yaml") as f:
        return yaml.safe_load(f)["rssFeeds"]

def run():
    print("🐾 Kitten Watch starting...")
    ensure_table()
    sources = load_sources()
    print(f"  {len(sources)} source(s) configured")
    matched = []
    for source in sources:
        print(f"  Fetching {source['name']}")
        items = fetch_items(source["url"])
        print(f"    {len(items)} item(s) fetched")
        for item in items:
            if is_seen(item.guid):
                continue
            item.source = source["name"]
            print(f"    New: {item.title!r}")
            if is_interesting(item):
                print("    ✅ Matched")
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
