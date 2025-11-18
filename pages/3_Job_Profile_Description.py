import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components
import base64
import os

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ---------------------------------------------------------
# LOAD PAGE ICON (PNG) -> INLINE BASE64
# ---------------------------------------------------------
def load_page_icon():
    path = "assets/icons/business_review_clipboard.png"
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

page_icon_b64 = load_page_icon()

# ---------------------------------------------------------
# HEADER (ÍCONE GRANDE + ALINHAMENTO PERFEITO)
# ---------------------------------------------------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:16px; margin-bottom:6px;">
    <img src="data:image/png;base64,{page_icon_b64}" style="width:42px; height:42px; margin-top:2px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Profile Description
    </h1>
</div>

<hr style="margin-top:8px; margin-bottom:0;">
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD EXCEL
# ---------------------------------------------------------
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()

# ---------------------------------------------------------
# INLINE SVG LOADER
# ---------------------------------------------------------
def load_svg(svg_name):
    path = f"assets/icons/sig/{svg_name}"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# MAP FINAL
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

# ---------------------------------------------------------
# TOP FILTERS
# ---------------------------------------------------------
st.subheader("🔍 Job Profile Description Explorer")

c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    job_family = st.selectbox("Job Family",
        ["All"] + sorted(df["Job Family"].dropna().unique()))

with c2:
    subfam_list = (
        df[df["Job Family"] == job_family]["Sub Job Family"].dropna().unique()
        if job_family != "All"
        else df["Sub Job Family"].dropna().unique()
    )
    sub_family = st.selectbox("Sub Job Family",
        ["All"] + sorted(subfam_list))

with c3:
    path_list = (
        df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique()
        if sub_family != "All"
        else df["Career Path"].dropna().unique()
    )
    career_path = st.selectbox("Career Path",
        ["All"] + sorted(path_list))

flt = df.copy()

if job_family != "All":
    flt = flt[flt["Job Family"] == job_family]
if sub_family != "All":
    flt = flt[flt["Sub Job Family"] == sub_family]
if career_path != "All":
    flt = flt[flt["Career Path"] == career_path]

flt["label"] = flt["Global Grade"].astype(str) + " • " + flt["Job Profile"]

selected = st.multiselect("Select up to 3 profiles:",
    flt["label"].tolist(), max_selections=3)

if not selected:
    st.stop()

profiles = [flt[flt["label"] == s].iloc[0].to_dict() for s in selected]

# ---------------------------------------------------------
# SECTION ORDER
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# BUILD HTML FINAL
# ---------------------------------------------------------
def build_html(profiles):

    n = len(profiles)

    html_code = f"""
<html>
<head>
<meta charset="UTF-8">

<style>

html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}}

#viewport {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* --------------------------
   TOP GRID – SAND1 CARDS
--------------------------- */
#top-area {{
    background: white;
    padding: 18px 24px;
    flex-shrink: 0;
}}

.grid-top {{
    display: grid;
    grid-template-columns: repeat({n}, 1fr);
    gap: 26px;
}}

.card-top {{
    background: #f5f3ee;        /* SAND1 */
    border-radius: 16px;
    padding: 24px 26px;
    box-shadow: none;           /* sem sombra */
}}

.title {{
    font-size: 20px;
    font-weight: 700;
    line-height: 1.28;
}}

.gg {{
    color: #145efc;
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
}}

.meta {{
    background: white;     /* AGORA O BLOCO MENOR É BRANCO */
    padding: 14px;
    border-radius: 12px;
    margin-top: 14px;
    border: 1px solid #e6e4df;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    font-size: 14px;
}}

/* --------------------------
   SCROLL AREA
--------------------------- */
#scroll-area {{
    flex: 1;
    overflow-y: auto;
    padding: 28px 24px 40px 24px;
}}

.grid-desc {{
    display: grid;
    grid-template-columns: repeat({n}, 1fr);
    gap: 28px;
}}

.row {{
    display: contents;
}}

.section-box {{
    padding-bottom: 32px;
}}

.section-title {{
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.section-line {{
    height: 1px;
    background: #e7e5e0;
    width: 100%;
    margin: 6px 0 14px 0;
}}

.section-text {{
    font-size: 14px;
    line-height: 1.42;
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

    <!-- TOP CARDS -->
    <div id="top-area">
        <div class="grid-top">
    """

    # ---------- TOP CARDS ----------
    for p in profiles:
        job = html.escape(p["Job Profile"])
        gg = html.escape(str(p["Global Grade"]))
        jf = html.escape(p["Job Family"])
        sf = html.escape(p["Sub Job Family"])
        cp = html.escape(p["Career Path"])
        fc = html.escape(p["Full Job Code"])

        html_code += f"""
        <div class="card-top">
            <div class="title">{job}</div>
            <div class="gg">GG {gg}</div>
            <div class="meta">
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        </div>
        """

    html_code += """
        </div>
    </div>

    <!-- BODY -->
    <div id="scroll-area">
        <div class="grid-desc">
    """

    # ---------- CONTENT ----------
    for sec in sections:

        html_code += "<div class='row'>"

        for p in profiles:
            val = p.get(sec, "")
            icon = icons_svg.get(sec, "")
            icon_block = f"<span class='icon-inline'>{icon}</span>"

            html_code += f"""
            <div class="section-box">
                <div class="section-title">{icon_block} {html.escape(sec)}</div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(str(val))}</div>
            </div>
            """

        html_code += "</div>"

    html_code += """
        </div>
    </div>

</div>

</body>
</html>
"""

    return html_code


# ---------------------------------------------------------
# RENDER HTML
# ---------------------------------------------------------
components.html(build_html(profiles), height=900, scrolling=False)
