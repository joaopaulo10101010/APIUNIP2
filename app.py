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

    if componente != "" and componente != "LDR":

        lista = sensor.SensorLista(con, componente)
        return render_template(f"{componente}.html", sensor=lista)
    
    else:

        lista = sensor.SensorLista(con, "LDR")
        return render_template("index.html", sensor=lista)

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

        sensor.ConsumirDadosJson(con,sensore,horadoregistro,valorcoletado)

        return jsonify({"mensagem": "Dados recebidos com sucesso!"})

    except Exception as ex:

        ExibeErro(str(ex),con)
        return jsonify({"mensagem": "Erro no envio"})

    finally:

        ExibeInformacao("Encerrando rotina recebimento...")

# @app.route("/", methods=["GET", "POST"])
# def inicio():

#     if request.method == "POST":

#         nome = request.form.get("nome", "").strip()
#         email = request.form.get("email", "").strip()
#         curso = request.form.get("curso", "").strip()

#         if not nome or not email or not curso:
#             flash("Preencha todos os campos para cadastrar o aluno.", "erro")
#             return redirect(url_for("inicio"))

#         novo_aluno = Aluno(
#         id=None, 
#         nome=nome,
#         email=email,
#         curso=curso,
#         )

#         repositorio.cadastrar(novo_aluno)
#         flash("Aluno cadastrado com sucesso!", "sucesso")
#         return redirect(url_for("inicio"))
    
#     alunos = repositorio.listar()
#     return render_template("index.html", alunos=alunos)

# @app.route("/editar/<int:id>", methods=["GET", "POST"])
# def editar(id):
#     aluno = repositorio.buscar_por_id(id)

#     if aluno is None:
#         return render_template("nao_encontrado.html"), 404
    
#     if request.method == "POST":
#         nome = request.form.get("nome", "").strip()
#         email = request.form.get("email", "").strip()
#         curso = request.form.get("curso", "").strip()

#         if not nome or not email or not curso:
#             flash("Preencha todos os campos.", "erro")
#             return render_template("editar.html", aluno=aluno)

#         aluno.nome = nome
#         aluno.email = email
#         aluno.curso = curso

#         repositorio.atualizar(aluno)

#         flash("Dados do aluno atualizados com sucesso!", "sucesso")

#         return redirect(url_for("inicio"))
    
#     return render_template("editar.html", aluno=aluno)

# @app.route("/excluir/<int:id>", methods=["POST"])
# def excluir(id):

#     excluido = repositorio.excluir(id)

#     if excluido:
#         flash("Aluno excluído com sucesso.", "sucesso")
#     else:
#         flash("O aluno não foi encontrado.", "erro")

#     return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)