from typing import Optional, Tuple
import aiosqlite

"""Что должно быть:

    Методы для чтения данных (получить пользователя по email, получить всех пользователей)

    Методы для записи данных (создать, обновить, удалить)

    Подключение к БД, курсоры, транзакции

Чего НЕ должно быть:

    Проверки сложности пароля

    Сравнения паролей

    Бизнес-правил ("пользователь с ролью X может Y")

    Хеширования

    Логики "если ... то ..."""


class UsersManager:
    """Позволяет пользователям регистрироваться, входить в систему, выходить из учетной записи,
    обновлять свои данные и удалять аккаунт."""
    def __init__(self, db_name="production.db"):
        self.db_name = db_name

    async def init_db(self):
        """
        name -> имя пользователя
        surname -> фамилия пользователя
        email -> почта
        password -> пароль 
        user -> роли пользователя (покупатель и продавец)
        is_active -> true, если акканут активный, false, если пользователь выйдет с аккаунта
        """
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Users (
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    user BOOLEAN DEFAULT TRUE,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.execute("""
                    CREATE INDEX IF NOT EXISTS ind_email ON Users(email)
                """)

                await db.commit()
                print("База данных успешно инициализирована")
                return True
        except aiosqlite.Error as e:
            print(f"Ошибка инициализации БД: {e}")
            return False
    
    async def check_email(self, email: str) -> bool:
        """Проверят наличие почты в базу данных и выводит True или False"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    "SELECT email FROM Users WHERE email = ?", 
                    (email,)
                )

                result = await cursor.fetchone()
                return result is not None
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return False
        
    async def get_user_password(self, email: str) -> Optional[Tuple[str]]:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    "SELECT password FROM Users WHERE email = ?",
                    (email,)
                )

                result = await cursor.fetchone()
                return result
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return None
        
    async def reg_user(self, user_data: dict) -> bool:
        """
        Добавление-регистрация пользователя в базу данных
        имя, фамилия, почта, пароль
        """
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""INSERT INTO Users (name, surname, email, password) 
                                 VALUES (?, ?, ?, ?)""", 
                                (user_data["name"],
                                user_data["surname"],
                                user_data['email'],
                                user_data["password"])
                                )
                
                await db.commit()
                # print(f"Пользователь {user_data["email"]} успешно зарегестрирован")
                return True
        except aiosqlite.Error as e:
            print(f"Ошибка добавления пользователя в БД: {e}")
            return False
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM Users WHERE email = ?",
                    (email,)
                )

                result = await cursor.fetchone()
                return dict(result) if result else None
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return None

    async def update_user(self, email: str, update_data: dict) -> bool:
        """Обновление информации пользователя"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                # Динамически строим запрос на основе переданных полей
                set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
                values = list(update_data.values()) + [email]
                
                await db.execute(
                    f"UPDATE Users SET {set_clause} WHERE email = ?",
                    values
                )
                await db.commit()
                return True
            
        except aiosqlite.Error as e:
            print(f"Ошибка обновления пользователя: {e}")
            return False
        
    async def logout_user(self, email: str) -> bool:

        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(
                    "UPDATE Users SET is_active = 0 WHERE email = ?",
                    (email,)
                )
                await db.commit()
                return True
            
        except aiosqlite.Error as e:
            print(f"Ошибка при логауте: {e}")
            return False

    async def del_user(self, email: str) -> bool:
        """Удаление пользователя: Удаление аккаунта (мягкое) — пользователь инициирует удаление, происходит logout,
        пользователь больше не может залогиниться, но при этом в базе учетная запись остается со статусом is_active=False."""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(
                    "UPDATE Users SET is_active = 0 WHERE email = ?",
                    (email,)
                )
                await db.commit()
                return True
            
        except aiosqlite.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")
            return False
        
    async def view_all_users(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT name, surname, email FROM Users")

                result = cursor.fetchall()
                return result
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")

class SellerManager(UsersManager):
    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS Seller (
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email UNIQUE TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAUL CURRENT_TIMESTAMP
                    )
                """)

                await db.commit()
                return True
            
        except aiosqlite.Error as e:
            print(f"Ошибка инициализация таблицы: {e}")
            return False

class AdminManager(UsersManager):
    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS Admin (
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email UNIQUE TEXT NOT NULL,
                    password TEXT NOT NULL,
                    admin BOOLEAN DEFAULT TRUE,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                await db.commit()
        except aiosqlite.Error as e:
            print(f"База данных успешно инициализирована: {e}")
            return False

user_manager = UsersManager()
seller_manager = SellerManager()
admin_manager = AdminManager()