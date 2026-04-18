from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.repo.subscription import subs_repo

from app.bot.keyboards.subs import get_new_sub_for_source

router = Router()

@router.message(Command("subs"))
async def process_command_subs(message: Message):
    telegram_id = message.from_user.id
    sub_source = await subs_repo.get_sub_source_by_telegram_id(telegram_id)

    if sub_source is None:
        await message.answer(
            f"У Вас нет активных подписок на источники",
            reply_markup=get_new_sub_for_source()
        )

    sources = ", ".join(sub_source)
    await message.answer(
        text=f"Источники: {sources}"
    )


    