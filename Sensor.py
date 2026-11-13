class Sensores:
    nome = ""
    tipo_valor = ""
    codigo = 0

    def __init__(self, codigo=0, nome="", tipo_valor=""):
        self.codigo = codigo
        self.nome = nome
        self.tipo_valor = tipo_valor


class ResultadosProcessados:
    codigo = 0
    pacoteRecebido_codigo = 0
    valor = 0

    def __init__(self, codigo=0, pacoteRecebido_codigo=0, valor=0):
        self.codigo = codigo
        self.pacoteRecebido_codigo = pacoteRecebido_codigo
        self.valor = valor


class PacotesRecebidos:
    codigo = 0
    sensor_codigo = 0
    data_hora_registro = ''
    valor = 0

    def __init__(self, codigo=0, sensor_codigo=0, data_hora_registro='', valor=0):
        self.codigo = codigo
        self.sensor_codigo = sensor_codigo
        self.data_hora_registro = data_hora_registro
        self.valor = valor


class Sensor:
    sensor = Sensores()
    resultadosProcessados = ResultadosProcessados()
    pacotesRecebidos = PacotesRecebidos()

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