import streamlit as st
from database import (
    crear_inversion, 
    obtener_inversiones_usuario,
    obtener_configuracion
)
from utils import aplicar_estilos_inbezt, calcular_interes_compuesto, formatear_cop
from config import INFO_BANCARIA
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dashboard Cliente - inBezt", page_icon="💰", layout="wide")
st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

# Verificar autenticación
if st.session_state.get('usuario') is None:
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página")
    st.stop()

usuario = st.session_state.usuario

# Solo clientes
if usuario['rol'] != 'cliente':
    st.error("❌ Esta página es solo para clientes")
    st.stop()

# Header
st.markdown(f"""
    <div class="header-inbezt">
        <h1>💰 Mi Dashboard</h1>
        <p>Bienvenido, {usuario['nombre']}</p>
    </div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["📊 Nueva Inversión", "📈 Mis Inversiones"])

# TAB 1: Nueva Inversión
with tab1:
    # Verificar si las solicitudes están pausadas
    config = obtener_configuracion()
    
    if config.get('pausar_solicitudes', False):
        st.error("⏸️ **Las solicitudes están pausadas temporalmente**")
        st.info("Estamos procesando las inversiones actuales. Pronto podrás hacer nuevas solicitudes.")
        st.stop()
    
    st.markdown("## 🧮 Calculadora de Inversión")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3>Simula tu inversión</h3>
                <p>Ingresa los datos para calcular tu retorno estimado</p>
            </div>
        """, unsafe_allow_html=True)
        
        monto = st.number_input(
            "💵 Monto a invertir (COP)",
            min_value=2000000,
            value=5000000,
            step=500000,
            help="Mínimo $2.000.000 COP"
        )
        
        meses = st.number_input(
            "📅 Tiempo (meses)",
            min_value=1,
            value=6,
            step=1,
            help="Mínimo 1 mes"
        )
        
        tasa = st.number_input(
            "📈 Tasa de interés mensual (%)",
            value=1.5,
            step=0.1,
            disabled=True,
            help="Tasa base de inBezt"
        )
        
        if st.button("🧮 Calcular Retorno", use_container_width=True):
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
            
            # Guardar en session_state para el siguiente paso
            st.session_state.calculo = {
                'monto': monto,
                'meses': meses,
                'tasa': tasa,
                'monto_final': monto_final,
                'intereses': intereses
            }
            
            st.success("✅ ¿Te gusta el resultado? Continúa con tu solicitud abajo 👇")
    
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
    
    # Formulario de solicitud
    if 'calculo' in st.session_state:
        st.markdown("---")
        st.markdown("## ✍️ Firma Digital del Contrato")
        
        calculo = st.session_state.calculo
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("solicitud_form"):
                st.info(f"📋 Vas a solicitar una inversión de **{formatear_cop(calculo['monto'])}** por **{calculo['meses']} meses**")
                
                firma_nombre = st.text_input(
                    "👤 Nombre Completo *",
                    placeholder="Como aparece en tu documento"
                )
                
                firma_cedula = st.text_input(
                    "🆔 Cédula *",
                    placeholder="Tu número de cédula"
                )
                
                notas = st.text_area(
                    "📝 Notas o comentarios (opcional)",
                    placeholder="Ej: Si me dan 1.9% puedo invertir 10 millones más",
                    help="Aquí puedes dejar solicitudes especiales o comentarios"
                )
                
                st.markdown("---")
                acepto_contrato = st.checkbox("✅ Acepto los términos del contrato de inversión")
                
                submit = st.form_submit_button("📤 Enviar Solicitud", use_container_width=True)
                
                if submit:
                    if not firma_nombre or not firma_cedula:
                        st.error("⚠️ Debes completar todos los campos obligatorios")
                    elif not acepto_contrato:
                        st.error("⚠️ Debes aceptar los términos del contrato")
                    else:
                        with st.spinner("Procesando solicitud..."):
                            exito, mensaje = crear_inversion(
                                usuario['id'],
                                calculo['monto'],
                                calculo['meses'],
                                firma_nombre,
                                firma_cedula,
                                notas if notas else None
                            )
                            
                            if exito:
                                st.success(f"✅ {mensaje}")
                                st.balloons()
                                
                                # Mostrar información bancaria
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
                                
                                # Limpiar session_state
                                del st.session_state.calculo
                            else:
                                st.error(f"❌ {mensaje}")
        
        with col2:
            st.markdown("""
                <div class="card">
                    <h4>📋 Resumen</h4>
                    <p><strong>Monto:</strong><br>{}</p>
                    <p><strong>Plazo:</strong><br>{} meses</p>
                    <p><strong>Tasa:</strong><br>{}% mensual</p>
                    <p><strong>Retorno:</strong><br>{}</p>
                </div>
            """.format(
                formatear_cop(calculo['monto']),
                calculo['meses'],
                calculo['tasa'],
                formatear_cop(calculo['monto_final'])
            ), unsafe_allow_html=True)

# TAB 2: Mis Inversiones
with tab2:
    st.markdown("## 📈 Mis Inversiones")
    
    inversiones = obtener_inversiones_usuario(usuario['id'])
    
    if not inversiones:
        st.info("📭 Aún no tienes inversiones. ¡Crea tu primera inversión en la pestaña anterior!")
    else:
        # Estadísticas generales
        total_invertido = sum(inv['monto'] for inv in inversiones)
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
        
        # Mostrar cada inversión
        for inv in inversiones:
            estado_color = {
                'pendiente': '🟡',
                'aprobado': '🟢',
                'rechazado': '🔴'
            }
            
            monto_final, intereses = calcular_interes_compuesto(
                float(inv['monto']), 
                float(inv['tasa_interes']), 
                inv['tiempo_meses']
            )
            
            with st.expander(f"{estado_color.get(inv['estado'], '⚪')} {inv['numero_solicitud']} - {formatear_cop(inv['monto'])} - {inv['estado'].upper()}"):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.write(f"**Monto:** {formatear_cop(inv['monto'])}")
                    st.write(f"**Plazo:** {inv['tiempo_meses']} meses")
                    st.write(f"**Tasa:** {inv['tasa_interes']}%")
                
                with col_b:
                    st.write(f"**Estado:** {inv['estado'].upper()}")
                    st.write(f"**Fecha:** {inv['fecha_solicitud'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Número:** {inv['numero_solicitud']}")
                
                with col_c:
                    st.write(f"**Retorno Estimado:** {formatear_cop(monto_final)}")
                    st.write(f"**Intereses:** {formatear_cop(intereses)}")
                
                if inv['notas']:
                    st.info(f"📝 **Notas:** {inv['notas']}")