from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def process_command_start(message: Message):
    await message.answer("""
                         Бот прдназначен для получения новостей\n
                         с таких источников как Bloomberd и Kommersant\n
    """)