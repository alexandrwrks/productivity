from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, desc, delete

from app.database.config_db import SessionLocal, logger
from app.database.models import Subscriptions
from app.news.config_news import NewsInfo, NAME_OF_SOURCE

from app.repo.news import news_repo

from datetime import datetime

class SubscriptionRepo:
    def __init__(self):
        pass

    async def create_sub_for_source(self, telegram_id: int, source: str) -> Optional[Subscriptions]:
        async with SessionLocal() as session:
            try:
                
                sub = Subscriptions(
                    telegram_id=telegram_id,
                    source=source
                )

                session.add(sub)
                await session.commit()
                await session.refresh(sub)

                return sub

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Unique error: {e}")
                return None
            
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return None
            
    async def delete_sub(self, telegram_id: int, source: str) -> bool:
        """
        *args
        telegram_id - уникальный id из телеграмм
        source - источник который нужно удалить
        """
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    delete(Subscriptions)
                    .where(
                        Subscriptions.telegram_id == telegram_id,
                        Subscriptions.source == source)
                )

                await session.commit()
                return result.rowcount > 0

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return False
    
    async def get_news_by_sub(self, source: str):
        last_news = await news_repo.get_last_news_by_source(source)
        if last_news is None:
            return False
        async with SessionLocal() as session:
            result = await session.execute(
                select(Subscriptions.telegram_id)
                .where(Subscriptions.source == source)
            )
            users = result.scalars().all()

        return {
            "news": last_news,
            "users": users
        }
    
    async def get_users_by_source(self, source: str):
        """Получение ТГ id по источнику"""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Subscriptions.telegram_id)
                .where(Subscriptions.source == source)
            )
            return result.scalars().all()
        
    async def get_sub_source_by_telegram_id(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(Subscriptions.source)
                    .where(
                        Subscriptions.telegram_id == telegram_id
                    )
                )

                sub_source = result.scalar_one_or_none()
                if sub_source is not None:
                    return sub_source
                
                return None

            except SQLAlchemyError as e:
                logger.exception(f"Database error: {e}")
                return False
        
subs_repo = SubscriptionRepo()