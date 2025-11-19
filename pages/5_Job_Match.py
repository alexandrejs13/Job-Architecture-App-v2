# ==========================================================
# 5_Job_Match.py — Página completa
# ==========================================================
import streamlit as st
import pandas as pd
import base64
import os
import html

from match_engine import compute_job_match, load_profiles
from html_renderer import render_description

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# CSS GLOBAL
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

.section-title-h1 {
    font-size: 36px;
    font-weight: 700;
    margin: 0;
    padding: 0;
}

.label-required {
    color: #c62828 !important;
    font-weight: 700;
}

.selectbox-error > div:first-child {
    border: 2px solid #c62828 !important;
}

.generate-btn {
    background: #145efc !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px 22px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    border: none !important;
}

.success-card {
    background: #f5f3ee;
    padding: 26px;
    border-radius: 18px;
    border: 1px solid #e3e1dd;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:16px; margin-top:12px;">
    <img src="https://cdn-icons-png.flaticon.com/512/992/992651.png" width="48">
    <h1 class="section-title-h1">Job Match</h1>
</div>
<hr>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD PROFILES
# ----------------------------------------------------------
df_profiles = load_profiles()

# ----------------------------------------------------------
# FORM FIELDS
# ----------------------------------------------------------
form_values = {}
errors = []

def field(label, options, col, key):
    global form_values, errors

    with col:
        missing = st.session_state.get(f"err_{key}", False)
        class_add = "selectbox-error" if missing else ""

        if missing:
            st.markdown(f"<div class='label-required'>{label}</div>", unsafe_allow_html=True)
        else:
            st.markdown(label)

        val = st.selectbox(
            "",
            ["Choose option"] + options,
            key=key,
            label_visibility="collapsed",
            help="",
            placeholder="Choose option",
        )

        form_values[key] = val
        return val


# ----------------------------------------------------------
# BUILD UI FORM
# ----------------------------------------------------------
st.markdown("### Job Family Information")
st.divider()

c1, c2 = st.columns(2)

job_fam_list = sorted(df_profiles["job_family"].dropna().unique().tolist())

job_family = field("Job Family", job_fam_list, c1, "job_family")

if job_family == "Choose option":
    sub_job_family = field("Sub Job Family", [], c2, "sub_job_family")
else:
    sub_list = sorted(df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"].dropna().unique().tolist())
    sub_job_family = field("Sub Job Family", sub_list, c2, "sub_job_family")


# ----------------------------------------------------------
# Strategic
# ----------------------------------------------------------
st.markdown("### Strategic Impact & Scope")
st.divider()

c1, c2, c3 = st.columns(3)

job_category = field("Job Category", 
    ["Executive","Manager","Professional","Technical Support","Business Support","Production"],
    c1, "job_category"
)

geographic_scope = field("Geographic Scope",
    ["Local","Regional","Multi-country","Global"],
    c1, "geographic_scope"
)

organizational_impact = field("Organizational Impact",
    ["Team","Department / Subfunction","Function","Business Unit","Enterprise-wide"],
    c1, "organizational_impact"
)

span_control = field("Span of Control",
    ["No direct reports","Supervises team","Leads professionals","Leads multiple teams","Leads managers"],
    c2, "span_of_control"
)

nature_work = field("Nature of Work",
    ["Process-oriented","Analysis-oriented","Specialist","Leadership-driven"],
    c2, "nature_of_work"
)

financial_impact = field("Financial Impact",
    ["No impact","Cost center impact","Department-level impact","Business Unit impact","Company-wide impact"],
    c2, "financial_impact"
)

stakeholder_complexity = field("Stakeholder Complexity",
    ["Internal team","Cross-functional","External vendors","Customers","Regulatory/Authorities"],
    c3, "stakeholder_complexity"
)

decision_type = field("Decision Type",
    ["Procedural","Operational","Tactical","Strategic"],
    c3, "decision_type"
)

decision_horizon = field("Decision Time Horizon",
    ["Daily","Weekly","Monthly","Annual","Multi-year"],
    c3, "decision_horizon"
)


# ----------------------------------------------------------
# AUTONOMY
# ----------------------------------------------------------
st.markdown("### Autonomy & Complexity")
st.divider()

c1, c2, c3 = st.columns(3)

autonomy = field("Autonomy Level",
    ["Close supervision","Regular guidance","Independent","Sets direction for others","Defines strategy"],
    c1, "autonomy_level"
)

problem_solving = field("Problem Solving Complexity",
    ["Routine/Standardized","Moderate","Complex","Ambiguous/Novel","Organization-level"],
    c1, "problem_solving_complexity"
)

knowledge_depth = field("Knowledge Depth",
    ["Entry-level knowledge","Applied knowledge","Advanced expertise","Recognized expert","Thought leader"],
    c2, "knowledge_depth"
)

operational_complexity = field("Operational Complexity",
    ["Stable operations","Some variability","Complex operations","High-variability environment"],
    c2, "operational_complexity"
)

influence_level = field("Influence Level",
    ["Team","Cross-team","Multi-function","External vendors/clients","Industry-level influence"],
    c3, "influence_level"
)


# ----------------------------------------------------------
# Knowledge
# ----------------------------------------------------------
st.markdown("### Knowledge, KPIs & Competencies")
st.divider()

c1, c2, c3 = st.columns(3)

education = field("Education Level",
    ["High School","Technical Degree","Bachelor’s","Post-graduate","Master’s","Doctorate"],
    c1, "education_level"
)

experience = field("Experience Level",
    ["< 2 years","2–5 years","5–10 years","10–15 years","15+ years"],
    c1, "experience_level"
)

specialization = field("Specialization Level",
    ["Generalist","Specialist","Deep Specialist"],
    c2, "specialization_level"
)

innovation_resp = field("Innovation Responsibility",
    ["Execution","Incremental improvements","Major improvements","Innovation leadership"],
    c2, "innovation_responsibility"
)

leadership_type = field("Leadership Type",
    ["None","Team Lead","Supervisor","Manager","Senior Manager","Director"],
    c3, "leadership_type"
)

org_influence = field("Organizational Influence",
    ["Team","Department","Business Unit","Function","Enterprise-wide"],
    c3, "organizational_influence"
)


# ----------------------------------------------------------
# BUTTON
# ----------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

btn_col = st.columns([1,6,1])[0]
with btn_col:
    generate = st.button("Generate Job Match Description", type="primary", use_container_width=False)


# ----------------------------------------------------------
# VALIDATE
# ----------------------------------------------------------
if generate:
    missing_any = False

    for key, value in form_values.items():
        if value == "Choose option":
            st.session_state[f"err_{key}"] = True
            missing_any = True
        else:
            st.session_state[f"err_{key}"] = False

    if missing_any:
        st.error("Please fill all required fields.")
        st.stop()

    # ----------------------------------------
    # COMPUTE MATCH
    # ----------------------------------------
    match = compute_job_match(form_values, df_profiles)

    # ----------------------------------------
    # RENDER HTML
    # ----------------------------------------
    html_result = render_description(match)

    st.components.v1.html(html_result, height=1500, scrolling=False)
