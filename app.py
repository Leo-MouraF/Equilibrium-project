from flask import Flask, abort, redirect, render_template, request, url_for
from app_service import gerar_novo_produto, ler_o_json, escrever_no_json 


app = Flask(__name__)

if __name__ == "__main__":
    app.run()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/suplementos")
def suplementos():
    return render_template("suplementos.html")


@app.route("/produtos_naturais")
def produtos_naturais():
    return render_template("produtos_naturais.html")


@app.route("/produto/<produto_id>")
def single_produto(produto_id):
    dados = ler_o_json()
    produto = dados.get(produto_id)
    for item in dados:
        if dados[item]["id"] == produto["id"]:
            produto_a_mostrar = dados[item]

    if produto == None:
        abort(404)
    else:
        return render_template("single_produto.html", produto=produto_a_mostrar)


@app.route("/submit_item", methods=["GET", "POST"])
def submit_item():
    if request.method == "POST":
        data = request.form
        novo_item = gerar_novo_produto(data)
        id = novo_item["id"]
        return redirect(url_for("single_produto", produto_id=id))
    else:
        return render_template("submit_item.html")