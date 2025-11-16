# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — FINAL CLEAN VERSION

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

# ==========================================================
# PAGE SETUP
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")

# ==========================================================
# HEADER (PADRÃO DAS OUTRAS PÁGINAS)
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
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/globe_trade.png", "Job Maps")

# ==========================================================
# CSS FINAL — CLEAN, SIG COLORS, STICKY, MERGE
# ==========================================================
CSS = """
<style>

:root {
    --border: #d9d9d9;
    --gg-bg: #000000;         /* SIG Black */
    --family-bg: #4F5D75;     /* Steel Blue */
    --subfam-bg: #E9EDF2;     /* Light Gray */
}

/* MAP WRAPPER */
.map-wrapper {
    height: 76vh;
    overflow: auto;
    background: white;
    border: 1px solid var(--border);
    border-radius: 10px;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    font-size: 0.88rem;
    border-collapse: collapse;
}

/* FAMILY HEADER — sticky row 1 */
.header-family {
    background: var(--family-bg);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid white;
    height: 50px;
    position: sticky;
    top: 0;
    z-index: 20;
}

/* SUBFAMILY HEADER — sticky row 2 */
.header-subfamily {
    background: var(--subfam-bg);
    color: #222;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid var(--border);
    height: 45px;
    position: sticky;
    top: 50px;
    z-index: 19;
}

/* GG COLUMN HEADER */
.gg-header {
    width: 140px !important;
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    position: sticky;
    top: 0;
    left: 0;
    z-index: 30;
    border-right: 2px solid white;
}

/* GG CELLS */
.gg-cell {
    width: 140px !important;
    background: var(--gg-bg);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    border-bottom: 1px solid white;
    border-right: 2px solid white;
    position: sticky;
    left: 0;
    z-index: 25;
}

/* NORMAL CELLS */
.cell {
    border-bottom: 1px solid var(--border);
    border-right: 1px solid var(--border);
    padding: 6px;
    display: flex;
    align-items: center;        /* CENTRALIZADO VERTICAL */
    gap: 8px;
    flex-wrap: wrap;
}

/* JOB CARD FIXO */
.job-card {
    background: white;
    border: 1px solid var(--border);
    border-left-width: 4px !important;
    border-radius: 6px;
    width: 135px;
    height: 75px;
    padding: 6px 8px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.job-card b {
    font-size: 0.78rem;
    margin-bottom: 3px;
    color: #111;
}

.job-card span {
    font-size: 0.70rem;
    color: #333;
}

/* FULLSCREEN EXIT BUTTON */
#exit-fullscreen-btn {
    position: fixed;
    bottom: 26px;
    right: 26px;
    background: #111 !important;
    color: white !important;
    padding: 12px 28px;
    border-radius: 28px;
    border: none;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.35);
    font-size: 15px;
    font-weight: 700;
    z-index: 99999;
    cursor: pointer;
}
#exit-fullscreen-btn:hover {
    transform: scale(1.06);
}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Erro: Job Profile.xlsx não encontrado.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan','None',''], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

df = df[(df["Job Family"]!="") & (df["Job Profile"]!="") & (df["Global Grade"]!="")]

# ==========================================================
# SIG COLORS PER CAREER PATH
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "manage" in p or "executive" in p: return "#00493b"   # SIG Forest 3
    if "professional" in p: return "#73706d"                 # SIG Sand 4
    if "tech" in p or "support" in p: return "#a09b05"       # SIG Moss 3
    return "#145efc"                                         # SIG Sky

# ==========================================================
# FILTERS
# ==========================================================
colA, colB = st.columns(2)
fam_filter = colA.selectbox("Job Family", ["Todas"] + sorted(df["Job Family"].unique()))
path_filter = colB.selectbox("Career Path", ["Todas"] + sorted(df["Career Path"].unique()))

df_filtered = df.copy()
if fam_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Job Family"] == fam_filter]
if path_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Career Path"] == path_filter]

# ==========================================================
# GENERATE MAP (WITH MERGE + VERTICAL CENTER)
# ==========================================================
@st.cache_data(ttl=600)
def generate_map(df):
    families = sorted(df["Job Family"].unique())
    grades = sorted(df["Global Grade"].unique(), key=lambda x:int(x), reverse=True)

    # MAP columns (subfamilies)
    submap = {}
    col_i = 2
    fam_span = {}

    for fam in families:
        subs = sorted(df[df["Job Family"]==fam]["Sub Job Family"].unique())
        fam_span[fam] = len(subs)
        for sf in subs:
            submap[(fam, sf)] = col_i
            col_i += 1

    grouped = df.groupby(["Job Family","Sub Job Family","Global Grade"])
    cards = {k:v.to_dict("records") for k,v in grouped}

    html = []
    html.append("<div class='map-wrapper'><div class='jobmap-grid' "
                f"style='grid-template-columns:140px repeat({len(submap)}, 1fr);'>")

    # HEADER GG
    html.append("<div class='gg-header'>GG</div>")

    # FAMILY ROW
    colpos = 2
    for fam in families:
        span = fam_span[fam]
        html.append(f"<div class='header-family' style='grid-column:{colpos}/span{span};'>{fam}</div>")
        colpos += span

    # SUBFAMILY
    for (fam, sf), c in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{c};'>{sf}</div>")

    # ROWS
    row = 3
    for g in grades:
        # GG cell
        html.append(f"<div class='gg-cell' style='grid-row:{row};'>GG {g}</div>")

        for (fam,sf),c in submap.items():
            recs = cards.get((fam,sf,g), [])
            cell = ""

            for r in recs:
                color = get_path_color(r["Career Path"])
                cell += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{r['Job Profile']}</b>"
                    f"<span>{r['Career Path']} – GG {g}</span>"
                    "</div>"
                )

            html.append(f"<div class='cell' style='grid-column:{c};'>{cell}</div>")

        row += 1

    html.append("</div></div>")
    return "".join(html)

# ==========================================================
# RENDER MAP
# ==========================================================
st.markdown(generate_map(df_filtered), unsafe_allow_html=True)

# ==========================================================
# FULLSCREEN LOGIC
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

if not st.session_state.fs:
    if st.button("⛶ Tela Cheia"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:
    st.markdown("<script>document.body.requestFullscreen();</script>", unsafe_allow_html=True)

    # EXIT BUTTON
    st.markdown(
        "<button id='exit-fullscreen-btn' onclick='document.exitFullscreen(); window.parent.location.reload();'>"
        "❌ Sair</button>",
        unsafe_allow_html=True
    )

    components.html("""
    <script>
        document.addEventListener("keydown", (e)=>{
            if(e.key==="Escape"){
                window.parent.document.querySelector('#exit-fullscreen-btn').click();
            }
        });
    </script>
    """, height=0, width=0)
