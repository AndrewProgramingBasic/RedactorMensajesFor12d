#!/bin/bash

# Cambiar directorio a la ubicación del archivo Python
# En Linux se usa '/' en lugar de '\'
cd "./utils"

# Activar el entorno virtual
# La ruta en Linux suele ser 'bin/activate' en lugar de 'Scripts/activate'
source venv/bin/activate

# Ejecutar el archivo Python
python3 redactorMensajes.py

# (Opcional) Pausar la ejecución
# En Linux no existe 'pause', usamos 'read' para esperar un Enter
echo "Presiona Enter para salir..."
read
exit