# ==========================================================
# html_renderer.py — Renderização IDENTICA ao Job Profile Description
# ==========================================================
import html

# ----------------------------------------------------------
# Carregar SVG inline
# ----------------------------------------------------------
def load_svg(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


ICON_MAP = {
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
# GERA HTML FINAL
# ----------------------------------------------------------
def render_description(match):
    job = html.escape(match["job_profile"])
    gg = html.escape(str(match["global_grade"]))
    jf = html.escape(match["job_family"])
    sf = html.escape(match["sub_job_family"])
    cp = html.escape(match["career_path"])
    fc = html.escape(match["full_job_code"])
    ms = match["match_score"]

    sections = match["sections"]

    html_code = f"""
<html>
<head>
<meta charset="utf-8"/>

<style>

body {{
    background: white;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
}}

.container {{
    padding: 20px 28px 40px 28px;
}}

.card {{
    background: #f5f3ee;
    border-radius: 18px;
    padding: 26px;
    border: 1px solid #e3e1dd;
    margin-bottom: 38px;
}}

.job-title {{
    font-size: 26px;
    font-weight: 700;
}}

.gg {{
    color: #145efc;
    font-size: 18px;
    margin-top: 4px;
}}

.meta {{
    background: #ffffff;
    padding: 14px 16px;
    margin-top: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    font-size: 15px;
}}

.section-title {{
    font-size: 18px;
    font-weight: 700;
    margin-top: 34px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.section-line {{
    height: 1px;
    background: #dfddd8;
    margin: 10px 0 16px 0;
}}

.section-text {{
    white-space: pre-wrap;
    font-size: 15px;
    line-height: 1.48;
}}

.icon svg {{
    width: 22px;
    height: 22px;
}}

</style>
</head>

<body>

<div class="container">

    <div class="card">
        <div class="job-title">{job}</div>
        <div class="gg">GG {gg}</div>

        <div class="meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fc}<br>
            <b>Match Score:</b> {ms}%
        </div>
    </div>
    """

    # SEÇÕES
    for sec_name, sec_value in sections.items():
        icon_path = ICON_MAP.get(sec_name, "")
        icon_svg = load_svg(icon_path)
        sec_html = html.escape(str(sec_value)) if sec_value else ""

        html_code += f"""
        <div class="section-title">
            <span class="icon">{icon_svg}</span> {sec_name}
        </div>
        <div class="section-line"></div>
        <div class="section-text">{sec_html}</div>
        """

    html_code += """
</div>
</body>
</html>
"""
    return html_code
