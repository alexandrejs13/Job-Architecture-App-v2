# pages/3_Job_Profile_Description.py
# FINAL – ONE SINGLE PAGE SCROLL (NO INTERNAL SCROLL)

import streamlit as st
import pandas as pd
import html
from pathlib import Path
import streamlit.components.v1 as components

# ---------------------------------------------
# PAGE CONFIG
# ---------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ---------------------------------------------
# PAGE HEADER
# ---------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin:0;">Job Profile Description</h1>
<hr style="margin-top:10px;">
""", unsafe_allow_html=True)

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df

df = load_job_profile()

if df.empty:
    st.error("Error loading Job Profile.xlsx")
    st.stop()

# ---------------------------------------------
# FILTERS
# ---------------------------------------------
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())

c1, c2, c3 = st.columns(3)

with c1:
    family = st.selectbox("Job Family", ["Select..."] + families)

with c2:
    subs = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()) if family != "Select..." else []
    subfam = st.selectbox("Sub Job Family", ["Select..."] + subs)

with c3:
    paths = sorted(df[df["Sub Job Family"] == subfam]["Career Path"].dropna().unique()) if subfam != "Select..." else []
    path = st.selectbox("Career Path", ["Select..."] + paths)

flt = df.copy()
if family != "Select...": flt = flt[flt["Job Family"] == family]
if subfam != "Select...": flt = flt[flt["Sub Job Family"] == subfam]
if path != "Select...": flt = flt[flt["Career Path"] == path]

if flt.empty:
    st.info("No profiles found.")
    st.stop()

flt["label"] = flt.apply(lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}", axis=1)
label_to_job = dict(zip(flt["label"], flt["Job Profile"]))

selected = st.multiselect("Select up to 3 profiles to compare:", flt["label"].tolist(), max_selections=3)

if not selected:
    st.stop()

profiles = [flt[flt["Job Profile"] == label_to_job[x]].iloc[0].to_dict() for x in selected]

# ---------------------------------------------
# ICONS & SECTIONS
# ---------------------------------------------
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
sections = list(icons.keys())

# ---------------------------------------------
# BUILD HTML (WITHOUT INTERNAL SCROLL)
# ---------------------------------------------
def build_html(profiles):

    n = len(profiles)
    grid_class = f"cols-{n}"

    html_page = f"""
    <html>
    <head>
    <style>

    body {{
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', sans-serif;
        background: #ffffff;
    }}

    /* GRID */
    .grid {{
        display: grid;
        gap: 24px;
        width: 100%;
    }}
    .cols-1 {{ grid-template-columns: 1fr; }}
    .cols-2 {{ grid-template-columns: 1fr 1fr; }}
    .cols-3 {{ grid-template-columns: 1fr 1fr 1fr; }}

    /* CARD */
    .card {{
        background: #fff;
        border: 1px solid #e4e4e4;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        display: flex;
        flex-direction: column;
        overflow: visible; 
    }}

    /* HEADER STICKY */
    .header {{
        background: #fff;
        padding: 22px;
        border-bottom: 1px solid #eee;
        position: sticky;
        top: 0;
        z-index: 10;
    }}

    .title {{
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 6px;
    }}

    .gg {{
        font-size: 18px;
        font-weight: 700;
        color: #145efc;
        margin-bottom: 12px;
    }}

    .meta {{
        background: #f4f2ec;
        padding: 12px;
        border-radius: 10px;
        font-size: 0.9rem;
    }}

    /* BODY (NO INTERNAL SCROLL) */
    .body {{
        padding: 22px;
        overflow: visible; 
    }}

    .section {{
        margin-bottom: 18px;
        padding-bottom: 16px;
        border-bottom: 1px solid #f0f0f0;
    }}

    .section-title {{
        font-size: 0.95rem;
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
        font-size: 0.88rem;
        line-height: 1.40;
        white-space: pre-wrap;
    }}

    </style>
    </head>

    <body>
        <div class="grid {grid_class}">
    """

    for p in profiles:

        job = html.escape(p.get("Job Profile", ""))
        gg = html.escape(str(p.get("Global Grade", "")).replace(".0",""))
        jf = html.escape(p.get("Job Family", ""))
        sf = html.escape(p.get("Sub Job Family", ""))
        cp = html.escape(p.get("Career Path", ""))
        fc = html.escape(p.get("Full Job Code", ""))

        html_page += f"""
        <div class="card">

            <div class="header">
                <div class="title">{job}</div>
                <div class="gg">GG {gg}</div>

                <div class="meta">
                    <div><b>Job Family:</b> {jf}</div>
                    <div><b>Sub Job Family:</b> {sf}</div>
                    <div><b>Career Path:</b> {cp}</div>
                    <div><b>Full Job Code:</b> {fc}</div>
                </div>
            </div>

            <div class="body">
        """

        for sec in sections:
            val = p.get(sec, "")
            if isinstance(val, float) and pd.isna(val):
                continue
            val = str(val).strip()
            if not val:
                continue

            icon = icons[sec]
            html_page += f"""
            <div class="section">
                <div class="section-title">
                    <img src="assets/icons/sig/{icon}">
                    {html.escape(sec)}
                </div>
                <div class="text">{html.escape(val)}</div>
            </div>
            """

        html_page += "</div></div>"

    html_page += """
        </div>
    </body>
    </html>
    """

    return html_page


# ---------------------------------------------
# RENDER FINAL LAYOUT (PAGE SCROLL ONLY)
# ---------------------------------------------
html_final = build_html(profiles)

components.html(html_final, height=2000, scrolling=True)
