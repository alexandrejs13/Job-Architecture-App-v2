import streamlit as st
import pandas as pd
import base64
import pdfkit
from pathlib import Path
from utils.global_css import load_global_css

# ==========================================================
# CONFIGURAÇÃO GERAL
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")
load_global_css()

# ==========================================================
# HEADER SIG DO APP
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style='margin:0; padding:0; font-size:36px; font-weight:700;'>
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CARREGAR DADOS
# ==========================================================
df = pd.read_excel("data/Job Profile.xlsx")

# Limpeza
df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(".0", "", regex=False)

# ==========================================================
# FILTROS
# ==========================================================
st.markdown("### Explorador de Perfis de Cargo")

col1, col2, col3 = st.columns(3)

with col1:
    fam = st.selectbox("Job Family", sorted(df["Job Family"].unique()))

with col2:
    subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
    subfam = st.selectbox("Sub Job Family", subs)

with col3:
    paths = sorted(df[(df["Job Family"] == fam) & (df["Sub Job Family"] == subfam)]["Career Path"].unique())
    career = st.selectbox("Career Path", paths)

filtered = df[
    (df["Job Family"] == fam) &
    (df["Sub Job Family"] == subfam) &
    (df["Career Path"] == career)
]

# PICKLIST
filtered["label"] = filtered.apply(
    lambda r: f"GG {r['Global Grade']} • {r['Job Profile']}",
    axis=1
)

selected_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(filtered["label"]),
    max_selections=3
)

if not selected_labels:
    st.stop()

selected_profiles = []
for lbl in selected_labels:
    jp = lbl.split("•", 1)[1].strip()
    row = filtered[filtered["Job Profile"] == jp].iloc[0]
    selected_profiles.append(row)

# ==========================================================
# FULLSCREEN (igual Job Maps)
# ==========================================================
if "fs3" not in st.session_state:
    st.session_state.fs3 = False

# botão aparece abaixo dos filtros
btn_col, _ = st.columns([0.13, 0.87])

with btn_col:
    if not st.session_state.fs3:
        if st.button("Tela Cheia"):
            st.session_state.fs3 = True
            st.rerun()
    else:
        if st.button("Sair"):
            st.session_state.fs3 = False
            st.rerun()

if st.session_state.fs3:
    st.markdown("<div class='fullscreen-wrapper'>", unsafe_allow_html=True)

# ==========================================================
# GERAÇÃO DO GRID DINÂMICO
# ==========================================================
num = len(selected_profiles)
grid_css = f"""
<div class="jp-grid" style="grid-template-columns: repeat({num}, 1fr);">
"""
st.markdown("### Comparação de Perfis", unsafe_allow_html=True)
st.markdown(grid_css, unsafe_allow_html=True)

# ==========================================================
# FUNÇÃO PARA EXPORTAR PDF
# ==========================================================
def create_pdf(card_html, filename):
    pdfkit.from_string(card_html, filename)

def pdf_download_button(card_html, filename):
    pdf_file = f"/mnt/data/{filename}"
    pdfkit.from_string(card_html, pdf_file)
    with open(pdf_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"""
    <a href="data:application/pdf;base64,{b64}" download="{filename}">
        <img class="pdf-icon" src="https://cdn-icons-png.flaticon.com/512/337/337946.png">
    </a>
    """

# ==========================================================
# CAMPOS DAS SEÇÕES EM ORDEM
# ==========================================================
sections = [
    ("🧭 Sub Job Family Description", "Sub Job Family Description"),
    ("🧠 Job Profile Description", "Job Profile Description"),
    ("🏛️ Career Band Description", "Career Band Description"),
    ("🎯 Role Description", "Role Description"),
    ("🏅 Grade Differentiator", "Grade Differentiator"),
    ("🎓 Qualifications", "Qualifications"),
    ("📌 Specific parameters / KPIs", "Specific parameters / KPIs"),
    ("⚙️ Competencies 1", "Competencies 1"),
    ("⚙️ Competencies 2", "Competencies 2"),
    ("⚙️ Competencies 3", "Competencies 3"),
]

# ==========================================================
# RENDERIZA OS CARDS
# ==========================================================
for row in selected_profiles:
    card_id = row["Job Profile"].replace(" ", "_")

    # Cabeçalho do card
    card_html = f"""
    <div class="jp-card">
        {pdf_download_button("PDF TEMP", f"{card_id}.pdf")}
        <div class="jp-card-header">
            <div class="jp-title">{row['Job Profile']}</div>
            <div class="jp-gg">GG {row['Global Grade']}</div>

            <div class="jp-meta-block">
                <div class="jp-meta-row"><b>Job Family:</b> {row['Job Family']}</div>
                <div class="jp-meta-row"><b>Sub Job Family:</b> {row['Sub Job Family']}</div>
                <div class="jp-meta-row"><b>Career Path:</b> {row['Career Path']}</div>
                <div class="jp-meta-row"><b>Full Job Code:</b> {row['Full Job Code']}</div>
            </div>
        </div>
    """

    # Seções
    for title, field in sections:
        value = str(row[field]).strip()
        if value and value.lower() != "nan":
            card_html += f"""
            <div class="jp-section">
                <div class="jp-section-title">{title}</div>
                <div class="jp-text">{value}</div>
            </div>
            """

    card_html += "</div>"

    st.markdown(card_html, unsafe_allow_html=True)

# Fecha fullscreen
if st.session_state.fs3:
    st.markdown("</div>", unsafe_allow_html=True)

# Fecha grid
st.markdown("</div>", unsafe_allow_html=True)
