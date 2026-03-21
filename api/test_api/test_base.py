import aiosqlite

class TestBase:
    def __init__(self, db_name="test_api.db"):
        self.db_name = db_name

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                        CREATE TABLE IF NOT EXISTS Users (
                        name TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                    """)
                
                await db.commit()
        
        except aiosqlite.Error as e:
            print(f"Ошибка инициализации базы данных")

    async def check_user_email_in_db(self, email: str) -> bool:
        """Проверяет наличие почты в БД"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT * FROM Users WHERE email = ?", (email,))
                
                result = await cursor.fetchone()
                if result is not None:
                    return result
                
                return False
            
        except aiosqlite.Error as e:
            print(f"ошибка чтения данныз: {e}")
                 
    async def get_user_by_email(self, email: str):
        """Возращаем всю информацию о пользователе по почте"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT * FROM Users WHERE email = ?", (email,))

                result = await cursor.fetchone()
                return result
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")

    async def get_hash_password_by_email(self, email: str) -> str:
        """Возращаем хешированный пароль из БД для указанного email"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT password FROM Users WHERE email = ?", (email,))

                hashed_password = await cursor.fetchone()
                return hashed_password
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")


    async def add_user_to_db(self, user_info: dict):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("INSERT INTO Users (name, surname, email, password) VALUES (?, ?, ?, ?)",
                                (user_info["name"],
                                 user_info["surname"],
                                 user_info["email"],
                                 user_info["password"])
                                )

                await db.commit()

        except aiosqlite.Error as e:
            print(f"Ошибка добавления: {e}")



test_base = TestBase()