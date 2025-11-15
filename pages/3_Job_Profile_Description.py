import streamlit as st

# LOGO em todas as páginas
with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.markdown("<br>", unsafe_allow_html=True)

# Cabeçalho com ícone
st.markdown(f"""
<div style='display:flex; align-items:center; gap:16px;'>
    <img src="/app/assets/icons/business_review_clipboard.png" width="48">
    <h1>Job Profile Description</h1>
</div>
""", unsafe_allow_html=True)

st.write("Conteúdo da página Job Profile Description.")
