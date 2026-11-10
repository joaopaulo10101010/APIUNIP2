from Connection import Conexao
from Sensor import *
from Funcoes import *

class SensorRepositorio:

    @staticmethod
    def GravarSensores(con:Conexao, sensor:Sensores):

        valida = con.BuscaValor("codigo","nome","tb_sensores",sensor.nome)

        if valida is not None:
            if valida > 0:
                return valida

        query = "INSERT INTO tb_sensores(nome,tipo_valor) VALUES (?, ?)"
        parametros = (sensor.nome, sensor.tipo_valor)
        
        return con.Comando(query,parametros)

    @staticmethod
    def GravarResultadoProcessado(con:Conexao, ResultP:ResultadosProcessados):

        query = "INSERT INTO tb_resultadosProcessados(pacoteRecebido_codigo,valor) VALUES (?, ?)"
        parametros = (ResultP.pacoteRecebido_codigo , ResultP.valor)
        
        return con.Comando(query,parametros)

    @staticmethod
    def GravarPacoteRecebido(con:Conexao, PacoteR:PacotesRecebidos):

        query = "INSERT INTO tb_pacotesRecebidos(data_hora_registro,sensor_codigo,valor) VALUES (?, ?, ?)"
        parametros = (PacoteR.data_hora_registro, PacoteR.sensor_codigo, PacoteR.valor)
        
        return con.Comando(query,parametros)

    @staticmethod
    def GravarSensor(self,con:Conexao, Sensor:Sensor):

        try:

            con.IniciarTransacao()

            self.GravarSensores(Sensor.sensor)
            codigo = self.GravarPacoteRecebido(Sensor.pacotesRecebidos)
            Sensor.resultadosProcessados.pacoteRecebido_codigo = codigo
            self.GravarResultadoProcessado(Sensor.resultadosProcessados)

            con.CommitTransacao()

        except Exception as ex:

            con.VoltarTransacao()
            ExibeErro(ex,con,"Erro ao Gravar o Sensor. Origem SensorRepositorio.py")

    @staticmethod
    def SensorLista(con:Conexao,sensornome:str):

        try:

            registros = con.execute(f"""
            SELECT
                p.codigo AS pacote_codigo,
                p.data_hora_registro AS data_hora_registro,
                s.codigo AS sensor_codigo,
                s.nome AS sensor_nome,
                s.tipo_valor AS tipo_valor,
                p.valor AS valor_original,
                r.codigo AS resultado_codigo,
                r.valor AS valor_processado
            FROM tb_pacotesRecebidos p
            INNER JOIN tb_sensores s ON p.sensor_codigo = s.codigo
            INNER JOIN tb_resultadosProcessados r ON r.pacoteRecebido_codigo = p.codigo
            where s.nome = ? order by p.codigo desc
            """,sensornome,).fetchall()

            lista: list[Sensor] = []

            for registro in registros:

                sensor = Sensores()
                sensor.codigo = registro["sensor_codigo"]
                sensor.nome = registro["sensor_nome"]
                sensor.tipo_valor = registro["tipo_valor"]

                pacote = PacotesRecebidos()
                pacote.codigo = registro["pacote_codigo"]
                pacote.valor = registro["valor_original"]
                pacote.data_hora_registro = registro["data_hora_registro"]

                resultado = ResultadosProcessados()
                resultado.codigo = registro["resultado_codigo"]
                resultado.valor = registro["valor_processado"]

                obj = Sensor()
                obj.sensor = sensor
                obj.pacotesRecebidos = pacote
                obj.resultadosProcessados = resultado

                lista.append(obj)

            return lista
        
        except Exception as ex:
            ExibeErro(ex,con,"Não foi possivel obter a lista de dados referente ao sensor no metodo SensorLista, classe SensorRepositorio.py")

    def ConsumirDadosJson(self,con:Conexao,sensor,data,valor):
        objsensor = Sensores()
        objsensor.nome = sensor

        objsensor.codigo = self.GravarSensores(con,Sensores)

        objpacoteRecebido = PacotesRecebidos()
        objpacoteRecebido.datahorareceb = data
        objpacoteRecebido.valor = valor
        objpacoteRecebido.sensorcodigo = objsensor.codigo

        objresultPross = ResultadosProcessados()
        objresultPross.valor = self.ProcessarSensor(objsensor.nome,objpacoteRecebido.valor)

        objSensorCompleto = Sensor()

        objSensorCompleto.sensor = objsensor
        objSensorCompleto.pacotesRecebidos = objpacoteRecebido
        objSensorCompleto.resultadosProcessados = objresultPross 

        self.GravarSensor(con,objSensorCompleto)


    @staticmethod
    def ProcessarSensor(self,sensor: str, valor: float) -> float:

        match sensor:
            case "BMP280":
                return self.ConverterBMP280(valor)

            case "DHT22":
                return self.SensorProcessamento.ConverterDHT22(valor)

            case "LDR":
                return self.SensorProcessamento.ConverterLDR(valor)

            case "MQ135":
                return self.SensorProcessamento.ConverterMQ135(valor)

            case _:
                return valor

    @staticmethod
    def ConverterLDR(valor: float):
        porcentagem = (valor / 4095.0) * 100.0
        return round(porcentagem, 2)

    @staticmethod
    def ConverterMQ135(valor: float):
        tensao = (valor / 4095.0) * 3.3
        return round(tensao, 2)

    @staticmethod
    def ConverterBMP280(valor: float):
        return round(valor, 2)

    @staticmethod
    def ConverterDHT22(valor: float):
        return round(valor, 2)





