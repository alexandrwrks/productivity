from dotenv import load_dotenv

import logging
import aiosqlite
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

class BaseREpository:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
    
    async def _get_connection(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:

                cursor = db.cursor()

        except aiosqlite.Error as e:
            logging.error(f"Ошибка подключения к БД")


    async def _execute_transaction(self): 
        """Шаблон для транзакций и уменьшения повторений"""
        pass 