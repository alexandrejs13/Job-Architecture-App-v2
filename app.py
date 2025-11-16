import streamlit as st

st.set_page_config(page_title="Job Architecture App", layout="wide")

# Logo (só aqui)
with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.markdown("---")

st.title("Bem-vindo ao Job Architecture App")
st.write("Selecione uma página no menu à esquerda.")
