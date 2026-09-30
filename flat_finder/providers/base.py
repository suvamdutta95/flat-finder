from abc import ABC, abstractmethod
from flat_finder.models import Listing

class ListingProvider(ABC):
    """Interface for an authorized property-listing data source."""
    @abstractmethod
    def load(self) -> list[Listing]:
        raise NotImplementedError
