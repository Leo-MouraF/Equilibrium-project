import base64
import imghdr
import json
from uuid import uuid4


def gerar_novo_produto(data, img, img_type):
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
    img_byte = img.read()
    image_data = base64.b64encode(img_byte).decode("utf-8")
    image_type = imghdr.what(None, h=img_byte)

    return image_data, image_type


def update_produto_service(data, produto_a_alterar, img, img_type):
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
    with open("data/produtos.json", "w", encoding="utf-8") as arquivo_produtos:
        produtos[novo_produto["id"]] = novo_produto
        novo_produto_json = json.dumps(produtos, indent=4, ensure_ascii=False)
        arquivo_produtos.write(novo_produto_json)


def ler_o_json():
    with open("data/produtos.json", "r", encoding="utf-8") as arquivo_produtos:
        produtos_dicionario = json.load(arquivo_produtos)
        return produtos_dicionario


def busca_produto(produto_id):
    dados = ler_o_json()
    produto = dados.get(produto_id)

    for item in dados:
        if dados[item]["id"] == produto["id"]:
            produto_a_mostrar = dados[item]
    return produto_a_mostrar


def service_delete_produto(produto_id):
    produtos_json = ler_o_json()
    del produtos_json[produto_id]

    with open("data/produtos.json", "w", encoding="utf-8") as arquivo_produtos:
        deletou_produto = json.dumps(produtos_json, indent=4, ensure_ascii=False)
        arquivo_produtos.write(deletou_produto)


def filtrar_produto():
    suplementos_dict = {}
    prdt_naturais_dict = {}
    produtos_json = ler_o_json()

    for produto_id, produto_info in produtos_json.items():
        if produto_info["categoria"] == "suplemento":
            suplementos_dict[produto_id] = produto_info
        else:
            prdt_naturais_dict[produto_id] = produto_info

    return suplementos_dict, prdt_naturais_dict
