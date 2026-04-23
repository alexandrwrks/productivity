from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.database.config_db import SessionLocal, logger
from app.database.models import News, Sources
from app.news.config_news import SOURCE_LINK, SOURCES, NewsInfo


class NewsRepo:
    async def _get_or_create_source(self, session, source_code: str) -> Sources | None:
        try:
            result = await session.execute(
                select(Sources).where(Sources.type == source_code)
            )
            source = result.scalar_one_or_none()
            if source is not None:
                return source

            source = Sources(
                name=SOURCES.get(source_code, source_code),
                type=source_code,
                config=SOURCE_LINK.get(source_code, ""),
            )
            session.add(source)
            await session.flush()
            return source
        except SQLAlchemyError as e:
            logger.error(f"Source create/get error: {e}")
            return None

    async def add_news(self, news_info: NewsInfo) -> Optional[News]:
        async with SessionLocal() as session:
            try:
                source = await self._get_or_create_source(session, news_info.source)
                if source is None:
                    await session.rollback()
                    return None

                news = News(
                    topic=news_info.topic,
                    title=news_info.title,
                    url=news_info.url,
                    created_at=news_info.created_at,
                    source_id=source.id,
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
                source = await self._get_or_create_source(session, news_info.source)
                if source is None:
                    await session.rollback()
                    return False

                result = await session.execute(
                    select(News).where(
                        News.title == news_info.title,
                        News.url == news_info.url,
                        News.source_id == source.id,
                    )
                )
                exists_news = result.scalar_one_or_none()

                if exists_news is not None:
                    return False

                news = News(
                    topic=news_info.topic,
                    title=news_info.title,
                    url=news_info.url,
                    created_at=news_info.created_at,
                    source_id=source.id,
                )
                session.add(news)
                await session.commit()
                return True

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Unique error: {e}")
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return False

    async def get_news_from_one_source(self, source: str, datatime: datetime):
        async with SessionLocal() as session:
            try:
                source_result = await session.execute(
                    select(Sources).where(Sources.type == source)
                )
                source_obj = source_result.scalar_one_or_none()
                if source_obj is None:
                    return []

                result = await session.execute(
                    select(News)
                    .options(selectinload(News.source_rel))
                    .where(News.source_id == source_obj.id, News.created_at == datatime)
                    .limit(20)
                )
                return result.scalars().all()

            except SQLAlchemyError as e:
                logger.error(f"Error receiving news from a source: {e}")
                return None

    async def get_last_news_per_source(self):
        async with SessionLocal() as session:
            last_news = []

            for source_code in SOURCES.keys():
                source_result = await session.execute(
                    select(Sources).where(Sources.type == source_code)
                )
                source_obj = source_result.scalar_one_or_none()
                if source_obj is None:
                    continue

                result = await session.execute(
                    select(News)
                    .options(selectinload(News.source_rel))
                    .where(News.source_id == source_obj.id)
                    .order_by(News.id.desc())
                    .limit(1)
                )

                news = result.scalars().first()
                if news is not None:
                    last_news.append(news)

            return last_news

    async def get_last_news_by_source(self, source: str):
        async with SessionLocal() as session:
            source_result = await session.execute(
                select(Sources).where(Sources.type == source)
            )
            source_obj = source_result.scalar_one_or_none()
            if source_obj is None:
                return None

            result = await session.execute(
                select(News)
                .options(selectinload(News.source_rel))
                .where(News.source_id == source_obj.id)
                .order_by(News.id.desc())
                .limit(1)
            )

            return result.scalars().first()


news_repo = NewsRepo()

