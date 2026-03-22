import json, re
import urllib.request
from scraper import FeedItem

P4H_URL_TEMPLATE = (
    "https://www.pets4homes.co.uk/sale/kittens/near-me/"
    "united-kingdom/england/west-yorkshire/"
    "?distance={distance}&price=%2C400&keyword=kitten"
)

def fetch_pets4homes(source_name: str, distance: int = 15) -> list[FeedItem]:
    url = P4H_URL_TEMPLATE.format(distance=distance)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")

    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    if not match:
        print("    ⚠️  Could not find __NEXT_DATA__ in pets4homes page")
        return []

    data = json.loads(match.group(1))
    page_props = data.get("props", {}).get("pageProps", {})
    listings = page_props.get("regularListings", []) + page_props.get("boostedListings", [])

    items = []
    seen_ids = set()
    for listing in listings:
        listing_id = listing.get("id", "")
        if listing_id in seen_ids:
            continue
        seen_ids.add(listing_id)

        slug = listing.get("slug", "")
        title = listing.get("generalInformation", {}).get("title", "") or listing.get("title", "")
        description = listing.get("displayDescription", "")
        price = listing.get("price", {}).get("amount", "")
        location = listing.get("location", {})
        location_str = ", ".join(filter(None, [location.get("postalTown"), location.get("adminRegion1")]))
        pub_date = listing.get("publishedAt", "")
        images = listing.get("images", [])
        image_url = None
        if images:
            raw = images[0].get("originalImage", "")
            uuid = raw.split("/originalImages/")[1].split("/")[0] if "/originalImages/" in raw else ""
            image_url = raw.replace("##NAME##", uuid) if uuid else None
        link = f"https://www.pets4homes.co.uk/classifieds/{slug}/"

        items.append(FeedItem(
            guid=f"p4h-{listing_id}",
            title=f"{title} — £{price}" if price else title,
            description_text=f"{location_str}\n{description}",
            link=link,
            image_url=image_url,
            pub_date=pub_date,
            source=source_name,
        ))
    return items
