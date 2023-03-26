from flask import Flask , request , render_template , redirect
from datetime import datetime, timedelta

def log_secao(ip_alvo):
    agora = datetime.now().timestamp()
    fim = agora + timedelta(minutes=5)

    with open("banco_dados/_logSecao.txt") as file:
        rows = file.read().split("\n")

    lista_ip = []
    for ln in rows:
        if ln[0] != "":
            cols = ln.split(";")

            ip = cols[0]
            ini_sec = cols[1]
            fim_sec = cols[2]

            lista_ip.append(ip)

            if ip_alvo in lista_ip:
                if fim_sec < agora:
                    ini_sec_novo = agora
                    fim_sec_novo = fim

                    cols[1] = ini_sec_novo
                    cols[2] = fim_sec_novo

                    remover_ln = ln
                    adiciona_ln = [ip,ini_sec_novo,fim_sec_novo]


            input(lista_ip)

    ip = ""

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


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")