import streamlit as st
import base64
import os
import pandas as pd

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Families", layout="wide")

# ==========================================================
# FUNÇÃO PNG
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER SIG
# ==========================================================
icon_path = "assets/icons/people_employees.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Families
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# GLOBAL LAYOUT — limita largura e impede esticar infinito
# ==========================================================
st.markdown("""
<style>

    /* Container principal do Streamlit */
    .main > div {
        max-width: 1400px;    /* limite máximo elegante */
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* Estilo para dataframes */
    .stDataFrame {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Estilo para cards / container padrão */
    .block-container, .stColumn {
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# CONTAINER CENTRAL PARA EVITAR PÁGINA INFINITA
# ==========================================================
container_style = """
<style>
.sig-container {
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
}
</style>
"""
st.markdown(container_style, unsafe_allow_html=True)


# ==========================================================
# ABRE CONTAINER
# ==========================================================
st.markdown('<div class="sig-container">', unsafe_allow_html=True)


# ==========================================================
# TEXTO PRINCIPAL
# ==========================================================
st.markdown("""
### What Job Families Represent in a Job Architecture

**Job Families** group roles based on similar nature of work, core capabilities, and functional purpose.  
They establish structure, clarity, and transparency inside the organization.

A robust Job Family framework:

- organizes work into meaningful capability clusters  
- supports fair and consistent leveling decisions  
- clarifies career path options  
- ensures functional comparability across teams and regions  
- strengthens compensation alignment  

---

### Families, Subfamilies, Profiles and Description

- **Job Family** → broad discipline  
- **Sub Job Family** → specialization within the discipline  
- **Profile** → defined role inside a subfamily  
- **Description** → purpose, scope, influence, and functional expectations  
""")

# ==========================================================
# LOAD ARQUIVO
# ==========================================================
file_path = "data/Job Family.xlsx"

if not os.path.exists(file_path):
    st.error("Arquivo **'Job Family.xlsx'** não encontrado na pasta `data/`.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = [str(c).strip() for c in df.columns]

required_cols = {"Job Family", "Sub Job Family"}

if not required_cols.issubset(df.columns):
    st.error(
        "O arquivo deve conter as colunas exatas: Job Family e Sub Job Family."
    )
    st.stop()

# ==========================================================
# PICKLIST
# ==========================================================
st.markdown("### Explore Job Families and Subfamilies")

families = sorted(df["Job Family"].dropna().unique())
selected_family = st.selectbox("Select a Job Family:", families)

subfamilies = sorted(
    df[df["Job Family"] == selected_family]["Sub Job Family"]
    .dropna()
    .unique()
)

selected_subfamily = st.selectbox("Select a Sub Job Family:", subfamilies)

df_filtered = df[
    (df["Job Family"] == selected_family) &
    (df["Sub Job Family"] == selected_subfamily)
]

st.markdown("---")

# ==========================================================
# TABELA
# ==========================================================
st.markdown("### Job Family & Subfamily Detail")

st.dataframe(df_filtered, use_container_width=True)

# ==========================================================
# FECHA CONTAINER
# ==========================================================
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# RODAPÉ
# ==========================================================
st.caption("Navigate to Job Profiles, Structure Levels and Job Match.")
