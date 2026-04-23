from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config_db import SessionLocal, logger
from app.database.models import Sources, Subscriptions
from app.news.config_news import SOURCE_LINK, SOURCES


class SubscriptionRepo:
    async def _get_or_create_source(self, session, source_code: str) -> Sources | None:
        async with SessionLocal() as session:
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

    async def get_sub_source_by_telegram_id(self, telegram_id: int) -> list[str]:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(Sources.type)
                    .join(Subscriptions, Subscriptions.source_id == Sources.id)
                    .where(
                        Subscriptions.telegram_id == telegram_id,
                        Subscriptions.is_active.is_(True),
                    )
                )
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                logger.error(f"Get subscriptions error: {e}")
                return []

    async def get_active_user_ids_by_source(self, source: str) -> list[int]:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(Subscriptions.telegram_id)
                    .join(Sources, Sources.id == Subscriptions.source_id)
                    .where(
                        Sources.type == source,
                        Subscriptions.is_active.is_(True),
                    )
                )
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                logger.error(f"Get users by source error: {e}")
                return []

    async def create_sub_for_source(self, telegram_id: int, source: str) -> Optional[Subscriptions]:
        async with SessionLocal() as session:
            try:
                source_obj = await self._get_or_create_source(session, source)
                if source_obj is None:
                    await session.rollback()
                    return None

                existing_result = await session.execute(
                    select(Subscriptions).where(
                        Subscriptions.telegram_id == telegram_id,
                        Subscriptions.source_id == source_obj.id,
                    )
                )
                existing = existing_result.scalar_one_or_none()

                if existing is not None:
                    existing.is_active = True
                    await session.commit()
                    await session.refresh(existing)
                    return existing

                sub = Subscriptions(
                    telegram_id=telegram_id,
                    source_id=source_obj.id,
                    is_active=True,
                )
                session.add(sub)
                await session.commit()
                await session.refresh(sub)
                return sub

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Sub unique error: {e}")
                return None
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return None

    async def delete_sub(self, telegram_id: int, source: str) -> bool:
        async with SessionLocal() as session:
            try:
                source_result = await session.execute(
                    select(Sources).where(Sources.type == source)
                )
                source_obj = source_result.scalar_one_or_none()
                if source_obj is None:
                    return True

                await session.execute(
                    update(Subscriptions)
                    .where(
                        Subscriptions.telegram_id == telegram_id,
                        Subscriptions.source_id == source_obj.id,
                    )
                    .values(is_active=False)
                )

                await session.commit()
                return True

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return False


subs_repo = SubscriptionRepo()

