from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel, EmailStr
from test_service import test_service
from test_base import test_base
from contextlib import asynccontextmanager

import uvicorn
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await test_base.init_db()
    yield

app = FastAPI(title="Мой магазин на FastAPI", lifespan=lifespan)

class RegistrationUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    reply_password: str

    def check_password_match(self):
        if self.password != self.reply_password:
            raise ValueError("Пароли не совпадают")

class AuthorizationUser(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str | None = None
    message: str

@app.get("/", response_model=dict)
async def main_page():
    """Главная страница"""
    return {
        "message": "Основная страница магазина",
    }

@app.get("/register")
async def register_page():
    return {
        "message": "Страница регистрации"
    }

@app.get("/login")
async def login_page():
    return {
        "message": "Страница авторизации"
    }

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_panel(user_info: RegistrationUser):
    if user_info.password != user_info.reply_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введённые данные не совпадают"
        )
    
    if len(user_info.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать минимум 6 символов"
        )

    user_data = {
        "name": user_info.name,
        "surname": user_info.surname,
        "email": user_info.email,
        "password": user_info.password
    }

    await test_service.data_preparation(user_data)

    return UserResponse(
        name=user_info.name,
        surname=user_info.surname,
        email=user_info.email,
        message="Региситрация прошла успешна"
    )

@app.post("/login", response_model=dict)
async def login_panel(
    auth_info: AuthorizationUser
):
    checker, checker_error = await test_service.checker_auth(auth_info.email, auth_info.password)
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
    

    return {
        "message": f"Добро пожаловать {auth_info.email}!",
        "access-token": "fake-jwt-token",
        "token_type": "bearer"
    }


if __name__ == "__main__":

    uvicorn.run("test_login:app", host="127.0.0.1", port=8000, reload=True)