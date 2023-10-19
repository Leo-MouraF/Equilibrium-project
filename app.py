from flask import Flask, abort, redirect, render_template, request, url_for

from app_service import (
    busca_produto,
    filtrar_produto,
    gerar_novo_produto,
    processa_imagem,
    service_delete_produto,
    update_produto_service,
)

app = Flask(__name__)

if __name__ == "__main__":
    app.run()


@app.route("/")
def index():
    suplementos, produtos_naturais = filtrar_produto()
    return render_template(
        "index.html", suplementos=suplementos, produtos_naturais=produtos_naturais
    )


@app.route("/suplementos")
def suplementos():
    suplementos, produtos_naturais = filtrar_produto()
    return render_template("suplementos.html", suplementos=suplementos)


@app.route("/produtos_naturais")
def produtos_naturais():
    suplementos, produtos_naturais = filtrar_produto()
    return render_template(
        "produtos_naturais.html", produtos_naturais=produtos_naturais
    )


@app.route("/produto/<produto_id>")
def single_produto(produto_id):
    produto = busca_produto(produto_id)

    if produto == None:
        return f"Produto não encontrado", abort(404)
    else:
        return render_template("single_produto.html", produto=produto)


@app.route("/update_produto/<produto_id>", methods=["GET"])
def update_produto(produto_id):
    if request.method == "GET":
        produto = busca_produto(produto_id)

        if produto == None:
            return f"Produto não encontrado", abort(404)
        return render_template("update_produto.html", produto=produto)


@app.route("/apply_update_produto/<produto_id>", methods=["POST"])
def apply_update_produto(produto_id):
    if request.method == "POST":
        produto = busca_produto(produto_id)
        data = request.form
        img_form = request.files["imagem"]
        img, img_type = processa_imagem(img_form)
        produto_novo = update_produto_service(data, produto, img, img_type)
    else:
        return f"Produto não encontrado", abort(404)

    return render_template("single_produto.html", produto=produto_novo)


@app.route("/submit_item", methods=["GET", "POST"])
def submit_item():
    if request.method == "POST":
        data = request.form
        img_form = request.files["imagem"]
        img, img_type = processa_imagem(img_form)
        novo_item = gerar_novo_produto(data, img, img_type)
        id = novo_item["id"]
        return redirect(url_for("single_produto", produto_id=id))
    else:
        return render_template("submit_item.html")


@app.route("/delete_produto/<produto_id>", methods=["POST"])
def delete_produto(produto_id):
    service_delete_produto(produto_id)
    return redirect(url_for("index"))
