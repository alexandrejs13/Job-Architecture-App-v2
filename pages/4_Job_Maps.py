# pages/4_Job_Maps.py
# Job Maps • Visual Clean • Mesclagem Vertical • Sticky Headers • Fullscreen

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
# 2. CSS CLEAN + STICKY + FULLSCREEN
# ==========================================================
clean_css = """
<style>
:root {
    --border: #d9d9d9;
    --subtle-bg: #f7f7f7;
    --header-bg: #eaeaea;
    --gg-bg: #111111;        /* GG bem escuro */
    --text-gray: #444;
}

/* WRAPPER DO MAPA */
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
    border-collapse: collapse;
    font-size: 0.88rem;
    grid-auto-rows: 110px;
}

/* CÉLULAS GENÉRICAS */
.jobmap-grid > div {
    box-sizing: border-box;
}

/* HEADER FAMÍLIA (linha 1) */
.header-family {
    background: var(--header-bg);
    border-right: 0.5px solid var(--border);
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 0;
    z-index: 20;
    height: 50px;
}

/* HEADER SUBFAMÍLIA (linha 2) */
.header-subfamily {
    background: var(--subtle-bg);
    border-right: 0.5px solid var(--border);
    font-weight: 600;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 50px;        /* logo abaixo da família */
    z-index: 19;
    height: 45px;
}

/* REMOVER "linha branca" entre família e subfamília */
.header-family {
    border-bottom: 0px solid transparent;
}
.header-subfamily {
    border-top: 0px solid transparent;
}

/* COLUNA GG HEADER (canto superior esquerdo) */
.gg-header {
    background: var(--gg-bg);
    color: white;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 0;
    left: 0;
    z-index: 30;
    border-right: 2px solid white;
    border-bottom: 1px solid white;
}

/* CÉLULAS GG (coluna fixa) */
.gg-cell {
    background: var(--gg-bg);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    left: 0;
    z-index: 25;
    border-right: 2px solid white;
    border-bottom: 1px solid white;  /* linha branca entre GG's */
}

/* CELULAS DE CARGO */
.cell {
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    padding: 6px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;       /* centraliza verticalmente os cards na célula (inclusive mesclada) */
    align-content: center;
}

/* JOB CARD – TAMANHO FIXO (135 x 75) */
.job-card {
    background: white;
    border: 0.5px solid var(--border);
    border-left-width: 4px !important;   /* borda lateral mais grossa */
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

/* FULLSCREEN WRAPPER (aplicado via CSS dinâmico quando fullscreen=True) */
.map-wrapper.fullscreen {
    position: fixed !important;
    top: 0;
    left: 0;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 9999 !important;
    border-radius: 0 !important;
    border: none !important;
}

/* BOTÃO PRETO FOSCO PARA SAIR DO FULLSCREEN */
#exit-fullscreen-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 100000 !important;
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
# 3. CARREGAMENTO DE DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo Job Profile não encontrado ou vazio.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(
    ["nan", "None", "<NA>"], "-"
)
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

df = df[
    (df["Job Family"] != "")
    & (df["Job Profile"] != "")
    & (df["Global Grade"] != "")
]

# ==========================================================
# 4. CORES SIG NA BORDA ESQUERDA DO CARD
# ==========================================================
def get_path_color(path_name: str) -> str:
    """
    Cores usando a lógica SIG:
    - Management / Executive  -> #00493b (verde petróleo escuro)
    - Professional            -> #73706d (cinza escuro)
    - Technical / Support     -> #a09b05 (verde musgo)
    - Default (Project etc.)  -> #145efc (azul SIG)
    """
    p = str(path_name).lower()
    if "manage" in p or "executive" in p:
        return "#00493b"   # Management
    if "professional" in p:
        return "#73706d"   # Professional
    if "tech" in p or "support" in p:
        return "#a09b05"   # Technical
    return "#145efc"       # Project / default

# ==========================================================
# 5. FILTROS MINIMALISTAS + BOTÃO DE TELA CHEIA
# ==========================================================
families = ["Todas"] + sorted(df["Job Family"].unique())
paths = ["Todas"] + sorted(df["Career Path"].unique())

if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

colA, colB, colC = st.columns([2, 2, 1])
fam_filter = colA.selectbox("Job Family", families)
path_filter = colB.selectbox("Career Path", paths)

with colC:
    st.write("")  # espaçamento
    if not st.session_state.fullscreen:
        if st.button("⛶ Tela Cheia", use_container_width=True):
            st.session_state.fullscreen = True
            st.rerun()

df_flt = df.copy()
if fam_filter != "Todas":
    df_flt = df_flt[df_flt["Job Family"] == fam_filter]
if path_filter != "Todas":
    df_flt = df_flt[df_flt["Career Path"] == path_filter]

# ==========================================================
# 6. GERAÇÃO DO MAPA COM MESCLAGEM VERTICAL
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df_local: pd.DataFrame) -> str:
    """
    - Mantém a estrutura do primeiro mapa que você gostou
    - Adiciona mesclagem vertical quando o conteúdo da célula é igual em GG diferentes
    - Mantém GG visível em cada linha (coluna 1)
    - Sticky:
        - GG em X/Y (header e linhas)
        - Família e Subfamily
    """

    if df_local.empty:
        return "<div style='padding:20px;'>Nenhum dado encontrado.</div>"

    grades = sorted(
        df_local["Global Grade"].unique(),
        key=lambda x: int(x) if str(x).isdigit() else 999,
        reverse=True,
    )
    families_order = sorted(df_local["Job Family"].unique())

    # --- MAPA DE SUBFAMÍLIAS E SPAN DA FAMÍLIA ---
    submap = {}
    header_spans = {}
    col_index = 2  # 1ª coluna é GG

    for fam in families_order:
        subs = sorted(df_local[df_local["Job Family"] == fam]["Sub Job Family"].unique())
        header_spans[fam] = len(subs)
        for sf in subs:
            submap[(fam, sf)] = col_index
            col_index += 1

    # --- AGRUPAMENTO DE CARDS POR (Família, Subfamília, GG) ---
    grouped = df_local.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards_data = {k: v.to_dict("records") for k, v in grouped}

    # --- MAPA DE CONTEÚDO PARA MESCLAGEM VERTICAL ---
    content_map = {}
    span_map = {}
    skip_set = set()

    # assinatura de conteúdo por célula (para saber quando mesclar)
    for g in grades:
        for (fam, sf), c_idx in submap.items():
            recs = cards_data.get((fam, sf, g), [])
            if recs:
                # assinatura: conjunto de (Job Profile + Career Path)
                sig = "|".join(
                    sorted(f"{r['Job Profile']}|{r['Career Path']}" for r in recs)
                )
                content_map[(g, c_idx)] = sig
            else:
                content_map[(g, c_idx)] = None

    # cálculo do span vertical
    for (fam, sf), c_idx in submap.items():
        for i, g in enumerate(grades):
            if (g, c_idx) in skip_set:
                continue

            current_sig = content_map[(g, c_idx)]
            if current_sig is None:
                span_map[(g, c_idx)] = 1
                continue

            span = 1
            for g2 in grades[i + 1 :]:
                if content_map[(g2, c_idx)] == current_sig:
                    span += 1
                    skip_set.add((g2, c_idx))
                else:
                    break
            span_map[(g, c_idx)] = span

    # ======================================================
    # CONSTRUÇÃO DO HTML
    # ======================================================
    # largura da primeira coluna GG = 160px (mais confortável)
    num_sub_cols = len(submap)
    grid_style = (
        f"grid-template-columns: 160px repeat({num_sub_cols}, 220px);"
        "grid-template-rows: 50px 45px;"
    )

    html = []
    html.append(
        f"<div class='map-wrapper{' fullscreen' if st.session_state.get('fullscreen', False) else ''}'>"
        f"<div class='jobmap-grid' style='{grid_style}'>"
    )

    # HEADER GG (cobre linha 1 e 2)
    html.append(
        "<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>"
    )

    # HEADER FAMÍLIAS (linha 1)
    col = 2
    for fam in families_order:
        span = header_spans[fam]
        html.append(
            f"<div class='header-family' style='grid-row:1; grid-column:{col} / span {span};'>{fam}</div>"
        )
        col += span

    # HEADER SUBFAMÍLIAS (linha 2)
    for (fam, sf), c_idx in submap.items():
        html.append(
            f"<div class='header-subfamily' style='grid-row:2; grid-column:{c_idx};'>{sf}</div>"
        )

    # LINHAS DE GG + CÉLULAS
    row_idx = 3
    for g in grades:
        # GG LABEL – COLUNA 1, STICKY
        html.append(
            f"<div class='gg-cell' style='grid-row:{row_idx}; grid-column:1;'>GG {g}</div>"
        )

        for (fam, sf), c_idx in submap.items():
            # se essa célula está sendo mesclada com alguma acima, pular
            if (g, c_idx) in skip_set:
                continue

            span = span_map.get((g, c_idx), 1)
            row_span = (
                f"grid-row:{row_idx} / span {span};"
                if span > 1
                else f"grid-row:{row_idx};"
            )

            records = cards_data.get((fam, sf, g), [])
            cards_html = ""

            # monta cards — todos com o mesmo tamanho
            for rec in records:
                color = get_path_color(rec["Career Path"])
                # Texto: "Career Path GG-13" etc.
                label = f"{rec['Career Path']} GG-{g}"
                cards_html += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rec['Job Profile']}</b>"
                    f"<span>{label}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-column:{c_idx}; {row_span}'>{cards_html}</div>"
            )

        row_idx += 1

    html.append("</div></div>")  # fecha jobmap-grid e map-wrapper
    return "".join(html)


# ==========================================================
# 7. FULLSCREEN (CSS + BOTÃO SAIR)
# ==========================================================
# Quando em fullscreen, aplicamos CSS extra para usar a tela toda
if st.session_state.fullscreen:
    st.markdown(
        """
        <style>
        .map-wrapper {
            position: fixed !important;
            top: 0;
            left: 0;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 9999 !important;
            border-radius: 0 !important;
            border: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ESC para sair (recarrega a página e reseta fullscreen=False)
    components.html(
        """
        <script>
        document.addEventListener('keydown', (e)=>{
            if(e.key === "Escape"){
                window.parent.location.reload();
            }
        });
        </script>
        """,
        height=0,
        width=0,
    )

    # Botão preto fosco no canto inferior direito
    st.markdown(
        """
        <button id="exit-fullscreen-btn" onclick="window.parent.location.reload()">
            ❌ Sair
        </button>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# 8. RENDERIZAÇÃO FINAL DO MAPA
# ==========================================================
st.markdown(generate_map_html(df_flt), unsafe_allow_html=True)
