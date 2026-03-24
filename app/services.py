from passlib.context import CryptContext
from repositories.base_repository import test_base
from pydantic import EmailStr, BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models.schemas import APIException

import app.core.exceptions as ex
import logging

logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


class MainTestService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def password_hashing(self, password: str) -> str:
        return self.pwd_context.hash(password)

class TestRegistrationService(MainTestService):
    async def check_email_for_reg(self, email: EmailStr) -> bool:
        email_exists = await test_base.get_email_exists(email)

        if email_exists == ex.EMAIL_FOUND:
            raise APIException(
                message="Почта уже зарегестрирована",
                code=409
            )
        
        elif email_exists == ex.DATA_BASE_ERROR:
            raise APIException(
                message=ex.MES_INTERNAL_ERROR,
                code=500
            )
        
        logging.info("Успешная проверка")
        return True


    async def data_preparation(self, user_info: dict) -> bool:
        hashed_password = await self.password_hashing(user_info["password"])

        user_info["password"] = hashed_password

        add_user = await test_base.add_user_to_db(user_info)

        if add_user == ex.UNIQUE_EMAIL:
            logging.warning(f"Почта уже зарегестрирована: {user_info['email']}")
            raise APIException(
                message="Почта уже существует",
                code=409
            )
        
        elif add_user == ex.DATA_BASE_ERROR:
            raise APIException(
                message=ex.MES_INTERNAL_ERROR,
                code=500
            )
        
        elif add_user == ex.ADD_USER_SUCCESS:
            logging.info(f"Успешное добавление пользователя")
            return True
            

class TestAuthorizationService(MainTestService):
    async def check_email_for_login(self, email: EmailStr) -> bool:
        email_exists = await test_base.get_email_exists(email)

        if email_exists == ex.EMAIL_NOT_EXISTS:
            raise APIException(
                message="Сначала пройдите регистрацию",
                code=409
            )
        
        elif email_exists == ex.DATA_BASE_ERROR:
            raise APIException(
                message=ex.MES_INTERNAL_ERROR,
                code=500
            )

        return True
    
    async def verify_password(self, password: str, email: EmailStr) -> bool:
        take_hash_password = await test_base.get_hashed_password(email)
        if take_hash_password == ex.NOT_PASSWORD:
            logging.error(f"Отсутствие пароля в базе данных для {email}")
            raise APIException(
                message="Отсутсвие пароля в БД"
            )
        
        elif take_hash_password == ex.DATA_BASE_ERROR:
            logging.error("Ошибка БД")
            raise APIException(
                message=ex.MES_INTERNAL_ERROR,
                code=500
            )
        
        hash_password = take_hash_password
        pas_checker = await self.pwd_context.verify(password, hash_password) 
        if not pas_checker:
            logging.warning(f"Отсутствие схожести паролей - {email}")
            raise APIException(
                message="Пароль не совпадает",
            )
        
        logging.info("Проверка прошла успешно")
        return True 
    
    async def authorization(self, email: EmailStr, password: str) -> bool:
        check_email = await self.check_email_for_login(email)
        ver_password = await self.verify_password(password, email)
        
        if check_email and ver_password:
            return True
        else:
            return False

class TestDeleteService(MainTestService):
    async def soft_delete_account(self, email: EmailStr) -> bool:
        del_account = await test_base.soft_delete_account(email)
    
        if del_account == ex.DATA_BASE_ERROR:
            logging.error(ex.DATA_BASE_ERROR)
            raise APIException(
                message=ex.MES_INTERNAL_ERROR
            )
        
        logging.info(ex.ACC_SOFT_DELETE)
        return True

