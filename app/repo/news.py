from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select

from app.database.config_db import SessionLocal, logger
from app.database.models import News
from app.news.config import NewsInfo

from datetime import datetime

class NewsRepo:
    def __init__(self):
        pass

    async def add_news(self, news_info: NewsInfo) -> Optional[News]:
        """
        Добавление новостей в базу данных
        *args -> умеет данные нужные для добавления новости в базу данных

        """
        async with SessionLocal() as session:
            try:
                news = News(
                    title=news_info.title,
                    url=news_info.url,
                    created_at=news_info.created_at,
                    source=news_info.source,
                )

                session.add(news)
                await session.commit()
                await session.refresh(news)

                return news
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Unique error: {e}")
                return None
            
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return None
            
    async def exists_news_in_data_base(self, news_info: NewsInfo):
        async with SessionLocal() as session:
            try:
                exists_news = await session.execute(select(News).where(
                    News.title == news_info.title,
                    News.url == news_info.url,
                    News.source == news_info.source
                ))

                result = exists_news.scalar_one_or_none()

                if result is None:
                    await self.add_news()

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Database have this news: {e}")
                return None

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return None
            
    async def get_news_from_one_source_(self, name_source: str, datatime: datetime):
        async with SessionLocal() as session:
            try:
                exists_news = await session.execute(select(News.title).where(
                    News.source == name_source,
                    News.created_at == datatime
                ))

                result = exists_news.scalar_one_or_none()

                if result is None:
                    return f"Нет новостей с {name_source}"
                
                list_news = []
                for news in result:
                    list_news.append(news)

                return list_news

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error receiving news from a source: {e}")
                return None
    

news_repo = NewsRepo()
