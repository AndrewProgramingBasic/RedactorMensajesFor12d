from lectorFor12 import *
from datetime import datetime
import random
def redactorFor12dNormal(archivo,cdc):
    
    [actividades, generales] = for12Data(archivo)

    horaInicio = str(actividades[0]["FECHA Y HORA DE INICIO"])[11:]

    # Función para obtener el saludo según la hora
    def get_saludo(actividad):
        hora = int(((str(actividad["FECHA Y HORA DE INICIO"]))[11:])[:2])
        if hora >= 6 and hora <= 11:
            return "Buenos Días"
        elif hora >= 12 and hora <= 17:
            return "Buenas Tardes"
        return "Buenas Noches"

    
    def notificacionFinal():
        return mensajeFinActividades() + generales['name']

    # Mensaje inicial del trabajo
    messageInitial = f"{get_saludo(actividades[0])}\n\nSe da Inicio al siguiente Trabajo\n\n\nTicket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales['name']}  \n*Hora de inicio:* {horaInicio}\n\n*Servicios / Aplicaciones Afectadas*\n\n\n N/A\n\n*Justificación:*\n {generales['justify']}\n\n*Responsable de Trabajo:*\n\n [INGRESE AQUI LOS DATOS DEL EJECUTANTE]\n\n"

    # Mensaje final del trabajo
    messageFinal = f"\n\n\n{get_saludo(actividades[-1])}\n\nSe da Fin al siguiente Trabajo\n\n\n Ticket \n*CDC# {cdc}*\n\n*Nombre del Trabajo:*\n\n {generales['name']}   \n\n*Resultado:*\n\n\nOK\n\n*Justificación:*\n{notificacionFinal()}\n\n*Responsable de Trabajo:*\n\n [INGRESE AQUI LOS DATOS DEL EJECUTANTE]\n\n"

        
    # Función para eliminar texto después de una frase específica
    def eliminar_texto_despues_frase(texto, frase):
        posicion_fin_frase = texto.find(frase)
        if posicion_fin_frase != -1:
            texto_modificado = texto[:posicion_fin_frase]
        else:
            texto_modificado = texto
        return texto_modificado


    # Función para generar un mensaje genérico
    def messageGenerico(actividad, saludo):
        message = f"\n\n{saludo}, {mensajeContinuidadRandom()} se solicita al personal de la {eliminar_texto_despues_frase(actividad['RESPONSABLE'], 'tlf')} ejecutar las siguientes actividades:\n\n\t{actividad['ACTIVIDAD']}\n"
        return message

    # Función para guardar el texto en un archivo
    def guardar_en_txt(texto, nombre_archivo):
        with open(nombre_archivo, "w") as archivo:
            archivo.write(texto)

    # Generar todos los mensajes
    todosLosMensajes = messageInitial
    for i in range(len(actividades)):
        actividadesPast=actividades[i -1]['RESPONSABLE']
        actividadesNext= "asofdhafapio"
        if ((i +1) < len(actividades)):
            actividadesNext= actividades[i +1]['RESPONSABLE']

        if i > 0 and i < len(actividades)-1:
            if actividades[i]['RESPONSABLE'] == actividadesPast:
                todosLosMensajes+=f"\t{actividades[i]['ACTIVIDAD']}\n\n"
            else: 
                todosLosMensajes += messageGenerico(actividades[i], get_saludo(actividades[i]))
            if(actividadesNext!=actividades[i]['RESPONSABLE'] ):
                todosLosMensajes+=f"\n{mensajeFinalRandom()}\n\n"
                todosLosMensajes += "-" * 200
    todosLosMensajes += messageFinal

    # Guardar los mensajes en un archivo de texto
    guardar_en_txt(todosLosMensajes, "../"+cdc+".txt")

    print("¡Texto guardado en el archivo "+cdc+".txt!")