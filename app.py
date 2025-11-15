import streamlit as st

st.set_page_config(page_title="Job Architecture App", layout="wide")

# Logo centralizado acima do menu nativo
with st.sidebar:
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.markdown("<br>", unsafe_allow_html=True)

st.write("# Bem-vindo ao Job Architecture App")
st.write("Selecione uma página no menu à esquerda.")
