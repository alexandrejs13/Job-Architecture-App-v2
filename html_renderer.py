# ==========================================================
# html_renderer.py — padrão SIG para descrição final
# ==========================================================

import html
import os
import pandas as pd

def load_svg(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


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


def render_job_match_description(match_data, df_profiles):

    idx = match_data["profile_index"]
    row = df_profiles.loc[idx]

    title = html.escape(row["job_profile"])
    jf = html.escape(row["job_family"])
    sf = html.escape(row["sub_job_family"])
    cp = html.escape(row["career_path"])
    code = html.escape(row["full_job_code"])

    # HTML SIG completo
    html_code = f"""
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: white;
        }}
        .card {{
            background: #f5f3ee;
            border-radius: 16px;
            padding: 26px;
            border: 1px solid #e3e1dd;
            margin-bottom: 28px;
        }}
        .job-title {{
            font-size: 26px;
            font-weight: 700;
        }}
        .gg {{
            font-size: 18px;
            color: #145efc;
            font-weight: 700;
            margin-top: 6px;
        }}
        .meta {{
            margin-top: 14px;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #e0ddd7;
            background: white;
            font-size: 14px;
        }}
        .section-title {{
            margin-top: 36px;
            font-size: 18px;
            font-weight: 700;
            display: flex;
            gap: 8px;
            align-items: center;
        }}
        .divider {{
            height: 1px;
            background: #dcd8d1;
            margin: 10px 0 16px 0;
        }}
        .section-text {{
            white-space: pre-wrap;
            font-size: 15px;
            line-height: 1.45;
        }}
        .icon {{
            height: 20px;
            width: 20px;
        }}
    </style>

    <div class="card">
        <div class="job-title">{title}</div>
        <div class="gg">GG {row['global_grade']}</div>

        <div class="meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {code}
        </div>
    </div>
    """

    for sec in SECTION_ORDER:
        col = sec

        icon = load_svg(ICONS.get(sec, ""))
        content = html.escape(str(row[col])) if col in df_profiles.columns else ""

        html_code += f"""
        <div class="section-title">
            <span class="icon">{icon}</span>
            {html.escape(sec)}
        </div>
        <div class="divider"></div>
        <div class="section-text">{content}</div>
        """

    return html_code
