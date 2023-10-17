import json
from uuid import uuid4


def gerar_novo_produto(data):
    name = str(data.get("nome"))
    preco = data.get("valor")
    description = str(data.get("descricao"))
    category = str(data.get("categoria"))
    novo_produto = {
        "id": str(uuid4()),
        "nome": name,
        "preco": preco,
        "descricao": description,
        "categoria": category,
    }

    produtos_json = ler_o_json()
    escrever_no_json(produtos_json, novo_produto)

    return novo_produto


def update_produto_service(data, produto_a_alterar):
    name = str(data.get("nome"))
    preco = data.get("valor")
    description = str(data.get("descricao"))
    category = str(data.get("categoria"))
    produto_a_alterar = {
        "id": produto_a_alterar["id"],
        "nome": name,
        "preco": preco,
        "descricao": description,
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
