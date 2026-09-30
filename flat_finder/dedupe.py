import re
from typing import Iterable
from flat_finder.models import Listing

def _normalize(text: str) -> str:
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())

def listing_key(item: Listing) -> tuple:
    return (
        _normalize(item.title), _normalize(item.locality), item.bhk,
        int(item.area_sqft), round(float(item.price_inr), 2),
        item.purpose.casefold(),
    )

def dedupe_listings(items: Iterable[Listing]) -> list[Listing]:
    seen = set()
    output = []
    for item in items:
        key = listing_key(item)
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return sorted(output, key=lambda x: x.posted_at, reverse=True)
