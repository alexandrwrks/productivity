from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, TIMESTAMP, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config_db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class Sources(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    config: Mapped[str] = mapped_column(String, nullable=False)


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    source_rel: Mapped[Sources] = relationship("Sources")

    @property
    def source(self) -> str | None:
        return self.source_rel.type if self.source_rel else None


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint("telegram_id", "source_id", name="uq_subscription_telegram_source"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    source_rel: Mapped[Sources] = relationship("Sources")


class NewsDelivery(Base):
    __tablename__ = "news_delivery"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"))
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey("news.id"))
    status: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    send_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

