# Usamos una versión ligera de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Evitamos que Python genere archivos .pyc y permitimos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalamos dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos (que movimos a la raíz)
COPY requirements.txt .

# Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto (app.py, templates, utils, etc.)
COPY . .

# Exponemos el puerto de Flask
EXPOSE 5000

# Ejecutamos con Gunicorn
# -w 4: Cuatro procesos trabajando en paralelo
# -b 0.0.0.0:5000: Escuchando en todas las IPs del contenedor
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]