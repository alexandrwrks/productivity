from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr

class RegUserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    reply_password: str = Field(min_length=6)

class LogUserSchema(BaseModel):
    email: EmailStr
    password: str

class UserDBSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    # можно добавить created_at с типом данных - datetime

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None

class TokenDataSchema(BaseModel):
    email: EmailStr | None = None
    user_id: int | None = None

class APIException(Exception): # класс для ошибок
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)