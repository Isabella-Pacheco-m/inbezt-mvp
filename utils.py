def calcular_interes_compuesto(monto, tasa_mensual, meses):
    """
    Calcula el interés compuesto
    Retorna: (monto_final, intereses_ganados)
    """
    tasa_decimal = tasa_mensual / 100
    monto_final = monto * ((1 + tasa_decimal) ** meses)
    intereses = monto_final - monto
    return monto_final, intereses

def formatear_cop(monto):
    """Formatea un número como pesos colombianos"""
    return f"${monto:,.0f} COP".replace(",", ".")

def aplicar_estilos_inbezt():
    """Retorna el CSS personalizado de inBezt"""
    return """
    <style>
    /* Fuentes y colores principales */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Gradientes de inBezt */
    .gradient-purple {
        background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%);
    }
    
    /* Botones personalizados */
    .stButton>button {
        background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(155, 135, 245, 0.4);
    }
    
    /* Tarjetas */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0f2fe;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #9b87f5;
        box-shadow: 0 0 0 2px rgba(155, 135, 245, 0.2);
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #9b87f5 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Alertas */
    .alert-success {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Tablas */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Header personalizado */
    .header-inbezt {
        background: linear-gradient(135deg, #9b87f5 0%, #7dd3fc 50%, #f472b6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """