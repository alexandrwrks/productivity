from dataclasses import dataclass

from datetime import datetime

SOURCE_LINK = {
    "vtomske": "https://vtomske.ru/tag/tomsk",
    "kommersant": "https://www.kommersant.ru/lenta/news?from=lenta_news",
    "euronews": "https://www.euronews.com/just-in"
}

SOURCES = {
    "vtomske": "Vtomske",
    "kommersant": "Kommersant",
    "euronews": "EuroNews"
}

@dataclass
class NewsInfo:
    topic: str
    title: str
    url: str
    created_at: datetime
    source: str