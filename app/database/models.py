from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config_db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Первичный ключ
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False) # Уникальный телеграмм id


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Первичный ключ
    topic: Mapped[str] = mapped_column(String) # Тема, если указанна
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False) # Заголовок 
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False) # Ссылка на новость
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP) # Время создания
    source: Mapped[str] = mapped_column(String) # Источник


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Первичный ключ
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id")) # Внешний ключ привязанный к users.telegram_id
    source: Mapped[str] = mapped_column(String) # Источник


