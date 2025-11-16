# pages/4_Job_Maps.py
# Layout Final Ajustado – Borda branca entre GG Header e GG21

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")

# ==========================================================
# HEADER CLEAN
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
# CSS — Layout Perfeito + Borda branca GG fix
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

/* WRAPPER */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-radius: 10px;
    border: 0.5px solid var(--border);
    background: white;
}

/* GRID BASE */
.jobmap-grid {
    display: grid;
    width: max-content;
    font-size: 0.88rem;
}

/* FAMÍLIA */
.header-family {
    background: var(--family-bg);
    color: white;
    height: 55px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    position: sticky;
    top: 0;
    z-index: 10;
    border-right: 1px solid white;
    padding: 0px 6px;
    text-align:center;
}

/* SUBFAMÍLIA */
.header-subfamily {
    background: var(--subfamily-bg);
    color: #222;
    min-height: 44px !important;
    max-height: 65px !important;
    padding: 4px 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 55px;
    z-index: 9;
    border-right: 1px solid var(--border);
    text-align: center;
    line-height: 1.15;
    white-space: normal;
}

/* GG HEADER – agora com borda branca inferior */
.gg-header {
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    width: 140px !important;
    display: flex;
    justify-content: center;
    align-items: center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 30;
    border-bottom: 1px solid white !important;
}

/* GG CELLS */
.gg-cell {
    background: var(--gg-bg);
    color: white;
    width: 140px !important;
    display: flex;
    justify-content: center;
    align-items: center;
    position: sticky;
    left: 0;
    z-index: 25;
    border-bottom: 1px solid white;
}

/* CELLS */
.cell {
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 6px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}

/* CARDS */
.job-card {
    background: white;
    border: 1px solid var(--border);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 6px 8px;
    width: 135px;
    height: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.job-card b {
    font-size: 0.78rem;
    margin-bottom: 3px;
}

.job-card span {
    font-size: 0.70rem;
    color: #555;
}

/* FULLSCREEN BUTTONS – SIG BLUE */
.full-btn {
    background: var(--sig-blue) !important;
    color: white !important;
    border-radius: 28px !important;
    padding: 10px 22px !important;
    font-weight: 700 !important;
    border: none !important;
}
.full-btn:hover {
    background: #0d4ccc !important;
}

#exit-fullscreen-btn {
    position: fixed;
    bottom: 26px;
    right: 26px;
    z-index: 999999 !important;
}

</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ==========================================================
# CARREGAR DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo Job Profile não encontrado.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan','None','<NA>',''], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True)

# ==========================================================
# CORES SIG POR CARREIRA
# ==========================================================
def get_path_color(path_name):
    p = str(path_name).lower()
    if "manage" in p or "executive" in p: return "#00493b"
    if "professional" in p: return "#73706d"
    if "tech" in p or "support" in p: return "#a09b05"
    return "#145efc"

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
# GERAÇÃO DO MAPA (layout perfeito)
# ==========================================================
@st.cache_data(ttl=600)
def generate_map(df):

    fam_max = (
        df.groupby("Job Family")["Global Grade"]
        .apply(lambda x: max(int(g) for g in x if str(g).isdigit()))
        .sort_values(ascending=False)
    )
    families_order = fam_max.index.tolist()

    submap_ordered = {}
    for fam in families_order:
        tmp = (
            df[df["Job Family"] == fam]
            .groupby("Sub Job Family")["Global Grade"]
            .apply(lambda x: max(int(g) for g in x if str(g).isdigit()))
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

    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    html = []
    html.append("<div class='map-wrapper'><div class='jobmap-grid'>")

    # GG header
    html.append("<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    # Família
    col = 2
    for fam in families_order:
        subs = submap_ordered[fam]
        span = len(subs)
        html.append(f"<div class='header-family' style='grid-column:{col} / span {span};'>{fam}</div>")
        col += span

    # Subfamília
    for (fam, sub), c in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{c};'>{sub}</div>")

    # GG CELLS + BORDER TOP ON FIRST ROW
    row = 3
    first_row = True

    for g in grades:

        if first_row:
            html.append(f"<div class='gg-cell' style='grid-row:{row}; border-top:1px solid white !important;'>GG {g}</div>")
            first_row = False
        else:
            html.append(f"<div class='gg-cell' style='grid-row:{row};'>GG {g}</div>")

        for (fam, sub), c_idx in submap.items():
            recs = cards.get((fam, sub, g), [])
            cell = ""

            for r in recs:
                color = get_path_color(r["Career Path"])
                cell += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{r['Job Profile']}</b>"
                    f"<span>{r['Career Path']} – GG {g}</span>"
                    "</div>"
                )

            html.append(f"<div class='cell' style='grid-column:{c_idx}; grid-row:{row};'>{cell}</div>")

        row += 1

    html.append("</div></div>")
    return "".join(html)

# RENDER
st.markdown(generate_map(df_flt), unsafe_allow_html=True)

# ==========================================================
# FULLSCREEN
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

if not st.session_state.fs:
    if st.button("⛶ Tela Cheia", key="enterfs", type="primary"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:

    components.html("""
    <script>
    document.addEventListener('keydown', (e)=>{
        if(e.key === "Escape"){
            window.parent.document.querySelector('#exit-fullscreen-btn').click();
        }
    });
    </script>
    """, height=0, width=0)

    st.markdown("""
    <button class="full-btn" id="exit-fullscreen-btn" onclick="window.parent.location.reload()">
        ❌ Sair
    </button>
    """, unsafe_allow_html=True)
