from dataclasses import dataclass

from datetime import datetime

SOURCE = {
    "vtomske": "https://vtomske.ru/tag/tomsk",
    "kommersant": "https://www.kommersant.ru/lenta/news?from=lenta_news",
    "euronews": "https://www.euronews.com/just-in"
}

NAME_OF_SOURCE = [
    "vtomske",
    "kommersant",
    "euronews",
]

LINK_OF_SOURCE = [
    "https://vtomske.ru/tag/tomsk",
    "https://www.kommersant.ru/lenta/news?from=lenta_news",
    "https://www.euronews.com/just-in"
]

@dataclass
class NewsInfo:
    topic: str
    title: str
    url: str
    created_at: datetime
    source: str