import streamlit as st
from database import login_usuario
from utils import aplicar_estilos_inbezt
from PIL import Image

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

try:
    logo = Image.open("assets/logo.jpeg")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, width=200)
except:
    pass

st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            Iniciar Sesión
        </h1>
    </div>
""", unsafe_allow_html=True)

if st.session_state.get('usuario') is not None:
    st.success("✅ Ya has iniciado sesión")
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.usuario = None
        st.session_state.page = None
        st.rerun()
    st.stop()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("login_form"):
        st.markdown("### Ingresa tus credenciales")
        
        email = st.text_input("📧 Email", placeholder="tu@email.com")
        contrasena = st.text_input("🔒 Contraseña", type="password", placeholder="Tu contraseña")
        
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
                        if usuario['rol'] == 'admin':
                            st.session_state.page = "admin"
                        else:
                            st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(f"❌ {mensaje}")
    
    st.markdown("---")
    
    if st.button("📝 ¿No tienes cuenta? Regístrate", use_container_width=True):
        st.session_state.page = "registro"
        st.rerun()
    
    if st.button("🏠 Volver al inicio", use_container_width=True):
        st.session_state.page = None
        st.rerun()
    
    with st.expander("🔍 Ver credenciales de administrador"):
        st.code("Email: inbezt@gmail.com\nContraseña: inBeztAdmin1957-")