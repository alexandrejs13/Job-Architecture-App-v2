import streamlit as st
import base64
from pathlib import Path

# ==========================================================
# CONFIG GERAL
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
)

BASE_DIR = Path(__file__).parent

# ==========================================================
# FIX DEFINITIVO: Ocultar item "app" do menu e resolver conflito
# ==========================================================
# Injeta CSS de alta prioridade no Streamlit para ocultar o link da página principal ("/")
# e garantir que não haja conflito com o botão de recolher.
st.markdown("""
<style>
/* 1. Oculta o link de navegação da página inicial (item "app"). Este seletor é o mais comum para o item. */
[data-testid="stSidebarNav"] a[href="/"] {
    display: none !important;
}
/* 2. Oculta o rótulo da aplicação ("streamlitApp" ou texto fantasma) que aparece na barra lateral/cabeçalho. */
[data-testid="stSidebarContent"] > div:first-child > div:first-child > div:nth-child(2) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# CSS GLOBAL SIG
# ==========================================================
# Mantém a injeção do CSS global para as outras páginas
css_path = BASE_DIR / "assets" / "css" / "layout_global.css"

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO DA PÁGINA
# ==========================================================
# A página principal está vazia, conforme solicitado.
# A aplicação agora começará na próxima página do menu (ex: 1_Job_Architecture.py),
# e o item "app" estará oculto.
