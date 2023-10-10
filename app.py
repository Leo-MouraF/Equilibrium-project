import json

from flask import Flask, render_template, abort, request, redirect, url_for
from uuid import uuid4

from data.produtos import produtos

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
    produto = produtos.get(produto_id)
    if (produto == None):
        abort(404)
    else:
        return render_template("single_produto.html", produto=produto)

@app.route('/submit_item', methods=['GET', 'POST'])
def submit_item():
    if request.method == 'POST':
        novo_item = gerar_novo_produto()
        id = novo_item['id']
        print(novo_item)
        print(produtos)
        return redirect(url_for('single_produto', produto_id=id))
    else:
        return  render_template('submit_item.html')


def gerar_novo_produto():
    name = str(request.form.get('nome'))
    preco = request.form.get('valor')
    description = str(request.form.get('descricao'))
    category = str(request.form.get('categoria'))
    novo_produto = {
        'id':str(uuid4()),
        'nome':name,
        'preco':preco,
        'descricao':description,
        'categoria':category
    }
    
    produtos_json = ler_o_json()
    escrever_no_json(produtos_json, novo_produto)

    return novo_produto

def escrever_no_json(produtos, novo_produto):
    with open('data/produtos.json', 'a') as arquivo_produtos:
        produtos[novo_produto] = novo_produto
        novo_produto_json = json.dump(produtos, indent=4)
        arquivo_produtos.writelines(novo_produto_json)

def ler_o_json():
    with open('data/produtos.json', 'r') as arquivo_produtos:
        produtos_dicionario = json.load(arquivo_produtos)

        return produtos_dicionario