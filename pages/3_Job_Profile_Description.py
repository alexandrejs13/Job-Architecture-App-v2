import streamlit as st
import pandas as pd
import html
from pathlib import Path

# --------------------------------------------
# PAGE CONFIG
# --------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")


# --------------------------------------------
# HEADER
# --------------------------------------------
def header_png(icon_path, title_text):
    st.markdown(
        f"""
        <style>
            .page-title {{
                display:flex;
                align-items:center;
                gap:16px;
                margin-bottom:10px;
            }}
            .page-title img {{
                width:42px;
                height:42px;
                image-rendering:crisp-edges;
            }}
            .page-title h1 {{
                margin:0;
                font-size:36px;
                font-weight:800;
            }}
        </style>

        <div class="page-title">
            <img src="{icon_path}">
            <h1>{title_text}</h1>
        </div>
        <hr style="margin-top:12px;">
        """,
        unsafe_allow_html=True,
    )

header_png("assets/icons/business_review_clipboard.png", "Job Profile Description")


# --------------------------------------------
# CSS FIX EXTRA (GRID 3 COL + CARDS)
# --------------------------------------------
st.markdown(
    """
<style>

.jp-grid {
    display: grid;
    gap: 24px;
    width: 100%;
}

@media (min-width: 1200px) {
    .jp-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 800px) and (max-width:1199px) {
    .jp-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 799px) {
    .jp-grid { grid-template-columns: 1fr; }
}

.jp-card {
    background: #faf9f7;
    border: 1px solid #e6e2db;
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
}

.jp-header {
    padding: 22px;
    background: white;
    border-bottom: 1px solid #e6dfd6;
}

.jp-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin: 0;
}

.jp-gg {
    margin-top: 4px;
    font-size: 1.05rem;
    color: #145efc;
    font-weight: 700;
}

.jp-meta {
    background: #f2efeb;
    padding: 18px;
    margin: 0 22px 22px 22px;
    border-radius: 12px;
    border: 1px solid #e3ddd6;
}

.jp-section {
    padding: 20px 22px;
    border-left: 5px solid #145efc33;
    margin: 14px 0;
    background: white;
    border-radius: 10px;
}

.jp-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    margin-bottom: 8px;
}

.jp-section-title svg {
    width: 22px;
    height: 22px;
}

.jp-text {
    white-space: pre-wrap;
    line-height: 1.42;
    font-size: 0.92rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------
# LOAD EXCEL
# --------------------------------------------
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


# --------------------------------------------
# FILTERS
# --------------------------------------------
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


# --------------------------------------------
# PICKLIST
# --------------------------------------------
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


# --------------------------------------------
# LOAD SVG ICONS
# --------------------------------------------
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


# --------------------------------------------
# RENDER
# --------------------------------------------
st.markdown("### ✨ Comparativo de Perfis Selecionados")

st.markdown('<div class="jp-grid">', unsafe_allow_html=True)

for card in rows:

    # header
    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    card_html = f"""
    <div class="jp-card">
        <div class="jp-header">
            <div class="jp-title">{job}</div>
            <div class="jp-gg">GG {gg}</div>
        </div>

        <div class="jp-meta">
            <div><b>Job Family:</b> {jf}</div>
            <div><b>Sub Job Family:</b> {sf}</div>
            <div><b>Career Path:</b> {cp}</div>
            <div><b>Full Job Code:</b> {fc}</div>
        </div>
    """

    # sections
    for sec in sections:
        content = card.get(sec, "")
        if content is None or str(content).lower() == "nan" or str(content).strip() == "":
            content = "—"

        svg_icon = icons[sec]

        card_html += f"""
        <div class="jp-section">
            <div class="jp-section-title">
                {svg_icon}
                <span>{sec}</span>
            </div>
            <div class="jp-text">{html.escape(str(content))}</div>
        </div>
        """

    card_html += "</div>"

    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
