from pydantic import BaseModel, EmailStr

class Cliente(BaseModel):
    id_: int
    nome: str
    email: EmailStr
    telefone: str

class ClienteCriarAtualizar(BaseModel):
    nome: str
    email: EmailStr
    telefone: str