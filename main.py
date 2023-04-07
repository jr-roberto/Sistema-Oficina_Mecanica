from flask import Flask , request , render_template , redirect
from datetime import datetime, timedelta
import pandas as pd

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
        return render_template("web/login.html")

@app.route("/loja")
def loja():
    # Verifica - Plataform
    plataform = request.user_agent.string.lower()
    ip_client = request.remote_addr

    if log_secao(ip_client) == False:
        return redirect("/")

    if "android" in plataform:
        return render_template("mobile/loja.html")

    else:
        return render_template("web/loja.html")

@app.route("/servico")
def servico():
    return render_template("mobile/servico.html")

@app.route("/cliente")
def cliente():
    return render_template("mobile/cliente.html")

@app.route("/pesquisa_cliente/<cpf>")
def pesq_cliente(cpf):
    return {"resposta":f"O servidor recebeu : {cpf}"}

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")