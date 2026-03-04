from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Подключаем статические файлы (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="templates")

# Здесь будет ваша БД (вы сказали, что уже сделали)
# Пример простой БД в памяти:
tasks_db = [
    {"id": 1, "title": "Задача 1", "completed": False},
    {"id": 2, "title": "Задача 2", "completed": True},
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница"""
    completed = sum(1 for task in tasks_db if task["completed"])
    total = len(tasks_db)
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "tasks": tasks_db,
            "completed": completed,
            "total": total
        }
    )

@app.post("/add")
async def add_task(title: str = Form(...)):
    """Добавление новой задачи"""
    new_id = len(tasks_db) + 1
    tasks_db.append({"id": new_id, "title": title, "completed": False})
    # return {"status": "ok", "task": tasks_db[-1]}
    return RedirectResponse(url="/", status_code=303)

@app.post("/complete/{task_id}")
async def complete_task(task_id: int):
    """Отметка задачи как выполненной"""
    for task in tasks_db:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]  # Переключаем статус 
            # return {"status": "ok", "task": task}      
            return RedirectResponse(url="/", status_code=303)
    # return {"status": "error", "message": "Task not found"}
    return RedirectResponse(url="/", status_code=303    )

@app.post("/delete/{task_id}")
async def delete_task(task_id: int):
    """Удаление задачи"""
    global tasks_db
    tasks_db = [task for task in tasks_db if task["id"] != task_id]
    # return {"status": "ok"}
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)