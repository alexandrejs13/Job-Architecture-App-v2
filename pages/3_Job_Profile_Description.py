# ============================================================
# pages/3_Job_Profile_Description.py
# VERSÃO FINAL — LAYOUT EXECUTIVO SIG + ÍCONES CORPORATIVOS
# ============================================================

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ------------------------------------------------------------
# HEADER PADRÃO
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# CSS GLOBAL FINALIZADO
# ------------------------------------------------------------
css_path = Path("utils/global_css.py").resolve()
from utils.global_css import load_global_css
load_global_css()

# ------------------------------------------------------------
# CSS LOCAL DA PÁGINA (ÍCONES + SINCRONIZAÇÃO)
# ------------------------------------------------------------
st.markdown("""
<style>

.jp-card-wrapper {
    display: flex;
    flex-direction: column;
    height: 650px;
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid #e6e6e6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    padding: 0;
    position: relative;
    overflow: hidden;
}

.jp-card-header {
    padding: 18px 22px 14px 22px;
    background: #ffffff;
    border-bottom: 1px solid #eee;
    position: sticky;
    top: 0;
    z-index: 10;
}

.jp-title {
    font-family: 'PPSIGFlow-SemiBold', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 2px;
}

.jp-gg {
    font-size: 1rem;
    font-weight: 800;
    color: #145efc;
    margin-bottom: 6px;
}

.jp-meta {
    font-size: 0.9rem;
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
}

.jp-body {
    padding: 18px 22px;
    overflow-y: auto;
}

.jp-body::-webkit-scrollbar {
    width: 8px;
}
.jp-body::-webkit-scrollbar-thumb {
    background: #c8c8c8;
    border-radius: 10px;
}

.jp-section {
    background: #fafafa;
    padding: 14px 14px;
    border-radius: 12px;
    margin-bottom: 14px;
}
.jp-section.alt {
    background: #f0f4ff;
}

.jp-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 8px;
}

.jp-section-title img {
    width: 22px;
    opacity: 0.9;
}

.jp-text {
    font-size: 0.9rem;
    color: #333;
    line-height: 1.45;
    white-space: pre-wrap;
}

.jp-footer {
    padding: 20px;
    text-align: right;
}

.jp-footer img {
    width: 28px;
    cursor: pointer;
    opacity: 0.8;
    transition: 0.2s;
}
.jp-footer img:hover {
    opacity: 1;
    transform: scale(1.08);
}

/* GRID CONTROLADO */
.jp-grid {
    display: grid;
    gap: 22px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
@st.cache_data
def load_job_profile():
    path = Path("data/Job Profile.xlsx")
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()
    df["Global Grade"] = (
        df["Global Grade"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
    )
    return df

df = load_job_profile()
if df.empty:
    st.error("❌ 'Job Profile.xlsx' não encontrado")
    st.stop()

# Garantir colunas
columns_needed = [
    "Job Family", "Sub Job Family", "Career Path",
    "Job Profile", "Global Grade", "Full Job Code",
    "Sub Job Family Description", "Job Profile Description",
    "Career Band Description", "Role Description",
    "Grade Differentiator", "Qualifications",
    "Specific parameters / KPIs", "Competencies 1",
    "Competencies 2", "Competencies 3",
]
for c in columns_needed:
    if c not in df.columns:
        df[c] = ""

# ------------------------------------------------------------
# FILTROS
# ------------------------------------------------------------
st.markdown("### 🔍 Explorador de Perfis")

familias = sorted(df["Job Family"].unique())

col1, col2, col3 = st.columns(3)
with col1:
    fam = st.selectbox("Job Family:", ["Selecione..."] + familias)
with col2:
    subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique()) if fam!="Selecione..." else []
    sub = st.selectbox("Sub Job Family:", ["Selecione..."] + subs)
with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].unique()) if sub!="Selecione..." else []
    trilha = st.selectbox("Career Path:", ["Selecione..."] + paths)

filtered = df.copy()
if fam!="Selecione...": filtered = filtered[filtered["Job Family"] == fam]
if sub!="Selecione...": filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha!="Selecione...": filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Selecione filtros válidos.")
    st.stop()

# ------------------------------------------------------------
# PICKLIST
# ------------------------------------------------------------
filtered["label"] = filtered.apply(
    lambda r: f'GG {r["Global Grade"]} • {r["Job Profile"]}', axis=1
)
map_label = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(map_label.keys()),
    max_selections=3,
)
if not selecionados:
    st.stop()

lista = [map_label[l] for l in selecionados]
cards = [filtered[filtered["Job Profile"] == x].iloc[0].to_dict() for x in lista]

# ------------------------------------------------------------
# ICONES CORPORATIVOS (22px)
# ------------------------------------------------------------
ICONES = {
    "Sub Job Family Description": "assets/icons/sig/Hierarchy.svg",
    "Job Profile Description": "assets/icons/sig/File_Clipboard_Text.svg",
    "Career Band Description": "assets/icons/sig/Hierarchy.svg",
    "Role Description": "assets/icons/sig/Shopping_Business_Target.svg",
    "Grade Differentiator": "assets/icons/sig/Edit_Pencil.svg",
    "Qualifications": "assets/icons/sig/Content_Book_Phone.svg",
    "Specific parameters / KPIs": "assets/icons/sig/Graph_Bar.svg",
    "Competencies 1": "assets/icons/sig/Setting_Cog.svg",
    "Competencies 2": "assets/icons/sig/Setting_Cog.svg",
    "Competencies 3": "assets/icons/sig/Setting_Cog.svg",
}

sections = [
    "Sub Job Family Description",
    "Job Profile Description",
    "Career Band Description",
    "Role Description",
    "Grade Differentiator",
    "Qualifications",
    "Specific parameters / KPIs",
    "Competencies 1",
    "Competencies 2",
    "Competencies 3",
]

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
cols = len(cards)
grid = f"grid-template-columns: repeat({cols}, 1fr);"
st.markdown("---")
st.markdown(f'<div class="jp-grid" style="{grid}">', unsafe_allow_html=True)

# ------------------------------------------------------------
# RENDER CARDS
# ------------------------------------------------------------
for card in cards:
    html_card = []
    html_card.append('<div class="jp-card-wrapper">')

    # HEADER
    html_card.append('<div class="jp-card-header">')
    html_card.append(f'<div class="jp-title">{html.escape(card["Job Profile"])}</div>')
    html_card.append(f'<div class="jp-gg">GG {html.escape(card["Global Grade"])}</div>')

    html_card.append('<div class="jp-meta">')
    html_card.append(f"<div><b>Job Family:</b> {html.escape(card['Job Family'])}</div>")
    html_card.append(f"<div><b>Sub Job Family:</b> {html.escape(card['Sub Job Family'])}</div>")
    html_card.append(f"<div><b>Career Path:</b> {html.escape(card['Career Path'])}</div>")
    html_card.append(f"<div><b>Full Job Code:</b> {html.escape(card['Full Job Code'])}</div>")
    html_card.append("</div></div>")

    # BODY
    html_card.append('<div class="jp-body">')

    for i, section in enumerate(sections):
        content = card.get(section, "").strip()
        if not content: 
            continue

        classe = "jp-section alt" if i % 2 else "jp-section"
        icon = ICONES[section]

        html_card.append(f'''
            <div class="{classe}">
                <div class="jp-section-title">
                    <img src="{icon}">
                    {section}
                </div>
                <div class="jp-text">{html.escape(content)}</div>
            </div>
        ''')

    html_card.append("</div>")  # body

    # FOOTER + PDF
    html_card.append('''
        <div class="jp-footer">
            <img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">
        </div>
    ''')

    html_card.append("</div>")  # wrapper
    st.markdown("".join(html_card), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
