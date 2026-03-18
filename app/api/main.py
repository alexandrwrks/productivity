# import fastapi
# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# import uvicorn
# import os
# import aiosqlite


# app = FastAPI()


# app.mount(
#     "/static",
#     StaticFiles(directory='static'),
#     name='static'
# )

# templates = Jinja2Templates(directory='templates')

# @app.get("/")
# async def read_item(request: Request):
#     return templates.TemplateResponse(
#         'base.html', {
#             'request': request
#         }
#     )
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Подключаем статические файлы (CSS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="templates")

# Модель товара (соответствует структуре БД)
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: Optional[str] = None

# Тестовые данные (в реальном проекте здесь будет запрос к БД)
def get_products_from_db():
    """Функция, имитирующая получение данных из БД"""
    return [
        Product(id=1, name="Смартфон Galaxy S23", description="Флагманский смартфон с отличной камерой", price=79990, image_url=""),
        Product(id=2, name="Ноутбук AirBook Pro", description="Тонкий и мощный ноутбук для работы", price=129990, image_url=""),
        Product(id=3, name="Беспроводные наушники", description="Шумоподавление, 30 часов работы", price=15990, image_url=""),
        Product(id=4, name="Умные часы Watch 5", description="Следите за здоровьем и тренировками", price=24990, image_url=""),
        Product(id=5, name="Планшет Tab S9", description="Для учебы и развлечений", price=45990, image_url=""),
        Product(id=6, name="Игровая консоль", description="1 ТБ, две игры в комплекте", price=45990, image_url=""),
        Product(id=7, name="Фитнес-браслет", description="Водонепроницаемый, пульсометр", price=3990, image_url=""),
        Product(id=8, name="Внешний аккумулятор", description="20000 mAh, быстрая зарядка", price=2990, image_url=""),
        Product(id=9, name="Bluetooth-колонка", description="Защита от воды, стереозвук", price=4990, image_url=""),
        Product(id=10, name="Мышь беспроводная", description="Тихая, эргономичная", price=1990, image_url=""),
        Product(id=11, name="Клавиатура механическая", description="RGB-подсветка, для игр", price=6990, image_url=""),
        Product(id=12, name="Монитор 27\"", description="4K, IPS-матрица", price=32990, image_url=""),
        Product(id=13, name="SSD диск 1TB", description="NVMe, скорость 3500MB/s", price=8990, image_url=""),
    ]

@app.get("/")
async def root(request: Request):
    # Получаем товары из БД
    products = get_products_from_db()
    
    # Передаем товары в шаблон
    return templates.TemplateResponse(
        "base.html", 
        {
            "request": request, 
            "products": products
        }
    )

@app.get("/catalog")
async def catalog(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})

@app.get("/profile")
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)