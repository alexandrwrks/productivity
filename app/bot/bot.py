from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from handlers import * # ипортировать роутер, и класс для роутера

import aiogram
import os
import asyncio

load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN'))

dp = Dispatcher()
dp.include_router(router='')

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    # handle_manager = класс со всеми хэндлерами
    await dp.start_polling(bot)

if __name__ == "__main__":
    print('Бот запущен!')
    asyncio.run(main())