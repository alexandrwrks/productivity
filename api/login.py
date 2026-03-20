from api.models.base import UsersManager
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from pydantic import EmailStr
from services import Service

app = FastAPI()

app.mount(
    "/static",
    StaticFiles("static"),
    name="static"
)

user_manager = UsersManager()
service = Service()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {
            "request": request
        }
    )

@app.post("/login")
async def login_panel(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    user_data = {
        "email": email,
        "password": password
    }
    
    user_loging = await user_manager.check_email(user_data["email"])
    if not user_loging:
        return templates.TemplateResponse(
            "login.html", {
                "request": request,
                "message": "Ошибка! Снача зарегестрируйтесь"
            }
        )
    
    password_user_loging = await service.verify_password(user_data)
    if not password_user_loging:
        return templates.TemplateResponse(
            "login.html", {
                "request": request,
                "message": "Ввёд неверный пароль!"
            }
        )

    return templates.TemplateResponse(
        "profile.html", {
            "request": request,
            "message": "Авторизация прошла успешно"
        }
    )