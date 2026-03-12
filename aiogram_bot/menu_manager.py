from aiogram.types import Message
from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MenuManager:
    """
    Главное меню.
    Главное меню. Игра. Напоминалка. Помощь. 
    Обработка сообщений для каждого пункта меню.
    Обработка функций для каждой функции меню.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
    # Добавление клавиатуры
    async def main_menu(self, message: Message):

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Игра'), 
                 KeyboardButton(text='Напоминалка'), 
                 KeyboardButton(text='Помощь')],
                [KeyboardButton(text='Счётчик калорий'), 
                 KeyboardButton(text='Отчёт за день'), 
                 KeyboardButton(text='Удалить все напоминания')]
            ],
            resize_keyboard=True,
            input_field_placeholder="Выберите действие..."
        )
        await message.answer('Главное меню:', reply_markup=keyboard)
