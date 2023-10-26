import sqlite3
from pathlib import Path
from sqlite3 import Error

ROOT_DIR = Path(__file__).parent
DB_NAME = "produtos.db"
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = "produtos"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute(
    f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}"
    "("
    "id TEXT PRIMARY KEY,"
    "nome TEXT,"
    "preco REAL,"
    "descricao TEXT,"
    "imagem TEXT,"
    "tipo TEXT"
    "categoria TEXT"
    ")"
)
conn.commit()

cursor.close()
conn.close()
