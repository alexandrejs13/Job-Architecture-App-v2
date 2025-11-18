import streamlit as st
import base64
import os
import textwrap

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# DESBLOQUEIO DE HTML (resolve escape/sanitização)
# ==========================================================
st.markdown(
    """
    <meta http-equiv="Content-Security-Policy"
          content="default-src * 'unsafe-inline' 'unsafe-eval' data:;
                   style-src * 'unsafe-inline' 'unsafe-eval' data:;">
    """,
    unsafe_allow_html=True,
)

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
# HTML DA TELA INICIAL
# ==========================================================
html = f"""
<style>
@font-face {{
    font-family: 'SIGFlowBold';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: bold;
}}

h1.sig-title {{
    font-family: 'SIGFlowBold', sans-serif;
    font-size: 64px;
    margin: 0px;
    padding: 0px;
    text-align: center;
}}

p.sig-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    margin-top: 6px;
    color: #666;
    text-align: center;
    max-width: 800px;
}}
</style>

<div style="
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:flex-start;
    height:100vh;
    padding-top:40px;
">

    <img src="data:image/png;base64,{icon_b64}"
         style="width:360px; height:360px; margin-bottom:20px;">

    <h1 class="sig-title">Job Architecture</h1>

    <p class="sig-subtitle">
        Integrated global job framework enabling standardized governance and consistent role alignment
    </p>

</div>
"""

# Renderiza corretamente
st.markdown(html, unsafe_allow_html=True)
