from .utils import *
from .lector_web import for12Data, conActividadesPrevias, detectar_tipo_web

def generar_mensajes_normal(libro, cdc):
    [actividades, generales] = for12Data(libro)
    if not actividades: return "Error: No se encontraron actividades."
    
    horaInicio = extraer_hora_texto(actividades[0].get("FECHA Y HORA DE INICIO", ""))
    
    def messageGenerico(actividad):
        responsable = str(actividad['RESPONSABLE']).split('tlf')[0].split('Telf')[0].strip()
        return f"\n\n{get_saludo()}, dando continuidad con la For12D, se solicita al personal de la {responsable} ejecutar las siguientes actividades:\n\n\t{actividad['ACTIVIDAD']}\n"

    res = f"{get_saludo()}\n\nSe da Inicio al siguiente Trabajo\n\nTicket *CDC# {cdc}*\n\n*Nombre:* {generales['name']}\n*Hora inicio:* {horaInicio}\n\n*Afectación:* N/A\n\n*Justificación:*\n{generales['justify']}\n\n*Responsable:*\n{generales['owner']}\n\n"

    for i in range(len(actividades)):
        if 0 < i < len(actividades) - 1:
            if actividades[i]['RESPONSABLE'] == actividades[i-1]['RESPONSABLE']:
                res += f"\t{actividades[i]['ACTIVIDAD']}\n\n"
            else:
                res += messageGenerico(actividades[i])
            
            if (i + 1 < len(actividades)) and (actividades[i+1]['RESPONSABLE'] != actividades[i]['RESPONSABLE']):
                res += f"\nAgradezco el envío de evidencias.\n\n" + "-"*40 + "\n"

    res += f"\n\n{get_saludo()}\n\nSe da Fin al Trabajo *CDC# {cdc}*\n*Resultado:* OK\n*Justificación:* Actividades completadas.\n*Responsable:* {generales['owner']}"
    return res

def generar_mensajes_previas(libro, cdc):
    [ventana, previas, generales] = conActividadesPrevias(libro)
    res = "--- ACTIVIDADES PREVIAS ---\n"
    
    for i in range(len(previas)):
        responsable = str(previas[i]['RESPONSABLE']).split('Telf')[0].strip()
        if i == 0 or previas[i]['RESPONSABLE'] != previas[i-1]['RESPONSABLE']:
            res += f"\n{get_saludo()}, se solicita a {responsable}:\n\t{previas[i]['ACTIVIDAD']}\n"
        else:
            res += f"\t{previas[i]['ACTIVIDAD']}\n"

    res += "\n\n--- ACTIVIDADES VENTANA ---\n"
    res += generar_mensajes_normal(libro, cdc)
    return res