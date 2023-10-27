
DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id TEXT NOT NULL, 
    nome TEXT NOT NULL,
    preco FLOAT NOT NULL,
    imagem TEXT,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL
);