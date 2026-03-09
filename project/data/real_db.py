"""
Создать базу данных для сайта использую sqlite3.
При регистрации: имя, почта и пароль вводятся пользователем.
При авторизации: пользователь вводит почту и пароль, после проверяется истонность введённых данных
После чего выводится ошибка про не правильном вводе, если же всё верно указано то переходим в файл profile.html
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn
import sqlite3
import os

app = FastAPI()

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")

static_dir = os.path.join(FRONTEND_DIR, "static")
# image_dir = os.path.join(FRONTEND_DIR, "images")
templates_dir = os.path.join(FRONTEND_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# app.mount("/images", StaticFiles(directory=image_dir), name="images")

app.mount(
    "/static",
    StaticFiles(directory=static_dir),
    name="static"
)

# app.mount(
#     "/images",
#     StaticFiles(directory=image_dir),
#     name="images"
# )

templates = Jinja2Templates(directory=templates_dir)

class DataManager:
    def __init__(self, db_name = "my_database.db"):
        self.db_name = db_name
        print(f"Инициализация БД {self.db_name}")
        self.init_db()

    def init_db(self):
        """ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                        )          
                    ''')    
            
            connection.commit()
            print(f"Создана таблица Users в базе данных: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Ошибка создания таблицы: {e}")
        finally:
            if connection:
                connection.close()

    def add_user(self, user_data):
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            name, email, password = user_data
            """Проверка существоания email в БД"""
            print(f"Добавление данных")
            cursor.execute('''
                    SELECT * FROM Users
                           WHERE email = ?
                           ''', (email,))
            result = cursor.fetchone()

            if result:
                return {
                    "success": False,
                        "error": "Пользователь уже существует"
                }
            else: 
                cursor.execute("INSERT INTO Users (name, email, password) VALUES (?, ?, ?)", (name, email, password,))
                connection.commit()
                return {
                    "success": True,
                    "message": "Пользователь добавлен"
                }
            
        except sqlite3.Error as e:
            print(f"Ошибка добавления данныз: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    def view_all_data(self):
        """ПРОСМОТР ВСЕХ ДАННЫХ В БАЗЕ"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            print("\n" + "="*60)
            print("💾 СОДЕРЖИМОЕ БАЗЫ ДАННЫХ")
            print("="*60)

            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
            print(f"Всего пользователей: {len(users)}")
        
        except sqlite3.Error as e:
            print(f"❌ Ошибка при чтение данных: {e}")
        finally:
            if connection:
                connection.close()

    def check_data(self):
        """ПРОВЕРКА НАЛИЧИЯ ДАННЫХ В ТАБЛИЦАХ"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            tables = ['Users']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table}: {count} записей")

        except sqlite3.Error as e:
            print(f"❌ Ошибка при проверке: {e}")
        finally:
            if connection:
                connection.close()

db = DataManager()

@app.get("/", response_class=HTMLResponse)
async def init_register_page(request: Request):
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

# @app.get("/profile", response_class=HTMLResponse)
# async def profile_page(request: Request):
#     return templates.TemplateResponse(
#         "profile.html", {
#             "request": request
#         }
#     )

@app.post("/register")
async def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):  
    user = []
    user.extend([name, email, password])
    result = db.add_user(user)
    if not result.get("success", False):
        return templates.TemplateResponse(
        "register.html", {
            "request": request,
            "error": "Ошибка регистрации"
            }
        )
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        connection = sqlite3.connect(db.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email,password))
        result = cursor.fetchone()

        if result:
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse(
                "login.html", {
                    "request": request,
                    "error": "Неверный email или пароль"
        }
    )
    except sqlite3.Error as e:
        print(f"Ошибка проверки: {e}")
    finally:
        if connection:
            connection.close()


"""
Пользователь при регистрации вводит имя, почту и пароль, ***: str = Form(...).
Нужно проверить есть ли почта в БД, если есть то отправь ошибку, 
если нет, то перекидываем на авторизацию.

Во время регистрации проверяем email на совпадение с базой данных, 
если такой email сузествует, то проверяем пароль, если правильно ввёден,
то переносимся на profile.html, если нет то остаёмся на странице авторизации 
"""

if __name__ == "__main__":
    uvicorn.run("real_db:app", host="127.0.0.1", port=8000, reload=True)