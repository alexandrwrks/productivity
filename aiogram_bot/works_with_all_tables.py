from typing import Any, Optional, Union

import hashlib
import sqlite3
import aiosqlite
import asyncio

class BaseDB:
    def __init__(self, db_name: str ="my_database.db"):
        self.db_name = db_name

    async def execute_query(
            self,
            query: str,
            params: tuple = (),
            fetch_one: bool = False,
            fetch_all: bool = False
    ):
        """Универсальный метод для работы с БД"""  
        try:       
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("PRAGMA foreign_keys = ON")

                cursor = await db.execute(query, params)

                if fetch_one:
                    result = await cursor.fetchone()
                    print(f"Запрос выполнен: {query[:50]}...")
                    return result
                elif fetch_all:
                    result = await cursor.fetchall()
                    print(f"Запрос выполнен: {query[:50]}...")
                    return result
                else:
                    await db.commit()
                    print(f"Запрос выполнене: {query[:50]}...")
                    return cursor.lastrowid

        except aiosqlite.Error as e:
            print(f"Ошибка БД: {e}")
            return None
        
class UsersDataManager(BaseDB):
    async def init_table(self):
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                user_email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
                )
            '''
            result = await self.execute_query(query)
            return result
        except aiosqlite.Error as e:
            print(f"Ошибка инициализации таблицы: {e}")
            return None
    
    async def view_all_data(self):
        try:
            query = 'SELECT * FROM Users'

            result = await self.execute_query(query, fetch_all=True)
            if result:
                print(f"Всего пользователей: {len(result)}")
            return result
        
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return None
        
    async def hash_password(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    async def add_user_to_db(self, user_id: int, name: str, email: str, password: str):        
        try:
            check_query = 'SELECT * FROM Users WHERE user_email = ?'
            check_params = (email,)
            
            result = await self.execute_query(check_query, check_params, fetch_one=True)

            if result:
                print(f"Ошибка при регистрации: {email} уже занят")
            else:
                hashed_password = await self.hash_password(password)
                add_query = '''INSERT INTO Users (user_id, user_name, user_email, password)VALUES (?, ?, ?, ?)'''
                add_params = (user_id, name, email, hashed_password)

                await self.execute_query(add_query, add_params)
                print(f"Успешное добавление данных в БД {self.db_name}")

        except aiosqlite.Error as e:
            print(f"❌ Ошибка добавления данных в таблицу Users: {e}")
            return None
        
    async def login_users(self, email: str, password: str):
        """
        Аутентификация пользователя по email и password
        """
        try:
            login_query = 'SELECT * FROM Users WHERE user_email = ?'
            login_params = (email,)

            result = await self.execute_query(login_query, login_params, fetch_one=True)

            if not result:
                print(f"Пользователь по такому email - {email} не найден")
                return None
            # result[0]=id, [1]=user_id, [2]=user_name, [3]=user_email, [4]=password
            stored_password_hash = result[4]  # Получаем хеш из БД
            input_password_hash = await self.hash_password(password)

            if stored_password_hash == input_password_hash:
                print(f"Пользователь {result[2]} успешно вошёл в систему")
                return {
                    'id': result[0],
                    'user_id': result[1],
                    'user_name': result[2],
                    'user_email': result[3]
                }   
            else:
                print('Неверный пароль')
                return None
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return None
            
        
class ProductsData(BaseDB):
    async def init_table(self):
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS Products (
                id_of_name INTEGER PRIMARY KEY AUTOINCREMENT,
                name_of_product TEXT NOT NULL,
                calories REAL NOT NULL,
                carbs REAL NOT NULL,
                protein REAL NOT NULL,
                fats REAL NOT NULL
                )
            '''
            result = await self.execute_query(query)
            return result
        except aiosqlite.Error as e:
            print(f"❌ Ошибка инициализации таблицы: {e}")
            return None

    async def view_all_data(self):
        try:
            check_query = 'SELECT * FROM Products'

            result = await self.execute_query(check_query, fetch_all=True)
            return len(result)
        
        except sqlite3.Error as e:
            print(f"Ошибка при чтение данных: {e}")
            return None
        
    async def find_data(self, name_of_product: str):
        try:
            query = '''
            SELECT * FROM Products 
            WHERE LOWER(name_of_product) LIKE LOWER(?)
            ''' 
            result = await self.execute_query(query, (f'%{name_of_product}%',), fetch_all=True)
            return result
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return None

class ReportInfoProducts(BaseDB):
    async def init_table(self):
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS ProductsReport (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_of_product TEXT NOT NULL,
                calories REAL NOT NULL,
                carbs REAL NOT NULL,
                protein REAL NOT NULL,
                fats REAL NOT NULL, 
                user_id INTEGER NOT NULL,
                datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
                )
            '''
            result = await self.execute_query(query)
            return result
        
        except aiosqlite.Error as e:
            print(f"Ошибка инициализации табоицы: {e}")
            return None

    async def add_products_to_db(
            self,
            user_id: int,
            product_name: str,
            calories: float, 
            carbs: float,
            protein: float,
            fats: float
    ):
        try:
            query = '''
            INSERT INTO ProductsReport
            (name_of_product, calories, carbs, protein, fats, user_id, datetime)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            '''
            params = (product_name, calories, carbs, protein, fats, user_id)
            result = await self.execute_query(query, params)
            return result
        except aiosqlite as e:
            print(f"Ошибка добваления данных: {e}")
            return None

    async def get_daily_report_formatted(self, user_id: int):
        try:
            query = '''
            SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fats), COUNT(*) 
            FROM ProductsReport
            WHERE user_id = ? AND DATE(datetime) = DATE('now')
            '''
            result = await self.execute_query(query, (user_id,))
            return result
        except aiosqlite as e:
            print(f"Ошибка чтения данных: {e}")
            return None
    
    async def get_weekly_stats(self, user_id: int):
        try:
            query = '''
            SELECT DATE(datetime) as day, SUM(calories), SUM(protein), SUM(carbs), SUM(fats)
            FROM ProductsReport
            WHERE user_id = ? AND DATE(datetime) >= DATE('now', '-7 days')
            GROUP BY DATE(datetime)
            ORDER BY day DESC
            '''
            result = await self.execute_query(query, (user_id,))
            return result
        except aiosqlite as e:
            print(f"Ошибка чтения данных: {e}")
            return None
        
class Reminders(BaseDB):
    async def init_table(self):
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS Reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reminder_text TEXT NOT NULL,
                reminder_time TIMESTAMP NOT NULL,  -- Когда должно сработать
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',  -- active, completed, cancelled
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
                )
            '''
            result = await self.execute_query(query)
            return result
        
        except aiosqlite.Error as e:
            print(f"Ошибка инициализации таблицы: {e}")
            return None
        
    async def add_reminder(self, user_id: int, text: str, reminder_text: str):
        add_query = '''
        INSERT INTO Reminders (user_id, reminder_text, reminder_time)
        VALUES (?, ?, ?)
        '''
        return await self.execute_query(add_query, (user_id, text, reminder_text))


"""
Логирование пользователя с хэшированным паролем
stored_password = cursor.fetchone()[4]  # Получаем хеш из БД
if stored_password == hash_password(input_password):
    print("Пароль верный")
"""

class WorkDB:
    def __init__(self):
        self.PRODUCT = ProductsData()
        self.REPORT = ReportInfoProducts()
        self.USERS = UsersDataManager()
        self.REMINDERS = Reminders()

    async def handle_start(self):
        await self.PRODUCT.init_table()
        await self.REPORT.init_table()
        await self.USERS.init_table()
        await self.REMINDERS.init_table()

    async def add_data(self):
        await self.USERS.add_user_to_db(19898, "Alex", "email@mail.ru", "qwerty")

    async def log_user(self):
        await self.USERS.login_users("email@mail.ru", "qwerty")

async def main():
    work_db = WorkDB()
    await work_db.handle_start()
    await work_db.add_data()
    await work_db.log_user()

if __name__ == "__main__":
    asyncio.run(main())
