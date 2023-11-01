
DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id TEXT NOT NULL, 
    nome TEXT NOT NULL,
    preco FLOAT NOT NULL,
    imagem TEXT,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL
);

DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id TEXT NOT NULL,
    email TEXT NOT NULL,
    senha_hash TEXT NOT NULL,
    senha_salt TEXT NOT NULL
)