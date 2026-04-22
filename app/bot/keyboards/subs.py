from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.bot.config import SubscriptionsCallback

from app.news.config_news import SOURCES

def get_sources_keyboard(selected_sources: set[str]):
    keyboard = InlineKeyboardBuilder()

    for source_code, source_name in SOURCES.items():
        is_selected = source_code in selected_sources
        button_text = f"✅ {source_name}" if is_selected else source_name

        keyboard.button(
            text=button_text,
            callback_data=SubscriptionsCallback(
                action="toggle",
                source=source_code,
            ).pack(),
        )

    keyboard.add(
        InlineKeyboardButton(
            text="Сохранить",
            callback_data=SubscriptionsCallback(action="save").pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=SubscriptionsCallback(action="cancel").pack(),
        )
    )

    return keyboard.adjust(1).as_markup()
