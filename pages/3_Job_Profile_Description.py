# pages/3_Job_Profile_Description.py
# FINAL VERSION – FULL HTML LAYOUT WITH ST.HTML (OPTION A)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# -----------------------------------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin:0;">
    Job Profile Description
</h1>
<hr style="margin-top:8px;">
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CSS – FULL CONTROL
# -----------------------------------------------------------------------------
CSS = """
<style>

body, html, [data-testid="stAppViewContainer"] {
    font-family: 'Segoe UI', sans-serif !important;
}

/* GRID OF CARDS */
.jp-grid {
    display: grid;
    gap: 30px;
    width: 100%;
}

/* 1, 2 or 3 columns depending on selection */
.cols-1 { grid-template-columns: 1fr; }
.cols-2 { grid-template-columns: 1fr 1fr; }
.cols-3 { grid-template-columns: 1fr 1fr 1fr; }

/* CARD */
.jp-card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e5e5e5;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    height: 82vh;              /* FIXED HEIGHT – REQUIRED */
    display: flex;
    flex-direction: column;
    overflow: hidden;          /* prevents invading */
}

/* STICKY HEADER INSIDE CARD */
.jp-card-header {
    background: #ffffff;
    padding: 20px 24px 16px 24px;
    border-bottom: 1px solid #eee;
    position: sticky;
    top: 0;
    z-index: 3;
}

.jp-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    font-size: 18px;
    font-weight: 700;
    color: #145efc;
    margin-bottom: 12px;
}

/* META */
.jp-meta {
    background: #f4f2ec;
    padding: 12px 14px;
    border-radius: 12px;
    font-size: 0.90rem;
}

/* BODY THAT SCROLLS */
.jp-body {
    padding: 20px 24px 24px 24px;
    overflow-y: auto;
    flex: 1;
}

/* SECTION */
.jp-section {
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section:last-child {
    border-bottom: none;
}

.jp-section-title {
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.jp-section-title img {
    width: 20px;
}

.jp-text {
    font-size: 0.88rem;
    line-height: 1.40;
    white-space: pre-wrap;
}

</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
@st.cache_data(ttl=600)
def load_job_profile():
    p = Path("data") / "Job Profile.xlsx"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_excel(p)
    df.columns = df.columns.str.strip()
    return df

df = load_job_profile()
if df.empty:
    st.error("Error loading Job Profile.xlsx")
    st.stop()

# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# ICONS
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# RENDER HTML
# -----------------------------------------------------------------------------

def render_cards(profiles):
    n = len(profiles)
    cls = f"cols-{n}"

    html_out = f'<div class="jp-grid {cls}">'

    for p in profiles:
        job = html.escape(p.get("Job Profile", ""))
        gg = html.escape(str(p.get("Global Grade", "")).replace(".0", ""))
        jf = html.escape(p.get("Job Family", ""))
        sf = html.escape(p.get("Sub Job Family", ""))
        cp = html.escape(p.get("Career Path", ""))
        fc = html.escape(p.get("Full Job Code", ""))

        html_out += """
        <div class="jp-card">
            <div class="jp-card-header">
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
        """.format(job=job, gg=gg, jf=jf, sf=sf, cp=cp, fc=fc)

        for sec in sections:
            val = p.get(sec, "")
            if isinstance(val, float) and pd.isna(val):
                continue
            val = str(val).strip()
            if not val:
                continue

            sec_html = html.escape(sec)
            val_html = html.escape(val)
            icon = icons[sec]

            html_out += f"""
            <div class="jp-section">
                <div class="jp-section-title">
                    <img src="assets/icons/sig/{icon}">
                    {sec_html}
                </div>
                <div class="jp-text">{val_html}</div>
            </div>
            """

        html_out += "</div></div>"  # close jp-body and jp-card

    html_out += "</div>"  # close grid
    return html_out


html_final = render_cards(profiles)

# -----------------------------------------------------------------------------
# RENDER
# -----------------------------------------------------------------------------
st.html(html_final, height=900)

