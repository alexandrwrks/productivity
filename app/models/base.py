from typing import Any, Optional, Union
from decimal import Decimal
from PIL import Image
from aiogram.types import Message
from aiogram import Bot

import aiosqlite as sq
import hashlib
import asyncio

class BaseDB:
    def __init__(self, db_name='ai_assistant.db'):  # Исправлено название
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
            async with sq.connect(self.db_name) as db:
                await db.execute('PRAGMA foreign_keys = ON')

                cursor = await db.execute(query, params)
            
                if fetch_one:
                    result = await cursor.fetchone()
                    print(f"Запрос выполнен успешно: {query[:40]}...")
                    return result
                elif fetch_all:
                    result = await cursor.fetchall()
                    print(f"Запрос выполнен успешно: {query[:40]}...")
                    return result
                else:
                    await db.commit()
                    print(f"Запрос выполнен успешно: {query[:40]}...")
                    return cursor.lastrowid
                
        except sq.Error as e:
            print(f"Ошибка выполнения запроса {query[:40]}: {e}")
            return None

class UsersDataManager(BaseDB):
    async def init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            username TEXT,
            name TEXT,          
            phone TEXT,
            email TEXT
        )
        """
        await self.execute_query(query)

    async def save_user_to_db(self, user_data: dict, user_id: int, username: str):
        try:
            async with sq.connect(self.db_name) as db:

                await db.execute('''INSERT INTO Items (user_id, name, email, username, phone, city) 
                                 VALUES (?, ?, ?, ?, ?, ?)''', (
                                     user_id,
                                     user_data['name'],
                                     user_data['email'],
                                     username,
                                     user_data['phone'],
                                     user_data['city']
                                 )
                    )
                await db.commit()
        except sq.Error as e:
            print(f"Ошибка добавления товара в БД: {e}")


    async def delete_data(self, email: str):
        """Удаление пользователя по email"""
        try:
            async with sq.connect(self.db_name) as con:
                await con.execute("DELETE FROM Users WHERE email = ?", (email,))
                await con.commit()
                print(f"Пользователь с email {email} удален")
        except sq.Error as e:
            print(f"Ошибка удаления данных: {e}")

class ItemsDataManager(BaseDB):
    async def init_db(self):
        """
        user_id -> уникальный тг номер пользователя
        useranme -> username пользователя(админа), который создал карточку товара
        photo -> изоброжение/фотография которую прислыл пользователь через ТГ бота или через FastAPi(скорее всего через бота)
        price -> цена которую указал продавец
        description -> описание товара для удобства пользователям
        photo -> изображения товара(photo.id)
        """
        product_query = """
        CREATE TABLE IF NOT EXISTS Items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            username TEXT NOT NULL,
            price REAL NOT NULL,
            active BOOLEAN DEFAULT TRUE,
            description TEXT,
            photo TEXT
        )
        """
        await self.execute_query(product_query)

    """
    Сделать отдельыне функции для добавления информации в таблицу Items.
    Каждая функция будет овечать за одну позицию которую пользоваетль добавит в БД.
    Корневая функция add_item, после чего в неё добавить функции добавления позиций
    """
    async def save_item_to_db(self, data: dict, username: str):
        try:
            async with sq.connect(self.db_name) as db:

                await db.execute('INSERT INTO Items (item_name, username, price, description, photo) VALUES (?, ?, ?, ?, ?)', (
                    data['name'],
                    username,
                    data['price'],
                    data.get('description', ''),
                    data['photo_file_id']
                ))
                await db.commit()
        except sq.Error as e:
            print(f"Ошибка добавления товара в БД: {e}")

    async def add_item_photo(self, photo: Image):
        img = Image.open('image.png')  # img теперь переменная-изображение
        img.show()  # показать фото
        img.save('new_image.jpg') # сохранить фото
        img.size()
        img.resize()

    async def get_items_data(self):
        async with sq.connect(self.db_name) as db:
            cursor = await db.execute('SELECT item_id, item_name, username, price FROM Items WHERE active')
            result = await cursor.fetchall()
            return result

class OrdersDataManager(BaseDB):
    async def init_db(self):
        """
        id -> номер заказа(лучше всего если будет начинаться с 100001)
        is_active -> активный ли заказ, если FALSE то значит заказ либо отменили, либо довезли до клиента
        user_id -> user_id это уникальный тг номер пользователя который совершил заказ
        username -> связан с user_id (таблица Users), получаем его вопремя регистрации пользователя или же тогда перед совершением покупки

        Что ещё добавить?
        """
        order_query = """
        CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT = 100000,
        username TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        is_active BOOLEAN DEFAULT True
        )
        """
        await self.execute_query(order_query)

    async def add_order(
            self,
            user_data: tuple, # получаю user_id(покупателя), username(покупателя), item_id(с начал сравнить с item_id Items)
    ):
        order_query = 'SELECT * FROM Items WHERE item_id = ? VALUE (?)'  
        await self.execute_query(order_query, (user_data[0]))  
    
        add_order = '''

'''




async def main():
    um = UsersDataManager()
    im = ItemsDataManager()
    om = OrdersDataManager()
    await um.init_db()
    await im.init_db()
    # await om.init_db()


    # await um.add_user_from_bot()

if __name__ == "__main__":
    asyncio.run(main())