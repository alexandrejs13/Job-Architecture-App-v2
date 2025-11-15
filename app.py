import streamlit as st
import importlib
from pathlib import Path
import base64

st.set_page_config(page_title="Job Architecture App", page_icon="🧩", layout="wide")

css = Path("assets/custom.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

MENU = {
    "Job Architecture": {"module": "pages.job_architecture", "icon": "assets/icons/governance.png"},
    "Job Families": {"module": "pages.job_families", "icon": "assets/icons/people_employees.png"},
    "Job Profile Description": {"module": "pages.job_profile_description", "icon": "assets/icons/business_review_clipboard.png"},
    "Job Maps": {"module": "pages.job_maps", "icon": "assets/icons/globe_trade.png"},
    "Job Match": {"module": "pages.job_match", "icon": "assets/icons/checkmark_success.png"},
    "Structure Level": {"module": "pages.structure_level", "icon": "assets/icons/governance.png"},
    "Dashboard": {"module": "pages.dashboard", "icon": "assets/icons/data_2_perfromance.png"},
}

def icon(path):
    try:
        b=base64.b64encode(open(path,"rb").read()).decode()
        return f"<img src='data:image/png;base64,{b}' width='22'>"
    except:
        return ""

with st.sidebar:
    st.image("assets/SIG_Logo_RGB_Black.png", width=160)
    st.markdown("<h3>Menu</h3>", unsafe_allow_html=True)
    choice=None
    for label,info in MENU.items():
        if st.button(f"{icon(info['icon'])} {label}", use_container_width=True):
            choice=label
    if choice is None:
        choice=list(MENU.keys())[0]

mod=importlib.import_module(MENU[choice]["module"])
mod.run()
