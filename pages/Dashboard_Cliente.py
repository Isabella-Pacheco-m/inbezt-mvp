import streamlit as st
from database import crear_inversion, obtener_inversiones_usuario, obtener_configuracion
from utils import aplicar_estilos_inbezt, calcular_interes_compuesto, formatear_cop
from config import INFO_BANCARIA
from PIL import Image

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

# ---------------------------
# Estilos UI
# ---------------------------
st.markdown("""
<style>

:root {
    --purple: #9b87f5;
    --blue: #7dd3fc;
    --pink: #f472b6;
    --light-purple: #f3f0ff;
    --light-blue: #e0f2fe;
}

.card-ui {
    background: white;
    border-radius: 16px;
    border: 1px solid #eee;
    padding: 1.5rem 1.4rem;
}

.card-gradient {
    border-radius: 16px;
    padding: 1.6rem;
    color: #333;
    background: linear-gradient(135deg, var(--light-purple) 0%, var(--light-blue) 100%);
}

.metric-box {
    background: white;
    border: 1px solid #eee;
    padding: 0.8rem 1rem;
    border-radius: 12px;
}

h2, h3, h4 {
    font-weight: 600;
}

.stTabs [role="tab"] {
    padding: 0.8rem 1.2rem !important;
    border-radius: 10px;
    font-size: 1.05rem;
}

.stTabs [role="tab"][aria-selected="true"] {
    background: var(--purple) !important;
    color: white !important;
}

input, textarea, select {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------
# Validación de sesión
# ---------------------------
if st.session_state.get('usuario') is None:
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página")
    st.stop()

usuario = st.session_state.usuario

if usuario['rol'] != 'cliente':
    st.error("❌ Esta página es solo para clientes")
    st.stop()

# ---------------------------
# HEADER
# ---------------------------
col_logo, col_title, col_logout = st.columns([1, 4, 1])

with col_logo:
    try:
        logo = Image.open("assets/logo.jpeg")
        st.image(logo, width=70)
    except:
        st.markdown("### 🐮")

with col_title:
    st.markdown(f"""
        <div style="padding-top:0.4rem;">
            <h2 style="
                margin:0;
                font-size: 1.9rem;
                background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;">
                Hola, {usuario['nombre']}
            </h2>
            <p style="margin:0; color:#666; font-size: 1rem;">Tu tablero de inversiones</p>
        </div>
    """, unsafe_allow_html=True)

with col_logout:
    st.markdown("<div style='padding-top:0.7rem;'>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.usuario = None
        st.session_state.page = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# TABS
# ---------------------------
tabs = st.tabs(["🧮 Calculadora", "📈 Mis Inversiones"])

# =========================================
# TAB 1 - SIMULADOR
# =========================================
with tabs[0]:

    config = obtener_configuracion()

    if config.get('pausar_solicitudes', False):
        st.error("⏸️ Las solicitudes están pausadas temporalmente")
        st.info("Estamos procesando inversiones actuales. Pronto podrás continuar.")
        st.stop()

    st.markdown("### 🧮 Simulador de Inversión")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='card-ui'>", unsafe_allow_html=True)
        monto = st.number_input("💵 Monto a invertir (COP)", min_value=2000000, value=5000000, step=500000)
        meses = st.number_input("📅 Tiempo (meses)", min_value=1, value=6, step=1)
        tasa = st.number_input("📈 Tasa de interés mensual (%)", value=1.5, step=0.1, disabled=True)

        if st.button("🧮 Calcular Retorno", use_container_width=True, type="primary"):
            monto_final, intereses = calcular_interes_compuesto(monto, tasa, meses)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("### 📊 Resultado")
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Inversión", formatear_cop(monto))

            with col_b:
                st.metric("Intereses", formatear_cop(intereses))

            with col_c:
                st.metric("Retorno Total", formatear_cop(monto_final))

            st.session_state.calculo = {
                'monto': monto,
                'meses': meses,
                'tasa': tasa,
                'monto_final': monto_final,
                'intereses': intereses
            }
        else:
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card-gradient'>", unsafe_allow_html=True)
        st.markdown("""
            <h4>💡 Información</h4>
            <ul style="line-height:1.8;">
                <li><strong>Tasa:</strong> 1.5% mensual</li>
                <li><strong>Interés:</strong> Compuesto</li>
                <li><strong>Mínimo:</strong> $2.000.000</li>
                <li><strong>Plazo:</strong> Desde 1 mes</li>
            </ul>
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # FIRMA DIGITAL
    # ---------------------------
    if 'calculo' in st.session_state:

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## ✍️ Firma Digital del Contrato")
        st.markdown("<br>", unsafe_allow_html=True)

        calculo = st.session_state.calculo

        col1, col2 = st.columns([2, 1])

        with col1:

            with st.expander("📄 Ver Contrato de Inversión", expanded=False):
                st.markdown("""
                **CONTRATO DE INVERSIÓN GANADERA — inBezt**

                1. **OBJETO:** Capital destinado a proyectos ganaderos administrados por inBezt SAS.  
                2. **RENTABILIDAD:** Interés compuesto mensual base 1.5%.  
                3. **RESPALDO:** Activos ganaderos del proyecto.  
                4. **RETIRO:** Capital + rendimientos al vencimiento.  
                5. **LEY APLICABLE:** República de Colombia.  
                """)

            st.markdown("<div class='card-ui'>", unsafe_allow_html=True)

            with st.form("solicitud_form"):
                st.info(f"📋 Solicitud por **{formatear_cop(calculo['monto'])}** durante **{calculo['meses']} meses**")

                firma_nombre = st.text_input("👤 Nombre Completo *")
                firma_cedula = st.text_input("🆔 Cédula *")
                notas = st.text_area("📝 Notas adicionales (opcional)")

                st.markdown("---")
                acepto = st.checkbox("Acepto los términos del contrato")

                submit = st.form_submit_button("📤 Enviar Solicitud", use_container_width=True)

                if submit:
                    if not firma_nombre or not firma_cedula:
                        st.error("⚠️ Completa todos los campos obligatorios")
                    elif not acepto:
                        st.error("⚠️ Debes aceptar los términos")
                    else:
                        with st.spinner("Procesando..."):
                            exito, mensaje = crear_inversion(
                                usuario['id'], calculo['monto'], calculo['meses'],
                                firma_nombre, firma_cedula, notas or None
                            )

                            if exito:
                                st.success(f"✅ {mensaje}")
                                st.balloons()
                                st.markdown("### 🏦 Información Bancaria")
                                st.info(f"""
**Banco:** {INFO_BANCARIA['banco']}  
**Cuenta:** {INFO_BANCARIA['numero_cuenta']} ({INFO_BANCARIA['tipo_cuenta']})  
**Titular:** {INFO_BANCARIA['titular']}  
**NIT:** {INFO_BANCARIA['nit']}  

💰 **Monto a transferir:** {formatear_cop(calculo['monto'])}  
                                """)

                                del st.session_state.calculo
                            else:
                                st.error(f"❌ {mensaje}")

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card-ui'>", unsafe_allow_html=True)
            st.markdown("### 📋 Resumen")
            st.write(f"**Monto:** {formatear_cop(calculo['monto'])}")
            st.write(f"**Plazo:** {calculo['meses']} meses")
            st.write(f"**Tasa:** {calculo['tasa']}%")
            st.write(f"**Retorno:** {formatear_cop(calculo['monto_final'])}")
            st.markdown("</div>", unsafe_allow_html=True)


# =========================================
# TAB 2 - MIS INVERSIONES
# =========================================
with tabs[1]:
    st.markdown("### 📈 Mis Inversiones")
    st.markdown("<br>", unsafe_allow_html=True)

    inversiones = obtener_inversiones_usuario(usuario['id'])

    if not inversiones:
        st.info("🔭 Aún no tienes inversiones. Usa la pestaña calculadora.")
    else:

        total_invertido = sum(float(i['monto']) for i in inversiones)
        aprobadas = sum(1 for i in inversiones if i['estado'] == 'aprobado')
        pendientes = sum(1 for i in inversiones if i['estado'] == 'pendiente')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Invertido", formatear_cop(total_invertido))

        with col2:
            st.metric("Aprobadas", aprobadas)

        with col3:
            st.metric("Pendientes", pendientes)

        with col4:
            st.metric("Solicitudes", len(inversiones))

        st.markdown("---")

        estado_color = {
            'pendiente': '🟡',
            'aprobado': '🟢',
            'rechazado': '🔴'
        }

        for inv in inversiones:

            monto_final, intereses = calcular_interes_compuesto(
                float(inv['monto']),
                float(inv['tasa_interes']),
                inv['tiempo_meses']
            )

            with st.expander(f"{estado_color.get(inv['estado'],'⚪')} {inv['numero_solicitud']} — {formatear_cop(float(inv['monto']))} — {inv['estado'].upper()}"):
                
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.write(f"**Monto:** {formatear_cop(float(inv['monto']))}")
                    st.write(f"**Plazo:** {inv['tiempo_meses']} meses")
                    st.write(f"**Tasa:** {float(inv['tasa_interes'])}%")

                with col_b:
                    st.write(f"**Estado:** {inv['estado'].upper()}")
                    st.write(f"**Fecha:** {inv['fecha_solicitud'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Solicitud:** {inv['numero_solicitud']}")

                with col_c:
                    st.write(f"**Retorno Estimado:** {formatear_cop(monto_final)}")
                    st.write(f"**Intereses:** {formatear_cop(intereses)}")

                if inv['notas']:
                    st.info(f"📝 {inv['notas']}")
