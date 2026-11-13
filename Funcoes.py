from Connection import Conexao
import datetime

def ExibeErro(ex:Exception,con:Conexao,texto="",codigoLog:int = 0):

    msg = ""

    if texto == "":
        msg = str(ex)
    else:
        msg = f"{texto} | Exception: {str(ex)}" 

    ExibeMsg("ERRO",f"{msg}")

    GravarLogBanco(con,"ERRO",msg)

def ExibeInformacao(con:Conexao,texto="",codigoLog:int = 0):

    ExibeMsg("INFO",f"{texto}")

    if codigoLog > 0:
        GravarLogBanco(con,"INFO",texto)


def ExibeMsg(tipo:str,msg:str):

    datahora = datetime.datetime.now()

    print(f"[{datahora.strftime("%d/%m/%Y %H:%M:%S")}] [{tipo}] - {msg}")

def GravarLogBanco(con:Conexao,tipo:str,descricao:str,codigo:int = 0):

    if codigo == 0:
        query = "INSERT INTO tb_log(tipo,descricao) VALUES (?, ?)"
        parametros = (tipo, descricao)
    else:
        query = "INSERT INTO tb_log(tipo,descricao,pacoteRecebido_codigo) VALUES (?, ?)"
        parametros = (tipo, descricao,codigo)
        
    con.Comando(query,parametros)