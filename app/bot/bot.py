from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from app.bot.routers import router, HandleManager

import aiogram
import os
import asyncio

load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN'))

dp = Dispatcher()
dp.include_router(router)

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    handle = HandleManager(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print('Бот запущен!')
    asyncio.run(main())