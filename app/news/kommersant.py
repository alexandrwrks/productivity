import httpx
import asyncio

from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.news.config import NewsInfo

from datetime import datetime

SOURCE="kommersant"

async def parsing_kommersant() -> Optional[NewsInfo]:
    async with httpx.AsyncClient(timeout=20.0) as client:

        url="https://www.kommersant.ru/lenta/news?from=lenta_news"
        response = await client.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        news_cards = soup.find_all("div", class_="uho__text", limit=5)

        news = []

        for card in news_cards:
            # Поиск даты и времени
            datatime = card.find("p", class_="uho__tag")
            datatime_text = datatime.get_text(" ", strip=True)

            # Разделяем полученные данные на дату и время
            date, time = datatime_text.split(", ")

            # Валидация полученной даты и времени для базы данных
            data = f"{date} {time}"
            valid_datatime = datetime.strptime(data, "%d.%m.%Y %H:%M")

            # Поиск названия нвости
            title = card.find("a", class_="uho__link")
            title_text = title.get_text(" ", strip=True)

            # Получение ссылки на новость
            link = title.get("href")

            # Сборка полной ссылки на новость
            full_link = urljoin(url, link)

            news_info = NewsInfo(
                title=title_text,
                url=full_link,
                created_at=valid_datatime,
                source=SOURCE
            )

            news.append(news_info)

        return news
        
async def main():

    news = await parsing_kommersant()

    for item in news:
        print(
            f"Заголовок: {item.title}\n"
            f"Ссылка: {item.url}\n"
            f"Дата публикаций: {item.created_at}\n"
            f"Источник: {item.source}\n\n"
            
        )



asyncio.run(main())