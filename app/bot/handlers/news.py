from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.news.vtomske import process_vtomske
from app.repo.news import news_repo

router = Router()


@router.message(Command("news"))
async def process_command_news(message: Message):
    news_info = await process_vtomske()

    if news_info is None:
        await message.answer("Новости сейчас недоступны, попробуйте позже.")
        return

    await news_repo.add_news(news_info)

    await message.answer(
        f"<b>{news_info.title}</b>\n\n"
        f"🕐 Время: {news_info.time}\n"
        f"🌐 Источник: {news_info.source}\n\n"
        f"<a href=\"{news_info.url}\">Открыть новость</a>",
        parse_mode="HTML",
    )
