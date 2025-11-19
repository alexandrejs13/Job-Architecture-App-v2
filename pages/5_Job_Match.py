import streamlit as st
import base64
import os
import streamlit.components.v1 as components
import html

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ---------------------------------------------------------
# HEADER (mesmo padrão SIG)
# ---------------------------------------------------------
def load_png(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return ""

icon_b64 = load_png("assets/icons/checkmark_success.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0;">Job Match</h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# GLOBAL CSS — mesmo estilo do Job Profile Explorer
# ==========================================================
st.markdown("""
<style>
.main > div {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD SVG ICONS (mesmo modelo da sua outra página)
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
# INPUT FORM (mesmo que você já tinha)
# ==========================================================
st.markdown("## Job Family Information")

col1, col2 = st.columns(2)

with col1:
    job_family = st.selectbox("Job Family", [
        "Corporate Affairs/Communications", "Finance", "HR", "IT", 
        "Marketing", "Operations", "Engineering", "Sales"
    ])

with col2:
    sub_job_family = st.selectbox("Sub Job Family", [
        "General Communications", "Internal Communications",
        "External Communications", "Media Relations", "Brand & Content"
    ])

# ==========================================================
# 3 CARDS (Inputs)
# ==========================================================
cA, cB, cC = st.columns(3)

with cA:
    st.markdown("### Strategic Impact & Scope")
    job_category = st.selectbox("Job Category *", 
        ["Executive", "Manager", "Professional", "Technical Support", "Business Support", "Production"]
    )
    geo_scope = st.selectbox("Geographic Scope *", ["Local", "Regional", "Multi-country", "Global"])
    org_impact = st.selectbox("Organizational Impact *", [
        "Team", "Department / Subfunction", "Function", 
        "Multi-function / Business Unit", "Enterprise-wide"
    ])
    span_control = st.selectbox("Span of Control *", [
        "No direct reports", "Individual contributor with influence", 
        "Supervises technicians/operators", "Leads professionals", 
        "Leads multiple teams", "Leads managers", "Leads multi-layer organization"
    ])

with cB:
    st.markdown("### Autonomy & Complexity")
    autonomy = st.selectbox("Autonomy Level *", [
        "Works under close supervision", "Works under regular guidance", 
        "Works independently", "Sets direction for others", "Defines organizational strategy"
    ])
    problem_solving = st.selectbox("Problem Solving Complexity *", [
        "Routine / Standardized", "Moderate analysis", "Complex analysis",
        "Novel / ambiguous problems", "Strategic, organization-changing problems"
    ])
    knowledge_depth = st.selectbox("Knowledge Depth *", [
        "Basic / Entry-level knowledge", "Applied technical / professional knowledge",
        "Advanced specialized expertise", "Recognized expert", 
        "World-class mastery / thought leader"
    ])
    influence = st.selectbox("Influence Level *", [
        "Internal team only", "Internal cross-team", "Internal multi-function",
        "External vendors/clients", "Influences industry-level practices"
    ])

with cC:
    st.markdown("### Knowledge, KPIs & Competencies")
    education = st.selectbox("Education Level *", [
        "High School", "Technical Degree", "Bachelor’s",
        "Post-graduate / Specialization", "Master’s", "Doctorate"
    ])
    experience = st.selectbox("Experience Level *",
        ["< 2 years", "2–5 years", "5–10 years", "10–15 years", "15+ years"]
    )
    kpis = st.multiselect("Primary KPIs * (select ≥1)", [
        "Financial", "Customer", "Operational", "Quality", "Safety",
        "Compliance", "Project Delivery", "People Leadership"
    ])
    competencies = st.multiselect("Core Competencies * (select ≥1)", [
        "Communication", "Collaboration", "Analytical Thinking", "Technical Expertise",
        "Leadership", "Innovation", "Strategic Thinking", "Customer Orientation"
    ])

# ==========================================================
# BOTÃO
# ==========================================================
center = st.columns([4, 2, 4])[1]
generate = center.button("Generate Job Match Description", use_container_width=True)

# ==========================================================
# HTML BUILDER — IDÊNTICO AO JOB PROFILE EXPLORER
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
    font-family: 'Segoe UI', sans-serif;
    background: #faf9f7;
}}

.container {{
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}}

.card-main {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #e3e1dd;
    margin-bottom: 34px;
}}

.title {{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
}}

.section {{
    margin-bottom: 32px;
}}

.section-title {{
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.section-line {{
    height: 1px;
    background: #e8e6e1;
    margin: 8px 0 14px 0;
}}

.section-text {{
    font-size: 14px;
    line-height: 1.45;
}}

.icon-inline {{
    width: 20px;
    height: 20px;
}}

</style>
</head>

<body>
<div class="container">

    <div class="card-main">
        <div class="title">Job Match Summary</div>
        <div><b>Job Family:</b> {html.escape(job_family)}</div>
        <div><b>Sub Job Family:</b> {html.escape(sub_job_family)}</div>
    </div>

    <!-- SECTION 1 -->
    <div class="section">
        <div class="section-title">
            <span class="icon-inline">{icons_svg["Strategic Impact & Scope"]}</span>
            Strategic Impact & Scope
        </div>
        <div class="section-line"></div>
        <div class="section-text">
            <b>Job Category:</b> {html.escape(job_category)}<br>
            <b>Geographic Scope:</b> {html.escape(geo_scope)}<br>
            <b>Organizational Impact:</b> {html.escape(org_impact)}<br>
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
            <b>Autonomy:</b> {html.escape(autonomy)}<br>
            <b>Problem Solving:</b> {html.escape(problem_solving)}<br>
            <b>Knowledge Depth:</b> {html.escape(knowledge_depth)}<br>
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
            <b>Education:</b> {html.escape(education)}<br>
            <b>Experience:</b> {html.escape(experience)}<br>
            <b>KPIs:</b> {", ".join(kpis)}<br>
            <b>Competencies:</b> {", ".join(competencies)}
        </div>
    </div>

</div>
</body>

</html>
"""

# ==========================================================
# RENDER HTML
# ==========================================================
if generate:
    html_code = build_html()
    components.html(html_code, height=1200, scrolling=True)
