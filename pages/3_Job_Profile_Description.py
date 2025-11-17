# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação de até 3 perfis (SIG Design System)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER COM ÍCONE PNG (HTML, sem st.image)
# ==========================================================
def header_with_icon():
    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:14px;
            margin-top:8px;
            margin-bottom:8px;
        ">
            <img src="assets/icons/business_review_clipboard.png"
                 style="
                    width:32px;
                    height:32px;
                    image-rendering:-webkit-optimize-contrast;
                    image-rendering:crisp-edges;
                 ">
            <h1 style="
                margin:0;
                padding:0;
                font-size:36px;
                font-weight:700;
            ">
                Job Profile Description
            </h1>
        </div>
        <hr style="margin-top:6px; margin-bottom:4px;">
        """,
        unsafe_allow_html=True,
    )

header_with_icon()

# ==========================================================
# CSS GLOBAL DA PÁGINA (layout + cards + scroll sync)
# ==========================================================
custom_css = """
<style>
/* -------- Fonte global (já carregada via assets/css/fonts) -------- */
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
    font-weight: 400;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-SemiBold.otf') format('opentype');
    font-weight: 600;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: 700;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

/* Sidebar fixa, não redimensionável */
[data-testid="stSidebar"] {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
}
[data-testid="stSidebar"] > div {
    width: 300px !important;
}

/* Conteúdo central limitado */
.block-container {
    max-width: 1600px !important;
    padding-top: 0.5rem !important;
}

/* Título da área de filtros */
.jp-section-title-main {
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}

/* -------- GRID PRINCIPAL DE COMPARAÇÃO -------- */
.jp-comparison-grid {
    display: grid;
    gap: 24px;
    width: 100%;
}

/* CARD – altura fixa, header fixo e body rolável */
.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 650px;       /* Altura padrão pedida */
    overflow: hidden;    /* esconde scroll externo */
}

/* HEADER do card (fica sempre visível porque não rola) */
.jp-card-header {
    padding: 18px 22px 12px 22px;
    border-bottom: 1px solid #f0f0f0;
    background: #ffffff;
    z-index: 5;
}

.jp-title {
    font-size: 1.20rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Bloco meta (Job Family, Sub, Path, Code) */
.jp-meta-block {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 0.88rem;
}
.jp-meta-row {
    margin-bottom: 4px;
}

/* BODY rolável com descrições */
.jp-card-body {
    flex: 1;
    overflow-y: auto;
    padding: 14px 22px 10px 22px;
}

/* Scrollbar mais discreta */
.jp-card-body::-webkit-scrollbar {
    width: 8px;
}
.jp-card-body::-webkit-scrollbar-thumb {
    background: #c8c8c8;
    border-radius: 10px;
}

/* -------- SEÇÕES DENTRO DO BODY -------- */
.jp-section {
    padding: 12px 10px 12px 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    background: #fafafa;
}

.jp-section.alt {
    background: #f0f4ff;
}

.jp-section-title {
    font-weight: 600;
    font-size: 0.92rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ícone SVG inline dentro do título */
.jp-section-title svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
}

.jp-text {
    line-height: 1.45;
    font-size: 0.90rem;
    white-space: pre-wrap;
}

/* Footer do card com ícone de PDF */
.jp-footer {
    padding: 10px 18px 12px 18px;
    text-align: right;
    border-top: 1px solid #f2f2f2;
}

.jp-footer img {
    width: 24px;
    height: 24px;
    cursor: pointer;
    opacity: 0.75;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
    transition: 0.2s ease;
}

.jp-footer img:hover {
    opacity: 1;
    transform: scale(1.05);
}

/* Responsividade: em telas menores cai para 2 ou 1 colunas */
@media (max-width: 1200px) {
    .jp-comparison-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
}
@media (max-width: 900px) {
    .jp-comparison-grid {
        grid-template-columns: 1fr !important;
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================================
# SVG INLINE – lidos do diretório assets/icons/sig
# ==========================================================
def load_svg(name: str) -> str:
    """Lê o SVG e devolve o conteúdo pronto para embed inline."""
    path = Path("assets/icons/sig") / name
    if not path.exists():
        return ""  # se faltar algum, não quebra a página
    return path.read_text(encoding="utf-8")

SVG_HIERARCHY = load_svg("Hierarchy.svg")
SVG_CLIPBOARD = load_svg("File_Clipboard_Text.svg")
SVG_BAG = load_svg("Shopping_Business_Target.svg")
SVG_PENCIL = load_svg("Edit_Pencil.svg")
SVG_BOOK = load_svg("Content_Book_Phone.svg")
SVG_GRAPH = load_svg("Graph_Bar.svg")
SVG_COG = load_svg("Setting_Cog.svg")

# Mapeamento das seções -> SVG inline
SECTION_SVGS = {
    "Sub Job Family Description": SVG_HIERARCHY,
    "Job Profile Description": SVG_CLIPBOARD,
    "Career Band Description": SVG_HIERARCHY,
    "Role Description": SVG_BAG,
    "Grade Differentiator": SVG_PENCIL,
    "Qualifications": SVG_BOOK,
    "Specific parameters / KPIs": SVG_GRAPH,
    "Competencies 1": SVG_COG,
    "Competencies 2": SVG_COG,
    "Competencies 3": SVG_COG,
}

SECTIONS_ORDER = list(SECTION_SVGS.keys())

# ==========================================================
# CARREGAMENTO DOS DADOS – APENAS Job Profile.xlsx
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    # Normalizar Global Grade
    if "Global Grade" in df.columns:
        df["Global Grade"] = (
            df["Global Grade"]
            .astype(str)
            .str.strip()
            .str.replace(r"\\.0$", "", regex=True)
        )
    return df

df = load_job_profile()
if df.empty:
    st.error("Arquivo 'Job Profile.xlsx' não encontrado ou vazio em data/Job Profile.xlsx.")
    st.stop()

# Garante colunas necessárias
for col in [
    "Job Family",
    "Sub Job Family",
    "Career Path",
    "Job Profile",
    "Global Grade",
    "Full Job Code",
    "Sub Job Family Description",
    "Job Profile Description",
    "Career Band Description",
    "Role Description",
    "Grade Differentiator",
    "Qualifications",
    "Specific parameters / KPIs",
    "Competencies 1",
    "Competencies 2",
    "Competencies 3",
]:
    if col not in df.columns:
        df[col] = ""

# ==========================================================
# FILTROS – Família / Subfamilia / Career Path
# ==========================================================
st.markdown(
    '<div class="jp-section-title-main">🔍 Explorador de Perfis</div>',
    unsafe_allow_html=True,
)

familias = sorted(
    [f for f in df["Job Family"].dropna().unique() if str(f).strip() != ""]
)

col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family", ["Selecione..."] + familias, index=0)

with col2:
    if familia != "Selecione...":
        subs = sorted(
            [
                s
                for s in df[df["Job Family"] == familia]["Sub Job Family"]
                .dropna()
                .unique()
                if str(s).strip() != ""
            ]
        )
    else:
        subs = []
    sub = st.selectbox("Sub Job Family", ["Selecione..."] + subs, index=0)

with col3:
    if sub != "Selecione...":
        paths = sorted(
            [
                p
                for p in df[df["Sub Job Family"] == sub]["Career Path"]
                .dropna()
                .unique()
                if str(p).strip() != ""
            ]
        )
    else:
        paths = []
    trilha = st.selectbox("Career Path", ["Selecione..."] + paths, index=0)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar os perfis.")
    st.stop()

# ==========================================================
# PICKLIST – até 3 perfis para comparar
# ==========================================================
filtered = filtered.copy()
filtered["GG_clean"] = filtered["Global Grade"].astype(str).str.strip()
filtered["label"] = filtered.apply(
    lambda r: f'GG {r["GG_clean"] or "-"} • {r["Job Profile"]}', axis=1
)
label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)
if not selecionados_labels:
    st.info("Selecione pelo menos 1 perfil para exibir os detalhes.")
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

# ==========================================================
# PREPARAR DADOS DOS CARDS
# ==========================================================
cards_data = []
for nome in selecionados:
    row = filtered[filtered["Job Profile"] == nome]
    if row.empty:
        continue
    cards_data.append(row.iloc[0].to_dict())

if not cards_data:
    st.warning("Nenhum perfil encontrado após aplicar os filtros.")
    st.stop()

num_cards = len(cards_data)
grid_template = f"grid-template-columns: repeat({num_cards}, minmax(0, 1fr));"

st.markdown("---")
st.markdown("### ✨ Comparativo de Perfis Selecionados", unsafe_allow_html=True)

# ==========================================================
# RENDER – GRID DE CARDS (HEADER FIXO + BODY ROLÁVEL SINCRONIZADO)
# ==========================================================
html_parts = [
    f'<div class="jp-comparison-grid" style="{grid_template}">'
]

for card in cards_data:
    job_profile = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    job_family = html.escape(str(card.get("Job Family", "")))
    sub_family = html.escape(str(card.get("Sub Job Family", "")))
    career_path = html.escape(str(card.get("Career Path", "")))
    full_code = html.escape(str(card.get("Full Job Code", "")))

    def esc(colname: str) -> str:
        return html.escape(str(card.get(colname, "") or "")).strip()

    card_html = []
    card_html.append('<div class="jp-card">')

    # HEADER (fixo)
    card_html.append('<div class="jp-card-header">')
    card_html.append(f'<div class="jp-title">{job_profile}</div>')
    card_html.append(f'<div class="jp-gg">GG {gg}</div>')
    card_html.append('<div class="jp-meta-block">')
    card_html.append(f'<div class="jp-meta-row"><b>Job Family:</b> {job_family}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Sub Job Family:</b> {sub_family}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Career Path:</b> {career_path}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Full Job Code:</b> {full_code}</div>')
    card_html.append('</div>')  # meta-block
    card_html.append('</div>')  # jp-card-header

    # BODY (rolável + sincronizado)
    card_html.append('<div class="jp-card-body jp-sync-body">')

    for idx, section_name in enumerate(SECTIONS_ORDER):
        content = esc(section_name)
        if not content or content.lower() == "nan":
            continue

        svg_inline = SECTION_SVGS.get(section_name, "")
        alt_class = " alt" if idx % 2 == 1 else ""

        card_html.append(f'<div class="jp-section{alt_class}">')
        card_html.append('<div class="jp-section-title">')
        if svg_inline:
            card_html.append(svg_inline)
        card_html.append(f'<span>{html.escape(section_name)}</span>')
        card_html.append('</div>')  # jp-section-title
        card_html.append(f'<div class="jp-text">{content}</div>')
        card_html.append('</div>')  # jp-section

    card_html.append('</div>')  # jp-card-body

    # Footer PDF no final do card
    card_html.append('<div class="jp-footer">')
    card_html.append(
        '<img src="assets/icons/sig/pdf_c3_white.svg" '
        'title="Export PDF">'
    )
    card_html.append('</div>')  # jp-footer

    card_html.append('</div>')  # jp-card

    html_parts.append("".join(card_html))

html_parts.append("</div>")  # fecha grid

# HTML + CSS na página
st.markdown("".join(html_parts), unsafe_allow_html=True)

# ==========================================================
# JS PARA SINCRONIZAR O SCROLL ENTRE OS CARDS
# ==========================================================
sync_scroll_js = """
<script>
(function() {
  const syncScroll = () => {
    const bodies = document.querySelectorAll('.jp-sync-body');
    bodies.forEach(body => {
      body.addEventListener('scroll', () => {
        const pos = body.scrollTop;
        bodies.forEach(b => {
          if (b !== body) {
            b.scrollTop = pos;
          }
        });
      });
    });
  };
  window.addEventListener('load', syncScroll);
})();
</script>
"""
st.markdown(sync_scroll_js, unsafe_allow_html=True)
