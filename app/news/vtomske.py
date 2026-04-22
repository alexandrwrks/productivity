import asyncio
from datetime import date, datetime

import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.news.config_news import NAME_OF_SOURCE, NewsInfo, SOURCES


class VtomskeNews:
    async def parsing_vtomske(self) -> list[NewsInfo]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            url = "https://vtomske.ru/tag/tomsk"
            response = await client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("a", class_="lenta_material", limit=5)

            list_news: list[NewsInfo] = []
            for card in cards:
                link = card.get("href")
                title_tag = card.find("div", class_="lenta_material_title")
                time_tag = card.find("div", class_="lenta_material_info")
                time_div = time_tag.find("div") if time_tag else None

                if not link or not title_tag or not time_div:
                    continue

                title = title_tag.get_text(" ", strip=True)
                time_text = time_div.get_text(" ", strip=True)

                dt = datetime.strptime(f"{date.today()} {time_text}", "%Y-%m-%d %H:%M")
                full_link = urljoin(url, link)

                list_news.append(
                    NewsInfo(
                        topic=None,
                        title=title,
                        created_at=dt,
                        url=full_link,
                        source=NAME_OF_SOURCE[0],
                    )
                )

            return list_news


vtomske_news = VtomskeNews()


async def main():
    list_of_news = await vtomske_news.parsing_vtomske()

    for news in list_of_news:
        print(
            f"Заголовок: {news.title}\n"
            f"Ссылка: {news.url}\n"
            f"Дата публикаций: {news.created_at}\n"
            f"Источник: {news.source}\n\n"
        )


if __name__ == "__main__":
    asyncio.run(main())
