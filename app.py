# Home - Job Architecture App

import streamlit as st
from pathlib import Path

# ==========================================================
# CONFIG GERAL
# ==========================================================
st.set_page_config(
    page_title="Job Architecture App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CSS GLOBAL (se existir)
# ==========================================================
css_path = Path("assets/css/main.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# ==========================================================
# LAYOUT PRINCIPAL - SEM HEADER COM ÍCONE/TÍTULO
# A página começa diretamente pela imagem HERO
# ==========================================================

# Container de largura máxima, alinhado com as demais páginas
with st.container():
    # ======================================================
    # HERO IMAGE – mesma largura das demais páginas
    # ======================================================
    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:flex-start;
            align-items:flex-start;
            margin-top:16px;
            margin-bottom:28px;
        ">
            <img 
                src="assets/home/home_card.jpg" 
                alt="Job Architecture Hero" 
                style="
                    width:100%;
                    max-width:1180px;
                    border-radius:26px;
                    object-fit:cover;
                    display:block;
                "
            >
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # BLOCO DE TEXTO PRINCIPAL – IDENTIDADE VISUAL SIG
    # Usando as fontes já carregadas pelo main.css:
    #   - 'PP-Sigflow-SemiBold'
    #   - 'PP-Sigflow-Regular'
    # ======================================================
    st.markdown(
        """
        <h1 style="
            font-family: 'PP-Sigflow-SemiBold';
            font-size: 40px;
            margin-bottom: 10px;
            color: #000;
        ">
            Job Architecture
        </h1>

        <p style="
            font-family: 'PP-Sigflow-Regular';
            font-size: 18px;
            line-height: 1.6;
            max-width: 900px;
            color: #000;
        ">
            Bem-vindo ao portal de Job Architecture. Aqui você encontra as estruturas organizadas 
            de famílias de cargos, perfis de posição, níveis, responsabilidades e competências 
            essenciais para garantir consistência, governança e alinhamento global.
            <br><br>
            Explore as seções ao lado para navegar por famílias, perfis, comparações, dashboards 
            e muito mais — tudo com a identidade visual SIG e uma experiência totalmente integrada.
        </p>
        """,
        unsafe_allow_html=True,
    )
