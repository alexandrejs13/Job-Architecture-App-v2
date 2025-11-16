# pages/4_Job_Maps.py
# VERSÃO FINAL — Botão 100px alinhado ao GG, fullscreen perfeito, layout intacto.

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")

# ==========================================================
# HEADER
# ==========================================================
def header(icon_path: str, title: str):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"<h1 style='margin:0; padding:0; font-size:36px; font-weight:700;'>{title}</h1>",
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/globe_trade.png", "Job Maps")

# ==========================================================
# CSS FINAL
# ==========================================================
css = """
<style>

:root {
    --border: #d9d9d9;
    --gg-bg: #000; 
    --family-bg: #4F5D75; 
    --subfamily-bg: #E9EDF2;
    --sig-blue: #145efc;
}

/* FULLSCREEN */
.fullscreen-container {
    padding: 1.5rem !important;
}

/* WRAPPER */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-radius: 10px;
    border: .5px solid var(--border);
    background: white;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    font-size: .88rem;
}

/* COLUNA GG — 100px */
.gg-header {
    width: 100px !important;
    min-width: 100px !important;
    max-width: 100px !important;
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    display:flex;
    align-items:center;
    justify-content:center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 30;
}

.gg-cell {
    width: 100px !important;
    min-width: 100px !important;
    max-width: 100px !important;
    background: var(--gg-bg);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    position: sticky;
    left:0;
    z-index:25;
}

/* FAMÍLIA */
.header-family {
    height:55px !important;
    background: var(--family-bg);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    position:sticky;
    top:0;
    border-right:1px solid white;
}

/* SUBFAMÍLIA */
.header-subfamily {
    min-height:44px !important;
    max-height:65px !important;
    background: var(--subfamily-bg);
    text-align:center;
    display:flex;
    align-items:center;
    justify-content:center;
    position:sticky;
    top:55px;
    left:100px !important;
    border-right:1px solid var(--border);
}

/* CELLS */
.cell {
    padding:10px;
    border-right:1px solid var(--border);
    border-bottom:1px solid var(--border);
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    align-items:center;
}

/* CARD 100px */
.job-card {
    width:180px;
    min-height:100px;
    padding:10px;
    background:white;
    border:1px solid var(--border);
    border-left-width:4px !important;
    border-radius:6px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    gap:4px;
    box-shadow:0 1px 3px rgba(0,0,0,0.06);
}

.job-card span {
    font-size:.74rem;
    color: var(--sig-blue);
    line-height:1.1;
}

/* BOTÕES — 100px ALINHADO AO GG */
.gg-button-wrapper {
    width:100px !important;
    margin-top:18px;
    margin-bottom:18px;
}

.full-btn {
    width:100px !important;
    background:var(--sig-blue) !important;
    color:white !important;
    border:none !important;
    border-radius:26px !important;
    padding:10px 0 !important;
    font-weight:700 !important;
    text-align:center;
}
.full-btn:hover {
    background:#0d4ccc !important;
}

</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ==========================================================
# DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo Job Profile não encontrado.")
    st.stop()

df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan','None','<NA>',''], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True)

# ==========================================================
# Cores SIG
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "executive" in p or "manage" in p: return "#00493b"
    if "professional" in p: return "#73706d"
    if "tech" in p or "support" in p: return "#a09b05"
    return "#145efc"

# ==========================================================
# Ordem Career Path
# ==========================================================
def sort_key(rec):
    p = rec["Career Path"].lower()
    if "executive" in p or "manage" in p: return 1
    if "professional" in p: return 2
    if "tech" in p or "support" in p: return 3
    return 4

# ==========================================================
# FILTROS
# ==========================================================
colA, colB = st.columns(2)
fam_filter = colA.selectbox("Job Family", ["Todas"] + sorted(df["Job Family"].unique()))
path_filter = colB.selectbox("Career Path", ["Todas"] + sorted(df["Career Path"].unique()))

df_flt = df.copy()
if fam_filter != "Todas":
    df_flt = df_flt[df_flt["Job Family"] == fam_filter]
if path_filter != "Todas":
    df_flt = df_flt[df_flt["Career Path"] == path_filter]

# ==========================================================
# GERA MAPA
# ==========================================================
@st.cache_data(ttl=600)
def generate_map(df):

    fam_max = (
        df.groupby("Job Family")["Global Grade"]
        .apply(lambda x: max(int(g) for g in x))
        .sort_values(ascending=False)
    )
    families_order = fam_max.index.tolist()

    submap_ordered = {}
    for fam in families_order:
        tmp = (
            df[df["Job Family"] == fam]
            .groupby("Sub Job Family")["Global Grade"]
            .apply(lambda x: max(int(g) for g in x))
            .sort_values(ascending=False)
        )
        submap_ordered[fam] = tmp.index.tolist()

    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x), reverse=True)

    submap = {}
    col_index = 2
    for fam in families_order:
        for sf in submap_ordered[fam]:
            submap[(fam, sf)] = col_index
            col_index += 1

    grouped = df.groupby(["Job Family","Sub Job Family","Global Grade"])
    cards = {k: v.to_dict("records") for k,v in grouped}

    html=[]
    html.append("<div class='map-wrapper'><div class='jobmap-grid'>")

    html.append("<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    col = 2
    for fam in families_order:
        subs = submap_ordered[fam]
        span=len(subs)
        html.append(f"<div class='header-family' style='grid-column:{col} / span {span};'>{fam}</div>")
        col += span

    for (fam,sub),c in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{c};'>{sub}</div>")

    row = 3
    for g in grades:
        html.append(f"<div class='gg-cell' style='grid-row:{row};'>GG {g}</div>")
        for (fam,sub),c_idx in submap.items():
            recs = cards.get((fam,sub,g), [])
            recs_sorted = sorted(recs, key=sort_key)

            cell=""
            for r in recs_sorted:
                color = get_path_color(r["Career Path"])
                cell += f"""
                <div class='job-card' style='border-left-color:{color};'>
                    <b>{r['Job Profile']}</b>
                    <span>{r['Career Path']} – GG {g}</span>
                </div>
                """

            html.append(f"<div class='cell' style='grid-column:{c_idx}; grid-row:{row};'>{cell}</div>")
        row+=1

    html.append("</div></div>")
    return "".join(html)

content = generate_map(df_flt)

# ==========================================================
# FULLSCREEN
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

# BOTÃO ABAIXO DA COLUNA GG
st.markdown("<div class='gg-button-wrapper'>", unsafe_allow_html=True)

if not st.session_state.fs:
    if st.button("Tela Cheia", key="enter_full", use_container_width=True):
        st.session_state.fs = True
        st.rerun()
else:
    if st.button("Sair", key="exit_full", use_container_width=True):
        st.session_state.fs = False
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# CONTEÚDO
if st.session_state.fs:
    st.markdown("<div class='fullscreen-container'>", unsafe_allow_html=True)
    st.markdown(content, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown(content, unsafe_allow_html=True)
