import streamlit as st
from utils.database import create_tables

# Inicializa o banco de dados e as tabelas
create_tables()

st.set_page_config(
    page_title="Cores e Fragrâncias by Berenice",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Olá, bem-vinda ao Cores e Fragrâncias by Berenice!")

st.markdown("""
    Este é o seu aplicativo completo para **gerenciamento de estoque** da loja.
    Utilize o menu lateral para navegar entre as diferentes seções.
    
    * **Estoque Completo:** Visualize e filtre todos os produtos disponíveis.
    * **Área Administrativa:** Faça login para gerenciar produtos, incluindo a adição, edição e remoção.
""")

st.image("assets/logo.png", width=250)

# Botão de Logout para a área administrativa
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    if st.sidebar.button("Sair"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

        st.rerun()
