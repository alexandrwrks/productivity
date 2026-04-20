from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.news.config_news import NAME_OF_SOURCE

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