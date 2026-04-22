import os
import re
from datetime import datetime, time

def extraer_hora_entero(valor):
    if isinstance(valor, (datetime, time)):
        return valor.hour
    valor_str = str(valor).strip().upper()
    match = re.search(r"(\d{1,2}):\d{2}", valor_str)
    if match:
        hora = int(match.group(1))
        if "PM" in valor_str and hora < 12: hora += 12
        elif "AM" in valor_str and hora == 12: hora = 0
        return hora
    return 0

def extraer_hora_texto(valor):
    if isinstance(valor, (datetime, time)):
        return valor.strftime("%H:%M")
    valor_str = str(valor).strip().upper()
    match = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)", valor_str)
    return match.group(1) if match else valor_str

def get_saludo(actividad):
    valor_hora = actividad.get("FECHA Y HORA DE INICIO") or actividad.get("FECHA Y HORA INICIO")
    hora = extraer_hora_entero(valor_hora)
    if 6 <= hora <= 11: return "Buenos Días"
    elif 12 <= hora <= 17: return "Buenas Tardes"
    return "Buenas Noches"

def limpiar_nombre_archivo(nombre):
    if not nombre: return "Sin_Nombre"
    limpio = str(nombre).replace("\n", " ").replace("\r", " ").strip()
    for car in r'\/:*?"<>|':
        limpio = limpio.replace(car, "")
    return limpio

def guardar_en_txt(texto, ruta_relativa):
    """Guarda en UTF-8 con BOM para que Windows reconozca los acentos perfectamente"""
    ruta_absoluta = os.path.abspath(ruta_relativa)
    directorio = os.path.dirname(ruta_absoluta)
    
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
        
    # 'utf-8-sig' añade el BOM necesario para Excel y Bloc de Notas
    with open(ruta_absoluta, "w", encoding="utf-8-sig") as f:
        f.write(texto)