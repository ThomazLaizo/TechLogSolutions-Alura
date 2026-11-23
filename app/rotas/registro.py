from fastapi import Depends, APIRouter, HTTPException, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencias import obter_usuario_repositorio
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.modelos.usuario import UsuarioCriarAtualizar
from typing import Annotated

router = APIRouter(
    prefix = "/registro"
)

templates = Jinja2Templates(directory= 'templates')

@router.get("/", response_class = HTMLResponse)
async def pagina_registro(request : Request):
    return templates.TemplateResponse(
        request = request,
        name = "registro.html"
    )

@router.post("/")
async def registrar_usuario(usuario_repositorio : Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)], request : Request, nome = Form(...), email = Form(...), senha = Form(...), confirma_senha = Form(...)):
    data = {
        "nome" :  nome,
        "email" : email,
        "senha" : senha,
        "confirma_senha" : confirma_senha
    }

    if not all([nome, email, senha, confirma_senha]):
        return templates.TemplateResponse(
        request = request,
        context = {"error" : "Campos obrigatórios faltantes.",
                   **data
                   })

    usuario_existente = await usuario_repositorio.buscar_usuario_email(email)
    if usuario_existente:
        return templates.TemplateResponse(
        name = "registro.html",
        request = request,
        context = {"error" : "Usuário Inválido.",
                   **data
                    })

    usuario_criar = UsuarioCriarAtualizar(nome = nome, email = email, senha = senha)
    usuario = await usuario_repositorio.add_usuario(usuario_criar)

    if usuario: 
        response = RedirectResponse(url = "/login", status_code = 303)
        return response
    return templates.TemplateResponse(
        name = "registro.html",
        request = request,
        context = {"error" : "Não foi possível criar o usuário, tente novamente mais tarde.",
                   **data
                   })