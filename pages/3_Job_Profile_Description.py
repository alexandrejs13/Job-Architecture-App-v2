import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ---------------------------------------------------------
# HEADER (PNG HD perfeito)
# ---------------------------------------------------------
def header_png(icon_path, title_text):
    st.markdown(
        f"""
        <style>
            .page-title-jp {{
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 12px;
                margin-top: 10px;
            }}
            .page-title-jp img {{
                width: 40px;
                height: 40px;
                object-fit: contain;
                object-position: center;
                image-rendering: -webkit-optimize-contrast;
                image-rendering: crisp-edges;
                display: block;
            }}
            .page-title-jp h1 {{
                margin: 0;
                padding: 0;
                font-size: 34px;
                font-weight: 800;
            }}
        </style>

        <div class="page-title-jp">
            <img src="{icon_path}">
            <h1>{title_text}</h1>
        </div>
        <hr style="margin-top:6px; margin-bottom:30px;">
        """,
        unsafe_allow_html=True,
    )


header_png("assets/icons/business_review_clipboard.png", "Job Profile Description")


# ---------------------------------------------------------
# GLOBAL CSS (puxa estilo SIG)
# ---------------------------------------------------------
st.markdown(
    """
<style>

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif;
    background: white !important;
}

/* área principal */
.block-container {
    max-width: 1500px !important;
    padding-top: 0rem;
}

/* GRID responsivo */
.jp-grid {
    display: grid;
    gap: 26px;
}
@media (min-width: 900px) and (max-width: 1299px) {
    .jp-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1300px) {
    .jp-grid { grid-template-columns: repeat(3, 1fr); }
}

/* CARD principal */
.jp-card {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 14px;
    padding: 26px 30px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}

/* TÍTULO DO CARD */
.jp-title {
    font-weight: 800;
    font-size: 1.35rem;
    margin-bottom: 2px;
}
.jp-gg {
    color: #145efc;
    font-weight: 800;
    margin-bottom: 16px;
}

/* META BLOCO */
.jp-meta {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 22px;
    font-size: 0.94rem;
}

/* SEÇÕES */
.jp-section {
    margin-bottom: 28px;
    padding: 18px;
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #eceae6;
}

.jp-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    font-size: 1.02rem;
    margin-bottom: 10px;
}

.jp-section-title svg {
    width: 22px;
    height: 22px;
}

.jp-text {
    white-space: pre-wrap;
    font-size: 0.94rem;
    line-height: 1.45;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# CARREGAR EXCEL
# ---------------------------------------------------------
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
    st.error("Não foi possível carregar Job Profile.xlsx")
    st.stop()

# ---------------------------------------------------------
# FILTROS
# ---------------------------------------------------------
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
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

# ---------------------------------------------------------
# PICKLIST
# ---------------------------------------------------------
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
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in selecionados]

# ---------------------------------------------------------
# SVG inline
# ---------------------------------------------------------
def svg(name):
    with open(f"assets/icons/sig/{name}", "r") as f:
        return f.read()

icons = {
    "Sub Job Family Description": svg("Hierarchy.svg"),
    "Job Profile Description": svg("Content_Book_Phone.svg"),
    "Career Band Description": svg("File_Clipboard_Text.svg"),
    "Role Description": svg("Shopping_Business_Target.svg"),
    "Grade Differentiator": svg("User_Add.svg"),
    "Qualifications": svg("Edit_Pencil.svg"),
    "Specific parameters / KPIs": svg("Graph_Bar.svg"),
    "Competencies 1": svg("Setting_Cog.svg"),
    "Competencies 2": svg("Setting_Cog.svg"),
    "Competencies 3": svg("Setting_Cog.svg"),
}

sections = list(icons.keys())

# ---------------------------------------------------------
# RENDERIZAÇÃO
# ---------------------------------------------------------
st.markdown("### ✨ Comparativo de Perfis Selecionados")

st.markdown('<div class="jp-grid">', unsafe_allow_html=True)

for card in rows:

    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    card_html = f"""
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

    for sec in sections:
        content = str(card.get(sec, "")).strip()
        
        if not content or content.lower() == "nan":
            content = "—"

        card_html += f"""
        <div class="jp-section">
            <div class="jp-section-title">{icons[sec]}<span>{sec}</span></div>
            <div class="jp-text">{html.escape(content)}</div>
        </div>
        """

    card_html += "</div>"

    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
