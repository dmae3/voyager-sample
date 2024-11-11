from dataclasses import dataclass
from typing import List


@dataclass
class SearchResult:
    _id: str
    name: str
    space: str
    amenities: List[str]
    price: float
    similarity_score: float

    def format_amenities(self) -> str:
        """アメニティを見やすく整形"""
        return "\n  - " + "\n  - ".join(self.amenities)
