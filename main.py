from flask import Flask,request , render_template

app  = Flask(__name__)

@app.route("/")
def index():

    # Tela inicial do sistema
    # Verifica - Plataform
    plataform = request.user_agent.string.lower()

    if "android" in plataform:
        return render_template("mobile/login.html")

    else:
        return render_template("web/login.html")

    # Entrando no sistema
    if request.method == "POST":
        return render_template("Ir para tela principal do sistema - (Cliente) ou (Funcionario)")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")