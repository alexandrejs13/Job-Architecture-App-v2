# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação de até 3 perfis, layout executivo, somente Job Profile.xlsx

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER PADRÃO (NOVA IDENTIDADE)
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
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)


header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS LOCAL – FUNDO BRANCO + LAYOUT EXECUTIVO
# ==========================================================
custom_css = """
<style>
/* Fundo branco do app */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}

/* Container mais amplo, mas sem esticar infinito */
.block-container {
    max-width: 1400px !important;
}

/* Título da área de filtros */
.jp-section-title-main {
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}

/* Grid de comparação: 1, 2 ou 3 colunas */
.jp-comparison-grid {
    display: grid;
    gap: 20px;
    margin-top: 20px;
}

/* Card / coluna de perfil */
.jp-card {
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid #e3e3e3;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    padding: 18px 18px 20px 18px;
    display: flex;
    flex-direction: column;
}

/* Header do card */
.jp-title {
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 4px;
    color: #222;
}
.jp-gg {
    font-size: 0.95rem;
    font-weight: 800;
    color: #145efc;
    margin-bottom: 12px;
}

/* Bloco meta (Job Family, Sub, etc.) */
.jp-meta-block {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.88rem;
    margin-bottom: 14px;
}
.jp-meta-row {
    margin-bottom: 4px;
}

/* Seções de descrição */
.jp-section {
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 10px;
    background: #fafafa;
    border-left: 4px solid #145efc;
}
.jp-section.alt {
    background: #f0f4ff; /* alternativa suave */
    border-left-color: #4f5d75;
}
.jp-section-title {
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.jp-text {
    font-size: 0.88rem;
    line-height: 1.45;
    white-space: pre-wrap;
}

/* Quando não há conteúdo, omitir espaço */
.jp-section.empty {
    display: none;
}

/* Mensagens de info/warning mais discretas */
.jp-info {
    font-size: 0.9rem;
    color: #555;
}

/* Responsividade: garante que com 3 colunas não vire "palito" em telas menores */
@media (max-width: 1200px) {
    .jp-comparison-grid {
        grid-template-columns: 1fr 1fr !important;
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
# CARREGAMENTO DOS DADOS – APENAS Job Profile.xlsx
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)

    # Normalizar strings
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    # Limpeza de GG
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

# Garantir colunas usadas (evita KeyError se faltar algo)
expected_cols = [
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
]
for c in expected_cols:
    if c not in df.columns:
        df[c] = ""

# ==========================================================
# FILTROS – Família / Subfamilia / Career Path
# ==========================================================
st.markdown('<div class="jp-section-title-main">🔍 Explorador de Perfis</div>', unsafe_allow_html=True)

familias = sorted([f for f in df["Job Family"].dropna().unique() if str(f).strip() != ""])

col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family:", ["Selecione..."] + familias, index=0)

with col2:
    if familia != "Selecione...":
        subs = sorted(
            [
                s
                for s in df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()
                if str(s).strip() != ""
            ]
        )
    else:
        subs = []
    sub = st.selectbox("Sub Job Family:", ["Selecione..."] + subs, index=0)

with col3:
    if sub != "Selecione...":
        paths = sorted(
            [
                p
                for p in df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()
                if str(p).strip() != ""
            ]
        )
    else:
        paths = []
    trilha = st.selectbox("Career Path:", ["Selecione..."] + paths, index=0)

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
st.markdown("### ✨ Comparativo de Perfis Selecionados")

# ==========================================================
# RENDER – GRID DE CARDS
# ==========================================================
html_parts = [f'<div class="jp-comparison-grid" style="{grid_template}">']

for card in cards_data:
    job_profile = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    job_family = html.escape(str(card.get("Job Family", "")))
    sub_family = html.escape(str(card.get("Sub Job Family", "")))
    career_path = html.escape(str(card.get("Career Path", "")))
    full_code = html.escape(str(card.get("Full Job Code", "")))

    def esc(colname: str) -> str:
        return html.escape(str(card.get(colname, "") or "")).strip()

    sections = [
        ("🧭 Sub Job Family Description", esc("Sub Job Family Description")),
        ("🧠 Job Profile Description", esc("Job Profile Description")),
        ("🏛️ Career Band Description", esc("Career Band Description")),
        ("🎯 Role Description", esc("Role Description")),
        ("🏅 Grade Differentiator", esc("Grade Differentiator")),
        ("🎓 Qualifications", esc("Qualifications")),
        ("📌 Specific parameters / KPIs", esc("Specific parameters / KPIs")),
        ("⚙️ Competencies 1", esc("Competencies 1")),
        ("⚙️ Competencies 2", esc("Competencies 2")),
        ("⚙️ Competencies 3", esc("Competencies 3")),
    ]

    card_html = []
    card_html.append('<div class="jp-card">')

    # Cabeçalho fixo do card
    card_html.append(f'<div class="jp-title">{job_profile}</div>')
    card_html.append(f'<div class="jp-gg">GG {gg}</div>')

    # Bloco meta
    card_html.append('<div class="jp-meta-block">')
    card_html.append(f'<div class="jp-meta-row"><b>Job Family:</b> {job_family}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Sub Job Family:</b> {sub_family}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Career Path:</b> {career_path}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Full Job Code:</b> {full_code}</div>')
    card_html.append("</div>")

    # Seções (alternando cor)
    for idx, (title, content) in enumerate(sections):
        content = content.strip()
        if not content or content.lower() == "nan":
            # Se vazio, não mostra
            continue

        section_classes = "jp-section"
        if idx % 2 == 1:
            section_classes += " alt"

        card_html.append(f'<div class="{section_classes}">')
        card_html.append(f'<div class="jp-section-title">{html.escape(title)}</div>')
        card_html.append(f'<div class="jp-text">{content}</div>')
        card_html.append("</div>")

    card_html.append("</div>")  # fecha jp-card
    html_parts.append("".join(card_html))

html_parts.append("</div>")  # fecha grid
st.markdown("".join(html_parts), unsafe_allow_html=True)
