
import streamlit as st
st.set_page_config(page_title="Job Profile Description", layout="wide")

col1, col2 = st.columns([0.12, 0.88])
with col1:
    st.image("assets/icons/business_review_clipboard.png", width=48)
with col2:
    st.title("Job Profile Description")

st.markdown("---")

st.write("Conteúdo da página Job Profile Description.")
