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
# HEADER PADRÃO SIG (PNG com antialiasing)
# ==========================================================
def header(icon_path, title):
    st.markdown(f"""
    <style>
        .page-header {{
            display: flex;
            align-items: center;
            gap: 18px;
        }}
        .page-header img {{
            width: 42px;
            height: 42px;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
        }}
        .page-header-title {{
            font-size: 36px;
            font-weight: 700;
            font-family: 'PPSIGFlow', sans-serif;
            margin: 0;
            padding: 0;
        }}
    </style>

    <div class="page-header">
        <img src="{icon_path}">
        <h1 class="page-header-title">{title}</h1>
    </div>
    <hr style="margin-top:6px; margin-bottom:20px;">
    """, unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS GLOBAL – FONTE + LAYOUT EXECUTIVO + SCROLL SYNC
# ==========================================================
st.markdown("""
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
    font-family: "PPSIGFlow", sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

/* Sidebar travada */
[data-testid="stSidebar"] {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
    overflow: hidden !important;
}

/* GRID principal */
.jp-grid {
    display: grid;
    gap: 26px;
}

/* CARD EXECUTIVO */
.jp-card {
    background: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    height: 650px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
}

/* HEADER FIXO 160px */
.jp-header {
    padding: 20px 22px 14px 22px;
    background: white;
    position: sticky;
    top: 0;
    z-index: 10;
    height: 160px;
    border-bottom: 1px solid #eee;
}

.jp-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 4px;
}
.jp-gg {
    font-weight: 700;
    color: #145efc;
    margin-bottom: 12px;
}

.jp-meta {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.88rem;
}

/* BODY ROLÁVEL – scroll sincronizado */
.jp-body {
    padding: 14px 22px;
    overflow-y: auto;
    height: calc(650px - 160px);
}

/* SEÇÕES */
.jp-section {
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid #f0f0f0;
}
.jp-section.alt {
    background: #fafafa;
    padding: 12px;
    border-radius: 8px;
}
.jp-section-title {
    font-weight: 700;
    font-size: 0.92rem;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.jp-text {
    white-space: pre-wrap;
    font-size: 0.9rem;
    line-height: 1.45;
}

/* PDF FOOTER */
.jp-footer {
    padding: 12px 15px;
    text-align: right;
}
.jp-footer img {
    width: 26px;
    cursor: pointer;
    opacity: 0.75;
}
.jp-footer img:hover {
    opacity: 1;
    transform: scale(1.1);
}

/************ SCROLL SYNC ************/
</style>

<script>
window.addEventListener("load", function() {
    const bodies = document.querySelectorAll(".jp-body");
    bodies.forEach(b => {
        b.addEventListener("scroll", () => {
            const pos = b.scrollTop;
            bodies.forEach(other => {
                if (b !== other) other.scrollTop = pos;
            });
        });
    });
});
</script>

""", unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================
@st.cache_data
def load_job_profile():
    file = Path("data") / "Job Profile.xlsx"
    if not file.exists():
        return pd.DataFrame()
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    return df

df = load_job_profile()
if df.empty:
    st.error("Arquivo Job Profile.xlsx não encontrado.")
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
    subs = sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()) if familia!="Selecione..." else []
    sub = st.selectbox("Sub Job Family", ["Selecione..."] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()) if sub!="Selecione..." else []
    trilha = st.selectbox("Career Path", ["Selecione..."] + paths)

filtered = df.copy()
if familia!="Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub!="Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha!="Selecione...":
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
    "Selecione até 3 perfis:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

perfils = [label_to_profile[l] for l in selecionados_labels]
rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in perfils]

# ==========================================================
# SEÇÕES (com emojis minimalistas)
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
# RENDERIZAÇÃO DOS CARDS
# ==========================================================
grid = f"grid-template-columns: repeat({len(rows)}, 1fr);"
st.markdown(f'<div class="jp-grid" style="{grid}">', unsafe_allow_html=True)

for card in rows:
    job = html.escape(str(card.get("Job Profile","")))
    gg = html.escape(str(card.get("Global Grade","")))
    jf = html.escape(str(card.get("Job Family","")))
    sf = html.escape(str(card.get("Sub Job Family","")))
    cp = html.escape(str(card.get("Career Path","")))
    fc = html.escape(str(card.get("Full Job Code","")))

    # CARD
    st.markdown('<div class="jp-card">', unsafe_allow_html=True)

    # HEADER FIXO
    st.markdown(f"""
    <div class="jp-header">
        <div class="jp-title">{job}</div>
        <div class="jp-gg">GG {gg}</div>

        <div class="jp-meta">
            <div><b>Job Family:</b> {jf}</div>
            <div><b>Sub Job Family:</b> {sf}</div>
            <div><b>Career Path:</b> {cp}</div>
            <div><b>Full Job Code:</b> {fc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # BODY ROLÁVEL
    st.markdown('<div class="jp-body">', unsafe_allow_html=True)

    for i, (title, colname) in enumerate(sections):
        content = str(card.get(colname,"")).strip()
        if not content or content.lower()=="nan":
            continue

        alt = " alt" if i % 2 else ""

        st.markdown(f"""
        <div class="jp-section{alt}">
            <div class="jp-section-title">{title}</div>
            <div class="jp-text">{html.escape(content)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # fecha body

    # FOOTER PDF
    st.markdown("""
    <div class="jp-footer">
        <img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # fecha card

st.markdown("</div>", unsafe_allow_html=True)  # fecha grid
