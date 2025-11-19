# match_engine.py
import pandas as pd
from typing import Dict, Any, List


# ==========================================================
# HELPERS
# ==========================================================
def _encode_map() -> Dict[str, int]:
    return {
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


def _enc(x: Any, emap: Dict[str, int]) -> int:
    return emap.get(x, 0)


def _clean_list(x: Any) -> List[str]:
    if pd.isna(x):
        return []
    return [i.strip() for i in str(x).split(",") if i.strip()]


def _overlap(a: List[str], b: List[str]) -> float:
    if not b:
        return 0.0
    return len(set(a).intersection(set(b))) / len(b)


# ==========================================================
# PUBLIC: MAIN MATCH FUNCTION
# ==========================================================
def compute_job_match(form_inputs: Dict[str, Any], df_profiles: pd.DataFrame) -> Dict[str, Any] | None:
    """
    form_inputs: dicionário vindo da UI (5_Job_Match.py) com:
      - job_family, sub_job_family
      - job_category, geo_scope, org_impact, span_control, nature_work,
        financial_impact, stakeholder_complexity, decision_type, decision_horizon,
        autonomy, problem_solving, knowledge_depth, operational_complexity,
        influence_level, education, experience, specialization_level,
        innovation_resp, leadership_type, org_influence,
        kpis_selected (list), competencies_selected (list)

    df_profiles: DataFrame carregado de "data/Job Profile.xlsx"
                 usando os nomes ORIGINAIS das colunas:
                 "Job Family", "Sub Job Family", "Career Path", "Full Job Code",
                 "Job Profile", "Global Grade",
                 "Sub Job Family Description", "Job Profile Description",
                 "Career Band Description", "Role Description",
                 "Grade Differentiator", "Qualifications",
                 "Specific parameters / KPIs", "Competencies 1", "Competencies 2", "Competencies 3"

    Retorna:
        {"row": best_row (Series), "score_pct": int} ou None.
    """

    emap = _encode_map()

    job_family = form_inputs["job_family"]
    sub_job_family = form_inputs["sub_job_family"]

    # 1) HARD FILTER: mesma Job Family + Sub Job Family
    df_filtered = df_profiles[
        (df_profiles["Job Family"] == job_family) &
        (df_profiles["Sub Job Family"] == sub_job_family)
    ].copy()

    if df_filtered.empty:
        return None

    # 2) User signature (numérico) — mesmo que a versão unificada
    user_sig = {
        "cat": _enc(form_inputs["job_category"], emap),
        "geo": _enc(form_inputs["geo_scope"], emap),
        "impact": _enc(form_inputs["org_impact"], emap),
        "span": _enc(form_inputs["span_control"], emap),
        "nature": _enc(form_inputs["nature_work"], emap),
        "finimp": _enc(form_inputs["financial_impact"], emap),
        "stake": _enc(form_inputs["stakeholder_complexity"], emap),
        "dtype": _enc(form_inputs["decision_type"], emap),
        "dhoriz": _enc(form_inputs["decision_horizon"], emap),

        "auto": _enc(form_inputs["autonomy"], emap),
        "ps": _enc(form_inputs["problem_solving"], emap),
        "kdepth": _enc(form_inputs["knowledge_depth"], emap),
        "opcomp": _enc(form_inputs["operational_complexity"], emap),
        "infl": _enc(form_inputs["influence_level"], emap),

        "edu": _enc(form_inputs["education"], emap),
        "exp": _enc(form_inputs["experience"], emap),
        "spec": _enc(form_inputs["specialization_level"], emap),
        "innov": _enc(form_inputs["innovation_resp"], emap),
        "lead": _enc(form_inputs["leadership_type"], emap),
        "orginf": _enc(form_inputs["org_influence"], emap),
    }

    kpis_selected = form_inputs["kpis_selected"]
    competencies_selected = form_inputs["competencies_selected"]

    # 3) KPIs / Competências da base
    df_filtered["__kpis_list"] = df_filtered["Specific parameters / KPIs"].apply(_clean_list)

    df_filtered["__comp_list"] = (
        df_filtered["Competencies 1"].fillna("") + "," +
        df_filtered["Competencies 2"].fillna("") + "," +
        df_filtered["Competencies 3"].fillna("")
    ).apply(_clean_list)

    # 4) Global Grade numérico para penalidade
    df_filtered["__gg_num"] = pd.to_numeric(df_filtered["Global Grade"], errors="coerce")

    scores: List[float] = []

    for _, row in df_filtered.iterrows():
        gg_val = row["__gg_num"]
        grade_penalty = 0.0
        if pd.notna(gg_val):
            try:
                if abs(int(gg_val) - user_sig["lead"]) > 4:
                    grade_penalty = -0.15
            except Exception:
                grade_penalty = 0.0

        # Similaridade KPIs / Competências
        kpi_score = _overlap(kpis_selected, row["__kpis_list"])
        comp_score = _overlap(competencies_selected, row["__comp_list"])

        # Score final (mesmo espírito da versão unificada)
        final_score = (
            0.40 * (user_sig["geo"] + user_sig["impact"] + user_sig["auto"] + user_sig["ps"] + user_sig["kdepth"]) +
            0.20 * (user_sig["dtype"] + user_sig["dhoriz"] + user_sig["opcomp"]) +
            0.20 * (kpi_score * 5) +
            0.15 * (comp_score * 5) +
            0.05 * (user_sig["edu"] + user_sig["exp"]) +
            grade_penalty
        )

        scores.append(final_score)

    df_filtered["__match_score"] = scores

    best = df_filtered.sort_values("__match_score", ascending=False).iloc[0]
    max_score = float(df_filtered["__match_score"].max())
    if max_score <= 0:
        score_pct = 60
    else:
        score_pct = int(round((float(best["__match_score"]) / max_score) * 100))

    return {"row": best, "score_pct": score_pct}
