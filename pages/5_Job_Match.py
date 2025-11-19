# ==========================================================
# PAGE CONFIG + HEADER (SIG STANDARD)
# ==========================================================
import streamlit as st
import pandas as pd
import numpy as np
import base64
import os
import html
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="Job Match", layout="wide")


# ----------------------------------------------------------
# LOAD ICON
# ----------------------------------------------------------
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


icon_path = "assets/icons/checkmark_success.png"
icon_b64 = load_icon_png(icon_path)


# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.markdown(f"""
<div style="
    display:flex;
    align-items:center;
    gap:18px;
    margin-top:12px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:56px; height:56px;">
    <h1 style="
        font-size:36px;
        font-weight:700;
        margin:0;
        padding:0;
    ">
        Job Match
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)


# ==========================================================
# GLOBAL LAYOUT — SIG WIDTH CONTROL (FULL VERSION)
# ==========================================================
st.markdown("""
<style>

    /* Main container */
    .main > div {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    .stDataFrame {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }

    .block-container, .stColumn {
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Card style */
    .card-block {
        background: #f8f7f5;
        padding: 20px 22px;
        border-radius: 14px;
        border: 1px solid #e4e2dd;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 14px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# FIX EMPTY LABELS OUTSIDE CARDS (STREAMLIT HACK)
# ==========================================================
st.markdown("""
<style>
    /* Hide empty labels Streamlit generates */
    .stSelectbox > label {
        display: none !important;
    }

    /* Reduce spacing on selects */
    .stSelectbox {
        margin-top: -6px !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================================
# LOAD JOB PROFILE DATA
# ==========================================================
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")


df = load_profiles()


# ==========================================================
# LOAD ICONS (SVG)
# ==========================================================
def load_svg(svg_name):
    path = f"assets/icons/sig/{svg_name}"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


icons_svg = {
    "Sub Job Family Description": load_svg("Hierarchy.svg"),
    "Job Profile Description": load_svg("Content_Book_Phone.svg"),
    "Career Band Description": load_svg("File_Clipboard_Text.svg"),
    "Role Description": load_svg("Shopping_Business_Target.svg"),
    "Grade Differentiator": load_svg("User_Add.svg"),
    "Qualifications": load_svg("Edit_Pencil.svg"),
    "Specific parameters / KPIs": load_svg("Graph_Bar.svg"),
    "Competencies 1": load_svg("Setting_Cog.svg"),
    "Competencies 2": load_svg("Setting_Cog.svg"),
    "Competencies 3": load_svg("Setting_Cog.svg"),
}


sections = [
    "Sub Job Family Description",
    "Job Profile Description",
    "Career Band Description",
    "Role Description",
    "Grade Differentiator",
    "Qualifications",
    "Specific parameters / KPIs",
    "Competencies 1",
    "Competencies 2",
    "Competencies 3",
]


# ==========================================================
# DESCRIPTION LAYOUT (PREMIUM — 1 COLUMN)
# ==========================================================
def build_single_profile_html(p):

    job = html.escape(p["Job Profile"])
    gg  = html.escape(str(p["Global Grade"]))
    jf  = html.escape(p["Job Family"])
    sf  = html.escape(p["Sub Job Family"])
    cp  = html.escape(p["Career Path"])
    fc  = html.escape(p["Full Job Code"])

    html_code = f"""
<html>
<head>
<meta charset="UTF-8">

<style>

html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}}

#viewport {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.card-top {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e3e1dd;
}}

.title {{
    font-size: 20px;
    font-weight: 700;
}}

.gg {{
    color: #145efc;
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
}}

.meta {{
    background: white;
    padding: 14px;
    margin-top: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
}}

#scroll-area {{
    flex: 1;
    overflow-y: auto;
    padding: 22px 4px 32px 0;
}}

.section-box {{
    padding-bottom: 26px;
}}

.section-title {{
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.section-line {{
    height: 1px;
    background: #e8e6e1;
    width: 100%;
    margin: 8px 0 14px 0;
}}

.section-text {{
    font-size: 14px;
    white-space: pre-wrap;
}}

.icon-inline {{
    width: 20px;
    height: 20px;
}}

</style>

</head>

<body>
<div id="viewport">

    <div id="top-area">
        <div class="card-top">
            <div class="title">{job}</div>
            <div class="gg">GG {gg}</div>

            <div class="meta">
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        </div>
    </div>

    <div id="scroll-area">
"""

    for sec in sections:
        icon = icons_svg.get(sec, "")
        text = html.escape(str(p.get(sec, "")))

        html_code += f"""
        <div class="section-box">
            <div class="section-title">
                <span class="icon-inline">{icon}</span>
                {html.escape(sec)}
            </div>
            <div class="section-line"></div>
            <div class="section-text">{text}</div>
        </div>
        """

    html_code += """
    </div>
</div>
</body>
</html>
"""
    return html_code



# ==========================================================
# MATCH ENGINE
# ==========================================================
def clean_text(t):
    if pd.isna(t): return ""
    t = str(t).lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return t


def extract_keywords(text):
    return set(clean_text(text).split())


def score_match(user_tags, row):

    weights = {
        "Grade Differentiator": 25,
        "Qualifications": 20,
        "Specific parameters / KPIs": 15,
        "Competencies 1": 10,
        "Competencies 2": 10,
        "Competencies 3": 10,
        "Job Profile Description": 5,
        "Role Description": 3,
        "Career Band Description": 2,
    }

    score = 0

    for col, w in weights.items():
        kw = extract_keywords(row.get(col, ""))
        overlap = len(user_tags.intersection(kw))
        score += overlap * w

    return score



# ==========================================================
# USER INPUT — FAMILY + SUBFAMILY
# ==========================================================
st.subheader("Job Family Information")

c1, c2 = st.columns(2)

with c1:
    family = st.selectbox("Job Family", sorted(df["Job Family"].dropna().unique()))

with c2:
    sublist = df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
    subfamily = st.selectbox("Sub Job Family", sorted(sublist))

flt = df[(df["Job Family"] == family) & (df["Sub Job Family"] == subfamily)]

if flt.empty:
    st.stop()


# ==========================================================
# 3 CARDS CONTAINER
# ==========================================================
with st.container():

    colA, colB, colC = st.columns(3)

    # ------------------------------------------------------
    # CARD 1 — STRATEGIC IMPACT & SCOPE
    # ------------------------------------------------------
    with colA:
        st.markdown('<div class="card-block">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Strategic Impact & Scope</div>', unsafe_allow_html=True)

        job_category = st.selectbox(
            "Job Category *",
            ["Executive", "Manager", "Professional", "Technical Support", "Business Support", "Production"]
        )

        geo_scope = st.selectbox(
            "Geographic Scope *",
            ["Local", "Regional", "Multi-country", "Global"]
        )

        org_impact = st.selectbox(
            "Organizational Impact *",
            ["Team", "Department / Subfunction", "Function", "Multi-function / BU-wide", "Enterprise-wide"]
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

    # ------------------------------------------------------
    # CARD 2 — AUTONOMY & COMPLEXITY
    # ------------------------------------------------------
    with colB:
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

    # ------------------------------------------------------
    # CARD 3 — KNOWLEDGE, KPIs & COMPETENCIES
    # ------------------------------------------------------
    with colC:
        st.markdown('<div class="card-block">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Knowledge, KPIs & Competencies</div>', unsafe_allow_html=True)

        education = st.selectbox(
            "Education Level *",
            [
                "High School",
                "Technical Degree",
                "Bachelor’s",
                "Post-graduate / Specialization",
                "Master’s",
                "Doctorate"
            ]
        )

        experience = st.selectbox(
            "Experience Level *",
            [
                "< 2 years",
                "2–5 years",
                "5–10 years",
                "10–15 years",
                "15+ years"
            ]
        )

        kpis = st.multiselect(
            "Primary KPIs * (select ≥1)",
            ["Financial", "Customer", "Operational", "Quality", "Safety", "Compliance", "Project Delivery", "People Leadership"]
        )

        competencies = st.multiselect(
            "Core Competencies * (select ≥1)",
            ["Communication", "Collaboration", "Analytical Thinking", "Technical Expertise", "Leadership", "Innovation", "Strategic Thinking", "Customer Orientation"]
        )

        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# USER TAG BUILDER
# ==========================================================
def build_user_tags():

    tags = set()

    tags.update(job_category.lower().split())
    tags.update(geo_scope.lower().split())
    tags.update(org_impact.lower().replace("/", " ").split())
    tags.update(span_control.lower().split())
    tags.update(autonomy.lower().split())
    tags.update(problem_solving.lower().split())
    tags.update(knowledge_depth.lower().split())
    tags.update(influence.lower().split())

    edu_map = {
        "High School": ["basic"],
        "Technical Degree": ["technical"],
        "Bachelor’s": ["bachelor", "degree"],
        "Post-graduate / Specialization": ["advanced", "specialization"],
        "Master’s": ["master"],
        "Doctorate": ["phd", "doctorate"]
    }
    tags.update(edu_map.get(education, []))

    exp_map = {
        "< 2 years": ["junior"],
        "2–5 years": ["intermediate"],
        "5–10 years": ["senior"],
        "10–15 years": ["expert"],
        "15+ years": ["leader"]
    }
    tags.update(exp_map.get(experience, []))

    for k in kpis:
        tags.add(k.lower())

    for c in competencies:
        tags.add(c.lower())

    return tags



# ==========================================================
# BUTTON
# ==========================================================
st.write("")
generate = st.button("Generate Job Match Description", type="primary")



# ==========================================================
# RUN MATCH
# ==========================================================
if generate:

    if not kpis:
        st.error("Please select at least one KPI.")
        st.stop()

    if not competencies:
        st.error("Please select at least one competency.")
        st.stop()

    user_tags = build_user_tags()

    flt = flt.copy()
    flt["score"] = flt.apply(lambda r: score_match(user_tags, r), axis=1)

    best = flt.sort_values("score", ascending=False).iloc[0].to_dict()

    st.success(f"Matched Job Profile: **{best['Job Profile']}** (GG {best['Global Grade']})")

    components.html(
        build_single_profile_html(best),
        height=900,
        scrolling=False
    )
