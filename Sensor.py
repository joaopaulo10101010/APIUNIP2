class Sensores:
    def __init__(self, codigo=0, nome="", tipo_valor="double"):
        self.codigo = codigo
        self.nome = nome
        self.tipo_valor = tipo_valor

class ResultadosProcessados:
    def __init__(self, codigo=0, pacoteRecebido_codigo=0, valor=0):
        self.codigo = codigo
        self.pacoteRecebido_codigo = pacoteRecebido_codigo
        self.valor = valor

class PacotesRecebidos:
    def __init__(self, codigo=0, sensorcodigo=0, datahorarecebi=0,valor = 0):
        self.codigo = codigo
        self.sensorcodigo = sensorcodigo
        self.datahorareceb = datahorarecebi
        self.valor = valor

class Sensor:
    def __init__(self, _sensor=Sensores(), _pacotesRecebidos=PacotesRecebidos(), _resultadosProcessados=ResultadosProcessados()):
        self.sensor = _sensor
        self.resultadosProcessados = _resultadosProcessados
        self.pacotesRecebidos = _pacotesRecebidos

    def GetNome(self):
        return self.sensor.nome

    def GetTipoValot(self):
        return self.sensor.tipo_valor

    def GetValorProcessado(self):
        return self.resultadosProcessados.valor

    def GetValorRecebido(self):
        return self.pacotesRecebidos.valor

    def GetDataHoraRecebida(self):
        return self.pacotesRecebidos.data_hora_registro
