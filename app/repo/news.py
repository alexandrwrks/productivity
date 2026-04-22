from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config_db import SessionLocal, logger
from app.database.models import News
from app.news.config_news import NAME_OF_SOURCE, NewsInfo


class NewsRepo:
    def __init__(self):
        pass

    async def add_news(self, news_info: NewsInfo) -> Optional[News]:
        async with SessionLocal() as session:
            try:
                news = News(
                    topic=news_info.topic,
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

    async def exists_news_in_database(self, news_info: NewsInfo) -> bool:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(News).where(
                        News.title == news_info.title,
                        News.url == news_info.url,
                        News.source == news_info.source,
                    )
                )
                exists_news = result.scalar_one_or_none()

                if exists_news is not None:
                    return True

                return (await self.add_news(news_info)) is not None

            except IntegrityError as e:
                logger.error(f"Unique error: {e}")
                return False

            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                return False

    async def get_news_from_one_source(self, source: str, datatime: datetime):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(News)
                    .where(News.source == source, News.created_at == datatime)
                    .limit(20)
                )
                return result.scalars().all()

            except SQLAlchemyError as e:
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

            return result.scalars().first()


news_repo = NewsRepo()
