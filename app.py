import streamlit as st
import base64
import os
from pathlib import Path

# ==========================================================
# CONFIG GERAL – igual às demais páginas
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CARREGA CSS GLOBAL (layout_global.css)
# ==========================================================
def load_global_css():
    css_path = Path("assets/css/layout_global.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_global_css()

# ==========================================================
# FUNÇÃO PARA CARREGAR IMAGEM EM BASE64
# ==========================================================
def load_image_b64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HERO IMAGE – mesma largura das demais páginas
# ==========================================================
hero_path = "assets/home/home_card.jpg"
hero_b64 = load_image_b64(hero_path)

st.markdown(
    f"""
<div style="
    max-width: 1100px;
    margin: 24px auto 40px auto;
">
    <img 
        src="data:image/jpg;base64,{hero_b64}" 
        alt="Job Architecture"
        style="
            width: 100%;
            height: auto;
            border-radius: 28px;
            display: block;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
        "
    >
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# TÍTULO + TEXTO – alinhados com a imagem, fonte SIG
# ==========================================================
st.markdown(
    """
<div style="
    max-width: 1100px;
    margin: 0 auto 80px auto;
">
    <h1 style="
        font-family: 'PPSIGFlow';
        font-size: 40px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #000;
    ">
        Job Architecture
    </h1>

    <p style="
        font-family: 'PPSIGFlow';
        font-size: 18px;
        font-weight: 400;
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
    unsafe_allow_html=True,
)
