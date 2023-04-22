from flask import Flask , request , render_template , redirect, jsonify
from datetime import datetime, timedelta
from banco_dados import banco as db
import pandas as pd

import json

# Veerifica se secao é valida 
def log_secao(ip_alvo):
    agora = datetime.now()

    # Definir o tempo maximo para sessao valida
    fim = int((agora + timedelta( minutes=30 )).strftime("%Y%m%d%H%M%S"))
    agora = int(agora.strftime("%Y%m%d%H%M%S"))

    df = pd.read_csv("banco_dados/log_secao.csv",sep=";")    

    values = list(df.values)

    lista_ip = list(df["endereco_ip"])

    if ip_alvo not in lista_ip:
        values.append([ip_alvo,agora,fim])
        salvar_log(values)
        return False

    if ip_alvo in lista_ip:
        query = df[(df["endereco_ip"]==ip_alvo)]
        fim_sec = query["fim_secao"].values[0]

        if fim_sec > agora:
            return True
        else:
            df.loc[query.index[0],['inicio_sec','fim_secao']] = [agora,fim]
            values = df.values
            salvar_log(values)
            return False

def salvar_log(base):
    columns = ['endereco_ip','inicio_sec','fim_secao']
    values = base
    df_novo = pd.DataFrame(data=values,columns=columns)
    return df_novo.to_csv("banco_dados/log_secao.csv",sep=";", index=False)

app  = Flask(__name__)
app.route("static/img/moto.png")
app.route("static/img/carro.png")
app.route("static/img/undefined.png")
app.route("static/img/adicionar.png")

@app.route("/", methods=['POST','GET'])
def index():
    # Tela inicial do sistema
    # Verifica - Plataform
    plataform = request.user_agent.string.lower()

    if request.method == "POST":
        form_front = request.form.to_dict()
        tipo_usuario = form_front['tipo_usuario']
        usuario = form_front['usuario']

        if tipo_usuario == "funcionario":
            rota_destino = "loja"
        else:
            rota_destino = "cliente"

        return redirect(f"/{rota_destino}")

    if "android" in plataform:
        return render_template("mobile/login.html")

    else:
        return render_template("mobile/login.html")

@app.route("/loja")
def loja():
    # Verifica - Plataform
    plataform = request.user_agent.string.lower()
    ip_client = request.remote_addr

    print(plataform)

    if log_secao(ip_client) == False:
        return redirect("/")

    if "android" in plataform or "iphone" in plataform:
        return render_template("mobile/loja.html")

    else:
        return render_template("mobile/loja.html")

@app.route("/servico" , methods=["GET","POST"])
def servico():

    if request.method == "POST":
        acao_usuario = request.form.get("acao")

        # Se vier formulario secao
        if acao_usuario:

            # Secao - iniciar atendimento
            if acao_usuario == "iniciando_atendimento":
                return render_template("mobile/servico_cad_cliente.html")
            
            if acao_usuario == "iniciando_servico":
                return render_template("mobile/servico_ini_servico.html")

        d_atendimento = request.form

        id_cliente = d_atendimento.get('idUsuario')

        # Cadastrando novo usuario
        if id_cliente == 'Novo Usuario':
            
            novo_usuario = db.Usuario(
                nome_completo=d_atendimento.get('nome_completo'),
                contato=d_atendimento.get('contato'),
                cpf_acesso=d_atendimento.get('cpf_acesso'),
                tipo_usuario=d_atendimento.get('tipo_usuario')
            )
            
            db.novo_usuario(novo_usuario)

        id_cliente = db.ver_usuario_detalhes(d_atendimento.get('cpf_acesso'))

        veiculo = db.Veiculo(
            tipo_veiculo=d_atendimento.get('tipo_veiculo'),
            cor_veiculo=d_atendimento.get('cor_veiculo'),
            placa_veiculo=d_atendimento.get('placa_veiculo')
        )
        
        db.novo_veiculo( id_cliente=id_cliente[0][0] , veiculo=veiculo)
        
        resposta = d_atendimento.to_dict()
        resposta = json.dumps(resposta)
        
        return render_template("mobile/servico.html", atendimento=resposta )

    return render_template("mobile/servico.html")

@app.route("/cliente")
def cliente():
    return render_template("mobile/cliente.html")

@app.route("/pesquisa_cliente/<cpf>")
def pesq_cliente(cpf):
    resposta = db.ver_usuario_detalhes(cpf_usuario=cpf)
    return jsonify(resposta)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")