import streamlit as st
st.set_page_config(page_title="Job Architecture", layout="wide")

col1, col2 = st.columns([0.12, 0.88])
with col1:
    st.image("assets/icons/governance.png", width=48)
with col2:
    st.title("Job Architecture")

st.markdown("---")

st.write("Conteúdo da página Job Architecture.")
