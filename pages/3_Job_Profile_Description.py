import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# -------------------------------------------------------------------
# HEADER
# -------------------------------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin-bottom:4px;">
    Job Profile Description
</h1>
<hr style="margin-top:0;">
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------------
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()

# -------------------------------------------------------------------
# FILTERS
# -------------------------------------------------------------------
st.subheader("🔍 Job Profile Description Explorer")

c1, c2, c3 = st.columns(3)

with c1:
    job_family = st.selectbox(
        "Job Family", 
        ["All"] + sorted(df["Job Family"].dropna().unique())
    )

with c2:
    subfam_list = df[df["Job Family"] == job_family]["Sub Job Family"].dropna().unique() \
                   if job_family != "All" else df["Sub Job Family"].dropna().unique()

    sub_family = st.selectbox(
        "Sub Job Family",
        ["All"] + sorted(subfam_list)
    )

with c3:
    path_list = df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique() \
                if sub_family != "All" else df["Career Path"].dropna().unique()

    career_path = st.selectbox(
        "Career Path",
        ["All"] + sorted(path_list)
    )

flt = df.copy()

if job_family != "All":
    flt = flt[flt["Job Family"] == job_family]
if sub_family != "All":
    flt = flt[flt["Sub Job Family"] == sub_family]
if career_path != "All":
    flt = flt[flt["Career Path"] == career_path]

# LABEL = A) Global Grade + Job Profile
flt["label"] = flt["Global Grade"].astype(str) + " • " + flt["Job Profile"]

selected = st.multiselect(
    "Select up to 3 profiles:",
    flt["label"].tolist(),
    max_selections=3
)

if not selected:
    st.stop()

profiles = [
    flt[flt["label"] == s].iloc[0].to_dict()
    for s in selected
]

# -------------------------------------------------------------------
# SECTIONS
# -------------------------------------------------------------------
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

icons = {
    "Sub Job Family Description": "Hierarchy.svg",
    "Job Profile Description": "File_Clipboard_Text.svg",
    "Career Band Description": "Hierarchy.svg",
    "Role Description": "Shopping_Business_Suitcase.svg",
    "Grade Differentiator": "Edit_Pencil.svg",
    "Qualifications": "Content_Book_Phone.svg",
    "Specific parameters / KPIs": "Graph_Bar.svg",
    "Competencies 1": "Setting_Cog.svg",
    "Competencies 2": "Setting_Cog.svg",
    "Competencies 3": "Setting_Cog.svg",
}

# -------------------------------------------------------------------
# BUILD HTML FINAL
# -------------------------------------------------------------------
def build_html(profiles):

    n = len(profiles)

    html_code = f"""
    <html>
    <head>
    <style>

    html, body, #wrap {{
        margin: 0;
        padding: 0;
        overflow: visible !important;
        font-family: 'Segoe UI', sans-serif;
    }}

    /* GRID */
    .grid {{
        display: grid;
        grid-template-columns: repeat({n}, 1fr);
        gap: 32px;
        width: 100%;
    }}

    /* TOP CARDS (sticky) */
    .card-top {{
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
        position: sticky;
        top: 0;
        z-index: 50;
    }}

    .title {{
        font-size: 22px;
        font-weight: 700;
    }}

    .gg {{
        color: #145efc;
        font-size: 18px;
        font-weight: 700;
        margin-top: 8px;
    }}

    .meta {{
        background: #f5f3ee;
        border: 1px solid #e3e1dd;
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
        font-size: 15px;
        line-height: 1.45;
    }}

    /* SCROLL AREA (UNIFIED SCROLL dynamic height) */
    .scroll-area {{
        height: calc(100vh - 330px);   /* 🔥🔥 PATCH APLICADO AQUI */
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 12px;
        margin-top: 26px;
    }}

    /* DESCRIPTION CARDS */
    .card-desc {{
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}

    .section-title {{
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .section-title img {{
        width: 20px;
    }}

    .text {{
        font-size: 15px;
        line-height: 1.45;
        white-space: pre-wrap;
        margin-bottom: 18px;
    }}

    </style>
    </head>

    <body>
    <div id="wrap">

        <!-- TOP CARDS -->
        <div class="grid">
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

    # ---------- DESCRIPTION SECTION (scroll único) ----------
    html_code += """
        </div>

        <div class="scroll-area">
            <div class="grid">
    """

    for p in profiles:
        html_code += "<div class='card-desc'>"

        for sec in sections:
            val = p.get(sec, "")
            if not val or str(val).strip() == "":
                continue

            icon = icons[sec]

            html_code += f"""
                <div class="section-title">
                    <img src="assets/icons/sig/{icon}">
                    {html.escape(sec)}
                </div>
                <div class="text">{html.escape(str(val))}</div>
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

# -------------------------------------------------------------------
# RENDER HTML
# -------------------------------------------------------------------
components.html(build_html(profiles), height=1800, scrolling=False)
