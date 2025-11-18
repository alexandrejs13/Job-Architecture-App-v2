# Home - Job Architecture App

import streamlit as st
import base64
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG/JPG INLINE (BASE64)
# ==========================================================
def load_image_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ==========================================================
# CSS GLOBAL SIG
# ==========================================================
css_path = "assets/css/sig_style.css"
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ==========================================================
# FONTES PP SIG FLOW
# ==========================================================
try:
    from utils.fonts import load_pp_fonts
    load_pp_fonts()
except:
    pass


# ==========================================================
# IMAGEM DE CAPA — PRIMEIRO ELEMENTO DA PÁGINA
# ==========================================================
home_img_path = "assets/home/home_card.jpg"
home_img_b64 = load_image_b64(home_img_path)

st.markdown(
    f"""
    <div class="sig-container" style="margin-top: 12px; margin-bottom: 32px;">
        <img 
            src="data:image/jpeg;base64,{home_img_b64}" 
            style="
                width: 100%; 
                max-width: 1400px; 
                display: block; 
                margin: 0 auto; 
                border-radius: 12px;
            "
        >
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# TÍTULO + TEXTO DESCRITIVO (FONTES SIG)
# ==========================================================
st.markdown(
    """
    <div class="sig-container" style="margin-top: 0px;">

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

    </div>
    """,
    unsafe_allow_html=True
)
