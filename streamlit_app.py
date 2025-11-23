import streamlit as st
from utils import aplicar_estilos_inbezt
from PIL import Image

st.set_page_config(
    page_title="inBezt - Inversión Ganadera",
    page_icon="🐮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
    section[data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

if 'usuario' not in st.session_state:
    st.session_state.usuario = None

if 'page' not in st.session_state:
    st.session_state.page = None

if st.session_state.usuario is not None:
    if st.session_state.usuario['rol'] == 'admin':
        st.session_state.page = "admin"
    else:
        st.session_state.page = "dashboard"

if st.session_state.page == "login":
    exec(open("pages/Login.py").read())
elif st.session_state.page == "registro":
    exec(open("pages/Registro.py").read())
elif st.session_state.page == "dashboard":
    exec(open("pages/Dashboard_Cliente.py").read())
elif st.session_state.page == "admin":
    exec(open("pages/Panel_Admin.py").read())
else:
    try:
        logo = Image.open("assets/logo.jpeg")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, use_container_width=True)
    except:
        pass
    
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0 3rem 0; background: linear-gradient(135deg, #f3f0ff 0%, #e0f2fe 50%, #fce7f3 100%); 
                    border-radius: 20px; margin-bottom: 2rem;">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem; color: #333;">Bienvenido a inBezt</h2>
            <p style="font-size: 1.3rem; color: #555; max-width: 800px; margin: 0 auto; line-height: 1.6;">
                La forma más <strong>segura</strong> y <strong>rentable</strong> de invertir en el sector ganadero colombiano
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="card" style="background: white; box-shadow: 0 8px 16px rgba(0,0,0,0.1);">
                <h3 style="color: #9b87f5; font-size: 1.8rem;">💎 ¿Por qué invertir con inBezt?</h3>
                <ul style="font-size: 1.2rem; line-height: 2.2; color: #333;">
                    <li>✅ Rentabilidad desde <strong style="color: #9b87f5;">1.5% mensual</strong></li>
                    <li>✅ Inversión mínima de <strong style="color: #7dd3fc;">$2.000.000 COP</strong></li>
                    <li>✅ Contratos digitales <strong>seguros</strong></li>
                    <li>✅ <strong>Transparencia total</strong> en tu inversión</li>
                    <li>✅ Respaldo en el <strong>sector ganadero</strong></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 ¿Ya tienes cuenta?", use_container_width=True, type="primary", key="btn_login_main"):
                st.session_state.page = "login"
                st.rerun()
        
        with col_b:
            if st.button("📝 ¿Eres nuevo?", use_container_width=True, key="btn_registro_main"):
                st.session_state.page = "registro"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style="background: linear-gradient(135deg, #9b87f5 0%, #f472b6 100%); padding: 2rem; 
                        border-radius: 15px; text-align: center; color: white; margin-top: 2rem;">
                <h3 style="margin: 0 0 1rem 0;">🚀 Comienza hoy mismo</h3>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.95;">
                    Regístrate en menos de 2 minutos y empieza a hacer crecer tu capital con respaldo ganadero
                </p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0; color: #999; border-top: 1px solid #eee;">
        <p>© 2024 inBezt - Inversión Ganadera | Todos los derechos reservados</p>
    </div>
""", unsafe_allow_html=True)
