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
# ICON PATH
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

# ==========================================================
# HOME SCREEN — ÍCONE GIGANTE + SIG FLOW + SUBTÍTULO
# ==========================================================
st.markdown(f"""
<style>
@font-face {{
    font-family: 'SIGFlowBold';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: bold;
}}

h1.sig-title {{
    font-family: 'SIGFlowBold', sans-serif;
    font-size: 64px;
    font-weight: bold;
    margin: 0;
    padding: 0;
    text-align: center;
}}

p.sig-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    color: #555;
    margin-top: 12px;
    margin-bottom: 0;
    text-align: center;
    max-width: 800px;
}}
</style>

<div style="
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
">
    
    <img src="data:image/png;base64,{icon_b64}"
         style="width: 400px; height: 400px; margin-bottom: 32px;">
    
    <h1 class="sig-title">Job Architecture</h1>

    <p class="sig-subtitle">
        Integrated global job framework enabling standardized governance and consistent role alignment
    </p>

</div>
""", unsafe_allow_html=True)
