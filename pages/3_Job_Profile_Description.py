import streamlit as st

# PNG no título
st.markdown(f"""
<div style='display:flex; align-items:center; gap:16px; margin-top:20px;'>
    <img src='assets/icons/business_review_clipboard.png' width='48'>
    <h1 style='margin:0;'>Job Profile Description</h1>
</div>
""", unsafe_allow_html=True)

st.write("Conteúdo da página Job Profile Description.")
