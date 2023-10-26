import os

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, url_for

from app_service import (
    busca_produto,
    filtrar_produto,
    gerar_novo_produto,
    processa_imagem,
    service_delete_produto,
    update_produto_service,
)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    app.run()


@app.route("/")
def index():
    """
    Endpoint que renderiza a página inicial, separando dinamicamente os produtos
    por suas respectivas categorias (filtrar_produto).
    """

    suplementos, produtos_naturais = filtrar_produto()
    return render_template(
        "index.html", suplementos=suplementos, produtos_naturais=produtos_naturais
    )


@app.route("/login", methods=["GET", "POST"])
def efetuar_login():
    if request.method == "POST":
        data = request.form
        if data.get("email") != os.getenv("EMAIL_ADMIN") or data.get(
            "senha"
        ) != os.getenv("PASSWORD_ADMIN"):
            return f"Credenciais incorretas.", abort(404)
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/suplementos")
def suplementos():
    """
    Endpoint para renderizar os produtos de categoria 'suplemento'.
    É feito o desempacotamento da tupla de dicionários da função filtrar_produto
    porém, utiliza-se somente os itens da categoria de suplementos.

    Return:
    A página específica de suplementos.
    """

    suplementos, produtos_naturais = filtrar_produto()
    return render_template("suplementos.html", suplementos=suplementos)


@app.route("/produtos_naturais")
def produtos_naturais():
    """
    Endpoint para renderizar os produtos da categoria 'produtos naturais'.
    É feito o desempacotamento da tupla de dicionários da função filtrar_produto
    porém, utiliza-se somente os itens da categoria de produtos naturais.

    Return:
    A página específica de produtos naturais.
    """

    suplementos, produtos_naturais = filtrar_produto()
    return render_template(
        "produtos_naturais.html", produtos_naturais=produtos_naturais
    )


@app.route("/produto/<produto_id>")
def single_produto(produto_id):
    """
    Endpoint que renderiza um único produto na página, filtrado pelo seu id.
    """

    produto = busca_produto(produto_id)

    if produto == None:
        return f"Produto não encontrado", abort(404)
    else:
        return render_template("single_produto.html", produto=produto)


@app.route("/update_produto/<produto_id>", methods=["GET"])
def update_produto(produto_id):
    """
    Endpoint que renderiza página com os dados carregados nos respectivos inputs
    para que seja feita possíveis alterações.
    """

    if request.method == "GET":
        produto = busca_produto(produto_id)

        if produto == None:
            abort(404)
        return render_template("update_produto.html", produto=produto)


@app.route("/apply_update_produto/<produto_id>", methods=["POST"])
def apply_update_produto(produto_id):
    """
    Endpoint responsável pela aplicação das alterações feitas no endpoint:
    update_produto.
    """

    if request.method == "POST":
        produto = busca_produto(produto_id)
        data = request.form
        if not "imagem" in request.files or request.files["imagem"].filename == "":
            img = produto["imagem"]["imagem_data"]
            img_type = produto["imagem"]["tipo"]
            produto_novo = update_produto_service(data, produto, img, img_type)
        else:
            img_form = request.files["imagem"]
            img, img_type = processa_imagem(img_form)
            produto_novo = update_produto_service(data, produto, img, img_type)
    else:
        return render_template("update_produto.html", produto=produto)

    return render_template("single_produto.html", produto=produto_novo)


@app.route("/submit_item", methods=["GET", "POST"])
def submit_item():
    """
    Endpoint que renderiza a página para adicionar um novo item.
    Chamando as funções para a inserção dos dados no arquivo json.
    """

    if request.method == "POST":
        data = request.form
        if not "imagem" in request.files or request.files["imagem"].filename == "":
            raise ValueError("Não foi inserida uma imagem.")
        else:
            img_form = request.files["imagem"]
            img, img_type = processa_imagem(img_form)
            novo_item = gerar_novo_produto(data, img, img_type)
            id = novo_item["id"]

        return redirect(url_for("single_produto", produto_id=id))
    else:
        return render_template("submit_item.html")


@app.route("/delete_produto/<produto_id>", methods=["POST"])
def delete_produto(produto_id):
    """
    Endpoint que faz a deleção de determinado item a partir de seu id.
    """

    service_delete_produto(produto_id)
    return redirect(url_for("index"))
