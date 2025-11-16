# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — versão robusta + visual novo unificado

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from utils.data_loader import load_excel_data


# ==========================================================
# 1. CONFIGURAÇÃO DE PÁGINA + HEADER PADRÃO
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")


def header(icon_path: str, title: str):
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
            unsafe_allow_html=True,
        )
    # linha fina abaixo do título
    st.markdown("<hr style='margin-top:5px; margin-bottom:20px;'>", unsafe_allow_html=True)


header("assets/icons/globe_trade.png", "Job Maps")


# ==========================================================
# 2. CSS BASE DO MAPA (ROBUSTO + AJUSTES)
# ==========================================================
css_base = """
<style>
:root {
    --sig-sky:   #145efc;   /* Project / default */
    --sig-forest3: #00493b; /* Management */
    --sig-sand4: #73706d;   /* Professional */
    --sig-moss3: #a09b05;   /* Technical */
    --grid-border: #e0e0e0;
    --gg-bg: #222222;
    --gg-border: #ffffff;
}

/* container principal da página */
.block-container {
    max-width: 1600px !important;
    padding: 1.5rem 3.5rem 3rem !important;
}

/* wrapper do mapa */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    background: #fafafa;
    border-radius: 10px;
    border: 1px solid var(--grid-border);
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* grid do mapa */
.jobmap-grid {
    display: grid;
    width: max-content;
    border-collapse: collapse;
    font-size: 0.86rem;
    grid-auto-rows: 110px;
    background: #ffffff;
}

/* células genéricas */
.jobmap-grid > div {
    box-sizing: border-box;
}

/* família (linha 1) - STICKY, SEM LINHA EM BRANCO */
.header-family {
    font-weight: 800;
    color: #ffffff;
    padding: 0 6px;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 30;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid rgba(255,255,255,0.40);
    border-bottom: 0;      /* remove linha branca entre família e subfamília */
}

/* subfamília (linha 2) - STICKY logo abaixo da família */
.header-subfamily {
    font-weight: 600;
    padding: 0 6px;
    text-align: center;
    position: sticky;
    top: 50px;             /* exatamente a altura da família */
    z-index: 29;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f2efeb;
    color: #2f2f2f;
    border-right: 1px solid var(--grid-border);
    border-top: 0;         /* garante que não haja faixa branca entre as duas linhas */
}

/* cabeçalho GG (canto superior esquerdo) - STICKY nas duas direções */
.gg-header {
    background: var(--gg-bg);
    color: #ffffff;
    font-weight: 800;
    text-align: center;
    position: sticky;
    top: 0;
    left: 0;
    z-index: 40;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 2px solid var(--gg-border);
    border-bottom: 1px solid var(--gg-border);
}

/* coluna GG - STICKY na horizontal, altura por linha + borda branca entre linhas */
.gg-cell {
    background: var(--gg-bg);
    color: #ffffff;
    font-weight: 700;
    position: sticky;
    left: 0;
    z-index: 35;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 2px solid var(--gg-border);
    border-bottom: 1px solid var(--gg-border);  /* separação branca entre GGs */
}

/* células do corpo */
.cell {
    background: #ffffff;
    border-right: 1px solid var(--grid-border);
    border-bottom: 1px solid var(--grid-border);
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;        /* centraliza verticalmente os cards dentro da célula (inclusive mesclada) */
    justify-content: center;    /* centraliza horizontalmente o conjunto de cards */
}

/* cards dos cargos (visual clean + borda lateral fina colorida) */
.job-card {
    background: #ffffff;
    border: 1px solid var(--grid-border);
    border-left-width: 3px !important;  /* borda fina */
    border-radius: 8px;
    padding: 6px 8px;
    width: 150px;
    height: 78px;
    font-size: 0.76rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    transition: box-shadow 0.15s ease, transform 0.15s ease;
}
.job-card b {
    display: block;
    margin-bottom: 3px;
    font-weight: 700;
}
.job-card span {
    font-size: 0.72rem;
    color: #666666;
}
.job-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

/* FULLSCREEN: estilos adicionais são injetados dinamicamente via css_fullscreen */

#fs-exit-container button {
    background: #111111 !important;
    color: #ffffff !important;
    border-radius: 40px !important;
    padding: 12px 28px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35) !important;
}
#fs-exit-container button:hover {
    background: #000000 !important;
}
</style>
"""
st.markdown(css_base, unsafe_allow_html=True)


css_fullscreen = """
<style>
header, section[data-testid="stSidebar"], footer {
    display: none !important;
}
.block-container {
    max-width: 100vw !important;
    padding: 0 !important;
    margin: 0 !important;
}
.map-wrapper {
    position: fixed !important;
    top: 0;
    left: 0;
    width: 100vw !important;
    height: 100vh !important;
    border-radius: 0 !important;
    border-width: 0 !important;
    box-shadow: none !important;
    z-index: 9998 !important;
}
#fs-exit-container {
    position: fixed !important;
    bottom: 28px !important;
    right: 28px !important;
    z-index: 10000 !important;
}
</style>
"""


# ==========================================================
# 3. CARREGAMENTO E PREPARAÇÃO DO DATAFRAME
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Erro ao carregar dados do Job Profile.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = (
    df["Sub Job Family"].astype(str).str.strip().replace(["nan", "None", "<NA>", ""], "-")
)
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = (
    df["Global Grade"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
)

# limpa linhas inválidas
df = df[
    (df["Job Family"] != "")
    & (df["Job Profile"] != "")
    & (df["Global Grade"] != "")
]


# ==========================================================
# 4. CORES SIG POR CARREIRA (BORDA LATERAL DO CARD)
# ==========================================================
def get_path_color(path: str) -> str:
    p = str(path).lower()
    if "manage" in p or "executive" in p:
        return "#00493b"   # SIG Forest 3 – Management
    if "professional" in p:
        return "#73706d"   # SIG Sand 4 – Professional
    if "tech" in p or "support" in p:
        return "#a09b05"   # SIG Moss 3 – Technical
    return "#145efc"       # SIG Sky – Project / default


# ==========================================================
# 5. CONTROLES DE FILTRO + ESTADO DE TELA CHEIA
# ==========================================================
if "jobmap_fullscreen" not in st.session_state:
    st.session_state.jobmap_fullscreen = False

families = ["Todas"] + sorted(df["Job Family"].unique())
paths = ["Todas"] + sorted(df["Career Path"].unique())

if not st.session_state.jobmap_fullscreen:
    colA, colB, colC = st.columns([2.5, 2.5, 1])
    fam_sel = colA.selectbox("Job Family", families, key="jobmap_fam")
    path_sel = colB.selectbox("Career Path", paths, key="jobmap_path")
    colC.write("")  # espaçamento
    if colC.button("⛶ Tela cheia", use_container_width=True, key="jobmap_fs_enter"):
        st.session_state.jobmap_fullscreen = True
        st.rerun()
else:
    # em tela cheia, usamos os filtros já salvos no estado
    fam_sel = st.session_state.get("jobmap_fam", "Todas")
    path_sel = st.session_state.get("jobmap_path", "Todas")
    # aplica CSS de fullscreen
    st.markdown(css_fullscreen, unsafe_allow_html=True)

    # botão sair (preto fosco) fixo no canto inferior direito
    st.markdown("<div id='fs-exit-container'>", unsafe_allow_html=True)
    if st.button("Sair", key="jobmap_fs_exit"):
        st.session_state.jobmap_fullscreen = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ESC para sair da tela cheia
    components.html(
        """
        <script>
        document.addEventListener('keydown', function(e){
            if (e.key === 'Escape') {
                const btn = window.parent.document.querySelector('#fs-exit-container button');
                if (btn) { btn.click(); }
            }
        });
        </script>
        """,
        height=0,
        width=0,
    )

# aplica filtros ao dataframe
df_filtered = df.copy()
if fam_sel != "Todas":
    df_filtered = df_filtered[df_filtered["Job Family"] == fam_sel]
if path_sel != "Todas":
    df_filtered = df_filtered[df_filtered["Career Path"] == path_sel]

if df_filtered.empty:
    st.info("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()


# ==========================================================
# 6. FUNÇÃO PRINCIPAL DO MAPA (MERGE VERTICAL + STICKY)
# ==========================================================
def _grade_key(x: str) -> int:
    s = str(x).strip()
    return int(s) if s.isdigit() else 999


@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df_in: pd.DataFrame) -> str:
    families = sorted(df_in["Job Family"].unique())
    grades = sorted(df_in["Global Grade"].unique(), key=_grade_key, reverse=True)

    # ----- mapa de subfamílias -> posição da coluna -----
    submap = {}
    fam_span = {}
    col_index = 2  # coluna 1 é GG

    for fam in families:
        subs = sorted(df_in[df_in["Job Family"] == fam]["Sub Job Family"].unique())
        fam_span[fam] = len(subs)
        for sf in subs:
            submap[(fam, sf)] = col_index
            col_index += 1

    # ----- agrupamento dos cards -----
    grouped = df_in.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # ----- conteúdo e merge vertical -----
    content_map = {}
    span_map = {}
    skip_set = set()

    for g in grades:
        for (fam, sf), c_idx in submap.items():
            recs = cards.get((fam, sf, g), [])
            if recs:
                # assinatura do conteúdo da célula
                content_map[(g, c_idx)] = "|".join(
                    sorted(f"{r['Job Profile']}{r['Career Path']}" for r in recs)
                )
            else:
                content_map[(g, c_idx)] = None

    for (fam, sf), c_idx in submap.items():
        for i, g in enumerate(grades):
            if (g, c_idx) in skip_set:
                continue

            current_sig = content_map[(g, c_idx)]

            if current_sig is None:
                span_map[(g, c_idx)] = 1
                continue

            span = 1
            for next_g in grades[i + 1 :]:
                if content_map[(next_g, c_idx)] == current_sig:
                    span += 1
                    skip_set.add((next_g, c_idx))
                else:
                    break
            span_map[(g, c_idx)] = span

    # ----- construção do HTML -----
    num_subcols = len(submap)
    # 160px para GG + 220px por subfamília (confortável)
    grid_template = f"grid-template-columns:160px repeat({num_subcols}, 220px);"

    html = [f"<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>"]

    # cabeçalho GG (canto superior esquerdo)
    html.append("<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    # cabeçalho de famílias (linha 1)
    col = 2
    # paleta de cores suaves para famílias (usando tons SIG neutros)
    fam_colors = ["#145efc", "#f2efeb", "#dca0ff", "#73706d", "#bfbab5"]
    for i, fam in enumerate(families):
        span = fam_span[fam]
        bg = fam_colors[i % len(fam_colors)]
        html.append(
            f"<div class='header-family' "
            f"style='grid-row:1; grid-column:{col} / span {span}; background:{bg};'>"
            f"{fam}</div>"
        )
        col += span

    # cabeçalho de subfamílias (linha 2)
    for (fam, sf), c_idx in submap.items():
        html.append(
            f"<div class='header-subfamily' style='grid-row:2; grid-column:{c_idx};'>{sf}</div>"
        )

    # linhas por GG
    row_idx = 3
    for g in grades:
        # célula GG da linha
        html.append(
            f"<div class='gg-cell' style='grid-row:{row_idx}; grid-column:1;'>GG {g}</div>"
        )

        for (fam, sf), c_idx in submap.items():
            if (g, c_idx) in skip_set:
                continue

            span = span_map.get((g, c_idx), 1)
            row_span = (
                f"grid-row:{row_idx} / span {span};"
                if span > 1
                else f"grid-row:{row_idx};"
            )

            recs = cards.get((fam, sf, g), [])
            cell_html = ""

            for rec in recs:
                color = get_path_color(rec["Career Path"])
                cell_html += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rec['Job Profile']}</b>"
                    f"<span>{rec['Career Path']}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-column:{c_idx}; {row_span}'>{cell_html}</div>"
            )

        row_idx += 1

    html.append("</div></div>")
    return "".join(html)


# ==========================================================
# 7. RENDERIZAÇÃO FINAL DO MAPA
# ==========================================================
st.markdown(generate_map_html(df_filtered), unsafe_allow_html=True)
