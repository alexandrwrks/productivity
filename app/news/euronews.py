import asyncio
from datetime import datetime, timedelta
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from app.news.config_news import NewsInfo, SOURCES, SOURCE_LINK

TIME_DELTA = 5

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity"
}


class EuroNews:
    async def parsing_euronews(self) -> list[NewsInfo]:
        async with httpx.AsyncClient(
            headers=headers,
            follow_redirects=True
        ) as client:
            url = "https://www.euronews.com/just-in"
            response = await client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Получение отдельной карточки
            cards = soup.find_all("li", class_="tc-justin-timeline__item", limit=5)

            news_list = []
            for card in cards:
                meta = card.find("a", class_="tc-justin-timeline__article__metas")
                link = card.find("a", class_="tc-justin-timeline__article__link")
                title_h2 = card.find("h2", class_="tc-justin-timeline__article__title")
                time_tag = card.find("time", class_="tc-justin-timeline__article__date")

                if not meta or not link or not title_h2 or not time_tag:
                    continue

                time_span = time_tag.find("span", class_="tc-justin-timeline__article__hour")
                day_span = time_tag.find("span", class_="tc-justin-timeline__article__day")
                href = link.get("href")

                if not time_span or not day_span or not href:
                    continue

                topic_str = meta.get_text(strip=True)
                title = title_h2.get_text(" ", strip=True)
                time_str = time_span.get_text(" ", strip=True)
                date_str = day_span.get_text(" ", strip=True)

                valid_datetime = preparing_datetime(time_str, date_str)
                full_link = urljoin(url, href)

                news_list.append(
                    NewsInfo(
                        topic=topic_str,
                        title=title,
                        url=full_link,
                        source=SOURCES["euronews"],
                        created_at=valid_datetime,
                    )
                )

            return news_list

    async def print(self):
        async with httpx.AsyncClient(headers=headers,
            follow_redirects=True) as client:
            url = "https://www.euronews.com/just-in"
            response = await client.get(url)
            response.raise_for_status()
            print(response.text)
    
euro_news = EuroNews()


def preparing_datetime(time_str: str, date_str: str):
    datetime_str = f"{date_str} {time_str}"
    valid_datetime = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
    return valid_datetime + timedelta(hours=TIME_DELTA)


async def main():
    while True:
        try:
            news_list = await euro_news.parsing_euronews()
            if news_list is None:
                print(f"Нет новостей карточек")
                return
            
            for news in news_list:
                print(
                    f"Тема: {news.topic}\n\n"
                    f"Заголовок: {news.title}\n"
                    f"Ссылка: {news.url}\n"
                    f"Дата публикаций: {news.created_at}\n"
                    f"Источник: {news.source}\n\n"
                )
        except Exception as e:
            print(f"Ошибка при парсинге: {e}")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(euro_news.print())
