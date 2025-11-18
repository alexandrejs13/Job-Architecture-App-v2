import streamlit as st
import base64
import os
import textwrap

# CONFIG
st.set_page_config(page_title="Job Architecture", layout="wide")

# FUNÇÃO PNG
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ICON
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

# HTML FINAL
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
    font-weight: bold;
    margin: 0;
    padding: 0;
    text-align: center;
}}

p.sig-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    color: #555;
    margin-top: 8px;
    margin-bottom: 0;
    text-align: center;
    max-width: 800px;
}}
</style>

<div style="
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding-top: 40px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width: 350px; height: 350px; margin-bottom: 16px;">

    <h1 class="sig-title" style="margin-top: 0px;">Job Architecture</h1>

    <p class="sig-subtitle">
        Integrated global job framework enabling standardized governance and consistent role alignment
    </p>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
