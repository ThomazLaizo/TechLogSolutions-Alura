from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.rotas import cliente, login, registro
from app.autenticacao_mddleware import AuthenticationToken

templates = Jinja2Templates(directory= 'templates')

app = FastAPI(
    title = "TechLog Solutions API",
    description = "CRM para TechLog Solutions.",
    version = "1.0.0",
)

app.mount("/static", StaticFiles (directory="static"), name = "static")
app.add_middleware(AuthenticationToken)

app.include_router(cliente.router)
app.include_router(cliente.front_router)
app.include_router(login.router)
app.include_router(registro.router)

@app.get("/health")
async def health_check():
    return {"status" : "OK"}

@app.get("/", response_class = HTMLResponse)
async def front_page(request : Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html", 
        context = {"titulo" : "TechLogSolutions CRM", "versao" : "1.0.0"})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url = "/login", status_code = 303)
    response.delete_cookie("session_token")
    return response