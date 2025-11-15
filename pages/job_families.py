import streamlit as st, base64

def run():
    icon='assets/icons/people_employees.png'
    with open(icon,'rb') as f:
        b64=base64.b64encode(f.read()).decode()
    st.markdown(f"""
<div class='page-header' style='display:flex;align-items:center;gap:18px;margin-top:25px;'>
<img src='data:image/png;base64,{b64}' width='48'/>
<h1 style='font-size:48px;margin:0;'>Job Families</h1>
</div>
""", unsafe_allow_html=True)
    st.write("Conteúdo da página Job Families...")
