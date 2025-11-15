import streamlit as st
def run():
    st.markdown(f"""<div class='page-header'>
    <img src='assets/icons/checkmark_success.png' class='page-icon'>
    <h1>Job Match</h1>
    </div>""", unsafe_allow_html=True)
    st.write("Conteúdo da página Job Match")
