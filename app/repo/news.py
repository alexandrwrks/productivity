from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, desc

from app.database.config_db import SessionLocal, logger
from app.database.models import News
from app.news.config_news import NewsInfo, NAME_OF_SOURCE

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
            
    async def add_news_if_not_exists(self, news_info: NewsInfo):
        async with SessionLocal() as session:
            try:
                result = await session.execute(select(News).where(
                    News.title == news_info.title,
                    News.url == news_info.url,
                    News.source == news_info.source
                ))

                news = result.scalar_one_or_none()
                return news is not None

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Database have this news: {e}")
                return None

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return None
            
    async def get_news_from_one_source(self, source: str, datatime: datetime):
        async with SessionLocal() as session:
            try:
                exists_news = await session.execute(select(News.title).where(
                    News.source == source,
                    News.created_at == datatime
                ))

                result = exists_news.scalar_one_or_none()

                if result is None:
                    return f"Нет новостей с {source}"
                
                list_news = []
                for news in result:
                    list_news.append(news)

                return list_news

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error receiving news from a source: {e}")
                return None
    
    async def get_last_news_per_source(self):
        async with SessionLocal() as session:
            last_news = []

            for source in NAME_OF_SOURCE:
                result = await session.execute(
                    select(News)
                    .where(News.source == source)
                    .order_by(News.id.desc())
                    .limit(1)
                )

                news = result.scalars().first()
                if news is not None:
                    last_news.append(news)

            return last_news

    async def get_last_news_by_source(self, source: str):
        async with SessionLocal() as session:

            result = await session.execute(
                select(News)
                .where(News.source == source)
                .order_by(News.id.desc())
                .limit(1)
            )

            news = result.scalars().first()
            # Сделать обработку на None в другом месте
            return news

    async def add_news_if_not_exists(self, news_info: NewsInfo) -> Optional[News]:
        exists = await self.add_news_if_not_exists(news_info)
        if exists:
            return None
        return await self.add_news(news_info)

news_repo = NewsRepo()
