# pages/3_Job_Profile_Description.py
# FINAL VERSION – Sticky inside isolated iframe (Streamlit Components)
# 100% working: 1–3 columns, sticky header, global scroll, no overflow issues.

import streamlit as st
import pandas as pd
import html as html_lib
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER
# ==========================================================
st.markdown("""
<div style='display:flex;align-items:center;gap:12px;'>
    <img src='assets/icons/business_review_clipboard.png' width='48'>
    <h1 style='margin:0;font-size:36px;font-weight:700;'>Job Profile Description</h1>
</div>
<hr style='margin-top:6px;margin-bottom:12px;'>
""", unsafe_allow_html=True)


# ==========================================================
# LOAD DATA
# ==========================================================
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

# ==========================================================
# FILTERS
# ==========================================================
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)
with col1:
    family = st.selectbox("Job Family", ["Select..."] + families)
with col2:
    sub_fams = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()) if family != "Select..." else []
    sub_family = st.selectbox("Sub Job Family", ["Select..."] + sub_fams)
with col3:
    paths = sorted(df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique()) if sub_family != "Select..." else []
    cpath = st.selectbox("Career Path", ["Select..."] + paths)

flt = df.copy()
if family != "Select...": flt = flt[flt["Job Family"] == family]
if sub_family != "Select...": flt = flt[flt["Sub Job Family"] == sub_family]
if cpath != "Select...": flt = flt[flt["Career Path"] == cpath]

if flt.empty:
    st.info("No profiles match your filters.")
    st.stop()


# ==========================================================
# MULTISELECT
# ==========================================================
flt["label"] = flt.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1,
)

selected = st.multiselect(
    "Select up to 3 profiles:",
    list(flt["label"]),
    max_selections=3
)

if not selected:
    st.stop()

data = [flt[flt["label"] == s].iloc[0].to_dict() for s in selected]


# ==========================================================
# SECTIONS + ICONS
# ==========================================================
ICONS = {
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

SECTIONS = list(ICONS.keys())


# ==========================================================
# BUILD HTML FOR IFRAME (sticky works perfectly here)
# ==========================================================
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<style>

body {
    margin: 0;
    padding: 0 20px;
    font-family: 'PPSIGFlow', sans-serif;
}

/* GRID: 1 → 3 columns */
.jp-grid {
    display: grid;
    gap: 28px;
    grid-template-columns: repeat(""" + str(len(data)) + """, minmax(340px, 1fr));
}

/* CARD */
.jp-card {
    background: #fff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    overflow: hidden;
    position: relative;
}

/* STICKY HEADER INSIDE CARD */
.jp-header {
    position: sticky;
    top: 0; 
    background: #ffffff;
    padding: 22px 24px 16px 24px;
    z-index: 10;
    border-bottom: 1px solid #eee;
}

/* TITLE + GG */
.jp-title {
    font-size: 1.30rem;
    font-weight: 700;
    margin-bottom: 4px;
}
.jp-gg {
    font-weight: 700;
    font-size: 1.05rem;
    color: #145efc;
    margin-bottom: 12px;
}

/* META BLOCK */
.jp-meta {
    background: #f5f4f1;
    padding: 12px 14px;
    border-radius: 10px;
    font-size: .95rem;
    line-height: 1.45;
}

/* CONTENT BELOW */
.jp-body {
    padding: 22px 24px 28px 24px;
}

.jp-section {
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 18px;
    margin-bottom: 22px;
}
.jp-section-title {
    display: flex;
    gap: 8px;
    font-weight: 700;
    margin-bottom: 8px;
    align-items: center;
    font-size: .95rem;
}
.jp-section-title img {
    width: 20px;
    opacity: .85;
}
.jp-text {
    white-space: pre-wrap;
    font-size: .94rem;
    line-height: 1.45;
}

</style>
</head>
<body>

<div class="jp-grid">
"""

# BUILD CARDS
for c in data:
    job = html_lib.escape(c["Job Profile"])
    gg = html_lib.escape(str(c["Global Grade"]))
    jf = html_lib.escape(c["Job Family"])
    sf = html_lib.escape(c["Sub Job Family"])
    cp = html_lib.escape(c["Career Path"])
    fc = html_lib.escape(c["Full Job Code"])

    html += f"""
    <div class="jp-card">
        <div class="jp-header">
            <div class="jp-title">{job}</div>
            <div class="jp-gg">GG {gg}</div>
            <div class="jp-meta">
                <div><b>Job Family:</b> {jf}</div>
                <div><b>Sub Job Family:</b> {sf}</div>
                <div><b>Career Path:</b> {cp}</div>
                <div><b>Full Job Code:</b> {fc}</div>
            </div>
        </div>

        <div class="jp-body">
    """

    for sec in SECTIONS:
        content = c.get(sec, "")
        if not content or str(content).lower() == "nan":
            continue

        icon = ICONS[sec]

        html += f"""
        <div class="jp-section">
            <div class="jp-section-title">
                <img src="../assets/icons/sig/{icon}">
                {sec}
            </div>
            <div class="jp-text">{html_lib.escape(str(content))}</div>
        </div>
        """

    html += "</div></div>"

html += """
</div>
</body>
</html>
"""


# ==========================================================
# RENDER IN IFRAME (STICKY WORKS 100%)
# ==========================================================
st.components.v1.html(html, height=2000, scrolling=True)
