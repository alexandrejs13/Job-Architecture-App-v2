# ==========================================================
# HEADER — SIG Standard (DO NOT CHANGE)
# ==========================================================
import streamlit as st
import base64
import os

def load_icon_png(path):
    if not os.path.exists(path):
        return "" 
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/people_employees.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Family Micro-Analysis
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)


# ==========================================================
# PAGE — Family Micro Analysis (ENGLISH VERSION)
# ==========================================================

import pandas as pd
import altair as alt

# SIG Palette
SIG_SKY = "#145EFC"
SIG_SPARK = "#DCA0FF"
SIG_FOREST = "#167665"
SIG_MOSS = "#C8C84E"
SIG_BLACK = "#000000"
SIG_SAND1 = "#F2EFEB"
SIG_PALETTE = [SIG_SKY, SIG_SPARK, SIG_BLACK, SIG_FOREST, SIG_MOSS]

# Load dataset
@st.cache_data
def load_job_profile():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_job_profile()

# Column mapping (from your real Excel)
COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_BAND = "Career Band Short"
COL_LEVEL = "Career Level"
COL_GRADE = "Global Grade"

# ==========================================================
# UI — Select Job Family
# ==========================================================

st.markdown("### Select a Job Family to explore")

families = sorted(df[COL_FAMILY].unique())
family_selected = st.selectbox("Job Family:", families)

family_df = df[df[COL_FAMILY] == family_selected]

# ==========================================================
# PREMIUM METRICS BLOCK — SLIM CARDS
# ==========================================================

st.markdown("""
<style>
.card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
    margin-top: 14px;
}
.card-sig {
    background-color: #F2EFEB;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #E6E0D8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    text-align: center;
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card-title {
    font-size: 17px;
    font-weight: 600;
    color: #000;
    margin-bottom: 4px;
}
.card-value {
    font-size: 34px;
    font-weight: 800;
    color: #145EFC;
    margin-top: -2px;
}
</style>
""", unsafe_allow_html=True)

sub_count = family_df[COL_SUBFAMILY].nunique()
profile_count = family_df[COL_PROFILE].nunique()
path_count = family_df[COL_CAREER_PATH].nunique()
band_count = family_df[COL_BAND].nunique()
grade_count = family_df[COL_GRADE].nunique()

st.markdown("## Overview")

st.markdown(f"""
<div class='card-grid'>
    <div class='card-sig'><div class='card-title'>Subfamilies</div><div class='card-value'>{sub_count}</div></div>
    <div class='card-sig'><div class='card-title'>Job Profiles</div><div class='card-value'>{profile_count}</div></div>
    <div class='card-sig'><div class='card-title'>Career Paths</div><div class='card-value'>{path_count}</div></div>

    <div class='card-sig'><div class='card-title'>Career Bands</div><div class='card-value'>{band_count}</div></div>
    <div class='card-sig'><div class='card-title'>Global Grades</div><div class='card-value'>{grade_count}</div></div>
    <div class='card-sig'><div class='card-title'>Career Levels</div><div class='card-value'>{family_df[COL_LEVEL].nunique()}</div></div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# DONUT — Profiles by Subfamily
# ==========================================================

st.markdown("## Distribution of Job Profiles by Subfamily")

sub_dist = (
    family_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtde")
    .sort_values("Qtde", ascending=False)
)

colA, colB = st.columns([1,1])

with colA:
    donut = alt.Chart(sub_dist).mark_arc(
        innerRadius=70,
        outerRadius=130
    ).encode(
        theta="Qtde:Q",
        color=alt.Color(f"{COL_SUBFAMILY}:N", scale=alt.Scale(range=SIG_PALETTE), legend=None),
        tooltip=[COL_SUBFAMILY, "Qtde"]
    )
    st.altair_chart(donut, use_container_width=False)

with colB:
    st.markdown("### ")
    st.markdown("### ")
    for i, row in sub_dist.iterrows():
        color = SIG_PALETTE[i % len(SIG_PALETTE)]
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <div style="width:14px; height:14px; background:{color}; border-radius:50%;"></div>
            <span style="font-size:16px; font-weight:600;">{row[COL_SUBFAMILY]}</span>
            <span style="margin-left:auto; background:{color}; color:white; padding:2px 10px; border-radius:12px; font-size:13px;">
                {row['Qtde']}
            </span>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# BARS — Career Path, Band, Grade
# ==========================================================

st.markdown("## Structure Distribution")

# Career Paths
path_dist = (
    family_df.groupby(COL_CAREER_PATH)[COL_PROFILE]
    .nunique()
    .reset_index(name="Profiles")
    .sort_values("Profiles", ascending=False)
)

st.markdown("### Job Profiles per Career Path")
bar_path = alt.Chart(path_dist).mark_bar(
    cornerRadiusTopLeft=6,
    cornerRadiusBottomLeft=6
).encode(
    x="Profiles:Q",
    y=alt.Y(f"{COL_CAREER_PATH}:N", sort='-x'),
    color=alt.Color("Profiles:Q", scale=alt.Scale(range=[SIG_SPARK, SIG_SKY]), legend=None),
)
st.altair_chart(bar_path, use_container_width=True)

# Career Bands
band_dist = (
    family_df.groupby(COL_BAND)[COL_PROFILE]
    .nunique()
    .reset_index(name="Profiles")
    .sort_values("Profiles", ascending=False)
)

st.markdown("### Job Profiles per Career Band")
bar_band = alt.Chart(band_dist).mark_bar(
    cornerRadiusTopLeft=6,
    cornerRadiusBottomLeft=6
).encode(
    x="Profiles:Q",
    y=alt.Y(f"{COL_BAND}:N", sort='-x'),
    color=alt.Color("Profiles:Q", scale=alt.Scale(range=[SIG_MOSS, SIG_SKY]), legend=None),
)
st.altair_chart(bar_band, use_container_width=True)

# Grades
grade_dist = (
    family_df.groupby(COL_GRADE)[COL_PROFILE]
    .nunique()
    .reset_index(name="Profiles")
    .sort_values(COL_GRADE)
)

st.markdown("### Job Profiles per Global Grade")
bar_grade = alt.Chart(grade_dist).mark_bar(
    cornerRadiusTopLeft=6,
    cornerRadiusBottomLeft=6
).encode(
    x="Profiles:Q",
    y=alt.Y(f"{COL_GRADE}:N", sort='-x'),
    color=alt.Color("Profiles:Q", scale=alt.Scale(range=[SIG_FOREST, SIG_SKY]), legend=None),
)
st.altair_chart(bar_grade, use_container_width=True)

# ==========================================================
# JOB PROFILE LIST
# ==========================================================

st.markdown("## Complete Job Profile Listing")
st.dataframe(
    family_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_BAND, COL_LEVEL, COL_GRADE]],
    use_container_width=True
)

# ==========================================================
# INSIGHTS — AI-STYLE
# ==========================================================

st.markdown("## Insights")

ins = []

if sub_count <= 2:
    ins.append("The family has a limited subfamily structure, which may restrict career mobility.")

if band_count == 1:
    ins.append("Job Profiles are concentrated in a single Career Band, suggesting limited vertical progression.")

if family_df[COL_LEVEL].nunique() <= 2:
    ins.append("Career Levels show a narrow progression range, indicating a flat structure.")

if path_count == 1:
    ins.append("Only one Career Path exists, reducing job diversification.")

if len(ins) == 0:
    st.success("This Job Family shows healthy structural diversity across subfamilies, bands, grades and career paths.")
else:
    for item in ins:
        st.warning(f"⚠ {item}")
