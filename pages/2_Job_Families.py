
import streamlit as st
st.set_page_config(page_title="Job Families", layout="wide")

col1, col2 = st.columns([0.10, 0.90])
with col1:
    st.image("assets/icons/people_employees.png", width=40)
with col2:
    st.title("Job Families")

st.markdown("---")
st.write("Conteúdo da página Job Families.")
