import re
from scraper import FeedItem

def normalize_title(title: str) -> str:
    """Normalize a title for dedup: lowercase, strip price/punctuation/whitespace."""
    t = title.lower()
    t = re.sub(r"£\s*[\d,.]+", "", t)        # remove prices
    t = re.sub(r"[^a-z0-9 ]+", "", t)        # keep only alphanumeric + spaces
    t = re.sub(r"\s+", " ", t).strip()        # collapse whitespace
    return t

MATCH_KEYWORDS = [
    "kitten", "kittens", "litter",
    "longhair", "long hair", "long-hair",
    "fluffy", "siberian", "maine coon",
    "norwegian forest", "ragdoll", "persian",
    "turkish angora", "semi-longhair", "semi longhair",
]

def is_interesting(item: FeedItem) -> bool:
    text = (item.title + " " + item.description_text).lower()
    return any(kw in text for kw in MATCH_KEYWORDS)
