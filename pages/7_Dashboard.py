# ==========================================================
# GLOBAL PAGE CSS — PADRÃO SIG (LARGURA FIXA)
# ==========================================================
st.markdown("""
<style>
/* Normaliza largura igual às demais páginas */
section.main > div { 
    max-width: 1180px !important;
    padding-left: 12px;
    padding-right: 12px;
}

/* Cards SIG slim */
.sig-card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.sig-card {
    background: #F2EFEB;
    padding: 14px 18px;
    border-radius: 14px;
    border: 1px solid #E6E0D8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    height: 95px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.sig-card-title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
}

.sig-card-value {
    font-size: 28px;
    font-weight: 800;
    color: #145EFC;
    margin-top: -2px;
}

/* Small icons aligned */
.sig-icon-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
}
.sig-small-icon {
    width: 32px;
    height: 32px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])



# ==========================================================
# TAB 1 — OVERVIEW MELHORADO
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # Basic metrics
    total_families   = df[COL_FAMILY].nunique()
    total_subfamilies = df[COL_SUBFAMILY].nunique()
    total_profiles   = df[COL_PROFILE].nunique()
    total_paths      = df[COL_CAREER_PATH].nunique()
    total_bands      = df[COL_BAND].nunique()
    total_grades     = df[COL_GRADE].nunique()

    # Additional richness
    avg_per_family = round(total_profiles / total_families, 1)
    avg_per_sub = round(total_profiles / total_subfamilies, 1)

    family_size = df.groupby(COL_FAMILY)[COL_PROFILE].nunique()
    largest_family = family_size.idxmax()
    largest_pct = round(family_size.max() / total_profiles * 100, 1)

    overview_cards = {
        "Total Families": total_families,
        "Total Subfamilies": total_subfamilies,
        "Total Job Profiles": total_profiles,
        "Total Career Paths": total_paths,
        "Total Career Bands": total_bands,
        "Total Global Grades": total_grades,
        "Avg Profiles per Family": avg_per_family,
        "Avg Profiles per Subfamily": avg_per_sub,
        f"Largest Family (% of structure)": f"{largest_pct}%",
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in overview_cards.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>""",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# TAB 2 — MICRO-ANALYSIS AJUSTADO
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    family_selected = st.selectbox("Select a Job Family:", families)
    family_df = df[df[COL_FAMILY] == family_selected]

    # Cards
    metrics = {
        "Subfamilies": family_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": family_df[COL_PROFILE].nunique(),
        "Career Paths": family_df[COL_CAREER_PATH].nunique(),
        "Career Bands": family_df[COL_BAND].nunique(),
        "Global Grades": family_df[COL_GRADE].nunique(),
        "Career Levels": family_df[COL_LEVEL].nunique(),
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in metrics.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>""",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Distribution of Job Profiles by Subfamily")

    sub_dist = (
        family_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colA, colB = st.columns([1,1])

    with colA:
        donut = alt.Chart(sub_dist).mark_arc(
            innerRadius=70, outerRadius=130
        ).encode(
            theta="Count:Q",
            color=alt.Color(COL_SUBFAMILY, scale=alt.Scale(range=SIG_PALETTE), legend=None),
            tooltip=[COL_SUBFAMILY, "Count"]
        )
        st.altair_chart(donut, use_container_width=False)

    with colB:
        for i, row in sub_dist.iterrows():
            color = SIG_PALETTE[i % len(SIG_PALETTE)]
            st.markdown(
                f"""
                <div class='sig-icon-wrapper'>
                    <div style="width:14px; height:14px; border-radius:50%; background:{color};"></div>
                    <div style="font-weight:600;">{row[COL_SUBFAMILY]}</div>
                    <div style="margin-left:auto; padding:2px 10px; border-radius:10px; background:{color}; color:white; font-weight:600;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
