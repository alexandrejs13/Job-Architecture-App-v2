import streamlit as st
import pandas as pd
import altair as alt
import base64, os

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# LOAD FONT (PP SIG FLOW)
# ==========================================================
def load_font_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

font_regular = load_font_base64("assets/fonts/PP-SIG-Flow-Regular.ttf")
font_semibold = load_font_base64("assets/fonts/PP-SIG-Flow-Semibold.ttf")

# ==========================================================
# GLOBAL CSS (APLICA TIPOGRAFIA + GRID REAL)
# ==========================================================
st.markdown(f"""
<style>

@font-face {{
    font-family: 'SIGFlow';
    src: url(data:font/ttf;base64,{font_regular}) format('truetype');
    font-weight: 400;
}}

@font-face {{
    font-family: 'SIGFlow';
    src: url(data:font/ttf;base64,{font_semibold}) format('truetype');
    font-weight: 600;
}}

*, body {{
    font-family: 'SIGFlow', sans-serif !important;
}}

section.main > div {{
    max-width: 1180px;
}}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 18px;
    margin-bottom: 32px;
}}

.kpi-box {{
    background: #F2EFEB;
    border: 1px solid #E5E0D8;
    border-radius: 14px;
    padding: 14px 18px;
    height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.kpi-title {{
    font-size: 14px;
    font-weight: 600;
    color: #000;
}}

.kpi-value {{
    font-size: 26px;
    font-weight: 600;
    color: #145EFC;
    margin-top: 4px;
}}

.legend-item {{
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:8px;
}}

.legend-dot {{
    width:12px;
    height:12px;
    border-radius:50%;
}}

.legend-badge {{
    margin-left:auto;
    background:#145EFC;
    color:white;
    padding:2px 12px;
    border-radius:12px;
    font-weight:600;
}}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path): return ""
    with open(path,"rb") as f: return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:600; margin:0; padding:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():
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
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])

# ==========================================================
# TAB 1
# ==========================================================
with tab1:

    st.markdown("## Overview")

    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
    }

    # CARDS — HORIZONTAIS DE VERDADE
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for t, v in kpis.items():
        st.markdown(
            f"""
            <div class='kpi-box'>
                <div class='kpi-title'>{t}</div>
                <div class='kpi-value'>{v}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # DONUT
    # ------------------------------------------------------
    st.markdown("## Subfamilies per Family")

    subf = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    SIG_COLORS = [
        "#145EFC", "#dca0ff", "#167665", "#f5f073", 
        "#73706d", "#bfba b5", "#e5dfd9", "#4fa593"
    ]

    subf["Color"] = [SIG_COLORS[i % len(SIG_COLORS)] for i in range(len(subf))]

    c1, c2 = st.columns([1.2,1])

    with c1:
        donut = (
            alt.Chart(subf)
            .mark_arc(innerRadius=60)
            .encode(
                theta="Count",
                color=alt.Color("Color:N", scale=None),
                tooltip=[COL_FAMILY, "Count"]
            )
        )
        st.altair_chart(donut, use_container_width=True)

    with c2:
        for _, row in subf.iterrows():
            st.markdown(
                f"""
                <div class='legend-item'>
                    <div class='legend-dot' style='background:{row["Color"]};'></div>
                    <div style="font-weight:600;">{row[COL_FAMILY]}</div>
                    <div class='legend-badge'>{row["Count"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ------------------------------------------------------
    # BARRAS — ESPAÇADAS, ALTURA PREMIUM
    # ------------------------------------------------------
    st.markdown("## Profiles per Subfamily (Total)")

    bars_df = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bars = (
        alt.Chart(bars_df)
        .mark_bar(size=32)
        .encode(
            x="Count:Q",
            y=alt.Y(f"{COL_SUBFAMILY}:N", sort='-x'),
            color=alt.value("#145EFC")
        )
        .properties(height=36 * len(bars_df))
    )

    st.altair_chart(bars, use_container_width=True)

# ==========================================================
# TAB 2
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    fams = sorted(df[COL_FAMILY].unique())
    sel = st.selectbox("Select Family:", fams)

    fam_df = df[df[COL_FAMILY] == sel]

    metrics = {
        "Subfamilies": fam_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
        "Career Paths": fam_df[COL_CAREER_PATH].nunique(),
    }

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for t, v in metrics.items():
        st.markdown(
            f"""
            <div class='kpi-box'>
                <div class='kpi-title'>{t}</div>
                <div class='kpi-value'>{v}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.dataframe(
        fam_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_GRADE]],
        use_container_width=True
    )
