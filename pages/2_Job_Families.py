import streamlit as st

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Families", layout="wide")

# ---------------------------------------------------------
# HEADER PADRÃO (igual ao Job Profile Description)
# ---------------------------------------------------------
def header(icon_path: str, title: str) -> None:
    # mesma proporção de colunas e tamanho de ícone da página Job Profile Description
    col1, col2 = st.columns([0.08, 0.92])

    with col1:
        # aumenta o ícone para dar destaque (mesmo padrão do Job Profile Description)
        st.image(icon_path, width=64)

    with col2:
        st.markdown(
            f"""
            <h1 style="
                margin: 0;
                padding: 0;
                font-size: 36px;
                font-weight: 700;
            ">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )

    # mesma linha sutil abaixo do título + respiro
    st.markdown(
        "<hr style='margin-top:10px; margin-bottom:32px;'>",
        unsafe_allow_html=True,
    )

# 🔧 ATENÇÃO AQUI:
# Se o arquivo for SVG, troque para "people_employees.svg"
header("assets/icons/people_employees.png", "Job Families")

# ---------------------------------------------------------
# A PARTIR DAQUI VEM O CONTEÚDO DA PÁGINA (tabelas, filtros etc.)
# ---------------------------------------------------------

st.write("Conteúdo da página Job Families aqui…")
