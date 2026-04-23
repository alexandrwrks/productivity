from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.news.config_news import SOURCE_LINK, SOURCES

router = Router()


@router.message(Command("sources"))
async def get_news_sources(message: Message):
    lines = []
    for code, name in SOURCES.items():
        lines.append(f"<b><a href=\"{SOURCE_LINK[code]}\">{name}</a></b>")

    await message.answer("\n".join(lines), parse_mode="HTML")

