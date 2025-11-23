import streamlit as st
from database import crear_inversion, obtener_inversiones_usuario, obtener_configuracion
from utils import aplicar_estilos_inbezt, calcular_interes_compuesto, formatear_cop
from config import INFO_BANCARIA
from PIL import Image

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

if st.session_state.get('usuario') is None:
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página")
    st.stop()

usuario = st.session_state.usuario

if usuario['rol'] != 'cliente':
    st.error("❌ Esta página es solo para clientes")
    st.stop()

col_logo, col_title, col_logout = st.columns([1, 4, 1])

with col_logo:
    try:
        logo = Image.open("assets/logo.jpeg")
        st.image(logo, width=80)
    except:
        st.markdown("# 🐮")

with col_title:
    st.markdown(f"""
        <div style="padding: 0.5rem 0;">
            <h2 style="margin: 0; background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                {usuario['nombre']}
            </h2>
            <p style="margin: 0; color: #666;">Dashboard de Inversiones</p>
        </div>
    """, unsafe_allow_html=True)

with col_logout:
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.usuario = None
        st.session_state.page = None
        st.rerun()

st.markdown("---")

tabs = st.tabs(["🧮 Calculadora", "📈 Mis Inversiones"])

with tabs[0]:
    config = obtener_configuracion()
    
    if config.get('pausar_solicitudes', False):
        st.error("⏸️ **Las solicitudes están pausadas temporalmente**")
        st.info("Estamos procesando las inversiones actuales. Pronto podrás hacer nuevas solicitudes.")
    else:
        st.markdown("## 🧮 Simulador de Inversión")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            monto = st.number_input("💵 Monto a invertir (COP)", min_value=2000000, value=5000000, step=500000)
            meses = st.number_input("📅 Tiempo (meses)", min_value=1, value=6, step=1)
            tasa = st.number_input("📈 Tasa de interés mensual (%)", value=1.5, step=0.1, disabled=True)
            
            if st.button("🧮 Calcular Retorno", use_container_width=True, type="primary"):
                monto_final, intereses = calcular_interes_compuesto(monto, tasa, meses)
                
                st.markdown("---")
                st.markdown("### 📊 Resultado de tu Inversión")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Inversión Inicial", formatear_cop(monto))
                with col_b:
                    st.metric("Intereses Ganados", formatear_cop(intereses))
                with col_c:
                    st.metric("Total a Recibir", formatear_cop(monto_final))
                
                st.session_state.calculo = {
                    'monto': monto,
                    'meses': meses,
                    'tasa': tasa,
                    'monto_final': monto_final,
                    'intereses': intereses
                }
                
                st.success("✅ ¿Te gusta el resultado? Continúa abajo para firmar tu solicitud 👇")
        
        with col2:
            st.markdown("""
                <div class="card" style="background: linear-gradient(135deg, #f3f0ff 0%, #e0f2fe 100%);">
                    <h4>💡 Información</h4>
                    <ul>
                        <li><strong>Tasa:</strong> 1.5% mensual</li>
                        <li><strong>Interés:</strong> Compuesto</li>
                        <li><strong>Mínimo:</strong> $2.000.000</li>
                        <li><strong>Plazo:</strong> Desde 1 mes</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        if 'calculo' in st.session_state:
            st.markdown("---")
            st.markdown("## ✍️ Firma Digital del Contrato")
            
            calculo = st.session_state.calculo
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                with st.expander("📄 Ver Contrato de Inversión", expanded=False):
                    st.markdown("""
                    **CONTRATO DE INVERSIÓN GANADERA - inBezt**
                    
                    Entre **inBezt SAS** (EL ADMINISTRADOR) y el cliente firmante (EL INVERSIONISTA), se establece:
                    
                    1. **OBJETO:** El Inversionista entrega capital para inversión en proyectos ganaderos gestionados por el Administrador.
                    
                    2. **MONTO Y PLAZO:** Según lo especificado en la solicitud firmada digitalmente.
                    
                    3. **RENTABILIDAD:** Tasa de interés compuesto mensual según lo acordado (base 1.5%).
                    
                    4. **GARANTÍAS:** El capital invertido está respaldado por activos ganaderos del proyecto.
                    
                    5. **RETIRO:** Al vencimiento del plazo acordado, el Inversionista recibirá el capital más los rendimientos.
                    
                    6. **JURISDICCIÓN:** Leyes de la República de Colombia.
                    """)
                
                with st.form("solicitud_form"):
                    st.info(f"📋 Vas a solicitar una inversión de **{formatear_cop(calculo['monto'])}** por **{calculo['meses']} meses**")
                    
                    firma_nombre = st.text_input("👤 Nombre Completo *", placeholder="Como aparece en tu documento")
                    firma_cedula = st.text_input("🆔 Cédula *", placeholder="Tu número de cédula")
                    notas = st.text_area("📝 Notas o comentarios (opcional)", placeholder="Ej: Si me dan 1.9% puedo invertir 10 millones más")
                    
                    st.markdown("---")
                    acepto_contrato = st.checkbox("✅ He leído y acepto los términos del contrato de inversión")
                    
                    submit = st.form_submit_button("📤 Enviar Solicitud", use_container_width=True)
                    
                    if submit:
                        if not firma_nombre or not firma_cedula:
                            st.error("⚠️ Debes completar todos los campos obligatorios")
                        elif not acepto_contrato:
                            st.error("⚠️ Debes aceptar los términos del contrato")
                        else:
                            with st.spinner("Procesando solicitud..."):
                                exito, mensaje = crear_inversion(usuario['id'], calculo['monto'], calculo['meses'], firma_nombre, firma_cedula, notas if notas else None)
                                
                                if exito:
                                    st.success(f"✅ {mensaje}")
                                    st.balloons()
                                    
                                    st.markdown("### 🏦 Información Bancaria")
                                    st.info(f"""
**Realiza tu transferencia a:**
- **Banco:** {INFO_BANCARIA['banco']}
- **Tipo de cuenta:** {INFO_BANCARIA['tipo_cuenta']}
- **Número de cuenta:** {INFO_BANCARIA['numero_cuenta']}
- **Titular:** {INFO_BANCARIA['titular']}
- **NIT:** {INFO_BANCARIA['nit']}

**Monto a transferir:** {formatear_cop(calculo['monto'])}

⚠️ **Importante:** Una vez realices la transferencia, nuestro equipo verificará tu inversión en las próximas 24-48 horas.
                                    """)
                                    
                                    del st.session_state.calculo
                                else:
                                    st.error(f"❌ {mensaje}")
            
            with col2:
                st.markdown(f"""
                    <div class="card">
                        <h4>📋 Resumen</h4>
                        <p><strong>Monto:</strong><br>{formatear_cop(calculo['monto'])}</p>
                        <p><strong>Plazo:</strong><br>{calculo['meses']} meses</p>
                        <p><strong>Tasa:</strong><br>{calculo['tasa']}% mensual</p>
                        <p><strong>Retorno:</strong><br>{formatear_cop(calculo['monto_final'])}</p>
                    </div>
                """, unsafe_allow_html=True)

with tabs[1]:
    st.markdown("## 📈 Mis Inversiones")
    
    inversiones = obtener_inversiones_usuario(usuario['id'])
    
    if not inversiones:
        st.info("🔭 Aún no tienes inversiones. ¡Crea tu primera inversión en la pestaña Calculadora!")
    else:
        total_invertido = sum(float(inv['monto']) for inv in inversiones)
        aprobadas = sum(1 for inv in inversiones if inv['estado'] == 'aprobado')
        pendientes = sum(1 for inv in inversiones if inv['estado'] == 'pendiente')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Invertido", formatear_cop(total_invertido))
        with col2:
            st.metric("Inversiones Aprobadas", aprobadas)
        with col3:
            st.metric("Pendientes", pendientes)
        with col4:
            st.metric("Total Solicitudes", len(inversiones))
        
        st.markdown("---")
        
        for inv in inversiones:
            estado_color = {'pendiente': '🟡', 'aprobado': '🟢', 'rechazado': '🔴'}
            
            monto_final, intereses = calcular_interes_compuesto(float(inv['monto']), float(inv['tasa_interes']), inv['tiempo_meses'])
            
            with st.expander(f"{estado_color.get(inv['estado'], '⚪')} {inv['numero_solicitud']} - {formatear_cop(float(inv['monto']))} - {inv['estado'].upper()}"):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.write(f"**Monto:** {formatear_cop(float(inv['monto']))}")
                    st.write(f"**Plazo:** {inv['tiempo_meses']} meses")
                    st.write(f"**Tasa:** {float(inv['tasa_interes'])}%")
                
                with col_b:
                    st.write(f"**Estado:** {inv['estado'].upper()}")
                    st.write(f"**Fecha:** {inv['fecha_solicitud'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Número:** {inv['numero_solicitud']}")
                
                with col_c:
                    st.write(f"**Retorno Estimado:** {formatear_cop(monto_final)}")
                    st.write(f"**Intereses:** {formatear_cop(intereses)}")
                
                if inv['notas']:
                    st.info(f"📝 **Notas:** {inv['notas']}")