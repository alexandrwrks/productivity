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

# Backward-compatible lists for legacy imports.
NAME_OF_SOURCE = list(SOURCES.keys())
LINK_OF_SOURCE = [SOURCE_LINK[key] for key in NAME_OF_SOURCE]

@dataclass
class NewsInfo:
    topic: str
    title: str
    url: str
    created_at: datetime
    # vtomske | kommersant | euronews
    source: str
