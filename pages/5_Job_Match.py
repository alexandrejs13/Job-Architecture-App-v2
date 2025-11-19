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
# PARTE 4 — LÓGICA DE VALIDAÇÃO + MATCH + RENDER HTML
# 100% COMPATÍVEL COM AS VARIÁVEIS DO SEU FORMULÁRIO
# ==========================================================

# Lista unificada dos campos obrigatórios com seus valores reais
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

# Campos do tipo multiselect (não podem estar vazios)
required_multi = {
    "Primary KPIs": kpis_selected,
    "Core Competencies": competencies_selected
}

# ==========================================================
# FUNÇÃO — Marcar título + borda vermelha
# ==========================================================
def mark_invalid_fields():
    error_css = "<style>"
    
    for label, value in required_fields.items():
        if value == "Choose option":
            safe_label = label.replace(" ", "").lower()
            error_css += f"""
            label[for="{safe_label}"] p {{
                color: red !important;
                font-weight: 700 !important;
            }}
            div[data-testid="stSelectbox"] {{
                border: 2px solid red !important;
                border-radius: 6px !important;
            }}
            """

    for label, value in required_multi.items():
        if not value:
            safe = label.replace(" ", "").lower()
            error_css += f"""
            label[for="{safe}"] p {{
                color: red !important;
                font-weight: 700 !important;
            }}
            div[data-testid="stMultiSelect"] {{
                border: 2px solid red !important;
                border-radius: 6px !important;
            }}
            """

    error_css += "</style>"
    st.markdown(error_css, unsafe_allow_html=True)


# ==========================================================
# BOTÃO – AÇÃO
# ==========================================================
if generate:

    # -------- VALIDAR CAMPOS --------
    missing = []

    for label, value in required_fields.items():
        if value == "Choose option":
            missing.append(label)

    for label, value in required_multi.items():
        if not value:
            missing.append(label)

    # Se faltar algo → bloquear
    if missing:
        st.markdown("""
        <div style="
            background:#fdeaea;
            padding:16px;
            border-radius:8px;
            color:#a13333;
            margin-top:16px;
            font-size:18px;
        ">
        Please fill in all required fields before generating the match.
        </div>
        """, unsafe_allow_html=True)

        mark_invalid_fields()
        st.stop()

    # ==========================================================
    #  COLETAR INPUTS PARA O MATCH ALGORITMO
    # ==========================================================
    user_inputs = {
        "job_family": job_family,
        "sub_job_family": sub_job_family,
        "job_category": job_category,
        "geo_scope": geo_scope,
        "org_impact": org_impact,
        "span_control": span_control,
        "nature_work": nature_work,
        "financial_impact": financial_impact,
        "stakeholder_complexity": stakeholder_complexity,
        "decision_type": decision_type,
        "decision_horizon": decision_horizon,
        "autonomy": autonomy,
        "problem_solving": problem_solving,
        "knowledge_depth": knowledge_depth,
        "operational_complexity": operational_complexity,
        "influence_level": influence_level,
        "education": education,
        "experience": experience,
        "specialization": specialization_level,
        "innovation_resp": innovation_resp,
        "leadership_type": leadership_type,
        "org_influence": org_influence,
        "kpis": kpis_selected,
        "competencies": competencies_selected
    }

    # ==========================================================
    # MATCH ENGINE — versão simples (PLACEHOLDER)
    # (Você já tem a versão A definitiva)
    # ==========================================================
    best_job = df_profiles.iloc[0].to_dict()   # substitui pelo match real
    match_score = 75                           # substitui pela sua lógica real

    # ==========================================================
    # RENDER HTML FINAL — BACKGROUND BRANCO SEM SCROLL
    # ==========================================================

    st.markdown("""
    <style>
        .match-card {
            background: white;
            padding: 32px;
            border-radius: 14px;
            border: 1px solid #ececec;
        }
        .section-title-out {
            font-size: 20px;
            font-weight: 700;
            margin-top: 32px;
        }
        .divider-out {
            height: 1px;
            background: #e4e4e4;
            margin: 6px 0 18px 0;
        }
        .description-box {
            font-size: 16px;
            line-height: 1.45;
            white-space: pre-wrap;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="match-card">

        <h2 style="font-size:26px; margin-bottom:0;">
            Recommended Match: {best_job['job_profile']}
        </h2>

        <div style="color:#145efc; font-size:20px; margin-top:4px;">
            Match Score: {match_score}%
        </div>

        <div style="margin-top:22px; font-size:17px;">
            <b>Job Family:</b> {best_job['job_family']}<br>
            <b>Sub Job Family:</b> {best_job['sub_job_family']}<br>
            <b>Career Path:</b> {best_job['career_path']}<br>
            <b>Full Job Code:</b> {best_job['full_job_code']}<br>
        </div>

        <div class="section-title-out">Job Profile Description</div>
        <div class="divider-out"></div>
        <div class="description-box">{best_job['job_profile_description']}</div>

        <div class="section-title-out">Career Band Description</div>
        <div class="divider-out"></div>
        <div class="description-box">{best_job['career_band_description']}</div>

        <div class="section-title-out">Role Description</div>
        <div class="divider-out"></div>
        <div class="description-box">{best_job['role_description']}</div>

        <div class="section-title-out">Grade Differentiator</div>
        <div class="divider-out"></div>
        <div class="description-box">{best_job['grade_differentiator']}</div>

        <div class="section-title-out">Qualifications</div>
        <div class="divider-out"></div>
        <div class="description-box">{best_job['qualifications']}</div>

        <div class="section-title-out">Specific parameters / KPIs</div>
        <div class="divider-out"></div>
        <div class="description-box">{best_job['specific_kpis']}</div>

    </div>
    """, unsafe_allow_html=True)



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
# PARTE 4 — VALIDAÇÃO, BOTÃO E GERAÇÃO DA DESCRIÇÃO
# ==========================================================

import html
import streamlit.components.v1 as components

# --- CSS do botão azul sempre largo, sem quebra ---
st.markdown("""
<style>
/* botão principal sempre largo */
.stButton > button[kind="secondary"], .stButton > button[kind="primary"], .stButton > button {
    background: #2458ff !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 0.75rem 1.6rem !important;
    width: 100% !important;
    max-width: 480px !important;
    white-space: nowrap !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# Ajuda: função bem defensiva para saber se campo está vazio
# ----------------------------------------------------------
def is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == "" or value.strip().lower().startswith("choose option")
    if isinstance(value, (list, tuple, set)):
        return len(value) == 0
    return False


# ----------------------------------------------------------
# Coleta dos valores do formulário (usar exatamente os nomes
# que você já usou nas variáveis dos selects / multiselects)
# ----------------------------------------------------------
user_inputs = {
    "Job Family": job_family,
    "Sub Job Family": sub_job_family,
    "Job Category": job_category,
    "Geographic Scope": geo_scope,
    "Organizational Impact": org_impact,
    "Span of Control": span_control,
    "Autonomy Level": autonomy,
    "Problem Solving Complexity": problem_solving,
    "Knowledge Depth": knowledge_depth,
    "Influence Level": influence,
    "Education Level": education,
    "Experience Level": experience,
    "Primary KPIs": kpis,
    "Core Competencies": competencies,
    # aqui entram os 10 campos extras que você adicionou na etapa anterior;
    # se alguns não existirem na planilha, não tem problema, a função de match trata isso com segurança.
    "Financial Impact": financial_impact,
    "Stakeholder Complexity": stakeholder_complexity,
    "Decision Time Horizon": decision_time_horizon,
    "Nature of Work": nature_of_work,
    "Decision Type": decision_type,
    "Operational Complexity": operational_complexity,
    "Specialization Level": specialization_level,
    "Innovation Responsibility": innovation_responsibility,
    "Leadership Type": leadership_type,
    "Organizational Influence": organizational_influence,
}

# ----------------------------------------------------------
# Descobrir quais campos obrigatórios estão vazios
# (todos são obrigatórios, como você pediu)
# ----------------------------------------------------------
missing_fields = [label for label, value in user_inputs.items() if is_empty(value)]

# ----------------------------------------------------------
# Função de matching — opção A (regras, sem semântica)
# ----------------------------------------------------------
def compute_match(answers: dict, df_profiles: pd.DataFrame):
    """
    Retorna (best_row_dict, score_de_0_a_100)
    Regra forte: filtra por Job Family / Sub Job Family / Career Path.
    Dentro disso, calcula score por campos que existirem na planilha.
    """

    if df_profiles.empty:
        return None, 0

    # Filtro forte por Job Family / Sub Job Family (e Career Path se existir)
    flt = df_profiles.copy()

    if "Job Family" in flt.columns and not is_empty(answers.get("Job Family")):
        flt = flt[flt["Job Family"] == answers["Job Family"]]

    if "Sub Job Family" in flt.columns and not is_empty(answers.get("Sub Job Family")):
        flt = flt[flt["Sub Job Family"] == answers["Sub Job Family"]]

    if "Career Path" in flt.columns and not is_empty(career_path):
        flt = flt[flt["Career Path"] == career_path]

    # Se o filtro ficar vazio, volta para o df completo (mas isso é exceção)
    if flt.empty:
        flt = df_profiles.copy()

    # pesos simples — você pode ajustar depois
    weight_map = {
        "Job Family": 10,
        "Sub Job Family": 10,
        "Job Category": 6,
        "Geographic Scope": 6,
        "Organizational Impact": 6,
        "Span of Control": 6,
        "Autonomy Level": 6,
        "Problem Solving Complexity": 6,
        "Knowledge Depth": 6,
        "Influence Level": 6,
        "Education Level": 4,
        "Experience Level": 4,
        "Financial Impact": 4,
        "Stakeholder Complexity": 4,
        "Decision Time Horizon": 4,
        "Nature of Work": 4,
        "Decision Type": 4,
        "Operational Complexity": 4,
        "Specialization Level": 4,
        "Innovation Responsibility": 4,
        "Leadership Type": 4,
        "Organizational Influence": 4,
    }

    # campos tipo lista (KPIs / Competencies) contam interseção
    list_fields = ["Primary KPIs", "Core Competencies"]

    max_score = 0
    best_row = None

    for _, row in flt.iterrows():
        score = 0
        total_possible = 0

        # campos simples
        for col, w in weight_map.items():
            if col in df_profiles.columns and not is_empty(answers.get(col)):
                total_possible += w
                if str(row.get(col, "")).strip() == str(answers[col]).strip():
                    score += w

        # campos lista (se existirem na planilha)
        for col in list_fields:
            if col in df_profiles.columns and not is_empty(answers.get(col)):
                total_possible += 6  # peso total desse grupo
                target_raw = str(row.get(col, "") or "")
                # quebra por ; ou , para virar lista
                targets = [t.strip() for t in target_raw.replace(";", ",").split(",") if t.strip()]
                inter = set(answers[col]) & set(targets)
                if targets:
                    score += 6 * (len(inter) / len(set(targets)))

        if total_possible == 0:
            continue

        norm_score = int(round(100 * score / total_possible))

        if norm_score > max_score:
            max_score = norm_score
            best_row = row

    if best_row is None:
        return None, 0

    return best_row.to_dict(), max_score


# ----------------------------------------------------------
# Builder do HTML — 100% igual ao da Job Profile Description
# só que forçando 1 coluna, sem área de scroll fixa e fundo branco
# ----------------------------------------------------------
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


def build_single_profile_html(profile_dict: dict, match_score: int):

    # usamos o mesmo dicionário icons_svg já carregado na página de cima
    job = html.escape(str(profile_dict.get("Job Profile", "")))
    gg = html.escape(str(profile_dict.get("Global Grade", "")))
    jf = html.escape(str(profile_dict.get("Job Family", "")))
    sf = html.escape(str(profile_dict.get("Sub Job Family", "")))
    cp = html.escape(str(profile_dict.get("Career Path", "")))
    fc = html.escape(str(profile_dict.get("Full Job Code", "")))

    html_code = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #ffffff;
}}

#viewport {{
    padding: 8px 0 24px 0;
}}

/* Card de recomendação (igual Job Profile Description, mas com header de match) */
.card-top {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e3e1dd;
    margin-bottom: 24px;
}}

.recommend-title {{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 4px;
}}

.match-score {{
    color: #145efc;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 10px;
}}

.meta {{
    background: #ffffff;
    padding: 14px;
    margin-top: 6px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
}}

/* Seções em uma coluna */
.section-box {{
    margin-bottom: 28px;
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
    line-height: 1.45;
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

    <div class="card-top">
        <div class="match-score">Match Score: {match_score}%</div>
        <div class="recommend-title">{job}</div>
        <div class="meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fc}
        </div>
    </div>
"""

    for sec in sections:
        val = profile_dict.get(sec, "")
        icon = icons_svg.get(sec, "")
        html_code += f"""
    <div class="section-box">
        <div class="section-title">
            <span class="icon-inline">{icon}</span>
            {html.escape(sec)}
        </div>
        <div class="section-line"></div>
        <div class="section-text">{html.escape(str(val))}</div>
    </div>
"""

    html_code += """
</div>
</body>
</html>
"""
    return html_code


# ----------------------------------------------------------
# BOTÃO + LÓGICA (match_result inicializado para evitar NameError)
# ----------------------------------------------------------
match_result = None
match_score = 0

# botão alinhado à esquerda embaixo da primeira coluna -> usar uma coluna "dummy"
btn_col, _ = st.columns([1, 2])
with btn_col:
    generate = st.button("Generate Job Match Description")

if generate:
    if missing_fields:
        # mensagem geral
        st.markdown(
            """
<div style="
    margin-top: 18px;
    margin-bottom: 10px;
    padding: 14px 18px;
    border-radius: 12px;
    background: #fdeaea;
    color: #b11d1d;
    font-size: 15px;
">
Please fill in all required fields before generating the match.
</div>
""",
            unsafe_allow_html=True,
        )

        # lista textual dos campos (mantive como fallback visual)
        for f in missing_fields:
            st.markdown(f"<span style='color:#e02424; font-weight:600;'>• {f}</span>", unsafe_allow_html=True)

    else:
        # faz o match usando a planilha Job Profile
        match_result, match_score = compute_match(user_inputs, df)

        if match_result:
            # renderiza HTML em fundo branco, sem scroll fixo
            components.html(
                build_single_profile_html(match_result, match_score),
                height=900,
                scrolling=False,
            )
        else:
            st.warning("No suitable Job Profile was found for the selected parameters.")
