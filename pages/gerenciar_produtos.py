import streamlit as st
import os
from utils.database import add_produto, get_all_produtos, update_produto, delete_produto, get_produto_by_id

# Definições de listas para os filtros
MARCAS = ["Eudora", "O Boticário", "Jequiti", "Avon", "Mary Kay"]
ESTILOS = ["Perfumaria", "Skincare", "Cabelo", "Corpo e Banho", "Make", "Masculinos", "Femininos", "Nina Secrets", "Marcas", "Infantil", "Casa", "Solar", "Maquiage", "Teen", "Kits e Presentes", "Cuidados com o Corpo", "Lançamentos"]
TIPOS = ["Perfumaria masculina", "Perfumaria feminina", "Body splash", "Body spray", "Eau de perfum", "Desodorantes", "Perfumaria infantil", "Perfumaria vegana", "Familia olfativa", "Clareador de manchas", "Anti-idade", "Protetor solar facial", "Rosto", "Tratamento para o rosto", "Acne", "Limpeza", "Esfoliante", "Tonico facial", "Kits de tratamento", "Tratamento para cabelos", "Shampoo", "Condicionador", "Leave-in e Creme para Pentear", "Finalizador", "Modelador", "Acessorios", "Kits e looks", "Boca", "Olhos", "Pinceis", "Paleta", "Unhas", "Sobrancelhas", "Kits de tratamento", "Hidratante", "Cuidados pós-banho", "Cuidados para o banho", "Barba", "Óleo corporal", "Cuidados intimos", "Unissexy", "Bronzeamento", "Protetor solar", "Depilação", "Mãos", "Labios", "Pés", "Pós sol", "Protetor solar corporal", "Colonias", "Estojo", "Sabonetes", "Creme hidratante para as mãos", "Creme hidratante para os pés", "Miniseries", "Kits de perfumes", "Antisinais", "Máscara", "Creme bisnaga", "Roll On Fragranciado", "Roll On On Duty", "Sabonete liquido", "Sabonete em barra", "Shampoo 2 em 1", "Spray corporal", "Booster de Tratamento", "Creme para Pentear", "Óleo de Tratamento", "Pré-shampoo", "Sérum de Tratamento", "Shampoo e Condicionador"]

# Função principal da página
def gerenciar_produtos_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.error("Você precisa estar logado para acessar esta página.")
        st.info("Por favor, acesse a página 'Área Administrativa' para fazer login.")
        return

    st.title("Gerenciamento de Produtos")
    st.sidebar.markdown(f"**Olá, {st.session_state['username']}!**")
    
    # Menu de Ações
    action = st.sidebar.selectbox("Selecione uma Ação", ["Adicionar Produto", "Visualizar/Modificar/Remover Produtos"])

    if action == "Adicionar Produto":
        add_product_form()
    elif action == "Visualizar/Modificar/Remover Produtos":
        manage_products_list()

# Formulário para adicionar um produto
def add_product_form():
    st.subheader("Adicionar Novo Produto")
    with st.form("add_product_form", clear_on_submit=True):
        nome = st.text_input("Nome do Produto", max_chars=100)
        col1, col2 = st.columns(2)
        with col1:
            preco = st.number_input("Preço (R$)", min_value=0.01, format="%.2f")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=0, step=1)
        
        marca = st.selectbox("Marca", MARCAS)
        estilo = st.selectbox("Estilo", ESTILOS)
        tipo = st.selectbox("Tipo de Produto", TIPOS)
        
        foto = st.file_uploader("Adicionar Foto do Produto", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Adicionar Produto")
        if submitted:
            if nome and preco and quantidade:
                photo_name = None
                if foto:
                    # Salva a imagem na pasta /assets
                    photo_name = foto.name
                    with open(os.path.join("assets", photo_name), "wb") as f:
                        f.write(foto.getbuffer())
                
                add_produto(nome, preco, quantidade, marca, estilo, tipo, photo_name)
                st.success(f"Produto '{nome}' adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios (Nome, Preço, Quantidade).")

# Lista de produtos com opções para modificar e remover
def manage_products_list():
    st.subheader("Lista de Produtos")
    produtos = get_all_produtos()
    
    if not produtos:
        st.info("Nenhum produto cadastrado.")
        return

    # Usando o st.expander para cada produto para um layout mais limpo
    for p in produtos:
        produto_id, nome, preco, quantidade, marca, estilo, tipo, foto = p
        
        with st.expander(f"**{nome}** - (ID: {produto_id})"):
            col_info, col_img, col_actions = st.columns([3, 1, 1])
            
            with col_info:
                st.write(f"**Preço:** R$ {preco:.2f}")
                st.write(f"**Quantidade:** {quantidade}")
                st.write(f"**Marca:** {marca}")
                st.write(f"**Estilo:** {estilo}")
                st.write(f"**Tipo:** {tipo}")

            with col_img:
                if foto and os.path.exists(os.path.join("assets", foto)):
                    st.image(f"assets/{foto}", width=100)
                else:
                    st.info("Sem foto")

            with col_actions:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Modificar", key=f"mod_{produto_id}"):
                    st.session_state["edit_product_id"] = produto_id
                    st.session_state["edit_mode"] = True
                    st.experimental_rerun()
                
                if st.button("Remover", key=f"rem_{produto_id}"):
                    delete_produto(produto_id)
                    st.warning(f"Produto '{nome}' removido.")
                    st.experimental_rerun()

    if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
        show_edit_form()

# Formulário para modificar um produto
def show_edit_form():
    produto_id = st.session_state["edit_product_id"]
    produto_info = get_produto_by_id(produto_id)

    if not produto_info:
        st.error("Produto não encontrado para edição.")
        st.session_state["edit_mode"] = False
        return

    st.subheader(f"Modificar Produto: {produto_info[1]}")
    with st.form("edit_product_form"):
        nome = st.text_input("Nome do Produto", value=produto_info[1])
        col1, col2 = st.columns(2)
        with col1:
            preco = st.number_input("Preço (R$)", value=float(produto_info[2]), format="%.2f")
        with col2:
            quantidade = st.number_input("Quantidade", value=int(produto_info[3]), step=1)
        
        marca = st.selectbox("Marca", MARCAS, index=MARCAS.index(produto_info[4]))
        estilo = st.selectbox("Estilo", ESTILOS, index=ESTILOS.index(produto_info[5]))
        tipo = st.selectbox("Tipo de Produto", TIPOS, index=TIPOS.index(produto_info[6]))
        
        uploaded_file = st.file_uploader("Alterar Foto", type=["jpg", "png", "jpeg"])
        
        submit_update = st.form_submit_button("Salvar Alterações")
        if submit_update:
            photo_name = produto_info[7]
            if uploaded_file:
                photo_name = uploaded_file.name
                with open(os.path.join("assets", photo_name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            update_produto(produto_id, nome, preco, quantidade, marca, estilo, tipo, photo_name)
            st.success("Produto atualizado com sucesso!")
            st.session_state["edit_mode"] = False
            st.experimental_rerun()

gerenciar_produtos_page()