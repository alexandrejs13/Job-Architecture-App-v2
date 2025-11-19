# ==========================================================
# JOB MATCH — ARQUIVO FINAL COMPLETO (PARTE 1/4)
# ==========================================================

import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components
import base64
import os

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# CSS SIG — ANTI-ESTICAR + ESTILO DAS OUTRAS PÁGINAS
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

.block-container, .stColumn {
    max-width: 1400px !important;
    margin-left: auto !important;
    margin-right: auto !important;
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
}

/* Labels e títulos */
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

/* Campos obrigatórios vermelhos */
.required-label {
    color: red !important;
    font-weight: 600 !important;
}

.required-box select, .required-box input {
    border: 2px solid red !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# ICONE CABEÇALHO
# ----------------------------------------------------------
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

# ----------------------------------------------------------
# HEADER — PADRÃO SIG
# ----------------------------------------------------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:10px; margin-bottom:8px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:48px; height:48px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:32px;">
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD JOB PROFILE DATA
# ----------------------------------------------------------
@st.cache_data
def load_job_profiles():
    df = pd.read_excel("data/Job Profile.xlsx")

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
        "Competencies 3": "desc_comp3",
    }

    rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=rename_map)
    df.columns = [c.strip() for c in df.columns]

    return df

df_profiles = load_job_profiles()

# ---------------------------
# LOAD SVG ICONS
# ---------------------------
def load_svg(svg_name):
    path = f"assets/icons/sig/{svg_name}"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()
        svg = svg.replace('<?xml version="1.0" encoding="utf-8"?>','')
        return svg

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

# ----------------------------------------------------------
# TÍTULO DO BLOCO 1 — JOB FAMILY INFORMATION
# ----------------------------------------------------------
st.markdown("""
<div class="section-title">Job Family Information</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)
# ==========================================================
# FORMULÁRIO COMPLETO — ORIGINAIS + 10 CAMPOS AVANÇADOS
# Continuação direta do arquivo
# ==========================================================

# --------------------------------------------
# SEÇÃO JOB FAMILY INFORMATION
# --------------------------------------------
col_jf1, col_jf2 = st.columns(2)

job_families = sorted(df_profiles["job_family"].dropna().unique().tolist())

with col_jf1:
    job_family = st.selectbox(
        "Job Family",
        ["Choose option"] + job_families,
        key="job_family"
    )

with col_jf2:
    if job_family == "Choose option":
        sub_job_family = st.selectbox("Sub Job Family", ["Choose option"], key="sub_job_family")
    else:
        subf_list = (
            df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"]
            .dropna()
            .unique()
            .tolist()
        )
        sub_job_family = st.selectbox(
            "Sub Job Family",
            ["Choose option"] + sorted(subf_list),
            key="sub_job_family"
        )

# ==========================================================
# SEÇÃO 1 — STRATEGIC IMPACT & SCOPE
# ==========================================================
st.markdown("""
<div class="section-title">Strategic Impact & Scope</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

c1a, c1b, c1c = st.columns(3)

with c1a:
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
        ["Choose option", "Team", "Department / Subfunction", "Function", "Business Unit", "Enterprise-wide"]
    )

with c1b:
    span_control = st.selectbox(
        "Span of Control",
        ["Choose option", "No direct reports", "Supervises team", "Leads professionals", "Leads multiple teams", "Leads managers"]
    )

    nature_work = st.selectbox(
        "Nature of Work",
        ["Choose option", "Process-oriented", "Analysis-oriented", "Specialist", "Leadership-driven"]
    )

    financial_impact = st.selectbox(
        "Financial Impact",
        ["Choose option", "No impact", "Cost center impact", "Department-level impact", "Business Unit impact", "Company-wide impact"]
    )

with c1c:
    stakeholder_complexity = st.selectbox(
        "Stakeholder Complexity",
        ["Choose option", "Internal team", "Cross-functional", "External vendors", "Customers", "Regulatory/Authorities"]
    )

    decision_type = st.selectbox(
        "Decision Type",
        ["Choose option", "Procedural", "Operational", "Tactical", "Strategic"]
    )

    decision_horizon = st.selectbox(
        "Decision Time Horizon",
        ["Choose option", "Daily", "Weekly", "Monthly", "Annual", "Multi-year"]
    )

# ==========================================================
# SEÇÃO 2 — AUTONOMY & COMPLEXITY
# ==========================================================
st.markdown("""
<div class="section-title">Autonomy & Complexity</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

c2a, c2b, c2c = st.columns(3)

with c2a:
    autonomy = st.selectbox(
        "Autonomy Level",
        ["Choose option", "Close supervision", "Regular guidance", "Independent", "Sets direction for others", "Defines strategy"]
    )

    problem_solving = st.selectbox(
        "Problem Solving Complexity",
        ["Choose option", "Routine/Standardized", "Moderate", "Complex", "Ambiguous/Novel", "Organization-level"]
    )

with c2b:
    knowledge_depth = st.selectbox(
        "Knowledge Depth",
        ["Choose option", "Entry-level knowledge", "Applied knowledge", "Advanced expertise", "Recognized expert", "Thought leader"]
    )

    operational_complexity = st.selectbox(
        "Operational Complexity",
        ["Choose option", "Stable operations", "Some variability", "Complex operations", "High-variability environment"]
    )

with c2c:
    influence_level = st.selectbox(
        "Influence Level",
        ["Choose option", "Team", "Cross-team", "Multi-function", "External vendors/clients", "Industry-level influence"]
    )

# ==========================================================
# SEÇÃO 3 — KNOWLEDGE, KPIs & COMPETENCIES
# ==========================================================
st.markdown("""
<div class="section-title">Knowledge, KPIs & Competencies</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

c3a, c3b, c3c = st.columns(3)

with c3a:
    education = st.selectbox(
        "Education Level",
        ["Choose option", "High School", "Technical Degree", "Bachelor’s", "Post-graduate", "Master’s", "Doctorate"]
    )

    experience = st.selectbox(
        "Experience Level",
        ["Choose option", "< 2 years", "2–5 years", "5–10 years", "10–15 years", "15+ years"]
    )

with c3b:
    kpis_selected = st.multiselect(
        "Primary KPIs",
        ["Financial", "Customer", "Operational", "Quality", "Safety", "Compliance", "Project Delivery", "People Leadership"]
    )

    specialization_level = st.selectbox(
        "Specialization Level",
        ["Choose option", "Generalist", "Specialist", "Deep Specialist"]
    )

with c3c:
    competencies_selected = st.multiselect(
        "Core Competencies",
        ["Communication", "Collaboration", "Analytical Thinking", "Technical Expertise", "Leadership", "Innovation", "Strategic Thinking", "Customer Orientation"]
    )

    innovation_resp = st.selectbox(
        "Innovation Responsibility",
        ["Choose option", "Execution", "Incremental improvements", "Major improvements", "Innovation leadership"]
    )

# Linha extra
c3d, c3e = st.columns(2)

with c3d:
    leadership_type = st.selectbox(
        "Leadership Type",
        ["Choose option", "None", "Team Lead", "Supervisor", "Manager", "Senior Manager", "Director"]
    )

with c3e:
    org_influence = st.selectbox(
        "Organizational Influence",
        ["Choose option", "Team", "Department", "Business Unit", "Function", "Enterprise-wide"]
    )

# ----------------------------------------------------------
# BOTÃO GERAR
# ----------------------------------------------------------
col_button = st.columns([1, 6, 1])[0]
with col_button:
    generate = st.button("Generate Job Match Description", use_container_width=True)
# ==========================================================
# PARTE 3 — VALIDAÇÃO + HARD FILTER + MATCH ENGINE WTW
# ==========================================================

# -------------------------------
# 1) VALIDAÇÃO OBRIGATÓRIA
# -------------------------------
required_fields = {
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

errors = []

for label, value in required_fields.items():
    if value == "Choose option" or value == "":
        errors.append(label)

# KPIs e Competências são lists → obrigatórios
if len(kpis_selected) == 0:
    errors.append("Primary KPIs")

if len(competencies_selected) == 0:
    errors.append("Core Competencies")

# -------------------------------
# 2) EXIBIR ERROS, SE HOUVER
# -------------------------------
if generate and len(errors) > 0:
    st.error("Please fill in all required fields before generating the match.")
    for e in errors:
        st.markdown(f"<div class='required-label'>• {e}</div>", unsafe_allow_html=True)
    st.stop()

# -------------------------------
# 3) SE CHEGOU AQUI, ESTÁ TUDO OK
# -------------------------------

if generate:

    # ==========================================================
    # HARD FILTER TOTAL — WTW (IMPEDITIVO)
    # ==========================================================
    df_filtered = df_profiles.copy()

    df_filtered = df_filtered[
        (df_filtered["job_family"] == job_family) &
        (df_filtered["sub_job_family"] == sub_job_family)
    ]

    if df_filtered.empty:
        st.error("No Job Profiles match the selected Job Family + Sub Job Family.")
        st.stop()

    # ==========================================================
    # 4) NORMALIZAÇÃO DOS PARÂMETROS EM ESCALAS NUMÉRICAS
    # ==========================================================

    encode_map = {
        "Choose option": 0,

        # JOB CATEGORY
        "Executive": 5, "Manager": 4, "Professional": 3,
        "Technical Support": 2, "Business Support": 2, "Production": 1,

        # GEOGRAPHIC SCOPE
        "Local": 1, "Regional": 2, "Multi-country": 3, "Global": 4,

        # ORG IMPACT
        "Team": 1, "Department / Subfunction": 2,
        "Function": 3, "Business Unit": 4, "Enterprise-wide": 5,

        # SPAN OF CONTROL
        "No direct reports": 1, "Supervises team": 2, "Leads professionals": 3,
        "Leads multiple teams": 4, "Leads managers": 5,

        # NATURE OF WORK
        "Process-oriented": 1, "Analysis-oriented": 2,
        "Specialist": 3, "Leadership-driven": 4,

        # FINANCIAL IMPACT
        "No impact": 1, "Cost center impact": 2,
        "Department-level impact": 3, "Business Unit impact": 4,
        "Company-wide impact": 5,

        # STAKEHOLDERS
        "Internal team": 1, "Cross-functional": 2,
        "External vendors": 3, "Customers": 4, "Regulatory/Authorities": 5,

        # DECISION TYPE
        "Procedural": 1, "Operational": 2, "Tactical": 3, "Strategic": 4,

        # DECISION HORIZON
        "Daily": 1, "Weekly": 2, "Monthly": 3,
        "Annual": 4, "Multi-year": 5,

        # AUTONOMY
        "Close supervision": 1, "Regular guidance": 2, "Independent": 3,
        "Sets direction for others": 4, "Defines strategy": 5,

        # PROBLEM SOLVING
        "Routine/Standardized": 1, "Moderate": 2,
        "Complex": 3, "Ambiguous/Novel": 4, "Organization-level": 5,

        # KNOWLEDGE DEPTH
        "Entry-level knowledge": 1, "Applied knowledge": 2,
        "Advanced expertise": 3, "Recognized expert": 4, "Thought leader": 5,

        # OPERATIONAL COMPLEXITY
        "Stable operations": 1, "Some variability": 2,
        "Complex operations": 3, "High-variability environment": 4,

        # INFLUENCE
        "Team": 1, "Cross-team": 2, "Multi-function": 3,
        "External vendors/clients": 4, "Industry-level influence": 5,

        # SPECIALIZATION LEVEL
        "Generalist": 1, "Specialist": 2, "Deep Specialist": 3,

        # INNOVATION RESPONSIBILITY
        "Execution": 1,
        "Incremental improvements": 2,
        "Major improvements": 3,
        "Innovation leadership": 4,

        # LEADERSHIP TYPE
        "None": 1, "Team Lead": 2, "Supervisor": 3,
        "Manager": 4, "Senior Manager": 5, "Director": 6,

        # ORGANIZATIONAL INFLUENCE
        "Team": 1, "Department": 2,
        "Business Unit": 3, "Function": 4, "Enterprise-wide": 5,

        # EDUCATION
        "High School": 1, "Technical Degree": 2, "Bachelor’s": 3,
        "Post-graduate": 4, "Master’s": 5, "Doctorate": 6,

        # EXPERIENCE
        "< 2 years": 1, "2–5 years": 2, "5–10 years": 3,
        "10–15 years": 4, "15+ years": 5,
    }

    def enc(x):
        return encode_map.get(x, 0)

    # ==========================================================
    # 5) USER SIGNATURE (assinatura completa)
    # ==========================================================
    user_sig = {
        "cat": enc(job_category),
        "geo": enc(geo_scope),
        "impact": enc(org_impact),
        "span": enc(span_control),
        "nature": enc(nature_work),
        "finimp": enc(financial_impact),
        "stake": enc(stakeholder_complexity),
        "dtype": enc(decision_type),
        "dhoriz": enc(decision_horizon),

        "auto": enc(autonomy),
        "ps": enc(problem_solving),
        "kdepth": enc(knowledge_depth),
        "opcomp": enc(operational_complexity),
        "infl": enc(influence_level),

        "edu": enc(education),
        "exp": enc(experience),
        "spec": enc(specialization_level),
        "innov": enc(innovation_resp),
        "lead": enc(leadership_type),
        "orginf": enc(org_influence),
    }

    # ==========================================================
    # 6) KPIs / Competências como LISTAS
    # ==========================================================
    def clean_list(x):
        if pd.isna(x): return []
        return [i.strip() for i in str(x).split(",") if i.strip()]

    df_filtered["kpis_list"] = df_filtered["desc_kpis"].apply(clean_list)

    df_filtered["comp_list"] = (
        df_filtered["desc_comp1"].fillna("") + "," +
        df_filtered["desc_comp2"].fillna("") + "," +
        df_filtered["desc_comp3"].fillna("")
    ).apply(clean_list)

    # ==========================================================
    # 7) SCORE CALCULATION — WTW-STYLE
    # ==========================================================

    def overlap(a, b):
        if not b: return 0
        return len(set(a).intersection(set(b))) / len(b)

    scores = []

    for idx, row in df_filtered.iterrows():

        # Distância de grade → penalidade sutil
        if abs(int(row["global_grade"]) - user_sig["lead"]) > 4:
            grade_penalty = -0.15
        else:
            grade_penalty = 0

        # Similaridade estrutural
        structural = (
            abs(user_sig["geo"] - 0) +
            abs(user_sig["impact"] - 0) +
            abs(user_sig["auto"] - 0) +
            abs(user_sig["ps"] - 0) +
            abs(user_sig["kdepth"] - 0)
        )

        # KPIs
        kpi_score = overlap(kpis_selected, row["kpis_list"])

        # Competências
        comp_score = overlap(competencies_selected, row["comp_list"])

        # Score final ponderado
        final_score = (
            0.40 * (user_sig["geo"] + user_sig["impact"] + user_sig["auto"] + user_sig["ps"] + user_sig["kdepth"]) +
            0.20 * (user_sig["dtype"] + user_sig["dhoriz"] + user_sig["opcomp"]) +
            0.20 * (kpi_score * 5) +
            0.15 * (comp_score * 5) +
            0.05 * (user_sig["edu"] + user_sig["exp"])
            +
            grade_penalty
        )

        scores.append(final_score)

    df_filtered["match_score"] = scores

    # ==========================================================
    # 8) SELECIONAR MELHOR PERFIL
    # ==========================================================
    best = df_filtered.sort_values("match_score", ascending=False).iloc[0]
    score_pct = int((best["match_score"] / df_filtered["match_score"].max()) * 100)
# ==========================================================
# PARTE 4 — HTML FINAL (IDÊNTICO AO JOB PROFILE DESCRIPTION)
# ==========================================================

    # ------------------------------------------------------
    # Campos do metacard
    # ------------------------------------------------------
    mc_job_family = best["job_family"]
    mc_sub_family = best["sub_job_family"]
    mc_career_path = best["career_path"]
    mc_full_code = best["full_job_code"]
    mc_profile = best["job_profile"]
    mc_grade = best["global_grade"]

    # ------------------------------------------------------
    # HTML FINAL — layout SIG idêntico
    # ------------------------------------------------------
    html_code = f"""
<html>
<head>
<meta charset="UTF-8">
<style>

html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #faf9f7;
}}

#viewport {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* Top card grid */
.grid-top {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
    width: 100%;
    padding-right: 8px;
}}

/* Full description grid */
.grid-desc {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 28px;
    width: 100%;
    padding-right: 8px;
}}

/* Metacard */
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

.section-box {{
    padding-bottom: 28px;
}}

.section-title {{
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.section-title svg {{
    width: 20px;
    height: 20px;
}}

.section-line {{
    height: 1px;
    background: #e8e6e1;
    width: 100%;
    margin: 8px 0 14px 0;
}}

.section-text {{
    font-size: 14px;
    line-height: 1.45;
    white-space: pre-wrap;
}}

#scroll-area {{
    flex: 1;
    overflow-y: auto;
    padding: 20px 4px 32px 4px;
}}

</style>
</head>

<body>

<div id="viewport">

    <!-- METACARD -->
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

    <!-- MAIN DESCRIPTION -->
    <div id="scroll-area">
        <div class="grid-desc">
    """

    # ------------------------------------------------------
    # MULTI-SEÇÃO — RENDER COM SVG INLINE
    # ------------------------------------------------------
    sections = [
        ("Sub Job Family Description", "desc_sub_family"),
        ("Job Profile Description", "desc_profile"),
        ("Career Band Description", "desc_career_band"),
        ("Role Description", "desc_role"),
        ("Grade Differentiator", "desc_grade_diff"),
        ("Qualifications", "desc_qualifications"),
        ("Specific parameters / KPIs", "desc_kpis"),
        ("Competencies 1", "desc_comp1"),
        ("Competencies 2", "desc_comp2"),
        ("Competencies 3", "desc_comp3"),
    ]

    for sec_title, col in sections:
        icon_svg = icons_svg.get(sec_title, "")
        value = best.get(col, "")

        html_code += f"""
        <div class="section-box">
            <div class="section-title">{icon_svg} {html.escape(sec_title)}</div>
            <div class="section-line"></div>
            <div class="section-text">{html.escape(str(value))}</div>
        </div>
        """

    html_code += """
        </div>
    </div>

</div>

</body>
</html>
"""

    # ------------------------------------------------------
    # RENDERIZAÇÃO FINAL
    # ------------------------------------------------------
    components.html(html_code, height=1400, scrolling=True)
