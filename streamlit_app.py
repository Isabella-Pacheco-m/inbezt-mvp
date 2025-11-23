import streamlit as st
from utils import aplicar_estilos_inbezt
from PIL import Image

COLORS = {
    'purple': '#9b87f5',
    'blue': '#7dd3fc',
    'pink': '#f472b6',
    'light_purple': '#f3f0ff',
    'light_blue': '#e0f2fe',
    'light_pink': '#fce7f3'
}

st.set_page_config(
    page_title="inBezt - Inversión Ganadera",
    page_icon="🐮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none }
section[data-testid="stSidebar"] { display: none }
body { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-weight: 700; }
.card {
    background: white;
    padding: 2.2rem;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}
.btn-main {
    background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 100%);
    padding: 0.9rem 0;
    font-size: 1.15rem;
    border-radius: 12px;
    color: white;
    width: 100%;
    border: none;
}
.btn-secondary {
    background: white;
    padding: 0.9rem 0;
    font-size: 1.15rem;
    border-radius: 12px;
    color: #333;
    border: 2px solid #9b87f5;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

if 'usuario' not in st.session_state:
    st.session_state.usuario = None

if 'page' not in st.session_state:
    st.session_state.page = None

if st.session_state.usuario is not None and st.session_state.page is None:
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
    
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 3rem 1rem 3.5rem 1rem;
            background: linear-gradient(135deg, {COLORS['light_purple']} 0%, {COLORS['light_blue']} 50%, {COLORS['light_pink']} 100%);
            border-radius: 25px;
            margin-bottom: 2.5rem;
        ">
            <h2 style="font-size: 2.7rem; margin-bottom: 1rem; color: #222;">
                Bienvenido a inBezt
            </h2>
            <p style="font-size: 1.35rem; max-width: 850px; margin: 0 auto; line-height: 1.7; color: #444;">
                La forma más <strong>segura</strong> y <strong>rentable</strong> de invertir en el sector ganadero colombiano
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div class="card">
                <h3 style="color: {COLORS['purple']}; font-size: 1.8rem; margin-bottom: 1rem;">
                    💎 ¿Por qué invertir con inBezt?
                </h3>
                <ul style="font-size: 1.2rem; line-height: 2.2; color: #333; padding-left: 1rem;">
                    <li>Rentabilidad desde <strong style="color: {COLORS['purple']};">1.5% mensual</strong></li>
                    <li>Inversión mínima de <strong style="color: {COLORS['blue']};">$2.000.000 COP</strong></li>
                    <li>Contratos digitales seguros</li>
                    <li>Transparencia total en tu inversión</li>
                    <li>Respaldo en el sector ganadero</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Iniciar Sesión", use_container_width=True, key="btn_login_main"):
                st.session_state.page = "login"
                st.rerun()
        
        with col_b:
            if st.button("📝 Crear Cuenta", use_container_width=True, key="btn_registro_main"):
                st.session_state.page = "registro"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {COLORS['purple']} 0%, {COLORS['pink']} 100%);
                padding: 2.2rem;
                border-radius: 18px;
                text-align: center;
                color: white;
                margin-top: 2.5rem;
            ">
                <h3 style="margin: 0 0 1rem 0; font-size: 1.7rem;">🚀 Comienza hoy mismo</h3>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.95;">
                    Regístrate en menos de 2 minutos y empieza a hacer crecer tu capital con respaldo ganadero
                </p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #999;
        border-top: 1px solid #eee;
        font-size: 0.9rem;
    ">
        © 2024 inBezt - Inversión Ganadera | Todos los derechos reservados
    </div>
""", unsafe_allow_html=True)
