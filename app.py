import streamlit as st
import importlib, base64
from pathlib import Path

st.set_page_config(page_title="Job Architecture App", page_icon="🧩", layout="wide", menu_items={})

def b64(path):
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode()

MENU = {
    "Job Architecture": ("pages.job_architecture","assets/icons/governance.png"),
    "Job Families": ("pages.job_families","assets/icons/people_employees.png"),
    "Job Profile Description": ("pages.job_profile_description","assets/icons/business_review_clipboard.png"),
    "Job Maps": ("pages.job_maps","assets/icons/globe_trade.png"),
    "Job Match": ("pages.job_match","assets/icons/checkmark_success.png"),
    "Structure Level": ("pages.structure_level","assets/icons/governance.png"),
    "Dashboard": ("pages.dashboard","assets/icons/data_2_perfromance.png"),
}

params=st.query_params
current=params.get("page",["Job Architecture"])[0]

# LOAD CSS & JS
st.markdown(f"<style>{Path('assets/css/navbar.css').read_text()}</style>", unsafe_allow_html=True)
st.markdown(f"<script>{Path('assets/js/menu.js').read_text()}</script>", unsafe_allow_html=True)

# NAVBAR
logo_b64=b64("assets/icons/SIG_Logo_RGB_Black.png")
nav_html=f"""
<div class="navbar">
  <div class="nav-left">
    <img src="data:image/png;base64,{logo_b64}" height="40">
    <span style="font-size:22px;font-weight:700;">Job Architecture App</span>
  </div>
  <div class="nav-right" id="nav-right">
"""

for label,(mod,icon) in MENU.items():
    icon_b=b64(icon)
    sel="nav-selected" if label==current else ""
    nav_html+=f"""
<a class="nav-item {sel}" href="/?page={label}">
  <img class="nav-icon" src="data:image/png;base64,{icon_b}"/>
  <span>{label}</span>
</a>
"""

nav_html+="</div></div>"
st.markdown(nav_html, unsafe_allow_html=True)

mod=importlib.import_module(MENU[current][0])
mod.run()
