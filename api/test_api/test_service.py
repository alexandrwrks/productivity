from test_base import test_base
from passlib.context import CryptContext
from pydantic import EmailStr


class MainTestService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def password_hashing(self, password: str) -> str:
        """Получаем пароль и возращаем хешированный пароль"""
        return self.pwd_context.hash(password)
    
    async def check_email_in_db(self, email: EmailStr) -> bool:
        """Возращает bool значение"""
        return await test_base.check_email_exists(email)

    
class TestRegistrationService(MainTestService):
    """
    Чтобы добавить пользователя - нужно првоерить наличие почты в БД, если нет, то делаем валидацию данных,
    после добавляем данные в таблицу Users. 
    В UsersActivity автоматически добавляем данные добавляем 
    """
    async def data_preparation(self, user_info: dict):
        
        hashed_password = await self.password_hashing(user_info["password"])

        user_info["password"] = hashed_password

        add_user = await test_base.add_user_to_db(user_info)

        if add_user:
            return True
        else:
            return False


class TestAuthorizationService(MainTestService):
    async def verify_password(self, password: str, email: EmailStr) -> bool | None:
        """Проверяем введёный пароль с паролем из БД"""
        try:
            take_hash_password = await test_base.get_hashed_password(email)
            if take_hash_password is None:
                return None
            
            if take_hash_password is False:
                return False
            
            return self.pwd_context.verify(password, take_hash_password)

        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        
    async def checker_auth(self, email: EmailStr, input_password: str):
        """Првоверка во время авторизации"""
        check_email_in_db = await test_base.check_email_exists(email)

        if check_email_in_db is None:
            return False, "error"
        elif check_email_in_db is False:
            return False, "not email"
        
        
        hashed_password_exists = await self.verify_password(input_password, email)
        if not hashed_password_exists:
            return False, "not password"
    
        return True, "Welcome"

class TestDeleteService(MainTestService):
    async def soft_delete_account(self, email: EmailStr):
        
        del_account = await test_base.soft_delete_account(email)

        if del_account:
            return True
        
        return False



main_service = MainTestService()
reg_service = TestRegistrationService()
auth_service = TestAuthorizationService()
del_service = TestDeleteService()