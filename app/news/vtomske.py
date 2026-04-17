import httpx
import asyncio

from typing import Optional

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.news.config import NewsInfo

SOURCE="vtomske"

async def process_vtomske() -> Optional[NewsInfo]:
    async with httpx.AsyncClient() as client:
        url = "https://vtomske.ru/"
        response = await client.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        news_card = soup.find_all("a", class_="lenta_material", limit=5)

        seen = set()

        for card in news_card:
            link = card.get("href")
            if not link:
                continue

            title_tag = card.find("div", class_="lenta_material_title")
            if not title_tag:
                continue

            title = title_tag.get_text(" ", strip=True)

            time_tag = card.find("div", class_="lenta_material_info")

            time_text = "Нет времени"

            if time_tag:
                time_div = time_tag.find("div")
                if time_div:
                    time_text = time_div.get_text(strip=True)

            full_link = urljoin(url, link)

            if full_link in seen:
                continue

            seen.add(full_link)

            news = NewsInfo(
                title=title,
                time=time_text,
                url=full_link,
                source=SOURCE
            )

            return news


if __name__ == "__main__":
    asyncio.run(process_vtomske())
