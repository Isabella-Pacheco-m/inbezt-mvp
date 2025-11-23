import streamlit as st
from database import login_usuario
from utils import aplicar_estilos_inbezt

st.set_page_config(page_title="Login - inBezt", page_icon="🔐", layout="centered")
st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-inbezt">
        <h1>🔐 Iniciar Sesión</h1>
    </div>
""", unsafe_allow_html=True)

# Si ya está autenticado, redirigir
if st.session_state.get('usuario') is not None:
    st.success("✅ Ya has iniciado sesión")
    st.info("👈 Ve al menú para acceder a tu dashboard")
    
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.usuario = None
        st.rerun()
    st.stop()

# Formulario de login
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("login_form"):
        st.markdown("### Ingresa tus credenciales")
        
        email = st.text_input(
            "📧 Email",
            placeholder="tu@email.com"
        )
        
        contrasena = st.text_input(
            "🔑 Contraseña",
            type="password",
            placeholder="Tu contraseña"
        )
        
        submit = st.form_submit_button("Ingresar", use_container_width=True)
        
        if submit:
            if not email or not contrasena:
                st.error("⚠️ Por favor completa todos los campos")
            else:
                with st.spinner("Verificando credenciales..."):
                    usuario, mensaje = login_usuario(email, contrasena)
                    
                    if usuario:
                        st.session_state.usuario = usuario
                        st.success(f"✅ {mensaje}")
                        st.balloons()
                        st.info("🔄 Redirigiendo...")
                        st.rerun()
                    else:
                        st.error(f"❌ {mensaje}")
    
    st.markdown("---")
    st.info("💡 **¿No tienes cuenta?** Ve a la página de **Registro** en el menú lateral")
    
    # Credenciales de prueba (puedes quitar esto en producción)
    with st.expander("🔍 Ver credenciales de administrador"):
        st.code("""
Email: inbezt@gmail.com
Contraseña: inBeztAdmin1957-
        """)