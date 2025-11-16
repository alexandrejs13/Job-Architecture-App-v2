import streamlit as st
import pandas as pd
import re
import html

st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER NOVO (mantido igual ao app novo)
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
# CSS — fundo branco e layout igual ao app novo
# ==========================================================
st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background-color: white !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* GRID */
.comparison-grid {
    display: grid;
    gap: 22px;
    margin-top: 25px;
}

.grid-cell {
    background: white;
    border: 1px solid #e0e0e0;
    padding: 16px;
    border-radius: 8px;
}

.header-cell {
    background: #f5f7fa;
    border: 1px solid #e0e0e0;
}

.fjc-title {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 6px;
}

.fjc-gg {
    font-size: 14px;
    font-weight: 700;
    color: #145efc;
}

.meta-cell {
    font-size: 0.9rem;
    color: #444;
}

.meta-row {
    margin-bottom: 6px;
}

.section-cell {
    border-left-width: 5px !important;
    border-left-style: solid !important;
    background: #fafafa;
}

.section-title {
    font-weight: 700;
    margin-bottom: 8px;
}

.section-content {
    font-size: 0.88rem;
    line-height: 1.45;
    white-space: pre-wrap;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# LOAD DATA
# ==========================================================
def normalize_grade(val):
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "-", "na"):
        return ""
    return re.sub(r"\.0$", "", s)

@st.cache_data
def load_excel(path):
    try:
        df = pd.read_excel(path)
        for c in df.columns:
            df[c] = df[c].astype(str).str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_excel("data/Job Profile.xlsx")
levels = load_excel("data/Level Structure.xlsx")

if df.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado.")
    st.stop()

df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
df["GG"] = df["Global Grade"]
df["Global Grade Num"] = pd.to_numeric(df["Global Grade"], errors="coerce").fillna(0).astype(int)

if not levels.empty:
    levels.rename(columns=lambda x: x.strip(), inplace=True)
    levels["Global Grade"] = levels["Global Grade"].apply(normalize_grade)
    levels["Global Grade Num"] = pd.to_numeric(levels["Global Grade"], errors="coerce").fillna(0).astype(int)

# ==========================================================
# IDENTIFICAÇÃO AUTOMÁTICA DA COLUNA "LEVEL NAME"
# ==========================================================
level_name_col = None
for col in levels.columns:
    if col.lower().replace(" ", "") in ["levelname", "level", "lvlname"]:
        level_name_col = col
        break

# fallback caso não exista nenhuma coluna válida
if level_name_col is None:
    level_name_col = levels.columns[-1]

# ==========================================================
# FILTROS
# ==========================================================
st.subheader("Explorador de Perfis de Cargo")

familias = sorted(df["Job Family"].unique())

col1, col2, col3 = st.columns(3)
with col1:
    familia = st.selectbox("Job Family", familias)

with col2:
    subs = sorted(df[df["Job Family"] == familia]["Sub Job Family"].unique())
    sub = st.selectbox("Sub Job Family", subs)

with col3:
    paths = sorted(df[(df["Job Family"] == familia) & (df["Sub Job Family"] == sub)]["Career Path"].unique())
    trilha = st.selectbox("Career Path", paths)

filtered = df[
    (df["Job Family"] == familia)
    & (df["Sub Job Family"] == sub)
    & (df["Career Path"] == trilha)
]

filtered["label"] = filtered.apply(
    lambda r: f"GG {r['GG']} • {r['Job Profile']}", axis=1
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

# ==========================================================
# CARDS
# ==========================================================
st.markdown("## Comparação de Perfis")

cards = []
for nome in selecionados:
    row = filtered[filtered["Job Profile"] == nome].iloc[0]

    gg_num = int(row["Global Grade Num"])
    match = levels[levels["Global Grade Num"] == gg_num]

    level_name = ""
    if not match.empty and level_name_col in match.columns:
        level_name = match[level_name_col].iloc[0]

    cards.append(
        {
            "row": row,
            "level": level_name,
        }
    )

# ==========================================================
# GRID
# ==========================================================
n = len(cards)
grid = f'<div class="comparison-grid" style="grid-template-columns: repeat({n}, 1fr);">'

# HEADERS
for c in cards:
    grid += f"""
    <div class="grid-cell header-cell">
        <div class="fjc-title">{html.escape(c['row']['Job Profile'])}</div>
        <div class="fjc-gg">GG {c['row']['Global Grade']} • {html.escape(c['level'])}</div>
    </div>
    """

# META
for c in cards:
    r = c["row"]
    grid += f"""
    <div class="grid-cell meta-cell">
        <div class="meta-row"><strong>Família:</strong> {html.escape(r['Job Family'])}</div>
        <div class="meta-row"><strong>Sub-Família:</strong> {html.escape(r['Sub Job Family'])}</div>
        <div class="meta-row"><strong>Carreira:</strong> {html.escape(r['Career Path'])}</div>
    </div>
    """

# CONFIG DAS SEÇÕES
sections = [
    ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
    ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
    ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
    ("🎯 Role Description", "Role Description", "#145efc"),
    ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
    ("🎓 Qualifications", "Qualifications", "#009688"),
]

# CONTEÚDO DAS SEÇÕES
for title, field, color in sections:
    for c in cards:
        content = str(c["row"].get(field, "")).strip()
        if content in ["", "nan", "None"]:
            grid += "<div class='grid-cell'></div>"
        else:
            grid += f"""
            <div class="grid-cell section-cell" style="border-left-color:{color};">
                <div class="section-title" style="color:{color};">{title}</div>
                <div class="section-content">{html.escape(content)}</div>
            </div>
            """

grid += "</div>"

st.markdown(grid, unsafe_allow_html=True)
