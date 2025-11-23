import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

# Colores de inBezt
COLORS = {
    'purple': '#9b87f5',
    'blue': '#7dd3fc',
    'pink': '#f472b6',
    'light_purple': '#f3f0ff',
    'light_blue': '#e0f2fe',
    'light_pink': '#fce7f3'
}

# Configuración de base de datos desde Streamlit Secrets
DB_CONFIG = {
    'host': st.secrets["database"]["host"],
    'port': st.secrets["database"]["port"],
    'database': st.secrets["database"]["database"],
    'user': st.secrets["database"]["user"],
    'password': st.secrets["database"]["password"]
}

def get_db_connection():
    """Crea y retorna una conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return None

# Información bancaria del negocio
INFO_BANCARIA = {
    'banco': 'Bancolombia',
    'tipo_cuenta': 'Cuenta de Ahorros',
    'numero_cuenta': '1234567890',
    'titular': 'inBezt SAS',
    'nit': '900.123.456-7'
}