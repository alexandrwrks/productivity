from aiogram import Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

import asyncio

class KeyBoardManager:
    """Класс олько для создания клавиатур"""

    @staticmethod
    def get_start_keyboard():
        """Возращает стартовую клавиатуру для регистрации"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='💾 Закончить регистрацию')]
            ],
            resize_keyboard=True
        )

    @staticmethod
    def main_keyboard():

        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='📓 Каталог'),
                 KeyboardButton(text='📱 Мои заказы'),
                 KeyboardButton(text='❔ Поддержка')]
            ],
            resize_keyboard=True
        )


    def make_order(self):
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='❌ Отменить'),
                 KeyboardButton(text='✅ Подтвердить')]
            ],
            resize_keyboard=True
        )
        

    async def main_admin_menu():
        
        keyboard = ReplyKeyboardMarkup(
            keyboard = [
                [KeyboardButton(text='Статистика'),
                 KeyboardButton(text='Добавить товар'),
                 KeyboardButton(text=''),]
            ],
            resize_keyboard=True
        )

    
    async def create_item(self, message: Message):
        pass

