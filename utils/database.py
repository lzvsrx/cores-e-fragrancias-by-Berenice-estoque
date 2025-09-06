import sqlite3

# Define o nome do arquivo do banco de dados
DATABASE = "estoque.db"

# Função para conectar ao banco de dados
def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados SQLite.
    A propriedade row_factory é configurada para permitir o acesso aos dados por nome da coluna.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar as tabelas 'produtos' e 'users'
def create_tables():
    """
    Cria as tabelas 'produtos' e 'users' se elas ainda não existirem.
    A tabela 'produtos' inclui a coluna 'data_validade' e 'id' com AUTOINCREMENT.
    A tabela 'users' também tem 'id' com AUTOINCREMENT.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela para os produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            marca TEXT,
            estilo TEXT,
            tipo TEXT,
            foto TEXT,
            data_validade TEXT
        );
    """)

    # Tabela para usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Funções de CRUD para produtos
def add_produto(nome, preco, quantidade, marca, estilo, tipo, foto, data_validade):
    """
    Adiciona um novo produto ao banco de dados.
    
    Args:
        nome (str): Nome do produto.
        preco (float): Preço do produto.
        quantidade (int): Quantidade em estoque.
        marca (str): Marca do produto.
        estilo (str): Estilo do produto.
        tipo (str): Tipo de produto.
        foto (str): Caminho para a foto do produto.
        data_validade (str): Data de validade (formato TEXT).
    """
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO produtos (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade)
    )
    conn.commit()
    conn.close()

def get_all_produtos():
    """
    Retorna todos os produtos do banco de dados.
    
    Returns:
        list: Uma lista de objetos de produto (sqlite3.Row).
    """
    conn = get_db_connection()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return produtos

def get_produto_by_id(produto_id):
    """
    Busca e retorna um produto pelo seu ID.
    
    Args:
        produto_id (int): O ID do produto a ser buscado.
        
    Returns:
        sqlite3.Row or None: O objeto do produto ou None se não for encontrado.
    """
    conn = get_db_connection()
    produto = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()
    conn.close()
    return produto

def update_produto(produto_id, nome, preco, quantidade, marca, estilo, tipo, foto, data_validade):
    """
    Atualiza as informações de um produto existente.
    
    Args:
        produto_id (int): O ID do produto a ser atualizado.
        nome (str): Novo nome do produto.
        preco (float): Novo preço do produto.
        quantidade (int): Nova quantidade em estoque.
        marca (str): Nova marca do produto.
        estilo (str): Novo estilo do produto.
        tipo (str): Novo tipo de produto.
        foto (str): Novo caminho para a foto.
        data_validade (str): Nova data de validade.
    """
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE produtos SET
            nome = ?, preco = ?, quantidade = ?, marca = ?, estilo = ?, tipo = ?, foto = ?, data_validade = ?
        WHERE id = ?
        """,
        (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade, produto_id)
    )
    conn.commit()
    conn.close()

def delete_produto(produto_id):
    """
    Deleta um produto do banco de dados pelo seu ID.
    
    Args:
        produto_id (int): O ID do produto a ser deletado.
    """
    conn = get_db_connection()
    conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

# Funções para usuários
def add_user(username, password):
    """
    Adiciona um novo usuário ao banco de dados.
    
    Args:
        username (str): O nome de usuário.
        password (str): A senha.
    """
    conn = get_db_connection()
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    """
    Busca e retorna um usuário pelo nome de usuário.
    
    Args:
        username (str): O nome de usuário a ser buscado.
        
    Returns:
        sqlite3.Row or None: O objeto do usuário ou None se não for encontrado.
    """
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

# Bloco de execução principal para demonstração
if __name__ == "__main__":
    print("Criando as tabelas...")
    create_tables()

    print("\nAdicionando um usuário de demonstração...")
    add_user("admin", "senha123")
    user = get_user("admin")
    if user:
        print(f"Usuário encontrado: {user['username']}")

    print("\nAdicionando um produto de demonstração...")
    add_produto(
        nome="Camiseta", 
        preco=29.90, 
        quantidade=50, 
        marca="CoolWear", 
        estilo="Casual", 
        tipo="Vestuário", 
        foto="caminho/para/foto.jpg", 
        data_validade="2025-12-31"
    )
    print("Produto adicionado com sucesso.")

    print("\nBuscando todos os produtos...")
    produtos = get_all_produtos()
    for produto in produtos:
        print(dict(produto)) # Convertendo para dicionário para uma visualização melhor

    print("\nAtualizando o produto com ID 1...")
    update_produto(
        produto_id=1,
        nome="Camiseta Premium",
        preco=39.90,
        quantidade=45,
        marca="CoolWear",
        estilo="Casual",
        tipo="Vestuário",
        foto="caminho/para/nova_foto.jpg",
        data_validade="2026-12-31"
    )
    produto_atualizado = get_produto_by_id(1)
    if produto_atualizado:
        print("Produto atualizado:")
        print(dict(produto_atualizado))

    print("\nDeletando o produto com ID 1...")
    delete_produto(1)
    produto_deletado = get_produto_by_id(1)
    if not produto_deletado:
        print("Produto deletado com sucesso.")
