import streamlit as st
from utils import aplicar_estilos_inbezt
from PIL import Image

st.set_page_config(
    page_title="inBezt - Inversión Ganadera",
    page_icon="🐮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f3f0ff 0%, #e0f2fe 50%, #fce7f3 100%);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

if 'usuario' not in st.session_state:
    st.session_state.usuario = None

with st.sidebar:
    try:
        logo = Image.open("assets/logo.jpeg")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("### 🐮 inBezt")
    
    st.markdown("---")
    st.markdown("### 📍 Navegación")
    
    if st.session_state.usuario is None:
        if st.button("🔐 Iniciar Sesión", use_container_width=True, key="btn_login_sidebar"):
            st.session_state.page = "login"
            st.rerun()
        if st.button("📝 Registrarse", use_container_width=True, key="btn_registro_sidebar"):
            st.session_state.page = "registro"
            st.rerun()
    else:
        usuario = st.session_state.usuario
        if usuario['rol'] == 'cliente':
            if st.button("💰 Mi Dashboard", use_container_width=True, type="primary", key="btn_dashboard_sidebar"):
                st.session_state.page = "dashboard"
                st.rerun()
        elif usuario['rol'] == 'admin':
            if st.button("⚙️ Panel Admin", use_container_width=True, type="primary", key="btn_admin_sidebar"):
                st.session_state.page = "admin"
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True, key="btn_logout_sidebar"):
            st.session_state.usuario = None
            st.session_state.page = None
            st.rerun()

if 'page' not in st.session_state:
    st.session_state.page = None

if st.session_state.page == "login":
    import sys
    sys.path.insert(0, 'pages')
    from Login import main as login_main
    login_main()
elif st.session_state.page == "registro":
    import sys
    sys.path.insert(0, 'pages')
    from Registro import main as registro_main
    registro_main()
elif st.session_state.page == "dashboard":
    import sys
    sys.path.insert(0, 'pages')
    from Dashboard_Cliente import main as dashboard_main
    dashboard_main()
elif st.session_state.page == "admin":
    import sys
    sys.path.insert(0, 'pages')
    from Panel_Admin import main as admin_main
    admin_main()
else:
    if st.session_state.usuario is None:
        try:
            logo = Image.open("assets/logo.jpeg")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo, use_container_width=True)
        except:
            pass
        
        st.markdown("""
            <div style="text-align: center; margin: 2rem 0 3rem 0;">
                <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800;">
                    inBezt
                </h1>
                <p style="font-size: 1.3rem; color: #666; margin: 1rem 0 0 0;">
                    Plataforma de Inversión Ganadera
                </p>
            </div>
        """, unsafe_allow_html=True)
        
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

    else:
        usuario = st.session_state.usuario
        
        col_logo, col_title = st.columns([1, 5])
        
        with col_logo:
            try:
                logo = Image.open("assets/logo.jpeg")
                st.image(logo, width=100)
            except:
                st.markdown("# 🐮")
        
        with col_title:
            st.markdown("""
                <div style="padding: 1rem 0;">
                    <h1 style="margin: 0; background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%); 
                               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                               background-clip: text;">
                        inBezt
                    </h1>
                    <p style="margin: 0; font-size: 1.1rem; color: #666;">
                        Plataforma de Inversión Ganadera
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.success(f"👋 Bienvenido, **{usuario['nombre']}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if usuario['rol'] == 'admin':
                st.markdown("""
                    <div class="card" style="background: linear-gradient(135deg, #f3f0ff 0%, #fce7f3 100%);">
                        <h3>⚙️ Panel de Administración</h3>
                        <p>Gestiona todas las solicitudes de inversión, usuarios y configuración del sistema.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("⚙️ Ir al Panel Admin", use_container_width=True, type="primary", key="btn_admin_main"):
                    st.session_state.page = "admin"
                    st.rerun()
            else:
                st.markdown("""
                    <div class="card" style="background: linear-gradient(135deg, #f3f0ff 0%, #e0f2fe 100%);">
                        <h3>💰 Tu Dashboard</h3>
                        <p>Crea nuevas inversiones y revisa el estado de tu portafolio.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("💰 Ir a Mi Dashboard", use_container_width=True, type="primary", key="btn_dashboard_main"):
                    st.session_state.page = "dashboard"
                    st.rerun()
        
        with col2:
            st.markdown("""
                <div class="card">
                    <h4>📊 Tu Cuenta</h4>
                    <p><strong>Nombre:</strong> {}</p>
                    <p><strong>Email:</strong> {}</p>
                    <p><strong>Rol:</strong> {}</p>
                </div>
            """.format(usuario['nombre'], usuario['email'], usuario['rol'].upper()), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0; color: #999; border-top: 1px solid #eee;">
        <p>© 2024 inBezt - Inversión Ganadera | Todos los derechos reservados</p>
    </div>
""", unsafe_allow_html=True)
