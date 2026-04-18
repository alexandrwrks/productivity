from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.news.config_news import NAME_OF_SOURCE

def get_new_sub_for_source():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=f"{NAME_OF_SOURCE[0]}", callback_data="sub_vtomske")

    return keyboard.adjust(1).as_markup()