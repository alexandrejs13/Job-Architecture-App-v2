# ==========================================================
# DASHBOARD — ULTRA MINIMALISTA SIG (VERSÃO DEFINITIVA)
# ==========================================================

import streamlit as st
import base64
import os
import pandas as pd
import altair as alt

# ==========================================================
# CONFIG PÁGINA
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# LOAD ICON
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER SIG PADRÃO
# ==========================================================
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
# CORES SIG
# ==========================================================
SIG_BLUE = "#145EFC"
GRAY_LABEL = "#666"
GRAY_LINE = "#E6E6E6"

# ==========================================================
# LOAD DATA
# ==========================================================
df = pd.read_excel("data/Job Profile.xlsx")
df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

COL_FAMILY = "job_family"
COL_SUBFAMILY = "sub_job_family"
COL_PROFILE = "job_profile"
COL_GRADE = "global_grade"
COL_CAREER_PATH = "career_path"

# ==========================================================
# FUNÇÃO — BAR MINIMALISTA
# ==========================================================
def minimal_bar(df, category, value):
    return (
        alt.Chart(df)
        .mark_bar(size=22, color=SIG_BLUE)
        .encode(
            x=alt.X(f"{value}:Q", title="", axis=alt.Axis(grid=False)),
            y=alt.Y(category, sort='-x', title="", axis=alt.Axis(labelLimit=220)),
            tooltip=[category, value]
        )
        .properties(height=380)
        .configure_view(strokeWidth=0)
    )

# ==========================================================
# CARD FLAT MINIMALISTA (sem caixa)
# ==========================================================
def card(title, value):
    return f"""
        <div style="padding:6px 0 10px 0;">
            <div style="font-size:13px; color:{GRAY_LABEL}; margin-bottom:2px;">{title}</div>
            <div style="font-size:28px; font-weight:600; color:{SIG_BLUE};">{value}</div>
        </div>
    """

# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])


# ==========================================================
# OVERVIEW — MINIMALISTA PREMIUM
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # ---------------- LINE 1 — KPIs PRINCIPAIS ----------------
    kpi1 = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Grades": df[COL_GRADE].nunique(),
    }

    c1, c2, c3, c4 = st.columns(4)
    for col, (title, value) in zip([c1, c2, c3, c4], kpi1.items()):
        with col:
            st.markdown(card(title, value), unsafe_allow_html=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # ---------------- LINE 2 — KPIs DERIVADOS ----------------
    kpi2 = {
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Avg Profiles / Family": round(df[COL_PROFILE].nunique() / df[COL_FAMILY].nunique(), 1),
        "Avg Profiles / Subfamily": round(df[COL_PROFILE].nunique() / df[COL_SUBFAMILY].nunique(), 1),
    }

    c5, c6, c7 = st.columns(3)
    for col, (title, value) in zip([c5, c6, c7], kpi2.items()):
        with col:
            st.markdown(card(title, value), unsafe_allow_html=True)

    # ------- separador minimalista -------
    st.markdown(f"<hr style='border:0.5px solid {GRAY_LINE}; margin:34px 0;'>",
                unsafe_allow_html=True)

    # ======================================================
    # BAR — Profiles per Family (limpo e elegante)
    # ======================================================
    st.markdown("### Profiles per Family")

    df_family = (
        df.groupby(COL_FAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(minimal_bar(df_family, COL_FAMILY, "Count"), use_container_width=True)

    st.markdown(f"<hr style='border:0.5px solid {GRAY_LINE}; margin:34px 0;'>",
                unsafe_allow_html=True)

    # ======================================================
    # BAR — Profiles per Subfamily
    # ======================================================
    st.markdown("### Profiles per Subfamily")

    df_sub = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(minimal_bar(df_sub, COL_SUBFAMILY, "Count"), use_container_width=True)



# ==========================================================
# FAMILY MICRO-ANALYSIS — MINIMALISTA
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].dropna().unique())
    selected = st.selectbox("Select a Family:", families)

    df_sel = df[df[COL_FAMILY] == selected]

    # ---------------- KPIs SELECIONADOS ----------------
    k_sel_1 = {
        "Subfamilies": df_sel[COL_SUBFAMILY].nunique(),
        "Profiles": df_sel[COL_PROFILE].nunique(),
        "Grades": df_sel[COL_GRADE].nunique(),
    }

    c1, c2, c3 = st.columns(3)
    for col, (title, value) in zip([c1, c2, c3], k_sel_1.items()):
        with col:
            st.markdown(card(title, value), unsafe_allow_html=True)

    c4 = st.columns(1)[0]
    c4.markdown(card("Career Paths", df_sel[COL_CAREER_PATH].nunique()),
                unsafe_allow_html=True)

    st.markdown(f"<hr style='border:0.5px solid {GRAY_LINE}; margin:34px 0;'>",
                unsafe_allow_html=True)

    # ---------- BAR — Profiles per Subfamily (dentro da família) ----------
    st.markdown("### Profiles per Subfamily (Selected Family)")

    df_sel_prof = (
        df_sel.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    st.altair_chart(minimal_bar(df_sel_prof, COL_SUBFAMILY, "Count"),
                    use_container_width=True)
