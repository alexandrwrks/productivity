from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.news.config_news import NAME_OF_SOURCE, LINK_OF_SOURCE

router = Router()

@router.message(Command("sources"))
async def get_news_sources(message: Message):

    print("Декоратор на команду sources")

    await message.answer(
        f"<b><a href=\"{LINK_OF_SOURCE[0]}\">{NAME_OF_SOURCE}</a></b>\n",
        parse_mode="HTML"
    )