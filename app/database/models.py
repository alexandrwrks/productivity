from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config_db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    time: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    source: Mapped[str] = mapped_column(String)


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"))
    source: Mapped[str] = mapped_column(String)


