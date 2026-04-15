from dataclasses import dataclass

@dataclass
class NewsInfo:
    title: str
    time: str
    source: str
    url: str