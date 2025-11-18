# ==========================================================
# DASHBOARD — VERSÃO FINAL (Página 7)
# ==========================================================

import streamlit as st
import base64
import os
import pandas as pd
import altair as alt

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# FUNÇÃO — CARREGAR ÍCONE PNG INLINE
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER PADRÃO SIG
# ==========================================================
icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)



# ==========================================================
# CORES SIG
# ==========================================================
SIG_COLORS = [
    "#145efc",  # Sky
    "#dca0ff",  # Spark lilac
    "#000000",  # Black
    "#167865",  # Forest 2
    "#f5f073",  # Moss 1
]



# ==========================================================
# IMPORTAÇÃO DO ARQUIVO
# ==========================================================
df = pd.read_excel("data/Job Profile.xlsx")

# Normaliza nomes de colunas
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Mapeamento fixo
COL_FAMILY = "job_family"
COL_SUBFAMILY = "sub_job_family"
COL_PROFILE = "job_profile"
COL_GRADE = "global_grade"
COL_BAND = "career_band"
COL_CAREER_PATH = "career_path"



# ==========================================================
# FUNÇÕES DE GRÁFICOS SIG
# ==========================================================

def sig_donut(df, category, value):
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=70)
        .encode(
            theta=alt.Theta(f"{value}:Q"),
            color=alt.Color(
                category,
                scale=alt.Scale(range=SIG_COLORS),
                legend=None
            ),
            tooltip=[category, value]
        )
    )


def sig_bar(df, category, value):
    return (
        alt.Chart(df)
        .mark_bar(size=28)
        .encode(
            x=alt.X(f"{value}:Q", title=""),
            y=alt.Y(category, sort='-x', title=""),
            color=alt.Color(
                category,
                scale=alt.Scale(range=SIG_COLORS),
                legend=None
            ),
            tooltip=[category, value]
        )
    )


def sig_legend(df, category, value):
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    for i, row in df.iterrows():
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between;
                        padding:6px 10px; margin-bottom:6px;
                        background:#f5f5f5; border-radius:8px;">
                <div style="font-size:15px; font-weight:500;">{row[category]}</div>
                <div style="background:{SIG_COLORS[i % len(SIG_COLORS)]};
                            padding:4px 10px; border-radius:12px;
                            color:white; font-weight:600;">
                    {row[value]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )



# ==========================================================
# ABAS — Overview / Family Micro-Analysis
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])



# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # ------------ CARDS -------------
    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Career Bands": df[COL_BAND].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
        "Avg Profiles / Family": round(df[COL_PROFILE].nunique() / df[COL_FAMILY].nunique(), 1),
        "Avg Profiles / Subfamily": round(df[COL_PROFILE].nunique() / df[COL_SUBFAMILY].nunique(), 1),
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)



    # ======================================================
    # DONUT — Subfamilies per Family
    # ======================================================
    st.markdown("### Subfamilies per Family")

    df_sub = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colA, colB = st.columns([1, 1])

    with colA:
        st.altair_chart(sig_donut(df_sub, COL_FAMILY, "Count"),
                        use_container_width=True)

    with colB:
        sig_legend(df_sub, COL_FAMILY, "Count")



    # ======================================================
    # BAR — Profiles per Subfamily
    # ======================================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Profiles per Subfamily")

    df_prof = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colL, colR = st.columns([1.2, 1])

    with colL:
        st.altair_chart(sig_bar(df_prof, COL_SUBFAMILY, "Count"),
                        use_container_width=True)

    with colR:
        sig_legend(df_prof, COL_SUBFAMILY, "Count")



# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].dropna().unique())
    selected = st.selectbox("Select a Job Family:", families)

    df_sel = df[df[COL_FAMILY] == selected]

    # ---------- Cards ----------
    kpis_family = {
        "Subfamilies": df_sel[COL_SUBFAMILY].nunique(),
        "Job Profiles": df_sel[COL_PROFILE].nunique(),
        "Career Paths": df_sel[COL_CAREER_PATH].nunique(),
        "Career Bands": df_sel[COL_BAND].nunique(),
        "Global Grades": df_sel[COL_GRADE].nunique(),
        "Career Levels": df_sel[COL_GRADE].nunique(),
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis_family.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ----- Gráfico Profiles per Subfamily -----
    st.markdown("### Profiles per Subfamily (Selected Family)")

    df_sel_prof = (
        df_sel.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(sig_bar(df_sel_prof, COL_SUBFAMILY, "Count"),
                    use_container_width=True)
