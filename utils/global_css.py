import streamlit as st
from pathlib import Path

def load_global_css():
    css = """
    <style>

    /*****************************************************************
     *  LAYOUT GLOBAL DO APP – FUNDO, SIDEBAR, CONTAINER
     *****************************************************************/

    /* Fundo geral branco do app */
    [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        color: #222 !important;
    }

    /* Limita a largura do conteúdo principal (evita stretching infinito) */
    .block-container {
        max-width: 1600px !important;
        padding-top: 1rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Sidebar fixa e não redimensionável */
    [data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* Impede expandir/colapsar internamente */
    [data-testid="stSidebar"] > div {
        width: 300px !important;
    }

    /*****************************************************************
     *  BOTÕES STREAMLIT – ESTILO PADRÃO SIG BLUE
     *****************************************************************/

    .stButton > button {
        background: #145efc !important;
        color: white !important;
        border-radius: 28px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background: #0d4ccc !important;
        transform: translateY(-1px);
    }

    /*****************************************************************
     *  GRID DE CARDS JOB PROFILE – BASE GLOBAL
     *****************************************************************/

    .jp-grid {
        display: grid;
        gap: 20px;
        width: 100%;
    }

    /* Cards individuais */
    .jp-card {
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        display: flex;
        flex-direction: column;
        height: 650px;               /* Altura fixa padrão */
        overflow-y: auto;            /* Scroll interno */
    }

    /* Scroll comportado */
    .jp-card::-webkit-scrollbar {
        width: 8px;
    }
    .jp-card::-webkit-scrollbar-thumb {
        background: #c8c8c8;
        border-radius: 10px;
    }

    /* Título do card (fixo no topo) */
    .jp-card-header {
        position: sticky;
        top: 0;
        background: white;
        padding-bottom: 12px;
        padding-top: 6px;
        z-index: 5;
        border-bottom: 1px solid #eee;
    }

    .jp-title {
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 4px;
        color: #222;
    }

    .jp-gg {
        color: #145efc;
        font-weight: 700;
        margin-bottom: 12px;
    }

    /* Metadados iniciais */
    .jp-meta-block {
        margin-bottom: 18px;
        font-size: 0.95rem;
    }

    .jp-meta-row {
        padding: 3px 0;
    }

    /*****************************************************************
     *  SEÇÕES DO JOB PROFILE
     *****************************************************************/

    .jp-section {
        border-left: 5px solid #145efc;
        padding-left: 12px;
        margin-bottom: 22px;
    }

    /* Título de cada seção */
    .jp-section-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 4px;
        color: #145efc;
    }

    /* Texto */
    .jp-text {
        white-space: pre-wrap;
        line-height: 1.45;
        color: #444;
        font-size: 0.93rem;
    }

    /* Alternância de cores das seções */
    .jp-section:nth-child(even) {
        background: #fafafa;
        border-radius: 8px;
        padding: 12px;
        border-left: 5px solid #1d6bff !important;
    }

    /*****************************************************************
     *  PDF ICON
     *****************************************************************/

    .pdf-icon {
        position: absolute;
        top: 16px;
        right: 18px;
        width: 26px;
        height: 26px;
        cursor: pointer;
        opacity: 0.75;
        transition: 0.2s ease;
    }

    .pdf-icon:hover {
        opacity: 1;
        transform: scale(1.1);
    }

    /*****************************************************************
     *  FULLSCREEN MODE (Mesmo comportamento do Job Maps)
     *****************************************************************/
    .fullscreen-wrapper {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }

    </style>
    """

    st.markdown(css, unsaf
