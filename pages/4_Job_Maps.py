
import streamlit as st
st.set_page_config(page_title="Job Maps", layout="wide")

col1, col2 = st.columns([0.12, 0.88])
with col1:
    st.image("assets/icons/globe_trade.png", width=48)
with col2:
    st.title("Job Maps")

st.markdown("---")

st.write("Conteúdo da página Job Maps.")
