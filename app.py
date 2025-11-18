import streamlit as st
from pathlib import Path

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# IMPORTA O CSS GLOBAL SIG (fonte, sidebar, layout)
# ==========================================================
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================================
# HERO IMAGE — inicia a página diretamente pela imagem
# ==========================================================
image_path = Path("assets/home/home_card.jpg")

if image_path.exists():
    st.image(str(image_path), use_column_width=True)
else:
    st.error("Imagem não encontrada: assets/home/home_card.jpg")


# ==========================================================
# TÍTULO + TEXTO — usando a fonte SIG (PPSIGFlow)
# ==========================================================
st.markdown(
    """
    <div style="margin-top: 24px;">

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
    unsafe_allow_html=True
)
