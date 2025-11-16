# pages/3_Job_Profile_Description.py
# Nova versão completa, integrada ao design atual do app SIG

import streamlit as st
import pandas as pd
import numpy as np
import re
import html

from utils.data_loader import load_excel_data

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER — identidade visual nova
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
# CSS GLOBAL + COR DE FUNDO SIG
# ==========================================================
st.markdown("""
<style>
html, body, .main, .block-container, [data-testid="stAppViewContainer"] {
    background: #f5f3f0 !important;
}

.comparison-grid {
    display: grid;
    gap: 20px;
    margin-top: 25px;
}

.grid-cell {
    background: #fff;
    border: 1px solid #e0e0e0;
    padding: 16px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
}

.header-cell {
    background: #f8f9fa;
    border-bottom: none;
}

.fjc-title {
    font-size: 18px;
    font-weight: 800;
    color: #2c3e50;
    margin-bottom: 10px;
    min-height: 45px;
}

.fjc-gg {
    font-weight: 700;
    color: #145efc;
}

.meta-cell {
    font-size: 0.9rem;
    color: #333;
    min-height: 110px;
}

.meta-row {
    margin-bottom: 4px;
}

.section-cell {
    border-left-width: 5px;
    border-left-style: solid;
    background: #fafafa;
}

.section-title {
    font-weight: 700;
    margin-bottom: 6px;
}

.section-content {
    font-size: 0.9rem;
    color: #444;
    line-height: 1.45;
    white-space: pre-wrap;
}

.footer-cell {
    height: 10px;
    border: none;
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# FUNÇÕES
# ==========================================================
def normalize_grade(val):
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "na", "-"):
        return ""
    return re.sub(r"\.0$", "", s)

# ==========================================================
# CARREGAMENTO DOS ARQUIVOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())
levels = data.get("level_structure", pd.DataFrame())

if df.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado.")
    st.stop()

# ==========================================================
# NORMALIZAÇÃO DO JOB PROFILE
# ==========================================================
df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(
    ["nan", "None", "<NA>", ""], "-"
)
df["Career Path"] = df["Career Path"].astype(str).str.strip()

df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
df["GG"] = df["Global Grade"]
df["Global Grade Num"] = pd.to_numeric(df["Global Grade"], errors="coerce").fillna(0).astype(int)

# ==========================================================
# NORMALIZAÇÃO DO LEVELS — FIX DEFINITIVO
# ==========================================================
if not levels.empty:

    # padroniza nomes das colunas
    levels.columns = (
        levels.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # tenta localizar a coluna de level name
    if "level_name" not in levels.columns:
        for c in levels.columns:
            if "level" in c:
                levels.rename(columns={c: "level_name"}, inplace=True)
                break

    # normaliza gg
    if "global_grade" in levels.columns:
        levels["global_grade"] = levels["global_grade"].apply(normalize_grade)
        levels["gg_num"] = pd.to_numeric(
            levels["global_grade"], errors="coerce"
        ).fillna(0).astype(int)
    else:
        levels["gg_num"] = 0

# ==========================================================
# FILTROS
# ==========================================================
st.markdown("## Explorador de Perfis de Cargo")

col1, col2, col3 = st.columns(3)

with col1:
    fam = st.selectbox("Job Family", ["Todas"] + sorted(df["Job Family"].unique()))

with col2:
    subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique()) if fam != "Todas" else []
    sub = st.selectbox("Sub Job Family", ["Todas"] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].unique()) if sub != "Todas" else []
    path = st.selectbox("Career Path", ["Todas"] + paths)

filtered = df.copy()
if fam != "Todas":
    filtered = filtered[filtered["Job Family"] == fam]
if sub != "Todas":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if path != "Todas":
    filtered = filtered[filtered["Career Path"] == path]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar perfis.")
    st.stop()

# ==========================================================
# MULTISELECT (GG + Cargo)
# ==========================================================
filtered["label"] = filtered.apply(
    lambda r: f"GG {r['GG']} • {r['Job Profile']}", axis=1
)
mapping = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(mapping.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

selecionados = [mapping[l] for l in selecionados_labels]

# ==========================================================
# EXTRAÇÃO DOS CARDS
# ==========================================================
cards_data = []
for job in selecionados:

    row = filtered[filtered["Job Profile"] == job]
    if row.empty:
        continue

    row = row.iloc[0].copy()
    gg_num = int(row["Global Grade Num"])

    # level name
    lvl = ""
    if not levels.empty and "level_name" in levels.columns:
        match = levels[levels["gg_num"] == gg_num]
        if not match.empty:
            lvl = match["level_name"].iloc[0]

    cards_data.append({"row": row, "level": lvl})

if not cards_data:
    st.warning("Não foi possível carregar os perfis selecionados.")
    st.stop()

# ==========================================================
# GRID DE COMPARAÇÃO
# ==========================================================
st.markdown("## Comparação de Perfis")

cols = len(cards_data)
grid_style = f"grid-template-columns: repeat({cols}, 1fr);"

html_grid = f'<div class="comparison-grid" style="{grid_style}">'

# Cabeçalho
for card in cards_data:
    r = card["row"]
    lvl = card["level"]

    html_grid += f"""
    <div class="grid-cell header-cell">
        <div class="fjc-title">{html.escape(r['Job Profile'])}</div>
        <div class="fjc-gg">GG {r['GG']} • {lvl}</div>
    </div>
    """

# Metadados
for card in cards_data:
    r = card["row"]

    meta = f"""
        <div class="meta-row"><strong>Família:</strong> {html.escape(r["Job Family"])}</div>
        <div class="meta-row"><strong>Sub-Família:</strong> {html.escape(r["Sub Job Family"])}</div>
        <div class="meta-row"><strong>Carreira:</strong> {html.escape(r["Career Path"])}</div>
    """

    html_grid += f'<div class="grid-cell meta-cell">{meta}</div>'

# Seções do conteúdo
sections = [
    ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
    ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
    ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
    ("🎯 Role Description", "Role Description", "#145efc"),
    ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
    ("🎓 Qualifications", "Qualifications", "#009688"),
]

for title, field, color in sections:
    for card in cards_data:
        text = str(card["row"].get(field, "")).strip()

        if text == "" or text.lower() == "nan":
            html_grid += "<div class='grid-cell section-cell' style='background:transparent;border:none;'></div>"
        else:
            html_grid += f"""
            <div class="grid-cell section-cell" style="border-left-color:{color};">
                <div class="section-title" style="color:{color};">{title}</div>
                <div class="section-content">{html.escape(text)}</div>
            </div>
            """

# Rodapé
for _ in cards_data:
    html_grid += "<div class='grid-cell footer-cell'></div>"

html_grid += "</div>"

st.markdown(html_grid, unsafe_allow_html=True)
