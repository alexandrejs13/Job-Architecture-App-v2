import streamlit as st
import pandas as pd
import base64, os
import altair as alt

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# ICON
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_job_profile():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_job_profile()

# column mapping
COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_GRADE = "Global Grade"
COL_PATH = "Career Path"

# ==========================================================
# CSS — Cards SIG
# ==========================================================
st.markdown("""
<style>

section.main > div {
    max-width: 1180px;
    padding-left: 10px;
    padding-right: 10px;
}

/* Grid auto-fit responsivo */
.sig-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
}

/* Card SIG */
.sig-card {
    background: #F2EFEB;  /* SIG Sand 1 */
    border-radius: 14px;
    border: 1px solid #E5E0D8;
    padding: 14px 18px;
    height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.sig-title {
    font-size: 14px;
    font-weight: 600;
    color: #000;
}

.sig-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC;  /* SIG Sky */
}

.block-space {
    margin-top: 32px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# TABS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])


# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # KPIs
    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
        "Career Paths": df[COL_PATH].nunique(),
    }

    st.markdown("<div class='sig-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
            <div class="sig-card">
                <div class="sig-title">{title}</div>
                <div class="sig-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


    # ======================================================
    # GRAPH 1 — Subfamilies per Family (Pizza SIG)
    # ======================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Subfamilies per Family")

    pizza_df = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    # SIG cores oficiais
    SIG_COLORS = [
        "#145EFC", "#dca0ff", "#4fa593", "#167665",
        "#00493b", "#f5f073", "#c0b846", "#a0b905"
    ]

    base = alt.Chart(pizza_df).encode(
        theta=alt.Theta("Count:Q"),
        color=alt.Color("Job Family:N", scale=alt.Scale(range=SIG_COLORS)),
        tooltip=[COL_FAMILY, "Count"]
    )

    chart_pizza = base.mark_arc(innerRadius=65, outerRadius=120)

    colA, colB = st.columns([1,1])

    with colA:
        st.altair_chart(chart_pizza, use_container_width=True)

    with colB:
        for i, row in pizza_df.iterrows():
            color = SIG_COLORS[i % len(SIG_COLORS)]
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <div style="width:12px; height:12px; background:{color}; border-radius:50%;"></div>
                    <div style="font-weight:600; font-size:16px;">{row[COL_FAMILY]}</div>
                    <div style="margin-left:auto; background:{color}; color:white; padding:2px 10px; font-size:13px; border-radius:10px;">
                        {row["Count"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ======================================================
    # GRAPH 2 — Profiles per Subfamily (Total)
    # ======================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily (Total)")

    bar_df = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bar_chart = (
        alt.Chart(bar_df)
        .mark_bar(size=22, color="#145EFC")
        .encode(
            x=alt.X("Count:Q", title="Count"),
            y=alt.Y("Sub Job Family:N", sort="-x", title=""),
            tooltip=["Sub Job Family", "Count"]
        )
        .properties(height=650)
    )

    st.altair_chart(bar_chart, use_container_width=True)



# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    fam = st.selectbox("Select Family:", families)

    fam_df = df[df[COL_FAMILY] == fam]

    metrics = {
        "Subfamilies": fam_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
        "Career Paths": fam_df[COL_PATH].nunique(),
        "Profiles / Subfamily": round(fam_df[COL_PROFILE].nunique() / max(fam_df[COL_SUBFAMILY].nunique(),1), 1),
    }

    st.markdown("<div class='sig-grid'>", unsafe_allow_html=True)
    for title, value in metrics.items():
        st.markdown(
            f"""
            <div class="sig-card">
                <div class="sig-title">{title}</div>
                <div class="sig-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


    # Bar chart local (clean)
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown(f"## Profiles per Subfamily — {fam}")

    sub_df = (
        fam_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    chart_local = (
        alt.Chart(sub_df)
        .mark_bar(size=22, color="#145EFC")
        .encode(
            x="Count:Q",
            y=alt.Y("Sub Job Family:N", sort="-x", title=""),
            tooltip=["Sub Job Family", "Count"]
        )
        .properties(height=500)
    )

    st.altair_chart(chart_local, use_container_width=True)


    # Table
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("### Full Job Profile Listing")
    st.dataframe(
        fam_df[[COL_SUBFAMILY, COL_PROFILE, COL_PATH, COL_GRADE]],
        use_container_width=True
    )
