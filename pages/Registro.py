import streamlit as st
from database import crear_usuario
from utils import aplicar_estilos_inbezt
import re

st.set_page_config(page_title="Registro - inBezt", page_icon="📝", layout="centered")
st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-inbezt">
        <h1>📝 Registro de Usuario</h1>
        <p>Únete a inBezt y comienza a invertir</p>
    </div>
""", unsafe_allow_html=True)

# Si ya está autenticado
if st.session_state.get('usuario') is not None:
    st.info("✅ Ya tienes una sesión activa")
    st.stop()

def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def validar_cedula(cedula):
    return cedula.isdigit() and len(cedula) >= 6

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 10

# Formulario de registro
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("registro_form"):
        st.markdown("### Información Personal")
        
        nombre = st.text_input(
            "👤 Nombre Completo *",
            placeholder="Juan Pérez García"
        )
        
        cedula = st.text_input(
            "🆔 Cédula *",
            placeholder="1234567890",
            max_chars=15
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            telefono = st.text_input(
                "📱 Teléfono *",
                placeholder="3001234567",
                max_chars=10
            )
        with col_b:
            ciudad = st.text_input(
                "🏙️ Ciudad *",
                placeholder="Bogotá"
            )
        
        email = st.text_input(
            "📧 Email *",
            placeholder="tu@email.com"
        )
        
        negocio = st.text_input(
            "🏢 Negocio/Empresa (opcional)",
            placeholder="Mi Empresa SAS"
        )
        
        st.markdown("### Seguridad")
        
        contrasena = st.text_input(
            "🔒 Contraseña *",
            type="password",
            placeholder="Mínimo 6 caracteres"
        )
        
        confirmar = st.text_input(
            "🔒 Confirmar Contraseña *",
            type="password",
            placeholder="Repite tu contraseña"
        )
        
        st.markdown("---")
        acepto = st.checkbox("Acepto los términos y condiciones de inBezt")
        
        submit = st.form_submit_button("✅ Crear Cuenta", use_container_width=True)
        
        if submit:
            # Validaciones
            errores = []
            
            if not all([nombre, cedula, telefono, email, ciudad, contrasena, confirmar]):
                errores.append("⚠️ Todos los campos marcados con * son obligatorios")
            
            if not validar_cedula(cedula):
                errores.append("⚠️ La cédula debe contener solo números (mínimo 6 dígitos)")
            
            if not validar_telefono(telefono):
                errores.append("⚠️ El teléfono debe tener 10 dígitos")
            
            if not validar_email(email):
                errores.append("⚠️ Email no válido")
            
            if len(contrasena) < 6:
                errores.append("⚠️ La contraseña debe tener al menos 6 caracteres")
            
            if contrasena != confirmar:
                errores.append("⚠️ Las contraseñas no coinciden")
            
            if not acepto:
                errores.append("⚠️ Debes aceptar los términos y condiciones")
            
            if errores:
                for error in errores:
                    st.error(error)
            else:
                with st.spinner("Creando tu cuenta..."):
                    exito, mensaje = crear_usuario(
                        nombre, cedula, telefono, email, ciudad, contrasena, negocio
                    )
                    
                    if exito:
                        st.success("🎉 " + mensaje)
                        st.balloons()
                        st.info("👉 Ahora puedes iniciar sesión en la página de **Login**")
                        st.session_state.registro_exitoso = True
                    else:
                        st.error("❌ " + mensaje)
    
    st.markdown("---")
    st.info("💡 **¿Ya tienes cuenta?** Ve a la página de **Login** en el menú lateral")