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

class TestBase:
    def __init__(self, db_name="test_api.db", log_name = "test_logging"):
        self.db_name = db_name
        self.log_name = log_name

    async def init_db(self):
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

    """Функции для возврата информации о пользователе"""
    async def check_email_exists(self, email: EmailStr) -> bool:
        """Проверяет наличие почты в БД"""
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
            return None # При ошибке возращаем None
    
    async def get_hashed_password(self, email: EmailStr):
        """Получаем хешированный пароль"""
        try: 
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT password FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()
                return result[0] if result else None

        except aiosqlite.Error as e:
            logging.error(f"Ошибка получения данных: {e}")
            return "Ошибка чтения данных"

    async def get_user_by_email(self, email: EmailStr):
        """Возращаем всю информацию о пользователе по почте"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT * FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()
                return result
                
        except aiosqlite.Error as e:
            logging.error(f"Ошибка чтения данных: {e}")
            return None

    async def add_user_to_db(self, user_info: dict):
        """Добавляем пользователя в базу данных"""
        # with open(self.log_name, "a") as f:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("INSERT INTO Users (name, surname, email, password) VALUES (?, ?, ?, ?)",
                                (user_info["name"],
                                user_info["surname"],
                                user_info["email"],
                                user_info["password"])
                                )

                await db.commit()
                return True
            
        except aiosqlite.IntegrityError as e:
            logging.error(f"Ошибка добавления! Почта данная почта уже находится в БД: {e}")
            return False
        
        except aiosqlite.Error as e:
            logging.error(f"Ошибка добавления: {e}")
            return False

    async def delete_account(self, user_info: dict):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    UPDATE Users
                    SET is_active = FALSE
                    WHERE email = ?
                """, (user_info["email"]))
                
                await db.commit()
                return True
            
        except aiosqlite.Error as e:
            logging.error("Ошибка удаления пользователя")
            return False
"""
Ошибка в chech_email_exists
get_hash_password_by_email
add_user_to_db
except блоки не возращают ошибки на сервер
"""

test_base = TestBase()

async def main():

    await test_base.init_db()
    
if __name__ == "__main__":
    asyncio.run(main())