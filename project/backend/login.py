from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
users = []

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.dirname(BACKEND_DIR)

FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")

static_dir = os.path.join(FRONTEND_DIR, "static")

templates_dir = os.path.join(FRONTEND_DIR, "templates")

app.mount(
    "/static",
    StaticFiles(directory=static_dir),
    name="static"
)

templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/register")

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {
            "request": request
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
async def register_user(
    name : str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):  
    for user in users:
        if user["email"] == email:
            return {
                "status": "error",
                "message": "Такой email уже зарегистрирован"
            }
        
    users.append({
        "name":name,
        "email":email,
        "password":password
    })
    print(f"=== РЕГИСТРАЦИЯ ===")
    print(f"Новый пользователь: {name}, {email}")
    print(f"Все пользователи: {users}")
    print(f"===================")
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    print(f"=== ПОПЫТКА ВХОДА ===")
    print(f"Введенный email: {email}")
    print(f"Введенный пароль: {password}")
    print(f"Все пользователи в системе: {users}")

    for user in users:
        print(f"Проверяем пользователя: {user['email']} | Пароль: {user['password']}")
        
        if user["email"] == email:
            print(f"Email найден! Сравниваем пароли...")
            print(f"Пароль из БД: '{user['password']}', Введенный пароль: '{password}'")
            
            if user["password"] == password:
                print("✓ Пароль верный! Вход разрешен")
                return {"status": "success", "message": "Успешный вход!"}
            else:
                print("✗ Пароль неверный")
                return {"status": "error", "message": "Неверный пароль"}
    
    print(f"✗ Email {email} не найден в системе")
    print(f"===================")
    return {"status": "error", "message": "Пользователь не найден"}


if __name__ == "__main__":
    uvicorn.run("login:app",  host="127.0.0.1", port=8000, reload=True)