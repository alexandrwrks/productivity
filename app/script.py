import asyncio
import time
from sqlalchemy import func, select

from app.database.config_db import SessionLocal, engine
from app.database.models import Base, News, User
from app.news.kommersant import parsing_kommersant
from app.repo.users import UserRepo


async def ensure_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def print_table_stats(stage: str) -> None:
    async with SessionLocal() as session:
        users_count = await session.scalar(select(func.count()).select_from(User))
        news_count = await session.scalar(select(func.count()).select_from(News))

    print(f"[{stage}] users={users_count}, news={news_count}")


async def main() -> None:
    await ensure_tables()
    await print_table_stats("before")

    # Create a unique test telegram_id on each run.
    test_telegram_id = int(time.time())
    user_repo = UserRepo()
    user = await user_repo.add_user(test_telegram_id)
    if user is None:
        print("User was not created (possibly duplicate or DB error).")
    else:
        print(f"Inserted test user: telegram_id={user.telegram_id}")

    parsed_news = await parsing_kommersant()
    if not parsed_news:
        print("No news parsed from kommersant.")
    else:
        print(f"Parsed from kommersant: {len(parsed_news)} news items")

    await print_table_stats("after")

    async with SessionLocal() as session:
        latest_news = await session.execute(
            select(News).where(News.source == "kommersant").order_by(News.id.desc()).limit(3)
        )
        rows = latest_news.scalars().all()

    if rows:
        print("Latest news rows:")
        for row in rows:
            print(f"- id={row.id} source={row.source} title={row.title[:80]}")
    else:
        print("No rows in news table for source=kommersant")


if __name__ == "__main__":
    asyncio.run(main())
