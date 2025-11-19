import streamlit as st
import base64
import os
import html
import streamlit.components.v1 as components

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")


# ==========================================================
# CSS GLOBAL — TITULAÇÃO, GRID, BOTÃO, LAYOUT
# ==========================================================
st.markdown("""
<style>

/* Limite de largura */
.main > div {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
}

/* Títulos das 3 colunas */
.section-header {
    font-size: 20px !important;
    font-weight: 700 !important;
    margin: 0 0 10px 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;

    /* FIXA ALTURA — impede desalinhamento */
    height: 30px;
    display: flex;
    align-items: center;
}

/* Botão azul SIG */
div.stButton > button {
    background-color: #145efc !important;
    color: white !important;
    border-radius: 8px !important;
    height: 46px !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    border: none !important;
}
div.stButton > button:hover {
    background-color: #0f4ad6 !important;
    color: white !important;
}

/* Remove margem invisível dos h1/h2 internos */
h1, h2, h3 {
    margin-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# ICON PNG DO HEADER
# ==========================================================
def load_png(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return ""

icon_b64 = load_png("assets/icons/checkmark_success.png")


# ==========================================================
# HEADER — ÍCONE + TÍTULO
# ==========================================================
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0;">Job Match</h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)


# ==========================================================
# LOAD SVG ICONS — IGUAL AO JOB PROFILE DESCRIPTION
# ==========================================================
def load_svg(svg_name):
    path = f"assets/icons/sig/{svg_name}"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

icons_svg = {
    "Strategic Impact & Scope": load_svg("Hierarchy.svg"),
    "Autonomy & Complexity": load_svg("Setting_Cog.svg"),
    "Knowledge, KPIs & Competencies": load_svg("Graph_Bar.svg"),
}


# ==========================================================
# JOB FAMILY INPUTS
# ==========================================================
st.markdown("## Job Family Information")

colA, colB = st.columns(2)

with colA:
    job_family = st.selectbox("Job Family", [
        "Corporate Affairs/Communications", "Finance", "HR", "IT",
        "Marketing", "Operations", "Engineering", "Sales"
    ])

with colB:
    sub_job_family = st.selectbox("Sub Job Family", [
        "General Communications", "Internal Communications",
        "External Communications", "Media Relations", "Brand & Content"
    ])


# ==========================================================
# INPUT CARDS (3 SEÇÕES)
# ==========================================================
c1, c2, c3 = st.columns(3)

# --------- CARD 1 ---------
with c1:
    st.markdown('<div class="section-header">Strategic Impact & Scope</div>', unsafe_allow_html=True)

    job_category = st.selectbox("Job Category *",
        ["Executive","Manager","Professional","Technical Support","Business Support","Production"]
    )
    geo_scope = st.selectbox("Geographic Scope *", ["Local","Regional","Multi-country","Global"])
    org_impact = st.selectbox("Organizational Impact *",
        ["Team","Department / Subfunction","Function","Multi-function / Business Unit","Enterprise-wide"]
    )
    span_control = st.selectbox("Span of Control *",
        ["No direct reports","Individual contributor with influence","Supervises technicians/operators",
         "Leads professionals","Leads multiple teams","Leads managers","Leads multi-layer organization"]
    )

# --------- CARD 2 ---------
with c2:
    st.markdown('<div class="section-header">Autonomy & Complexity</div>', unsafe_allow_html=True)

    autonomy = st.selectbox("Autonomy Level *",
        ["Works under close supervision","Works under regular guidance","Works independently",
         "Sets direction for others","Defines organizational strategy"]
    )
    problem_solving = st.selectbox("Problem Solving Complexity *",
        ["Routine / Standardized","Moderate analysis","Complex analysis",
         "Novel / ambiguous problems","Strategic, organization-changing problems"]
    )
    knowledge_depth = st.selectbox("Knowledge Depth *",
        ["Basic / Entry-level knowledge","Applied technical / professional knowledge",
         "Advanced specialized expertise","Recognized expert","World-class mastery / thought leader"]
    )
    influence = st.selectbox("Influence Level *",
        ["Internal team only","Internal cross-team","Internal multi-function",
         "External vendors/clients","Influences industry-level practices"]
    )

# --------- CARD 3 ---------
with c3:
    st.markdown('<div class="section-header">Knowledge, KPIs & Competencies</div>', unsafe_allow_html=True)

    education = st.selectbox("Education Level *",
        ["High School","Technical Degree","Bachelor’s","Post-graduate / Specialization","Master’s","Doctorate"]
    )
    experience = st.selectbox("Experience Level *",
        ["< 2 years","2–5 years","5–10 years","10–15 years","15+ years"]
    )
    kpis = st.multiselect("Primary KPIs * (select ≥1)", [
        "Financial","Customer","Operational","Quality","Safety",
        "Compliance","Project Delivery","People Leadership"
    ])
    competencies = st.multiselect("Core Competencies * (select ≥1)", [
        "Communication","Collaboration","Analytical Thinking","Technical Expertise",
        "Leadership","Innovation","Strategic Thinking","Customer Orientation"
    ])


# ==========================================================
# BOTÃO
# ==========================================================
button_center = st.columns([4,2,4])[1]
generate = button_center.button("Generate Job Match Description", use_container_width=True)


# ==========================================================
# HTML DO RESULTADO — IDÊNTICO AO JOB PROFILE DESCRIPTION EXPLORER
# ==========================================================
def build_html():

    return f"""
<html>
<head>
<meta charset='UTF-8'>
<style>

body {{
    margin:0;
    padding:0;
    background:#faf9f7;
    font-family:'Segoe UI',sans-serif;
}}

.container {{
    max-width:1100px;
    margin:auto;
    padding:20px 30px;
}}

.card-top {{
    background:#f5f3ee;
    border-radius:16px;
    padding:24px;
    border:1px solid #e3e1dd;
    margin-bottom:34px;
}}

.title {{
    font-size:22px;
    font-weight:700;
    margin-bottom:8px;
}}

.section {{
    margin-bottom:38px;
}}

.section-title {{
    font-size:16px;
    font-weight:700;
    display:flex;
    align-items:center;
    gap:6px;
}}

.section-line {{
    height:1px;
    background:#e8e6e1;
    margin:8px 0 14px 0;
}}

.section-text {{
    white-space:pre-wrap;
    font-size:14px;
    line-height:1.45;
}}

.icon-inline {{
    width:20px;
    height:20px;
}}

</style>
</head>

<body>
<div class="container">

    <div class="card-top">
        <div class="title">Job Match Summary</div>
        <b>Job Family:</b> {html.escape(job_family)}<br>
        <b>Sub Job Family:</b> {html.escape(sub_job_family)}<br>
    </div>

    <!-- SECTION 1 -->
    <div class="section">
        <div class="section-title">
            <span class="icon-inline">{icons_svg["Strategic Impact & Scope"]}</span>
            Strategic Impact & Scope
        </div>
        <div class="section-line"></div>
        <div class="section-text">
<b>Job Category:</b> {html.escape(job_category)}
<b>Geographic Scope:</b> {html.escape(geo_scope)}
<b>Organizational Impact:</b> {html.escape(org_impact)}
<b>Span of Control:</b> {html.escape(span_control)}
        </div>
    </div>

    <!-- SECTION 2 -->
    <div class="section">
        <div class="section-title">
            <span class="icon-inline">{icons_svg["Autonomy & Complexity"]}</span>
            Autonomy & Complexity
        </div>
        <div class="section-line"></div>
        <div class="section-text">
<b>Autonomy:</b> {html.escape(autonomy)}
<b>Problem Solving:</b> {html.escape(problem_solving)}
<b>Knowledge Depth:</b> {html.escape(knowledge_depth)}
<b>Influence:</b> {html.escape(influence)}
        </div>
    </div>

    <!-- SECTION 3 -->
    <div class="section">
        <div class="section-title">
            <span class="icon-inline">{icons_svg["Knowledge, KPIs & Competencies"]}</span>
            Knowledge, KPIs & Competencies
        </div>
        <div class="section-line"></div>
        <div class="section-text">
<b>Education:</b> {html.escape(education)}
<b>Experience:</b> {html.escape(experience)}
<b>KPIs:</b> {", ".join(kpis)}
<b>Competencies:</b> {", ".join(competencies)}
        </div>
    </div>

</div>
</body></html>
"""


# ==========================================================
# RENDER HTML
# ==========================================================
if generate:
    components.html(build_html(), height=1500, scrolling=True)
