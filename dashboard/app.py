from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="ARCHON Dashboard",
    description="Archaeological Site Monitoring System"
)

app.mount(
    "/static",
    StaticFiles(directory="dashboard/static"),
    name="static"
)

templates = Jinja2Templates(directory="dashboard/templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/api/health")
async def health():
    return {
        "system": "ARCHON",
        "status": "ONLINE",
        "message": "Dashboard is running"
    }