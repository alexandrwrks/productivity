from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_choose_source():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Kommersant", callback_data="kommersant_btn")
    keyboard.button(text="Bloomberg", callback_data="Bloomberg_btn")
    keyboard.button(text="Vtomske", callback_data="vtomske_btn")

    return keyboard.adjust(2).as_markup()