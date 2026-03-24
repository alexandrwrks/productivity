from pydantic import EmailStr, BaseModel
from passlib.context import CryptContext

class MainService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def password_hashing(self, password: str) -> str:
        return self.pwd_context.hash(password)