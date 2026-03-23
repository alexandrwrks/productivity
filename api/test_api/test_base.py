from sqlalchemy.orm import Session
from pydantic import EmailStr
from datetime import datetime

import asyncio
import logging
import aiosqlite

logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

class MainTestBase:
    def __init__(self, db_name="test_api.db"):
        self.db_name = db_name

    async def init_db(self):
        """Метод для инициализации всех нужных таблиц для работы с пользоваетлями"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                # Создаем таблицу Users
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
                # Создаем таблицу UserActive
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS UserActive (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL UNIQUE,
                        is_active BOOLEAN DEFAULT 1,
                        deleted_at TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
                    )
                """)
                
                """
                FOREIGN KEY -> user_id получается Users(id), а Users(id) это число автоматически присваемое в таблице Users
                """

                # Создаем индекс
                await db.execute("""
                    CREATE INDEX IF NOT EXISTS idx_user_active_user_id 
                    ON UserActive(user_id)
                """)
                
                await db.commit()
                logging.info("The database has been successfully initialized")
                
        except aiosqlite.Error as e:
            logging.error(f"Initialization error: {e}")
            raise

    """Добавление данных"""
    async def add_user_to_db(self, user_info: dict) -> bool:
        """Добавляем пользователя в базу данных"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                async with db.execute("BEGIN"):
                    cursor = await db.execute("INSERT INTO Users (name, surname, email, password) VALUES (?, ?, ?, ?)",
                                (user_info["name"],
                                user_info["surname"],
                                user_info["email"],
                                user_info["password"])
                                )
                    
                    user_id = cursor.lastrowid

                    await db.execute("INSERT INTO UserActive (user_id, is_active) VALUES (?, 1)", (user_id,))

                    await db.commit()
                    return True
            
        except aiosqlite.IntegrityError as e:
            logging.error(f"Ошибка добавления! Почта данная почта уже находится в БД: {e}")
            return False
        
        except aiosqlite.Error as e:
            logging.error(f"Ошибка добавления: {e}")
            return False

    """Проверка данных"""
    async def check_email_exists(self, email: EmailStr) -> bool | None:
        """Возращает bool тип данных"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    "SELECT email FROM Users WHERE email = ?", 
                    (email,)
                )

                result = await cursor.fetchone()
                if result: # Если почта есть в БД, то возращаем True, иначе False
                    return True
                
                return False
                
        except aiosqlite.Error as e:
            logging.error(f"Ошибка чтения данных: {e}")
            return None
        
    async def check_users_active_exists(self, email: EmailStr) -> bool | None:
        """Проверка активности пользоваетля"""
        try: 
            async with aiosqlite.connect(self.db_name) as db:

                cursor = await db.execute("SELECT is_active FROM UserActive WHERE email = ?", (email,))

                is_active_tuple = await cursor.fetchone()

                if is_active_tuple:
                    is_active = is_active_tuple[0]
                    if is_active == 1:
                        return True

                return None
            
        except aiosqlite.Error as e:
            logging.error(f"Data reading error: {e}")
            return False
      

    """Получение данных"""
    async def get_hashed_password(self, email: EmailStr) -> str:
        """Получаем хешированный пароль"""
        try: 
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT password FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()
                if result:
                    logging.info(f"Успешное получение пароля для {email}")
                    return result[0]
                else:
                    logging.warning(f"Отсутвие пароля в БД для {email}")
                    return "Отсутвие пароля в БД"

        except aiosqlite.Error as e:
            logging.error(f"Ошибка получения данных: {e}")
            return None

    async def get_user_by_email(self, email: EmailStr) -> tuple | None:
        """Возращаем всю информацию о пользователе по почте"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT * FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()
                if result:
                    logging.info(f"Успешное получение данных пользователя")
                    return result
                else:
                    logging.warning(f"Успешное выполнение запроса ")
                    return None
                
        except aiosqlite.Error as e:
            logging.error(f"Data reading error: {e}")
            return None
        
    async def get_user_id_by_email(self, email: EmailStr) -> int | None: 
        """Возращает id пользователя по email или None если не найден"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    "SELECT id FROM Users WHERE email = ?",
                    (email,)
                )
                result = await cursor.fetchone()
                if result:
                    logging.info(f"Успешно получения id")
                    return result[0]
                else:
                    logging.warning(f"Отсутствует id по email: {email}")
                    return None

        except aiosqlite.Error as e:
            logging.error(f": {e}")
            return None

    async def get_user_id_by_email(self, email: EmailStr) -> str:
        try: 
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    """SELECT ua.id
                    FROM UserActive
                    JOIN Users u ON ua.user_if = u.id
                    WHERE u.email = ?""", (email,))
                
                result = cursor.fetchone()
                if result:
                    logging.info(f"Успешное получение данных по email: {email}")
                    return result[0] 
                else:
                    logging.info(f"Отсутвие наличия данных по email: {email}")
                    return f"Нет записей по данному email: {email}"
                    
        
        except aiosqlite.connect(self.db_name) as db:
            logging.error()

    async def get_user_active_by_email(self, email: EmailStr) -> str:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("""
                        SELECT ua.is_active 
                        FROM UserActive ua
                        JOIN Users u ON ua.user_id = u.id
                        WHERE u.email = ?
                    """, (email,))

                result = await cursor.fetchone()
                return result[0] if result else "Активность пользоваетля по email отсутствует"
        
        except aiosqlite.Error as e:
            logging.error(f"Reading data error")

    """Удаление данных"""
    async def soft_delete_account(self, email: EmailStr) -> bool | None:
        """Мягкое удаление акканута"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                async with db.execute("BEGIN"):
                    cursor = await db.execute("SELECT id FROM Users WHERE email = ?", (email,))
                    result = await cursor.fetchone()
                    if not result:
                        return None
                    
                    user_id = result[0]
                    await db.execute("UPDATE UserActive SET is_active = 0, deleted_at = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))
                    
                    await db.commit()
                    return True
            
        except aiosqlite.Error as e:
            logging.error(f"User deletion error: {e}")
            return False
        
    async def hard_delete_account(self, email: EmailStr) -> bool:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("PRAGMA foreign_keys = ON")         

                await db.execute("DELETE FROM Users WHERE email = ?", (email,))
                await db.commit()
                return True
            
        except aiosqlite.Error as e:
            logging.error(f"User deletion error: {e}")
            return False




            
"""Методы с user_id и email можно связать с помощью JOIN

SELECT ua.is_active 
FROM UserActive ua
JOIN Users u ON ua.user_id = u.id
WHERE u.email = ?"""


test_base = MainTestBase()


async def main():

    await test_base.init_db()
    
if __name__ == "__main__":
    asyncio.run(main())