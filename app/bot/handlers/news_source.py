from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("new_sources"))
async def get_news_sources(message: Message):

    await message.answer(
        f"Источники новостей: <b>vtomske</b>",
        parse_mode="HTML"
    )