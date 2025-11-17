# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação de até 3 perfis (SIG Design System)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS GLOBAL
# ==========================================================
custom_css = """
<style>

@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
    font-weight: 400;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-SemiBold.otf') format('opentype');
    font-weight: 600;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: 700;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

.block-container {
    max-width: 1600px !important;
    padding-top: 1rem !important;
}

/* GRID */
.jp-comparison-grid {
    display: grid;
    gap: 24px;
}

/* CARD */
.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    padding: 0;
    position: relative;
    overflow: visible !important;
}

/* 🔥 CABEÇALHO FIXO (fixo NA PÁGINA e sem texto aparecendo atrás!) */
.jp-card-header {
    position: sticky;
    top: 90px;
    background: #ffffff;
    padding: 18px 22px 14px 22px;
    z-index: 50;
    border-bottom: 1px solid #eee;
    box-shadow: 0 3px 8px rgba(0,0,0,0.06);
}

/* Títulos */
.jp-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 12px;
}

/* META BLOCK */
.jp-meta-block {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.9rem;
}

/* SEÇÕES */
.jp-section {
    padding: 14px 22px;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section.alt {
    background: #fafafa;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.92rem;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.jp-section-title img {
    width: 20px;
    opacity: 0.9;
}

.jp-text {
    line-height: 1.45;
    font-size: 0.9rem;
    white-space: pre-wrap;
}

/* FOOTER PDF */
.jp-footer {
    padding: 15px;
    text-align: right;
}

.jp-footer img {
    width: 26px;
    opacity: 0.8;
    cursor: pointer;
}

.jp-footer img:hover {
    opacity: 1;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================================
# LOAD JOB PROFILE
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df

df = load_job_profile()
if df.empty:
    st.error("Erro ao carregar Job Profile.xlsx")
    st.stop()

# ==========================================================
# FILTROS
# ==========================================================
st.subheader("🔍 Explorador de Perfis")

familias = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family", ["Selecione..."] + familias)

with col2:
    subs = sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()) if familia != "Selecione..." else []
    sub = st.selectbox("Sub Job Family", ["Selecione..."] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()) if sub != "Selecione..." else []
    trilha = st.selectbox("Career Path", ["Selecione..."] + paths)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

# ==========================================================
# PICKLIST
# ==========================================================
filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.info("Selecione ao menos 1 perfil.")
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]
rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in selecionados]

num = len(rows)
grid_template = f"grid-template-columns: repeat({num}, 1fr);"

st.markdown("---")
st.markdown("### ✨ Comparativo de Perfis Selecionados")

# Ícones
icons = {
    "Sub Job Family Description": "Hierarchy.svg",
    "Job Profile Description": "File_Clipboard_Text.svg",
    "Career Band Description": "Hierarchy.svg",
    "Role Description": "Shopping_Business_Suitcase.svg",
    "Grade Differentiator": "Edit_Pencil.svg",
    "Qualifications": "Content_Book_Phone.svg",
    "Specific parameters / KPIs": "Graph_Bar.svg",
    "Competencies 1": "Setting_Cog.svg",
    "Competencies 2": "Setting_Cog.svg",
    "Competencies 3": "Setting_Cog.svg",
}

sections_order = list(icons.keys())

html_parts = [f'<div class="jp-comparison-grid" style="{grid_template}">']

# ==========================================================
# CARDS
# ==========================================================
for card in rows:

    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    card_html = []
    card_html.append('<div class="jp-card">')

    # CABEÇALHO FIXO
    card_html.append('<div class="jp-card-header">')
    card_html.append(f'<div class="jp-title">{job}</div>')
    card_html.append(f'<div class="jp-gg">GG {gg}</div>')
    card_html.append('<div class="jp-meta-block">')
    card_html.append(f"<div><b>Job Family:</b> {jf}</div>")
    card_html.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    card_html.append(f"<div><b>Career Path:</b> {cp}</div>")
    card_html.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    card_html.append("</div>")
    card_html.append("</div>")  # header

    # SEÇÕES
    for i, sec in enumerate(sections_order):
        content = str(card.get(sec, "")).strip()
        if not content or content.lower() == "nan":
            continue

        icon = icons[sec]
        alt = " alt" if i % 2 == 1 else ""

        card_html.append(f'<div class="jp-section{alt}">')
        card_html.append(
            f'<div class="jp-section-title"><img src="assets/icons/sig/{icon}"> {sec}</div>'
        )
        card_html.append(f'<div class="jp-text">{html.escape(content)}</div>')
        card_html.append("</div>")

    # FOOTER
    card_html.append('<div class="jp-footer">')
    card_html.append('<img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">')
    card_html.append("</div>")

    card_html.append("</div>")  # card wrapper

    html_parts.append("".join(card_html))

html_parts.append("</div>")  # grid

st.markdown("".join(html_parts), unsafe_allow_html=True)
