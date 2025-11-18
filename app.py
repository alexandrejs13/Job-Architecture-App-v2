import streamlit as st
from pathlib import Path

# ==========================================================
# CONFIG GLOBAL
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CSS GLOBAL SIG (FONTE, CORES, LAYOUT)
# ==========================================================
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================================
# CSS MODERNO EXCLUSIVO DA HOME (SAFE)
# ==========================================================
st.markdown(
    """
    <style>

    /* Fade-in do conteúdo */
    .fade-in {
        opacity: 0;
        animation: fadeIn 1.2s ease-out forwards;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Glass container */
    .glass-box {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 36px 42px;
        border: 1px solid rgba(255,255,255,0.35);
        margin-top: -80px; /* sobe sobre a imagem */
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }

    /* linha sutil */
    .divider {
        height: 1px;
        background: #eee;
        margin: 34px 0 34px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# HERO IMAGE — moderna, grande, “hero section”
# ==========================================================
img_path = "assets/home/home_card.jpg"

st.markdown(
    f"""
    <div style="
        width:100%;
        height:auto;
        display:flex;
        justify-content:center;
        margin-top: 18px;
        margin-bottom: 0px;
    ">
        <img src="{img_path}" style="
            width: 100%;
            max-width: 1500px;
            border-radius: 26px;
            object-fit: cover;
            box-shadow: 0 12px 34px rgba(0,0,0,0.15);
        ">
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# GLASS PANEL + TEXTO MODERNO
# ==========================================================
st.markdown(
    """
    <div style="width:100%; display:flex; justify-content:center;">
        <div class="glass-box fade-in" style="max-width:1500px; width:100%;">

            <h1 style="
                font-family: 'PPSIGFlow';
                font-size: 46px;
                font-weight: 600;
                letter-spacing: -0.6px;
                margin-bottom: 16px;
                color: #111;
            ">
                Job Architecture
            </h1>

            <p style="
                font-family: 'PPSIGFlow';
                font-size: 20px;
                font-weight: 400;
                line-height: 1.65;
                color: #333;
                max-width: 920px;
                opacity: .96;
            ">
                Bem-vindo ao portal de Job Architecture. Aqui você encontra as estruturas organizadas 
                de famílias de cargos, perfis de posição, níveis, responsabilidades e competências 
                essenciais para garantir consistência, governança e alinhamento global.
            </p>

            <div class="divider"></div>

            <p style="
                font-family: 'PPSIGFlow';
                font-size: 20px;
                font-weight: 400;
                line-height: 1.65;
                color: #333;
                max-width: 920px;
                opacity: .96;
            ">
                Explore as seções ao lado para navegar por famílias, perfis, comparações, dashboards 
                e muito mais — tudo com a identidade visual SIG e uma experiência totalmente integrada.
            </p>

        </div>
    </div>
    """,
    unsafe_allow_html=True
)
