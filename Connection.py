import sqlite3

class Conexao:

    nomeDoBanco = "unipBD"

    QueryBanco = """
    create table if not exists tb_sensores(
        codigo int auto_increment not null,
        nome varchar(30) not null,
        tipo_valor varchar(30) not null,
        primary key(codigo)
    );

    create table if not exists tb_pacotesRecebidos(
        codigo int auto_increment not null,
        data_hora_registro datetime not null,
        sensor_codigo int not null,
        valor double not null default 0,
        primary key(codigo),
        foreign key(sensor_codigo) references tb_sensores(codigo)
    );

    create table if not exists tb_resultadosProcessados(
        codigo int auto_increment not null,
        pacoteRecebido_codigo int not null,
        valor double not null default 0,
        primary key(codigo),
        foreign key(pacoteRecebido_codigo) references tb_pacotesRecebidos(codigo)
    );

    create table if not exists tb_log(
        codigo int auto_increment,
        data_hora_log datetime default CURRENT_TIMESTAMP,
        descricao varchar(500) default '',
        tipo varchar(30) not null,
        pacoteRecebido_codigo int,
        primary key(codigo),
        foreign key(pacoteRecebido_codigo) references tb_pacotesRecebidos(codigo)
    );"""

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

    def Comando(self,comando:str,parametro = ()):

        try:

            con = self.conectar()

            cursor = con.cursor()

            if parametro == ():
                con.execute(comando)
            else:
                con.execute(comando,parametro)

            return cursor.lastrowid

        finally:
            con.close()

    def BuscaValor(self,campo: str,chave: str,tabela: str,valor,clasula:str = ""):
        
        try:

            con = self.conectar()

            query = f"{campo} AS CAMPO, {chave} AS CHAVE FROM {tabela} WHERE {chave} IN (?)"

            if clasula != "":
                query += " " + clasula

            retorno = con.execute(query).fetchone()

            if retorno is None:
                return None
            
            return retorno ["CAMPO"]

        except:

            return None

        finally:
            con.close()

    def IniciarTransacao(self):
        self.conexao.start_transaction()

    def CommitTransacao(self):
        self.conexao.commit()

    def VoltarTransacao(self):
        self.conexao.rollback()
    