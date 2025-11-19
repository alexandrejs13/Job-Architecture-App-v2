# ==========================================================
# PAGE 5 — JOB MATCH
# ==========================================================

import streamlit as st
import pandas as pd
import base64
import os

from match_engine import compute_match
from html_renderer import render_job_match_description

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# GLOBAL CSS — SIG
# ----------------------------------------------------------
st.markdown("""
<style>

    /* ========================================== */
    /* CONTAINER PRINCIPAL */
    /* ========================================== */
    .main > div {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* ========================================== */
    /* TÍTULOS DE SEÇÕES */
    /* ========================================== */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 32px;
        margin-bottom: 4px;
    }

    .divider-line {
        height: 1px;
        background: #d9d4cd;
        margin-bottom: 18px;
    }

    /* ========================================== */
    /* BOTÃO AZUL */
    /* ========================================== */
    .blue-btn > button {
        background-color: #145efc !important;
        color: white !important;
        font-size: 18px !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        width: 420px !important;
        border: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    /* ========================================== */
    /* ERRO — LABEL ACIMA */
    /* ========================================== */
    .error-label {
        color: #d90429 !important;
        font-weight: 700;
        font-size: 15px !important;
        margin-bottom: 4px;
        display: block;
    }

    /* ========================================== */
    /* BORDA VERMELHA NA CAIXA */
    /* ========================================== */
    .error-border select, 
    .error-border input, 
    .error-border div[data-baseweb="select"] {
        border: 2px solid #d90429 !important;
        border-radius: 6px !important;
    }

    /* CAIXA DE ERRO */
    .error-box {
        background: #fdecec;
        border-left: 6px solid #e63946;
        padding: 16px;
        border-radius: 8px;
        font-size: 17px;
        margin-top: 18px;
        color: #9d1c1c;
    }

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df_profiles = load_profiles()


# ----------------------------------------------------------
# TÍTULO DA PÁGINA
# ----------------------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin-top:10px; margin-bottom:0;">
    Job Match
</h1>
<hr style="margin-top:14px; margin-bottom:36px;">
""", unsafe_allow_html=True)



# ==========================================================
# FORMULÁRIO COMPLETO
# ==========================================================

def label_html(label, error_list):
    if label in error_list:
        return f"<span class='error-label'>{label}</span>"
    return f"<span>{label}</span>"


missing_fields_display = []


# ----------------------------------------------------------
# JOB FAMILY INFORMATION
# ----------------------------------------------------------
st.markdown("<div class='section-title'>Job Family Information</div><div class='divider-line'></div>", unsafe_allow_html=True)

cjf1, cjf2 = st.columns(2)

job_families = sorted(df_profiles["job_family"].dropna().unique().tolist())

with cjf1:
    st.markdown(label_html("Job Family", missing_fields_display), unsafe_allow_html=True)
    job_family = st.selectbox("", ["Choose option"] + job_families, key="jf")

with cjf2:
    st.markdown(label_html("Sub Job Family", missing_fields_display), unsafe_allow_html=True)

    if job_family == "Choose option":
        sub_job_family = st.selectbox("", ["Choose option"], key="subjf")
    else:
        sub_list = (
            df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"]
            .dropna().unique().tolist()
        )
        sub_job_family = st.selectbox("", ["Choose option"] + sorted(sub_list), key="subjf")


# ----------------------------------------------------------
# SECTION 1 — STRATEGIC IMPACT & SCOPE
# ----------------------------------------------------------
st.markdown("<div class='section-title'>Strategic Impact & Scope</div><div class='divider-line'></div>", unsafe_allow_html=True)

c1a, c1b, c1c = st.columns(3)

with c1a:
    st.markdown(label_html("Job Category", missing_fields_display), unsafe_allow_html=True)
    job_category = st.selectbox("", ["Choose option", "Executive", "Manager", "Professional", 
                                     "Technical Support", "Business Support", "Production"])

    st.markdown(label_html("Geographic Scope", missing_fields_display), unsafe_allow_html=True)
    geo_scope = st.selectbox("", ["Choose option", "Local", "Regional", "Multi-country", "Global"])

    st.markdown(label_html("Organizational Impact", missing_fields_display), unsafe_allow_html=True)
    org_impact = st.selectbox("", ["Choose option", "Team", "Department / Subfunction", 
                                   "Function", "Business Unit", "Enterprise-wide"])

with c1b:
    st.markdown(label_html("Span of Control", missing_fields_display), unsafe_allow_html=True)
    span_control = st.selectbox("", ["Choose option", "No direct reports", "Supervises team", 
                                     "Leads professionals", "Leads multiple teams", "Leads managers"])

    st.markdown(label_html("Nature of Work", missing_fields_display), unsafe_allow_html=True)
    nature_work = st.selectbox("", ["Choose option", "Process-oriented", "Analysis-oriented", 
                                    "Specialist", "Leadership-driven"])

    st.markdown(label_html("Financial Impact", missing_fields_display), unsafe_allow_html=True)
    financial_impact = st.selectbox("", ["Choose option", "No impact", "Cost center impact", 
                                         "Department-level impact", "Business Unit impact", 
                                         "Company-wide impact"])

with c1c:
    st.markdown(label_html("Stakeholder Complexity", missing_fields_display), unsafe_allow_html=True)
    stakeholder_complexity = st.selectbox("", ["Choose option", "Internal team", "Cross-functional",
                                               "External vendors", "Customers", "Regulatory/Authorities"])

    st.markdown(label_html("Decision Type", missing_fields_display), unsafe_allow_html=True)
    decision_type = st.selectbox("", ["Choose option", "Procedural", "Operational", "Tactical", "Strategic"])

    st.markdown(label_html("Decision Time Horizon", missing_fields_display), unsafe_allow_html=True)
    decision_horizon = st.selectbox("", ["Choose option", "Daily", "Weekly", "Monthly", "Annual", "Multi-year"])


# ----------------------------------------------------------
# SECTION 2 — AUTONOMY & COMPLEXITY
# ----------------------------------------------------------
st.markdown("<div class='section-title'>Autonomy & Complexity</div><div class='divider-line'></div>", unsafe_allow_html=True)

c2a, c2b, c2c = st.columns(3)

with c2a:
    st.markdown(label_html("Autonomy Level", missing_fields_display), unsafe_allow_html=True)
    autonomy = st.selectbox("", ["Choose option", "Close supervision", "Regular guidance", 
                                 "Independent", "Sets direction for others", "Defines strategy"])

    st.markdown(label_html("Problem Solving Complexity", missing_fields_display), unsafe_allow_html=True)
    problem_solving = st.selectbox("", ["Choose option", "Routine/Standardized", "Moderate",
                                        "Complex", "Ambiguous/Novel", "Organization-level"])

with c2b:
    st.markdown(label_html("Knowledge Depth", missing_fields_display), unsafe_allow_html=True)
    knowledge_depth = st.selectbox("", ["Choose option", "Entry-level knowledge", "Applied knowledge",
                                        "Advanced expertise", "Recognized expert", "Thought leader"])

    st.markdown(label_html("Operational Complexity", missing_fields_display), unsafe_allow_html=True)
    operational_complexity = st.selectbox("", ["Choose option", "Stable operations", "Some variability",
                                               "Complex operations", "High-variability environment"])

with c2c:
    st.markdown(label_html("Influence Level", missing_fields_display), unsafe_allow_html=True)
    influence_level = st.selectbox("", ["Choose option", "Team", "Cross-team", "Multi-function",
                                        "External vendors/clients", "Industry-level influence"])


# ----------------------------------------------------------
# SECTION 3 — KNOWLEDGE, KPIs & COMPETENCIES
# ----------------------------------------------------------
st.markdown("<div class='section-title'>Knowledge, KPIs & Competencies</div><div class='divider-line'></div>", unsafe_allow_html=True)

c3a, c3b, c3c = st.columns(3)

with c3a:
    st.markdown(label_html("Education Level", missing_fields_display), unsafe_allow_html=True)
    education = st.selectbox("", ["Choose option", "High School", "Technical Degree", "Bachelor’s",
                                  "Post-graduate", "Master’s", "Doctorate"])

    st.markdown(label_html("Experience Level", missing_fields_display), unsafe_allow_html=True)
    experience = st.selectbox("", ["Choose option", "< 2 years", "2–5 years", "5–10 years",
                                   "10–15 years", "15+ years"])

with c3b:
    st.markdown(label_html("Primary KPIs", missing_fields_display), unsafe_allow_html=True)
    kpis_selected = st.multiselect("", ["Financial", "Customer", "Operational", "Quality", "Safety",
                                        "Compliance", "Project Delivery", "People Leadership"])

    st.markdown(label_html("Specialization Level", missing_fields_display), unsafe_allow_html=True)
    specialization_level = st.selectbox("", ["Choose option", "Generalist", "Specialist", "Deep Specialist"])

with c3c:
    st.markdown(label_html("Core Competencies", missing_fields_display), unsafe_allow_html=True)
    competencies_selected = st.multiselect("", ["Communication", "Collaboration", "Analytical Thinking",
                                                "Technical Expertise", "Leadership", "Innovation",
                                                "Strategic Thinking", "Customer Orientation"])

    st.markdown(label_html("Innovation Responsibility", missing_fields_display), unsafe_allow_html=True)
    innovation_resp = st.selectbox("", ["Choose option", "Execution", "Incremental improvements",
                                        "Major improvements", "Innovation leadership"])

c3d, c3e = st.columns(2)

with c3d:
    st.markdown(label_html("Leadership Type", missing_fields_display), unsafe_allow_html=True)
    leadership_type = st.selectbox("", ["Choose option", "None", "Team Lead", "Supervisor",
                                        "Manager", "Senior Manager", "Director"])

with c3e:
    st.markdown(label_html("Organizational Influence", missing_fields_display), unsafe_allow_html=True)
    org_influence = st.selectbox("", ["Choose option", "Team", "Department", "Business Unit",
                                      "Function", "Enterprise-wide"])


# ----------------------------------------------------------
# BOTÃO — ALINHADO À ESQUERDA
# ----------------------------------------------------------
btn_col, _, _ = st.columns([2, 5, 1])

with btn_col:
    generate = st.button("Generate Job Match Description",
                         key="btn_generate",
                         use_container_width=False)
    st.markdown("<div class='blue-btn'></div>", unsafe_allow_html=True)


# ==========================================================
# PROCESSAMENTO DO MATCH
# ==========================================================
fields_dict = {
    "Job Family": job_family,
    "Sub Job Family": sub_job_family,
    "Job Category": job_category,
    "Geographic Scope": geo_scope,
    "Organizational Impact": org_impact,
    "Span of Control": span_control,
    "Nature of Work": nature_work,
    "Financial Impact": financial_impact,
    "Stakeholder Complexity": stakeholder_complexity,
    "Decision Type": decision_type,
    "Decision Time Horizon": decision_horizon,
    "Autonomy Level": autonomy,
    "Problem Solving Complexity": problem_solving,
    "Knowledge Depth": knowledge_depth,
    "Operational Complexity": operational_complexity,
    "Influence Level": influence_level,
    "Education Level": education,
    "Experience Level": experience,
    "Specialization Level": specialization_level,
    "Innovation Responsibility": innovation_resp,
    "Leadership Type": leadership_type,
    "Organizational Influence": org_influence,
}

# Campos MULTI obrigatórios
multi_required = {
    "Primary KPIs": kpis_selected,
    "Core Competencies": competencies_selected
}

missing = []

# Validação normal
for k, v in fields_dict.items():
    if v == "Choose option":
        missing.append(k)

# Validação multiselect
for k, v in multi_required.items():
    if not v:
        missing.append(k)


if generate:

    if missing:
        st.markdown("<div class='error-box'>Please fill all required fields.</div>", unsafe_allow_html=True)

        for m in missing:
            st.markdown(f"<div class='error-label'>{m} is required.</div>", unsafe_allow_html=True)
    else:
        result, _ = compute_match(fields_dict, df_profiles)

        html_out = render_job_match_description(result, df_profiles)

        st.markdown(html_out, unsafe_allow_html=True)
