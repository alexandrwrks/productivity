from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from calories_manager import CaloriesManager
from reminder_manager import ReminderManager
from game_manager import GameManager
from help_manager import HelpManager
from menu_manager import MenuManager

router = Router()

class HandleManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.CALORIES = CaloriesManager(self.bot)
        self.REMIND = ReminderManager(self.bot)
        self.GAME = GameManager(self.bot)
        self.HELP = HelpManager(self.bot)
        self.MENU = MenuManager(self.bot)
        self.setup_handlers()

    def setup_handlers(self):

        @router.message(Command("start"))
        async def handle_start(message: Message):
            await self.MENU.main_menu(message)
        
        @router.message(Command('remind'))
        async def handle_remind(message: Message):
            await self.REMIND.remind(message)

        @router.message(Command('game'))
        async def handle_game(message: Message):
            await self.GAME.start_game(message)
        

        @router.message(Command("help"))
        async def help(message: Message):
            await self.HELP.command_help(message)

        @router.message(Command("calories"))
        async def calories_handle(message: Message):
            await self.CALORIES.parcing_text(message)
        
        @router.message()
        async def handle_all_message(message: Message):
            if message.text == 'Игра':
                await message.answer('Вы выбрали игру!')
                await self.GAME.start_game(message)
            elif message.text == 'Напоминалка':
                await message.answer('Вы выбрали напоминалку!')
                await message.answer(
                    "Введите напоминание в формате:\n\n/remind [минуты] [текст]\n\n" \
                    "Пример: /remind 5 Позвонить маме"
                    )
            
            elif message.text == 'Счётчик калорий':
                await message.answer('Вы выбрали счётчик калорий')
                await message.answer(
                    "Введите счётчик в формате:\n\n/calories [продукт] [грам]\n\n" \
                    "Пример: /calories макароны 150"
                    )
            
            elif message.text == 'Помощь':
                await self.HELP.comand_help(message)

            elif message.text == 'Главное меню':
                await self.MENU.main_menu(message)
            
            elif message.text == 'Играть снова':
                await self.GAME.start_game(message)

            elif message.text == 'Отчёт за день':
                await self.CALORIES.send_daily_calories(message)
            
            elif message.text == 'Удалить все напоминания':
                await self.REMIND.cancel_all_reminders(message)

            elif message.text in ['Камень', 'Ножницы', 'Бумага']:
                await self.GAME.game(message)
            
            else:
                await message.answer("Пожалуйста, выберите пункт из меню.")

