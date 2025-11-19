# ==========================================================
# html_renderer.py — Render do HTML do Job Match
# ==========================================================

import base64
import os


ICON_MAP = {
    "Sub Job Family Description": "Hierarchy.svg",
    "Job Profile Description": "Content_Book_Phone.svg",
    "Career Band Description": "File_Clipboard_Text.svg",
    "Role Description": "Shopping_Business_Target.svg",
    "Grade Differentiator": "User_Add.svg",
    "Qualifications": "Edit_Pencil.svg",
    "Specific Parameters / KPIs": "Graph_Bar.svg",
    "Competencies 1": "Setting_Cog.svg",
    "Competencies 2": "Setting_Cog.svg",
    "Competencies 3": "Setting_Cog.svg",
}


def load_svg_icon(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------
# Função principal
# ----------------------------------------------------------
def render_job_description(best_match_row, score):
    html = []

    # ------------------------------------------------------
    # Card Superior
    # ------------------------------------------------------
    html.append(f"""
    <div class="card">
        <div class="job-title">{best_match_row['job_title']}</div>
        <div class="gg">{best_match_row['gg']}</div>

        <div class="meta">
            <b>Job Family:</b> {best_match_row['job_family']}<br>
            <b>Sub Job Family:</b> {best_match_row['sub_job_family']}<br>
            <b>Career Path:</b> {best_match_row['career_path']}<br>
            <b>Full Job Code:</b> {best_match_row['full_job_code']}<br>
            <b>Match Score:</b> {round(score,2)}%
        </div>
    </div>
    """)

    # ------------------------------------------------------
    # Seções da descrição
    # ------------------------------------------------------
    sections = [
        ("Sub Job Family Description", "sub_job_family_description"),
        ("Job Profile Description", "job_profile_description"),
        ("Career Band Description", "career_band_description"),
        ("Role Description", "role_description"),
        ("Grade Differentiator", "grade_differentiator"),
        ("Qualifications", "qualifications"),
        ("Specific Parameters / KPIs", "specific_parameters_kpis"),
        ("Competencies 1", "competencies_1"),
        ("Competencies 2", "competencies_2"),
        ("Competencies 3", "competencies_3"),
    ]

    for label, column in sections:
        icon_file = ICON_MAP.get(label, "")
        icon_path = f"assets/icons/{icon_file}"
        svg = load_svg_icon(icon_path)

        text = best_match_row.get(column, "")
        if not text:
            continue

        html.append(f"""
        <div class="section-title">
            <span class="icon">{svg}</span>
            {label}
        </div>
        <div class="section-text">{text}</div>
        """)

    return "\n".join(html)
