# Plataforma de Unificación y Calidad de Datos (ETL Básico y Dashboard)

## Descripción General

Este proyecto aborda el desafío común de manejar datos heterogéneos, inconsistentes y desordenados ("data legacy") provenientes de diversas fuentes. Implementa un pipeline ETL (Extract, Transform, Load) básico utilizando Python (Pandas, NumPy) para consolidar, limpiar, normalizar y estandarizar estos datos, dejándolos listos para análisis fiables, toma de decisiones o para alimentar modelos de Inteligencia Artificial. Adicionalmente, incluye un dashboard interactivo (Streamlit, Plotly) para visualizar los datos limpios y obtener insights rápidos.

## Problema Abordado

Los datos en formatos inconsistentes (fechas variadas, errores tipográficos, valores faltantes, duplicados, números como texto) dificultan enormemente el análisis, la generación de informes y la aplicación de técnicas de IA, llevando a resultados erróneos y pérdida de tiempo.

## Solución Implementada: Pipeline ETL con Python

Se desarrolló un pipeline automatizado con los siguientes pasos:

1.  **Extract (Extracción):**
    *   Lectura inicial de datos desde archivos CSV (diseñado para ser extensible a APIs, BBDD).
    *   Lectura inicial como texto (`dtype=str`) para manejo seguro de datos sucios.

2.  **Transform (Transformación):** Etapa central de limpieza y normalización:
    *   **Limpieza de Nombres de Columnas:** Estandarización (minúsculas, sin espacios/caracteres especiales).
    *   **Limpieza de Texto:** Eliminación de espacios extra, corrección de mayúsculas/minúsculas.
    *   **Manejo de Valores Faltantes:** Identificación (explícitos e implícitos como 'N/A') e imputación (ej. 'Sin Notas').
    *   **Conversión de Tipos de Datos:**
        *   **Fechas:** Parseo inteligente de múltiples formatos a `datetime` estándar.
        *   **Números:** Conversión de texto ('uno', '$ 1,250.50') a tipos numéricos (`int`, `float`), eliminando símbolos/comas.
    *   **Estandarización Categórica:** Unificación de valores equivalentes ('Laptop Modelo X' vs 'Laptop Model X').
    *   **Eliminación de Filas Inválidas:** Descarte de filas con datos críticos no recuperables.
    *   **Eliminación de Duplicados:** Basado en `id_transaccion`.
    *   **Formato Final:** Aplicación de 'Title Case' para legibilidad.

3.  **Load (Carga):** Los datos limpios y ordenados se guardan en:
    *   Archivo CSV (`datos_limpios.csv`).
    *   Archivo Excel (`datos_limpios.xlsx`) con formato avanzado (colores, anchos, formatos numéricos) usando `XlsxWriter`.
    *   *(Capacidad opcional comentada para cargar a BBDD SQL (SQLAlchemy) y NoSQL (pymongo)).*

## Visualización: Dashboard Interactivo

Se creó un dashboard con `Streamlit` y `Plotly` para:

*   Mostrar métricas clave de resumen.
*   Explorar los datos limpios en una tabla interactiva.
*   Visualizar insights:
    *   Ingresos por ciudad (barras).
    *   Cantidad por producto (barras horizontales).
    *   Tendencia de ingresos mensual (líneas).

## Pila Tecnológica

*   **Lenguaje:** Python 3
*   **Manipulación de Datos:** `Pandas`, `NumPy`
*   **Excel Avanzado:** `XlsxWriter`
*   **Dashboard Web:** `Streamlit`
*   **Gráficos:** `Plotly`
*   **BBDD (Opcional):** `SQLAlchemy`, `pymongo`
*   **Gestión de Entorno:** `venv`, `pip`, `requirements.txt`
*   **Control de Versiones:** Git, GitHub

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/TamaraKaren/Consolidacion_Normalizacion_Datos.git
    cd Consolidacion_Normalizacion_Datos
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1.  **Ejecutar el Pipeline ETL:**
    ```bash
    python etl_pipeline.py  # Reemplaza 'etl_pipeline.py' con el nombre real de tu script ETL
    ```
    *Esto generará los archivos `datos_limpios.csv` y `datos_limpios.xlsx`.*
2.  **Lanzar el Dashboard:**
    ```bash
    streamlit run dashboard.py # Reemplaza 'dashboard.py' con el nombre real de tu script de dashboard
    ```
3.  Abrir la URL proporcionada por Streamlit en el navegador.

## Capturas de Pantalla (Ejemplos)

Ejemplo Excel antes

<img width="619" alt="{911425B5-67BC-4A7E-9EBB-3D1743D4F25A}" src="https://github.com/user-attachments/assets/e70f28f5-ac65-4320-89ee-497e368c89cf" />


Ejemplo Excel despues


<img width="944" alt="{958FB6D6-250F-496A-AD45-63CEC5C76C4C}" src="https://github.com/user-attachments/assets/fcd97850-871a-4a51-97a8-58efe84ac58d" />


Ejemplo Dashboard


<img width="929" alt="{F719778E-75F8-4B07-9A2F-8349363E562A}" src="https://github.com/user-attachments/assets/a8be6dc1-11d3-4a9e-aec6-5338de87794e" />
<img width="926" alt="{F4144A1E-1C92-4A31-A405-E29E943E16F6}" src="https://github.com/user-attachments/assets/bceac91a-239e-4f33-b1a2-df5514c74847" />
<img width="929" alt="{E25D809E-AC74-4CA4-BF25-2407BDC2BF43}" src="https://github.com/user-attachments/assets/17bb0329-e652-4995-a49d-816499eba5fc" />


## Habilidades Demostradas

*   **Diseño e implementación de pipelines ETL** con Python.
*   **Limpieza y transformación de datos avanzada (Data Wrangling/Cleansing)** usando Pandas: manejo de múltiples formatos, valores faltantes, tipos de datos, duplicados, estandarización.
*   **Validación de Calidad de Datos**.
*   **Generación de salidas de datos estructuradas** (CSV, Excel formateado).
*   **Creación de dashboards interactivos** para visualización y monitoreo de datos (`Streamlit`, `Plotly`).
*   **Aplicación de buenas prácticas** (entornos virtuales, gestión de dependencias, control de versiones).

