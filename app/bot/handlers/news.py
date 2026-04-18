from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.news.vtomske import parsing_vtomske
from app.repo.news import news_repo

router = Router()


@router.message(Command("news"))
async def process_command_news(message: Message):
    list_news = await parsing_vtomske()

    if list_news is None:
        await message.answer("Новости сейчас недоступны, попробуйте позже.")
        return

    for news in list_news:
        await news_repo.add_news(news)

        await message.answer(
            f"<a href=\"{news.url}\"><b>{news.title}</b></a>\n\n"
            f"🕐 Время: {news.created_at}\n"
            f"🌐 Источник: {news.source}\n\n",
            parse_mode="HTML",
        )
