import base64
import imghdr
import json
from uuid import uuid4

from db_services import get_db_connection


def gerar_novo_produto(data, img):
    """
    Função responsável por adicionar um novo produto ao json.
    data => parâmetro que recebe o formulário.

    Return:
    novo_produto, dicionário com todas as informações adicionadas, isso após ser
    inserido ao json.
    """
    for item in data:
        if not data.get(item):
            raise ValueError("Necessário preencher todos os campos.")

    id = str(uuid4())
    name = str(data.get("nome"))
    preco = float(data.get("valor"))
    description = str(data.get("descricao"))
    imagem = img
    category = str(data.get("categoria"))

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO produtos (id, nome, preco, imagem, descricao, categoria)'
        'VALUES (?, ?, ?, ?, ?, ?)',
        (id, name, preco, imagem, description, category)
        )
    conn.commit()
    conn.close()

    return id


def processa_imagem(img):
    """
    Return:
    Caminho da imagem
    """

    imagem_path = f'{img.replace("static", "")}'

    return imagem_path


def update_produto_service(data, produto_a_alterar, img):
    """
    Função que têm o mesmo principio da função 'gerar_novo_produto'.
    Diferenças: O valor vem carregado do json e as alterações feitas no formulário
    serão processadas e aplicadas ao mesmo produto.

    Return:
    produto_a_alterar => Mesmo produto vindo do json (utiulizando o mesmo id), aplicando
    as devidas alterações feitas pelo usuário.
    """

    name = str(data.get("nome"))
    preco = data.get("valor")
    description = str(data.get("descricao"))
    category = str(data.get("categoria"))

    conn = get_db_connection()
    conn.execute(
        'UPDATE produtos SET nome=?, preco=?, descricao=?, imagem=?, categoria=? WHERE id=?',
        (name, preco, description, img, category, produto_a_alterar['id'])
        )
    conn.commit()
    produto = conn.execute('SELECT * FROM produtos WHERE id=?', (produto_a_alterar['id'],)).fetchone()
    conn.close()


    return dict(produto)


def busca_produto(produto_id):
    """
    Função que busca por um produto específico dentro do arquivo json.
    O arquivo é percorrido por um um for, verificando se o id encontrado é o
    mesmo passado como parâmetro para a função.

    Return:
    O dicionário com o id especificado.
    """

    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id=?', (produto_id,)).fetchone()
    produto_info = dict(produto)
    print(produto_info)

    return produto_info


def service_delete_produto(produto_id):
    """
    Função que remove um produto do arquivo json a partir do id.
    Com os produtos recuperados em 'produtos_json', é feita a deleção direta no
    id do produto.
    Em seguida é reescrito todo o arquivo, sem o produto deletado.
    """
    # conn = get_db_connection()
    # produtos = conn.execute('SELECT * FROM produtos').fetchall()
    # produtos_dict = dict(produtos)
    # del produtos_dict[produto_id]

    # with open("data/produtos.json", "w", encoding="utf-8") as arquivo_produtos:
    #     deletou_produto = json.dumps(produtos_json, indent=4, ensure_ascii=False)
    #     arquivo_produtos.write(deletou_produto)


def filtrar_produto():
    """
    Função que faz a filtragem a partir da categoria do produto.

    Return:
    Uma tupla de dicionários para cada categoria.
    """
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    suplementos_dict = {}
    prdt_naturais_dict = {}
    # produtos_json = ler_o_json()

    for produto in produtos:
        produto_info = dict(produto)
        if produto_info["categoria"] == "suplemento":
            suplementos_dict[produto['id']] = produto_info
        else:
            prdt_naturais_dict[produto['id']] = produto_info

    return suplementos_dict, prdt_naturais_dict
