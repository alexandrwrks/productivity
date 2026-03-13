from dotenv import load_dotenv
from aiogram import Dispatcher, Bot, Router

import aiogram
import os

load_dotenv()
print(os.getenv('BOT_TOKEN'))
print(os.getenv('ADMIN_IDS'))

dp = Dispatcher()



