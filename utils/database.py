import sqlite3

# Conexão e criação das tabelas
def create_connection():
    conn = sqlite3.connect('data/produtos.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Tabela para usuários administrativos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Tabela para os produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            marca TEXT,
            estilo TEXT,
            tipo TEXT,
            foto TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Adiciona um novo usuário (admin)
def add_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Busca um usuário
def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Funções de CRUD para produtos
# Adiciona um produto
def add_produto(nome, preco, quantidade, marca, estilo, tipo, foto):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, quantidade, marca, estilo, tipo, foto) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (nome, preco, quantidade, marca, estilo, tipo, foto))
    conn.commit()
    conn.close()

# Busca todos os produtos
def get_all_produtos():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos
def add_produto(nome, preco, quantidade, marca, estilo, tipo, foto):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, quantidade, marca, estilo, tipo, foto) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (nome, preco, quantidade, marca, estilo, tipo, foto))
    conn.commit()
    conn.close()

def get_all_produtos():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def get_produto_by_id(produto_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def update_produto(produto_id, nome, preco, quantidade, marca, estilo, tipo, foto):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos
        SET nome=?, preco=?, quantidade=?, marca=?, estilo=?, tipo=?, foto=?
        WHERE id=?
    """, (nome, preco, quantidade, marca, estilo, tipo, foto, produto_id))
    conn.commit()
    conn.close()

def delete_produto(produto_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
    conn.commit()
    conn.close()

# Funções para usuários
def add_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user