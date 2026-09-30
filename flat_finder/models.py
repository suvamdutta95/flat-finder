from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Listing:
    title: str
    locality: str
    city: str
    purpose: str
    property_type: str
    bhk: int
    area_sqft: int
    price_inr: float
    furnishing: str
    parking: bool
    lift: bool
    posted_at: str
    source: str
    url: str

    def to_dict(self) -> dict:
        return asdict(self)
