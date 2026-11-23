from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    id_: int
    nome: str
    email: EmailStr
    senha: str | None = None

class UsuarioCriarAtualizar(BaseModel):
    nome: str
    email: EmailStr
    senha: str | None = None