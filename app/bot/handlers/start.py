from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.news.config_news import NAME_OF_SOURCE

from app.repo.users import user_repo

router = Router()

@router.message(Command("start"))
async def process_command_start(message: Message):
    await user_repo.get_exists_user(message.from_user.id)
    
    await message.answer(
        "Бот предназначен для получения новостей из\n"
        f"источников:    {NAME_OF_SOURCE[0]}, {NAME_OF_SOURCE[1]} и {NAME_OF_SOURCE[2]}\n"
    )