import asyncio
import sqlite3
import uvicorn

from telebot import types
import telebot

from bot_token import BOT_TOKEN

"""
Для регистрации пользователя в ТГ боте
БД принимает список из id_пользователя, имени, почты и пароля
Сделать проверку использования почты в базе данных
чтобы не было такого что на сайте уже зарегестрировались, а потом решили зарегистрироваться в ТГ.
База данных для почты должна быть синхронизирована с БД ТГ(создаю 1 таблицу где я буду проверять почту как для сайта так и для ТГ бота)
Во время работы принимает строку:
/calories [продукт1] [вес] ... datetime и id_пользователя.

datetime нужен:
для того чтобы отправлять итоги за день если пользователь запросит об этом информацию
для того чтобы пользователь мог запросить результат за неделю и ему сразу же вычислили калории съеденные за неделю
"""


class DataManager:
    def __init__(self, db_name = "my_database.db"):
        self.db_name = db_name
        
    def init_data_base(self):

        connection = None 
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            """
            В БД будет находиться обычный id - нумерация пользователей и user_id - ТГ id
            """

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS TUsers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    )
                ''')
            
            connection.commit()
            print(f"Инициализированна таблица TUsers в базе данных {self.db_name}")
            print(f"В таблице инициализированны id, user_id, name, email, password стобцы")
        except sqlite3.Error as e:
            print(f"❌ Ошибка инициализации базы данных {self.db_name}")
        finally:
            if connection:
                connection.close()

    async def add_user_data(self, received_data):
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            user_id, name, email, password = received_data
            cursor.execute('''
                    SELECT * FROM TUsers (user_id, name) 
                        WHERE email = ?
                ''', (email,))
            result = cursor.fetchone()

            if result:
                print(f"Ошибка почта уже используется")
                return {
                    "status": "error",
                    "message": "Почта уже используется"
                }
            else:
                cursor.execute('''
                            INSERT INTO TUsers (user_id, name, email, password) 
                               VALUE (?, ?, ?, ?)
                               ''', (user_id, name, email, password))
                connection.commit()            
            print(f"Добавлен пользователь: {name} id {user_id}")
        except sqlite3.Error as e:
            print(f"❌ Ошибка добавления пользователя: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    def test_data(self, received_data):

        connection = None

        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            user_id, name, email, password = received_data # user_id - ТГ id
            cursor.execute('SELECT * FROM TUsers WHERE email = ? AND password = ?', )



        except sqlite3.Error as e:
            print(f"❌ Ошибка проверки данных")
        finally:
            if connection:
                connection.close()

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(BOT_TOKEN)
        self.DB = DataBase(self.bot)
        self.setup_handlers()

    def setup_handlers(self):

        @self.bot.message_handler(commands=['start'])
        def handle(message):
            self.register_menu(message)

    def register_menu(self, message):
        
        self.bot.send_message(
            message.chat.id,
            f"Введите имя для регистрации: "
            )       
        name =  message.text
        user_data = (message.chat.id, name)
        self.add_name_to_db(user_data)
    
    def add_name_to_db(self, user_data):

        user_id, name = user_data

        # self.bot.send_message(
        #     message.chat.id,
        #     f"Введите имя для регистрации: "
        #     )
        # self.bot.send_message(
        #     message.chat.id,
        #     f"Введите имя для регистрации: "
        #     )
        # self.bot.send_message(
        #     message.chat.id,
        #     f"Введите имя для регистрации: "
        #     )

class DataBase:
    def __init__(self, db_name = "my_database.db"):
        self.db_name = db_name

    def init_base(self):
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()

            cursor.execute('''
                CREATE TABLE User_Name (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TETX NOT NULL
                        )
                        ''', )
            con.commit()
            print(f"База данных '{self.db_name}' иницилаизирована")
        except sqlite3.Error as e:
            print(f"❌ Ошибка инициализации базы данных '{self.db_name}'")
        finally:
            if con:
                con.close()

    def add_users_to_db(self, received_data):

        con = None
        try:
            con = sqlite3.connect(self.db_name)

        except sqlite3.Error as e:
            print(f"❌ Ошибка добавления пользователя в БД")
        finally:
            if con:
                con.close()



# async def main():
#     db = DataManager()
#     db.init_data_base()
#     await db.add_user_data()

# if __name__ == "__main__":
#     asyncio.run(main())