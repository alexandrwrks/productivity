from aiogram.filters import Command
from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.repo.subscription import subs_repo
from app.news.config_news import SOURCES

router = Router()

class SubscriptionsCallback(CallbackData, prefix="subsrc"):
    action: str
    source: str | None = None


class SubscriptionsState(StatesGroup):
    choosing_sources = State()

@router.message(Command("subs"))
async def process_command_subs(message: Message, state: FSMContext):
    selecte_sources = set()

    await state.set_state(SubscriptionsState.choosing_sources)
    await state.update_data(selecte_sources=list(selecte_sources))

    await message.answer(
        text="Выберите источники для подписки: ",
        reply_markup=get_sources_keyboard(selecte_sources)
    )

@router.callback_query(
    SubscriptionsState.choosing_sources,
    SubscriptionsCallback.filter(F.action == "toggle")
)
async def toggle_source(
    callback: CallbackQuery,
    callback_data: SubscriptionsCallback,
    state: FSMContext
):
    data = await state.get_data()
    selected_sources = set(data.get("selected_sources", []))

    source =callback_data.source

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
    SubscriptionsCallback.filter(F.action == "save")
)
async def save_sources(
    callback: CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()
    selected_sources = set(data.get("selected_sources", []))

    # Добавить сохранение в БД

    if selected_sources:
        selected_names = [SOURCES[source] for source in selected_sources]
        text="Подписки сохранены:\n\n" + "\n".join(f"• {name}" for name in selected_names)
    else:
        text = "Вы не выбрали ни одного исчтоника."

    await callback.message.edit_text(text=text)
    await state.clear()
    await callback.answer()

@router.callback_query(
    SubscriptionsState.choosing_sources,
    SubscriptionsCallback.filter(F.action == "cancel")
)
async def cancel_sources(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()
    await callback.message.edit_text("Выбор источников отменён.")
    await callback.answer()



from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.news.config_news import NAME_OF_SOURCE, SOURCES

from app.bot.handlers.subs import SubscriptionsCallback

SOURCE_BUTTON = {
    NAME_OF_SOURCE[0]: f"{NAME_OF_SOURCE[0]}_btn"
    , NAME_OF_SOURCE[1]: f"{NAME_OF_SOURCE[1]}_btn"
    , NAME_OF_SOURCE[2]: f"{NAME_OF_SOURCE[2]}_btn"
}

def get_new_sub_for_source():

    keyboard = InlineKeyboardBuilder()

    for name, callback in SOURCE_BUTTON.items():
        keyboard.add(InlineKeyboardButton(text=name, callback_data=callback))


    return keyboard.adjust(1).as_markup()


def get_sources_keyboard(selected_sources: set[str]):
    keyboard = InlineKeyboardBuilder()

    for source_code, source_name in SOURCES.items():
        is_selected = source_code in selected_sources
        button_text = f"✅ {source_name}" if is_selected else source_name

        keyboard.button(
            text=button_text,
            callback_data=SubscriptionsCallback(
                action="toggle",
                source=source_code
            ).pack()
        )

    keyboard.button(
        text="Сохранить",
        callback_data=SubscriptionsCallback(
            action="save",
        ).pack()
    )

    keyboard.button(
        text="Отмена",
        callback_data=SubscriptionsCallback(
            action="cancel"
        ).pack()
    )

    return keyboard.adjust(1, 1, 1, 2).as_markup()