from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config_db import SessionLocal, logger
from app.database.models import User


class UserRepo:
    def __init__(self):
        pass

    async def add_user(self, telegram_id: int) -> Optional[User]:
        async with SessionLocal() as session:
            try:
                new_user = User(telegram_id=telegram_id)
                session.add(new_user)

                await session.commit()
                await session.refresh(new_user)

                return new_user
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"User unique error: {e}")
                return None
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                return None

    async def get_exists_user(self, telegram_id: int) -> Optional[User]:
        """Проверка наличия пользователя в БД"""
        async with SessionLocal() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            exists_user = result.scalar_one_or_none()

            if exists_user is None:
                await self.add_user(telegram_id)

            return

user_repo = UserRepo()