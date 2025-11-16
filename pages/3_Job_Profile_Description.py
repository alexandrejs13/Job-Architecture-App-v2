##############################
# PAGE 3 – JOB PROFILE DESCRIPTION
# Full Executive Layout + PDF per card + Fullscreen
##############################

import streamlit as st
import pandas as pd
import base64
from utils.data_loader import load_excel_data
from utils.global_css import inject_global_css  # seu CSS unificado
import uuid

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER (MANTER PADRÃO DO NOVO APP)
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# CSS global
inject_global_css()

# ==========================================================
# LOAD DATA
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("❌ O arquivo Job Profile.xlsx não foi encontrado.")
    st.stop()

df = df.copy()
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# ==========================================================
# FILTERS
# ==========================================================
st.markdown(
    "<h3 style='margin-top:10px; font-weight:700;'>🔍 Explore Job Profiles</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

familias = sorted(df["Job Family"].unique())
with col1:
    fam = st.selectbox("Job Family:", ["Selecione..."] + familias)

subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique()) if fam != "Selecione..." else []
with col2:
    subfam = st.selectbox("Sub Job Family:", ["Selecione..."] + subs)

paths = sorted(df[df["Sub Job Family"] == subfam]["Career Path"].unique()) if subfam != "Selecione..." else []
with col3:
    trilha = st.selectbox("Career Path:", ["Selecione..."] + paths)

filtered = df.copy()
if fam != "Selecione...":
    filtered = filtered[filtered["Job Family"] == fam]
if subfam != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == subfam]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar perfis.")
    st.stop()

filtered["label"] = filtered.apply(
    lambda r: f"GG {r['Global Grade']} • {r['Job Profile']}", axis=1
)

selected_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(filtered["label"]),
    max_selections=3,
)

if not selected_labels:
    st.stop()

selected_profiles = filtered[filtered["label"].isin(selected_labels)]

# ==========================================================
# FULLSCREEN HANDLER
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

btn_col, _ = st.columns([0.13, 0.87])

if not st.session_state.fs:
    with btn_col:
        if st.button("Tela Cheia"):
            st.session_state.fs = True
            st.experimental_rerun()
else:
    # esconder sidebar via CSS
    hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display:none;}
        .block-container {padding-left:2rem !important;}
    </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

    with btn_col:
        if st.button("Sair"):
            st.session_state.fs = False
            st.experimental_rerun()

# ==========================================================
# CARD STYLES (HTML)
# ==========================================================
SECTION_ORDER = [
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
# RENDER PROFILE CARD
# ==========================================================
def build_profile_card(row):
    uid = str(uuid.uuid4()).replace("-", "")[:8]

    # PDF icon
    pdf_btn = f"""
        <div style='position:absolute; top:16px; right:16px;'>
            <a href='#' onclick="downloadPdf('{uid}')">
                <svg width="22" height="22" stroke='#145efc' fill='none' stroke-width='2' 
                     stroke-linecap='round' stroke-linejoin='round'>
                    <path d="M14 2H6a2 2 0 0 0-2 2v16l6-3 6 3V8"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
            </a>
        </div>
    """

    # content
    html = f"""
    <div class="jp-card" id="card-{uid}">
        {pdf_btn}

        <div class="jp-title">{row['Job Profile']}</div>
        <div class="jp-gg">GG {row['Global Grade']}</div>

        <div class="jp-meta-block">
            <div class="jp-meta-row"><b>Job Family:</b> {row['Job Family']}</div>
            <div class="jp-meta-row"><b>Sub Job Family:</b> {row['Sub Job Family']}</div>
            <div class="jp-meta-row"><b>Career Path:</b> {row['Career Path']}</div>
            <div class="jp-meta-row"><b>Full Job Code:</b> {row.get('Full Job Code','-')}</div>
        </div>

        <div class="jp-scroll">
    """

    for title, col in SECTION_ORDER:
        txt = row.get(col, "").strip()
        if len(txt) < 2 or txt.lower() == "nan":
            continue
        html += f"""
        <div class="jp-section">
            <div class="jp-section-title">{title}</div>
            <div class="jp-text">{txt}</div>
        </div>
        """

    html += "</div></div>"

    return html


# ==========================================================
# LAYOUT (1, 2 ou 3 COLUNAS)
# ==========================================================
num_cols = len(selected_profiles)
cols = st.columns(num_cols)

cards_html = []
for i, (_, row) in enumerate(selected_profiles.iterrows()):
    card_html = build_profile_card(row)
    cols[i].markdown(card_html, unsafe_allow_html=True)

# ==========================================================
# JS PARA PDF EXPORT
# ==========================================================
st.markdown("""
<script>
function downloadPdf(id){
    const card = document.getElementById("card-" + id);
    var opt = {
        margin:       0.5,
        filename:     'JobProfile-' + id + '.pdf',
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' }
    };
    html2pdf().from(card).set(opt).save();
}
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
""", unsafe_allow_html=True)
