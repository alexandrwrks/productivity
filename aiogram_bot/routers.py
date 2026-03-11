from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from calories_manager import CaloriesManager
from reminder_manager import ReminderManager

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

        # @router.message(Command())
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

        # @router.message(Command("about"))
        # async def start(message: Message):
        #     await message.answer(f"Твоё имя: {message.from_user.first_name}")
        
        @router.message()
        async def handle_all_message(message: Message):
            if message.text == 'Игра':




