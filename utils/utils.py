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

def limpiar_campos(lista_campos):
    """Filtra y elimina los valores None de la lista de encabezados"""
    return [campo for campo in lista_campos if campo is not None]

def eliminar_vacios(rows):
    """Elimina diccionarios vacíos o filas que no tengan datos reales"""
    return [row for row in rows if row and any(v is not None for v in row.values())]

def obtener_datos_generales(libro):
    """Extrae el nombre y la justificación de la hoja 'Datos Generales'"""
    datos = {}
    try:
        hoja_gen = libro['Datos Generales']
        acum1 = 1
        area = ""
        for fila in hoja_gen.iter_rows():
            # Usamos str() para evitar errores si el valor es None o Int
            if acum1 == 11:
                valor_area = fila[4].value
                area = str(valor_area) if valor_area else ""
            
            if acum1 == 17:
                datos["name"] = fila[0].value
                
            if acum1 == 20:
                datos["justify"] = fila[0].value
                
            if acum1 == 25:
                # Convertimos a str cada celda para evitar el error de concatenación
                nombre = str(fila[0].value) if fila[0].value else ""
                telefono = str(fila[3].value) if fila[3].value else ""
                datos["owner"] = nombre + " // " + telefono + " // "
                
            acum1 += 1
            
        # Unimos el área al owner (verificando que owner exista)
        if "owner" in datos:
            datos["owner"] += area
        else:
            datos["owner"] = "No definido"

    except Exception as e:
        print(f"Error al leer Datos Generales: {e}")
        # IMPORTANTE: Incluir 'owner' aquí para evitar KeyError
        datos = {
            "name": "No encontrado", 
            "justify": "No encontrado", 
            "owner": "No encontrado"
        }
    return datos
