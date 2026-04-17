from dataclasses import dataclass

from datetime import datetime

@dataclass
class NewsInfo:
    title: str
    url: str
    created_at: datetime
    source: str