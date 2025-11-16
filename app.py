
import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

# Center container
st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)

st.markdown("""
<div style='background-color:#f2efeb; border-radius:25px; padding:0; max-width:900px; width:100%;'>
    <img src='assets/home/home_card.jpg'
         style='width:100%; border-top-left-radius:25px; border-top-right-radius:25px;'>
    <div style='padding:30px; text-align:left;'>
        <h2 style='font-family:PPSIGFlow, sans-serif;'>Job Architecture</h2>
        <p style='font-size:18px; line-height:1.5;'>
        Uma base única de descrições de cargos genéricas que serve como referência global para classificar,
        harmonizar e padronizar todos os cargos da empresa. Aqui, você encontra títulos consistentes,
        níveis claros e perfis alinhados internacionalmente — tudo pensado para que o gestor escolha apenas
        o cargo local correto enquanto o sistema cuida do restante. Mais simplicidade no dia a dia,
        menos dúvidas e uma estrutura organizacional totalmente integrada.
        </p>
        <p style='color:#145efc; font-size:18px; font-weight:600;'>Job Architecture →</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
