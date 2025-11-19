# ==========================================================
# match_engine.py — Engine de match determinístico
# ==========================================================
import pandas as pd

# ----------------------------------------------------------
# CARREGAR PERFIS
# ----------------------------------------------------------
def load_profiles(path="data/Job Profile.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


# ----------------------------------------------------------
# MAPEAMENTO DE PESO POR CAMPO → ajustado para FINANCE não virar SALES
# Campos com correspondência exata valem mais
# ----------------------------------------------------------
WEIGHTS = {
    "job_family": 5,
    "sub_job_family": 4,
    "career_path": 3,
    "job_category": 3,
    "geographic_scope": 2,
    "organizational_impact": 2,
    "span_of_control": 3,
    "nature_of_work": 2,
    "financial_impact": 2,
    "stakeholder_complexity": 2,
    "decision_type": 2,
    "decision_time_horizon": 1,
    "autonomy_level": 3,
    "problem_solving_complexity": 3,
    "knowledge_depth": 2,
    "operational_complexity": 2,
    "influence_level": 2,
    "education_level": 1,
    "experience_level": 2,
    "specialization_level": 1,
    "innovation_responsibility": 1,
    "leadership_type": 3,
    "organizational_influence": 2,
}

# ----------------------------------------------------------
# NORMALIZAÇÃO → remover acentos / caixa baixa
# ----------------------------------------------------------
import unicodedata

def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


# ----------------------------------------------------------
# MATCH DETERMINÍSTICO
# ----------------------------------------------------------
def compute_job_match(user_inputs: dict, df_profiles: pd.DataFrame):
    """
    user_inputs → dicionário com os 25 campos do formulário
    df_profiles → dataframe carregado do arquivo Excel
    """

    df = df_profiles.copy()
    df_norm = df.copy()

    # normalizar perfis
    for col in df_norm.columns:
        df_norm[col] = df_norm[col].apply(normalize)

    # normalizar entradas
    user_norm = {k: normalize(v) for k, v in user_inputs.items()}

    # score acumulado
    scores = []

    for idx, row in df_norm.iterrows():
        score = 0
        total_weight = 0

        for field, weight in WEIGHTS.items():
            if field not in user_norm:
                continue

            profile_value = row.get(field, "")
            user_value = user_norm.get(field, "")

            if user_value and profile_value and user_value == profile_value:
                score += weight

            total_weight += weight

        if total_weight == 0:
            final_score = 0
        else:
            final_score = round((score / total_weight) * 100, 2)

        scores.append(final_score)

    df["match_score"] = scores
    best_row = df.sort_values("match_score", ascending=False).iloc[0]

    return {
        "match_score": float(best_row["match_score"]),
        "job_profile": best_row["job_profile"],
        "job_family": best_row["job_family"],
        "sub_job_family": best_row["sub_job_family"],
        "career_path": best_row["career_path"],
        "global_grade": best_row["global_grade"],
        "full_job_code": best_row["full_job_code"],
        "sections": {
            "Sub Job Family Description": best_row["sub_job_family_description"],
            "Job Profile Description": best_row["job_profile_description"],
            "Career Band Description": best_row["career_band_description"],
            "Role Description": best_row["role_description"],
            "Grade Differentiator": best_row["grade_differentiator"],
            "Qualifications": best_row["qualifications"],
            "Specific parameters / KPIs": best_row["specific_parameters_/_kpis"],
            "Competencies 1": best_row["competencies_1"],
            "Competencies 2": best_row["competencies_2"],
            "Competencies 3": best_row["competencies_3"],
        }
    }
