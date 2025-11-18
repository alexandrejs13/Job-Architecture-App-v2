# ==========================================================
# DASHBOARD PREMIUM — SIG Job Architecture (Cards + Donuts + Bars)
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

# Paleta SIG — cores oficiais
SIG_SKY = "#145EFC"
SIG_SPARK = "#DCA0FF"
SIG_FOREST = "#167665"
SIG_MOSS = "#C8C84E"
SIG_BLACK = "#000000"
SIG_SAND1 = "#F2EFEB"
SIG_SAND2 = "#E5DFD9"

SIG_PALETTE = [SIG_SKY, SIG_SPARK, SIG_BLACK, SIG_FOREST, SIG_MOSS]

# Carregar dados
@st.cache_data
def load_job_profile():
    df = pd.read_excel("data/Job Profile.xlsx")
    return df

df = load_job_profile()

# Ajuste de colunas conforme seu arquivo real
COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_BAND = "Career Band Short"
COL_LEVEL = "Career Level"
COL_GRADE = "Global Grade"


# ==========================================================
# CARDS PREMIUM — VISÃO GERAL
# ==========================================================

st.markdown("""
<style>
.card-sig {
    background-color: #F2EFEB;
    padding: 22px;
    border-radius: 20px;
    border: 1px solid #E0DBD5;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    text-align: center;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #000000;
    margin-bottom: 6px;
}
.card-value {
    font-size: 42px;
    font-weight: 800;
    color: #145EFC;
    margin-top: -4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## Visão geral da Job Architecture")

qtd_familias = df[COL_FAMILY].nunique()
qtd_subfamilias = df[COL_SUBFAMILY].nunique()
qtd_profiles = df[COL_PROFILE].nunique()
qtd_career_paths = df[COL_CAREER_PATH].nunique()
qtd_bands = df[COL_BAND].nunique()
qtd_grades = df[COL_GRADE].nunique()

# Linha 1
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='card-sig'><div class='card-title'>Famílias</div><div class='card-value'>{qtd_familias}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card-sig'><div class='card-title'>Subfamílias</div><div class='card-value'>{qtd_subfamilias}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card-sig'><div class='card-title'>Job Profiles únicos</div><div class='card-value'>{qtd_profiles}</div></div>", unsafe_allow_html=True)

# Linha 2
col4, col5, col6 = st.columns(3)
col4.markdown(f"<div class='card-sig'><div class='card-title'>Career Paths</div><div class='card-value'>{qtd_career_paths}</div></div>", unsafe_allow_html=True)
col5.markdown(f"<div class='card-sig'><div class='card-title'>Career Bands</div><div class='card-value'>{qtd_bands}</div></div>", unsafe_allow_html=True)
col6.markdown(f"<div class='card-sig'><div class='card-title'>Grades Globais</div><div class='card-value'>{qtd_grades}</div></div>", unsafe_allow_html=True)


# ==========================================================
# DONUT PREMIUM — Distribuição de Job Profiles por Família
# ==========================================================

st.markdown("## Distribuição de Job Profiles por Família")

import altair as alt

familia_profiles = (
    df.groupby(COL_FAMILY)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtde")
    .sort_values("Qtde", ascending=False)
)

# Donut Chart Altair
donut = alt.Chart(familia_profiles).encode(
    theta=alt.Theta("Qtde:Q", stack=True),
    color=alt.Color("Job Family:N", scale=alt.Scale(range=SIG_PALETTE)),
    tooltip=["Job Family", "Qtde"]
).mark_arc(innerRadius=80, outerRadius=140)

st.altair_chart(donut, use_container_width=False)


# ==========================================================
# BARRAS PREMIUM — Top Subfamílias
# ==========================================================

st.markdown("## Top 15 Subfamílias por número de Job Profiles")

sub_profiles = (
    df.groupby([COL_SUBFAMILY])[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtde")
    .sort_values("Qtde", ascending=False)
    .head(15)
)

bar = alt.Chart(sub_profiles).mark_bar(
    cornerRadiusTopLeft=6,
    cornerRadiusTopRight=6
).encode(
    x=alt.X("Qtde:Q", title="Quantidade"),
    y=alt.Y(f"{COL_SUBFAMILY}:N", sort='-x', title="Subfamília"),
    color=alt.Color("Qtde:Q",
                    scale=alt.Scale(range=[SIG_SPARK, SIG_SKY]),
                    legend=None
                    ),
    tooltip=[COL_SUBFAMILY, "Qtde"]
)

st.altair_chart(bar, use_container_width=True)


# ==========================================================
# SEMI-GAUGE — Profundidade de Carreira (Simplificado)
# ==========================================================

st.markdown("## Profundidade média de Career Level por Família")

career_per_family = (
    df.groupby(COL_FAMILY)[COL_LEVEL]
    .nunique()
    .reset_index(name="Níveis")
    .sort_values("Níveis", ascending=False)
)

familia_sel = st.selectbox(
    "Selecione uma família:",
    career_per_family[COL_FAMILY].unique()
)

valor = career_per_family[career_per_family[COL_FAMILY] == familia_sel]["Níveis"].iloc[0]

gauge_html = f"""
<div style="width:320px; height:200px; margin:auto;">
    <svg width="320" height="200">
        <path d="M20 180 A140 140 0 0 1 300 180" stroke="#E5DFD9" stroke-width="30" fill="none"/>
        <path d="M20 180 A140 140 0 {1 if valor>3 else 0} 1 {20 + valor*35} 180"
              stroke="{SIG_SKY}" stroke-width="30" fill="none"/>
        <circle cx="160" cy="180" r="12" fill="{SIG_BLACK}"/>
        <text x="160" y="160" text-anchor="middle" font-size="34" font-weight="800" fill="{SIG_BLACK}">{valor}</text>
        <text x="160" y="185" text-anchor="middle" font-size="16" fill="{SIG_BLACK}">{familia_sel}</text>
    </svg>
</div>
"""

st.markdown(gauge_html, unsafe_allow_html=True)
