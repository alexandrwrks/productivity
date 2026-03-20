from login import app as login_app
from reg import app as reg_app
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(reg_app)
app.include_router(login_app)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="/static"
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def setup_market(
    request: Request
):
    return RedirectResponse(
        url="/market"
    )

@app.post("/market")
async def market(
    request: Request
):
    return templates.TemplateResponse(
        "market.html", {
            "request": Request
        }
    )