from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config_db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Первичный ключ
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False) # Уникальный телеграмм id


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Первичный ключ
    topic: Mapped[str | None] = mapped_column(String, nullable=True) # Тема, если указанна
    title: Mapped[str] = mapped_column(String, nullable=False) # Заголовок 
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False) # Ссылка на новость
    source: Mapped[str] = mapped_column(String, nullable=False) # Источник
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False) # Время создания


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint("telegram_id", "source", name="uq_subscription_telegram_source"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Первичный ключ
    telegram_id: Mapped[int] = mapped_column(
        Integer
        , ForeignKey("users.telegram_id")
        , nullable=False) # Внешний ключ привязанный к users.telegram_id
    source: Mapped[str] = mapped_column(String, nullable=False) # Источник

