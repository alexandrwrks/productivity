from aiogram import Bot, Dispatcher
from bot_token import BOT_TOKEN
from routers import router, HandleManager

import asyncio
import aiogram

dp = Dispatcher()
dp.include_router(router)

async def main():
    bot = Bot(token=BOT_TOKEN)
    HM = HandleManager(bot)
    await dp.start_polling(bot)

"""
HandleManager(BOT_TOKEN), почле этого бот токен передйёт на другие классы
"""

if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())