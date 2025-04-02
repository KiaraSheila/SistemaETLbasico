import streamlit as st
import pandas as pd
import plotly.express as px # Para gráficos más personalizables (opcional, pero recomendado)

# --- Configuración de la Página ---
# Usar layout ancho para aprovechar el espacio
st.set_page_config(layout="wide", page_title="Dashboard ETL - Ventas")

# --- Título del Dashboard ---
st.title("📊 Dashboard de Resultados ETL - Ventas Consolidadas")
st.markdown("Visualización de los datos limpios generados por el pipeline ETL.")

# --- Cargar Datos Limpios ---
# Intentar cargar desde el CSV generado por el pipeline
DATA_FILE = 'datos_limpios.csv'

@st.cache_data # Cachear la carga de datos para mejorar rendimiento
def load_cleaned_data(file_path):
    try:
        # Asegurarse de parsear la fecha correctamente al cargar
        df = pd.read_csv(file_path, parse_dates=['fecha'])
        # Calcular ingresos por fila para análisis
        if 'cantidad' in df.columns and 'precio_unitario' in df.columns:
             df['ingresos'] = df['cantidad'] * df['precio_unitario']
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error inesperado al cargar los datos: {e}")
        return None

df_clean = load_cleaned_data(DATA_FILE)

# --- Mostrar Mensaje si no hay Datos ---
if df_clean is None:
    st.error(f"❌ No se pudo cargar el archivo '{DATA_FILE}'. Asegúrate de que el pipeline ETL (`limpieza_datos.py`) se haya ejecutado correctamente.")
    st.stop() # Detener la ejecución si no hay datos

st.success(f"✔️ Datos cargados exitosamente desde '{DATA_FILE}'.")

# --- Resumen de Métricas Clave ---
st.header("🚀 Resumen General")

total_records = len(df_clean)
total_revenue = df_clean['ingresos'].sum() if 'ingresos' in df_clean.columns else 0
avg_transaction_value = total_revenue / total_records if total_records > 0 else 0
start_date = df_clean['fecha'].min()
end_date = df_clean['fecha'].max()

# Usar columnas para mostrar métricas lado a lado
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transacciones Limpias", f"{total_records:,}")
col2.metric("Ingresos Totales", f"€{total_revenue:,.2f}")
col3.metric("Valor Promedio Trans.", f"€{avg_transaction_value:,.2f}")
# Asegurar que las fechas no sean NaT antes de formatear
col4.metric("Periodo", f"{start_date.strftime('%Y-%m-%d') if pd.notna(start_date) else 'N/A'} a {end_date.strftime('%Y-%m-%d') if pd.notna(end_date) else 'N/A'}")


# --- Exploración de Datos ---
st.header("🔍 Exploración de Datos Limpios")
# Usar un expander para no ocupar mucho espacio por defecto
with st.expander("Ver Tabla de Datos Completa", expanded=False):
    # Mostrar el dataframe interactivo
    st.dataframe(df_clean.drop(columns=['ingresos'], errors='ignore')) # Ocultar columna calculada si se desea


# --- Visualizaciones ---
st.header("📈 Visualizaciones Principales")

# Usar columnas para gráficos
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("💰 Ingresos por Ciudad")
    # Agrupar por ciudad y sumar ingresos
    revenue_by_city = df_clean.groupby('ciudad')['ingresos'].sum().sort_values(ascending=False).reset_index()
    # Crear gráfico de barras con Plotly Express para mejor interactividad
    fig_city = px.bar(revenue_by_city,
                      x='ciudad',
                      y='ingresos',
                      title="Ingresos Totales por Ciudad",
                      labels={'ciudad': 'Ciudad', 'ingresos': 'Ingresos (€)'},
                      text_auto='.2s') # Mostrar valores en las barras
    fig_city.update_layout(xaxis_title="Ciudad", yaxis_title="Ingresos (€)")
    st.plotly_chart(fig_city, use_container_width=True)

with viz_col2:
    st.subheader("📦 Cantidad Vendida por Producto")
    # Agrupar por producto y sumar cantidad
    qty_by_product = df_clean.groupby('descripcion_producto')['cantidad'].sum().sort_values(ascending=False).reset_index()
    # Crear gráfico de barras
    fig_product = px.bar(qty_by_product,
                         x='cantidad',
                         y='descripcion_producto', # Producto en el eje Y para mejor lectura si hay muchos
                         orientation='h', # Gráfico horizontal
                         title="Cantidad Total Vendida por Producto",
                         labels={'descripcion_producto': 'Producto', 'cantidad': 'Cantidad Vendida'},
                         text='cantidad') # Mostrar cantidad en las barras
    fig_product.update_layout(yaxis_title="Producto", xaxis_title="Cantidad Vendida")
    st.plotly_chart(fig_product, use_container_width=True)

# --- Gráfico de Tendencia Temporal ---
st.subheader("📅 Ingresos a lo largo del Tiempo")

# Asegurarse que 'fecha' es el índice para resampling
df_time = df_clean.set_index('fecha')

# Opción de Resampling (Diario 'D', Semanal 'W', Mensual 'M' o 'ME' para fin de mes)
# Usaremos 'ME' para agrupar por mes
revenue_over_time = df_time.resample('ME')['ingresos'].sum().reset_index()

# Crear gráfico de línea
fig_time = px.line(revenue_over_time,
                   x='fecha',
                   y='ingresos',
                   title="Tendencia Mensual de Ingresos",
                   labels={'fecha': 'Mes', 'ingresos': 'Ingresos (€)'},
                   markers=True) # Mostrar puntos en la línea
fig_time.update_layout(xaxis_title="Mes", yaxis_title="Ingresos (€)")
st.plotly_chart(fig_time, use_container_width=True)


# --- Información Adicional ---
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Este dashboard muestra los resultados del pipeline ETL "
    "diseñado para limpiar y consolidar datos de ventas. "
    "Usa Streamlit para la visualización."
)
st.sidebar.header("Fuente de Datos")
st.sidebar.markdown(f"Datos cargados desde: `{DATA_FILE}`")