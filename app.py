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
# HEADER — HOME CENTRALIZADA
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

html_home = f"""
<div style='
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 40px;
'>
    <img src='data:image/png;base64,{icon_b64}'
         style='
            width: 200px;
            height: 200px;
            margin-bottom: 28px;
         '>

    <h1 style='
        font-size: 48px;
        font-weight: 700;
        margin: 0;
        padding: 0;
        text-align: center;
    '>
        Job Architecture
    </h1>
</div>
"""

st.markdown(html_home, unsafe_allow_html=True)
