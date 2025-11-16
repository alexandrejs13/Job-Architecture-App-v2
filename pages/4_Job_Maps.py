# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — versão completa, moderna, funcional

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path

from utils.data_loader import load_excel_data
from utils.ui import setup_sidebar
from utils.ui_components import lock_sidebar


# ==========================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Job Map",
    page_icon="🗺️",
    layout="wide"
)

setup_sidebar()
lock_sidebar()


# ==========================================================
# 2. CSS NOVO — CLEAN, MODERNO, RESPONSIVO
# ==========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>

:root {
    --blue: #145efc;
    --gray-line: #e5e5e5;
    --dark-gray: #2f2f2f;
    --subtle-bg: #fafafa;
}

/* HEADER NOVO */
.page-header {
    background-color: var(--blue);
    color: white;
    padding: 22px 36px;
    font-size: 1.35rem;
    font-weight: 750;
    border-radius: 12px;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}
.page-header img { width: 46px; height: 46px; }

/* MAP WRAPPER */
.map-wrapper {
    height: 74vh;
    overflow: auto;
    background: white;
    border-radius: 10px;
    border: 2px solid var(--gray-line);
    position: relative;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    background: white;
    grid-auto-rows: 115px;
    font-size: 0.86rem;
}

/* CÉLULAS */
.cell {
    background: white;
    border-right: 1px solid var(--gray-line);
    border-bottom: 1px solid var(--gray-line);
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

/* GG HEADER FIXO */
.gg-header {
    background: var(--dark-gray);
    color: white;
    font-weight: 800;
    display: flex;
    justify-content: center;
    align-items: center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 30;
    border-right: 2px solid white;
    border-bottom: 1px solid var(--gray-line);
}

/* COLUNA GG FIXA */
.gg-cell {
    background: var(--dark-gray);
    color: white;
    font-weight: 700;
    position: sticky;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 25;
    border-right: 2px solid white;
}

/* HEADER FAMÍLIAS FIXO */
.header-family {
    background: #4F5D75;
    color: white;
    font-weight: 700;
    padding: 5px;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 20;
    border-right: 1px solid white;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* HEADER SUBFAMÍLIAS FIXO */
.header-subfamily {
    background: #E9EDF2;
    color: #222;
    font-weight: 600;
    padding: 5px;
    text-align: center;
    position: sticky;
    top: 50px;
    height: 45px;
    z-index: 19;
    border-right: 1px solid var(--gray-line);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* CARDS CLEAN */
.job-card {
    background: white;
    border: 1px solid var(--gray-line);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 5px 7px;
    width: 135px;
    height: 75px;
    font-size: 0.75rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.job-card b {
    font-size: 0.76rem;
    margin-bottom: 3px;
}

/* FULLSCREEN */
.fullscreen-wrapper {
    position: fixed !important;
    top: 0; left: 0;
    height: 100vh !important;
    width: 100vw !important;
    background: white;
    z-index: 9999 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* BOTÃO PRETO FOSCO */
#exit-fs button {
    background: #111 !important;
    color: white !important;
    border-radius: 40px !important;
    padding: 12px 30px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35) !important;
}
#exit-fs button:hover {
    background: #000 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. HEADER DA PÁGINA
# ==========================================================
st.markdown("""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/globe%20trade.png">
  Mapeamento de Cargos (Job Map)
</div>
""", unsafe_allow_html=True)


# ==========================================================
# 4. CARREGAMENTO DOS DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Erro: Não foi possível carregar Job Profile.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].replace(['nan', 'None', '<NA>', ''], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)


# ==========================================================
# 5. CORES DISCRETAS DO CARD
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "manage" in p or "executive" in p: return "#4F5D75"
    if "professional" in p: return "#2F2F2F"
    if "tech" in p: return "#7C7C7C"
    return "#5F6C7A"


# ==========================================================
# 6. FILTROS
# ==========================================================
colA, colB = st.columns(2)
fam = colA.selectbox("Job Family", ["Todas"] + sorted(df["Job Family"].unique()))
path = colB.selectbox("Career Path", ["Todas"] + sorted(df["Career Path"].unique()))

df_filtered = df.copy()
if fam != "Todas": df_filtered = df_filtered[df_filtered["Job Family"] == fam]
if path != "Todas": df_filtered = df_filtered[df_filtered["Career Path"] == path]


# ==========================================================
# 7. MAPA — MERGE VERTICAL + STICKY
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df):

    families = sorted(df["Job Family"].unique())
    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x), reverse=True)

    # MAPA DE COLUNAS
    submap = {}
    col_i = 2
    fam_span = {}

    for f in families:
        subs = sorted(df[df["Job Family"] == f]["Sub Job Family"].unique())
        fam_span[f] = len(subs)
        for sf in subs:
            submap[(f, sf)] = col_i
            col_i += 1

    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # MERGE VERTICAL
    content = {}
    span = {}
    skip = set()

    for g in grades:
        for (f, sf), idx in submap.items():
            rec = cards.get((f, sf, g), [])
            content[(g, idx)] = "|".join(sorted(r["Job Profile"] for r in rec)) if rec else None

    for (f, sf), idx in submap.items():
        for i, g in enumerate(grades):
            if (g, idx) in skip: continue

            current = content[(g, idx)]
            if current is None:
                span[(g, idx)] = 1
                continue

            s = 1
            for g2 in grades[i+1:]:
                if content[(g2, idx)] == current:
                    s += 1
                    skip.add((g2, idx))
                else:
                    break
            span[(g, idx)] = s

    # HTML
    html = ["<div class='map-wrapper'><div class='jobmap-grid' style='grid-template-columns:160px repeat(" + str(len(submap)) + ", 200px);'>"]

    # GG HEADER
    html.append("<div class='gg-header'>GG</div>")

    # FAMÍLIA
    col = 2
    for f in families:
        html.append(f"<div class='header-family' style='grid-column:{col} / span {fam_span[f]};'>{f}</div>")
        col += fam_span[f]

    # SUBFAMÍLIA
    for (f, sf), idx in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{idx};'>{sf}</div>")

    # LINHAS
    r = 3
    for g in grades:

        html.append(f"<div class='gg-cell' style='grid-row:{r};'>GG {g}</div>")

        for (f, sf), idx in submap.items():

            if (g, idx) in skip:
                continue

            sp = span.get((g, idx), 1)
            rspan = f"grid-row:{r} / span {sp};"

            recs = cards.get((f, sf, g), [])
            cell = ""

            for rc in recs:
                color = get_path_color(rc["Career Path"])
                cell += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rc['Job Profile']}</b>"
                    f"<span>{rc['Career Path']}</span>"
                    "</div>"
                )

            html.append(f"<div class='cell' style='grid-column:{idx}; {rspan}'>{cell}</div>")

        r += 1

    html.append("</div></div>")
    return "".join(html)


# ==========================================================
# 8. BOTÃO FULLSCREEN + MAPA FINAL
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

colFS = st.columns([6,1])[1]
if not st.session_state.fs:
    if colFS.button("⛶ Tela Cheia"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:
    st.markdown("<div class='fullscreen-wrapper'>", unsafe_allow_html=True)

    # BOTÃO SAIR
    st.markdown("<div id='exit-fs'>", unsafe_allow_html=True)
    if st.button("Sair"):
        st.session_state.fs = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ESC para sair
    components.html("""
        <script>
        document.addEventListener('keydown', (e)=>{
            if(e.key==='Escape'){
                const btn = window.parent.document.querySelector('#exit-fs button');
                if(btn){ btn.click(); }
            }
        });
        </script>
    """, height=0, width=0)


# ==========================================================
# 9. RENDERIZAÇÃO DO MAPA
# ==========================================================
st.markdown(generate_map_html(df_filtered), unsafe_allow_html=True)
