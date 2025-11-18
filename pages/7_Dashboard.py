import streamlit as st
import pandas as pd
import altair as alt
import os, base64

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
# GLOBAL CSS — SIG DESIGN
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

.sig-divider {{
    border: none;
    border-bottom: 1px solid #e2e2e2;
    margin: 28px 0 20px 0;
}}

.chart-card {{
    background: #ffffff;
    border-radius: 14px;
    padding: 20px 26px;
    border: 1px solid #e4e4e4;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 26px;
}}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HEADER SIG (PADRÃO)
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

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
tab1, tab2 = st.tabs(["📊 Overview", "🔎 Family Micro-Analysis"])


# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Executive Job Architecture Overview")

    # ========== KPIs HORIZONTAIS REAL OFICIAL ==========
    kpis = {
        "Job Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_PATH].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    cols = st.columns(len(kpis))

    for col, (label, number) in zip(cols, kpis.items()):
        col.markdown(f"""
            <div style="
                background:#ffffff;
                border-radius:12px;
                padding:14px 18px;
                border:1px solid #e4e4e4;
                box-shadow:0 2px 8px rgba(0,0,0,0.04);
                height:90px;
                display:flex;
                flex-direction:column;
                justify-content:center;
            ">
                <div style="font-size:13px; font-weight:600; color:#727272;">
                    {label}
                </div>
                <div style="font-size:26px; font-weight:700; margin-top:4px; color:#145efc;">
                    {number}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='sig-divider'>", unsafe_allow_html=True)

    
    # --------------------- Grade Distribution --------------------------
    st.markdown("### Grade Distribution (Structure Complexity)")

    grade_df = (
        df.groupby(COL_GRADE)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values(COL_GRADE)
    )

    chart = (
        alt.Chart(grade_df)
        .mark_bar(size=26)
        .encode(
            x="Count:Q",
            y=alt.Y(f"{COL_GRADE}:N", sort='-x'),
            color=alt.value("#145efc"),
            tooltip=[COL_GRADE, "Count"]
        )
        .properties(height=40 * len(grade_df))
    )

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)



# ==========================================================
# TAB 2 — FAMILY MICRO ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family & Subfamily Deep Dive")

    families = sorted(df[COL_FAMILY].unique())
    selected_family = st.selectbox("Select a Family:", families)

    subfamilies = sorted(df[df[COL_FAMILY] == selected_family][COL_SUBFAMILY].unique())
    selected_subfamily = st.selectbox("Select a Subfamily:", subfamilies)

    sub_df = df[
        (df[COL_FAMILY] == selected_family) &
        (df[COL_SUBFAMILY] == selected_subfamily)
    ]

    # ========== KPIs HORIZONTAIS (SUBFAMILY) ==========
    sub_kpis = {
        "Profiles": sub_df[COL_PROFILE].nunique(),
        "Grades": sub_df[COL_GRADE].nunique(),
    }

    cols = st.columns(len(sub_kpis))

    for col, (label, number) in zip(cols, sub_kpis.items()):
        col.markdown(f"""
            <div style="
                background:#ffffff;
                border-radius:12px;
                padding:14px 18px;
                border:1px solid #e4e4e4;
                box-shadow:0 2px 8px rgba(0,0,0,0.04);
                height:90px;
                display:flex;
                flex-direction:column;
                justify-content:center;
            ">
                <div style="font-size:13px; font-weight:600; color:#727272;">
                    {label}
                </div>
                <div style="font-size:26px; font-weight:700; margin-top:4px; color:#145efc;">
                    {number}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='sig-divider'>", unsafe_allow_html=True)


    # --------------------- Grade Spread --------------------------
    st.markdown("### Grade Spread")

    g_spread = (
        sub_df.groupby(COL_GRADE)[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
        .sort_values(COL_GRADE)
    )

    bars = (
        alt.Chart(g_spread)
        .mark_bar(size=26)
        .encode(
            x="Profiles:Q",
            y=alt.Y(f"{COL_GRADE}:N", sort='-x'),
            color=alt.value("#145efc"),
            tooltip=[COL_GRADE, "Profiles"]
        )
    )

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.altair_chart(bars, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------- Data Table --------------------------
    st.markdown("### Profiles in Subfamily")

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.dataframe(sub_df[[COL_PROFILE, COL_PATH, COL_GRADE]], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
