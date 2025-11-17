# pages/3_Job_Profile_Description.py

import streamlit as st
import pandas as pd
import html
from pathlib import Path

st.set_page_config(page_title="Job Profile Description", layout="wide")

# HEADER
st.markdown("""
<div style='display:flex;align-items:center;gap:12px;'>
    <img src='assets/icons/business_review_clipboard.png' width='48'>
    <h1 style='margin:0;font-size:36px;font-weight:700;'>Job Profile Description</h1>
</div>
<hr style="margin-top:6px;margin-bottom:12px;">
""", unsafe_allow_html=True)

# CSS PARA O HTML
CSS = """
<style>

body {
    margin: 0;
    font-family: 'PPSIGFlow', sans-serif;
}

.jp-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}

.jp-card {
    background: #fff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    overflow: hidden;
    position: relative;
}

/* CABEÇALHO FIXO DENTRO DO CARD */
.jp-header {
    position: sticky;
    top: 0;
    background: #ffffff;
    padding: 22px 24px 16px 24px;
    z-index: 10;
    border-bottom: 1px solid #eee;
}

.jp-title {
    font-size: 1.3rem;
    font-weight: 700;
}

.jp-gg {
    font-size: 1rem;
    font-weight: 700;
    color: #145efc;
    margin-top: 8px;
    margin-bottom: 12px;
}

.jp-meta {
    background: #f5f4f1;
    padding: 12px 14px;
    border-radius: 10px;
    font-size: 0.92rem;
    line-height: 1.45;
}

/* CORPO DO CARD (SCROLL GLOBAL – NÃO TEM OVERFLOW AQUI) */
.jp-body {
    padding: 22px 24px 24px 24px;
}

.jp-section {
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 18px;
    margin-bottom: 20px;
}

.jp-section-title {
    font-size: 0.95rem;
    font-weight: 700;
    display: flex;
    gap: 8px;
    align-items: center;
}

.jp-section-title img {
    width: 20px;
    opacity: .8;
}

.jp-text {
    font-size: 0.90rem;
    line-height: 1.45;
    white-space: pre-wrap;
}

</style>
"""

# CARDS RENDERING FUNCTION (HTML)
def render_cards(cards):
    html_content = CSS
    html_content += "<div class='jp-grid'>"

    for c in cards:

        job = html.escape(c["Job Profile"])
        gg  = html.escape(str(c["Global Grade"]))
        jf  = html.escape(c["Job Family"])
        sf  = html.escape(c["Sub Job Family"])
        cp  = html.escape(c["Career Path"])
        fc  = html.escape(c["Full Job Code"])

        html_content += f"""
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

        for sec, icon in ICONS.items():
            content = c.get(sec, "")
            if not content or str(content).lower() == "nan":
                continue

            html_content += f"""
            <div class="jp-section">
                <div class="jp-section-title">
                    <img src="assets/icons/sig/{icon}">
                    {sec}
                </div>
                <div class="jp-text">{html.escape(str(content))}</div>
            </div>
            """

        html_content += "</div></div>"

    html_content += "</div>"
    return html_content


# ================================================
# LOAD DATA
# ================================================
@st.cache_data
def load():
    p = Path("data") / "Job Profile.xlsx"
    if not p.exists(): return pd.DataFrame()
    df = pd.read_excel(p)
    df.columns = df.columns.str.strip()
    return df

df = load()

# FILTERS
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())
col1, col2, col3 = st.columns(3)

with col1:
    family = st.selectbox("Job Family", ["Select..."] + families)

with col2:
    subs = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()) if family != "Select..." else []
    subfam = st.selectbox("Sub Job Family", ["Select..."] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == subfam]["Career Path"].dropna().unique()) if subfam != "Select..." else []
    cpath = st.selectbox("Career Path", ["Select..."] + paths)

flt = df.copy()
if family != "Select...": flt = flt[flt["Job Family"] == family]
if subfam != "Select...": flt = flt[flt["Sub Job Family"] == subfam]
if cpath != "Select...": flt = flt[flt["Career Path"] == cpath]

if flt.empty:
    st.info("No job profiles match the selected criteria.")
    st.stop()


# ICONS MAP
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

# MULTISELECT
flt["label"] = flt.apply(lambda r: f"GG {int(r['Global Grade'])} • {r['Job Profile']}", axis=1)

selected = st.multiselect("Select up to 3 job profiles:", flt["label"], max_selections=3)
if not selected:
    st.stop()

profiles = [flt[flt["label"] == s].iloc[0].to_dict() for s in selected]

# RENDER HTML CARDS WITH PERFECT STICKY
st.html(render_cards(profiles), scrolling=True, height=1500)
