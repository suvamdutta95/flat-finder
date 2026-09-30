from pathlib import Path
import pandas as pd
from flat_finder.models import Listing
from flat_finder.providers.base import ListingProvider

class CSVListingProvider(ListingProvider):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[Listing]:
        frame = pd.read_csv(self.path)
        return [
            Listing(
                title=row["title"], locality=row["locality"], city=row["city"],
                purpose=row["purpose"], property_type=row["property_type"],
                bhk=int(row["bhk"]), area_sqft=int(row["area_sqft"]),
                price_inr=float(row["price_inr"]), furnishing=row["furnishing"],
                parking=bool(row["parking"]), lift=bool(row["lift"]),
                posted_at=row["posted_at"], source=row["source"], url=row["url"]
            )
            for _, row in frame.iterrows()
        ]
