import aiosqlite

class UsersManager:
    """Позволяет пользователям регистрироваться, входить в систему, выходить из учетной записи,
    обновлять свои данные и удалять аккаунт."""
    def __init__(self, db_name=""):
        self.db_name = db_name

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(
                    """CREATE TABLE IF NOT EXISTS Users (
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    roles TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                    )
                """)

                db.commit()

        except aiosqlite.Error as e:
            print(f"Ошибка инициализации БД: {e}")
        
    async def reg_user(self, user_data: dict):
        """Регистрация: Ввод имени (фамилии, отчества), email, пароля, повтор пароля."""
        pass

    async def login_user(self, user_data: dict):
        """Login: пользователь входить в систему по email и паролю.
        * После login система при последующих обращениях должна идентифицировать пользователя."""
        pass

    async def update_user(self):
        """Обновление информации: Пользователь может редактировать свой профиль."""
        pass
    
    async def logout_user(self):
        """Logout: пользователь выходит из системы."""
        pass

    async def del_user(self):
        """Удаление пользователя: Удаление аккаунта (мягкое) — пользователь инициирует удаление, происходит logout,
        пользователь больше не может залогиниться, но при этом в базе учетная запись остается со статусом is_active=False."""
        pass