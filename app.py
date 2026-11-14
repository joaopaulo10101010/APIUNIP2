from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from Sensor import *
from SensorRepositorio import *
from Funcoes import *
from Connection import Conexao
import datetime

app = Flask(__name__)
app.secret_key = "chave123"

con = Conexao()
sensor = SensorRepositorio()


@app.route("/lista/<string:componente>", methods=["GET"])
def lista(componente):

    if componente == "":
        componente = "LDR"

    ExibeInformacao(con, f"Carregando página {componente}")

    lista = sensor.SensorLista(con, componente)

    medias = SensorRepositorio.SensorMediaDiaria(
        con,
        componente
    )

    unidades = {
        "LDR": "%",
        "MQ135": "V",
        "BMP280": "hPa",
        "DHT22": "°C",
        "LDRTEMP": "°C"
    }

    if componente == "LDR":
        pagina = f"index.html"
    else:
        pagina = f"{componente}.html"

    return render_template(
        pagina,
        lista=lista,
        medias=medias,
        unidade=unidades.get(componente, "")
    )

@app.route("/", methods=["GET"])
def inicio():
    return redirect(url_for("lista",componente="LDR"))

@app.route("/sensor/insert", methods=["POST"])
def receber_sensor():

    try:

        ExibeInformacao(con,"Recebendo pacotes externos...")

        dados = request.get_json()

        sensore = dados["Sensor"]
        horadoregistro = datetime.datetime.now()
        valorcoletado = dados["VALORCOLETADO"]     

        ExibeInformacao(con,f"Pacote recebido com sucesso. SENSOR: {sensore}, HORA: {horadoregistro}, VALOR: {valorcoletado} - {dados}")

        SensorRepositorio.ConsumirDadosJson(con,sensore,horadoregistro,valorcoletado)
        ExibeInformacao(con, "Pacote salvo no banco de dados.")

        return jsonify({"mensagem": "Dados recebidos com sucesso!"})

    except Exception as ex:

        ExibeErro(ex,con,"Erro no EndPoint receber sensor")
        return jsonify({"mensagem": "Erro no envio"})

    finally:

        ExibeInformacao(con,"Encerrando rotina recebimento...")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)