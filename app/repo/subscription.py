from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config_db import SessionLocal, logger
from app.database.models import Subscriptions
from app.repo.news import news_repo

from app.news.config_news import SOURCES

from app.bot.config import SubscriptionsSources

class SubscriptionRepo:
    def __init__(self):
        pass

    async def create_sub_for_source(self, telegram_id: int, source: str) -> Optional[Subscriptions]:
        async with SessionLocal() as session:
            try:
                sub = Subscriptions(
                    telegram_id=telegram_id,
                    source=source,
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

    async def add_sub(self, telegram_id: int, source: str):
        async with SessionLocal() as session:
            return


    async def delete_sub(self, telegram_id: int, source: str) -> bool:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    delete(Subscriptions).where(
                        Subscriptions.telegram_id == telegram_id,
                        Subscriptions.source == source,
                    )
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
                select(Subscriptions.telegram_id).where(Subscriptions.source == source)
            )
            users = result.scalars().all()

        return {
            "news": last_news,
            "users": users,
        }

    async def get_users_by_source(self, source: str):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Subscriptions.telegram_id).where(Subscriptions.source == source)
            )
            return result.scalars().all()

    async def get_sub_source_by_telegram_id(self, telegram_id: int) -> list[str]:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(Subscriptions.source).where(
                        Subscriptions.telegram_id == telegram_id
                    )
                )
                return result.scalars().all()

            except SQLAlchemyError as e:
                logger.exception(f"Database error: {e}")
                return []

    async def preparing_subs(
            self,
            sources: SubscriptionsSources,
            telegram_id: int
        ):
        async with SessionLocal() as session:
            try:
                for source in sources:
                    if source == True:
                        await self.add_sub(source, telegram_id)
                    else:
                        await self.delete_sub(source, telegram_id)

                return True
            
            except SQLAlchemyError as e:
                logger.exception(f"Database error: {e}")
                return False
            
            except Exception as e:
                logger.exception(f"Exceptions: {e}")
                return False



subs_repo = SubscriptionRepo()
