from lectorFor12 import *
from utils import *

def redactorFor12dActividadesPrevias(archivo, cdc, ejecutante):
    [actividades, previas, generales] = conActividadesPrevias(archivo)
    print("")
    print(actividades)
    print("")
    print(previas)
    print("")
    horaInicio = extraer_hora_texto(actividades[0]["FECHA Y HORA DE INICIO"])

    def eliminar_texto_despues_frase(texto, frase):
        pos = str(texto).find(frase)
        return texto[:pos] if pos != -1 else texto

    def messageGenerico(actividad, saludo):
        responsable = eliminar_texto_despues_frase(actividad['RESPONSABLE'], 'tlf')
        return f"\n\n{saludo}, {mensajeContinuidadRandom()} se solicita al personal de la {responsable} ejecutar las siguientes actividades:\n\n\t{actividad['ACTIVIDAD']}\n"

    todosLosMensajes = "ACTIVIDADES PREVIAS\n" + "="*60 + "\n\n"
    
    for i in range(len(previas)):
        if i == 0 or previas[i]['RESPONSABLE'] != previas[i-1]['RESPONSABLE']:
            todosLosMensajes += messageGenerico(previas[i], get_saludo(previas[i]))
        else:
            todosLosMensajes += f"\t{previas[i]['ACTIVIDAD']}\n\n"
        
        if i + 1 < len(previas) and previas[i+1]['RESPONSABLE'] != previas[i]['RESPONSABLE']:
            todosLosMensajes += f"\n{mensajeFinalRandom()}\n\n" + "-"*60 + "\n"

    todosLosMensajes += "\n\nACTIVIDADES VENTANA\n" + "="*60 + "\n"
    
    # Bloque de Inicio de Ventana Homologado
    messageInitial = (
        f"{get_saludo(actividades[0])}\n\n"
        f"Se da Inicio al siguiente Trabajo\n\n\n"
        f"Ticket \n*CDC# {cdc}*\n\n"
        f"*Nombre del Trabajo:*\n\n {generales['name']}  \n"
        f"*Hora de inicio:* {horaInicio}\n\n"
        f"*Servicios / Aplicaciones Afectadas*\n\n\n N/A\n\n"
        f"*Justificación:*\n {generales['justify']}\n\n"
        f"*Responsable de Trabajo:*\n\n {ejecutante}\n\n"
    )
    
    todosLosMensajes += messageInitial
    todosLosMensajes += "-" * 60 + "\n\n\n"

    for i in range(len(actividades)):
        if i == 0 or actividades[i]['RESPONSABLE'] != actividades[i-1]['RESPONSABLE']:
            todosLosMensajes += messageGenerico(actividades[i], get_saludo(actividades[i]))
        else:
            todosLosMensajes += f"\t{actividades[i]['ACTIVIDAD']}\n\n"
            
        if i + 1 < len(actividades) and actividades[i+1]['RESPONSABLE'] != actividades[i]['RESPONSABLE']:
            todosLosMensajes += f"\n{mensajeFinalRandom()}\n\n" + "-"*60 + "\n"

    # Mensaje Final
    todosLosMensajes += f"\n\n\n{get_saludo(actividades[-1])}\n\nSe da Fin al siguiente Trabajo\n\n\n Ticket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales['name']}   \n\n*Resultado:*\n\n\nOK\n\n*Justificación:*\n{mensajeFinActividades() + generales['name']}\n\n*Responsable de Trabajo:*\n\n {ejecutante}\n\n"

    nombre_f = f"{cdc} {limpiar_nombre_archivo(generales['name'])}.txt"
    guardar_en_txt(todosLosMensajes, os.path.join(".", "CDC", nombre_f))
    guardar_en_txt(todosLosMensajes, os.path.join(".", "salida.txt"))
    print(f"¡Éxito! Archivo con previas generado")