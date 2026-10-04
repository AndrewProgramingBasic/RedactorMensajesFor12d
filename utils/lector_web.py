import random
import traceback
from .utils import *

def parse_plan_de_trabajo(libro):
    """
    Parsea dinámicamente la hoja 'Plan de trabajo' sin importar la fila exacta de inicio.
    Detecta automáticamente encabezados de 'ACTIVIDADES PREVIAS' y 'ACTIVIDAD' (ventana),
    homologando los nombres de columnas y extrayendo las filas de actividades.
    Retorna: (previas, ventana)
    """
    if 'Plan de trabajo' not in libro.sheetnames:
        print("[ERROR] No se encontró la hoja 'Plan de trabajo' en el archivo Excel.")
        return [], []

    hoja = libro['Plan de trabajo']
    rows = list(hoja.iter_rows(values_only=True))
    
    previas = []
    ventana = []
    
    current_section = "ventana"
    current_headers = []
    
    for row_idx, row in enumerate(rows, start=1):
        if not row or all(v is None for v in row):
            continue
            
        first_val = row[0]
        is_num = False
        if isinstance(first_val, int):
            is_num = True
        elif first_val is not None:
            val_clean = str(first_val).strip()
            if val_clean.isdigit():
                is_num = True

        row_str = " ".join(str(v).upper() for v in row if v is not None)

        # 1. Si es fila de actividad (comienza con número): procesar actividad inmediatamente
        if is_num:
            if current_headers:
                item = {}
                for col_idx, val in enumerate(row):
                    if col_idx < len(current_headers):
                        header_name = current_headers[col_idx]
                        if header_name:
                            item[header_name] = val
                
                # Asegurar que tenga al menos actividad o responsable
                if item.get("ACTIVIDAD") or item.get("RESPONSABLE"):
                    if current_section == "previas":
                        previas.append(item)
                    else:
                        ventana.append(item)
            continue

        # 2. Banners de sección (ej: "ACTIVIDADES PREVIAS A LA VENTANA DE CAMBIO", "ACTIVIDADES DURANTE LA VENTANA DE CAMBIO")
        if "ACTIVIDADES PREVIAS" in row_str or ("PREVIA" in row_str and "VENTANA" in row_str and "DURANTE" not in row_str):
            current_section = "previas"
            print(f"[DEBUG] Fila {row_idx}: Banner detectado para sección '{current_section}'")
            continue
        elif "ACTIVIDADES DURANTE" in row_str or "ACTIVIDADES DE VENTANA" in row_str or "ACTIVIDADES VENTANA" in row_str:
            current_section = "ventana"
            print(f"[DEBUG] Fila {row_idx}: Banner detectado para sección '{current_section}'")
            continue

        # 3. Encabezados de columnas de la tabla (N°, ACTIVIDAD, FECHA Y HORA, RESPONSABLE...)
        if "ACTIVIDAD" in row_str and any(k in row_str for k in ["FECHA", "HORA", "RESPONSABLE"]):
            if "PREVIA" in row_str:
                current_section = "previas"
            else:
                current_section = "ventana"
                
            current_headers = []
            for h in row:
                if h is None:
                    current_headers.append(None)
                else:
                    h_clean = str(h).strip().upper()
                    if "ACTIVIDAD" in h_clean:
                        current_headers.append("ACTIVIDAD")
                    elif "FECHA" in h_clean and "INICIO" in h_clean:
                        current_headers.append("FECHA Y HORA DE INICIO")
                    elif "FECHA" in h_clean and "FIN" in h_clean:
                        current_headers.append("FECHA Y HORA FIN")
                    elif "RESPONSABLE" in h_clean:
                        current_headers.append("RESPONSABLE")
                    elif "AFECTACION" in h_clean:
                        current_headers.append("APLICA AFECTACION DE SERVICIO")
                    else:
                        current_headers.append(str(h).strip())
            print(f"[DEBUG] Fila {row_idx}: Encabezado detectado para sección '{current_section}'")
            continue

    print(f"[DEBUG] Plan de trabajo procesado: {len(previas)} previas, {len(ventana)} ventana.")
    return eliminar_vacios(previas), eliminar_vacios(ventana)

def detectar_tipo_web(libro):
    """Detecta dinámicamente si el formato tiene actividades previas."""
    try:
        previas, _ = parse_plan_de_trabajo(libro)
        return len(previas) > 0
    except Exception as e:
        print(f"[ERROR] Error al detectar tipo en el Excel: {e}")
        traceback.print_exc()
        return False

def for12Data(libro):
    """Lectura para archivos FOR12 (retorna actividades de ventana y datos generales)."""
    try:
        previas, ventana = parse_plan_de_trabajo(libro)
        # Si no hubo bloque de ventana formal pero sí actividades en previas, o viceversa:
        actividades = ventana if ventana else previas
        datos_generales = obtener_datos_generales(libro)
        return [actividades, datos_generales]
    except Exception as e:
        print(f"[ERROR] Error en for12Data: {e}")
        traceback.print_exc()
        return [[], {}]

def conActividadesPrevias(libro):
    """Lectura para archivos FOR12 con actividades previas."""
    try:
        previas, ventana = parse_plan_de_trabajo(libro)
        datos_generales = obtener_datos_generales(libro)
        return [ventana, previas, datos_generales]
    except Exception as e:
        print(f"[ERROR] Error en conActividadesPrevias: {e}")
        traceback.print_exc()
        return [[], [], {}]

# Mensajería Aleatoria Original
def mensajeFinalRandom():
    return random.choice([
        "Agradezco sus comentarios y solicito el envío de las evidencias.",
        "Quedo atento a sus comentarios y a la recepción de las evidencias.",
        "Estaré pendiente de sus comentarios y del envío de las evidencias.",
        "Agradezco de antemano sus comentarios y el envío de las evidencias."
    ])

def mensajeContinuidadRandom():
    return random.choice([
        "dando continuidad con la For12D,",
        "continuando con el trabajo,",
        "siguiendo con las actividades,",
        "prosiguiendo con lo estipulado en la For12D,"
    ])

def mensajeFinActividades():
    return random.choice([
        "Se confirma la ejecución exitosa de todas las actividades: ",
        "Se valida la correcta ejecución: ",
        "Se confirma la culminación exitosa de las actividades: "
    ])