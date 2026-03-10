import asyncio
import sqlite3
import uvicorn

import telebot

from bot_token import BOT_TOKEN

# BOT_TOKEN = telebot(BOT_TOKEN)

class DataManager:
    def __init__(self, db_name = "my_database.db"):
        self.db_name = db_name
        
    def init_data_base(self):

        connection = None 
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TUsers (
                    user_id INTEGER,
                    name TEXT NOT NULL
                    )
                ''')
            
            connection.commit()
            print(f"Инициализированна таблица TUsers в базе данных {self.db_name}")
        except sqlite3.Error as e:
            print(f"❌ Ошибка инициализации базы данных {self.db_name}")
        finally:
            if connection:
                connection.close()

    async def add_to_data_base(self, user_data):
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            user_id, name = user_data
            cursor.execute('''
                INSERT INTO TUsers (user_id, name)
                    VALUES (?, ?)
                ''', (user_id, name))   
            
            connection.commit()
            print(f"Добавлен пользователь: {name} ind {user_id}")
        except sqlite3.Error as e:
            print(f"❌ Ошибка добавления пользователя: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()


async def main():
    db = DataManager()
    db.init_data_base()
    user_data = (194945, "Oleg")
    await db.add_to_data_base(user_data)

if __name__ == "__main__":
    asyncio.run(main())

# if __name__ == "__main__":

    # uvicorn.run("telebot_db:app", host="127.0.0.1", post=8000, reload=True)