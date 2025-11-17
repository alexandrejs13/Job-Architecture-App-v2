import streamlit as st
from pathlib import Path

def load_global_css():
    fonts_path = Path("assets/css/fonts")

    css = f"""
    <style>

    /*****************************************************************
     *  FONTES PP-SIG FLOW – REGULAR / SEMIBOLD / BOLD
     *****************************************************************/

    @font-face {{
        font-family: 'PPSIGFlow';
        src: url('{fonts_path / "PPSIGFlow-Regular.otf"}') format("opentype");
        font-weight: 400;
        font-style: normal;
    }}

    @font-face {{
        font-family: 'PPSIGFlow';
        src: url('{fonts_path / "PPSIGFlow-SemiBold.otf"}') format("opentype");
        font-weight: 600;
        font-style: normal;
    }}

    @font-face {{
        font-family: 'PPSIGFlow';
        src: url('{fonts_path / "PPSIGFlow-Bold.otf"}') format("opentype");
        font-weight: 700;
        font-style: normal;
    }}

    html, body, [class*="css"], * {{
        font-family: 'PPSIGFlow', -apple-system, BlinkMacSystemFont, Segoe UI,
                     Roboto, Oxygen, Ubuntu, Cantarell, sans-serif !important;
        letter-spacing: -0.2px !important;
    }}

    /*****************************************************************
     *  LAYOUT GLOBAL DO APP – FUNDO, SIDEBAR, CONTAINER
     *****************************************************************/

    [data-testid="stAppViewContainer"] {{
        background: #ffffff !important;
        color: #222 !important;
    }}

    .block-container {{
        max-width: 1600px !important;
        padding-top: 1rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    [data-testid="stSidebar"] {{
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }}

    [data-testid="stSidebar"] > div {{
        width: 300px !important;
    }}

    /*****************************************************************
     *  BOTÕES STREAMLIT – ESTILO PADRÃO SIG BLUE
     *****************************************************************/

    .stButton > button {{
        background: #145efc !important;
        color: white !important;
        border-radius: 28px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.2s ease-in-out;
        font-family: 'PPSIGFlow' !important;
    }}

    .stButton > button:hover {{
        background: #0d4ccc !important;
        transform: translateY(-1px);
    }}

    /*****************************************************************
     *  GRID DE CARDS – BASE GLOBAL
     *****************************************************************/

    .jp-grid {{
        display: grid;
        gap: 20px;
        width: 100%;
    }}

    .jp-card {{
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        display: flex;
        flex-direction: column;
        height: 650px;
        overflow-y: auto;
        position: relative;
    }}

    .jp-card::-webkit-scrollbar {{
        width: 8px;
    }}
    .jp-card::-webkit-scrollbar-thumb {{
        background: #c8c8c8;
        border-radius: 10px;
    }}

    .jp-card-header {{
        position: sticky;
        top: 0;
        background: white;
        padding-bottom: 12px;
        padding-top: 6px;
        z-index: 6;
        border-bottom: 1px solid #eee;
    }}

    .jp-title {{
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 4px;
        color: #222;
    }}

    .jp-gg {{
        color: #145efc;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .jp-meta-block {{
        margin-bottom: 18px;
        font-size: 0.95rem;
    }}

    .jp-meta-row {{
        padding: 3px 0;
    }}

    /*****************************************************************
     *  SEÇÕES
     *****************************************************************/

    .jp-section {{
        padding-left: 12px;
        margin-bottom: 22px;
        border-radius: 8px;
    }}

    .jp-section-title {{
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 6px;
        color: #145efc;
        font-family: 'PPSIGFlow' !important;
    }}

    .jp-text {{
        white-space: pre-wrap;
        line-height: 1.45;
        color: #444;
        font-size: 0.93rem;
    }}

    .jp-section:nth-child(even) {{
        background: #fafafa;
    }}

    /*****************************************************************
     *  PDF ICON (final do card)
     *****************************************************************/

    .pdf-button {{
        margin-top: 14px;
        background: #145efc;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        width: fit-content;
        transition: 0.15s ease-in-out;
        font-family: 'PPSIGFlow' !important;
    }}

    .pdf-button:hover {{
        background: #0d4ccc;
        transform: translateY(-1px);
    }}

    /*****************************************************************
     *  FULLSCREEN MODE
     *****************************************************************/

    .fullscreen-wrapper {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

