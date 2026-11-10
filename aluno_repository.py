import sqlite3
from aluno import Aluno

class AlunoRepository:

    def __init__(self, banco="alunos.db"):
        self.banco = banco
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.banco)
        conexao.row_factory = sqlite3.Row
        return conexao
    
    def criar_tabela(self):

        conexao = self.conectar()

        try:
            conexao.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            curso TEXT NOT NULL
            )
            """)
            conexao.commit()

        finally:
            conexao.close()

    def cadastrar(self, aluno):

        conexao = self.conectar()

        try:
            conexao.execute("""
            INSERT INTO alunos (nome, email, curso)
            VALUES (?, ?, ?)
            """, (aluno.nome, aluno.email, aluno.curso))
            conexao.commit()

        finally:
            conexao.close()

    def listar(self):

        conexao = self.conectar()

        try:
            registros = conexao.execute("""
            SELECT id, nome, email, curso
            FROM alunos
            ORDER BY id DESC
            """).fetchall()
            return [
            Aluno(
            id=registro["id"],
            nome=registro["nome"],
            email=registro["email"],
            curso=registro["curso"],
            )
            for registro in registros
            ]
        
        finally:
            conexao.close()

    def buscar_por_id(self, id):

        conexao = self.conectar()

        try:
            registro = conexao.execute("""
            SELECT id, nome, email, curso
            FROM alunos
            WHERE id = ?
            """, (id,)).fetchone()

            if registro is None:
                return None
            
            return Aluno(
            id=registro["id"],
            nome=registro["nome"],
            email=registro["email"],
            curso=registro["curso"],
            )
        
        finally:
            conexao.close()

    def atualizar(self, aluno):

        conexao = self.conectar()
        
        try:
            cursor = conexao.execute("""
            UPDATE alunos
            SET nome = ?, email = ?, curso = ?
            WHERE id = ?
            """, (aluno.nome, aluno.email, aluno.curso, aluno.id))
            conexao.commit()
            return cursor.rowcount > 0
        
        finally:
            conexao.close()

    def excluir(self, id):

        conexao = self.conectar()

        try:
            cursor = conexao.execute(
            "DELETE FROM alunos WHERE id = ?",
            (id,),
            )
            conexao.commit()
            return cursor.rowcount > 0
        finally:
            conexao.close()