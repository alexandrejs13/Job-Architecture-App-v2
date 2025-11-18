import streamlit as st
import pandas as pd
import html
from streamlit.components.v1 import html as components_html

# ---------------------------------------------------
# LOAD DATA SAFELY
# ---------------------------------------------------
@st.cache_data
def load_profiles():
    # Caminho confirmado pelo usuário
    df = pd.read_excel("data/Job Profile.xlsx")
    return df

df = load_profiles()

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.title("Job Profile Description Explorer")

# ---------------------------------------------------
# SIMPLE SELECTOR
# ---------------------------------------------------
options = df["Job Profile"].unique().tolist()
selected = st.multiselect("Select profiles to compare", options, max_selections=3)

if len(selected) == 0:
    st.info("Selecione até 3 perfis acima.")
    st.stop()

profiles = df[df["Job Profile"].isin(selected)].to_dict(orient="records")

# ---------------------------------------------------
# BUILD HTML
# ---------------------------------------------------
def build_html(profiles):
    n = len(profiles)

    html_code = f"""
    <html>
    <head>
    <style>

    html, body {{
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', sans-serif;
        overflow: auto;  /* CORREÇÃO FUNDAMENTAL */
    }}

    #layout {{
        display: flex;
        flex-direction: column;
        height: 100vh;
    }}

    /* TOP FIXED CARDS */
    #top-block {{
        position: sticky;
        top: 0;
        z-index: 9999;
        background: white;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }}

    .grid-top {{
        display: grid;
        grid-template-columns: repeat({n}, 1fr);
        gap: 20px;
    }}

    .card-top {{
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
    }}

    .job {{
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 6px;
    }}

    .gg {{
        color: #145efc;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    /* SCROLLABLE DESCRIPTION AREA */
    #scroll-block {{
        flex: 1;
        overflow-y: auto;
        padding: 24px;
    }}

    .grid-desc {{
        display: grid;
        grid-template-columns: repeat({n}, 1fr);
        gap: 20px;
    }}

    .card-desc {{
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.10);
        font-size: 16px;
    }}

    </style>
    </head>

    <body>

    <div id="layout">

        <!-- FIXED TOP GRID -->
        <div id="top-block">
            <div class="grid-top">
    """

    # TOP CARDS
    for p in profiles:
        job = html.escape(str(p.get("Job Profile", "")))
        gg = html.escape(str(p.get("Global Grade", "")))
        jf = html.escape(str(p.get("Job Family", "")))
        sf = html.escape(str(p.get("Sub Job Family", "")))
        cp = html.escape(str(p.get("Career Path", "")))
        fc = html.escape(str(p.get("Full Job Code", "")))

        html_code += f"""
            <div class="card-top">
                <div class="job">{job}</div>
                <div class="gg">GG {gg}</div>
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        """

    html_code += """
            </div>
        </div>

        <!-- SCROLLABLE DESCRIPTION GRID -->
        <div id="scroll-block">
            <div class="grid-desc">
    """

    # DESCRIPTION CARDS
    for p in profiles:
        html_code += f"""
        <div class="card-desc">
            <b>Description for:</b><br>
            {html.escape(p.get("Job Profile", ""))}<br><br>
            Aqui entra o conteúdo completo depois.
        </div>
        """

    html_code += """
            </div>
        </div>

    </div>

    </body>
    </html>
    """

    return html_code


# ---------------------------------------------------
# RENDER HTML
# ---------------------------------------------------
final_html = build_html(profiles)
components_html(final_html, height=900)
