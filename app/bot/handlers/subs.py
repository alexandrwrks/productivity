from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.news.config_news import SOURCES
from app.repo.subscription import subs_repo
from app.repo.users import user_repo

from app.bot.config import SubscriptionsState, SubscriptionsCallback
from app.bot.keyboards.subs import get_sources_keyboard



router = Router()

@router.message(Command("subs"))
async def process_command_subs(message: Message, state: FSMContext):
    await user_repo.get_exists_user(message.from_user.id)
    current_sources = await subs_repo.get_sub_source_by_telegram_id(message.from_user.id)
    selected_sources = set(current_sources or [])

    await state.set_state(SubscriptionsState.choosing_sources)
    await state.update_data(selected_sources=list(selected_sources))

    await message.answer(
        text="Выберите источники для подписки:",
        reply_markup=get_sources_keyboard(selected_sources),
    )


@router.callback_query(
    SubscriptionsState.choosing_sources,
    SubscriptionsCallback.filter(F.action == "toggle"),
)
async def toggle_source(
    callback: CallbackQuery,
    callback_data: SubscriptionsCallback,
    state: FSMContext,
):
    data = await state.get_data()
    selected_sources = set(data.get("selected_sources", []))

    source = callback_data.source
    if source is None:
        await callback.answer()
        return

    if source in selected_sources:
        selected_sources.remove(source)
    else:
        selected_sources.add(source)

    await state.update_data(selected_sources=list(selected_sources))
    await callback.message.edit_reply_markup(
        reply_markup=get_sources_keyboard(selected_sources)
    )
    await callback.answer()


@router.callback_query(
    SubscriptionsState.choosing_sources,
    SubscriptionsCallback.filter(F.action == "save"),
)
async def save_sources(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = await state.get_data()
    selected_sources = set(data.get("selected_sources", []))

    telegram_id = callback.from_user.id
    await user_repo.get_exists_user(telegram_id)
    current_sources = set(await subs_repo.get_sub_source_by_telegram_id(telegram_id) or [])

    to_add = selected_sources - current_sources
    to_remove = current_sources - selected_sources

    for source in to_add:
        await subs_repo.create_sub_for_source(telegram_id=telegram_id, source=source)

    for source in to_remove:
        await subs_repo.delete_sub(telegram_id=telegram_id, source=source)

    if selected_sources:
        selected_names = [SOURCES[source] for source in sorted(selected_sources)]
        text = "Подписки сохранены:\n\n" + "\n".join(f"• {name}" for name in selected_names)
    else:
        text = "Вы не выбрали ни одного источника."

    await callback.message.edit_text(text=text)
    await state.clear()
    await callback.answer()


@router.callback_query(
    SubscriptionsState.choosing_sources,
    SubscriptionsCallback.filter(F.action == "cancel"),
)
async def cancel_sources(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    await callback.message.edit_text("Выбор источников отменён.")
    await callback.answer()



