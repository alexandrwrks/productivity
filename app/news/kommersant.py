import asyncio
from datetime import datetime
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from app.news.config_news import NewsInfo

SOURCE = "kommersant"


class KommersantNews:
    async def parsing_kommersant(self) -> list[NewsInfo]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            url = "https://www.kommersant.ru/lenta/news?from=lenta_news"
            response = await client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            news_list = soup.find("div", class_="rubric_lenta")
            if news_list is None:
                return []

            topic_text = None
            topic_list = news_list.find("ul", class_="crumbs tag_list")
            if topic_list is not None:
                topic_li = topic_list.find(
                    "li",
                    class_="crumbs__item tag_list__item tag_list__item--plus",
                )
                if topic_li is not None:
                    topic = topic_li.find("a", class_="tag_list__link")
                    if topic is not None:
                        topic_text = topic.get_text(" ", strip=True)

            news_cards = news_list.find_all("div", class_="uho__text")
            news: list[NewsInfo] = []

            for card in news_cards:
                datatime = card.find("p", class_="uho__tag")
                title = card.find("a", class_="uho__link")

                if datatime is None or title is None:
                    continue

                datatime_text = datatime.get_text(" ", strip=True)
                if ", " not in datatime_text:
                    continue

                date_part, time_part = datatime_text.split(", ", maxsplit=1)
                valid_datatime = datetime.strptime(
                    f"{date_part} {time_part}",
                    "%d.%m.%Y %H:%M",
                )

                title_text = title.get_text(" ", strip=True)
                link = title.get("href")
                if not link:
                    continue

                full_link = urljoin(url, link)
                news.append(
                    NewsInfo(
                        topic=topic_text,
                        title=title_text,
                        url=full_link,
                        created_at=valid_datatime,
                        source=SOURCE,
                    )
                )

            return news


kommersant_news = KommersantNews()


async def main():
    news = await kommersant_news.parsing_kommersant()

    for item in news:
        print(
            f"Заголовок: {item.title}\n"
            f"Ссылка: {item.url}\n"
            f"Дата публикаций: {item.created_at}\n"
            f"Источник: {item.source}\n\n"
        )


if __name__ == "__main__":
    asyncio.run(main())
