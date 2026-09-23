import traceback
from .lector_web import *
from .utils import *

def eliminar_texto_despues_frase(texto, frase):
    pos = str(texto).find(frase)
    return texto[:pos] if pos != -1 else str(texto)

def redactorFor12dNormal(archivo, cdc):
    [actividades, generales] = for12Data(archivo)
    if not actividades:
        print("[ERROR] No se encontraron actividades en el archivo.")
        raise ValueError("No se encontraron actividades en la hoja 'Plan de trabajo'.")
    
    saludo_inicial = get_saludo(actividades[0])
    horaInicio = extraer_hora_texto(actividades[0].get("FECHA Y HORA DE INICIO", ""))

    def messageGenerico(actividad, saludo):
        resp_raw = str(actividad.get('RESPONSABLE', ''))
        responsable = eliminar_texto_despues_frase(resp_raw, 'tlf')
        responsable = eliminar_texto_despues_frase(responsable, 'Telf').strip()
        act_text = str(actividad.get('ACTIVIDAD', '')).strip()
        return f"\n\n{saludo}, {mensajeContinuidadRandom()} se solicita al personal de la {responsable} ejecutar las siguientes actividades:\n\n\t{act_text}\n"

    messageInitial = (
        f"{saludo_inicial}\n\n"
        f"Se da Inicio al siguiente Trabajo\n\n\n"
        f"Ticket \n*CDC# {cdc}*\n\n"
        f"*Nombre del Trabajo:*\n\n {generales.get('name', '')}  \n"
        f"*Hora de inicio:* {horaInicio}\n\n"
        f"*Servicios / Aplicaciones Afectadas*\n\n\n N/A\n\n"
        f"*Justificación:*\n {generales.get('justify', '')}\n\n"
        f"*Responsable de Trabajo:*\n\n {generales.get('owner', '')}\n\n"
    )

    # 1. Separación entre el mensaje inicial y el primer correo de actividades
    todosLosMensajes = messageInitial + "-" * 60 + "\n"

    # 2. Omitir la última actividad del bucle de mensajes (corresponde al fin de ventana)
    actividades_proceso = actividades[:-1] if len(actividades) > 1 else actividades

    for i in range(len(actividades_proceso)):
        act_text = str(actividades_proceso[i].get('ACTIVIDAD', '')).strip()
        if i == 0 or actividades_proceso[i].get('RESPONSABLE') != actividades_proceso[i-1].get('RESPONSABLE'):
            todosLosMensajes += messageGenerico(actividades_proceso[i], get_saludo(actividades_proceso[i]))
        else:
            todosLosMensajes += f"\t{act_text}\n\n"
        
        # Despedida y separación al cambiar de responsable o al finalizar la última actividad a procesar
        es_ultima = (i == len(actividades_proceso) - 1)
        cambio_resp = (not es_ultima and actividades_proceso[i+1].get('RESPONSABLE') != actividades_proceso[i].get('RESPONSABLE'))
        
        if es_ultima or cambio_resp:
            todosLosMensajes += f"\n{mensajeFinalRandom()}\n\n" + "-"*60 + "\n"
                
    todosLosMensajes += f"\n\n\n{get_saludo(actividades[-1])}\n\nSe da Fin al siguiente Trabajo\n\n\n Ticket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales.get('name', '')}    \n\n*Resultado:*\n\n\nOK\n\n*Justificación:*\n{mensajeFinActividades() + str(generales.get('name', ''))}\n\n*Responsable de Trabajo:*\n\n {generales.get('owner', '')}\n\n"
    
    return todosLosMensajes

def redactorFor12dActividadesPrevias(archivo, cdc):
    [actividades, previas, generales] = conActividadesPrevias(archivo)
    if not actividades:
        print("[ERROR] No se encontraron actividades de ventana en el archivo.")
        raise ValueError("No se encontraron actividades de ventana en la hoja 'Plan de trabajo'.")
    
    saludo_inicial = get_saludo(actividades[0])
    horaInicio = extraer_hora_texto(actividades[0].get("FECHA Y HORA DE INICIO", ""))

    def messageGenerico(actividad, saludo):
        resp_raw = str(actividad.get('RESPONSABLE', ''))
        responsable = eliminar_texto_despues_frase(resp_raw, 'tlf')
        responsable = eliminar_texto_despues_frase(responsable, 'Telf').strip()
        act_text = str(actividad.get('ACTIVIDAD', '')).strip()
        return f"\n\n{saludo}, {mensajeContinuidadRandom()} se solicita al personal de la {responsable} ejecutar las siguientes actividades:\n\n\t{act_text}\n"

    todosLosMensajes = ""
    if previas:
        todosLosMensajes += "ACTIVIDADES PREVIAS\n" + "="*60 + "\n"
        for i in range(len(previas)):
            act_text = str(previas[i].get('ACTIVIDAD', '')).strip()
            if i == 0 or previas[i].get('RESPONSABLE') != previas[i-1].get('RESPONSABLE'):
                todosLosMensajes += messageGenerico(previas[i], get_saludo(previas[i]))
            else:
                todosLosMensajes += f"\t{act_text}\n\n"
            
            # Despedida y separación al cambiar de responsable o al finalizar las previas
            es_ultima_previa = (i == len(previas) - 1)
            cambio_resp = (not es_ultima_previa and previas[i+1].get('RESPONSABLE') != previas[i].get('RESPONSABLE'))
            
            if es_ultima_previa or cambio_resp:
                todosLosMensajes += f"\n{mensajeFinalRandom()}\n\n" + "-"*60 + "\n"

        todosLosMensajes += "\n\nACTIVIDADES VENTANA\n" + "="*60 + "\n\n"
    
    messageInitial = (
        f"{saludo_inicial}\n\n"
        f"Se da Inicio al siguiente Trabajo\n\n\n"
        f"Ticket \n*CDC# {cdc}*\n\n"
        f"*Nombre del Trabajo:*\n\n {generales.get('name', '')}  \n"
        f"*Hora de inicio:* {horaInicio}\n\n"
        f"*Servicios / Aplicaciones Afectadas*\n\n\n N/A\n\n"
        f"*Justificación:*\n {generales.get('justify', '')}\n\n"
        f"*Responsable de Trabajo:*\n\n {generales.get('owner', '')}\n\n"
    )
    
    # 1. Separación entre mensaje inicial y actividades de ventana
    todosLosMensajes += messageInitial + "-" * 60 + "\n"

    # 2. Omitir la última actividad (fin de ventana)
    actividades_proceso = actividades[:-1] if len(actividades) > 1 else actividades

    for i in range(len(actividades_proceso)):
        act_text = str(actividades_proceso[i].get('ACTIVIDAD', '')).strip()
        if i == 0 or actividades_proceso[i].get('RESPONSABLE') != actividades_proceso[i-1].get('RESPONSABLE'):
            todosLosMensajes += messageGenerico(actividades_proceso[i], get_saludo(actividades_proceso[i]))
        else:
            todosLosMensajes += f"\t{act_text}\n\n"
            
        es_ultima = (i == len(actividades_proceso) - 1)
        cambio_resp = (not es_ultima and actividades_proceso[i+1].get('RESPONSABLE') != actividades_proceso[i].get('RESPONSABLE'))
        
        if es_ultima or cambio_resp:
            todosLosMensajes += f"\n{mensajeFinalRandom()}\n\n" + "-"*60 + "\n"

    todosLosMensajes += f"\n\n\n{get_saludo(actividades[-1])}\n\nSe da Fin al siguiente Trabajo\n\n\n Ticket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales.get('name', '')}    \n\n*Resultado:*\n\n\nOK\n\n*Justificación:*\n{mensajeFinActividades() + str(generales.get('name', ''))}\n\n*Responsable de Trabajo:*\n\n {generales.get('owner', '')}\n\n"

    return todosLosMensajes