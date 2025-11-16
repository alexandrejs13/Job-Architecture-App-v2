import streamlit as st

# Cabeçalho com ícone (nativo)
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("assets/icons/business_review_clipboard.png", width=36)
with col2:
    st.header("Job Profile Description")

st.markdown("---")
st.write("Conteúdo da página Job Profile Description.")
