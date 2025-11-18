import streamlit as st
import base64
import os
import pandas as pd

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Families", layout="wide")

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG INLINE
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""  
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER (padronizado)
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
# TEXTO EXPLICATIVO (metodologia — inglês)
# ==========================================================
st.markdown("""
### What Job Families Represent in a Job Architecture

**Job Families** group roles based on the nature of work, shared capabilities, and functional purpose.  
They provide structure, alignment, and clarity across the organization, ensuring that similar work is evaluated consistently.

A robust Job Family framework:

- organizes work into meaningful capability clusters  
- supports fair leveling decisions  
- enables consistent career pathing  
- clarifies functional expectations  
- improves internal comparability and transparency  

---

### The Relationship Between Families and Subfamilies

- **Job Family** → the broad functional domain  
- **Sub Job Family** → the specialized track inside that domain  
- **Profile** → the specific role performed  
- **Description** → explains scope, purpose, and responsibilities  

This hierarchy ensures organizational consistency, regardless of naming differences across teams or countries.

---
""")


# ==========================================================
# CARREGAR ARQUIVO — **COM NOMES REAIS**
# ==========================================================
file_path = "data/Job Family.xlsx"

if not os.path.exists(file_path):
    st.error("Arquivo **'Job Family.xlsx'** não encontrado na pasta `data/`.")
    st.stop()

df = pd.read_excel(file_path)

# Normaliza nomes de colunas
df.columns = [str(c).strip() for c in df.columns]

# Verifica colunas REAIS
required_cols = {"Job Family", "Sub Job Family"}

if not required_cols.issubset(df.columns):
    st.error(
        f"O arquivo deve conter as colunas exatas: **{', '.join(required_cols)}**.\n\n"
        f"Colunas encontradas: {', '.join(df.columns)}"
    )
    st.stop()


# ==========================================================
# PICK-LIST dinâmico
# ==========================================================
st.markdown("### Explore Job Families and Subfamilies")

families = sorted(df["Job Family"].dropna().unique())
selected_family = st.selectbox("Select a Job Family:", families)

subfamilies = df[df["Job Family"] == selected_family]["Sub Job Family"].dropna().unique()
subfamilies = sorted(subfamilies)

selected_subfamily = st.selectbox("Select a Sub Job Family:", subfamilies)

# Filtrar tabela
df_filtered = df[
    (df["Job Family"] == selected_family) &
    (df["Sub Job Family"] == selected_subfamily)
]

st.markdown("---")

# ==========================================================
# TABELA RESULTANTE
# ==========================================================
st.markdown("### Job Family & Subfamily Detail")

st.dataframe(df_filtered, use_container_width=True)


# ==========================================================
# RODAPÉ
# ==========================================================
st.caption("Navigate to other modules to explore Job Profiles, Structure Levels and Job Match.")
