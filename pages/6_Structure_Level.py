
import streamlit as st
st.set_page_config(page_title="Structure Level", layout="wide")

col1, col2 = st.columns([0.10, 0.90])
with col1:
    st.image("assets/icons/process.png", width=40)
with col2:
    st.title("Structure Level")

st.markdown("---")
st.write("Conteúdo da página Structure Level.")
