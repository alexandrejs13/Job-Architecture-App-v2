# ==========================================================
# HEADER — padrão SIG (56px, alinhado, elegante)
# ==========================================================
import streamlit as st
import base64
import os

def load_icon_png(path):
    if not os.path.exists(path):
        return ""   # evita erros caso o arquivo não exista
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/checkmark_success.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="
    display:flex;
    align-items:center;
    gap:18px;
    margin-top:12px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:56px; height:56px;">
    <h1 style="
        font-size:36px;
        font-weight:700;
        margin:0;
        padding:0;
    ">
        Job Match
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# GLOBAL LAYOUT — limita largura e impede esticar infinito
# ==========================================================
st.markdown("""
<style>

    /* Container principal do Streamlit */
    .main > div {
        max-width: 1400px;    /* limite máximo elegante */
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* Estilo para dataframes */
    .stDataFrame {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Estilo para cards / container padrão */
    .block-container, .stColumn {
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

</style>
""", unsafe_allow_html=True)
