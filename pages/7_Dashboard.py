import streamlit as st
import pandas as pd
import altair as alt
import base64
import os

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# HELPERS
# ==========================================================
def load_icon_png(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_font_base64(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        return None


# ==========================================================
# LOAD SIG FONT (SE EXISTIR) + GLOBAL LAYOUT/CSS
# ==========================================================
font_regular_b64 = load_font_base64("assets/fonts/PP-SIG-Flow-Regular.ttf")
font_semibold_b64 = load_font_base64("assets/fonts/PP-SIG-Flow-Semibold.ttf")

font_css = ""
if font_regular_b64 and font_semibold_b64:
    font_css = f"""
    @font-face {{
        font-family: 'SIGFlow';
        src: url(data:font/ttf;base64,{font_regular_b64}) format('truetype');
        font-weight: 400;
    }}

    @font-face {{
        font-family: 'SIGFlow';
        src: url(data:font/ttf;base64,{font_semibold_b64}) format('truetype');
        font-weight: 600;
    }}

    *, body {{
        font-family: 'SIGFlow', system-ui, -apple-system, BlinkMacSystemFont,
                     'Segoe UI', sans-serif !important;
    }}
    """

SIG_COLORS = [
    "#145EFC",  # SIG Sky
    "#DCA0FF",  # SIG Spark
    "#167665",  # SIG Forest 2
    "#F5F073",  # SIG Moss 1
    "#73706D",  # SIG Sand 4
    "#BFBAB5",  # SIG Sand 3
    "#E5DFD9",  # SIG Sand 2
    "#4FA593",  # SIG Moss 2
]

st.markdown(
    f"""
<style>
{font_css}

    /* GLOBAL LAYOUT — impede esticar infinito e centraliza conteúdo */
    .main > div {{
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }}

    .stDataFrame {{
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }}

    .block-container, .stColumn {{
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* GRID PARA CARDS DE KPI */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 28px;
    }}

    .kpi-box {{
        background: #F8F6F3;
        border: 1px solid #E5E0D8;
        border-radius: 14px;
        padding: 12px 16px;
        min-height: 72px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 0 0 1px rgba(0,0,0,0.02);
    }}

    .kpi-title {{
        font-size: 13px;
        font-weight: 600;
        color: #444;
    }}

    .kpi-value {{
        font-size: 24px;
        font-weight: 600;
        color: #145EFC;
        margin-top: 2px;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# HEADER — padrão SIG
# ==========================================================
icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(
    f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:600; margin:0; padding:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""",
    unsafe_allow_html=True,
)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_excel("data/Job Profile.xlsx")


df = load_data()

COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_GRADE = "Global Grade"

# ==========================================================
# TABS
# ==========================================================
tab_overview, tab_family = st.tabs(["Overview", "Family Micro-Analysis"])

# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab_overview:
    st.markdown("## Overview")

    kpis = {
        "Job Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for label, value in kpis.items():
        st.markdown(
            f"""
            <div class='kpi-box'>
                <div class='kpi-title'>{label}</div>
                <div class='kpi-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # Subfamilies per Family — BARRAS VERTICAIS
    # ------------------------------------------------------
    st.markdown("### Subfamilies per Family")

    subf = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bar_colors = SIG_COLORS * (len(subf) // len(SIG_COLORS) + 1)
    subf["Color"] = bar_colors[: len(subf)]

    bar_chart = (
        alt.Chart(subf)
        .mark_bar()
        .encode(
            x=alt.X(f"{COL_FAMILY}:N", sort="-y", title="Job Family"),
            y=alt.Y("Count:Q", title="Number of Subfamilies"),
            color=alt.Color(
                "Color:N",
                scale=None,
                legend=None,
            ),
            tooltip=[COL_FAMILY, "Count"],
        )
        .properties(height=420)
    )

    st.altair_chart(bar_chart, use_container_width=True)

# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab_family:
    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].dropna().unique())
    selected_family = st.selectbox("Select Job Family:", families)

    family_df_all = df[df[COL_FAMILY] == selected_family]

    subfamilies = sorted(family_df_all[COL_SUBFAMILY].dropna().unique())
    subfamily_options = ["All"] + subfamilies
    selected_subfamily = st.selectbox("Select Sub Job Family:", subfamily_options)

    if selected_subfamily != "All":
        family_df = family_df_all[family_df_all[COL_SUBFAMILY] == selected_subfamily]
    else:
        family_df = family_df_all.copy()

    # KPIs para a família selecionada
    metrics = {
        "Subfamilies in Family": family_df_all[COL_SUBFAMILY].nunique(),
        "Profiles": family_df[COL_PROFILE].nunique(),
        "Career Paths": family_df[COL_CAREER_PATH].nunique(),
        "Global Grades": family_df[COL_GRADE].nunique(),
    }

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for label, value in metrics.items():
        st.markdown(
            f"""
            <div class='kpi-box'>
                <div class='kpi-title'>{label}</div>
                <div class='kpi-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # GRADE SPREAD — BARRAS VERTICAIS
    # ------------------------------------------------------
    st.markdown("### Grade Spread")

    if not family_df.empty:
        grade_spread = (
            family_df.groupby(COL_GRADE)[COL_PROFILE]
            .nunique()
            .reset_index(name="Profiles")
            .sort_values(COL_GRADE)
        )

        grade_chart = (
            alt.Chart(grade_spread)
            .mark_bar()
            .encode(
                x=alt.X(f"{COL_GRADE}:O", title="Global Grade"),
                y=alt.Y("Profiles:Q", title="Number of Profiles"),
                color=alt.value("#145EFC"),
                tooltip=[COL_GRADE, "Profiles"],
            )
            .properties(height=360)
        )

        st.altair_chart(grade_chart, use_container_width=True)
    else:
        st.info("No profiles found for the selected combination.")

    # ------------------------------------------------------
    # TABELA DE PERFIS
    # ------------------------------------------------------
    st.markdown("### Profiles in Selection")

    table_cols = [COL_PROFILE, COL_SUBFAMILY, COL_CAREER_PATH, COL_GRADE]
    st.dataframe(
        family_df[table_cols].sort_values([COL_SUBFAMILY, COL_PROFILE]),
        use_container_width=True,
    )
