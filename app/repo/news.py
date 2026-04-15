from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config_db import SessionLocal, logger
from app.database.models import News
from app.news.config import NewsInfo


class NewsRepo:
    def __init__(self):
        pass

    async def add_news(self, news_info: NewsInfo) -> Optional[News]:
        async with SessionLocal() as session:
            try:
                news = News(
                    title=news_info.title,
                    url=news_info.url,
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


news_repo = NewsRepo()
