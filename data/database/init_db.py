import hashlib
import os
import sqlite3
from uuid import uuid4

from dotenv import load_dotenv

script_directory = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_directory, '..\..', '.env')

load_dotenv(dotenv_path)

email_admin = os.environ.get('EMAIL_ADMIN')
password_admin = os.environ.get('PASSWORD_ADMIN')


salt = os.urandom(32)
hashed_password = hashlib.pbkdf2_hmac('sha256', password_admin.encode('utf-8'), salt, 100000)
hashed_password__hexadecimal = hashed_password.hex()

os.chdir(script_directory)

conn = sqlite3.connect("produtos.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO produtos (id, nome, preco, imagem, descricao, categoria) VALUES (?, ?, ?, ?, ?, ?)",
    ('id_1', 'exemplo_1', 199.99, 'imagem', 'descrição exemplo_1', 'suplemento')
)

id = str(uuid4())

cursor.execute(
    "INSERT INTO usuario (id, email, senha_hash, senha_salt) VALUES (?, ?, ?, ?)",
    (id, email_admin, hashed_password__hexadecimal, salt)
)

conn.commit()
conn.close()
