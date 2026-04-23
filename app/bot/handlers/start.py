from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.news.config_news import SOURCES
from app.repo.users import user_repo

router = Router()


@router.message(Command("start"))
async def process_command_start(message: Message):
    await user_repo.get_exists_user(message.from_user.id)

    source_names = ", ".join(SOURCES.values())
    await message.answer(
        "Бот присылает новости из источников:\n"
        f"{source_names}\n\n"
        "Команда /subs - выбрать подписки"
    )

