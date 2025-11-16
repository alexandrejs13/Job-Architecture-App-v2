# pages/4_Job_Maps.py — versão FINAL clean, sticky, merge, premium

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

st.set_page_config(page_title="Job Maps", layout="wide")

# ==========================================================
# HEADER CLEAN (mesmo padrão do app novo)
# ==========================================================
def header():
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image("assets/icons/globe_trade.png", width=48)
    with col2:
        st.markdown(
            "<h1 style='margin:0; padding:0; font-size:36px; font-weight:700;'>Job Maps</h1>",
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header()

# ==========================================================
# CSS MODERNO CLEAN PREMIUM
# ==========================================================
css = """
<style>

:root {
    --border: #d9d9d9;
    --family-bg: #f0f0f0;
    --subfamily-bg: #f8f8f8;
    --gg-bg: #3c3c3c;

    /* cores discretas por carreira */
    --mgmt: #4F5D75;
    --prof: #2F2F2F;
    --tech: #7C7C7C;
    --proj: #5F6C7A;
}

/* WRAPPER DO MAPA */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border: 0.5px solid var(--border);
    border-radius: 10px;
    background: white;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    border-collapse: collapse;
    font-size: 0.88rem;
    background: white;
}

/*************** HEADERS STICKY ***************/
.header-family {
    background: var(--family-bg);
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    font-weight: 700;
    text-align: center;
    display:flex; align-items:center; justify-content:center;
    position: sticky;
    top: 0;
    z-index: 50;
}

.header-subfamily {
    background: var(--subfamily-bg);
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    font-weight: 600;
    text-align: center;
    display:flex; align-items:center; justify-content:center;
    position: sticky;
    top: 45px;
    z-index: 40;
}

/*************** PRIMEIRA COLUNA STICKY ***************/
.gg-header {
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    display:flex; align-items:center; justify-content:center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 100;
}

.gg-cell {
    background: var(--gg-bg);
    color: white;
    font-weight: 700;
    display:flex; align-items:center; justify-content:center;
    position: sticky;
    left: 0;
    z-index: 90;
}

/*************** CÉLULAS ***************/
.cell {
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    padding: 6px;
    display:flex;
    flex-wrap: wrap;
    gap: 8px;
}

/*************** CARDS CLEAN ***************/
.job-card {
    background: white;
    border: 0.5px solid var(--border);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 6px 8px;
    width: 135px;
    height: 75px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    box-shadow:0 1px 3px rgba(0,0,0,0.06);
    transition: 0.20s ease;
}

.job-card:hover {
    transform: translateY(-3px);
    box-shadow:0 4px 12px rgba(0,0,0,0.12);
}

.job-card b {
    font-size:0.78rem;
    margin-bottom:3px;
    color:#333;
}

.job-card span {
    font-size:0.7rem;
    color:#666;
}

/*************** FULLSCREEN — BOTÃO PRETO FOSCO ***************/
#exit-fullscreen-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 999999 !important;
    background: #111 !important;
    color: white !important;
    border-radius: 28px !important;
    padding: 12px 28px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.35) !important;
    cursor: pointer;
}
#exit-fullscreen-btn:hover {
    transform: scale(1.06);
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)
