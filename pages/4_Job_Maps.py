# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — versão final e consolidada

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data


# ==========================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")


# ==========================================================
# 2. HEADER PADRÃO SIG
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"<h1 style='margin:0; padding:0; font-size:36px; font-weight:700;'>{title}</h1>",
            unsafe_allow_html=True,
        )
    st.markdown(
        "<hr style='margin-top:5px; margin-bottom:15px;'>",
        unsafe_allow_html=True
    )

header("assets/icons/globe_trade.png", "Job Maps")


# ==========================================================
# 3. CSS VISUAL CLEAN + STICKY + CORES SIG
# ==========================================================
st.markdown("""
<style>

:root {
    --border: #d9d9d9;
    --head-1: #4F5D75;     /* família */
    --head-2: #e9edf2;     /* subfamília */
    --gg-bg: #1e1e1e;
    --white: #ffffff;

    /* CORES SIG PARA CARREIRAS */
    --c-mgmt: #00493b;     /* Management */
    --c-prof: #73706d;     /* Professional */
    --c-tech: #a09b05;     /* Technical */
    --c-proj: #145efc;     /* Project / default */
}

/* WRAPPER */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: white;
}

/* GRID BASE */
.jobmap-grid {
    display: grid;
    width: max-content;
    font-size: 0.86rem;
}

/* FAMÍLIA (STICKY) */
.header-family {
    background: var(--head-1);
    color: white;
    font-weight: 700;
    text-align: center;
    border-right: 1px solid white;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 0;
    z-index: 30;
}

/* SUBFAMÍLIA (STICKY) */
.header-subfamily {
    background: var(--head-2);
    color: #222;
    font-weight: 600;
    text-align: center;
    border-right: 1px solid var(--border);
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 50px;
    z-index: 29;
}

/* GG HEADER (COLUNA FIXA) */
.gg-header {
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    position: sticky;
    top: 0;
    left: 0;
    z-index: 40;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 2px solid white;
}

/* GG CELLS (COLUNA FIXA) */
.gg-cell {
    background: var(--gg-bg);
    color: white;
    font-weight: 600;
    height: max-content;
    position: sticky;
    left: 0;
    z-index: 25;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 2px solid white;
    padding: 4px 10px;
}

/* CELLS DO MAPA */
.cell {
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 8px;
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
}

/* CARDS (TAMANHO FIXO) */
.job-card {
    width: 135px;
    height: 75px;
    background: white;
    border: 1px solid var(--border);
    border-left-width: 5px !important;
    border-radius: 6px;
    padding: 6px 8px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.job-card b {
    font-size: 0.76rem;
    margin-bottom: 3px;
}

.job-card span {
    font-size: 0.7rem;
    color: #555;
}

/* FULLSCREEN */
#exit-fullscreen-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 999999;
    background: #111 !important;
    color: white !important;
    padding: 12px 26px;
    border-radius: 30px;
    font-weight: 700;
    border: none;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35);
}
#exit-fullscreen-btn:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 4. LOAD DATA
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Erro: Não foi possível carregar o Job Profile.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(
    ["nan", "None", "<NA>", ""], "-"
)
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)


# ==========================================================
# 5. CORES SIG POR CARREIRA
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "manage" in p or "executive" in p:
        return "var(--c-mgmt)"
    if "professional" in p:
        return "var(--c-prof)"
    if "tech" in p or "support" in p:
        return "var(--c-tech)"
    return "var(--c-proj)"


# ==========================================================
# 6. FILTROS
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
# 7. GERAÇÃO DO MAPA
# ==========================================================
@st.cache_data(ttl=600)
def generate_map(df):

    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x), reverse=True)
    families = sorted(df["Job Family"].unique())

    # MAPA DE SUBFAMÍLIAS → COLUNAS
    submap = {}
    col_i = 2
    fam_spans = {}

    for f in families:
        subs = sorted(df[df["Job Family"] == f]["Sub Job Family"].unique())
        fam_spans[f] = len(subs)
        for sf in subs:
            submap[(f, sf)] = col_i
            col_i += 1

    # AGRUPA CARDS
    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # CONSTRÓI O HTML
    num_sub_cols = len(submap)
    grid_style = (
        f"grid-template-columns: 120px repeat({num_sub_cols}, max-content);"
        "grid-auto-rows: max-content;"
    )

    html = [f"<div class='map-wrapper'><div class='jobmap-grid' style='{grid_style}'>"]

    # HEADER COLUNA GG
    html.append("<div class='gg-header' style='grid-row:1 / span 2; grid-column:1;'>GG</div>")

    # FAMÍLIAS
    col = 2
    for f in families:
        span = fam_spans[f]
        html.append(
            f"<div class='header-family' style='grid-row:1; grid-column:{col} / span {span};'>{f}</div>"
        )
        col += span

    # SUBFAMÍLIAS
    for (f, sf), idx in submap.items():
        html.append(
            f"<div class='header-subfamily' style='grid-row:2; grid-column:{idx};'>{sf}</div>"
        )

    # LINHAS (CÉLULAS)
    row = 3
    for g in grades:

        html.append(
            f"<div class='gg-cell' style='grid-row:{row}; grid-column:1;'>GG {g}</div>"
        )

        for (f, sf), idx in submap.items():

            recs = cards.get((f, sf, g), [])
            cell_html = ""

            for rc in recs:
                color = get_path_color(rc["Career Path"])
                cell_html += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rc['Job Profile']}</b>"
                    f"<span>{rc['Career Path']} – GG {g}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-row:{row}; grid-column:{idx};'>{cell_html}</div>"
            )

        row += 1

    html.append("</div></div>")
    return "".join(html)


# ==========================================================
# 8. RENDERIZAÇÃO DO MAPA
# ==========================================================
st.markdown(generate_map(df_flt), unsafe_allow_html=True)


# ==========================================================
# 9. FULLSCREEN “APPLE-STYLE”
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

if not st.session_state.fs:
    if st.button("⛶ Tela Cheia"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:

    # ESC PARA SAIR
    components.html("""
        <script>
        document.addEventListener('keydown', (e)=>{
            if(e.key==="Escape"){
                window.parent.document.querySelector('#exit-fullscreen-btn').click();
            }
        });
        </script>
    """, height=0)

    st.markdown("""
        <button id="exit-fullscreen-btn"
                onclick="window.parent.location.reload();">❌ Sair</button>
    """, unsafe_allow_html=True)
