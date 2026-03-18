from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import fastapi
import uvicorn

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/register")

@app.get("/register", response_class=HTMLResponse)
async def reg_page(request: Request):
    return templates.TemplateResponse(
        "reg.html", {
            "request" : request
        }
    )

@app.post("/register")
async def reg_panel(
    name: str = Form(...),
    surname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    replay_password: str = Form(...)
):
    