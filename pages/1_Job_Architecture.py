import streamlit as st
import base64
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# LOAD ICON
# ==========================================================
def load_icon_png(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_b64 = load_icon_png("assets/icons/governance.png")

# ==========================================================
# HEADER — EXACTLY SAME VISUAL STANDARD
# ==========================================================
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Architecture
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
# MAIN TEXT — HIGHLY DETAILED, METHODOLOGICAL, IN ENGLISH
# ==========================================================
st.markdown("""
### What Job Architecture Really Is

**Job Architecture** is the structural framework that defines how every role in an organization fits together.  
It shapes how jobs are grouped, compared, evaluated, and aligned across different functions, countries, and career paths.

Rather than relying on job titles — which often vary or lose meaning over time — Job Architecture focuses on:

- **organizational impact**  
- **complexity of decisions**  
- **knowledge required**  
- **scope of influence**  
- **problem-solving autonomy**  
- **expected contribution to business results**

It is the foundation that links jobs to levels, grades, families, compensation, and career development.

---

### Why Organizations Use Job Architecture

Companies adopt a Job Architecture because it:

- creates **logical, repeatable criteria** for evaluating roles  
- eliminates inconsistencies caused by local titles  
- enables a **transparent and fair career structure**  
- supports global mobility and internal movement  
- aligns compensation to the *real size* of the job, not to the title  
- strengthens governance over hiring, promotion, and organizational design  
- clarifies expectations at each level and career stage  

A well-designed architecture ensures that similar roles are treated similarly, regardless of geography or team.

---

### Core Components of Job Architecture

A complete architecture is built on several interconnected components:

#### **1. Job Families**
Clusters of work with similar purpose or discipline.  
Examples: Finance, Engineering, HR, Technology, Commercial, Operations.

#### **2. Job Subfamilies**
More specific concentrations of expertise within a job family.  
Examples: Payroll, Software Engineering, Supply Chain, Total Rewards.

#### **3. Job Levels**
A standardized hierarchy defining progression of responsibility, decision-making, and scope.  
Each level describes how the role contributes to the organization.

#### **4. Job Profiles**
Clear definitions of what each role *does*, including:  
responsibilities, required skills, knowledge, complexity, autonomy, and typical outcomes.

#### **5. Career Path**
Pathways that reflect how careers grow:
- Management  
- Professional / Expert  
- Project or Program Leadership  
- Operations / Technical Tracks  

These paths align roles with different forms of impact — whether through expertise, leadership, or execution.

---

### How Jobs Are Evaluated and Positioned

Job Architecture relies on structured analysis to place each role in the correct level.  
This evaluation considers:

- **impact on business outcomes**  
- **breadth of influence** (team, department, enterprise)  
- **complexity of decisions**  
- **nature of problems solved**  
- **technical depth and conceptual thinking**  
- **autonomy versus guidance required**  
- **stakeholder management and communication demands**  

The result is a consistent map: each job is positioned based on its *real* contribution and complexity, not on historical naming or local preference.

---

### Why Job Architecture Is a Strategic Tool

#### **Talent Management**
Employees clearly understand what progression looks like and what skills or behaviors differentiate each level.

#### **Internal Equity**
Roles with similar complexity sit at similar levels, avoiding favoritism or inflation.

#### **Global Standardization**
Different regions and functions follow the same framework, reducing fragmentation.

#### **Compensation Governance**
Grades, pay ranges, and reward programs align organically with the architecture.

#### **Organizational Design**
Leaders gain visibility over overlaps, gaps, layering problems, and inconsistencies across teams.

---

### The Value It Creates

In practice, a solid Job Architecture enables:

- **predictable career growth**  
- **fairness in promotions**  
- **stronger hiring discipline**  
- **competitive and consistent pay practices**  
- **better workforce planning**  
- **clear communication of expectations**  

It becomes a living system that connects talent, performance, structure, and rewards.

---

Job Architecture is not just a catalog of jobs;  
it is the **operating system** that organizes how the company understands work, evaluates roles, and enables people to grow.
""")
