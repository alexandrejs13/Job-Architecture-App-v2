# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — Job Maps com layout SIG

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
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)


header("assets/icons/globe_trade.png", "Job Maps")


# ==========================================================
# 2. CSS — GRID, STICKY E FULLSCREEN
# ==========================================================
st.markdown(
    """
<style>
:root {
    --sig-sky:      #145efc;   /* Project / default */
    --sig-forest3:  #00493b;   /* Management */
    --sig-sand4:    #73706d;   /* Professional */
    --sig-moss3:    #a09b05;   /* Technical */
    --gg-bg:        #222222;
    --grid-border:  #e0e0e0;
    --sub-bg:       #f5f3ef;
}

/* container do mapa */
.map-wrapper {
    margin-top: 10px;
    max-height: 72vh;
    overflow: auto;
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid var(--grid-border);
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* grid base */
.jobmap-grid {
    display: grid;
    width: max-content;
    background: #ffffff;
    font-size: 0.86rem;
    grid-auto-rows: minmax(90px, auto);  /* altura automática, mas com mínimo confortável */
}

/* células de conteúdo */
.cell {
    border-right: 1px solid var(--grid-border);
    border-bottom: 1px solid var(--grid-border);
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;       /* centraliza verticalmente dentro da célula (inclusive mescladas) */
    align-content: center;
    background: #ffffff;
}

/* coluna GG — header e linhas */
.gg-header {
    background: var(--gg-bg);
    color: #ffffff;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 40;
    border-right: 1px solid #ffffff;
    border-bottom: 1px solid #ffffff;
}
.gg-cell {
    background: var(--gg-bg);
    color: #ffffff;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    left: 0;                  /* fixa horizontalmente (coluna congelada) */
    z-index: 30;
    border-right: 1px solid #ffffff;
    border-bottom: 1px solid #ffffff;   /* linhas bem separadas */
}

/* família (linha 1) */
.header-family {
    font-weight: 750;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 25;
    padding: 6px 8px;
    border-right: 1px solid #ffffff;
    border-bottom: 0 !important;       /* remove linha branca entre família e subfamília */
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
}

/* subfamília (linha 2) */
.header-subfamily {
    font-weight: 600;
    text-align: center;
    position: sticky;
    top: 50px;                          /* exatamente abaixo da família */
    z-index: 24;
    padding: 6px 8px;
    border-right: 1px solid var(--grid-border);
    border-top: 0 !important;          /* remove linha branca herdada */
    color: #222222;
    background: var(--sub-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    height: 42px;
}

/* card do job */
.job-card {
    background: #ffffff;
    border: 1px solid var(--grid-border);
    border-left-width: 3px !important; /* borda fina */
    border-radius: 8px;
    padding: 6px 8px;
    min-width: 180px;
    max-width: 230px;
    flex: 0 0 auto;                    /* ficam lado a lado, coluna alarga conforme 1,2,3... */
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}
.job-card b {
    display: block;
    font-size: 0.78rem;
    margin-bottom: 3px;
    line-height: 1.25;
}
.job-card span {
    font-size: 0.72rem;
    color: #555555;
}

/* botão fullscreen / sair */
#fs-exit-container {
    position: fixed;
    right: 30px;
    bottom: 30px;
    z-index: 10000;
}
#fs-exit-container button {
    background: #111111 !important;    /* preto fosco */
    color: #ffffff !important;
    border-radius: 40px !important;
    padding: 12px 26px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35) !important;
}
#fs-exit-container button:hover {
    background: #000000 !important;
}

/* wrapper em tela cheia */
.map-fullscreen {
    position: fixed !important;
    inset: 0 !important;
    background: #ffffff;
    z-index: 9000 !important;
    padding: 20px 24px !important;
    overflow: auto !important;
}

/* botão "Tela Cheia" normal */
[data-testid="stButton"] button {
    border-radius: 999px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# 3. CARREGAR E PREPARAR DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo 'Job Profile.xlsx' não encontrado ou vazio.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = (
    df["Sub Job Family"].astype(str).str.strip().replace(["nan", "None", "<NA>", ""], "-")
)
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

df = df[
    (df["Job Family"] != "")
    & (df["Job Profile"] != "")
    & (df["Global Grade"] != "")
]


# ==========================================================
# 4. CORES POR TRILHA (SIG)
# ==========================================================
def get_path_color(path: str) -> str:
    p = str(path).lower()
    if "manage" in p or "executive" in p:
        return "#00493b"  # SIG Forest 3 – Management
    if "professional" in p:
        return "#73706d"  # SIG Sand 4 – Professional
    if "tech" in p or "support" in p:
        return "#a09b05"  # SIG Moss 3 – Technical
    return "#145efc"      # SIG Sky – Project / default


# ==========================================================
# 5. FILTROS SIMPLES
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
# 6. FUNÇÃO DO MAPA — MERGE VERTICAL + CENTRALIZAÇÃO
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df: pd.DataFrame) -> str:
    if df.empty:
        return "<div style='padding:20px;'>Nenhum dado encontrado.</div>"

    families_order = sorted(df["Job Family"].unique())
    grades = sorted(
        df["Global Grade"].unique(),
        key=lambda x: int(x) if str(x).isdigit() else 999,
        reverse=True,
    )

    # ----- mapa de subfamílias → coluna do grid -----
    submap = {}
    col_index = 2  # 1 é GG
    header_spans = {}

    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        header_spans[fam] = len(subs)
        for s in subs:
            submap[(fam, s)] = col_index
            col_index += 1

    # ----- agrupamento dos cards por célula -----
    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # ----- assinatura de conteúdo para merge vertical -----
    content_map = {}
    span_map = {}
    skip_set = set()

    for g in grades:
        for (fam, sf), c_idx in submap.items():
            rec = cards.get((fam, sf, g), [])
            if rec:
                sig = "|".join(
                    sorted(f"{r['Job Profile']}{r['Career Path']}" for r in rec)
                )
                content_map[(g, c_idx)] = sig
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

    # ----- largura dinâmica das colunas (1,2,3 cards…) -----
    cards_count_map = {}
    for g in grades:
        for (fam, sf), c_idx in submap.items():
            rec = cards.get((fam, sf, g), [])
            cards_count_map[(g, c_idx)] = len(rec)

    col_widths = ["160px"]  # primeira coluna GG
    for (fam, sf), c_idx in sorted(submap.items(), key=lambda x: x[1]):
        max_cards = 0
        for g in grades:
            if (g, c_idx) not in skip_set:
                max_cards = max(max_cards, cards_count_map.get((g, c_idx), 0))

        max_cards = max(1, min(max_cards, 5))  # limita a 5 cards visíveis lado a lado
        base_card = 200  # largura base aproximada
        gap = 8
        width_px = base_card * max_cards + gap * max(0, max_cards - 1)
        col_widths.append(f"{width_px}px")

    grid_template = "grid-template-columns: " + " ".join(col_widths) + ";"

    # ======================================================
    # CONSTRUÇÃO DO HTML
    # ======================================================
    html = [f"<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>"]

    # HEADER GG (fixo no topo + esquerda)
    html.append("<div class='gg-header'>GG</div>")

    # FAMÍLIAS (linha 1, sticky)
    col = 2
    # paleta simples para famílias: alterna um conjunto de cores fortes
    fam_colors = [
        "#145efc",
        "#00493b",
        "#73706d",
        "#dca0ff",
        "#00493b",
        "#145efc",
        "#73706d",
    ]
    fam_color_map = {f: fam_colors[i % len(fam_colors)] for i, f in enumerate(families_order)}

    for fam in families_order:
        span = header_spans[fam]
        bg = fam_color_map[fam]
        html.append(
            f"<div class='header-family' "
            f"style='grid-row:1; grid-column:{col} / span {span}; background:{bg};'>"
            f"{fam}</div>"
        )
        col += span

    # SUBFAMÍLIAS (linha 2, sticky)
    for (fam, sf), c_idx in submap.items():
        bg_sub = "#f5f3ef"
        html.append(
            f"<div class='header-subfamily' "
            f"style='grid-row:2; grid-column:{c_idx}; background:{bg_sub};'>"
            f"{sf}</div>"
        )

    # LINHAS DE GG + CÉLULAS
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
                f"grid-row:{row_idx} / span {span};" if span > 1 else f"grid-row:{row_idx};"
            )

            recs = cards.get((fam, sf, g), [])
            cell_cards = ""

            for rc in recs:
                color = get_path_color(rc["Career Path"])
                cell_cards += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rc['Job Profile']}</b>"
                    f"<span>{rc['Career Path']}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-column:{c_idx}; {row_span}'>{cell_cards}</div>"
            )

        row_idx += 1

    html.append("</div></div>")
    return "".join(html)


# ==========================================================
# 7. CONTROLE DE TELA CHEIA
# ==========================================================
if "fs_jobmap" not in st.session_state:
    st.session_state.fs_jobmap = False

btn_col = st.columns([6, 1])[1]
if not st.session_state.fs_jobmap:
    if btn_col.button("⛶ Tela Cheia", use_container_width=True):
        st.session_state.fs_jobmap = True
        st.rerun()

# modo tela cheia
if st.session_state.fs_jobmap:
    st.markdown("<div class='map-fullscreen'>", unsafe_allow_html=True)

    # botão sair (preto fosco, canto inferior direito)
    st.markdown("<div id='fs-exit-container'>", unsafe_allow_html=True)
    if st.button("Sair"):
        st.session_state.fs_jobmap = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ESC para sair
    components.html(
        """
        <script>
        document.addEventListener('keydown', (e) => {
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

# ==========================================================
# 8. RENDERIZAÇÃO DO MAPA
# ==========================================================
st.markdown(generate_map_html(df_filtered), unsafe_allow_html=True)
