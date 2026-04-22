@echo off
set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

echo Activando entorno virtual...
:: Activamos el venv desde la raíz
call venv\Scripts\activate

echo Ejecutando script...
:: Ejecutamos el archivo que está dentro de utils
python utils\redactorMensajes.py

echo.
echo Proceso finalizado.
pause
