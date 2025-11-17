# pages/3_Job_Profile_Description.py
# NEW LAYOUT – Job Profile Description (modern full-page synchronized scroll)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER
# ==========================================================
def header():
    st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;">
            <img src='assets/icons/business_review_clipboard.png' width='48'>
            <h1 style="margin:0;font-size:36px;font-weight:700;">Job Profile Description</h1>
        </div>
        <hr style="margin-top:6px;margin-bottom:12px;">
    """, unsafe_allow_html=True)

header()

# ==========================================================
# GLOBAL CSS — FINAL WORKDAY / WTW STYLE
# ==========================================================
st.markdown("""
<style>

.jp-grid {
    display: grid;
    gap: 24px;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
}

/* CARD */
.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    overflow: hidden;                    /* prevents content from leaking above */
    position: relative;
}

/* INTERNAL FIXED HEADER */
.jp-header {
    position: sticky;
    top: 0;                              /* 🔥 fixo dentro do card, NÃO na página */
    background: #ffffff;
    padding: 18px 22px 14px 22px;
    z-index: 10;
    border-bottom: 1px solid #eee;
}

/* TITLE & GG */
.jp-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 12px;
}

/* META */
.jp-meta {
    background: #f5f4f1;
    padding: 10px 12px;
    border-radius: 10px;
    font-size: 0.9rem;
    line-height: 1.35;
}

/* BODY (scroll global, not inside card) */
.jp-body {
    padding: 18px 22px;
}

/* SECTIONS */
.jp-section {
    margin-bottom: 22px;
    padding-bottom: 16px;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.92rem;
    margin-bottom: 8px;
    display:flex;
    align-items:center;
    gap:8px;
}

.jp-section-title img {
    width:20px;
    opacity:0.8;
}

.jp-text {
    font-size:0.9rem;
    line-height:1.45;
    white-space:pre-wrap;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
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

# ==========================================================
# FILTERS
# ==========================================================
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

# ==========================================================
# PICKLIST
# ==========================================================
flt["label"] = flt.apply(
    lambda r: f"GG {int(r['Global Grade'])} • {r['Job Profile']}",
    axis=1
)

label_map = dict(zip(flt["label"], flt["Job Profile"]))

selected = st.multiselect(
    "Select up to 3 job profiles:",
    list(label_map.keys()),
    max_selections=3
)

if not selected:
    st.info("Please select at least one job profile.")
    st.stop()

profiles = [label_map[x] for x in selected]
cards = [flt[flt["Job Profile"] == p].iloc[0].to_dict() for p in profiles]

# ==========================================================
# ICONS
# ==========================================================
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

# ==========================================================
# BUILD CARDS
# ==========================================================
html_parts = ['<div class="jp-grid">']

for c in cards:

    job = html.escape(c["Job Profile"])
    gg  = html.escape(str(c["Global Grade"]))
    jf  = html.escape(c["Job Family"])
    sf  = html.escape(c["Sub Job Family"])
    cp  = html.escape(c["Career Path"])
    fc  = html.escape(c["Full Job Code"])

    card = []
    card.append('<div class="jp-card">')

    # HEADER (FIXED INSIDE CARD)
    card.append('<div class="jp-header">')
    card.append(f'<div class="jp-title">{job}</div>')
    card.append(f'<div class="jp-gg">GG {gg}</div>')
    card.append('<div class="jp-meta">')
    card.append(f"<div><b>Job Family:</b> {jf}</div>")
    card.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    card.append(f"<div><b>Career Path:</b> {cp}</div>")
    card.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    card.append('</div></div>')

    # BODY (FOLLOWS PAGE SCROLL)
    card.append('<div class="jp-body">')

    for sec in sections:
        content = str(c.get(sec, "")).strip()
        if not content or content.lower() == "nan":
            continue

        icon = icons[sec]

        card.append('<div class="jp-section">')
        card.append(f'<div class="jp-section-title"><img src="assets/icons/sig/{icon}">{sec}</div>')
        card.append(f'<div class="jp-text">{html.escape(content)}</div>')
        card.append('</div>')

    card.append('</div></div>')  # close body and card

    html_parts.append("".join(card))

html_parts.append("</div>")
st.markdown("".join(html_parts), unsafe_allow_html=True)
