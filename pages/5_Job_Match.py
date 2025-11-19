# ==========================================================
# 5_Job_Match.py — PÁGINA FINAL DO JOB MATCH (VERSÃO FECHADA)
# ==========================================================

import streamlit as st
import pandas as pd
import base64
import os

from match_engine import compute_job_match
from html_renderer import render_job_description

# ----------------------------------------------------------
# PAGE CONFIG SIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# LOAD ICON (PADRÃO SIG)
# ----------------------------------------------------------
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

# ----------------------------------------------------------
# HEADER (PADRÃO DAS OUTRAS PÁGINAS)
# ----------------------------------------------------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">Job Match</h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# GLOBAL CSS - SIG STYLE
# ----------------------------------------------------------
st.markdown("""
<style>

.main > div {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 20px;
    padding-right: 20px;
}

/* Título vermelho quando faltar */
.error-title {
    color: #C62828 !important;
    font-weight: 700;
}

/* Borda vermelha */
.error-border {
    border: 2px solid #C62828 !important;
    border-radius: 6px !important;
}

/* BOTÃO AZUL SIG */
.generate-btn {
    background-color: #145efc;
    color: #fff !important;
    border-radius: 12px;
    padding: 12px 26px;
    font-size: 18px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    display: inline-block;
}

/* CARD SUPERIOR */
.card {
    background: #f4f1ec;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 30px;
}

.job-title {
    font-size: 32px;
    font-weight: 800;
}

.gg {
    font-size: 20px;
    font-weight: 600;
    color: #145efc;
    margin-bottom: 14px;
}

/* SECTION TITLE */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 42px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-text {
    font-size: 17px;
    line-height: 1.48;
    color: #333;
    margin-bottom: 28px;
}

.icon svg {
    width: 28px;
    height: 28px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD SPREADSHEET (VERSÃO DEFINITIVA)
# ----------------------------------------------------------
excel_path = "data/Job Profile.xlsx"

if not os.path.exists(excel_path):
    st.error(f"""
    ❌ **Arquivo não encontrado:**

    `{excel_path}`

    Coloque o arquivo dentro da pasta:
    `/Job-Architecture-App/data/Job Profile.xlsx`
    """)
    st.stop()

df_profiles = pd.read_excel(excel_path).fillna("")

rename_map = {
    "Job Family": "job_family",
    "Sub Job Family": "sub_job_family",
    "Job Title": "job_title",
    "GG": "gg",
    "Career Path": "career_path",
    "Full Job Code": "full_job_code",
    "Sub Job Family Description": "sub_job_family_description",
    "Job Profile Description": "job_profile_description",
    "Career Band Description": "career_band_description",
    "Role Description": "role_description",
    "Grade Differentiator": "grade_differentiator",
    "Qualifications": "qualifications",
    "Specific parameters / KPIs": "specific_parameters_kpis",
    "Competencies 1": "competencies_1",
    "Competencies 2": "competencies_2",
    "Competencies 3": "competencies_3",
}

df_profiles.rename(columns=rename_map, inplace=True)

# ----------------------------------------------------------
# FORM INPUTS (COM CORREÇÃO DE ERROS)
# ----------------------------------------------------------
form = {}
errors = {}

def required_select(label, options):
    selected = st.selectbox(label, ["Choose option"] + options, key=label)

    missing = (selected == "Choose option")
    errors[label] = missing

    # highlight
    title_class = "error-title" if missing else ""
    box_class = "error-border" if missing else ""

    st.markdown(f"""
    <style>
    div[data-testid="stSelectbox"][key="{label}"] .stSelectbox {{
        border-radius: 6px;
    }}
    </style>
    """, unsafe_allow_html=True)

    form[label] = selected
    return selected


# ----------------------------------------------------------
# JOB FAMILY BLOCK
# ----------------------------------------------------------
st.markdown("""<h3 style="margin-bottom:4px; font-size:24px; font-weight:700;">Job Family Information</h3>
<div style="height:1px; background:#ddd; margin-bottom:18px;"></div>
""", unsafe_allow_html=True)

colA, colB = st.columns(2)

with colA:
    job_fams = sorted(df_profiles["job_family"].unique().tolist())
    job_family = required_select("Job Family", job_fams)

with colB:
    if job_family == "Choose option":
        sub_job_family = st.selectbox("Sub Job Family", ["Choose option"])
        errors["Sub Job Family"] = True
    else:
        subs = df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"].unique().tolist()
        sub_job_family = required_select("Sub Job Family", sorted(subs))

# ----------------------------------------------------------
# SEÇÃO 1 — STRATEGIC IMPACT & SCOPE
# ----------------------------------------------------------
st.markdown("""<h3 style="margin-bottom:4px; font-size:24px; font-weight:700;">Strategic Impact & Scope</h3>
<div style="height:1px; background:#ddd; margin-bottom:18px;"></div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    job_category = required_select("Job Category", ["Executive","Manager","Professional","Technical Support","Business Support","Production"])
    geo_scope = required_select("Geographic Scope", ["Local","Regional","Multi-country","Global"])
    org_impact = required_select("Organizational Impact", ["Team","Department / Subfunction","Function","Business Unit","Enterprise-wide"])

with c2:
    autonomy = required_select("Autonomy Level", ["Close supervision","Regular guidance","Independent","Sets direction for others","Defines strategy"])
    knowledge_depth = required_select("Knowledge Depth", ["Entry-level knowledge","Applied knowledge","Advanced expertise","Recognized expert","Thought leader"])
    operational_complexity = required_select("Operational Complexity", ["Stable operations","Some variability","Complex operations","High-variability environment"])

with c3:
    experience = required_select("Experience Level", ["< 2 years","2–5 years","5–10 years","10–15 years","15+ years"])
    education = required_select("Education Level", ["High School","Technical Degree","Bachelor’s","Post-graduate","Master’s","Doctorate"])

# ----------------------------------------------------------
# BOTÃO GERAR — AZUL, ESQUERDA, 1 LINHA
# ----------------------------------------------------------
left, _, _ = st.columns([1,6,1])
with left:
    generate = st.button("Generate Job Match Description", key="generate", help="Generate", type="primary")

# ----------------------------------------------------------
# EXECUTAR MATCH
# ----------------------------------------------------------
if generate:

    missing = [k for k, v in errors.items() if v]

    if missing:
        st.error("⚠️ Please complete all required fields.")
    else:
        form_inputs = {
            "job_family": job_family,
            "sub_job_family": sub_job_family,
            "job_category": job_category,
            "geo_scope": geo_scope,
            "org_impact": org_impact,
            "autonomy": autonomy,
            "knowledge_depth": knowledge_depth,
            "operational_complexity": operational_complexity,
            "experience": experience,
            "education": education,
        }

        best = compute_job_match(form_inputs, df_profiles)

        if best:
            html = render_job_description(best["row"], best["final_score"])
            st.markdown(html, unsafe_allow_html=True)
