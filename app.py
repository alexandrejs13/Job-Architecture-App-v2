import streamlit as st

def load_css():
    with open("assets/sig_theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.set_page_config(page_title="Job Architecture App", layout="wide")

with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.markdown("---")

st.markdown("# Bem-vindo ao Job Architecture App")
st.write("Selecione uma página no menu à esquerda.")
