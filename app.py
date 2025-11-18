import streamlit as st
from pathlib import Path

# ------------------------------------------------------------
# CONFIG GLOBAL DO APP
# ------------------------------------------------------------
st.set_page_config(
    page_title="Job Architecture App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CSS GLOBAL SIG (layout_global.css)
# ------------------------------------------------------------
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS global não encontrado: assets/css/layout_global.css")

# ------------------------------------------------------------
# HOME — CARTÃO CENTRALIZADO
# ------------------------------------------------------------
st.markdown(
    """
    <div style="
        display:flex;
        justify-content:center;
        width:100%;
        margin-top:40px;
    ">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        max-width:900px;
        width:100%;
        background-color:#f2efeb;
        padding:30px;
        border-radius:20px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
    ">
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# IMAGEM DO CARD
# ------------------------------------------------------------
st.image("assets/home/home_card.jpg", use_column_width=True)

# ------------------------------------------------------------
# TÍTULO
# ------------------------------------------------------------
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
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# DESCRIÇÃO
# ------------------------------------------------------------
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
    unsafe_allow_html=True
)
