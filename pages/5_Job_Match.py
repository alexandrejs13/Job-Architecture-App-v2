
import streamlit as st
st.set_page_config(page_title="Job Match", layout="wide")

col1, col2 = st.columns([0.10, 0.90])
with col1:
    st.image("assets/icons/checkmark_success.png", width=40)
with col2:
    st.title("Job Match")

st.markdown("---")
st.write("Conteúdo da página Job Match.")
