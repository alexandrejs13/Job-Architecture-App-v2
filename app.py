
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Job Architecture", page_icon="📊", layout="wide")

st.markdown('\n<style>\nimg.menu-icon {\n    width:40px !important;\n    margin-right:8px;\n    vertical-align:middle;\n}\n</style>\n', unsafe_allow_html=True)

icon_path = Path(__file__).resolve().parent / "icons" / "sig_icon.png"

col1,col2 = st.columns([1,8])
with col1:
    st.image(str(icon_path), width=120)
with col2:
    st.markdown("<h1 style='font-weight:700;'>Job Architecture</h1>", unsafe_allow_html=True)

st.write("""A single global database of generic job descriptions that serves as the reference to classify,
harmonize, and standardize all SIG positions. Here, you find consistent job titles, clear levels,
and globally aligned profiles — all structured so that managers only need to select the correct local position.""")
