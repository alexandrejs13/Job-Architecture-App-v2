# ==========================================================
# DASHBOARD — SIG OFFICIAL STYLE (Overview + Micro-Analysis)
# ==========================================================

import streamlit as st
import base64
import os
import pandas as pd
import altair as alt

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# ICON (PADRÃO SIG)
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:8px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:16px; margin-bottom:30px;">
""", unsafe_allow_html=True)

# ==========================================================
# PALETA SIG
# ==========================================================
SIG_SKY = "#145efc"
SIG_SPARK = "#dca0ff"
SIG_FOREST = "#00493b"
SIG_FOREST2 = "#167865"
SIG_MOSS = "#ffdf73"
SIG_MOSS2 = "#c0b846"
SIG_SAND1 = "#f2efeb"

# ==========================================================
# LOAD DATA
# ==========================================================
df = pd.read_excel("data/Job Profile.xlsx")
df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

COL_FAMILY = "job_family"
COL_SUB = "sub_job_family"
COL_PROFILE = "job_profile"
COL_GRADE = "global_grade"
COL_CAREER = "career_path"

# ==========================================================
# CARD STYLE SIG SAND1
# ==========================================================
def sig_card(title, value):
    return f"""
    <div style="
        background:{SIG_SAND1};
        padding:18px 26px;
        border-radius:10px;
        font-family:Arial, sans-serif;
        min-width:200px;
    ">
        <div style="font-size:14px; font-weight:600; color:#000;">{title}</div>
        <div style="font-size:30px; font-weight:700; color:{SIG_SKY}; margin-top:4px;">
            {value}
        </div>
    </div>
    """

# ==========================================================
# GRÁFICO DONUT (SIG COLORS)
# ==========================================================
def donut_chart(df, category, value, title=None):

    color_scale = alt.Scale(
        range=[SIG_SKY, SIG_SPARK, SIG_FOREST, SIG_FOREST2, SIG_MOSS, SIG_MOSS2]
    )

    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=60, stroke="white")
        .encode(
            theta=alt.Theta(value, type="quantitative"),
            color=alt.Color(category, scale=color_scale, legend=None),
            tooltip=[category, value]
        )
        .properties(width=380, height=380)
    )

    return chart


# ==========================================================
# GRÁFICO BARRA HORIZONTAL
# ==========================================================
def bar_chart(df, category, value):
    return (
        alt.Chart(df)
        .mark_bar(color=SIG_SKY, size=22)
        .encode(
            x=alt.X(f"{value}:Q", title=""),
            y=alt.Y(category, sort='-x', title=""),
            tooltip=[category, value]
        )
        .properties(height=380)
        .configure_view(strokeWidth=0)
    )


# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])

# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # KPIs solicitados
    c1, c2, c3, c4, c5 = st.columns(5)

    kpi_data = [
        ("Families", df[COL_FAMILY].nunique()),
        ("Subfamilies", df[COL_SUB].nunique()),
        ("Job Profiles", df[COL_PROFILE].nunique()),
        ("Grades", df[COL_GRADE].nunique()),
        ("Career Paths", df[COL_CAREER].nunique()),
    ]

    for col, (title, value) in zip([c1, c2, c3, c4, c5], kpi_data):
        col.markdown(sig_card(title, value), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # DONUT — Subfamily per Family
    # ------------------------------------------------------
    st.markdown("### Subfamilies per Family")

    df_donut = (
        df.groupby(COL_FAMILY)[COL_SUB]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(donut_chart(df_donut, COL_FAMILY, "Count"), use_container_width=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # BAR — Profiles per Subfamily
    # ------------------------------------------------------
    st.markdown("### Profiles per Subfamily")

    df_bar = (
        df.groupby(COL_SUB)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(bar_chart(df_bar, COL_SUB, "Count"), use_container_width=True)


# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].dropna().unique())
    selected = st.selectbox("Select a Family:", families)

    df_sel = df[df[COL_FAMILY] == selected]

    c1, c2, c3, c4, c5 = st.columns(5)

    kpi2_data = [
        ("Families", df_sel[COL_FAMILY].nunique()),
        ("Subfamilies", df_sel[COL_SUB].nunique()),
        ("Job Profiles", df_sel[COL_PROFILE].nunique()),
        ("Grades", df_sel[COL_GRADE].nunique()),
        ("Career Paths", df_sel[COL_CAREER].nunique()),
    ]

    for col, (title, value) in zip([c1, c2, c3, c4, c5], kpi2_data):
        col.markdown(sig_card(title, value), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------- RETORNO AO VISUAL DA SUA VERSÃO FAVORITA ----------
    st.markdown("### Profiles per Subfamily (Selected Family)")

    df_sel_bar = (
        df_sel.groupby(COL_SUB)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(bar_chart(df_sel_bar, COL_SUB, "Count"), use_container_width=True)

