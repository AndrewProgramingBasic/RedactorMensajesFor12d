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
    # Intentar obtener la hora de cualquiera de los dos posibles nombres de columna
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

def limpiar_campos(lista_campos):
    return [campo for campo in lista_campos if campo is not None]

def eliminar_vacios(rows):
    return [row for row in rows if row and any(v is not None for v in row.values())]

def obtener_datos_generales(libro):
    """Extrae datos generales buscando dinámicamente por etiquetas o por índices tradicionales"""
    datos = {}
    try:
        if 'Datos Generales' not in libro.sheetnames:
            print("[ADVERTENCIA] Hoja 'Datos Generales' no encontrada.")
            return {"name": "Sin_Nombre", "justify": "N/A", "owner": "No definido"}

        hoja_gen = libro['Datos Generales']
        filas = list(hoja_gen.iter_rows(values_only=True))

        name = None
        justify = None
        owner_name = None
        owner_phone = None
        area = ""

        # Búsqueda dinámica por etiquetas
        for idx, fila in enumerate(filas):
            if not fila:
                continue
            row_str = " ".join(str(v).upper() for v in fila if v is not None)

            # Unidad ejecutante (Área)
            if "UNIDAD EJECUTANTE" in row_str:
                for next_idx in range(idx + 1, min(idx + 4, len(filas))):
                    next_fila = filas[next_idx]
                    if len(next_fila) > 4 and next_fila[4]:
                        val_col4 = str(next_fila[4]).strip()
                        if val_col4 and val_col4.upper() not in ["COORDINACIÓN", "COORDINACION"]:
                            area = val_col4
                            break

            # Descripción del cambio
            if "DESCRIPCION DEL CAMBIO" in row_str or "DESCRIPCIÓN DEL CAMBIO" in row_str:
                for next_idx in range(idx + 1, min(idx + 3, len(filas))):
                    next_fila = filas[next_idx]
                    if next_fila and next_fila[0] and str(next_fila[0]).strip():
                        name = str(next_fila[0]).strip()
                        break

            # Justificación del cambio
            if "JUSTIFICACION DEL CAMBIO" in row_str or "JUSTIFICACIÓN DEL CAMBIO" in row_str:
                for next_idx in range(idx + 1, min(idx + 3, len(filas))):
                    next_fila = filas[next_idx]
                    if next_fila and next_fila[0] and str(next_fila[0]).strip():
                        justify = str(next_fila[0]).strip()
                        break

            # Responsable Ejecutante
            if "RESPONSABLE EJECUTANTE" in row_str:
                for next_idx in range(idx + 1, min(idx + 3, len(filas))):
                    next_fila = filas[next_idx]
                    if next_fila and next_fila[0] and str(next_fila[0]).strip():
                        owner_name = str(next_fila[0]).strip()
                        if len(next_fila) > 3 and next_fila[3]:
                            owner_phone = str(next_fila[3]).strip()
                        break

        # Fallback a índices fijos por si alguna plantilla antigua no tiene los textos esperados
        acum1 = 1
        for fila in filas:
            if acum1 == 11 and not area:
                if len(fila) > 4 and fila[4]:
                    area = str(fila[4]).strip()
            if acum1 == 17 and not name:
                if fila and fila[0]:
                    name = str(fila[0]).strip()
            if acum1 == 20 and not justify:
                if fila and fila[0]:
                    justify = str(fila[0]).strip()
            if acum1 == 25 and not owner_name:
                if fila and fila[0]:
                    owner_name = str(fila[0]).strip()
                if len(fila) > 3 and fila[3] and not owner_phone:
                    owner_phone = str(fila[3]).strip()
            acum1 += 1

        datos["name"] = name if name else "Sin_Nombre"
        datos["justify"] = justify if justify else "N/A"

        owner_str = f"{owner_name or 'No definido'} // {owner_phone or 'S/T'} // "
        if area:
            owner_str += area
        datos["owner"] = owner_str

    except Exception as e:
        print(f"[ERROR] Error al leer Datos Generales: {e}")
        datos = {"name": "No encontrado", "justify": "No encontrado", "owner": "No encontrado"}
    return datos