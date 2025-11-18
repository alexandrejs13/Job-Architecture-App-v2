# ==========================================================
# HEADER — versão centralizada
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin-top:60px;
    margin-bottom:20px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:200px; height:200px; margin-bottom:24px;">
    
    <h1 style="
        font-size:44px;
        font-weight:700;
        margin:0;
        padding:0;
        text-align:center;
    ">
        Job Architecture
    </h1>
</div>
""", unsafe_allow_html=True)
