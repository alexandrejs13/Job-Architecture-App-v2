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
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================================
# HERO IMAGE – mesma largura das demais páginas
# ==========================================================

# tenta jpg depois png
hero_path = None
for candidate in ["assets/home/home_card.jpg", "assets/home/home_card.png"]:
    if Path(candidate).exists():
        hero_path = candidate
        break

if hero_path is None:
    st.error("Imagem do card inicial não encontrada em `assets/home/home_card.{jpg|png}`.")
else:
    # CSS para arredondar cantos da imagem
    st.markdown(
        """
        <style>
        .home-hero img {
            border-radius: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # container padrão (mesma largura das outras páginas)
    with st.container():
        st.markdown('<div class="home-hero">', unsafe_allow_html=True)
        st.image(hero_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# TEXTO ABAIXO DO BANNER (mantendo sua descrição)
# ==========================================================
st.markdown(
    """
    <h1 style="
        font-size:42px;
        margin-top:25px;
        font-weight:800;
        color:#222;
    ">
        Job Architecture
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="
        font-size:20px;
        line-height:1.55;
        margin-top:10px;
        color:#333;
    ">
    A unified database of generic job descriptions that serves as a global reference 
    for classifying, harmonizing, and standardizing all roles across the company.  
    Here you will find consistent titles, clear levels, and internationally aligned profiles.  
    Managers simply select the correct local job, while the system handles the rest—ensuring 
    simplicity, reducing uncertainty, and promoting a fully integrated organizational structure.
    </p>
    """,
    unsafe_allow_html=True,
)
