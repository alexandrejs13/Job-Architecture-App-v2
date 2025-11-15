import streamlit as st

# PNG no título
st.markdown(f"""
<div style='display:flex; align-items:center; gap:16px; margin-top:20px;'>
    <img src='assets/icons/data_2_perfromance.png' width='48'>
    <h1 style='margin:0;'>Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.write("Conteúdo da página Dashboard.")
