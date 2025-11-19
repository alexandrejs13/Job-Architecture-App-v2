import streamlit as st
import base64
import os

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ---------------------------------------------------------
# FIXED GLOBAL LAYOUT — prevents infinite stretch
# ---------------------------------------------------------
st.markdown("""
<style>

    .main > div {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    .block-container, .stColumn {
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* CARD BLOCK */
    .card-block {
        background: #f7f5f2;
        padding: 24px 26px;
        border-radius: 16px;
        border: 1px solid #e6e2dc;
        margin-bottom: 26px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 16px;
        color: #111;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
def load_icon_png(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return ""

icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0;">Job Match</h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)


# =================================================================
# JOB FAMILY
# =================================================================
st.markdown("## Job Family Information")

col1, col2 = st.columns(2)

with col1:
    job_family = st.selectbox(
        "Job Family",
        [
            "Corporate Affairs/Communications",
            "Finance",
            "HR",
            "IT",
            "Marketing",
            "Operations",
            "Engineering",
            "Sales"
        ]
    )

with col2:
    sub_job_family = st.selectbox(
        "Sub Job Family",
        [
            "General Communications",
            "Internal Communications",
            "External Communications",
            "Media Relations",
            "Brand & Content"
        ]
    )


# =================================================================
# 3 REAL CARDS — sem NENHUM container extra
# =================================================================
cA, cB, cC = st.columns(3)

# ------------------------------
# CARD A
# ------------------------------
with cA:
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Strategic Impact & Scope</div>', unsafe_allow_html=True)

    job_category = st.selectbox(
        "Job Category *",
        ["Executive", "Manager", "Professional", "Technical Support", "Business Support", "Production"]
    )
    geo_scope = st.selectbox("Geographic Scope *", ["Local", "Regional", "Multi-country", "Global"])
    org_impact = st.selectbox(
        "Organizational Impact *",
        ["Team", "Department / Subfunction", "Function", "Multi-function / Business Unit", "Enterprise-wide"]
    )
    span_control = st.selectbox(
        "Span of Control *",
        [
            "No direct reports",
            "Individual contributor with influence",
            "Supervises technicians/operators",
            "Leads professionals",
            "Leads multiple teams",
            "Leads managers",
            "Leads multi-layer organization"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------
# CARD B
# ------------------------------
with cB:
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Autonomy & Complexity</div>', unsafe_allow_html=True)

    autonomy = st.selectbox(
        "Autonomy Level *",
        [
            "Works under close supervision",
            "Works under regular guidance",
            "Works independently",
            "Sets direction for others",
            "Defines organizational strategy"
        ]
    )

    problem_solving = st.selectbox(
        "Problem Solving Complexity *",
        [
            "Routine / Standardized",
            "Moderate analysis",
            "Complex analysis",
            "Novel / ambiguous problems",
            "Strategic, organization-changing problems"
        ]
    )

    knowledge_depth = st.selectbox(
        "Knowledge Depth *",
        [
            "Basic / Entry-level knowledge",
            "Applied technical / professional knowledge",
            "Advanced specialized expertise",
            "Recognized expert",
            "World-class mastery / thought leader"
        ]
    )

    influence = st.selectbox(
        "Influence Level *",
        [
            "Internal team only",
            "Internal cross-team",
            "Internal multi-function",
            "External vendors/clients",
            "Influences industry-level practices"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------
# CARD C
# ------------------------------
with cC:
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Knowledge, KPIs & Competencies</div>', unsafe_allow_html=True)

    education = st.selectbox(
        "Education Level *",
        ["High School", "Technical Degree", "Bachelor’s", "Post-graduate / Specialization", "Master’s", "Doctorate"]
    )

    experience = st.selectbox(
        "Experience Level *",
        ["< 2 years", "2–5 years", "5–10 years", "10–15 years", "15+ years"]
    )

    kpis = st.multiselect(
        "Primary KPIs * (select ≥1)",
        ["Financial", "Customer", "Operational", "Quality", "Safety", "Compliance", "Project Delivery", "People Leadership"]
    )

    competencies = st.multiselect(
        "Core Competencies * (select ≥1)",
        [
            "Communication", "Collaboration", "Analytical Thinking", "Technical Expertise", "Leadership",
            "Innovation", "Strategic Thinking", "Customer Orientation"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# =================================================================
# BUTTON
# =================================================================
center = st.columns([4, 2, 4])[1]
with center:
    generate = st.button("Generate Job Match Description", use_container_width=True)

# =================================================================
# GENERATION LOGIC
# =================================================================
if generate:

    description = f"""
### Job Match Description

**Job Family:** {job_family}  
**Sub Job Family:** {sub_job_family}

---

#### Strategic Impact & Scope
- **Job Category:** {job_category}
- **Geographic Scope:** {geo_scope}
- **Organizational Impact:** {org_impact}
- **Span of Control:** {span_control}

---

#### Autonomy & Complexity
- **Autonomy Level:** {autonomy}
- **Problem Solving Complexity:** {problem_solving}
- **Knowledge Depth:** {knowledge_depth}
- **Influence Level:** {influence}

---

#### Knowledge, KPIs & Competencies
- **Education Level:** {education}
- **Experience Level:** {experience}
- **KPIs:** {", ".join(kpis) if kpis else "None"}
- **Competencies:** {", ".join(competencies) if competencies else "None"}

---

### Narrative Summary

This role sits within the **{job_family} / {sub_job_family}** domain and operates at a **{job_category}** level.  
It influences the **{org_impact}** scope, with responsibilities spanning **{geo_scope.lower()}** impact.

The role requires **{autonomy.lower()}**, handles **{problem_solving.lower()}**, and demands **{knowledge_depth.lower()}**.  
Its sphere of influence reaches **{influence.lower()}**.

Qualifications expected include **{education}**, combined with **{experience}** of relevant experience.  
Performance is measured through KPIs such as **{", ".join(kpis)}**, supported by competencies including **{", ".join(competencies)}**.
    """

    st.success("Job Match Description generated successfully!")
    st.markdown(description)
