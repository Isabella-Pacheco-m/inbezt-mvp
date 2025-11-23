import streamlit as st
from database import (
    obtener_todos_usuarios,
    obtener_todas_inversiones,
    actualizar_estado_inversion,
    actualizar_tasa_inversion,
    total_aprobado_mes_actual,
    obtener_configuracion,
    actualizar_pausar_solicitudes
)
from utils import aplicar_estilos_inbezt, calcular_interes_compuesto, formatear_cop
import pandas as pd
from datetime import datetime

st.markdown(aplicar_estilos_inbezt(), unsafe_allow_html=True)

if st.session_state.get('usuario') is None:
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página")
    st.stop()

usuario = st.session_state.usuario

if usuario['rol'] != 'admin':
    st.error("❌ Esta página es solo para administradores")
    st.stop()

st.markdown(f"""
    <div class="header-inbezt">
        <h1>⚙️ Panel de Administración</h1>
        <p>Gestión completa de inBezt</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Solicitudes", "👥 Usuarios", "⚙️ Configuración"])

with tab1:
    st.markdown("## 📊 Estadísticas Generales")
    
    inversiones = obtener_todas_inversiones()
    usuarios_lista = obtener_todos_usuarios()
    total_mes = total_aprobado_mes_actual()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Total Mes Actual", formatear_cop(total_mes))
    
    with col2:
        pendientes = sum(1 for inv in inversiones if inv['estado'] == 'pendiente')
        st.metric("⏳ Pendientes", pendientes)
    
    with col3:
        aprobadas = sum(1 for inv in inversiones if inv['estado'] == 'aprobado')
        st.metric("✅ Aprobadas", aprobadas)
    
    with col4:
        rechazadas = sum(1 for inv in inversiones if inv['estado'] == 'rechazado')
        st.metric("❌ Rechazadas", rechazadas)
    
    with col5:
        total_clientes = sum(1 for u in usuarios_lista if u['rol'] == 'cliente')
        st.metric("👥 Total Clientes", total_clientes)
    
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 📈 Últimas Solicitudes")
        if inversiones:
            ultimas = inversiones[:5]
            data = []
            for inv in ultimas:
                data.append({
                    'Número': inv['numero_solicitud'],
                    'Cliente': inv['cliente_nombre'],
                    'Monto': formatear_cop(float(inv['monto'])),
                    'Estado': inv['estado'].upper(),
                    'Fecha': inv['fecha_solicitud'].strftime('%Y-%m-%d')
                })
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay solicitudes aún")
    
    with col_b:
        st.markdown("### 💵 Inversiones por Estado")
        if inversiones:
            total_pendiente = float(sum(inv['monto'] for inv in inversiones if inv['estado'] == 'pendiente'))
            total_aprobado = float(sum(inv['monto'] for inv in inversiones if inv['estado'] == 'aprobado'))
            total_rechazado = float(sum(inv['monto'] for inv in inversiones if inv['estado'] == 'rechazado'))
            
            st.write(f"**Pendiente:** {formatear_cop(total_pendiente)}")
            st.write(f"**Aprobado:** {formatear_cop(total_aprobado)}")
            st.write(f"**Rechazado:** {formatear_cop(total_rechazado)}")
            
            total_general = total_aprobado + total_pendiente + total_rechazado
            if total_general > 0:
                progreso = float(total_aprobado / total_general)
                st.progress(min(progreso, 1.0))
            else:
                st.progress(0.0)
        else:
            st.info("No hay datos para mostrar")

with tab2:
    st.markdown("## 📋 Gestión de Solicitudes de Inversión")
    
    inversiones = obtener_todas_inversiones()
    
    if not inversiones:
        st.info("🔭 No hay solicitudes de inversión aún")
    else:
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            filtro_estado = st.selectbox(
                "Filtrar por Estado",
                ["Todos", "pendiente", "aprobado", "rechazado"]
            )
        
        with col_filtro2:
            buscar_cliente = st.text_input("🔍 Buscar por nombre de cliente")
        
        with col_filtro3:
            ordenar = st.selectbox(
                "Ordenar por",
                ["Fecha (Reciente)", "Fecha (Antigua)", "Monto (Mayor)", "Monto (Menor)"]
            )
        
        inversiones_filtradas = inversiones.copy()
        
        if filtro_estado != "Todos":
            inversiones_filtradas = [inv for inv in inversiones_filtradas if inv['estado'] == filtro_estado]
        
        if buscar_cliente:
            inversiones_filtradas = [
                inv for inv in inversiones_filtradas 
                if buscar_cliente.lower() in inv['cliente_nombre'].lower()
            ]
        
        if ordenar == "Fecha (Reciente)":
            inversiones_filtradas.sort(key=lambda x: x['fecha_solicitud'], reverse=True)
        elif ordenar == "Fecha (Antigua)":
            inversiones_filtradas.sort(key=lambda x: x['fecha_solicitud'])
        elif ordenar == "Monto (Mayor)":
            inversiones_filtradas.sort(key=lambda x: float(x['monto']), reverse=True)
        elif ordenar == "Monto (Menor)":
            inversiones_filtradas.sort(key=lambda x: float(x['monto']))
        
        st.markdown(f"**Mostrando {len(inversiones_filtradas)} de {len(inversiones)} solicitudes**")
        st.markdown("---")
        
        for inv in inversiones_filtradas:
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
            
            with st.expander(
                f"{estado_color.get(inv['estado'], '⚪')} **{inv['numero_solicitud']}** | "
                f"{inv['cliente_nombre']} | {formatear_cop(float(inv['monto']))} | {inv['estado'].upper()}"
            ):
                st.markdown("### 👤 Información del Cliente")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Nombre:** {inv['cliente_nombre']}")
                    st.write(f"**Email:** {inv['cliente_email']}")
                
                with col2:
                    st.write(f"**Fecha Solicitud:** {inv['fecha_solicitud'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Número:** {inv['numero_solicitud']}")
                
                with col3:
                    st.write(f"**Estado Actual:** {inv['estado'].upper()}")
                
                st.markdown("---")
                
                st.markdown("### 💰 Detalles de la Inversión")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Monto", formatear_cop(float(inv['monto'])))
                
                with col2:
                    st.metric("Plazo", f"{inv['tiempo_meses']} meses")
                
                with col3:
                    st.metric("Tasa", f"{float(inv['tasa_interes'])}%")
                
                with col4:
                    st.metric("Retorno Total", formatear_cop(monto_final))
                
                st.markdown("---")
                
                st.markdown("### ✍️ Firma Digital")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Nombre en firma:** {inv['firma_nombre']}")
                
                with col2:
                    st.write(f"**Cédula en firma:** {inv['firma_cedula']}")
                
                if inv['notas']:
                    st.markdown("### 📝 Notas del Cliente")
                    st.info(inv['notas'])
                
                st.markdown("---")
                
                st.markdown("### ⚙️ Acciones de Administrador")
                
                col_acc1, col_acc2, col_acc3 = st.columns(3)
                
                with col_acc1:
                    st.markdown("**Cambiar Estado:**")
                    nuevo_estado = st.selectbox(
                        "Nuevo estado",
                        ["pendiente", "aprobado", "rechazado"],
                        index=["pendiente", "aprobado", "rechazado"].index(inv['estado']),
                        key=f"estado_{inv['id']}"
                    )
                    
                    if st.button(f"💾 Actualizar Estado", key=f"btn_estado_{inv['id']}"):
                        if actualizar_estado_inversion(inv['id'], nuevo_estado):
                            st.success(f"✅ Estado actualizado a: {nuevo_estado}")
                            st.rerun()
                        else:
                            st.error("❌ Error al actualizar")
                
                with col_acc2:
                    st.markdown("**Ajustar Tasa:**")
                    nueva_tasa = st.number_input(
                        "Nueva tasa (%)",
                        min_value=0.1,
                        max_value=10.0,
                        value=float(inv['tasa_interes']),
                        step=0.1,
                        key=f"tasa_{inv['id']}"
                    )
                    
                    if st.button(f"💾 Actualizar Tasa", key=f"btn_tasa_{inv['id']}"):
                        if actualizar_tasa_inversion(inv['id'], nueva_tasa):
                            st.success(f"✅ Tasa actualizada a: {nueva_tasa}%")
                            st.rerun()
                        else:
                            st.error("❌ Error al actualizar")
                
                with col_acc3:
                    st.markdown("**Resumen:**")
                    nueva_final, nuevos_int = calcular_interes_compuesto(
                        float(inv['monto']), nueva_tasa, inv['tiempo_meses']
                    )
                    st.write(f"**Nuevo retorno:** {formatear_cop(nueva_final)}")
                    st.write(f"**Nuevos intereses:** {formatear_cop(nuevos_int)}")

with tab3:
    st.markdown("## 👥 Gestión de Usuarios")
    
    usuarios_lista = obtener_todos_usuarios()
    
    if not usuarios_lista:
        st.info("No hay usuarios registrados")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            filtro_rol = st.selectbox("Filtrar por Rol", ["Todos", "cliente", "admin"])
        
        with col2:
            buscar_usuario = st.text_input("🔍 Buscar usuario")
        
        usuarios_filtrados = usuarios_lista.copy()
        
        if filtro_rol != "Todos":
            usuarios_filtrados = [u for u in usuarios_filtrados if u['rol'] == filtro_rol]
        
        if buscar_usuario:
            usuarios_filtrados = [
                u for u in usuarios_filtrados 
                if buscar_usuario.lower() in u['nombre_completo'].lower() or 
                   buscar_usuario.lower() in u['email'].lower()
            ]
        
        st.markdown(f"**Mostrando {len(usuarios_filtrados)} de {len(usuarios_lista)} usuarios**")
        st.markdown("---")
        
        data = []
        for u in usuarios_filtrados:
            data.append({
                'Nombre': u['nombre_completo'],
                'Cédula': u['cedula'],
                'Email': u['email'],
                'Teléfono': u['telefono'],
                'Ciudad': u['ciudad'],
                'Empresa': u['negocio_empresa'] or '-',
                'Rol': u['rol'].upper(),
                'Registro': u['fecha_registro'].strftime('%Y-%m-%d')
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

with tab4:
    st.markdown("## ⚙️ Configuración del Sistema")
    
    config = obtener_configuracion()
    total_mes = total_aprobado_mes_actual()
    
    st.markdown("### 💰 Control de Flujo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div class="card">
                <h3>Total Aprobado Este Mes</h3>
                <h2 style="color: #9b87f5;">{formatear_cop(total_mes)}</h2>
                <p>Monto total de inversiones aprobadas en {datetime.now().strftime('%B %Y')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pausado = config.get('pausar_solicitudes', False)
        
        st.markdown(f"""
            <div class="card" style="background: {'#fee2e2' if pausado else '#d1fae5'};">
                <h4>Estado del Sistema</h4>
                <h3>{'⏸️ PAUSADO' if pausado else '▶️ ACTIVO'}</h3>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎛️ Control de Solicitudes")
    
    pausar = st.toggle(
        "Pausar nuevas solicitudes de inversión",
        value=config.get('pausar_solicitudes', False),
        help="Cuando está activado, los clientes no podrán enviar nuevas solicitudes"
    )
    
    if st.button("💾 Guardar Configuración", type="primary"):
        if actualizar_pausar_solicitudes(pausar):
            st.success("✅ Configuración actualizada correctamente")
            st.rerun()
        else:
            st.error("❌ Error al actualizar configuración")
    
    if pausar:
        st.warning("⚠️ **Las solicitudes están pausadas.** Los clientes verán un mensaje informativo.")
    else:
        st.info("✅ **Las solicitudes están activas.** Los clientes pueden enviar nuevas inversiones.")
    
    st.markdown("---")
    
    st.markdown("### 📊 Estadísticas Adicionales")
    
    inversiones = obtener_todas_inversiones()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_invertido = float(sum(inv['monto'] for inv in inversiones if inv['estado'] == 'aprobado'))
        st.metric("💰 Total Invertido (Aprobado)", formatear_cop(total_invertido))
    
    with col2:
        inversiones_aprobadas = [i for i in inversiones if i['estado'] == 'aprobado']
        if inversiones_aprobadas:
            promedio = total_invertido / len(inversiones_aprobadas)
        else:
            promedio = 0
        st.metric("📊 Promedio por Inversión", formatear_cop(promedio))
    
    with col3:
        if inversiones:
            tasa_aprobacion = (len([i for i in inversiones if i['estado'] == 'aprobado']) / len(inversiones) * 100)
        else:
            tasa_aprobacion = 0
        st.metric("✅ Tasa de Aprobación", f"{tasa_aprobacion:.1f}%")