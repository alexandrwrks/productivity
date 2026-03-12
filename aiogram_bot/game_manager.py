from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

class GameManager:
    """
    Создание клавиатуры в ТГ боте. Начало работы игры: случайный выбор игрока и бота.
    Функцонал победы и проигрыша.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.CHOICES = ['Камень', 'Ножницы', 'Бумага']
        self.WIN_COMBINATIONS = [
            ('Камень', 'Ножницы'),
            ('Ножницы', 'Бумага'),
            ('Бумага', 'Камень')
        ]

    # Добавление клавиутры для игры
    async def start_game(self, message: Message):

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Камень"),
                 KeyboardButton(text="Ножницы"), 
                 KeyboardButton(text="Бумага")]
            ],
            resize_keyboard=True
        )
        await message.answer('Выберите: ', reply_markup=keyboard)

    # Логика игры
    async def game(self, message: Message):
        if not message.text:
            await message.answer("Пожалуйста используйте кнопки для игры")
            return

        user_choice = message.text
        if user_choice not in self.CHOICES:
            # ИСПРАВЛЕНО: здесь тоже нужно использовать KeyboardButton
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Камень"),
                    KeyboardButton(text="Ножницы"), 
                    KeyboardButton(text="Бумага")]
                ],
                resize_keyboard=True
            )
            await message.answer(
                "Пожалуйста, выберите один из вариантов на клавиатуре:",
                reply_markup=keyboard
            )
            return 
        
        bot_choice = random.choice(self.CHOICES)
        await message.answer(f"Бот выбрал: **{bot_choice}**", parse_mode="Markdown")

        if user_choice == bot_choice:
            result = 'Ничья!'
        elif (user_choice, bot_choice) in self.WIN_COMBINATIONS:
            result = 'Вы выиграли!'
        else:
            result = 'Вы проиграли!'
        
        await message.answer(result)

        # ИСПРАВЛЕНО: клавиатура после игры с KeyboardButton
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Играть снова'),
                KeyboardButton(text='Главное меню')]
            ],
            resize_keyboard=True
        )

        await message.answer('Хотите сыграть снова?', reply_markup=keyboard)