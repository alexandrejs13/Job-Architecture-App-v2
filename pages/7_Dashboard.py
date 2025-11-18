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
# FUNÇÃO PARA CARREGAR PNG INLINE
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER — padrão SIG (NÃO ALTERAR)
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


# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_job_profile():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_job_profile()

COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_BAND = "Career Band Short"
COL_GRADE = "Global Grade"
COL_LEVEL = "Career Level"


# ==========================================================
# GLOBAL CSS — CARTÕES PADRÃO SIG (SLIM)
# ==========================================================
st.markdown("""
<style>

section.main > div {
    max-width: 1180px;
    padding-left: 12px;
    padding-right: 12px;
}

/* GRID com cards pequenos */
.sig-card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
}

.sig-card {
    background: #F2EFEB;
    padding: 12px 16px;
    border-radius: 14px;
    border: 1px solid #E5E0D8;
    height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.sig-card-title {
    font-size: 14px;
    font-weight: 600;
    color: #000;
    margin-bottom: 4px;
}

.sig-card-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC;
}

/* Para limpar margens entre blocos */
.block-space { margin-top: 28px; }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])



# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # INDICADORES
    total_families = df[COL_FAMILY].nunique()
    total_subfamilies = df[COL_SUBFAMILY].nunique()
    total_profiles = df[COL_PROFILE].nunique()
    total_paths = df[COL_CAREER_PATH].nunique()
    total_bands = df[COL_BAND].nunique()
    total_grades = df[COL_GRADE].nunique()

    overview_cards = {
        "Families": total_families,
        "Subfamilies": total_subfamilies,
        "Job Profiles": total_profiles,
        "Career Paths": total_paths,
        "Career Bands": total_bands,
        "Global Grades": total_grades,
        "Avg Profiles / Family": round(total_profiles / total_families, 1),
        "Avg Profiles / Subfamily": round(total_profiles / total_subfamilies, 1),
    }

    # CARDS GRID
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in overview_cards.items():
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


    # DONUT DE DISTRIBUIÇÃO
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Distribution of Job Profiles by Family")

    dist_family = (
        df.groupby(COL_FAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
    )

    donut = alt.Chart(dist_family).mark_arc(innerRadius=65, outerRadius=120).encode(
        theta="Count:Q",
        color=alt.Color(COL_FAMILY, legend=None),
        tooltip=[COL_FAMILY, "Count"]
    )

    colA, colB = st.columns([1,1])

    with colA:
        st.altair_chart(donut, use_container_width=False)

    with colB:
        for _, row in dist_family.iterrows():
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; margin-bottom:6px; gap:10px;">
                    <div style="width:12px; height:12px; border-radius:50%; background:#145EFC;"></div>
                    <div style="font-size:15px; font-weight:600;">{row[COL_FAMILY]}</div>
                    <div style="margin-left:auto; background:#145EFC; padding:2px 10px; border-radius:10px; color:white; font-size:12px; font-weight:700;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )



# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    family_selected = st.selectbox("Select a Job Family:", families)
    family_df = df[df[COL_FAMILY] == family_selected]

    # CARDS SLIM
    metrics = {
        "Subfamilies": family_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": family_df[COL_PROFILE].nunique(),
        "Career Paths": family_df[COL_CAREER_PATH].nunique(),
        "Career Bands": family_df[COL_BAND].nunique(),
        "Global Grades": family_df[COL_GRADE].nunique(),
        "Career Levels": family_df[COL_LEVEL].nunique(),
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in metrics.items():
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


    # DONUT MICRO
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Job Profiles by Subfamily")

    sub_dist = (
        family_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
    )

    col1, col2 = st.columns([1,1])

    with col1:
        donut_sub = alt.Chart(sub_dist).mark_arc(
            innerRadius=65, outerRadius=120
        ).encode(
            theta="Count:Q",
            color=alt.Color(COL_SUBFAMILY, legend=None),
            tooltip=[COL_SUBFAMILY, "Count"]
        )
        st.altair_chart(donut_sub, use_container_width=False)

    with col2:
        for _, row in sub_dist.iterrows():
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; margin-bottom:6px; gap:10px;">
                    <div style="width:12px; height:12px; border-radius:50%; background:#167665;"></div>
                    <div style="font-size:15px; font-weight:600;">{row[COL_SUBFAMILY]}</div>
                    <div style="margin-left:auto; background:#167665; padding:2px 10px; border-radius:10px; color:white; font-size:12px; font-weight:700;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # TABELA COMPLETA
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Full Job Profile Listing")

    st.dataframe(
        family_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_BAND, COL_LEVEL, COL_GRADE]],
        use_container_width=True
    )
