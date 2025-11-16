# pages/4_Job_Maps.py
# Modern UI • Clean Design • Fullscreen • Career Indicators • Apple-style Exit Button

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIGURAÇÃO DE PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")

# ==========================================================
# HEADER NOVO (VISUAL CLEAN)
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
# CSS CLEAN + MODERNIZAÇÃO DO MAPA
# ==========================================================
clean_css = """
<style>

:root {
    --border: #d9d9d9;
    --subtle-bg: #f7f7f7;
    --header-bg: #eaeaea;
    --gg-bg: #3c3c3c;
    --text-gray: #444;
}

/* GRID WRAPPER */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-radius: 10px;
    border: 0.5px solid var(--border);
    background: white;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    border-collapse: collapse;
    font-size: 0.88rem;
}

/* HEADERS */
.header-family {
    background: var(--header-bg);
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-subfamily {
    background: var(--subtle-bg);
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    font-weight: 600;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* GG LEFT COLUMN */
.gg-header {
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
}

.gg-cell {
    background: var(--gg-bg);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* CELLS */
.cell {
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    padding: 6px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

/* JOB CARD CLEAN */
.job-card {
    background: white;
    border: 0.5px solid var(--border);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 6px 8px;
    width: 135px;
    height: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    transition: 0.20s ease;
}

.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.job-card b {
    font-size: 0.78rem;
    margin-bottom: 3px;
    color: #333;
}

.job-card span {
    font-size: 0.7rem;
    color: #666;
}

/* FULLSCREEN EXIT BUTTON - APPLE STYLE */
#exit-fullscreen-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 999999 !important;
    background: #111 !important;
    color: white !important;
    border-radius: 28px !important;
    padding: 12px 28px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.35) !important;
    cursor: pointer;
}
#exit-fullscreen-btn:hover {
    transform: scale(1.06);
}

</style>
"""
st.markdown(clean_css, unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DE DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo Job Profile não encontrado ou vazio.")
    st.stop()

# Pré-processamento
df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan', 'None', '<NA>'], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

df = df[(df["Job Family"] != "") & (df["Job Profile"] != "") & (df["Global Grade"] != "")]

# ==========================================================
# CORES DISCRETAS POR CARREIRA (OPÇÃO 2)
# ==========================================================
def get_path_color(path_name):
    p = str(path_name).lower()
    if "manage" in p or "executive" in p: return "#4F5D75"      # Taupe / Steel Blue
    if "professional" in p: return "#2F2F2F"                   # Graphite
    if "tech" in p or "support" in p: return "#7C7C7C"         # Cool Gray
    return "#5F6C7A"                                           # Blue-gray

# ==========================================================
# FILTROS (minimalistas)
# ==========================================================
families = ["Todas"] + sorted(df["Job Family"].unique())
paths = ["Todas"] + sorted(df["Career Path"].unique())

colA, colB = st.columns(2)
fam_filter = colA.selectbox("Job Family", families)
path_filter = colB.selectbox("Career Path", paths)

df_flt = df.copy()
if fam_filter != "Todas":
    df_flt = df_flt[df_flt["Job Family"] == fam_filter]
if path_filter != "Todas":
    df_flt = df_flt[df_flt["Career Path"] == path_filter]

# ==========================================================
# GERAÇÃO DO MAPA HTML (estrutura original preservada)
# ==========================================================
@st.cache_data(ttl=600)
def generate_map(df):

    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)
    families_order = sorted(df["Job Family"].unique())

    # subfamilias
    submap = {}
    col_index = 2
    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        for s in subs:
            submap[(fam, s)] = col_index
            col_index += 1

    # cards agrupados
    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    html = []
    html.append("<div class='map-wrapper'><div class='jobmap-grid'>")

    # GG header
    html.append(f"<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    # famílias
    col = 2
    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        span = len(subs)
        html.append(f"<div class='header-family' style='grid-row:1; grid-column:{col} / span {span};'>{fam}</div>")
        col += span

    # subfamílias
    for (fam, subfam), c in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-row:2; grid-column:{c};'>{subfam}</div>")

    # cells
    row_idx = 3
    for g in grades:
        html.append(f"<div class='gg-cell' style='grid-row:{row_idx}; grid-column:1;'>GG {g}</div>")

        for (fam, subfam), c_idx in submap.items():
            records = cards.get((fam, subfam, g), [])
            cell_html = ""

            for rec in records:
                color = get_path_color(rec["Career Path"])
                cell_html += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rec['Job Profile']}</b>"
                    f"<span>{rec['Career Path']}</span>"
                    "</div>"
                )

            html.append(f"<div class='cell' style='grid-row:{row_idx}; grid-column:{c_idx};'>{cell_html}</div>")

        row_idx += 1

    html.append("</div></div>")
    return "".join(html)

# Renderização
st.markdown(generate_map(df_flt), unsafe_allow_html=True)

# ==========================================================
# FULLSCREEN — BOTÃO PRETO FOSCO (APPLE STYLE)
# ==========================================================
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

# ATIVA FULLSCREEN
if st.button("⛶ Tela Cheia"):
    st.session_state.fullscreen = True
    st.rerun()

# FULLSCREEN MODE
if st.session_state.fullscreen:

    # ESC PARA SAIR
    components.html("""
    <script>
    document.addEventListener('keydown', (e)=>{
        if(e.key === "Escape"){
            window.parent.document.querySelector('#exit-fullscreen-btn').click();
        }
    });
    </script>
    """, height=0, width=0)

    # BOTÃO SAIR (PRETO FOSCO)
    st.markdown("""
    <button id="exit-fullscreen-btn" onclick="window.parent.location.reload()">
        ❌ Sair
    </button>
    """, unsafe_allow_html=True)
