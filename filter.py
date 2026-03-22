from scraper import FeedItem

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
