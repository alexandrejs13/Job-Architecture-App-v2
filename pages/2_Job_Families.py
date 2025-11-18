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
# HEADER — mesmo padrão visual das outras páginas
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
# TEXTO PRINCIPAL — explicação estilo WTW (sem citar WTW)
# ==========================================================
st.markdown("""
### What Job Families Represent in a Job Architecture

**Job Families** are the structural backbone that groups roles based on similar nature of work, core capabilities, and functional purpose.  
They ensure that jobs performing comparable activities are evaluated within a consistent and coherent framework.

A well-designed family structure:

- increases internal consistency  
- improves transparency in how roles relate to one another  
- organizes the organization’s capabilities into meaningful clusters  
- enables more accurate leveling decisions  
- supports fair compensation alignment  
- clarifies how work evolves within each discipline  

---

### The Role of Job Families in the Architecture

Each Job Family is built around a **shared functional domain**, such as Finance, Engineering, HR, Operations, Commercial, or Technology.  
Inside each family, **Job Subfamilies** capture more specific expertise areas — for example, within HR: Payroll, Talent Acquisition, Total Rewards, and HRBP.

This layered structure helps organizations define:

- **Career Path progression** within each specialty  
- **Skill expectations** by level and by discipline  
- **Functional depth versus business breadth**  
- **Common capabilities** required across similar jobs  

When combined with Job Levels and Job Profiles, Job Families create a clear, navigable career structure.

---

### How Job Families and Subfamilies Work Together

- **Job Family** = high-level discipline  
- **Job Subfamily** = specialized functional track inside the family  
- **Job Profile** = specific role definition  
- **Job Level** = organizational impact and complexity  

This hierarchy ensures that jobs can be compared fairly without being constrained by inconsistent job titles or local naming practices.

---
""")

# ==========================================================
# CARREGAR ARQUIVO Job Family.xlsx
# ==========================================================
file_path = "data/Job Family.xlsx"

if not os.path.exists(file_path):
    st.error("Arquivo **'Job Family.xlsx'** não encontrado na pasta `data/`.")
    st.stop()

df = pd.read_excel(file_path)

# Normaliza nomes de colunas para evitar erros
df.columns = [str(c).strip() for c in df.columns]

# Espera-se colunas: Job Family | Job Subfamily
if not {"Job Family", "Job Subfamily"}.issubset(df.columns):
    st.error("O arquivo deve conter as colunas: **Job Family** e **Job Subfamily**.")
    st.stop()

# ==========================================================
# PICK LIST — seletores de Family → Subfamily
# ==========================================================
st.markdown("### Explore Job Families and Subfamilies")

families = sorted(df["Job Family"].dropna().unique().tolist())
selected_family = st.selectbox("Select a Job Family:", families)

filtered_subfamilies = df[df["Job Family"] == selected_family]["Job Subfamily"].dropna().unique().tolist()
filtered_subfamilies = sorted(filtered_subfamilies)

selected_subfamily = st.selectbox("Select a Job Subfamily:", filtered_subfamilies)

st.markdown("---")

# ==========================================================
# TABELA FILTRADA OU COMPLETA
# ==========================================================
st.markdown("### Job Family & Subfamily Table")

df_display = df[
    (df["Job Family"] == selected_family) &
    (df["Job Subfamily"] == selected_subfamily)
]

st.dataframe(df_display, use_container_width=True)

# ==========================================================
# RODAPÉ
# ==========================================================
st.caption("Navigate to other sections to explore Job Profiles, Job Levels and Job Match.")
