import streamlit as st
from pathlib import Path

def load_global_css():
    css = """
    <style>

    /* LIMITA LARGURA MÁXIMA DO CONTEÚDO */
    .block-container {
        max-width: 1600px !important;
        padding-top: 1rem !important;
    }

    /* FUNDO GERAL BRANCO */
    [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
    }

    /* MENU LATERAL FIXO – NÃO REDIMENSIONÁVEL */
    [data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* EVITA EXPANDIR */
    [data-testid="stSidebar"] > div {
        width: 300px !important;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
