from flask import Flask , request , render_template , redirect, jsonify
from datetime import datetime, timedelta
from banco_dados import banco as db
import pandas as pd

import json

class Dict2Class(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])

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
    return render_template("mobile/loja.html")

@app.route("/servico" , methods=["GET","POST"])
def servico():
    if request.method == "POST":

        menu_opcao = request.form.get("acao")
        menu_servico = request.form.get("acao_servico")

        if menu_servico:
            if menu_servico == 'Adicionar':
                servico = db.Servico()
                servico.id_cliente = request.form.get("id_cliente")
                servico.nome_completo = request.form.get("nome_completo")
                servico.placa_veiculo = request.form.get("placa_veiculo")
                servico.servico_realizado = request.form.get("servico_realizado")
                servico.obs_servico = request.form.get("obs_servico")

                my_obj = request.form.to_dict()
                atendimento = Dict2Class(my_obj)

                db.novo_servico(servico)

                id_cliente = my_obj["id_cliente"]

                servicos = db.con_servico(int(id_cliente))

                return render_template("mobile/servico_ini_servico.html",atendimento=atendimento,servicos=servicos)

            if menu_servico == 'del':
                id_servico = request.form.get("cod_cliente")
                db.del_servico(id_servico)

        # Se vier formulario secao
        if menu_opcao:

            # Secao - iniciar atendimento
            if menu_opcao == "iniciando_atendimento":
                return render_template("mobile/servico_cad_cliente.html")
            
            if menu_opcao == "iniciando_servico":
                front_atendimento = request.form.get("front_atendimento")

                my_obj = json.loads(front_atendimento)
                atendimento = Dict2Class(my_obj)

                id_cliente = my_obj["id_cliente"]

                servicos = db.con_servico(int(id_cliente))

                return render_template("mobile/servico_ini_servico.html",atendimento=atendimento,servicos=servicos)

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

        if len(id_cliente) > 0:
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