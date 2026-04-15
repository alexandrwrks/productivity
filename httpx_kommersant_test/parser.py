import argparse
import asyncio
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from typing import Iterable

import httpx

KOMMERSANT_RSS_URL = "https://www.kommersant.ru/RSS/news.xml"


@dataclass(slots=True)
class NewsItem:
    title: str
    link: str
    pub_date: str
    description: str


def parse_rss(xml_text: str) -> list[NewsItem]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []

    items: list[NewsItem] = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        description = (item.findtext("description") or "").strip()
        if title and link:
            items.append(
                NewsItem(
                    title=title,
                    link=link,
                    pub_date=pub_date,
                    description=description,
                )
            )
    return items


async def fetch_news(
    client: httpx.AsyncClient,
    url: str = KOMMERSANT_RSS_URL,
) -> list[NewsItem]:
    response = await client.get(url)
    response.raise_for_status()
    return parse_rss(response.text)


def print_news(news: Iterable[NewsItem], limit: int) -> None:
    for index, item in enumerate(news, start=1):
        if index > limit:
            break
        print(f"{index}. {item.title}")
        print(f"   {item.pub_date}")
        print(f"   {item.link}")


async def main(limit: int, as_json: bool) -> None:
    timeout = httpx.Timeout(connect=5.0, read=15.0, write=5.0, pool=5.0)
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; headlines-test/1.0; +https://example.com/bot)"
    }
    async with httpx.AsyncClient(timeout=timeout, headers=headers, follow_redirects=True) as client:
        news = await fetch_news(client)

    if as_json:
        print(
            json.dumps(
                [asdict(item) for item in news[:limit]],
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print_news(news, limit=limit)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Минимальный парсер новостей Kommersant через httpx (RSS)."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Сколько новостей вывести (по умолчанию: 10).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывести результат в JSON.",
    )
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    asyncio.run(main(limit=args.limit, as_json=args.json))
