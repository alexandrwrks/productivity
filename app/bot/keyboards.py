from aiogram import Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

import asyncio

class KeyBoardManager:
    """Класс только для создания клавиатур"""

    @staticmethod
    def get_reg_keyboard():
        """Возращаем клавтуру для начала реигстрации"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='📓 Начать регистрацию')]
            ],
            resize_keyboard=True
        )
    
    @staticmethod
    def main_keyboard():
        """Основная клавиатура"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='📓 Каталог'),
                 KeyboardButton(text='📱 Мои заказы'),
                 KeyboardButton(text='❔Помощь')]
            ],
            resize_keyboard=True
        )

    @staticmethod
    def make_order():
        """Возращате клавиатуру с подтверждением создания товара"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='❌ Отменить'),
                 KeyboardButton(text='✅ Подтвердить')]
            ],
            resize_keyboard=True
        )
        
    @staticmethod
    async def main_admin_menu():
        """Возращает меню вдмина/админку"""
        return ReplyKeyboardMarkup(
            keyboard = [
                [KeyboardButton(text='💾 Статистика'),
                 KeyboardButton(text='✅ Добавить товар'),
                 KeyboardButton(text='❌ Убрать товар'),] # Выводиться список товаров от этого ползователя с кнопкой удаления товаров на каждой карточке
            ],
            resize_keyboard=True
        )
    
    @staticmethod
    async def create_item():
        pass
    
    @staticmethod
    async def help_menu():
        """Возращает клавиатуру для """
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='📖 Основные функции бота'),
                 KeyboardButton(text='📄 Написать в поддержку')]
            ]
        )

        