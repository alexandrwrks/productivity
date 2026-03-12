from aiogram import Bot
from aiogram.types import Message

class HelpManager:
    """
    Парсинг помощи, казывает на функции которые есть в боте
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        
    async def comand_help(self, message: Message):
        
        help_text = f"Для чего нужен этот бот\n\n" \
                    f"/start - для стрта бота\n"\
                    f"/remind - напоминалка\n" \
                    f"/game - игра камень, ножницы, бумага\n\n" \
                    f"Выберите что хотите сделать" \
                    
        await message.answer(help_text)