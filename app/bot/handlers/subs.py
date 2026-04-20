from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.repo.subscription import subs_repo
from app.news.config_news import NAME_OF_SOURCE

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
        return

    sources = ", ".join(sub_source)
    await message.answer(
        text=f"Источники: {sources}"
    )


@router.callback_query()
async def process_btn_vtomske(callback: CallbackQuery):
    pass

    