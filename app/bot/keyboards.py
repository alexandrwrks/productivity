from aiogram import Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

import asyncio

class KeyBoradManager:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def main_keyboard(self, message: Message):

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='📓 Каталог'),
                 KeyboardButton(text='📱 Мои заказы'),
                 KeyboardButton(text='❔ Поддержка')]
            ],
            resize_keyboard=True
        )
        await message.answer('Выберите: ', reply_markup=keyboard)

    async def make_order(self, message: Message):

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='❌ Отменить'),
                 KeyboardButton(text='✅ Подтвердить')]
            ],
            resize_keyboard=True
        )
        
        await message.answer('Подтвердите покупку: ', reply_markup=keyboard)

    async def main_admin_menu(self, message: Message):
        
        keyboard = ReplyKeyboardMarkup(
            keyboard = [
                [KeyboardButton(text='Статистика'),
                 KeyboardButton(text='Добавить товар'),
                 KeyboardButton(text=''),]
            ],
            resize_keyboard=True
        )

        await message.answer('Выберите действие: ', reply_markup=keyboard)
    
    async def create_item(self, message: Message):
        pass

