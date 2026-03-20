from api.models.base import UsersManager, user_manager
from passlib.context import CryptContext

"""Что должно быть:

    Проверка пароля (длина, сложность, совпадение с повтором)

    Хеширование пароля (с использованием CryptContext)

    Проверка, что email не занят (ВЫЗЫВАЕТ метод base.py для проверки!)

    Проверка при логине (пароль верный? ВЫЗЫВАЕТ метод base.py для получения пользователя)

    Решение, что делать после проверок (сохранить пользователя → ВЫЗВАТЬ метод base.py для сохранения)

Чего НЕ должно быть:

    Прямых SQL запросов

    Подключений к базе данных

    Знания о том, как именно хранятся данные (SQLite, PostgreSQL, файлы)"""

class Service:
    def __init__(self, users_manager: UsersManager):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.um = users_manager

    """
    Проверка длины пароля
    Хэширование пароля
    Проверка совпадения пароля с хэш паролем из БД
    Проверка правильности пароля при логине
    """

    async def check_len_password(self, password: str):
        """Проверка длины пароля"""
        return len(password) >= 8
    
    async def check_password_complexity(self, password: str):
        """Проверка сложности пароля"""
        if len(password) < 8:
            return False,

        if not any(c.isupper() for c in password):
            return False,

        if not any(c.islower() for c in password):
            return False,

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False,

        return True,

    async def password_hashing(self, password: str) -> str:
        """Хешируем пароль"""
        return self.pwd_context.hash(password)

    async def verify_password(self, plain_password: str, email: str) -> bool:
        """Подтверждение пароля и сравнение с БД"""
        try:
            result = await self.um.get_user_password(email)
            if result is None:
                return False
            hashed_password = result[0]
            return self.pwd_context.verify(plain_password, hashed_password)
        
        except Exception as e:
            print(f"Ошибка при проверке email: {e}")
            return False

    async def register_user(self, user_data: dict):
        """Регистрация пользователя с проверками"""
        if user_data["password"] != user_data["reply_password"]:
            return False,

        if not await self.check_len_password(user_data["password"]):
            return False,

        is_complex= await self.check_password_complexity(user_data["password"])
        if not is_complex:
            return False
        
        hashed_password = await self.password_hashing(user_data["password"])

        user = {
            "name": user_data["name"],
            "surname": user_data["surname"],
            "email": user_data["email"],
            "password": hashed_password
        }

        success = await self.um.reg_user(user)
        if success:
            return True
        else:
            return False


service = Service(user_manager)