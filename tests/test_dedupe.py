from flat_finder.dedupe import dedupe_listings
from flat_finder.models import Listing

def make(title: str, posted_at: str) -> Listing:
    return Listing(
        title=title, locality="New Town", city="Kolkata", purpose="Rent",
        property_type="Apartment", bhk=2, area_sqft=900, price_inr=25000,
        furnishing="Semi-Furnished", parking=True, lift=True,
        posted_at=posted_at, source="Test", url=f"https://example.com/{title}"
    )

def test_dedupe_keeps_newest_and_removes_exact_duplicate():
    items = [make("2BHK near metro","2026-09-28T00:00:00Z"),
             make("2BHK near metro","2026-09-29T00:00:00Z")]
    result = dedupe_listings(items)
    assert len(result) == 1
    assert result[0].posted_at == "2026-09-29T00:00:00Z"
