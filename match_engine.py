# ==========================================================
# match_engine.py — Engine de Match do Job Match
# ==========================================================

import pandas as pd
from difflib import SequenceMatcher


# ----------------------------------------------------------
# Função utilitária
# ----------------------------------------------------------
def ratio(a, b):
    """Retorna similaridade entre duas strings."""
    if not a or not b:
        return 0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# ----------------------------------------------------------
# Cálculo do score baseado nos campos do formulário
# ----------------------------------------------------------
def compute_job_match(form_inputs, df_profiles):
    """
    form_inputs = dicionário com todos os campos preenchidos
    df_profiles = dataframe do Job Profile.xlsx pré-processado
    """

    results = []

    for _, row in df_profiles.iterrows():
        score = 0
        weight_total = 0

        # --------------------- PESOS -----------------------
        WEIGHTS = {
            "job_family": 25,
            "sub_job_family": 25,
            "job_category": 8,
            "geo_scope": 8,
            "org_impact": 8,
            "autonomy": 6,
            "knowledge_depth": 6,
            "operational_complexity": 6,
            "experience": 5,
            "education": 5,
        }

        # --------------------------------------------------
        # JOB FAMILY MATCH (peso pesado)
        # --------------------------------------------------
        score += WEIGHTS["job_family"] * ratio(
            form_inputs["job_family"], row.get("job_family", "")
        )
        weight_total += WEIGHTS["job_family"]

        # --------------------------------------------------
        # SUB JOB FAMILY MATCH (peso pesado)
        # --------------------------------------------------
        score += WEIGHTS["sub_job_family"] * ratio(
            form_inputs["sub_job_family"], row.get("sub_job_family", "")
        )
        weight_total += WEIGHTS["sub_job_family"]

        # --------------------------------------------------
        # CAMPOS WTW — match parcial por similaridade
        # --------------------------------------------------
        for k_form, k_df, w in [
            ("job_category", "job_category", WEIGHTS["job_category"]),
            ("geo_scope", "geo_scope", WEIGHTS["geo_scope"]),
            ("org_impact", "org_impact", WEIGHTS["org_impact"]),
            ("autonomy", "autonomy", WEIGHTS["autonomy"]),
            ("knowledge_depth", "knowledge_depth", WEIGHTS["knowledge_depth"]),
            ("operational_complexity", "operational_complexity", WEIGHTS["operational_complexity"]),
            ("experience", "experience", WEIGHTS["experience"]),
            ("education", "education", WEIGHTS["education"]),
        ]:
            score += w * ratio(form_inputs[k_form], row.get(k_df, ""))
            weight_total += w

        # --------------------------------------------------
        final_score = (score / weight_total) * 100

        results.append({
            "job_title": row.get("job_title", ""),
            "gg": row.get("gg", ""),
            "job_family": row.get("job_family", ""),
            "sub_job_family": row.get("sub_job_family", ""),
            "career_path": row.get("career_path", ""),
            "full_job_code": row.get("full_job_code", ""),
            "final_score": final_score,
            "row": row
        })

    results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    return results[0] if results else None
