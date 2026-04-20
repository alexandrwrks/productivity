import httpx
import asyncio

from typing import Optional

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.news.config_news import NewsInfo

from app.news.config_news import NAME_OF_SOURCE

from datetime import date, datetime

class VtomskeNews:
    async def parsing_vtomske(self) -> Optional[NewsInfo]:
        async with httpx.AsyncClient() as client:
            url = "https://vtomske.ru/tag/tomsk"
            response = await client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Нахождение первой колонки с новстями 
            div = soup.find("div", class_="lenta_column")

            # Карточки нвостей
            news_card = soup.find_all("div", class_="lenta_column", limit=5)

            # Создания списка новостей
            list_news = []
            for card in news_card:
                # Получение "ссылки" на новость
                link_a = card.find("a", class_="lenta_material")
                link = link_a.get("href")

                # Получение заголовка
                title_tag = card.find("div", class_="lenta_material_title")
                title = title_tag.get_text(" ", strip=True)

                # Получение времени и даты
                time_tag = card.find("div", class_="lenta_material_info")
                time_div = time_tag.find("div")
                time_text = time_div.get_text(" ", strip=True)
                
                # Делаем валидацию даты
                today = date.today()
                datatime = f"{today} {time_text}"

                # Валидация даты и времени для БД
                datatime_str = datetime.strptime(datatime, "%Y-%m-%d %H:%M")
                # datatime_valid = datetime.strftime(datatime_str, "%d.%m.%Y %H:%M")

                # Создание полной ссылки на новость
                full_link = urljoin(url, link)

                # Добавляем данные новости
                list_news.append(NewsInfo(
                    topic=None,
                    title=title,
                    created_at=datatime_str,
                    url=full_link,
                    source=NAME_OF_SOURCE[0]
                ))
                
            # Возращаем список новостей 5 штук
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
