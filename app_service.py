import hashlib
from json import loads
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

    return produto_info


def service_delete_produto(produto_id):
    """
    Função que deleta o arquivo, a partir da pesquisa por id, da tabela produtos.
    """
    conn = get_db_connection()
    produto_a_deletar = conn.execute('DELETE FROM produtos WHERE id=?', (produto_id,))
    conn.commit()
    conn.close()
    
    return produto_a_deletar


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

    for produto in produtos:
        produto_info = dict(produto)
        if produto_info["categoria"] == "suplemento":
            suplementos_dict[produto['id']] = produto_info
        else:
            prdt_naturais_dict[produto['id']] = produto_info

    return suplementos_dict, prdt_naturais_dict


def verificar_login(data):
    """
    Faz a verificação do hash da senha do banco de dados com a inserida pelo 
    usuário, utilizando o email inserido para buscar na tabela.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT senha_salt FROM usuario WHERE email=?", (data['email'],))
    salt_db = cursor.fetchone()
       
    if not salt_db:
        raise ValueError('Usuário ou senha incorretos.')

    salt_db = bytes(salt_db[0])
    hashed_input_password = hashlib.pbkdf2_hmac('sha256', data['senha'].encode('utf-8'), salt_db, 100000)
    hashed_password_hexadecimal = hashed_input_password.hex()

    cursor.execute("SELECT * FROM usuario WHERE email=? AND senha_hash=?", (data['email'], hashed_password_hexadecimal))
    user_data = cursor.fetchone()
    if user_data:
        return user_data['id']
    raise ValueError('E-mail ou senha incorretos.')


def processa_hidden_input(data):
    """
    Corrige as aspas enviadas via formulário para que seja um objeto json 
    correto e envia novamente para a construção do objeto session.
    """
    str_json = data['produto'].replace("'", "\"")
    dict_json = loads(str_json)
    return dict_json

def processa_carrinho(data):
    try:
        dict_json = loads(data)
        return dict_json
    except:
        print(f"Erro ao decodificar JSON")
        return None
    

# def retornar_erro():
#     dict_erros = {
#         ValueError: 'Os dados inseridos estão incorretos',
#         TypeError: 'Tipo de dado incorreto'}
#     return dict_erros