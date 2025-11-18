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
# LOAD PAGE ICON (PNG) AS BASE64
# ---------------------------------------------------------
def load_icon_png(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

page_icon_b64 = load_icon_png("assets/icons/business_review_clipboard.png")

# ---------------------------------------------------------
# HEADER — ÍCONE + TÍTULO + ESPAÇO + SUBTÍTULO
# ---------------------------------------------------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-bottom:6px; margin-top:10px;">
    <img src="data:image/png;base64,{page_icon_b64}" style="width:48px; height:48px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Profile Description
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:36px;">
""", unsafe_allow_html=True)

# Subtítulo sem ícone de lupa
st.markdown("""
### Job Profile Description Explorer
""")

# ==========================================================
# GLOBAL LAYOUT — limita largura e impede esticar infinito
# ==========================================================
st.markdown("""
<style>

    /* Container principal do Streamlit */
    .main > div {
        max-width: 1400px;    /* limite máximo elegante */
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* Estilo para dataframes */
    .stDataFrame {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Estilo para cards / container padrão */
    .block-container, .stColumn {
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD DATA
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

# Icones SVG
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
# BUILD HTML
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

/* GRID PERFEITAMENTE DISTRIBUÍDO (FULL WIDTH) */
.grid-top {{
    display: grid;
    grid-template-columns: repeat({n}, 1fr);
    gap: 24px;
    width: 100%;
}}

.grid-desc {{
    display: grid;
    grid-template-columns: repeat({n}, 1fr);
    gap: 28px;
    width: 100%;
}}

/* CARD SUPERIOR → AGORA FUNDO SAND1 */
.card-top {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: none;
    border: 1px solid #e3e1dd;
}}

.title {{
    font-size: 20px;
    font-weight: 700;
    line-height: 1.25;
}}

.gg {{
    color: #145efc;
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
}}

.meta {{
    background: white;
    padding: 14px;
    margin-top: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
}}

/* SCROLL AREA */
#scroll-area {{
    flex: 1;
    overflow-y: auto;
    padding: 20px 4px 32px 4px;
}}

/* SECTION PERFEITAMENTE ALINHADA POR LINHAS */
.row {{
    display: contents;
}}

.section-box {{
    padding-bottom: 28px;
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

    <div id="top-area">
        <div class="grid-top">
    """

    # Top Cards
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

    <div id="scroll-area">
        <div class="grid-desc">
    """

    for sec in sections:
        html_code += "<div class='row'>"
        for p in profiles:
            val = p.get(sec, "")
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
        html_code += "</div>"

    html_code += """
        </div>
    </div>

</div>

</body></html>
"""
    return html_code

# Render
components.html(build_html(profiles), height=900, scrolling=False)
