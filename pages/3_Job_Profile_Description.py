# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação de até 3 perfis

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER PADRÃO
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700; font-family:'PPSIGFlow', sans-serif;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/people_employees.png", "Job Profile Description")


# ==========================================================
# CSS GLOBAL
# ==========================================================
custom_css = """
<style>

@font-face {
    font-family: 'PPSIGFlow';
    src: url('/mount/src/job-architecture-app/assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
}

body, p, div, span, h1, h2, h3, h4 {
    font-family: 'PPSIGFlow', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

.block-container {
    max-width: 1600px !important;
    padding-top: 1rem !important;
}

.jp-comparison-grid {
    display: grid;
    gap: 20px;
    width: 100%;
}

.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 650px;
    overflow-y: auto;
}

.jp-title {
    font-size: 1.35rem;
    font-weight: 800;
}

.jp-gg {
    font-size: 1rem;
    font-weight: 700;
    color: #145efc;
    margin-bottom: 12px;
}

.jp-meta-block {
    margin-bottom: 18px;
}

.jp-meta-row {
    font-size: 0.95rem;
    padding: 3px 0;
}

.jp-section {
    border-left: 5px solid #145efc;
    padding-left: 12px;
    margin-bottom: 22px;
}

.jp-section.alt {
    background: #fafafa;
    border-left-color: #1d6bff !important;
    border-radius: 8px;
    padding: 12px;
}

.jp-section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #145efc;
    display: flex;
    align-items: center;
    gap: 8px;
}

.jp-section-title img {
    width: 22px;
    height: 22px;
}

.jp-text {
    margin-top: 4px;
    white-space: pre-wrap;
    line-height: 1.45;
    font-size: 0.93rem;
    color: #444;
}

.jp-footer {
    margin-top: auto;
    text-align: right;
}

.jp-footer img {
    width: 26px;
    opacity: 0.75;
    cursor: pointer;
}

.jp-footer img:hover {
    opacity: 1;
    transform: scale(1.1);
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================================
# CARREGAR BASE
# ==========================================================
@st.cache_data
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
    return df

df = load_job_profile()

if df.empty:
    st.error("Arquivo 'Job Profile.xlsx' não encontrado.")
    st.stop()


# ==========================================================
# FILTROS
# ==========================================================
st.markdown(
    '<div style="font-size:1.3rem; font-weight:700; margin-bottom:1rem;">🔍 Explorador de Perfis</div>',
    unsafe_allow_html=True,
)

familias = sorted(df["Job Family"].dropna().unique())
col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family", ["Selecione..."] + familias)

with col2:
    subs = (
        sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique())
        if familia != "Selecione..."
        else []
    )
    sub = st.selectbox("Sub Job Family", ["Selecione..."] + subs)

with col3:
    paths = (
        sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique())
        if sub != "Selecione..."
        else []
    )
    trilha = st.selectbox("Career Path", ["Selecione..."] + paths)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar perfis.")
    st.stop()


# ==========================================================
# PICKLIST
# ==========================================================
filtered["label"] = filtered.apply(
    lambda r: f"GG {r['Global Grade']} • {r['Job Profile']}", axis=1
)
label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis:", options=list(label_to_profile.keys()), max_selections=3
)

if not selecionados_labels:
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]


# ==========================================================
# CARDS
# ==========================================================
cards_data = [
    filtered[filtered["Job Profile"] == nome].iloc[0].to_dict()
    for nome in selecionados
]

num_cards = len(cards_data)
grid_style = f"grid-template-columns: repeat({num_cards}, 1fr);"

st.markdown("### ✨ Comparativo de Perfis Selecionados")

html_parts = [f'<div class="jp-comparison-grid" style="{grid_style}">']


# MAPA DE SEÇÕES = (icone, título, coluna)
sections = [
    ("assets/icons/sig/Hierarchy.svg", "🧭 Sub Job Family Description", "Sub Job Family Description"),
    ("assets/icons/sig/File_Clipboard_Text.svg", "🧠 Job Profile Description", "Job Profile Description"),
    ("assets/icons/sig/Hierarchy.svg", "🏛️ Career Band Description", "Career Band Description"),
    ("assets/icons/sig/Shopping_Business_Target.svg", "🎯 Role Description", "Role Description"),
    ("assets/icons/sig/Edit_Pencil.svg", "🏅 Grade Differentiator", "Grade Differentiator"),
    ("assets/icons/sig/Content_Book_Phone.svg", "🎓 Qualifications", "Qualifications"),
    ("assets/icons/sig/Graph_Bar.svg", "📌 Specific parameters / KPIs", "Specific parameters / KPIs"),
    ("assets/icons/sig/Setting_Cog.svg", "⚙️ Competencies 1", "Competencies 1"),
    ("assets/icons/sig/Setting_Cog.svg", "⚙️ Competencies 2", "Competencies 2"),
    ("assets/icons/sig/Setting_Cog.svg", "⚙️ Competencies 3", "Competencies 3"),
]


# ==========================================================
# RENDER DOS CARDS
# ==========================================================
for card in cards_data:

    job = html.escape(card["Job Profile"])
    gg = html.escape(str(card["Global Grade"]))
    fml = html.escape(card["Job Family"])
    subf = html.escape(card["Sub Job Family"])
    path = html.escape(card["Career Path"])
    full = html.escape(card["Full Job Code"])

    block = []
    block.append('<div class="jp-card">')

    block.append(f'<div class="jp-title">{job}</div>')
    block.append(f'<div class="jp-gg">GG {gg}</div>')

    block.append('<div class="jp-meta-block">')
    block.append(f'<div class="jp-meta-row"><b>Job Family:</b> {fml}</div>')
    block.append(f'<div class="jp-meta-row"><b>Sub Job Family:</b> {subf}</div>')
    block.append(f'<div class="jp-meta-row"><b>Career Path:</b> {path}</div>')
    block.append(f'<div class="jp-meta-row"><b>Full Job Code:</b> {full}</div>')
    block.append('</div>')

    for idx, (icon, title, col) in enumerate(sections):
        text = html.escape(str(card.get(col, ""))).strip()
        if not text:
            continue

        css_class = "jp-section alt" if idx % 2 else "jp-section"
        block.append(f'<div class="{css_class}">')
        block.append(
            f'<div class="jp-section-title"><img src="{icon}">{title}</div>'
        )
        block.append(f'<div class="jp-text">{text}</div>')
        block.append("</div>")

    block.append('<div class="jp-footer">')
    block.append('<img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">')
    block.append("</div>")

    block.append("</div>")
    html_parts.append("".join(block))

html_parts.append("</div>")
st.markdown("".join(html_parts), unsafe_allow_html=True)
