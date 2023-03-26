from flask import Flask , request , render_template , redirect

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