import os, sys, yaml
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv(override=True)
from db import ensure_table, is_seen, mark_seen
from scraper import fetch_items
from pets4homes import fetch_pets4homes
from filter import is_interesting
from notifier import send_digest

MAX_AGE_DAYS = 5

def load_sources() -> list[dict]:
    with open("sources.yaml") as f:
        return yaml.safe_load(f)["sources"]

def fetch_source(source: dict):
    if source["type"] == "pets4homes":
        return fetch_pets4homes(source["name"], distance=source.get("distance", 15))
    return fetch_items(source["url"])

def run():
    print("🐾 Kitten Watch starting...")
    ensure_table()
    sources = load_sources()
    print(f"  {len(sources)} source(s) configured")
    matched = []
    for source in sources:
        print(f"  Fetching {source['name']}")
        try:
            items = fetch_source(source)
        except Exception as e:
            print(f"    ⚠️  Failed to fetch: {e}", file=sys.stderr)
            continue
        print(f"    {len(items)} item(s) fetched")
        cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
        for item in items:
            if is_seen(item.guid):
                continue
            if item.published_at and item.published_at < cutoff:
                print(f"    Skipping old post: {item.title!r} ({item.pub_date})")
                mark_seen(item.guid)
                continue
            item.source = source["name"]
            print(f"    New: {item.title!r}")
            if source.get("skipFilter") or is_interesting(item):
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
