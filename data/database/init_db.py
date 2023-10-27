import os
import sqlite3

script_directory = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_directory)

conn = sqlite3.connect("produtos.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO produtos (id, nome, preco, imagem, descricao, categoria) VALUES (?, ?, ?, ?, ?, ?)",
    ('id_1', 'exemplo_1', 199.99, 'imagem', 'descrição exemplo_1', 'suplemento')
)

conn.commit()
conn.close()
