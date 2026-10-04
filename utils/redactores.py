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


from datetime import datetime, time, date

def _serializar_valor(v):
    if v is None:
        return ""
    if isinstance(v, time):
        return v.strftime("%H:%M:%S")
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    return v


def normalizar_actividad(act):
    if not isinstance(act, dict):
        return {
            "ACTIVIDAD": str(act).strip(),
            "RESPONSABLE": "Responsable",
            "FECHA Y HORA DE INICIO": ""
        }
    norm = {}
    for k, v in act.items():
        val = _serializar_valor(v)
        k_upper = str(k).strip().upper()
        if "ACTIVIDAD" in k_upper or k_upper in ["NAME", "DESCRIPCION", "TEXTO", "TASK"]:
            norm["ACTIVIDAD"] = str(val).strip()
        elif "RESPONSABLE" in k_upper or k_upper in ["OWNER", "AREA", "ENCARGADO"]:
            norm["RESPONSABLE"] = str(val).strip()
        elif "INICIO" in k_upper or "FECHA" in k_upper or "HORA" in k_upper:
            norm["FECHA Y HORA DE INICIO"] = str(val).strip()
        else:
            norm[k] = val
            
    if "ACTIVIDAD" not in norm:
        norm["ACTIVIDAD"] = str(act.get("actividad") or act.get("name") or act.get("text") or "").strip()
    if "RESPONSABLE" not in norm:
        norm["RESPONSABLE"] = str(act.get("responsable") or act.get("owner") or "").strip()
    if "FECHA Y HORA DE INICIO" not in norm:
        val_f = act.get("fecha_inicio") or act.get("hora_inicio") or act.get("fecha") or ""
        norm["FECHA Y HORA DE INICIO"] = str(_serializar_valor(val_f)).strip()
        
    return norm


def normalizar_generales(gen):
    if not isinstance(gen, dict):
        return {"name": "Sin_Nombre", "justify": "N/A", "owner": "No definido"}
    name = (gen.get("name") or gen.get("nombre") or gen.get("descripcion") or 
            gen.get("trabajo") or gen.get("nombre_trabajo") or "Sin_Nombre")
    justify = (gen.get("justify") or gen.get("justificacion") or 
               gen.get("justificacion_cambio") or "N/A")
    owner = (gen.get("owner") or gen.get("responsable") or 
             gen.get("responsable_ejecutante") or "No definido")
    return {"name": str(name).strip(), "justify": str(justify).strip(), "owner": str(owner).strip()}


def _crear_dict_bloque(responsable, saludo, actividades):
    if not actividades:
        return {"responsable": responsable, "saludo": saludo, "actividades": [], "mensaje": ""}
    primera = actividades[0]
    texto = f"\n\n{saludo}, {mensajeContinuidadRandom()} se solicita al personal de la {responsable} ejecutar las siguientes actividades:\n\n\t{primera}\n"
    for a in actividades[1:]:
        texto += f"\t{a}\n\n"
    texto += f"\n{mensajeFinalRandom()}\n\n"
    return {
        "responsable": responsable,
        "saludo": saludo,
        "actividades": actividades,
        "mensaje": texto
    }


def construir_bloques_actividades(lista_actividades):
    if not lista_actividades:
        return []

    bloques = []
    current_resp = None
    current_saludo = None
    current_acts = []
    
    for act in lista_actividades:
        resp_raw = str(act.get('RESPONSABLE', ''))
        resp = eliminar_texto_despues_frase(resp_raw, 'tlf')
        resp = eliminar_texto_despues_frase(resp, 'Telf').strip()
        act_text = str(act.get('ACTIVIDAD', '')).strip()
        saludo = get_saludo(act)
        
        if current_resp is None or resp != current_resp:
            if current_acts:
                bloques.append(_crear_dict_bloque(current_resp, current_saludo, current_acts))
            current_resp = resp
            current_saludo = saludo
            current_acts = [act_text] if act_text else []
        else:
            if act_text:
                current_acts.append(act_text)
                
    if current_acts:
        bloques.append(_crear_dict_bloque(current_resp, current_saludo, current_acts))
        
    return bloques


def generar_redaccion_estructurada(generales, actividades, previas=None, cdc="000000"):
    generales = normalizar_generales(generales)
    actividades = [normalizar_actividad(a) for a in (actividades or [])]
    previas = [normalizar_actividad(p) for p in (previas or [])]
    
    if not actividades:
        raise ValueError("No se encontraron actividades de ventana.")
        
    cdc = str(cdc).strip() or "000000"
    
    saludo_inicial = get_saludo(actividades[0])
    horaInicio = extraer_hora_texto(actividades[0].get("FECHA Y HORA DE INICIO", ""))
    
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
    
    bloques_previas = construir_bloques_actividades(previas) if previas else []
    
    actividades_proceso = actividades[:-1] if len(actividades) > 1 else actividades
    bloques_actividades = construir_bloques_actividades(actividades_proceso)
    
    messageFinal = (
        f"\n\n\n{get_saludo(actividades[-1])}\n\n"
        f"Se da Fin al siguiente Trabajo\n\n\n"
        f"Ticket \n*CDC# {cdc}*\n\n"
        f"*Nombre del Trabajo:*\n\n {generales.get('name', '')}    \n\n"
        f"*Resultado:*\n\n\nOK\n\n"
        f"*Justificación:*\n{mensajeFinActividades() + str(generales.get('name', ''))}\n\n"
        f"*Responsable de Trabajo:*\n\n {generales.get('owner', '')}\n\n"
    )
    
    resultado_texto = ""
    if bloques_previas:
        resultado_texto += "ACTIVIDADES PREVIAS\n" + "="*60 + "\n"
        for b in bloques_previas:
            resultado_texto += b["mensaje"] + "-"*60 + "\n"
        resultado_texto += "\n\nACTIVIDADES VENTANA\n" + "="*60 + "\n\n"
        
    resultado_texto += messageInitial + "-"*60 + "\n"
    for b in bloques_actividades:
        resultado_texto += b["mensaje"] + "-"*60 + "\n"
    resultado_texto += messageFinal
    
    return {
        "resultado_texto": resultado_texto,
        "desglose": {
            "mensaje_inicial": messageInitial,
            "mensajes_previas": bloques_previas,
            "mensajes_actividades": bloques_actividades,
            "mensaje_final": messageFinal
        },
        "generales": generales,
        "actividades": actividades,
        "previas": previas
    }