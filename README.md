# Equilibrium-project
Projeto feito para uma loja de suplementos e produtos naturais, feito com o intuíto de aprendizagem e prática.
Utilizou-se o framework Flask para a construção da API.

# Como rodar a aplicação
## Após a clonagem do projeto, precisa criar um ambiente virtual e ativa-lo na pasta raiz:
Primeiramente, entrar no diretório da pasta do projeto:
#### cd nome-da-pasta-raiz

Criando o ambiente virtual:
#### python -m venv .venv

Ativando o ambiente (Windows):
#### .venv/Scripts/activate

Ativando o ambiente (Mac/Linux):
#### . .venv/bin/activate

Agora com o ambiente ativo, basta instalar as depencias com o seguinte comando:
#### pip install -r requirements.txt

Cire o arquivo .env baseado no arquivo .env.exemplo:
#### SECRET_KEY = 'nome_desejado'

E para rodar a aplicação:
#### flask run

Para testar a função de admin, basta colocar /login após o endereço local.
Seu email e senha serão:
#### email@gmail.com
#### senhasecreta

