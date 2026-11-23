import sqlite3
from contextlib import contextmanager

class BancoDeDadosLocal():
    def __init__(self, nome_arquivo = 'techlogsolutions.db'):
        self.nome_arquivo = nome_arquivo
        self.inicializar_banco()

    @contextmanager
    def conectar(self):
        con = sqlite3.connect(self.nome_arquivo)
        try:
            yield con
            con.commit()
        except Exception as e:
            con.rollback()
            raise e
        finally:
            con.close()

    def inicializar_banco(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    senha TEXT NOT NULL
                )
            ''')

        print('Banco Inicializado com Sucesso!')