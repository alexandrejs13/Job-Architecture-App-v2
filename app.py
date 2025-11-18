import streamlit as st
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# HERO IMAGE (topo da página, largura igual às demais)
# ==========================================================
st.markdown("""
<div style="display:flex; justify-content:center; margin-top:20px;">
    <img src="./assets/home/home_card.jpg"
         style="width:100%; max-width:1100px; border-radius:22px; box-shadow:0 6px 14px rgba(0,0,0,0.08);">
</div>
""", unsafe_allow_html=True)

# ==========================================================
# TÍTULO PRINCIPAL
# ==========================================================
st.markdown("""
<div style="
    max-width:1100px;
    margin-left:auto;
    margin-right:auto;
    margin-top:32px;
">
    <h1 style="
        font-size:42px;
        font-weight:800;
        margin:0;
        padding:0;
        color:#222;
    ">
        Job Architecture
    </h1>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# DESCRIÇÃO
# ==========================================================
st.markdown("""
<div style="
    max-width:1100px;
    margin-left:auto;
    margin-right:auto;
    margin-top:12px;
    font-size:20px;
    line-height:1.55;
    color:#333;
">
A unified database of generic job descriptions that serves as a global reference 
for classifying, harmonizing, and standardizing all roles across the company.  
<br><br>
Here you will find consistent titles, clear levels, and internationally aligned profiles.  
Managers simply select the correct local job, while the system handles the rest—ensuring 
simplicity, reducing uncertainty, and promoting a fully integrated organizational structure.
</div>
""", unsafe_allow_html=True)
