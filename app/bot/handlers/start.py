from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.news.config_news import NAME_OF_SOURCE

router = Router()

@router.message(Command("start"))
async def process_command_start(message: Message):
    await message.answer(
        "Бот прдназначен для получения новостей\n"
        f"с таких источников как {NAME_OF_SOURCE[0]}, {NAME_OF_SOURCE[1]} и {NAME_OF_SOURCE[2]}\n"
    )