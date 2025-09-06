import streamlit as st
import hashlib
from utils.database import add_user, get_user

# Função para hash da senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    st.title("Área Administrativa")
    
    st.markdown("Use o menu abaixo para fazer login ou criar uma conta de administrador.")
    choice = st.selectbox("Selecione uma opção", ["Login", "Cadastrar Novo Admin"])

    if choice == "Login":
        st.subheader("Login de Administrador")
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            user = get_user(username)
            if user:
                hashed_password = hash_password(password)
                if hashed_password == user[2]:
                    st.success(f"Bem-vindo, {username}!")
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Nome de usuário ou senha incorretos.")
            else:
                st.error("Nome de usuário não encontrado.")

    elif choice == "Cadastrar Novo Admin":
        st.subheader("Cadastro de Novo Administrador")
        new_username = st.text_input("Escolha um nome de usuário")
        new_password = st.text_input("Crie uma senha", type="password")
        confirm_password = st.text_input("Confirme a senha", type="password")

        if st.button("Cadastrar"):
            if new_password != confirm_password:
                st.error("As senhas não coincidem.")
            else:
                if get_user(new_username):
                    st.error("Nome de usuário já existe. Escolha outro.")
                else:
                    hashed_password = hash_password(new_password)
                    add_user(new_username, hashed_password)
                    st.success("Administrador cadastrado com sucesso! Agora você pode fazer login.")


login_page()
