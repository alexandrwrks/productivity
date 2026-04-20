from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.repo.news import news_repo

router = Router()


@router.message(Command("news"))
async def process_command_news(message: Message):
    last_news_from_all_source = await news_repo.get_last_news_per_source()

    if last_news_from_all_source is None:
        await message.answer("Новости сейчас недоступны, попробуйте позже.")
        return

    for news_info in last_news_from_all_source:
        await news_repo.exists_news_in_database(news_info)

        await message.answer(
            f"<a href=\"{news_info.url}\"><b>{news_info.title}</b></a>\n\n"
            f"Тема: {news_info.topic}\n"
            f"🕐 Время: {news_info.created_at}\n"
            f"🌐 Источник: {news_info.source}\n\n",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
