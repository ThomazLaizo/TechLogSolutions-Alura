from app.banco_de_dados.local import BancoDeDadosLocal
from app.modelos.usuario import Usuario, UsuarioCriarAtualizar


class UsuarioRepositorio:
    def __init__(self, banco_de_dados: BancoDeDadosLocal):
        self.db = banco_de_dados

    async def buscar_usuario_email_senha(self, email : str, senha : str) -> Usuario | None:
           with self.db.conectar() as conexao:
               cursor = conexao.cursor()
               cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
               linha = cursor.fetchone()
               if linha:
                    return [Usuario(id_ = linha[0], nome = linha[1], email = linha[2], senha = linha[3])]
               return None

    async def buscar_usuario_email(self, email : str) -> Usuario | None:
           with self.db.conectar() as conexao:
               cursor = conexao.cursor()
               cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
               linha = cursor.fetchone()
               if linha:
                    return [Usuario(id_ = linha[0], nome = linha[1], email = linha[2])]
               return None 

           
    async def add_usuario(self, usuario : UsuarioCriarAtualizar) -> Usuario:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)", (usuario.nome, usuario.email, usuario.senha))
            usuario_id = cursor.lastrowid
            return Usuario(id_ = usuario_id, nome = usuario.nome, email = usuario.email, senha = usuario.senha)