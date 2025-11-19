# ==========================================================
# match_engine.py — Engine oficial do Job Match
# ==========================================================

import pandas as pd

# ----------------------------------------------------------
# Normalizador simples para valores "Choose option"
# ----------------------------------------------------------
def normalize(value):
    if value is None:
        return ""
    if isinstance(value, str) and value.strip().lower() in ["choose option", "select option", ""]:
        return ""
    return value


# ----------------------------------------------------------
# Campos obrigatórios (títulos iguais ao formulário)
# ----------------------------------------------------------
REQUIRED_FIELDS = [
    "Job Family", "Sub Job Family", "Job Category", "Geographic Scope",
    "Organizational Impact", "Span of Control", "Nature of Work",
    "Financial Impact", "Stakeholder Complexity", "Decision Type",
    "Decision Time Horizon", "Autonomy Level", "Problem Solving Complexity",
    "Knowledge Depth", "Operational Complexity", "Influence Level",
    "Education Level", "Experience Level", "Specialization Level",
    "Innovation Responsibility", "Leadership Type", "Organizational Influence"
]


def validate_user_inputs(user_inputs: dict):
    missing = []
    for field in REQUIRED_FIELDS:
        if normalize(user_inputs.get(field)) == "":
            missing.append(field)
    return len(missing) == 0, missing


# ----------------------------------------------------------
# Pesos ajustados (versão refinada)
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
# FUNÇÃO PRINCIPAL — compute_match
# ----------------------------------------------------------
def compute_match(user_inputs: dict, df_profiles: pd.DataFrame):

    ok, missing = validate_user_inputs(user_inputs)
    if not ok:
        return None, missing

    ui = {k: normalize(v) for k, v in user_inputs.items()}

    scores = []

    for idx, row in df_profiles.iterrows():
        profile_score = 0
        max_score = 0

        for field, weight in WEIGHTS.items():
            max_score += weight
            col = field.lower().replace(" ", "_")

            if col not in df_profiles.columns:
                continue

            user_value = ui[field]
            profile_value = normalize(row[col])

            if user_value == profile_value:
                profile_score += weight

        # score final %
        pct = int((profile_score / max_score) * 100)

        scores.append({
            "profile_index": idx,
            "score": pct
        })

    ordered = sorted(scores, key=lambda x: x["score"], reverse=True)
    best = ordered[0] if ordered else None

    return best, []
