# ==========================================================
# PAGE 5 — JOB MATCH (PARTE 1 DE 3)
# Arquivo completo será montado juntando PARTE 1 + PARTE 2 + PARTE 3
# ==========================================================

import streamlit as st
import pandas as pd
import html
import base64
import os
import streamlit.components.v1 as components

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# GLOBAL CSS — identidade SIG, mesma das outras páginas
# ----------------------------------------------------------
st.markdown("""
<style>

    /* Container principal do Streamlit */
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

    .divider-line {
        height: 1px;
        background: #d9d9d9;
        margin: 6px 0 20px 0;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 34px;
        margin-bottom: 2px;
    }

    /* CAIXA DE ERRO */
    .error-label {
        color: #d00000 !important;
        font-weight: 700 !important;
    }

    .error-border > div > div > select,
    .error-border > div > div > input {
        border: 2px solid #d00000 !important;
    }

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD ICON FUNCTION
# ----------------------------------------------------------
def load_icon_png(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return ""

# ----------------------------------------------------------
# HEADER SIG — ÍCONE + TÍTULO
# ----------------------------------------------------------
page_icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:14px;">
    <img src="data:image/png;base64,{page_icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:36px;">
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD JOB PROFILES (MESMO ARQUIVO DA OUTRA PÁGINA)
# ----------------------------------------------------------
@st.cache_data
def load_job_profiles():
    df = pd.read_excel("data/Job Profile.xlsx")
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
    return df

df_profiles = load_job_profiles()

# ----------------------------------------------------------
# LOAD SVG ICONS (MESMOS DA PÁGINA JOB PROFILE DESCRIPTION)
# ----------------------------------------------------------
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
    "Competencies 3": load_svg("Setting_Cog.svg")
}

# ----------------------------------------------------------
# INÍCIO DO FORMULÁRIO (PARTE 2 VEM DEPOIS)
# ----------------------------------------------------------

st.markdown("""
<div class="section-title">Job Family Information</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

# ==========================================================
# FORMULÁRIO COMPLETO — ORIGINAIS + 10 CAMPOS AVANÇADOS
# ==========================================================

def field_error(label, condition):
    """Retorna classes CSS para marcar título e caixa em vermelho."""
    if condition:
        return ("error-label", {"class": "error-border"})
    return ("", {})

# --------------------------------------------
# SEÇÃO JOB FAMILY INFORMATION
# --------------------------------------------
col_jf1, col_jf2 = st.columns(2)

job_families = sorted(df_profiles["job_family"].dropna().unique().tolist())

# ---- JOB FAMILY ----
err_class, err_box = field_error("Job Family", False)

with col_jf1:
    job_family = st.selectbox(
        "**Job Family**",
        ["Choose option"] + job_families,
        key="job_family",
        help="Select the Job Family"
    )

# ---- SUB JOB FAMILY ----
with col_jf2:
    if job_family == "Choose option":
        sub_job_family = st.selectbox("**Sub Job Family**", ["Choose option"], key="sub_job_family")
    else:
        subf_list = (
            df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"]
            .dropna()
            .unique()
            .tolist()
        )
        sub_job_family = st.selectbox(
            "**Sub Job Family**",
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
# BOTÃO GERAR — AZUL LARGO
# ----------------------------------------------------------
col_button = st.columns([1, 3, 8])[1]
with col_button:
    generate = st.button(
        "Generate Job Match Description",
        use_container_width=True
    )

# ==========================================================
# PARTE 3 — VALIDAÇÃO + MATCH ENGINE + DESCRIÇÃO HTML
# ==========================================================

# Lista de campos obrigatórios (texto → variável)
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
    "Organizational Influence": org_influence
}

# campos multiselect
required_multi = {
    "Primary KPIs": kpis_selected,
    "Core Competencies": competencies_selected
}

# ----------------------------------------------------------
# EXECUTA MATCH APENAS SE CLICAR NO BOTÃO
# ----------------------------------------------------------
if generate:

    missing = []

    # Campos simples
    for label, value in required_fields.items():
        if value == "Choose option":
            missing.append(label)

    # Campos múltiplos
    for label, value in required_multi.items():
        if len(value) == 0:
            missing.append(label)

    # Se tiver campo faltando → mostra erro
    if missing:
        st.error("Please fill all required fields.")

        # deixa tudo vermelho
        for m in missing:
            st.markdown(f"<p class='error-label'>{m} is required.</p>", unsafe_allow_html=True)

        st.stop()

    # ------------------------------------------------------
    # MATCH ENGINE — Versão A refinada
    # ------------------------------------------------------

    df_filtered = df_profiles[
        (df_profiles["job_family"] == job_family) &
        (df_profiles["sub_job_family"] == sub_job_family)
    ].copy()

    if df_filtered.empty:
        st.error("No Job Profiles found for the selected Job Family and Sub Job Family.")
        st.stop()

    def score_match(row):
        score = 0

        # pesos principais
        if row["career_path"] == job_category:
            score += 20

        if row["job_family"] == job_family:
            score += 25

        if row["sub_job_family"] == sub_job_family:
            score += 25

        # Cross-similarity leve
        if any(kpi in str(row.get("specific_parameters_/_kpis", "")).lower() for kpi in [k.lower() for k in kpis_selected]):
            score += 10

        if any(comp in str(row.get("competencies_1", "")).lower() for comp in [c.lower() for c in competencies_selected]):
            score += 10

        return score

    df_filtered["match_score"] = df_filtered.apply(score_match, axis=1)
    df_filtered = df_filtered.sort_values("match_score", ascending=False)

    best_profile = df_filtered.iloc[0].to_dict()

    # ------------------------------------------------------
    # GERA HTML EXACTAMENTE IGUAL AO JOB PROFILE DESCRIPTION
    # ------------------------------------------------------

    sections = [
        "sub_job_family_description",
        "job_profile_description",
        "career_band_description",
        "role_description",
        "grade_differentiator",
        "qualifications",
        "specific_parameters_/_kpis",
        "competencies_1",
        "competencies_2",
        "competencies_3"
    ]

    def build_html_single(profile):

        html_code = """
        <html>
        <head>
        <meta charset="UTF-8">
        <style>

        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: #ffffff;
        }

        .card-top {
            background: #f5f3ee;
            border-radius: 16px;
            padding: 22px 24px;
            border: 1px solid #e3e1dd;
            margin-bottom: 28px;
        }

        .title {
            font-size: 20px;
            font-weight: 700;
        }

        .gg {
            color: #145efc;
            font-size: 16px;
            font-weight: 700;
            margin-top: 6px;
        }

        .meta {
            background: white;
            padding: 14px;
            margin-top: 14px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            font-size: 14px;
        }

        .section-title {
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .section-line {
            height: 1px;
            background: #e8e6e1;
            width: 100%;
            margin: 8px 0 14px 0;
        }

        .section-text {
            font-size: 14px;
            line-height: 1.45;
            white-space: pre-wrap;
        }

        .icon-inline {
            height: 20px;
            width: 20px;
        }

        </style>
        </head>
        <body>
        """

        # TOP CARD
        html_code += f"""
        <div class="card-top">
            <div class="title">{html.escape(str(profile["job_profile"]))}</div>
            <div class="gg">GG {html.escape(str(profile["global_grade"]))}</div>

            <div class="meta">
                <b>Job Family:</b> {html.escape(str(profile["job_family"]))}<br>
                <b>Sub Job Family:</b> {html.escape(str(profile["sub_job_family"]))}<br>
                <b>Career Path:</b> {html.escape(str(profile["career_path"]))}<br>
                <b>Full Job Code:</b> {html.escape(str(profile["full_job_code"]))}
            </div>
        </div>
        """

        # SECTIONS
        for sec in sections:
            nice_label = sec.replace("_", " ").title()
            icon = icons_svg.get(nice_label, "")

            html_code += f"""
            <div class="section-title">
                <span class="icon-inline">{icon}</span>
                {html.escape(nice_label)}
            </div>
            <div class="section-line"></div>
            <div class="section-text">{html.escape(str(profile.get(sec, "")))}</div>
            """

        html_code += "</body></html>"
        return html_code

    final_html = build_html_single(best_profile)

    # Render final
    components.html(final_html, height=1800, scrolling=False)

