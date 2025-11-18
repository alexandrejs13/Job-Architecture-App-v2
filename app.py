import streamlit as st
import base64
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG INLINE
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER — CENTRALIZADO
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

html_home = """
<div style='
    min-height:70vh;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
'>
    <img src='data:image/png;base64:{icon}' style='width:200px; height:200px; margin-bottom:25px;'>
    <h1 style='
        font-size:46px;
        font-weight:700;
        margin:0;
        padding:0;
        text-align:center;
    '>
        Job Architecture
    </h1>
</div>
"""

st.markdown(html_home.format(icon=icon_b64), unsafe_allow_html=True)
