# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Structure Level", layout="wide")


# ==========================================================
# HEADER PADRÃO DO APP NOVO
# ==========================================================
import base64

def load_icon_png(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_b64 = load_icon_png("assets/icons/process.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Structure Level
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
# SEÇÃO DE TEXTO — IDENTIDADE NOVA + SEU TEXTO
# ==========================================================
st.markdown("""
### What “Structure Level” Means in an Organizational Career Architecture

A **Structure Level** is the standardized layer that organizes all roles in the company into a clear, comparable hierarchy.  
Instead of relying on job titles — which can vary across teams and countries — the Structure Level defines the *real substance* of a role:  
its scope, decision-making responsibility, complexity, and expected contribution to the organization.

It acts as a backbone for the entire career framework, ensuring that every job connects coherently to:

- the global grade  
- the career path  
- the career band  
- the career level  

---

### How It Works in Practice

The Structure Level translates each role into a consistent **organizational slot**.

Using your table as reference:

- **Grades 21–17 → Executive Leadership**  
  Strategic direction, broad impact, enterprise-level accountability.

- **Grades 16–12 → People Managers**  
  Leading teams, performance management, driving execution.

- **Grades 16–10 → Professional Path**  
  Deep functional or technical expertise with significant autonomy and influence.

- **Grades 9–5 → Specialists & Analysts**  
  Core functional delivery, increasing independence and technical depth.

- **Project Roles**  
  Follow the same progression (Coordinator → Manager → Program Manager), mapped to the same structural backbone.

Each level builds logically on the previous one, showing a progression of capability, scope, and contribution.

---

### Why Structure Levels Matter

#### **Consistency Across the Organization**
Every job — whether in Management, Professional, or Projects — is mapped to the same hierarchy, making comparisons fair and transparent.

#### **Clear Career Paths**
Employees understand how to progress not only by title but by capability and responsibility.

#### **Compensation Alignment**
Each Structure Level reflects a degree of complexity and impact, simplifying governance of compensation philosophy.

#### **Eliminates Title Inflation**
Anchors the *real* size of the role, regardless of naming differences across regions or functions.

#### **Enables Mobility & Workforce Planning**
With all roles aligned to the same structure, mobility and comparisons across teams, countries and functions become easier and more precise.

---

### How the Levels Reflect Real Organizational Progression

**Management Path**
- 21–17 → Enterprise leadership  
- 16–12 → People managers

**Professional Path**
- 16–14 → Lead Experts / Senior Experts  
- 13–11 → Experts  
- 10–7 → Specialists / Senior Specialists  
- 6–5  → Assistants / Analysts  

**Projects Path**
- Same structural backbone, mapped to scope and responsibility of project leadership.

---

The **Structure Level** unifies all these paths into a single, coherent organizational map.
""")


# ==========================================================
# CARREGAMENTO DO ARQUIVO (MANTIDO DO JEITO CERTO)
# ==========================================================
data = load_excel_data()
df = data.get("level_structure", pd.DataFrame())

if df.empty:
    st.error(
        "Arquivo **'Level Structure.xlsx'** não encontrado na pasta `data/` "
        "ou o arquivo está vazio."
    )
    st.stop()


# ==========================================================
# TABELA — MANTER COMO ESTÁ NO APP NOVO
# ==========================================================
st.markdown("### Structure Level Table")

st.dataframe(df, use_container_width=True)


# ==========================================================
# RODAPÉ
# ==========================================================
st.caption("Continue navegando para acessar Job Maps e Job Match.")
