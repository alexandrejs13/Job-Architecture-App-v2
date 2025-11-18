import streamlit as st
import pandas as pd
import altair as alt
import base64, os

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# SAFE FONT LOADER (SIG FLOW)
# ==========================================================
def load_font_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

font_regular = load_font_base64("assets/fonts/PP-SIG-Flow-Regular.ttf")
font_semibold = load_font_base64("assets/fonts/PP-SIG-Flow-Semibold.ttf")

css_fonts = ""
if font_regular:
    css_fonts += f"""
    @font-face {{
        font-family: 'SIGFlow';
        src: url(data:font/ttf;base64,{font_regular}) format('truetype');
        font-weight: 400;
    }}"""
if font_semibold:
    css_fonts += f"""
    @font-face {{
        font-family: 'SIGFlow';
        src: url(data:font/ttf;base64,{font_semibold}) format('truetype');
        font-weight: 600;
    }}"""

# ==========================================================
# GLOBAL CSS – SIG DESIGN SYSTEM
# ==========================================================
st.markdown(f"""
<style>

{css_fonts}

* {{
    font-family: "SIGFlow", sans-serif !important;
}}

section.main > div {{
    max-width: 1280px;
    margin-left: auto;
    margin-right: auto;
}}

.kpi {{
    background: #ffffff;
    border-radius: 16px;
    padding: 18px 24px;
    border: 1px solid #e3e0da;
    box-shadow: 0 3px 14px rgba(0,0,0,0.06);
}}

.kpi-title {{
    font-size: 15px;
    font-weight: 600;
    color: #73706d;
}}

.kpi-value {{
    font-size: 34px;
    font-weight: 700;
    color: #145efc;
    margin-top: 8px;
}}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin: 20px 0;
}}

.card {{
    background: #ffffff;
    border-radius: 18px;
    padding: 26px 32px;
    border: 1px solid #e2e2e2;
    box-shadow: 0 3px 14px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}}

.badge {{
    display:inline-block;
    padding:4px 14px;
    border-radius:12px;
    font-weight:600;
    font-size:13px;
    color:white;
}}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER SIG (PADRÃO)
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path): return ""
    with open(path,"rb") as f: return base64.b64encode(f.read()).decode("utf-8")

icon_b64 = load_icon_png("assets/icons/data_2_perfromance.png")

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
df = pd.read_excel("data/Job Profile.xlsx")

COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_PATH = "Career Path"
COL_GRADE = "Global Grade"


# ==========================================================
# TABS
# ==========================================================
tab1, tab2 = st.tabs(["📊 Overview (Executive)", "🔎 Family Micro-Analysis"])


# ==========================================================
# TAB 1 – EXECUTIVE OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Organizational Structure Overview")

    # -----------------------------------------------------
    # KPIs WTW Style
    # -----------------------------------------------------
    kpis = {
        "Job Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_PATH].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(f"""
        <div class='kpi'>
            <div class='kpi-title'>{title}</div>
            <div class='kpi-value'>{value}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # Grade Distribution (Structure Complexity)
    # -----------------------------------------------------
    st.markdown("### Grade Distribution (Structure Complexity)")

    grade_df = (
        df.groupby(COL_GRADE)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values(COL_GRADE)
    )

    grade_chart = (
        alt.Chart(grade_df)
        .mark_bar(size=26)
        .encode(
            x="Count:Q",
            y=alt.Y(f"{COL_GRADE}:N", sort='-x'),
            color=alt.value("#145efc")
        )
        .properties(height=36 * len(grade_df))
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.altair_chart(grade_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # Family Footprint Heatmap
    # -----------------------------------------------------
    st.markdown("### Family Footprint Heatmap")

    heat_df = (
        df.groupby([COL_FAMILY, COL_SUBFAMILY])[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
    )

    heat = (
        alt.Chart(heat_df)
        .mark_rect()
        .encode(
            x=alt.X(f"{COL_SUBFAMILY}:N", title="Subfamily"),
            y=alt.Y(f"{COL_FAMILY}:N", title="Family"),
            color=alt.Color("Profiles:Q", scale=alt.Scale(
                range=["#dca0ff", "#145efc"])),
            tooltip=[COL_FAMILY, COL_SUBFAMILY, "Profiles"]
        )
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.altair_chart(heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # Career Path Distribution
    # -----------------------------------------------------
    st.markdown("### Career Path Distribution")

    cp_df = (
        df.groupby(COL_PATH)[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
    )

    cp_chart = (
        alt.Chart(cp_df)
        .mark_arc(innerRadius=70)
        .encode(
            theta="Profiles",
            color=alt.Color(COL_PATH, scale=alt.Scale(
                range=["#145efc","#4fa593","#167665","#f5f073"]
            )),
            tooltip=[COL_PATH,"Profiles"]
        )
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.altair_chart(cp_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Deep Dive by Family")

    families = sorted(df[COL_FAMILY].unique())
    sf = st.selectbox("Select Family", families)

    subf = sorted(df[df[COL_FAMILY] == sf][COL_SUBFAMILY].unique())
    ssf = st.selectbox("Select Subfamily", subf)

    sub_df = df[
        (df[COL_FAMILY] == sf) &
        (df[COL_SUBFAMILY] == ssf)
    ]

    # KPIs da Subfamily
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='kpi'>
        <div class='kpi-title'>Profiles</div>
        <div class='kpi-value'>{sub_df[COL_PROFILE].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='kpi'>
        <div class='kpi-title'>Grades</div>
        <div class='kpi-value'>{sub_df[COL_GRADE].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Grade profile for selected subfamily
    st.markdown("### Grade Spread")
    g_spread = (
        sub_df.groupby(COL_GRADE)[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
    )

    g_chart = (
        alt.Chart(g_spread)
        .mark_bar(size=24)
        .encode(
            x="Profiles:Q",
            y=alt.Y(f"{COL_GRADE}:N", sort='-x'),
            color=alt.value("#145efc"),
            tooltip=[COL_GRADE,"Profiles"]
        )
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.altair_chart(g_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # Show all profiles
    st.markdown("### Profiles in This Subfamily")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.dataframe(
        sub_df[[COL_PROFILE, COL_PATH, COL_GRADE]],
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
