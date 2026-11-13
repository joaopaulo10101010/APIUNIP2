import sqlite3

class Conexao:

    nomeDoBanco = "unipBD"

    QueryBanco = """
    CREATE TABLE IF NOT EXISTS tb_sensores(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(30) NOT NULL,
        tipo_valor VARCHAR(30) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS tb_pacotesRecebidos(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora_registro DATETIME NOT NULL,
        sensor_codigo INTEGER NOT NULL,
        valor DOUBLE NOT NULL DEFAULT 0,
        FOREIGN KEY(sensor_codigo) REFERENCES tb_sensores(codigo)
    );

    CREATE TABLE IF NOT EXISTS tb_resultadosProcessados(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        pacoteRecebido_codigo INTEGER NOT NULL,
        valor DOUBLE NOT NULL DEFAULT 0,
        FOREIGN KEY(pacoteRecebido_codigo) REFERENCES tb_pacotesRecebidos(codigo)
    );

    CREATE TABLE IF NOT EXISTS tb_log(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora_log DATETIME DEFAULT CURRENT_TIMESTAMP,
        descricao VARCHAR(500) DEFAULT '',
        tipo VARCHAR(30) NOT NULL,
        pacoteRecebido_codigo INTEGER,
        FOREIGN KEY(pacoteRecebido_codigo) REFERENCES tb_pacotesRecebidos(codigo)
    );
    """

    def __init__(self):
        self.iniciarBanco()

    def conectar(self):
        conexao = sqlite3.connect(self.nomeDoBanco)
        conexao.row_factory = sqlite3.Row
        return conexao
    
    def iniciarBanco(self):

        conexao = self.conectar()

        try:
            conexao.executescript(self.QueryBanco)
            conexao.commit()

        except:
            raise Exception("Ocorreu um erro ao tentar rodar o Script de criação do Banco de dados.")

        finally:
            conexao.close()

    def Comando(self, comando: str, parametro=()):

        con = None

        try:
            con = self.conectar()

            cursor = con.cursor()

            if parametro == ():
                cursor.execute(comando)
            else:
                cursor.execute(comando, parametro)

            con.commit()

            return cursor.lastrowid

        finally:
            if con is not None:
                con.close()

    def BuscaValor(self,campo: str,chave: str,tabela: str,valor,clasula:str = ""):
        
        try:

            con = self.conectar()
            query = f"{campo} AS CAMPO, {chave} AS CHAVE FROM {tabela} WHERE {chave} IN (?)"

            if clasula != "":
                query += " " + clasula

            retorno = con.execute(query,chave).fetchone()

            if retorno is None:
                return None
            
            return retorno ["CAMPO"]

        except Exception as ex:

            return None

        finally:
            con.close()

    def BuscaTodos(self, comando: str, parametros=()):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(comando, parametros)
            return cursor.fetchall()
        finally:
            conexao.close()

    def IniciarTransacao(self):
        self.conexao = self.conectar()
        self.conexao.execute("BEGIN")

    def CommitTransacao(self):
        self.conexao.commit()

    def VoltarTransacao(self):
        self.conexao.rollback()

    
    