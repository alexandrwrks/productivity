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
    def init_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            user_email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            )
        '''
        self.execute_query(query)

    def view_all_data(self):
        con = None

        try:
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()

            cursor.execute('SELECT * FROM Users')
            users = cursor.fetchall()

            print(f"Всего пользователей: {len(users)}")
        
        except sqlite3.Error as e:
            print(f"Ошибка при чтение данных: {e}")
        finally:
            if con:
                con.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user_to_db(self, user_id: int, name: str, email: str, password: str):
        con = None
        
        try:
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()

            cursor.execute('''
                        SELECT * FROM Users
                           WHERE user_email = ?  
            ''', (email,))

            result = cursor.fetchone()

            if result:
                print(f"Ошибка при регистрации: {email} уже занят")
            else:
                hashed_password = self.hash_password(password)
                cursor.execute('''
                            INSERT INTO Users 
                               (user_id, user_name, user_email, password)
                               VALUES (?, ?, ?, ?)
                ''', (user_id, name, email, hashed_password))
                print(f"Успешное добавление данных в БД {self.db_name}")
                con.commit()

        except sqlite3.Error as e:
            print(f"Ошибка добавления данных в таблицу Users: {e}")
        finally:
            if con:
                con.close()

class ProductsData(BaseDB):
    def init_table(self):
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
        self.execute_query(query)

    def view_all_data(self):
        con = None

        try:
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()

            cursor.execute('SELECT * FROM Products')
            users = cursor.fetchall()

            print(f"Всего продуктов: {len(users)}")
        
        except sqlite3.Error as e:
            print(f"Ошибка при чтение данных: {e}")
        finally:
            if con:
                con.close()

    def find_data(self, name_of_product: str):
        
        query = '''
        SELECT * FROM Products 
        WHERE LOWER(name_of_product) LIKE LOWER(?)
        ''' 
        result = self.execute_query(query, (f'%{name_of_product}%',), fetch_all=True)
        return result

class ReportInfoProducts(BaseDB):
    def init_table(self):
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
        self.execute_query(query)


    def add_products_to_db(self, user_id, product_name, calories, carbs, protein, fats):
        query = '''
        INSERT INTO ProductsReport
        (name_of_product, calories, carbs, protein, fats, user_id, datetime)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        '''
        params = (product_name, calories, carbs, protein, fats, user_id)
        return self.execute_query(query, params)

    def get_daily_report_formatted(self, user_id):
        query = '''
        SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fats), COUNT(*) 
        FROM ProductsReport
        WHERE user_id = ? AND DATE(datetime) = DATE('now')
        '''
        result = self.execute_query(query, (user_id,))
        return result
    
    def get_weekly_stats(self, user_id):
        query = '''
        SELECT DATE(datetime) as day, SUM(calories), SUM(protein), SUM(carbs), SUM(fats)
        FROM ProductsReport
        WHERE user_id = ? AND DATE(datetime) >= DATE('now', '-7 days')
        GROUP BY DATE(datetime)
        ORDER BY day DESC
        '''
        result = self.execute_query(query, (user_id,))
        return result
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

    def handle_start(self):
        self.PRODUCT.init_table()
        self.REPORT.init_table()
        self.USERS.init_table()

    def add_data(self):
        self.USERS.add_user_to_db(19898, "Alex", "email@mail.ru", "qwerty")

if __name__ == "__main__":
    work_db = WorkDB()
    work_db.handle_start()
    work_db.add_data()

# if __name__ == "__main__":
#     db_product.init_table()

# if __name__ == "__main__":
#     users_manager.init_table()
#     users_manager.add_user_to_db(1313414, "Alex", "email@gmail.com", "qwerty")
