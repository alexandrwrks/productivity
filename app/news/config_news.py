from dataclasses import dataclass

from datetime import datetime

NAME_OF_SOURCE = [
    "vtomske",
    "kommersant",
    "euronews",
]

@dataclass
class NewsInfo:
    topic: str
    title: str
    url: str
    created_at: datetime
    source: str