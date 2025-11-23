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

body {
    font-family: 'Inter', sans-serif;
}

.landing-container {
    max-width: 950px;
    margin: 0 auto;
}

.card {
    background: white;
    padding: 2.3rem;
    border-radius: 20px;
    height: 100%;
    box-shadow: 0 10px 24px rgba(0,0,0,0.12);
}

.img-card {
    border-radius: 20px;
    height: 100%;
    width: 100%;
    object-fit: cover;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.footer {
    text-align: center;
    padding: 1rem 0 0.5rem 0;
    color: #999;
    font-size: 0.8rem;
    border-top: 1px solid #eee;
    margin-top: 2rem;
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
            st.image(logo, width=200)
    except:
        pass

    st.markdown(f"""
        <div class="landing-container" style="
            background: linear-gradient(135deg, {COLORS['light_purple']} 0%, {COLORS['light_blue']} 50%, {COLORS['light_pink']} 100%);
            padding: 3rem 2rem;
            border-radius: 28px;
            margin: 2rem auto 3rem auto;
            text-align: center;
        ">
            <h2 style="font-size: 2.6rem; margin-bottom: 1rem; color: #222;">
                Bienvenido a inBezt
            </h2>
            <p style="font-size: 1.3rem; max-width: 780px; margin: 0 auto; color: #444; line-height: 1.7;">
                La forma más <strong>segura</strong> y <strong>rentable</strong> de invertir en el sector ganadero colombiano.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='landing-container'>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown(f"""
            <div class="card">
                <h3 style="color: {COLORS['purple']}; font-size: 1.8rem; margin-bottom: 1rem;">
                    💎 ¿Por qué invertir con inBezt?
                </h3>
                <ul style="font-size: 1.15rem; line-height: 2; color: #333; padding-left: 1rem;">
                    <li>Rentabilidad desde <strong style="color: {COLORS['purple']};">1.5% mensual</strong></li>
                    <li>Inversión mínima de <strong style="color: {COLORS['blue']};">$2.000.000 COP</strong></li>
                    <li>Contratos digitales seguros</li>
                    <li>Transparencia total en tu inversión</li>
                    <li>Respaldo en el sector ganadero</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        try:
            ganado = Image.open("assets/ganado.jpg")
            st.image(ganado, use_container_width=True, caption="", output_format="PNG")
        except:
            pass

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn_1, col_btn_2 = st.columns(2)

    with col_btn_1:
        if st.button("🔐 Iniciar Sesión", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    with col_btn_2:
        if st.button("📝 Crear Cuenta", use_container_width=True):
            st.session_state.page = "registro"
            st.rerun()

    st.markdown(f"""
        <div style="
            margin-top: 3rem;
            background: linear-gradient(135deg, {COLORS['purple']} 0%, {COLORS['pink']} 100%);
            padding: 2rem;
            border-radius: 18px;
            text-align: center;
            color: white;
        ">
            <h3 style="margin-bottom: 0.5rem; font-size: 1.6rem;">🚀 Comienza hoy mismo</h3>
            <p style="font-size: 1.05rem; opacity: 0.95;">
                Regístrate en menos de 2 minutos y empieza a hacer crecer tu capital.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        © 2024 inBezt — Inversión Ganadera  
    </div>
""", unsafe_allow_html=True)
