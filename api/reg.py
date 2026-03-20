from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from pydantic import EmailStr
from api.services import service
from api.models.base import user_manager
import asyncio

"""Что должно быть:

    GET /register — показать HTML форму

    POST /register — принять данные из формы

    Вызвать метод service.py для регистрации

    Вернуть либо страницу с ошибкой, либо редирект на успех

    Обработать HTTP ошибки (404, 500 и т.д.)

Чего НЕ должно быть:

    Проверок пароля (это работа service.py)

    Хеширования (это работа service.py)

    SQL запросов (это работа base.py)

    Бизнес-логики"""

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    await user_manager.init_db()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/register")

@app.get("/register", response_class=HTMLResponse)
async def reg_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {
            "request" : request,
            "data": {}
        }
    )
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {
            "request": request
        }
    )

@app.post("/register")
async def reg_panel(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    reply_password: str = Form(...)
):
    form_data = {
        "name": name,
        "surname": surname,
        "email": email
    }

    user_data = {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password,
        "reply_password": reply_password
    }

    success = await service.register_user(user_data)

    if success:

        return RedirectResponse(
            url="/login?registered=true",
            status_code=303
        )
    else:
        
        return templates.TemplateResponse(
           "register.html",
           {
               "request": request,
               "data": form_data
           },
           status_code=422
        )

@app.post("/login")
async def login_panel(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    user_exists = await user_manager.check_email(email)

    if not user_exists:
        return templates.TemplateResponse(
            "login.html", {
                "request": request,
                "error": "Пользователь с таким email не найден, Пожалуйста зарегистрируйтесь"
            }
        )
    
    password_valid = await service.verify_password(password, email)

    if not password_valid:
        return templates.TemplateResponse(
            "login.html", {
                "request": request,
                "email": email,
                "error": "Неверный пароль. Пожалуйста, попробуйте снова."
            }
        )
    
    user_info = await user_manager.get_user_by_email(email)

    return templates.TemplateResponse(
        "profile.html", {
            "request": request,
            "user": user_info,
            # "message": f"Добро пожаловать, {user_info["name"]} {user_info["surname"]}"
        }
    )