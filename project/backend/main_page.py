from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
users = []

# BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_DIR = os.path.dirname(BACKEND_DIR)

# FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")
# static_dir = os.path.join(FRONTEND_DIR, "static")
# image_dir = os.path.join(FRONTEND_DIR, "images")
# templates_dir = os.path.join(FRONTEND_DIR, "templates")

import os

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")

static_dir = os.path.join(FRONTEND_DIR, "static")
image_dir = os.path.join(FRONTEND_DIR, "images")
templates_dir = os.path.join(FRONTEND_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.mount("/images", StaticFiles(directory=image_dir), name="images")

app.mount(
    "/static",
    StaticFiles(directory=static_dir),
    name="static"
)

app.mount(
    "/images",
    StaticFiles(directory=image_dir),
    name="images"
)

templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return RedirectResponse(url="/main_page")

@app.get("/main_page", response_class=HTMLResponse)
async def main_page(request : Request):
    return templates.TemplateResponse(
        "main_page.html", {
            "request": request
        }
    )

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
    name: str = Form(...),
    email: str = Form(...),
    password = Form(...)
):
    for user in users:
        if user["email"] == email:
            return {
                "status": "error",
                "message": "Такой meail уже используется"
            }
        
    users.append({
        "name": name,
        "email":email,
        "password":password
    })

    print(f"РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОАВТЕЛЯ\nИМЯ: {name}\nEMAIL: {email}\nПароль: {password}")
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    for user in users:
        if user["email"] == email:
            print(f"{email} был найден в БД")

            if user["password"] == password:
                print("пароль верный")
                return RedirectResponse(url="/main_page", status_code=303)
            else:
                print("Паротль неверный")
                return {
                     "status": "error",
                     "message": "Неверный пароль"
                }
    return {
         "status": "error",
         "message": "Email не найден"
    }
             

if __name__ == "__main__":
    uvicorn.run("main_page:app", host="127.0.0.1", port=8000, reload=True)