import pywhatkit
import threading
import time
# Función para enviar mensajes a dos números al mismo tiempo
# Números de destino
numero = "+584163451313"
numero_destino2 = "+584163429227"

# Mensaje a enviar
mensaje = "CONSUMO"
# Cantidad de mensajes a enviar
cantidad_mensajes = 10

# Bucle para enviar múltiples mensajes
for i in range(cantidad_mensajes):
    # Crear un hilo para enviar mensajes simultáneamente
   pywhatkit.sendwhatmsg(numero, mensaje, 0, 0)
   time.sleep(1)