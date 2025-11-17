# ==========================================================
# Job Profile Description – Comparação de até 3 perfis (SIG)
# ==========================================================

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
def header(icon, title):
    col1, col2 = st.columns([0.07, 0.93])
    with col1:
        st.image(icon, width=54)
    with col2:
        st.markdown(
            f"<h1 style='margin:0; padding:0; font-size:36px; font-weight:700;'>{title}</h1>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")


# ----------------------------------------------------------
# CSS (SEM SCROLL, SEM STICKY, SEM ALTURA FIXA)
# ----------------------------------------------------------
st.markdown("""
<style>

@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-SemiBold.otf') format('opentype');
    font-weight:600;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight:700;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family:'PPSIGFlow', sans-serif !important;
    background:white !important;
}

/* GRID — 1, 2 ou 3 colunas */
.jp-grid {
    display:grid;
    gap:26px;
}
@media (min-width:900px) and (max-width:1299px){
    .jp-grid { grid-template-columns:repeat(2,1fr); }
}
@media (min-width:1300px){
    .jp-grid { grid-template-columns:repeat(3,1fr); }
}

/* CARD */
.jp-card {
    background:white;
    border:1px solid #e8e8e8;
    border-radius:14px;
    padding:26px;
    box-shadow:0 3px 10px rgba(0,0,0,0.06);
}

/* Título do cargo */
.jp-title {
    font-size:1.35rem;
    font-weight:700;
    margin-bottom:4px;
}

/* GG */
.jp-gg {
    font-weight:700;
    color:#145efc;
    margin-bottom:14px;
}

/* Meta */
.jp-meta {
    background:#f5f4f1;
    padding:12px;
    border-radius:10px;
    font-size:0.94rem;
    margin-bottom:20px;
}

/* Seções */
.jp-section {
    margin-bottom:26px;
}

.jp-section-title {
    display:flex;
    align-items:center;
    gap:10px;
    font-weight:700;
    font-size:1rem;
    margin-bottom:8px;
}

.jp-section-title img {
    width:22px;
    opacity:0.9;
}

.jp-text {
    white-space:pre-wrap;
    font-size:0.94rem;
    line-height:1.45;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# CARREGAR EXCEL
# ----------------------------------------------------------
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

# ----------------------------------------------------------
# FILTROS
# ----------------------------------------------------------
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


# ----------------------------------------------------------
# PICKLIST
# ----------------------------------------------------------
filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

# monta rows
selecionados = [label_to_profile[x] for x in selecionados_labels]
rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in selecionados]

# ----------------------------------------------------------
# ICONE correto por seção
# ----------------------------------------------------------
icons = {
    "Sub Job Family Description": "Hierarchy.svg",
    "Job Profile Description": "Content_Book_Phone.svg",
    "Career Band Description": "File_Clipboard_Text.svg",
    "Role Description": "Shopping_Business_Target.svg",
    "Grade Differentiator": "User_Add.svg",
    "Qualifications": "Edit_Pencil.svg",
    "Specific parameters / KPIs": "Graph_Bar.svg",
    "Competencies 1": "Setting_Cog.svg",
    "Competencies 2": "Setting_Cog.svg",
    "Competencies 3": "Setting_Cog.svg",
}

sections_order = list(icons.keys())


# ----------------------------------------------------------
# RENDER
# ----------------------------------------------------------
st.markdown("### ✨ Comparativo de Perfis Selecionados")
st.markdown('<div class="jp-grid">', unsafe_allow_html=True)

for card in rows:

    job = html.escape(str(card.get("Job Profile","")))
    gg = html.escape(str(card.get("Global Grade","")))
    jf = html.escape(str(card.get("Job Family","")))
    sf = html.escape(str(card.get("Sub Job Family","")))
    cp = html.escape(str(card.get("Career Path","")))
    fc = html.escape(str(card.get("Full Job Code","")))

    html_card = f"""
    <div class="jp-card">
        <div class="jp-title">{job}</div>
        <div class="jp-gg">GG {gg}</div>

        <div class="jp-meta">
            <div><b>Job Family:</b> {jf}</div>
            <div><b>Sub Job Family:</b> {sf}</div>
            <div><b>Career Path:</b> {cp}</div>
            <div><b>Full Job Code:</b> {fc}</div>
        </div>
    """

    for sec in sections_order:
        raw = str(card.get(sec,"")).strip()
        content = raw if raw and raw.lower()!="nan" else "—"
        icon = icons[sec]

        html_card += f"""
        <div class="jp-section">
            <div class="jp-section-title">
                <img src="assets/icons/sig/{icon}">
                {sec}
            </div>
            <div class="jp-text">{html.escape(content)}</div>
        </div>
        """

    html_card += "</div>"
    st.markdown(html_card, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
