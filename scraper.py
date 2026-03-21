import feedparser, re
from dataclasses import dataclass
from typing import Optional

@dataclass
class FeedItem:
    guid: str
    title: str
    description_text: str
    link: str
    image_url: Optional[str]
    pub_date: str
    source: str = ""

def _strip_html(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()

def fetch_items(feed_url: str) -> list[FeedItem]:
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries:
        guid = entry.get("id", entry.get("link", ""))
        title = entry.get("title", "")
        description_html = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
        description_text = _strip_html(description_html)
        link = entry.get("link", "")
        pub_date = entry.get("published", "")
        image_url = None
        media_content = entry.get("media_content", [])
        if media_content:
            image_url = media_content[0].get("url")
        items.append(FeedItem(guid=guid, title=title, description_text=description_text,
                              link=link, image_url=image_url, pub_date=pub_date))
    return items
