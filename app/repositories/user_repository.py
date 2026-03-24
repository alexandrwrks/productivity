from pydantic import EmailStr, BaseModel
from models.schemas import UserSchema, RegUserSchema, LogUserSchema
from dotenv import load_dotenv

import core.exceptions as ex
import asyncio
import logging
import aiosqlite
import os

logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

class UserDB(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    # можно добавить created_at с типом данных - datetime

class MainTestBase:
    def __init__(self, db_name = DB_NAME):
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

    async def add_user_to_db(self, user_info: dict) -> str:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                try:
                    await db.execute("BEGIN")
                    cursor = await db.execute("""
                        INSERT INTO Users (name, surname, email, password) 
                        VALUES (?, ?, ?, ?)""", (
                            user_info["name"],
                            user_info["surname"],
                            user_info["email"],
                            user_info["password"])
                        )
                    
                    user_id = cursor.lastrowid
                    
                    await db.execute("INSERT INTO UserActive (user_id, is_active) VALUES (?, 1)", (user_id,))

                    await db.commit()
                    return ex.ADD_USER_SUCCESS

                except aiosqlite.IntegrityError as e:
                    await db.rollback()
                    logging.warning(f"Почта {user_info['email']} уже существует")
                    return ex.UNIQUE_EMAIL
                
                except aiosqlite.Error as e:
                    await db.rollback()
                    logging.error(f"Ошибка добавления пользователя: {e}")
                    return ex.DATA_BASE_ERROR
                
        except aiosqlite.Error as e:
            logging.error(f"Ошибка подключения к БД: {e}")
            return ex.DATA_BASE_ERROR

    async def get_email_exists(self, email: EmailStr) -> str:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    "SELECT email FROM Users WHERE email = ?", 
                    (email,)
                )

                result = await cursor.fetchone()
                if result:
                    logging.info(ex.EMAIL_FOUND)
                    return result[0]
                
                return ex.EMAIL_NOT_EXISTS
                
        except aiosqlite.Error as e:
            logging.error(f"Ошибка чтения данных: {e}")
            return ex.DATA_BASE_ERROR
        
    async def check_users_active_exists(self, email: EmailStr) -> bool | str:
        """Проверка активности пользователя"""
        try: 
            async with aiosqlite.connect(self.db_name) as db: 
                cursor = await db.execute("""
                    SELECT ua.is_active
                    FROM UserActive ua
                    WHERE ua.user_id = (SELECT id FROM Users WHERE email = ?)
                """, (email,))

                result = await cursor.fetchone()

                if result:
                    return result[0] == 1 # True если активен, иначе False

                return ex.USER_ID_NOT_FOUND
                        
        except aiosqlite.Error as e:
            logging.error(f"Data reading error: {e}")
            return ex.DATA_BASE_ERROR
      
    async def get_hashed_password(self, email: EmailStr) -> str:
        try: 
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT password FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()
                if result:
                    logging.info(f"Успешное получение пароля для {email}")
                    return result[0]
                else:
                    logging.warning(f"Отсутвие пароля в БД для {email}")
                    return ex.NOT_PASSWORD

        except aiosqlite.Error as e:
            logging.error(f"Ошибка получения данных: {e}")
            return ex.DATA_BASE_ERROR

    async def get_user_by_email(self, email: EmailStr) -> dict | str:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT id, name, surname, email, created_at FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()

                if result:
                    user_dict = {
                        "id": result[0],
                        "name": result[1],
                        "surname": result[2],
                        "email": result[3],
                        "created_at": result[4]
                    }

                    logging.info(f"Успешное получение данных пользователя")
                    return user_dict
                else:
                    logging.info(f"Пользователь с таким email {email} не найден")
                    return ex.NOTHING_FOUND
                
        except aiosqlite.Error as e:
            logging.error(f"Data reading error: {e}")
            return ex.DATA_BASE_ERROR

    async def get_user_id_by_email(self, email: EmailStr) -> int | str:
        """Получить user_id пользователя по email"""
        try: 
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    """SELECT ua.user_id 
                    FROM UserActive ua
                    WHERE user_id = (SELECT id FROM Users WHERE email = ?)""", (email,))
                
                result = await cursor.fetchone()

                if result:
                    logging.info(f"Успешное получение user_id для email: {email}")
                    return result[0] 
                else:
                    logging.info(f"Отсутвие user_id для email: {email}")
                    return ex.NOT_INFO_ABOUT_EMAIL
                    
        except aiosqlite.Error as e:
            logging.error(f"Ошибка чтения данных: {e}")
            return ex.DATA_BASE_ERROR

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
                return result[0] if result else ex.NOT_ACTIVE_INFO
        
        except aiosqlite.Error as e:
            logging.error(f"Reading data error")
            return ex.DATA_BASE_ERROR

    async def soft_delete_account(self, email: EmailStr) -> str:
        """Мягкое удаление аккаунта"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                try:
                    await db.execute("BEGIN")

                    await db.execute("""
                        UPDATE UserActive 
                        SET is_active = 0, deleted_at = CURRENT_TIMESTAMP
                        WHERE user_id = (SELECT id FROM Users WHERE email = ?)
                    """, (email,))

                    await db.commit()

                    logging.info(f"Soft deletion successful for {email}")
                    return ex.ACC_SOFT_DELETE
                
                except aiosqlite.Error as e:
                    await db.rollback()
                    logging.error(f"User deletion error: {e}")
                    return ex.ERROR_ACC_SOFT_DELETE
                
        except aiosqlite.Error as e:
            logging.error(f"Database connection error: {e}")
            return ex.DATA_BASE_ERROR
        
    async def hard_delete_account(self, email: EmailStr) -> str:
        """Полное удаление аккаунта"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                try:
                    await db.execute("BEGIN")
                    await db.execute("PRAGMA foreign_keys = ON")         

                    await db.execute("DELETE FROM Users WHERE email = ?", (email,))
                    await db.commit()
                    return ex.ACC_HARD_DELETE

                except aiosqlite.Error as e:
                    await db.rollback()
                    logging.error(f"Ошибка удаления пользоваетля по email: {email}")
                    return ex.ERROR_ACC_HARD_DELETE
                
        except aiosqlite.Error as e:
            logging.error(f"Database connection error: {e}")
            return ex.DATA_BASE_ERROR


test_base = MainTestBase()


async def main():

    await test_base.init_db()
    
if __name__ == "__main__":
    asyncio.run(main())