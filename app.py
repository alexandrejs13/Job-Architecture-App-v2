import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Job Architecture", layout="wide")

# === CSS GLOBAL SIG (carrega fontes, sidebar, layout) ===
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === HERO IMAGE ===
img_path = "assets/home/home_card.jpg"
st.markdown(
    f"""
    <div style="
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 28px;
    ">
        <img src="{img_path}" style="
            width: 100%;
            max-width: 1500px;
            border-radius: 22px;
            object-fit: cover;
        ">
    </div>
    """,
    unsafe_allow_html=True
)

# === BLOCO DE CONTEÚDO MODERNO ===
st.markdown(
    """
    <section style="
        max-width: 1500px;
        margin: 0 auto;
        padding: 10px 0 40px 0;
        border-top: 1px solid #eee;
    ">

        <h1 style="
            font-family: 'PPSIGFlow';
            font-size: 42px;
            font-weight: 600;
            letter-spacing: -0.5px;
            margin-bottom: 14px;
            margin-top: 40px;
            color: #111;
        ">
            Job Architecture
        </h1>

        <p style="
            font-family: 'PPSIGFlow';
            font-size: 19px;
            font-weight: 400;
            line-height: 1.65;
            max-width: 900px;
            color: #333;
            opacity: 0.95;
        ">
            Bem-vindo ao portal de Job Architecture. Aqui você encontra as estruturas organizadas 
            de famílias de cargos, perfis de posição, níveis, responsabilidades e competências 
            essenciais para garantir consistência, governança e alinhamento global.
            <br><br>
            Explore as seções ao lado para navegar por famílias, perfis, comparações, dashboards 
            e muito mais — tudo com a identidade visual SIG e uma experiência totalmente integrada.
        </p>

    </section>
    """,
    unsafe_allow_html=True
)
