from lectorFor12 import *
from utils import *

def redactorFor12dNormal(archivo, cdc, ejecutante):
    [actividades, generales] = for12Data(archivo)
    horaInicio = extraer_hora_texto(actividades[0]["FECHA Y HORA DE INICIO"])

    def eliminar_texto_despues_frase(texto, frase):
        pos = str(texto).find(frase)
        return texto[:pos] if pos != -1 else texto

    def messageGenerico(actividad, saludo):
        responsable = eliminar_texto_despues_frase(actividad['RESPONSABLE'], 'tlf')
        return f"\n\n{saludo}, {mensajeContinuidadRandom()} se solicita al personal de la {responsable} ejecutar las siguientes actividades:\n\n\t{actividad['ACTIVIDAD']}\n"

    messageInitial = f"{get_saludo(actividades[0])}\n\nSe da Inicio al siguiente Trabajo\n\n\nTicket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales['name']}  \n*Hora de inicio:* {horaInicio}\n\n*Servicios / Aplicaciones Afectadas*\n\n\n N/A\n\n*Justificación:*\n {generales['justify']}\n\n*Responsable de Trabajo:*\n\n {ejecutante}\n\n"

    todosLosMensajes = messageInitial

    for i in range(len(actividades)):
        if i > 0 and i < len(actividades) - 1:
            if actividades[i]['RESPONSABLE'] == actividades[i-1]['RESPONSABLE']:
                todosLosMensajes += f"\t{actividades[i]['ACTIVIDAD']}\n\n"
            else: 
                todosLosMensajes += messageGenerico(actividades[i], get_saludo(actividades[i]))
            
            if (i + 1 < len(actividades)) and (actividades[i+1]['RESPONSABLE'] != actividades[i]['RESPONSABLE']):
                todosLosMensajes += f"\n{mensajeFinalRandom()}\n\n" + "-"*100 + "\n"
                
    todosLosMensajes += f"\n\n\n{get_saludo(actividades[-1])}\n\nSe da Fin al siguiente Trabajo\n\n\n Ticket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales['name']}   \n\n*Resultado:*\n\n\nOK\n\n*Justificación:*\n{mensajeFinActividades() + generales['name']}\n\n*Responsable de Trabajo:*\n\n {ejecutante}\n\n"
    
    nombre_f = f"{cdc} {limpiar_nombre_archivo(generales['name'])}.txt"
    guardar_en_txt(todosLosMensajes, os.path.join(".", "CDC", nombre_f))
    guardar_en_txt(todosLosMensajes, os.path.join(".", "salida.txt"))
    print(f"¡Éxito! Archivo generado")