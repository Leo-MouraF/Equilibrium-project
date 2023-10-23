import base64
import imghdr
import json
from uuid import uuid4


def gerar_novo_produto(data, img, img_type):
    """
    Função responsável por adicionar um novo produto ao json.
    data => parâmetro que recebe o formulário.

    img, img_type => recebem respectivamente: a imagem e o tipo da imagem, convertidas
    em base 64 na função processa_imagem.

    Return:
    novo_produto, dicionário com todas as informações adicionadas, isso após ser
    inserido ao json.
    """

    name = str(data.get("nome"))
    preco = data.get("valor")
    description = str(data.get("descricao"))
    category = str(data.get("categoria"))
    novo_produto = {
        "id": str(uuid4()),
        "nome": name,
        "preco": preco,
        "descricao": description,
        "imagem": {"imagem_data": img, "tipo": img_type},
        "categoria": category,
    }

    produtos_json = ler_o_json()
    escrever_no_json(produtos_json, novo_produto)

    return novo_produto


def processa_imagem(img):
    """
    Função que faz o processamento da imagem.
    img => Parâmetro que é a imagem vinda diretamente do formulário.

    img_byte => converte a imagem para bytes.

    image_data => retorna uma nova sequência de bytes em base 64. Em seguida, é
    feita a conversão para uma strin Unicode, para que possa ser inserido ao json.
    Biblioteca base64 => para conversão em bytes de base 64.
    decode => para conversão em string Unicode.

    image_type => Captura o tipo da imagem (png ou jpeg nesse caso).
    Biblioteca imghdr => para a captura do tipo.


    Return:
    a imagem processada e também o tipo dela.
    """

    img_byte = img.read()
    image_data = base64.b64encode(img_byte).decode("utf-8")
    image_type = imghdr.what(None, h=img_byte)

    return image_data, image_type


def update_produto_service(data, produto_a_alterar, img, img_type):
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
    produto_a_alterar = {
        "id": produto_a_alterar["id"],
        "nome": name,
        "preco": preco,
        "descricao": description,
        "imagem": {"imagem_data": img, "tipo": img_type},
        "categoria": category,
    }

    produtos_json = ler_o_json()
    escrever_no_json(produtos_json, produto_a_alterar)

    return produto_a_alterar


def escrever_no_json(produtos, novo_produto):
    """
    Função que permite a inserção de dados no arquivo json.
    Recebe o produto a ser inserido e filtra pelo id. Caso não haja aquele id
    no arquivo ainda, é feito um novo objeto.
    """

    with open("data/produtos.json", "w", encoding="utf-8") as arquivo_produtos:
        produtos[novo_produto["id"]] = novo_produto
        novo_produto_json = json.dumps(produtos, indent=4, ensure_ascii=False)
        arquivo_produtos.write(novo_produto_json)


def ler_o_json():
    """
    Função responsável pela leitura do arquivo json e retornar os produtos já
    existentes.

    Return:
    Um dicionário com todos os produtos existentes.
    """

    with open("data/produtos.json", "r", encoding="utf-8") as arquivo_produtos:
        produtos_dicionario = json.load(arquivo_produtos)
        return produtos_dicionario


def busca_produto(produto_id):
    """
    Função que busca por um produto específico dentro do arquivo json.
    O arquivo é percorrido por um um for, verificando se o id encontrado é o
    mesmo passado como parâmetro para a função.

    Return:
    O dicionário com o id especificado.
    """

    dados = ler_o_json()
    produto = dados.get(produto_id)

    for item in dados:
        if dados[item]["id"] == produto["id"]:
            produto_a_mostrar = dados[item]
    return produto_a_mostrar


def service_delete_produto(produto_id):
    """
    Função que remove um produto do arquivo json a partir do id.
    Com os produtos recuperados em 'produtos_json', é feita a deleção direta no
    id do produto.
    Em seguida é reescrito todo o arquivo, sem o produto deletado.
    """

    produtos_json = ler_o_json()
    del produtos_json[produto_id]

    with open("data/produtos.json", "w", encoding="utf-8") as arquivo_produtos:
        deletou_produto = json.dumps(produtos_json, indent=4, ensure_ascii=False)
        arquivo_produtos.write(deletou_produto)


def filtrar_produto():
    """
    Função que faz a filtragem a partir da categoria do produto.

    Return:
    Uma tupla de dicionários para cada categoria.
    """

    suplementos_dict = {}
    prdt_naturais_dict = {}
    produtos_json = ler_o_json()

    for produto_id, produto_info in produtos_json.items():
        if produto_info["categoria"] == "suplemento":
            suplementos_dict[produto_id] = produto_info
        else:
            prdt_naturais_dict[produto_id] = produto_info

    return suplementos_dict, prdt_naturais_dict
