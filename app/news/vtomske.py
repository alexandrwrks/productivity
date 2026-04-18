import httpx
import asyncio

from typing import Optional

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.news.config_news import NewsInfo

from app.news.config_news import NAME_OF_SOURCE

async def parsing_vtomske() -> Optional[NewsInfo]:
    async with httpx.AsyncClient() as client:
        url = "https://vtomske.ru/tag/tomsk"
        response = await client.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        news_card = soup.find_all("a", class_="lenta_material", limit=1)

        seen = set()
        list_news = []

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
                created_at=time_text,
                url=full_link,
                source=NAME_OF_SOURCE[0]
            )

            list_news.append(news)

        return list_news


async def main():

    list_of_news = await parsing_vtomske()

    for news in list_of_news:
        print(
            f"Заголовок: {news.title}\n"
            f"Ссылка: {news.url}\n"
            f"Дата публикаций: {news.created_at}\n"
            f"Источник: {news.source}\n\n"
        )

if __name__ == "__main__":
    asyncio.run(main())
