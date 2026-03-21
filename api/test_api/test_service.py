from test_base import test_base
from passlib.context import CryptContext

class TestService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def pasword_hashing(self, password: str) -> str:
        """Получаем пароль и возращаем хешированный пароль"""
        return self.pwd_context.hash(password)
     
    async def verify_password(self, password: str, email: str):
        """Проверяем введёный пароль с паролем из БД"""
        try:
            hashed_password = await test_base.get_hash_password_by_email(email)

            if hashed_password is None:
                return False

            return self.pwd_context.verify(password, hashed_password)
            
        except Exception as e:
            print(f"Ошибка: {e}")

    async def checker_auth(self, email: str, input_password: str):
        check_email_in_db = await test_base.check_user_email_in_db(email)
        if not check_email_in_db:
            return False, "not email"
        
        hashed_password = await self.verify_password(input_password, email)
        if not hashed_password:
            return False, "not password"
        
        return True, "Welcome"
    

    async def data_preparation(self, user_info: dict):
        
        hashed_password = await self.pasword_hashing(user_info["password"])

        user_info["password"] = hashed_password

        await test_base.add_user_to_db(user_info)


test_service = TestService()