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
            
    async def exists_news_in_database(self, news_info: NewsInfo):
        """
        Проверка есть ли новость в БД
        если новость существует то возращает True
        если новсти нет то сразу же добавляем в БД
        """
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(News)
                    .where(
                        News.title == news_info.title,
                        News.url == news_info.url,
                        News.source == news_info.source
                    )
                )

                exists_news = result.scalar_one_or_none()
                if exists_news is None:
                    await self.add_news(news_info)

                # return None

            except IntegrityError as e:
                logger.error(f"Unique error: {e}")
                return False
            
            except SQLAlchemyError as e:
                logger.error(f"DAtabase error: {e}")
                return False
            
    async def get_news_from_one_source(self, source: str, datatime: datetime):
        """Получаем новости с олного источника в дату"""
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(News.title)
                    .where(
                        News.source == source,
                        News.created_at == datatime
                    )
                    .limit(20)
                    )
                
                exists_news = result.scalars()

                if exists_news:
                    list_news = []
                    for news in result:
                        list_news.append(news)
                    return list_news
                    
                return f"Нет новостей с {source}"

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error receiving news from a source: {e}")
                return None
    
    async def get_last_news_per_source(self):
        """Получаем самую последнюю новость с каждого источника"""
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
        """Получаем последнюю новость с источника"""
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
        
news_repo = NewsRepo()
