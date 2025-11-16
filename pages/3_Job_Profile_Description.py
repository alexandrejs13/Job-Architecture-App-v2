import streamlit as st

# LOGO EM TODAS AS PÁGINAS
with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.markdown("---")

# Cabeçalho com ícone nítido e alinhado
col1, col2 = st.columns([0.10, 0.90])
with col1:
    st.image("assets/icons/business_review_clipboard.png", width=28)
with col2:
    st.markdown("## Job Profile Description")

st.markdown("---")
st.write("Conteúdo da página Job Profile Description.")
