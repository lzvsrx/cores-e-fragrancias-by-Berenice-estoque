import streamlit as st
from utils.database import get_all_produtos

def estoque_page():
    st.title("Estoque Completo de Produtos")

    # Obtém todos os produtos do banco de dados
    produtos = get_all_produtos()
    
    if not produtos:
        st.info("Nenhum produto cadastrado no estoque.")
        return

    # Extrai listas únicas para os filtros
    marcas = sorted(list(set(p[4] for p in produtos if p[4])))
    estilos = sorted(list(set(p[5] for p in produtos if p[5])))
    tipos = sorted(list(set(p[6] for p in produtos if p[6])))

    # Cria as colunas para os filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        marca_filtro = st.selectbox("Filtrar por Marca", ["Todas"] + marcas)
    with col2:
        estilo_filtro = st.selectbox("Filtrar por Estilo", ["Todos"] + estilos)
    with col3:
        tipo_filtro = st.selectbox("Filtrar por Tipo de Produto", ["Todos"] + tipos)
    
    st.markdown("---")

    # Aplica os filtros
    produtos_filtrados = produtos
    if marca_filtro != "Todas":
        produtos_filtrados = [p for p in produtos_filtrados if p[4] == marca_filtro]
    if estilo_filtro != "Todos":
        produtos_filtrados = [p for p in produtos_filtrados if p[5] == estilo_filtro]
    if tipo_filtro != "Todos":
        produtos_filtrados = [p for p in produtos_filtrados if p[6] == tipo_filtro]
    
    if produtos_filtrados:
        st.subheader(f"Total de {len(produtos_filtrados)} produtos encontrados")
        
        # Exibe os produtos em um formato de grade ou tabela
        # Para uma exibição mais rica, você pode usar st.columns() e exibir cards com fotos
        for produto in produtos_filtrados:
            st.markdown(f"""
            ### **{produto[1]}**
            - **Preço:** R$ {produto[2]:.2f}
            - **Quantidade em Estoque:** {produto[3]}
            - **Marca:** {produto[4]}
            - **Estilo:** {produto[5]}
            - **Tipo:** {produto[6]}
            """)
            if produto[7]: # Verifica se há uma foto
                st.image(f"assets/{produto[7]}", width=200)
            st.markdown("---")
    else:
        st.warning("Nenhum produto corresponde aos filtros selecionados.")

estoque_page()