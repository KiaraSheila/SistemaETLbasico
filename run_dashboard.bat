@echo off
echo Activando entorno virtual...

:: Verifica si el script de activación existe
IF NOT EXIST ".\venv\Scripts\activate.bat" (
    echo ERROR: No se encuentra el script de activacion en .\venv\Scripts\activate.bat
    echo Asegurate de haber creado el entorno virtual correctamente.
    pause
    exit /b 1
)

:: Activa el entorno virtual
call .\venv\Scripts\activate.bat

echo Entorno virtual activado. Lanzando dashboard...

:: Verifica si el script del dashboard existe
IF NOT EXIST "dashboard.py" (
    echo ERROR: No se encuentra el archivo dashboard.py
    pause
    exit /b 1
)

:: Ejecuta Streamlit
streamlit run dashboard.py

echo.
echo El dashboard se ha lanzado. Puedes cerrar esta ventana cuando termines.
:: 'pause' es opcional, mantiene la ventana abierta al final
:: pause