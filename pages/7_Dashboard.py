# ==========================================================
# DASHBOARD — VERSÃO MINIMALISTA, MODERNA E ELEGANTE (SIG)
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
# CORES SIG (minimalistas)
# ==========================================================
SIG_COLORS = [
    "#145efc",
    "#dca0ff",
    "#000000",
    "#167865",
    "#f5f073",
]


# ==========================================================
# IMPORTAÇÃO DO ARQUIVO
# ==========================================================
df = pd.read_excel("data/Job Profile.xlsx")
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

COL_FAMILY = "job_family"
COL_SUBFAMILY = "sub_job_family"
COL_PROFILE = "job_profile"
COL_GRADE = "global_grade"
COL_CAREER_PATH = "career_path"


# ==========================================================
# FUNÇÕES DE GRÁFICOS MINIMALISTAS
# ==========================================================

def sig_donut(df, category, value):
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=90, stroke="#FFFFFF", strokeWidth=1)
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
        .mark_bar(size=22, cornerRadiusTopLeft=4, cornerRadiusBottomLeft=4)
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
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    for i, row in df.iterrows():
        st.markdown(
            f"""
            <div style="
                display:flex; 
                justify-content:space-between;
                align-items:center;
                padding:6px 10px;
                margin-bottom:6px;
                background:#FAFAFA;
                border:1px solid #E6E6E6;
                border-radius:6px;
            ">
                <div style="font-size:14px; color:#333;">{row[category]}</div>
                <div style="
                    background:{SIG_COLORS[i % len(SIG_COLORS)]};
                    padding:3px 10px;
                    border-radius:10px;
                    color:white;
                    font-weight:600;
                    font-size:12px;
                ">
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
# TAB 1 — OVERVIEW (EDITORIAL SIG)
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # ======================================================
    # CARDS — 2 LINHAS (ELEGANTES)
    # ======================================================
    kpis_line1 = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    kpis_line2 = {
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Avg Profiles / Family": round(df[COL_PROFILE].nunique() / df[COL_FAMILY].nunique(), 1),
        "Avg Profiles / Subfamily": round(df[COL_PROFILE].nunique() / df[COL_SUBFAMILY].nunique(), 1),
    }

    # ---- Linha 1 ----
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis_line1.items():
        st.markdown(
            f"""
            <div class='sig-card-minimal'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # ---- Linha 2 ----
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis_line2.items():
        st.markdown(
            f"""
            <div class='sig-card-minimal'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Separador
    st.markdown("<hr style='border:0.5px solid #E6E6E6; margin:36px 0;'>", unsafe_allow_html=True)


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

    colA, colB = st.columns([1.2, 0.8])

    with colA:
        st.altair_chart(sig_donut(df_sub, COL_FAMILY, "Count"),
                        use_container_width=True)

    with colB:
        sig_legend(df_sub, COL_FAMILY, "Count")

    st.markdown("<hr style='border:0.5px solid #E6E6E6; margin:36px 0;'>", unsafe_allow_html=True)


    # ======================================================
    # BAR — Profiles per Subfamily
    # ======================================================
    st.markdown("### Profiles per Subfamily")

    df_prof = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colL, colR = st.columns([1.2, 0.8])

    with colL:
        st.altair_chart(sig_bar(df_prof, COL_SUBFAMILY, "Count"),
                        use_container_width=True)

    with colR:
        sig_legend(df_prof, COL_SUBFAMILY, "Count")



# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS (EDITORIAL SIG)
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].dropna().unique())
    selected = st.selectbox("Select a Job Family:", families)

    df_sel = df[df[COL_FAMILY] == selected]

    # ---- Cards ----
    kpis_family_line1 = {
        "Subfamilies": df_sel[COL_SUBFAMILY].nunique(),
        "Job Profiles": df_sel[COL_PROFILE].nunique(),
        "Global Grades": df_sel[COL_GRADE].nunique(),
    }

    kpis_family_line2 = {
        "Career Paths": df_sel[COL_CAREER_PATH].nunique(),
    }

    # Linha 1
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis_family_line1.items():
        st.markdown(
            f"""
            <div class='sig-card-minimal'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # Linha 2
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis_family_line2.items():
        st.markdown(
            f"""
            <div class='sig-card-minimal'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:0.5px solid #E6E6E6; margin:36px 0;'>", unsafe_allow_html=True)


    # ---- Gráfico minimalista ----
    st.markdown("### Profiles per Subfamily (Selected Family)")

    df_sel_prof = (
        df_sel.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(sig_bar(df_sel_prof, COL_SUBFAMILY, "Count"),
                    use_container_width=True)
