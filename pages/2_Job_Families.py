import streamlit as st

def load_css():
    with open("assets/sig_theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.markdown("---")

col1, col2 = st.columns([0.10, 0.90])
with col1:
    st.image("assets/icons/people_employees.png", width=28)
with col2:
    st.markdown("# Job Families")

st.write("Conteúdo da página Job Families.")
