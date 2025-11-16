import streamlit as st

# Configuração da página para o menu lateral (usando ícone Lucide)
st.set_page_config(
    page_title="Job Profile Description", 
    layout="wide",
    icon="clipboard-list" 
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
        <img src="icons/business review clipboard.png" class="page-title-icon">
        <h1>Job Profile Description</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("Page: Job Profile Description")
