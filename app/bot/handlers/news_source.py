from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.news.config_news import SOURCE

router = Router()

@router.message(Command("sources"))
async def get_news_sources(message: Message):

    print("Декоратор на команду sources")

    await message.answer(
        f"<b><a href=\"{SOURCE[0]}\">{SOURCE['vtomske']}</a></b>\n",
        parse_mode="HTML"
    )