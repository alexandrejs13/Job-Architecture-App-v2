# pages/3_Job_Profile_Description.py
# Job Profile Description – comparison of up to 3 profiles

import html
from pathlib import Path

import pandas as pd
import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")


# ==========================================================
# HEADER
# ==========================================================
def header(icon_path: str, title: str) -> None:
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    # subtle divider
    st.markdown("<hr style='margin-top:8px; margin-bottom:4px;'>", unsafe_allow_html=True)


header("assets/icons/business_review_clipboard.png", "Job Profile Description")


# ==========================================================
# GLOBAL CSS
# ==========================================================
custom_css = """
<style>
/* ------------- Fonts ------------- */
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
    font-weight: 400;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-SemiBold.otf') format('opentype');
    font-weight: 600;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: 700;
}

/* base app */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif !important;
    background: #ffffff !important;
    color: #222222 !important;
}

.block-container {
    max-width: 1600px !important;
    padding-top: 0.5rem !important;
}

/* ------------- Comparison layout ------------- */

.jp-page {
    width: 100%;
}

/* sticky strip that keeps the 3 header cards always visible */
.jp-header-row {
    position: sticky;
    top: 80px;  /* below Streamlit top bar + page title */
    z-index: 40;
    padding: 4px 0 14px 0;
    /* white background so text from sections never appears behind */
    background: linear-gradient(
        to bottom,
        #ffffff 0%,
        #ffffff 70%,
        rgba(255,255,255,0.96) 85%,
        rgba(255,255,255,0.0) 100%
    );
}

/* common grid for header and body rows */
.jp-header-row,
.jp-body-row {
    display: grid;
    gap: 24px;
}

/* header cards – ONLY title + GG + meta block */
.jp-header-card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e6e6e6;
    box-shadow: 0 6px 14px rgba(15, 18, 35, 0.10);
    padding: 20px 22px 18px 22px;
}

/* body row with all long descriptions */
.jp-body-row {
    margin-top: 8px;
    display: grid;
    gap: 24px;
}

/* body cards – continuous content sections */
.jp-body-card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e6e6e6;
    box-shadow: 0 4px 10px rgba(15, 18, 35, 0.08);
    padding: 16px 22px 8px 22px;
}

/* title & GG inside header card */
.jp-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 14px;
}

/* meta block under the GG */
.jp-meta-block {
    background: #f5f4f1;
    border-radius: 12px;
    padding: 10px 13px;
    font-size: 0.92rem;
}

/* Section blocks inside body card */
.jp-section {
    padding: 14px 0 14px 0;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section:last-child {
    border-bottom: none;
    padding-bottom: 6px;
}

.jp-section.alt {
    background: #fafafa;
    margin: 0 -22px;
    padding-left: 22px;
    padding-right: 22px;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.jp-section-title img {
    width: 20px;
    opacity: 0.9;
}

.jp-text {
    line-height: 1.45;
    font-size: 0.9rem;
    white-space: pre-wrap;
}

/* subtle footer with PDF icon */
.jp-footer {
    padding-top: 12px;
    text-align: right;
}

.jp-footer img {
    width: 26px;
    opacity: 0.8;
    cursor: pointer;
}

.jp-footer img:hover {
    opacity: 1;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================================
# LOAD JOB PROFILE TABLE
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
    st.error("Error loading Job Profile.xlsx. Please check the file in the data folder.")
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
    if family != "Select...":
        subs = sorted(
            df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
        )
    else:
        subs = []
    sub_family = st.selectbox("Sub Job Family", ["Select..."] + subs)

with col3:
    if sub_family != "Select...":
        paths = sorted(
            df[df["Sub Job Family"] == sub_family]["Career Path"]
            .dropna()
            .unique()
        )
    else:
        paths = []
    career_path = st.selectbox("Career Path", ["Select..."] + paths)

# apply filters
filtered = df.copy()
if family != "Select...":
    filtered = filtered[filtered["Job Family"] == family]
if sub_family != "Select...":
    filtered = filtered[filtered["Sub Job Family"] == sub_family]
if career_path != "Select...":
    filtered = filtered[filtered["Career Path"] == career_path]

# build label for the multiselect
if not filtered.empty:
    filtered = filtered.copy()
    filtered["label"] = filtered.apply(
        lambda r: f"GG {str(r.get('Global Grade', '')).replace('.0','')} • {r.get('Job Profile', '')}",
        axis=1,
    )
    label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))
else:
    label_to_profile = {}

selected_labels = st.multiselect(
    "Select up to 3 profiles to compare:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selected_labels:
    st.info("Please select at least one profile to see the comparison.")
    st.stop()

selected_profiles = [label_to_profile[l] for l in selected_labels]
rows = [
    filtered[filtered["Job Profile"] == p].iloc[0].to_dict()
    for p in selected_profiles
]

num_cols = len(rows)
grid_style = f"grid-template-columns: repeat({num_cols}, minmax(320px, 1fr));"


# ==========================================================
# ICONS & SECTIONS
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

sections_order = list(icons.keys())


# ==========================================================
# BUILD HTML FOR HEADER CARDS + BODY CARDS
# ==========================================================
page_html_parts = [f'<div class="jp-page">']

# ----- sticky header row -----
page_html_parts.append(
    f'<div class="jp-header-row" style="{grid_style}">'
)

for card in rows:
    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", ""))).replace(".0", "")
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    header_card_html = []
    header_card_html.append('<div class="jp-header-card">')
    header_card_html.append(f'<div class="jp-title">{job}</div>')
    header_card_html.append(f'<div class="jp-gg">GG {gg}</div>')
    header_card_html.append('<div class="jp-meta-block">')
    header_card_html.append(f"<div><b>Job Family:</b> {jf}</div>")
    header_card_html.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    header_card_html.append(f"<div><b>Career Path:</b> {cp}</div>")
    header_card_html.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    header_card_html.append("</div>")  # meta-block
    header_card_html.append("</div>")  # jp-header-card

    page_html_parts.append("".join(header_card_html))

page_html_parts.append("</div>")  # end header row


# ----- body row with continuous descriptions -----
page_html_parts.append(
    f'<div class="jp-body-row" style="{grid_style}">'
)

for card in rows:
    body_html = []
    body_html.append('<div class="jp-body-card">')

    # each section in fixed order if content exists
    for idx, sec in enumerate(sections_order):
        raw_content = str(card.get(sec, "") or "").strip()
        if not raw_content or raw_content.lower() == "nan":
            continue

        icon_file = icons.get(sec, "")
        alt_class = " alt" if idx % 2 == 1 else ""

        body_html.append(f'<div class="jp-section{alt_class}">')
        if icon_file:
            body_html.append(
                f'<div class="jp-section-title">'
                f'<img src="assets/icons/sig/{icon_file}"> {sec}'
                f'</div>'
            )
        else:
            body_html.append(f'<div class="jp-section-title">{sec}</div>')

        body_html.append(
            f'<div class="jp-text">{html.escape(raw_content)}</div>'
        )
        body_html.append("</div>")  # jp-section

    # footer with (future) PDF export icon
    body_html.append('<div class="jp-footer">')
    body_html.append(
        '<img src="assets/icons/sig/pdf_c3_white.svg" title="Export to PDF">'
    )
    body_html.append("</div>")  # jp-footer

    body_html.append("</div>")  # jp-body-card

    page_html_parts.append("".join(body_html))

page_html_parts.append("</div>")  # end body row
page_html_parts.append("</div>")  # end jp-page wrapper

st.markdown("".join(page_html_parts), unsafe_allow_html=True)
