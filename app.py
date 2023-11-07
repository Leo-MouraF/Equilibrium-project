import os

from dotenv import load_dotenv
from flask import (Flask, abort, redirect, render_template, request, session,
                   url_for)

from app_service import (busca_produto, filtrar_produto, gerar_novo_produto,
                         processa_carrinho, processa_hidden_input,
                         processa_imagem, service_delete_produto,
                         update_produto_service, verificar_login)

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.secret_key = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    app.run()


@app.before_request
def antes_da_solicitacao():
    session.modified = True

@app.route("/")
def index():
    """
    Endpoint que renderiza a página inicial, separando dinamicamente os produtos
    por suas respectivas categorias (filtrar_produto).
    """
    email = ''
    if 'carrinho' not in session:
        session['carrinho'] = {}
    
    if 'email' in session:
        email = session['email']
        suplementos, produtos_naturais = filtrar_produto()
        return render_template(
            "index.html", 
            suplementos=suplementos, 
            produtos_naturais=produtos_naturais,
            email=email
        )
    else: 
        suplementos, produtos_naturais = filtrar_produto()
        return render_template(
            "index.html", 
            suplementos=suplementos, 
            produtos_naturais=produtos_naturais
            )


@app.route("/login", methods=["GET", "POST"])
def efetuar_login():
    """
    Endpoint para realização do login, com email e senha.
    """
    if request.method == "POST":
        data = request.form
        if data['email'] == "" or data['senha'] == "":
            raise ValueError('Um dos campos está vazio.')
        else:
            verificar_login(data)
            session['email'] = data['email']
            return redirect(url_for("index"))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

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
            img = produto["imagem"]
            produto_novo = update_produto_service(data, produto, img)
        else:
            img_form = request.files["imagem"]
            file_name = os.path.join(app.config['UPLOAD_FOLDER'], img_form.filename)
            img_form.save(file_name)
            img = processa_imagem(file_name)
            produto_novo = update_produto_service(data, produto, img)
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
            file_name = os.path.join(app.config['UPLOAD_FOLDER'], img_form.filename)
            img_form.save(file_name)
            img = processa_imagem(file_name)
            novo_item = gerar_novo_produto(data, img)

        return redirect(url_for("single_produto", produto_id=novo_item))
    else:
        return render_template("submit_item.html")


@app.route("/delete_produto/<produto_id>", methods=["POST"])
def delete_produto(produto_id):
    """
    Endpoint que faz a deleção de determinado item a partir de seu id.
    """

    service_delete_produto(produto_id)
    return redirect(url_for("index"))


@app.route("/adicionar_ao_carrinho", methods=['GET', 'POST'])
def adicionar_ao_carrinho():
    preco_total = session.get('preco_total', 0)
    if request.method == 'POST':
        data = request.form
        item_processado = processa_hidden_input(data)
        item_processado['preco'] = float(item_processado['preco'])
        if item_processado['id'] not in session['carrinho']:
            session['carrinho'].update({
                item_processado['id']:{
                'id':item_processado['id'], 
                'nome':item_processado['nome'],
                'preco':item_processado['preco'],
                'descricao': item_processado['descricao'],
                'categoria': item_processado['categoria'],
                }
                })
            preco_total += item_processado['preco']
            session['preco_total'] = preco_total
            print(session['carrinho'])
        return redirect(request.referrer)
    
    if not session['carrinho']:
        preco_total = session.pop('preco_total', None)

    return render_template('carrinho.html')

@app.route('/remove_do_carrinho', methods=['GET', 'POST'])
def remover_do_carrinho():
    item_id = request.form.get('item_id')

    if item_id in session['carrinho']:
        session['preco_total'] -= float(session['carrinho'][item_id]['preco'])
        del session['carrinho'][item_id]
    
    if not session['carrinho']:
        session.pop('preco_total', None)

    return render_template('carrinho.html')

@app.route('/esvazia_carrinho', methods=['GET', 'POST'])
def esvaziar_carrinho():
    if request.method == 'POST':
        session.pop('carrinho', None)
        session.pop('preco_total', None)
    return redirect(url_for('index'))

@app.route('/comprar_carrinho', methods=['GET', 'POST'])
def comprar_carrinho():
    str_compra = {}
    carrinho = request.form.get('carrinho')
    carrinho_dict = processa_carrinho(carrinho)

    print('Carrinho Dict:', carrinho_dict)
    for item in carrinho_dict:
        str_compra.update(
            {item:{
            'id':carrinho_dict[item]['id'],
            'nome':carrinho_dict[item]['nome'],
            'preco':carrinho_dict[item]['preco'],
            'categoria':carrinho_dict[item]['categoria']
            }})
        
    result_str = ''
    
    secrets_keys = ['id']
    for id in str_compra.keys():
        for key, value in str_compra[id].items():
            if key not in secrets_keys:
                result_str += f'{key} = {value} %0a'
        result_str += '-'*10 + '%0a'

    result_str += f'%0aTOTAL: R${session.get("preco_total")}'
    return render_template('checkout.html', mensagem_str=result_str, mensagem_dict=str_compra)


@app.route("/error/<error>", methods=['GET'])
def mostrar_erro(error):
    return render_template('error.html', error=error)