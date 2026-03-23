from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from test_service import MainTestService, TestRegistrationService, TestAuthorizationService, TestDeleteService  
from test_base import test_base
from contextlib import asynccontextmanager

import uvicorn

main_service = MainTestService()
reg_service = TestRegistrationService()
auth_service = TestAuthorizationService()
del_service = TestDeleteService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await test_base.init_db()
    yield

app = FastAPI(title="Мой магазин на FastAPI", lifespan=lifespan)

class RegistrationUserSchemas(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    reply_password: str


class AuthorizationUserSchemas(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserSchemas(BaseModel):
    name: str
    surname: str
    email: EmailStr
    message: str

class DeleteUserSchemas(BaseModel):
    email: EmailStr

@app.get("/", response_model=dict)
async def main_page():
    """Главная страница"""
    return {
        "message": "Основная страница магазина",
    }

@app.get("/register", response_model=dict)
async def register_page():
    """Страница регистрации"""
    return {
        "message": "Страница регистрации"
    }

@app.get("/login", response_model=dict)
async def login_page():
    """Страцница авторизации"""
    return {
        "message": "Страница авторизации"
    }

@app.get("/delete-account", response_model=dict)
async def delete_account_page():
    """Удаление акканта"""
    return {
        "message": "Страница удаления аккаунта"
    }

@app.post("/register", response_model=UserSchemas, status_code=status.HTTP_201_CREATED)
async def register_panel(user_info: RegistrationUserSchemas):
    if user_info.password != user_info.reply_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введённые данные не совпадают"
        )

    check_email_in_db = await main_service.check_email_in_db(user_info.email)

    if not check_email_in_db:
        user_data = {
            "name": user_info.name,
            "surname": user_info.surname,
            "email": user_info.email,
            "password": user_info.password
        }

        add_user = await reg_service.data_preparation(user_data)

        if add_user:
            return UserSchemas(
                name=user_info.name,
                surname=user_info.surname,
                email=user_info.email,
                message="Регистрация прошла успешно"
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error with data base"
            ) 
    
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Данная почта уже зарегистрирована"
    )

@app.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login_panel(
    auth_info: AuthorizationUserSchemas
):
    checker, checker_error = await  auth_service.checker_auth(auth_info.email, auth_info.password)
    if not checker and checker_error == "not email":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сначала пройдите регистрацию"
        )
    
    if not checker and checker_error == "not password":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не верно введён пароль!"
        )
    
    if checker_error == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return {
        "message": f"Добро пожаловать {auth_info.email}!",
        "access-token": "fake-jwt-token",
        "token_type": "bearer"
    }

@app.post("/delete-account", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user_info: DeleteUserSchemas
):
    """Эндпоинт для мягкого удаления пользователя"""
    del_account = await del_service.soft_delete_account(user_info.email)

    if not del_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account deletion error"
        )
    
    return {
        "message": f"Вы успешно удалили аккаунт {user_info.email}"
    }


if __name__ == "__main__":

    uvicorn.run("test_login:app", host="127.0.0.1", port=8000, reload=True)