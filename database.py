import bcrypt
from datetime import datetime
import random
import string
from config import get_db_connection

def hash_password(password):
    """Hashea una contraseña"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verifica una contraseña contra su hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generar_numero_solicitud():
    """Genera un número único de solicitud"""
    fecha = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.digits, k=6))
    return f"INV-{fecha}-{random_str}"

# ===== USUARIOS =====

def crear_usuario(nombre, cedula, telefono, email, ciudad, contrasena, negocio=None):
    """Crea un nuevo usuario cliente"""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión a la base de datos"
    
    try:
        cursor = conn.cursor()
        hashed_pwd = hash_password(contrasena)
        
        cursor.execute("""
            INSERT INTO usuarios (nombre_completo, cedula, telefono, email, ciudad, 
                                  negocio_empresa, contrasena, rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'cliente')
            RETURNING id
        """, (nombre, cedula, telefono, email, ciudad, negocio, hashed_pwd))
        
        conn.commit()
        return True, "Usuario creado exitosamente"
    except Exception as e:
        conn.rollback()
        if 'cedula' in str(e):
            return False, "La cédula ya está registrada"
        elif 'email' in str(e):
            return False, "El email ya está registrado"
        return False, f"Error al crear usuario: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def login_usuario(email, contrasena):
    """Autentica un usuario"""
    conn = get_db_connection()
    if not conn:
        return None, "Error de conexión"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre_completo, email, rol, contrasena
            FROM usuarios WHERE email = %s
        """, (email,))
        
        usuario = cursor.fetchone()
        
        if not usuario:
            return None, "Usuario no encontrado"
        
        if verify_password(contrasena, usuario['contrasena']):
            return {
                'id': usuario['id'],
                'nombre': usuario['nombre_completo'],
                'email': usuario['email'],
                'rol': usuario['rol']
            }, "Login exitoso"
        else:
            return None, "Contraseña incorrecta"
    finally:
        cursor.close()
        conn.close()

def obtener_todos_usuarios():
    """Obtiene todos los usuarios (para admin)"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre_completo, cedula, telefono, email, ciudad, 
                   negocio_empresa, rol, fecha_registro
            FROM usuarios
            ORDER BY fecha_registro DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ===== INVERSIONES =====

def crear_inversion(usuario_id, monto, tiempo_meses, firma_nombre, firma_cedula, notas):
    """Crea una nueva solicitud de inversión"""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    
    try:
        cursor = conn.cursor()
        numero = generar_numero_solicitud()
        
        cursor.execute("""
            INSERT INTO inversiones (usuario_id, monto, tiempo_meses, firma_nombre, 
                                     firma_cedula, notas, numero_solicitud)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (usuario_id, monto, tiempo_meses, firma_nombre, firma_cedula, notas, numero))
        
        conn.commit()
        return True, f"Solicitud creada: {numero}"
    except Exception as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def obtener_inversiones_usuario(usuario_id):
    """Obtiene todas las inversiones de un usuario"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM inversiones 
            WHERE usuario_id = %s
            ORDER BY fecha_solicitud DESC
        """, (usuario_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obtener_todas_inversiones():
    """Obtiene todas las inversiones (para admin)"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.*, u.nombre_completo as cliente_nombre, u.email as cliente_email
            FROM inversiones i
            JOIN usuarios u ON i.usuario_id = u.id
            ORDER BY i.fecha_solicitud DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def actualizar_estado_inversion(inversion_id, nuevo_estado):
    """Actualiza el estado de una inversión"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inversiones SET estado = %s WHERE id = %s
        """, (nuevo_estado, inversion_id))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

def actualizar_tasa_inversion(inversion_id, nueva_tasa):
    """Actualiza la tasa de interés de una inversión"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inversiones SET tasa_interes = %s WHERE id = %s
        """, (nueva_tasa, inversion_id))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

# ===== CONFIGURACIÓN =====

def obtener_configuracion():
    """Obtiene la configuración actual"""
    conn = get_db_connection()
    if not conn:
        return {'pausar_solicitudes': False}
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT pausar_solicitudes FROM configuracion LIMIT 1")
        result = cursor.fetchone()
        return result if result else {'pausar_solicitudes': False}
    finally:
        cursor.close()
        conn.close()

def actualizar_pausar_solicitudes(pausar):
    """Actualiza el estado de pausa de solicitudes"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE configuracion SET pausar_solicitudes = %s, 
            fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (pausar,))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

def total_aprobado_mes_actual():
    """Calcula el total de dinero aprobado en el mes actual"""
    conn = get_db_connection()
    if not conn:
        return 0
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) as total
            FROM inversiones
            WHERE estado = 'aprobado' 
            AND EXTRACT(YEAR FROM fecha_solicitud) = EXTRACT(YEAR FROM CURRENT_DATE)
            AND EXTRACT(MONTH FROM fecha_solicitud) = EXTRACT(MONTH FROM CURRENT_DATE)
        """)
        result = cursor.fetchone()
        return float(result['total']) if result else 0
    finally:
        cursor.close()
        conn.close()