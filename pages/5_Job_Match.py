import streamlit as st
import pandas as pd
import base64
import os
import html
import streamlit.components.v1 as components

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(page_title="Job Match", layout="wide")

# ============================================================================
# CSS — IDENTIDADE VISUAL SIG (idêntico ao Job Profile Description)
# ============================================================================
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
}

.section-title {
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 0;
    margin: 0;
}

.divider-line {
    height: 1px;
    width: 100%;
    background: #e0ddd6;
    margin: 6px 0 18px 0;
}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD ICON – CHECKMARK SUCCESS
# ============================================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

# ============================================================================
# HEADER — IGUAL A TODAS AS SUAS PÁGINAS
# ============================================================================
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:10px; margin-bottom:8px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:48px; height:48px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:32px;">
""", unsafe_allow_html=True)

# ============================================================================
# LOAD JOB PROFILE DATA (Job Profile.xlsx)
# ============================================================================

@st.cache_data
def load_job_profiles():
    df = pd.read_excel("data/Job Profile.xlsx")

    # Normalização de colunas importantes
    rename_map = {
        "Job Family": "job_family",
        "Sub Job Family": "sub_job_family",
        "Career Path": "career_path",
        "Full Job Code": "full_job_code",
        "Job Profile": "job_profile",
        "Global Grade": "global_grade",
        "Sub Job Family Description": "desc_sub_family",
        "Job Profile Description": "desc_profile",
        "Career Band Description": "desc_career_band",
        "Role Description": "desc_role",
        "Grade Differentiator": "desc_grade_diff",
        "Qualifications": "desc_qualifications",
        "Specific parameters / KPIs": "desc_kpis",
        "Competencies 1": "desc_comp1",
        "Competencies 2": "desc_comp2",
        "Competencies 3": "desc_comp3"
    }

    # Renomear apenas as colunas que existem
    rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    # Remove espaços extras
    df.columns = [c.strip() for c in df.columns]

    return df

df_profiles = load_job_profiles()

# ============================================================================
# BLOCO 1 — JOB FAMILY INFORMATION (TÍTULO + LINHA DIVISÓRIA)
# ============================================================================
st.markdown("""
<div class="section-title">Job Family Information</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

# Preparação das listas dinâmicas
job_fams = sorted(df_profiles["job_family"].dropna().unique().tolist())

col1, col2 = st.columns(2)

with col1:
    job_family = st.selectbox(
        "Job Family",
        ["Choose option"] + job_fams
    )

with col2:
    if job_family == "Choose option":
        sub_job_family = st.selectbox("Sub Job Family", ["Choose option"])
    else:
        sub_list = df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"].dropna().unique().tolist()
        sub_job_family = st.selectbox("Sub Job Family", ["Choose option"] + sorted(sub_list))
# ============================================================================
# BLOCO 2 — STRATEGIC IMPACT & SCOPE
# ============================================================================
st.markdown("""
<div class="section-title">Strategic Impact & Scope</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

cA1, cA2, cA3 = st.columns(3)

with cA1:
    job_category = st.selectbox(
        "Job Category",
        ["Choose option", "Executive", "Manager", "Professional", "Technical Support", "Business Support", "Production"]
    )

    geo_scope = st.selectbox(
        "Geographic Scope",
        ["Choose option", "Local", "Regional", "Multi-country", "Global"]
    )

    org_impact = st.selectbox(
        "Organizational Impact",
        [
            "Choose option",
            "Team",
            "Department/Subfunction",
            "Function",
            "Multi-function/BU",
            "Enterprise-wide"
        ]
    )

with cA2:
    span_control = st.selectbox(
        "Span of Control",
        [
            "Choose option",
            "No direct reports",
            "Individual contributor with influence",
            "Supervises technicians/operators",
            "Leads professionals",
            "Leads multiple teams",
            "Leads managers",
            "Leads multi-layer org"
        ]
    )

    nature_work = st.selectbox(
        "Nature of Work",
        [
            "Choose option",
            "Process-oriented",
            "Project-oriented",
            "Client-oriented",
            "Operations",
            "Strategy",
            "Innovation",
            "Governance"
        ]
    )

    decision_type = st.selectbox(
        "Decision Type",
        [
            "Choose option",
            "Procedural",
            "Operational",
            "Analytical",
            "Financial",
            "Regulatory",
            "Strategic"
        ]
    )

with cA3:
    financial_impact = st.selectbox(
        "Financial Impact",
        [
            "Choose option",
            "No impact",
            "Cost control",
            "Budget owner",
            "Revenue influence",
            "P&L responsibility"
        ]
    )

    stakeholder_complexity = st.selectbox(
        "Stakeholder Complexity",
        [
            "Choose option",
            "Internal team",
            "Cross-functional",
            "Business Unit",
            "Regional",
            "Global",
            "Clients",
            "Regulators",
            "Board"
        ]
    )

    time_horizon = st.selectbox(
        "Decision Time Horizon",
        [
            "Choose option",
            "Daily",
            "Weekly",
            "Monthly",
            "Quarterly",
            "Annually",
            "3 Years",
            "5+ Years"
        ]
    )

# ============================================================================
# BLOCO 3 — AUTONOMY & COMPLEXITY
# ============================================================================
st.markdown("""
<div class="section-title">Autonomy & Complexity</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

cB1, cB2, cB3 = st.columns(3)

with cB1:
    autonomy = st.selectbox(
        "Autonomy Level",
        [
            "Choose option",
            "Close supervision",
            "Regular guidance",
            "Independent",
            "Sets direction for others",
            "Defines strategy"
        ]
    )

    prob_solve = st.selectbox(
        "Problem Solving Complexity",
        [
            "Choose option",
            "Routine/Standardized",
            "Moderate analysis",
            "Complex analysis",
            "Novel/Ambiguous",
            "Strategic transformation"
        ]
    )

with cB2:
    knowledge_depth = st.selectbox(
        "Knowledge Depth",
        [
            "Choose option",
            "Entry-level knowledge",
            "Applied technical/professional",
            "Advanced specialized expertise",
            "Recognized expert",
            "World-class mastery"
        ]
    )

    influence_level = st.selectbox(
        "Influence Level",
        [
            "Choose option",
            "Team",
            "Cross-team",
            "Multi-function",
            "External vendors/clients",
            "Industry-level influence"
        ]
    )

with cB3:
    operational_complexity = st.selectbox(
        "Operational Complexity",
        [
            "Choose option",
            "Stable operations",
            "Some variability",
            "High variability",
            "High-risk environment",
            "Ambiguous/Complex systems"
        ]
    )

# ============================================================================
# BLOCO 4 — KNOWLEDGE, KPIs & COMPETENCIES
# ============================================================================
st.markdown("""
<div class="section-title">Knowledge, KPIs & Competencies</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

cC1, cC2, cC3 = st.columns(3)

with cC1:
    education = st.selectbox(
        "Education Level",
        [
            "Choose option",
            "High School",
            "Technical Degree",
            "Bachelor’s",
            "Post-graduate",
            "Master’s",
            "Doctorate"
        ]
    )

    experience = st.selectbox(
        "Experience Level",
        [
            "Choose option",
            "<2 years",
            "2–5 years",
            "5–10 years",
            "10–15 years",
            "15+ years"
        ]
    )

with cC2:
    kpis_selected = st.multiselect(
        "Primary KPIs",
        [
            "Financial",
            "Customer",
            "Operational",
            "Quality",
            "Safety",
            "Compliance",
            "Project Delivery",
            "People Leadership"
        ]
    )

    competencies_selected = st.multiselect(
        "Core Competencies",
        [
            "Communication",
            "Collaboration",
            "Analytical Thinking",
            "Technical Expertise",
            "Leadership",
            "Innovation",
            "Strategic Thinking",
            "Customer Orientation"
        ]
    )

with cC3:
    specialization_level = st.selectbox(
        "Specialization Level",
        [
            "Choose option",
            "Generalist",
            "Functional Specialist",
            "Technical Expert",
            "Market-recognized Expert",
            "Global Authority"
        ]
    )

    innovation_scale = st.selectbox(
        "Innovation Responsibility",
        [
            "Choose option",
            "Execution",
            "Improvement",
            "Recreation",
            "Transformation",
            "Disruption"
        ]
    )

# Liderança
cC4, cC5 = st.columns(2)

with cC4:
    leadership_type = st.selectbox(
        "Leadership Type",
        [
            "Choose option",
            "None",
            "Project leadership",
            "Technical leadership",
            "Direct people management",
            "Matrix leadership",
            "Global leadership"
        ]
    )

with cC5:
    org_influence = st.selectbox(
        "Organizational Influence",
        [
            "Choose option",
            "Team",
            "Department",
            "Function",
            "Business Unit",
            "Company-wide",
            "Industry-level"
        ]
    )

# ============================================================================
# BOTÃO (alinhado à esquerda)
# ============================================================================
btn_col = st.columns([1, 6])[0]
generate = btn_col.button("Generate Job Match Description", use_container_width=False)

# ============================================================================
# VALIDAÇÃO OBRIGATÓRIA DOS CAMPOS
# ============================================================================
all_fields = [
    job_family, sub_job_family,
    job_category, geo_scope, org_impact, span_control,
    nature_work, decision_type, financial_impact,
    stakeholder_complexity, time_horizon,
    autonomy, prob_solve, knowledge_depth,
    influence_level, operational_complexity,
    education, experience,
    specialization_level, innovation_scale,
    leadership_type, org_influence
]

missing_basic = any(x == "Choose option" for x in all_fields)

missing_lists = (len(kpis_selected) == 0 or len(competencies_selected) == 0)

if generate and (missing_basic or missing_lists):
    st.error("Please complete all fields before generating the Job Match Description.")
    st.stop()
# ============================================================================
# MÓDULO 3 — MATCH AUTOMÁTICO + HTML FINAL
# ============================================================================

if generate:

    # --------------------------------------------------------------
    # 1) NORMALIZAÇÃO / CODIFICAÇÃO DE CAMPOS DO FORMULÁRIO
    # --------------------------------------------------------------
    # Cada resposta vira um nível numérico (para poder comparar)
    map_levels = {
        "Local": 1, "Team": 1, "Close supervision": 1,
        "Regional": 2, "Department/Subfunction": 2, "Regular guidance": 2,
        "Multi-country": 3, "Function": 3, "Independent": 3,
        "Global": 4, "Multi-function/BU": 4, "Sets direction for others": 4,
        "Enterprise-wide": 5, "Defines strategy": 5
    }

    def encode(value):
        return map_levels.get(value, 0)

    user_signature = {
        "geo_scope": encode(geo_scope),
        "org_impact": encode(org_impact),
        "autonomy": encode(autonomy),
        "problem_solving": encode(prob_solve),
        "knowledge_depth": encode(knowledge_depth),
        "influence": encode(influence_level),
    }

    # --------------------------------------------------------------
    # 2) FUNÇÕES DE SIMILARIDADE
    # --------------------------------------------------------------
    def score_simple(a, b):
        """Score numérico simples."""
        return 1 if a == b else 0

    def list_overlap(list_user, list_profile):
        """Calcula match percentual entre listas."""
        if not list_profile:
            return 0
        inter = len(set(list_user).intersection(set(list_profile)))
        return inter / len(list_profile)

    # --------------------------------------------------------------
    # 3) CRIA ASSINATURA PARA CADA JOB PROFILE DO EXCEL
    # --------------------------------------------------------------
    df_comp = df_profiles.copy()

    # KPIs e competências do perfil precisam ser listas
    def to_list(x):
        if pd.isna(x):
            return []
        return [i.strip() for i in str(x).split(",")]

    df_comp["kpis_list"] = df_comp["desc_kpis"].apply(to_list)
    df_comp["comp_list"] = (
        df_comp["desc_comp1"].fillna("") + "," +
        df_comp["desc_comp2"].fillna("") + "," +
        df_comp["desc_comp3"].fillna("")
    ).apply(to_list)

    # --------------------------------------------------------------
    # 4) CALCULA SCORE PARA CADA JOB PROFILE
    # --------------------------------------------------------------
    scores = []

    for idx, row in df_comp.iterrows():

        # matching estrutural (WTW)
        s_geo = score_simple(user_signature["geo_scope"], 0)  # sem base no Excel
        s_org = score_simple(user_signature["org_impact"], 0)
        s_aut = score_simple(user_signature["autonomy"], 0)
        s_ps  = score_simple(user_signature["problem_solving"], 0)
        s_kd  = score_simple(user_signature["knowledge_depth"], 0)
        s_inf = score_simple(user_signature["influence"], 0)

        # matching de KPIs + competências
        s_kpi = list_overlap(kpis_selected, row["kpis_list"])
        s_comp = list_overlap(competencies_selected, row["comp_list"])

        final_score = (
            0.40 * (s_geo + s_org) +
            0.30 * (s_aut + s_ps + s_kd + s_inf) +
            0.20 * (s_kpi) +
            0.10 * (s_comp)
        )

        scores.append(final_score)

    df_comp["match_score"] = scores

    # --------------------------------------------------------------
    # 5) SELECIONA O MELHOR PERFIL
    # --------------------------------------------------------------
    best = df_comp.sort_values("match_score", ascending=False).iloc[0]
    score_pct = int(best["match_score"] * 100)

    # Campos do metacard
    mc_job_family = best["job_family"]
    mc_sub_family = best["sub_job_family"]
    mc_career_path = best["career_path"]
    mc_full_code = best["full_job_code"]
    mc_profile = best["job_profile"]
    mc_grade = best["global_grade"]

    # --------------------------------------------------------------
    # 6) RENDERIZA HTML IDÊNTICO AO JOB PROFILE DESCRIPTION
    # --------------------------------------------------------------
    html_code = f"""
<html>
<head>
<meta charset="UTF-8">
<style>

html, body {{
    margin:0;
    padding:0;
    font-family:'Segoe UI', sans-serif;
    background:#faf9f7;
}}

#viewport {{
    height:100vh;
    display:flex;
    flex-direction:column;
    overflow:hidden;
}}

.grid-top {{
    display:grid;
    grid-template-columns:1fr;
    gap:24px;
    width:100%;
}}

.grid-desc {{
    display:grid;
    grid-template-columns:1fr;
    gap:28px;
    width:100%;
}}

.card-top {{
    background:#f5f3ee;
    border-radius:16px;
    padding:22px 24px;
    border:1px solid #e3e1dd;
}}

.title {{
    font-size:20px;
    font-weight:700;
}}

.gg {{
    color:#145efc;
    font-size:16px;
    font-weight:700;
    margin-top:6px;
}}

.meta {{
    background:white;
    padding:14px;
    margin-top:14px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    font-size:14px;
}}

.section-box {{
    padding-bottom:28px;
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
    width:100%;
    margin:8px 0 14px 0;
}}

.section-text {{
    font-size:14px;
    line-height:1.45;
    white-space:pre-wrap;
}}

</style>
</head>

<body>

<div id="viewport">

    <div id="top-area">
        <div class="grid-top">
            <div class="card-top">

                <div class="title">Recommended Match: {html.escape(mc_profile)}</div>
                <div class="gg">Match Score: {score_pct}%</div>

                <div class="meta">
                    <b>Job Family:</b> {html.escape(mc_job_family)}<br>
                    <b>Sub Job Family:</b> {html.escape(mc_sub_family)}<br>
                    <b>Career Path:</b> {html.escape(mc_career_path)}<br>
                    <b>Full Job Code:</b> {html.escape(mc_full_code)}
                </div>

            </div>
        </div>
    </div>

    <div id="scroll-area" style="flex:1; overflow-y:auto; padding:20px 4px 32px 4px;">
        <div class="grid-desc">

            <!-- Sub Job Family Description -->
            <div class="section-box">
                <div class="section-title">Sub Job Family Description</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_sub_family"]))}</div>
            </div>

            <!-- Job Profile Description -->
            <div class="section-box">
                <div class="section-title">Job Profile Description</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_profile"]))}</div>
            </div>

            <!-- Career Band Description -->
            <div class="section-box">
                <div class="section-title">Career Band Description</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_career_band"]))}</div>
            </div>

            <!-- Role Description -->
            <div class="section-box">
                <div class="section-title">Role Description</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_role"]))}</div>
            </div>

            <!-- Grade Differentiator -->
            <div class="section-box">
                <div class="section-title">Grade Differentiator</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_grade_diff"]))}</div>
            </div>

            <!-- Qualifications -->
            <div class="section-box">
                <div class="section-title">Qualifications</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_qualifications"]))}</div>
            </div>

            <!-- KPIs -->
            <div class="section-box">
                <div class="section-title">Specific KPIs</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_kpis"]))}</div>
            </div>

            <!-- Competencies -->
            <div class="section-box">
                <div class="section-title">Competencies 1</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_comp1"]))}</div>
            </div>

            <div class="section-box">
                <div class="section-title">Competencies 2</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_comp2"]))}</div>
            </div>

            <div class="section-box">
                <div class="section-title">Competencies 3</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(best["desc_comp3"]))}</div>
            </div>

        </div>
    </div>

</div>

</body>
</html>
"""

    # Render final
    components.html(html_code, height=1400, scrolling=True)
