# html_renderer.py
import html
import os
from typing import Dict
import pandas as pd

# ---------------------------------------------------------
# Carrega SVGs igual à página de Job Profile Description
# ---------------------------------------------------------
def load_svg(svg_name: str) -> str:
    path = os.path.join("assets", "icons", "sig", svg_name)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

ICONS_SVG: Dict[str, str] = {
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

SECTIONS_ORDER = [
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

# ---------------------------------------------------------
# CSS padronizado para ambos os renderers
# ---------------------------------------------------------
BASE_CSS = """
<style>
.job-match-wrapper {
    background: #ffffff;
    padding: 0;
    margin-top: 18px;
    margin-bottom: 30px;
    font-family: "Segoe UI", sans-serif;
}

/* Card superior */
.job-match-card {
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e3e1dd;
    margin-bottom: 24px;
}

.job-title {
    font-size: 20px;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 4px;
}

.job-gg {
    color: #145efc;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 12px;
}

.job-meta {
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
}

/* Seções de descrição */
.job-sections {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.section-box {
    padding-bottom: 4px;
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}

.section-icon {
    width: 20px;
    height: 20px;
    display: inline-block;
}

.section-line {
    height: 1px;
    background: #e8e6e1;
    width: 100%;
    margin: 8px 0 12px 0;
}

.section-text {
    font-size: 14px;
    line-height: 1.45;
    white-space: pre-wrap;
}
</style>
"""


# ---------------------------------------------------------
# RENDERER ORIGINAL (Job Profile Description)
# ---------------------------------------------------------
def render_job_description(best_match_row: pd.Series, final_score: float) -> str:
    job_title = html.escape(str(best_match_row.get("Job Profile", "")))
    gg = html.escape(str(best_match_row.get("Global Grade", "")))
    jf = html.escape(str(best_match_row.get("Job Family", "")))
    sf = html.escape(str(best_match_row.get("Sub Job Family", "")))
    cp = html.escape(str(best_match_row.get("Career Path", "")))
    fc = html.escape(str(best_match_row.get("Full Job Code", "")))

    out = [BASE_CSS]
    out.append('<div class="job-match-wrapper">')

    out.append(f"""
    <div class="job-match-card">
        <div class="job-title">{job_title}</div>
        <div class="job-gg">GG {gg}</div>

        <div class="job-meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fc}
        </div>
    </div>
    """)

    out.append('<div class="job-sections">')

    for sec in SECTIONS_ORDER:
        raw_val = best_match_row.get(sec, "")
        text_val = html.escape("" if pd.isna(raw_val) else str(raw_val))
        icon_svg = ICONS_SVG.get(sec, "")

        out.append(f"""
        <div class="section-box">
            <div class="section-title">
                <span class="section-icon">{icon_svg}</span>
                {html.escape(sec)}
            </div>
            <div class="section-line"></div>
            <div class="section-text">{text_val}</div>
        </div>
        """)

    out.append("</div></div>")
    return "\n".join(out)


# ---------------------------------------------------------
# NOVO RENDERER — Job Match Description (idêntico + MATCH %)
# ---------------------------------------------------------
def render_job_match_description(best_match_row: pd.Series, final_score: float) -> str:
    """
    Idêntico ao layout do Job Profile Description, porém adiciona:
    ✔ GG • Match XX%
    """
    job_title = html.escape(str(best_match_row.get("Job Profile", "")))
    gg = html.escape(str(best_match_row.get("Global Grade", "")))
    score_txt = f"{final_score:.0f}%"

    jf = html.escape(str(best_match_row.get("Job Family", "")))
    sf = html.escape(str(best_match_row.get("Sub Job Family", "")))
    cp = html.escape(str(best_match_row.get("Career Path", "")))
    fc = html.escape(str(best_match_row.get("Full Job Code", "")))

    out = [BASE_CSS]
    out.append('<div class="job-match-wrapper">')

    # ------------------ TOPO COM MATCH ------------------
    out.append(f"""
    <div class="job-match-card">
        <div class="job-title">{job_title}</div>

        <div class="job-gg">
            GG {gg} • Match {score_txt}
        </div>

        <div class="job-meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fc}
        </div>
    </div>
    """)

    # ------------------ SEÇÕES ------------------
    out.append('<div class="job-sections">')

    for sec in SECTIONS_ORDER:
        raw_val = best_match_row.get(sec, "")
        text_val = html.escape("" if pd.isna(raw_val) else str(raw_val))
        icon_svg = ICONS_SVG.get(sec, "")

        out.append(f"""
        <div class="section-box">
            <div class="section-title">
                <span class="section-icon">{icon_svg}</span>
                {html.escape(sec)}
            </div>
            <div class="section-line"></div>
            <div class="section-text">{text_val}</div>
        </div>
        """)

    out.append("</div></div>")
    return "\n".join(out)
