import asyncio
import os

from aiogram import Bot, Dispatcher
from app.bot.handlers import routers

from app.script import run_all

from dotenv import load_dotenv

load_dotenv()

async def main():
    token = os.getenv('BOT_TOKEN')
    
    bot = Bot(token)
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    print(f"Бот успешно запущен!")

    await asyncio.gather(
        dp.start_polling(bot),
        run_all()
    )


if __name__ == "__main__":
    asyncio.run(main())