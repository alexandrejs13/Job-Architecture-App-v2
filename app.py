import streamlit as st
import base64
import os

st.set_page_config(page_title="Job Architecture", layout="wide")

def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

html = f"""
<style>
@font-face {{
    font-family: 'SIGFlowBold';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
}}

@font-face {{
    font-family: 'SIGFlowRegular';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
}}

h1.sig-title {{
    font-family: 'SIGFlowBold', sans-serif;
    font-size: 64px;
    text-align: center;
    margin: 0;
}}

p.sig-subtitle {{
    font-family: 'SIGFlowRegular', sans-serif;
    font-size: 20px;
    color: #555;
    text-align: center;
    max-width: 800px;
    margin: 10px auto 0 auto;
}}
</style>

<div style="text-align:center; padding-top:40px;">

    <!-- ICON — Elegant: 300px + small spacing -->
    <img src="data:image/png;base64,{icon_b64}"
         style="width:300px; margin-bottom:10px;">

    <h1 class="sig-title">Job Architecture</h1>

    <p class="sig-subtitle">
        A global job framework designed to standardize governance and harmonize roles across the organization.
    </p>

</div>
"""

st.components.v1.html(html, height=800)
