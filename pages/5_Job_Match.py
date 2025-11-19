# ==========================================================
# match_engine.py — Engine responsável por:
# 1) Normalização dos dados selecionados pelo usuário
# 2) Validação de campos obrigatórios
# 3) Cálculo do score baseado em pesos
# 4) Seleção do melhor Job Profile
# ==========================================================

import pandas as pd

# ----------------------------------------------------------
# VALORES PADRONIZADOS (para normalização)
# ----------------------------------------------------------
def normalize(value):
    """Converte None, vazio, placeholder em vazio real."""
    if value is None:
        return ""
    if isinstance(value, str) and value.strip().lower() in ["choose option", "select option", ""]:
        return ""
    return value


# ----------------------------------------------------------
# LISTA DE CAMPOS OBRIGATÓRIOS NO FORMULÁRIO
# (Eles devem ser exatamente os mesmos nomes usados no 5_Job_Match)
# ----------------------------------------------------------
REQUIRED_FIELDS = [
    "Job Family",
    "Sub Job Family",
    "Job Category",
    "Span of Control",
    "Financial Impact",
    "Geographic Scope",
    "Stakeholder Complexity",
    "Organizational Impact",
    "Nature of Work",
    "Decision Type",
    "Decision Time Horizon",
    "Autonomy Level",
    "Knowledge Depth",
    "Problem Solving Complexity",
    "Operational Complexity",
    "Influence Level",
    "Education Level",
    "Experience Level",
    "Specialization Level",
    "Innovation Responsibility",
    "Leadership Type",
    "Organizational Influence"
]


# ----------------------------------------------------------
# FUNÇÃO: validar campos
# Retorna:
#   (is_valid, missing_fields)
# ----------------------------------------------------------
def validate_user_inputs(user_inputs: dict):
    missing = [f for f in REQUIRED_FIELDS if normalize(user_inputs.get(f, "")) == ""]
    return len(missing) == 0, missing


# ----------------------------------------------------------
# DICIONÁRIO DE PESOS
# (Peso maior = maior impacto no match)
# ----------------------------------------------------------
WEIGHTS = {
    "Job Category": 4,
    "Span of Control": 4,
    "Financial Impact": 4,
    "Geographic Scope": 3,
    "Organizational Impact": 3,
    "Stakeholder Complexity": 3,
    "Decision Type": 3,
    "Decision Time Horizon": 3,
    "Nature of Work": 2,
    "Autonomy Level": 2,
    "Problem Solving Complexity": 2,
    "Knowledge Depth": 2,
    "Operational Complexity": 2,
    "Influence Level": 2,
    "Experience Level": 2,
    "Specialization Level": 1,
    "Innovation Responsibility": 1,
    "Education Level": 1,
    "Leadership Type": 1,
    "Organizational Influence": 1,
}


# ----------------------------------------------------------
# FUNÇÃO PRINCIPAL: gerar match e score
# ----------------------------------------------------------
def compute_match(user_inputs: dict, df_profiles: pd.DataFrame):
    """
    user_inputs = dicionário com todos os valores selecionados
    df_profiles = dataframe carregado do Job Profile.xlsx
    """

    # Normalize inputs
    ui = {k: normalize(v) for k, v in user_inputs.items()}

    # VALIDAÇÃO
    valid, missing = validate_user_inputs(ui)
    if not valid:
        return None, missing

    # Agora começamos a calcular o score
    scores = []

    for idx, row in df_profiles.iterrows():

        profile_score = 0
        max_score = 0

        # Vamos comparar campo a campo
        for field, weight in WEIGHTS.items():
            max_score += weight

            # EXEMPLO:
            # Campo "Job Category" mapeia para coluna "job_category"
            df_col = field.lower().replace(" ", "_")

            # Se o dataframe não tiver a coluna, ignora
            if df_col not in df_profiles.columns:
                continue

            profile_value = normalize(row[df_col])
            user_value = ui[field]

            # Score: bateu exatamente → ganha peso
            if profile_value == user_value:
                profile_score += weight

        # Normaliza score final (%)
        final_percentage = int((profile_score / max_score) * 100)

        scores.append({
            "profile_index": idx,
            "Job Profile": row["job_profile"],
            "Job Family": row["job_family"],
            "Sub Job Family": row["sub_job_family"],
            "Career Path": row["career_path"],
            "Full Job Code": row["full_job_code"],
            "score": final_percentage,
        })

    # Ordena do maior score para o menor
    scores_sorted = sorted(scores, key=lambda x: x["score"], reverse=True)

    # Melhor match
    best = scores_sorted[0] if scores_sorted else None

    return best, []


# ==========================================================
# html_renderer.py
# Renderiza o HTML bonito no padrão SIG para o Job Match
# ==========================================================

import html
import os

# ----------------------------------------------------------
# FUNÇÃO PARA CARREGAR SVG INLINE
# ----------------------------------------------------------
def load_svg(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------
# MAPA DE ÍCONES — exatamente o mesmo do Job Profile Description
# ----------------------------------------------------------
ICONS = {
    "Sub Job Family Description": "assets/icons/sig/Hierarchy.svg",
    "Job Profile Description": "assets/icons/sig/Content_Book_Phone.svg",
    "Career Band Description": "assets/icons/sig/File_Clipboard_Text.svg",
    "Role Description": "assets/icons/sig/Shopping_Business_Target.svg",
    "Grade Differentiator": "assets/icons/sig/User_Add.svg",
    "Qualifications": "assets/icons/sig/Edit_Pencil.svg",
    "Specific parameters / KPIs": "assets/icons/sig/Graph_Bar.svg",
    "Competencies 1": "assets/icons/sig/Setting_Cog.svg",
    "Competencies 2": "assets/icons/sig/Setting_Cog.svg",
    "Competencies 3": "assets/icons/sig/Setting_Cog.svg",
}


# ----------------------------------------------------------
# LISTA NA ORDEM CORRETA DAS SEÇÕES
# ----------------------------------------------------------
SECTION_ORDER = [
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


# ----------------------------------------------------------
# FUNÇÃO PRINCIPAL → monta HTML completo
# ----------------------------------------------------------
def render_job_match_description(best_profile: dict, df_profiles):
    """
    Recebe o dicionário do best match (já obtido no engine)
    e devolve o HTML SIG completo
    """

    idx = best_profile["profile_index"]
    row = df_profiles.loc[idx]

    # ------------------------------------------------------
    # TOPO — card principal
    # ------------------------------------------------------
    title = html.escape(row["job_profile"])
    jf = html.escape(row["job_family"])
    sf = html.escape(row["sub_job_family"])
    cp = html.escape(row["career_path"])
    code = html.escape(row["full_job_code"])

    # ------------------------------------------------------
    # HTML CORE
    # ------------------------------------------------------
    html_code = f"""
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: white;
            margin: 0;
            padding: 0;
        }}

        .header-card {{
            background: #f5f3ee;
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 28px;
            border: 1px solid #e3e1dd;
        }}

        .job-title {{
            font-size: 28px;
            font-weight: 700;
            margin: 0;
            padding: 0;
            color: #000;
        }}

        .gg {{
            color: #145efc;
            font-size: 18px;
            font-weight: 700;
            margin-top: 6px;
        }}

        .meta {{
            background: white;
            padding: 16px;
            margin-top: 16px;
            border-radius: 12px;
            border: 1px solid #eceae5;
            font-size: 14px;
            line-height: 1.4;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 28px;
        }}

        .divider-line {{
            height: 1px;
            background: #e6e4df;
            margin: 10px 0 18px 0;
        }}

        .section-text {{
            font-size: 15px;
            line-height: 1.5;
            white-space: pre-wrap;
        }}

        .icon-inline {{
            width: 22px;
            height: 22px;
        }}
    </style>

    <div class="header-card">
        <div class="job-title">{title}</div>
        <div class="gg">GG {html.escape(str(row["global_grade"]))}</div>

        <div class="meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {code}
        </div>
    </div>
    """

    # ------------------------------------------------------
    # SEÇÕES COM TEXTO
    # ------------------------------------------------------
    for sec in SECTION_ORDER:
        col_name = sec  # coluna igual ao nome na planilha

        if col_name not in df_profiles.columns:
            continue

        content = html.escape(str(row[col_name])) if pd.notna(row[col_name]) else ""

        icon_path = ICONS.get(sec, "")
        icon_svg = load_svg(icon_path) if icon_path else ""

        html_code += f"""
            <div class="section-title">
                <span class="icon-inline">{icon_svg}</span>
                {html.escape(sec)}
            </div>
            <div class="divider-line"></div>
            <div class="section-text">{content}</div>
        """

    return html_code


# ==========================================================
# PAGE — JOB MATCH (Página 5)
# ==========================================================

import streamlit as st
import pandas as pd
import html
import base64
import os

from match_engine import compute_match
from html_renderer import render_job_match_description

# ----------------------------------------------------------
# CONFIGURAÇÃO DE PÁGINA
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# CSS SIG COMPLETO
# ----------------------------------------------------------
st.markdown("""
<style>

    /* =========================== */
    /* CONTAINER CENTRAL */
    /* =========================== */
    .main > div {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* =========================== */
    /* BOTÃO AZUL */
    /* =========================== */
    .blue-btn > button {
        background-color: #145efc !important;
        color: white !important;
        font-size: 18px !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        width: 420px !important;   /* LARGO */
        border: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    /* =========================== */
    /* MENSAGEM DE ERRO */
    /* =========================== */
    .error-box {
        background: #fdecec;
        border-left: 6px solid #e63946;
        padding: 16px;
        border-radius: 8px;
        font-size: 18px;
        margin-top: 18px;
        color: #9d1c1c;
    }

    .error-label {
        color: #d90429 !important;
        font-weight: 700;
        margin-bottom: 4px !important;
        display: block !important;
        font-size: 16px !important;
    }

    /* =========================== */
    /* BORDA VERMELHA */
    /* =========================== */
    .error-border select, .error-border div[data-baseweb="select"],
    .error-border input {
        border: 2px solid #d90429 !important;
        border-radius: 6px !important;
    }

    /* =========================== */
    /* DIVISOR DOS TÍTULOS */
    /* =========================== */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 6px;
    }

    .divider-line {
        height: 1px;
        background: #dedad3;
        margin-bottom: 20px;
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


# ==========================================================
# FUNÇÃO — CHECK REQUIRED
# ==========================================================
def validate_required(fields_dict):
    """
    Recebe dict: {field_name: valor}
    Retorna: lista de campos vazios
    """
    missing = []
    for label, value in fields_dict.items():
        if value == "Choose option" or value == "" or value is None:
            missing.append(label)
    return missing


# ==========================================================
# TÍTULO DA PÁGINA
# ==========================================================
st.markdown("""
<div style="display:flex; align-items:center; gap:18px; margin-bottom:6px; margin-top:10px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:36px;">
""", unsafe_allow_html=True)



# ==========================================================
# FORMULÁRIO COMPLETO — ORIGINAIS + 10 CAMPOS AVANÇADOS
# ==========================================================

# --------------------------------------------
# SEÇÃO JOB FAMILY INFORMATION
# --------------------------------------------

st.markdown("""<div class="section-title">Job Family Information</div>
<div class="divider-line"></div>""", unsafe_allow_html=True)

col_jf1, col_jf2 = st.columns(2)

job_families = sorted(df_profiles["job_family"].dropna().unique().tolist())

with col_jf1:
    job_family = st.selectbox("Job Family",
                              ["Choose option"] + job_families)

with col_jf2:
    if job_family == "Choose option":
        sub_job_family = st.selectbox("Sub Job Family",
                                      ["Choose option"])
    else:
        subs = (df_profiles[df_profiles["job_family"] == job_family]
                ["sub_job_family"].dropna().unique().tolist())
        sub_job_family = st.selectbox("Sub Job Family",
                                      ["Choose option"] + sorted(subs))


# ==========================================================
# SECTION 1 — STRATEGIC IMPACT & SCOPE
# ==========================================================
st.markdown("""
<div class="section-title">Strategic Impact & Scope</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

c1a, c1b, c1c = st.columns(3)

with c1a:
    job_category = st.selectbox("Job Category",
                                ["Choose option", "Executive", "Manager",
                                 "Professional", "Technical Support",
                                 "Business Support", "Production"])

    geo_scope = st.selectbox("Geographic Scope",
                             ["Choose option", "Local", "Regional",
                              "Multi-country", "Global"])

    org_impact = st.selectbox("Organizational Impact",
                              ["Choose option", "Team",
                               "Department / Subfunction",
                               "Function", "Business Unit",
                               "Enterprise-wide"])

with c1b:
    span_control = st.selectbox("Span of Control",
                                ["Choose option", "No direct reports",
                                 "Supervises team", "Leads professionals",
                                 "Leads multiple teams", "Leads managers"])

    nature_work = st.selectbox("Nature of Work",
                               ["Choose option", "Process-oriented",
                                "Analysis-oriented", "Specialist",
                                "Leadership-driven"])

    financial_impact = st.selectbox("Financial Impact",
                                    ["Choose option", "No impact",
                                     "Cost center impact",
                                     "Department-level impact",
                                     "Business Unit impact",
                                     "Company-wide impact"])

with c1c:
    stakeholder_complexity = st.selectbox("Stakeholder Complexity",
                                          ["Choose option", "Internal team",
                                           "Cross-functional",
                                           "External vendors",
                                           "Customers",
                                           "Regulatory/Authorities"])

    decision_type = st.selectbox("Decision Type",
                                 ["Choose option", "Procedural",
                                  "Operational", "Tactical", "Strategic"])

    decision_horizon = st.selectbox("Decision Time Horizon",
                                    ["Choose option", "Daily", "Weekly",
                                     "Monthly", "Annual", "Multi-year"])


# ==========================================================
# SECTION 2 — AUTONOMY & COMPLEXITY
# ==========================================================
st.markdown("""
<div class="section-title">Autonomy & Complexity</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

c2a, c2b, c2c = st.columns(3)

with c2a:
    autonomy = st.selectbox("Autonomy Level",
                            ["Choose option", "Close supervision",
                             "Regular guidance", "Independent",
                             "Sets direction for others",
                             "Defines strategy"])

    problem_solving = st.selectbox("Problem Solving Complexity",
                                   ["Choose option", "Routine/Standardized",
                                    "Moderate", "Complex",
                                    "Ambiguous/Novel",
                                    "Organization-level"])

with c2b:
    knowledge_depth = st.selectbox("Knowledge Depth",
                                   ["Choose option", "Entry-level knowledge",
                                    "Applied knowledge", "Advanced expertise",
                                    "Recognized expert", "Thought leader"])

    operational_complexity = st.selectbox("Operational Complexity",
                                          ["Choose option", "Stable operations",
                                           "Some variability",
                                           "Complex operations",
                                           "High-variability environment"])

with c2c:
    influence_level = st.selectbox("Influence Level",
                                   ["Choose option", "Team", "Cross-team",
                                    "Multi-function",
                                    "External vendors/clients",
                                    "Industry-level influence"])


# ==========================================================
# SECTION 3 — KNOWLEDGE, KPIs & COMPETENCIES
# ==========================================================
st.markdown("""
<div class="section-title">Knowledge, KPIs & Competencies</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

c3a, c3b, c3c = st.columns(3)

with c3a:
    education = st.selectbox("Education Level",
                             ["Choose option", "High School",
                              "Technical Degree", "Bachelor’s",
                              "Post-graduate", "Master’s", "Doctorate"])

    experience = st.selectbox("Experience Level",
                              ["Choose option", "< 2 years", "2–5 years",
                               "5–10 years", "10–15 years", "15+ years"])


with c3b:
    kpis_selected = st.multiselect("Primary KPIs",
                                   ["Financial", "Customer", "Operational",
                                    "Quality", "Safety", "Compliance",
                                    "Project Delivery",
                                    "People Leadership"])

    specialization_level = st.selectbox(
        "Specialization Level",
        ["Choose option", "Generalist", "Specialist", "Deep Specialist"]
    )

with c3c:
    competencies_selected = st.multiselect(
        "Core Competencies",
        ["Communication", "Collaboration", "Analytical Thinking",
         "Technical Expertise", "Leadership", "Innovation",
         "Strategic Thinking", "Customer Orientation"]
    )

    innovation_resp = st.selectbox(
        "Innovation Responsibility",
        ["Choose option", "Execution", "Incremental improvements",
         "Major improvements", "Innovation leadership"]
    )

c3d, c3e = st.columns(2)

with c3d:
    leadership_type = st.selectbox(
        "Leadership Type",
        ["Choose option", "None", "Team Lead", "Supervisor",
         "Manager", "Senior Manager", "Director"]
    )

with c3e:
    org_influence = st.selectbox(
        "Organizational Influence",
        ["Choose option", "Team", "Department", "Business Unit",
         "Function", "Enterprise-wide"]
    )


# ----------------------------------------------------------
# BOTÃO — ALINHADO À ESQUERDA
# ----------------------------------------------------------
col_btn, _, _ = st.columns([2, 5, 1])

with col_btn:
    generate = st.button("Generate Job Match Description",
                         key="btn_generate",
                         use_container_width=False,
                         help="Click to generate the recommended match.",
                         type="primary")

    st.markdown('<div class="blue-btn"></div>', unsafe_allow_html=True)



# ==========================================================
# PROCESSAMENTO DO MATCH
# ==========================================================
fields = {
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

missing = validate_required(fields)

if generate:
    if missing:
        st.markdown(
            '<div class="error-box">Please fill all required fields.</div>',
            unsafe_allow_html=True)

        # DEIXA TÍTULO + BORDA VERMELHA
        for m in missing:
            st.markdown(
                f"<div class='error-label'>{m} is required.</div>",
                unsafe_allow_html=True)

    else:
        # roda engine
        match_result = compute_match(fields, df_profiles)

        html_code = render_job_match_description(
            match_result,
            df_profiles
        )

        st.markdown(html_code, unsafe_allow_html=True)


