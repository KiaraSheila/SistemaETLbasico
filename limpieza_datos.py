# archivo: limpieza_datos.py (Versión Final Completa - Cabeceras Excel Formateadas)
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine
# from pymongo import MongoClient # Importación movida dentro del try/except
try:
    import xlsxwriter # Necesario para formato avanzado
except ImportError:
    print("Advertencia: Instala 'xlsxwriter' para formato Excel avanzado: pip install xlsxwriter")

# --- EXTRACT ---
def extract_data(file_path):
    """Lee datos desde un archivo CSV."""
    try:
        df = pd.read_csv(file_path, dtype=str, delimiter=',')
        print(f"Datos extraídos exitosamente de {file_path}")
        print(f"Número inicial de filas: {len(df)}")
        print("Primeras filas de datos crudos:")
        print(df.head())
        print("\nTipos de datos iniciales (leídos como string):")
        df.info()
        return df
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error durante la extracción: {e}")
        return None

# --- TRANSFORM ---
def clean_column_names(df):
    """Limpia los nombres de las columnas."""
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
    print("\nNombres de columnas limpiados:")
    print(df.columns)
    return df

def clean_text_data(df, columns):
    """Limpia datos de texto (espacios, minúsculas iniciales)."""
    print(f"\nLimpiando columnas de texto: {columns}")
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)
    return df

def handle_missing_values(df):
    """Maneja valores faltantes."""
    print("\nManejando valores faltantes...")
    missing_markers = ['n/a', 'na', 'null', '', '--']
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.lower().replace(missing_markers, np.nan, regex=False)
    print("Valores nulos por columna ANTES del tratamiento específico:")
    print(df.isnull().sum())
    if 'notas' in df.columns:
        df['notas'] = df['notas'].fillna('sin notas')
    print("\nValores nulos por columna DESPUÉS del tratamiento inicial:")
    print(df.isnull().sum())
    return df

def convert_data_types(df):
    """Convierte columnas a los tipos de datos correctos."""
    print("\nConvirtiendo tipos de datos...")
    # --- Fechas ---
    if 'fecha' in df.columns:
        print("Intentando convertir fechas con múltiples formatos...")
        original_dates = df['fecha'].copy()
        df['fecha'] = pd.to_datetime(original_dates, format='%Y-%m-%d', errors='coerce')
        mask = df['fecha'].isnull(); df.loc[mask, 'fecha'] = pd.to_datetime(original_dates[mask], format='%d/%m/%Y', errors='coerce')
        mask = df['fecha'].isnull(); df.loc[mask, 'fecha'] = pd.to_datetime(original_dates[mask], format='%Y/%m/%d', errors='coerce')
        mask = df['fecha'].isnull(); df.loc[mask, 'fecha'] = pd.to_datetime(original_dates[mask], format='%b %d, %y', errors='coerce')
        mask = df['fecha'].isnull(); df.loc[mask, 'fecha'] = pd.to_datetime(original_dates[mask], format='%b %d %Y', errors='coerce')
        print(f"Fechas convertidas. Nulos restantes en 'fecha': {df['fecha'].isnull().sum()}")
    # --- Números (Cantidad) ---
    if 'cantidad' in df.columns:
        replacements = {'uno': '1', 'dos': '2'}
        df['cantidad'] = df['cantidad'].astype(str).replace(replacements)
        df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    # --- Números (Precio Unitario) ---
    if 'precio_unitario' in df.columns:
        df['precio_unitario'] = df['precio_unitario'].astype(str).str.replace(r'[$, ]', '', regex=True)
        df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')
    print("\nTipos de datos DESPUÉS de la conversión:")
    df.info()
    print("\nValores nulos DESPUÉS de la conversión:")
    print(df.isnull().sum())
    return df

def standardize_categorical_data(df):
    """Estandariza valores en columnas categóricas."""
    print("\nEstandarizando datos categóricos...")
    if 'descripcion_producto' in df.columns:
        df['descripcion_producto'] = df['descripcion_producto'].astype(str)
        replacements = {'laptop model x': 'laptop modelo x', 'teclado inalambrico': 'teclado inalámbrico', 'monitor 24"': 'monitor 24 pulgadas'}
        df['descripcion_producto'] = df['descripcion_producto'].replace(replacements)
        print("\nValores únicos en 'descripcion_producto':"); print(df['descripcion_producto'].unique())
    if 'ciudad' in df.columns:
        df['ciudad'] = df['ciudad'].astype(str)
        city_replacements = { 'málaga': 'malaga' }
        df['ciudad'] = df['ciudad'].replace(city_replacements)
        print("\nValores únicos en 'ciudad':"); print(df['ciudad'].unique())
    return df

def remove_duplicates(df):
    """Elimina filas duplicadas basado en id_transaccion."""
    print("\nBuscando y eliminando duplicados...")
    initial_rows = len(df)
    subset_cols = ['id_transaccion']
    if all(col in df.columns for col in subset_cols):
        print(f"Eliminando duplicados basados en: {subset_cols}, manteniendo la primera.")
        df.drop_duplicates(subset=subset_cols, keep='first', inplace=True)
    else:
        print(f"Advertencia: Columna {subset_cols} no encontrada. Eliminando duplicados exactos.")
        df.drop_duplicates(inplace=True)
    rows_removed = initial_rows - len(df)
    print(f"Se eliminaron {rows_removed} filas duplicadas.")
    return df

def apply_transformations(df):
    """Aplica toda la secuencia de transformaciones."""
    if df is None: return None
    df = clean_column_names(df)
    text_cols = [col for col in ['nombre_cliente', 'producto_id', 'descripcion_producto', 'ciudad', 'region', 'notas'] if col in df.columns]
    df = clean_text_data(df, text_cols)
    df = handle_missing_values(df)
    df = convert_data_types(df)
    # --- Manejo de Nulos Críticos POST-Conversión ---
    cols_to_check_for_nan = ['fecha', 'cantidad', 'precio_unitario', 'id_transaccion']
    cols_to_check_for_nan = [col for col in cols_to_check_for_nan if col in df.columns]
    if cols_to_check_for_nan:
        initial_rows = len(df); print(f"\nFilas ANTES de dropna crítico: {initial_rows}"); print(f"Nulos ANTES:\n{df[cols_to_check_for_nan].isnull().sum()}")
        df.dropna(subset=cols_to_check_for_nan, inplace=True)
        print(f"Filas DESPUÉS de dropna crítico: {len(df)}"); print(f"Se eliminaron {initial_rows - len(df)} filas con nulos críticos.")
    else: print("\nAdvertencia: No se encontraron columnas críticas para dropna.")
    # --- Conversión Final de Tipos ---
    if 'cantidad' in df.columns and df['cantidad'].isnull().sum() == 0:
         try: df['cantidad'] = df['cantidad'].astype(int)
         except ValueError as e: print(f"Advertencia: 'cantidad' no se pudo convertir a entero: {e}")
    df = standardize_categorical_data(df)
    df = remove_duplicates(df)
    # Validación final
    if 'precio_unitario' in df.columns:
        invalid_prices = df[df['precio_unitario'] <= 0]
        if not invalid_prices.empty: print("\nALERTA: Precios no positivos:"); print(invalid_prices); df = df[df['precio_unitario'] > 0]

    # --- Aplicar Title Case ---
    print("\nAplicando formato Title Case a columnas de texto...")
    title_case_cols = ['nombre_cliente', 'descripcion_producto', 'ciudad', 'region', 'notas']
    for col in title_case_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title().replace('Nan', 'Sin Notas' if col == 'notas' else '')
    # --- Fin Title Case ---

    print("\n--- Transformación Completa ---")
    print("Primeras filas de datos limpios (con Title Case):")
    print(df.head())
    print("\nTipos de datos finales:")
    df.info()
    print(f"Número final de filas: {len(df)}")
    return df


# --- LOAD ---
def load_data(df, target_format='csv', **kwargs):
    """Carga los datos transformados con formato mejorado para Excel y cabeceras."""
    if df is None or df.empty: print("\nAdvertencia: No hay datos limpios para cargar."); return
    print(f"\nCargando datos en formato: {target_format.upper()}")
    try:
        if target_format == 'csv':
            file_path = kwargs.get('file_path', 'datos_limpios.csv')
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"Datos guardados exitosamente en {file_path}")

        elif target_format == 'excel':
            file_path = kwargs.get('file_path', 'datos_limpios.xlsx')
            sheet_name = kwargs.get('sheet_name', 'Datos Limpios')
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter', datetime_format='yyyy-mm-dd')
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            header_format = workbook.add_format({'bold': True, 'text_wrap': False, 'valign': 'vcenter', 'align': 'center', 'fg_color': '#DDEBF7', 'border': 1})
            currency_format = workbook.add_format({'num_format': '#,##0.00 €'})
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            integer_format = workbook.add_format({'num_format': '0'})

            # --- Escribir CABECERA formateada y transformada ---
            print("Formateando cabeceras para Excel...")
            for col_num, original_header_value in enumerate(df.columns.values):
                formatted_header = original_header_value.replace('_', ' ').title() # Transformar cabecera
                worksheet.write(0, col_num, formatted_header, header_format) # Escribir cabecera formateada

            # --- Aplicar formato y autoajuste a las COLUMNAS de datos ---
            for idx, col in enumerate(df.columns):
                series = df[col]; max_len = 0
                original_header_value = df.columns.values[idx] # Nombre original para buscar datos
                formatted_header = original_header_value.replace('_', ' ').title() # Nombre formateado para medir ancho
                try: max_len = max((series.astype(str).map(len).max(), len(formatted_header))) + 3
                except: max_len = len(formatted_header) + 3
                max_len = max(max_len, 12)
                col_format = None
                if pd.api.types.is_datetime64_any_dtype(series.dtype): col_format = date_format
                elif col == 'precio_unitario': col_format = currency_format
                elif col == 'cantidad': col_format = integer_format
                worksheet.set_column(idx, idx, max_len, col_format)

            writer.close()
            print(f"Datos guardados exitosamente y formateados en {file_path}")

        elif target_format == 'sql':
            connection_string = kwargs.get('db_connection_string'); table_name = kwargs.get('table_name', 'transacciones_limpias')
            if not connection_string: print("Error: Se requiere 'db_connection_string' para SQL."); return
            engine = create_engine(connection_string)
            with engine.connect() as connection: df.to_sql(table_name, con=connection, if_exists='replace', index=False); print(f"Datos cargados a tabla '{table_name}'.")

        elif target_format == 'mongodb':
            # --- Bloque CORREGIDO para importar pymongo ---
            try:
                from pymongo import MongoClient
                from pymongo.errors import ConnectionFailure
            except ImportError:
                print("Error: La librería 'pymongo' es necesaria para cargar en MongoDB.")
                print("Instálala con: pip install pymongo")
                return # Salir si no se puede importar
            # --- Fin Bloque CORREGIDO ---

            connection_string = kwargs.get('db_connection_string', 'mongodb://localhost:27017/')
            db_name = kwargs.get('db_name', 'mi_base_de_datos')
            collection_name = kwargs.get('collection_name', 'transacciones_limpias')
            try:
                client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
                client.admin.command('ping') # Verificar conexión
                db = client[db_name]
                collection = db[collection_name]
                df_copy = df.copy()
                # Convertir Timestamps a datetime estándar para MongoDB
                for col in df_copy.select_dtypes(include=['datetime64[ns]']).columns:
                    df_copy[col] = df_copy[col].dt.to_pydatetime()
                data_dict = df_copy.to_dict("records")
                collection.drop() # Borrar colección existente
                if data_dict: # Insertar solo si hay datos
                    collection.insert_many(data_dict)
                    print(f"Datos cargados exitosamente a MongoDB '{db_name}.{collection_name}'.")
                else:
                    print("No hay datos para insertar en MongoDB.")
                client.close()
            except ConnectionFailure:
                print(f"Error: No se pudo conectar a MongoDB en {connection_string}. Asegúrate que el servidor esté corriendo.")
            except Exception as mongo_e:
                 print(f"Error durante la carga a MongoDB: {mongo_e}")
        else:
            print(f"Error: Formato de carga '{target_format}' no soportado.")
    except Exception as e:
        print(f"Error durante la carga a {target_format}: {e}")

# --- Ejecución del Pipeline Completo ---
if __name__ == "__main__":
    raw_df = extract_data('datos_desordenados.csv')
    cleaned_df = apply_transformations(raw_df)
    if cleaned_df is not None and not cleaned_df.empty:
        print("\nOrdenando datos por fecha antes de guardar...")
        cleaned_df.sort_values(by='fecha', inplace=True)
        load_data(cleaned_df, target_format='csv', file_path='datos_limpios.csv')
        load_data(cleaned_df, target_format='excel', file_path='datos_limpios.xlsx')
        # print("\nIntentando cargar a SQLite..."); load_data(cleaned_df, target_format='sql', db_connection_string='sqlite:///mi_base_etl.db', table_name='ventas_consolidadas')
        # print("\nIntentando cargar a MongoDB..."); load_data(cleaned_df, target_format='mongodb', db_connection_string='mongodb://localhost:27017/', db_name='etl_db', collection_name='ventas_consolidadas')
    else:
        print("\nPipeline finalizado, pero no se generaron datos limpios para cargar.")