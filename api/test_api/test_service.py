from test_base import test_base
from passlib.context import CryptContext
from pydantic import EmailStr

class TestService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def password_hashing(self, password: str) -> str:
        """Получаем пароль и возращаем хешированный пароль"""
        return self.pwd_context.hash(password)
             

    async def verify_password(self, password: str, email: EmailStr) -> bool:
        """Проверяем введёный пароль с паролем из БД"""
        try:
            take_hash_password = await test_base.get_hashed_password(email)
            if take_hash_password is None:
                return False
            
            if take_hash_password == "Ошибка чтения данных":
                return False
            
            return self.pwd_context.verify(password, take_hash_password)

        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    async def checker_auth(self, email: EmailStr, input_password: str):
        """Првоерка во время авторизации"""
        check_email_in_db = await test_base.check_email_exists(email) # Получаем булевое значение

        if check_email_in_db is None:
            return False, "error"
        elif check_email_in_db is False:
            return False, "not email"
        
        
        hashed_password_exists = await self.verify_password(input_password, email)
        if not hashed_password_exists:
            return False, "not password"
    
        return True, "Welcome"
        

    async def check_email_for_registration(self, email: EmailStr):
        return await test_base.check_email_exists(email)

    async def data_preparation(self, user_info: dict):
        
        hashed_password = await self.password_hashing(user_info["password"])

        user_info["password"] = hashed_password

        add_user = await test_base.add_user_to_db(user_info)

        if add_user:
            return True
        else:
            return False

"""
get_hashed_password
verify_password
checker_auth
data_preperation
"""


test_service = TestService()