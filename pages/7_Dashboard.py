import streamlit as st

# Configuração da página para o menu lateral (usando ícone Lucide)
st.set_page_config(
    page_title="Dashboard", 
    layout="wide",
    icon="bar-chart-2" 
)

# Ícone PNG no título da página (usando HTML/Markdown para controle de tamanho)
st.markdown(
    """
    <style>
    .page-title-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .page-title-icon {
        height: 1.2em; /* Ajusta o tamanho do ícone para a proporção da fonte */
        width: auto;
        vertical-align: middle;
    }
    </style>
    <div class="page-title-container">
        <img src="icons/data 2 perfomance.png" class="page-title-icon">
        <h1>Dashboard</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("Page: Dashboard")
