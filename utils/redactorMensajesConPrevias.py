from lectorFor12 import *
import random
def redactorFor12dActividadesPrevias(archivo,cdc):
    [actividades, generales] = conActividadesPrevias(archivo)
    horaInicio = str(actividades[0]["FECHA Y HORA DE INICIO"])[11:]
    # Función para obtener el saludo según la hora
    def get_saludo(actividad):
        #print(actividad["FECHA Y HORA DE INICIO"])
        print(type(actividad["FECHA Y HORA DE INICIO"]))
        hora = int(((str(actividad["FECHA Y HORA DE INICIO"]))[11:])[:2])
        if hora >= 6 and hora <= 11:
            return "Buenos Días"
        elif hora >= 12 and hora <= 17:
            return "Buenas Tardes"
        return "Buenas Noches"

    def notificacionFinal():
        return "Se notifica que se realizaron de manera exitosa todas las actividades reflajadas en la For12d, logrando así la correcta ejecución del trabajo " + generales['name']

    horaFin = str(actividades[-1]["FECHA Y HORA DE INICIO"])[11:]

    # Mensaje inicial del trabajo
    messageInitial = f"{get_saludo(actividades[0])}\n\nSe le da Inicio al siguiente Trabajo\n\n\nTicket \n CDC# {cdc}\n\nNombre del Trabajo:\n\n {generales['name']}  \nHora de inicio: {horaInicio}\n\n Servicios / Aplicaciones Afectadas\n\n\n [LLENE AQUI LAS APLICACIONES AFECTADAS]\n\n Justificación:\n {generales['justify']}\n\nResponsable de Trabajo:\n\n [INGRESE AQUI LOS DATOS DEL EJECUTANTE]\n\n"

    # Mensaje final del trabajo
    messageFinal = f"\n\n\n{get_saludo(actividades[-1])}\n\nSe le da Fin al siguiente Trabajo\n\n\n Ticket \n CDC# {cdc}\n\nNombre del Trabajo:\n\n {generales['name']}   \n\n Resultado\n\n\n OK\n\n Justificación:\n {notificacionFinal()}\n\nResponsable de Trabajo:\n\n [INGRESE AQUI LOS DATOS DEL EJECUTANTE]\n\n"


        
    # Función para eliminar texto después de una frase específica
    def eliminar_texto_despues_frase(texto, frase):
        posicion_fin_frase = texto.find(frase)
        if posicion_fin_frase != -1:
            texto_modificado = texto[:posicion_fin_frase]
        else:
            texto_modificado = texto
        return texto_modificado

    # Función para obtener un mensaje final aleatorio
    def mensajeFinalRandom():
        messages = ["Agradezco sus comentarios y solicito el envío de las evidencias.",
                    "Quedo atento a sus comentarios y a la recepción de las evidencias.",
                    "Estaré pendiente de sus comentarios y del envío de las evidencias.",
                    "Esperaré su pronta respuesta con sus comentarios y las evidencias.",
                    "Quedo a la espera de sus comentarios y el envío de las evidencias.",
                    "Me encuentro atento a sus comentarios y al envío de las evidencias.",
                    "Agradezco de antemano sus comentarios y el envío de las evidencias."]
        return messages[random.randint(0, len(messages) - 1)]

    # Función para obtener un mensaje de continuidad aleatorio
    def mensajeContinuidadRandom():
        messages = ["dando continuidad con la For12D,",
                    "continuando con el trabajo,",
                    "siguiendo con las actividades, ",
                    "prosiguiendo con lo estipulado en la For12D, ",
                    "prosiguiendo con el trabajo, ",
                    "siguiendo con el trabajo, ",
                    "prosiguiendo con las actividades, "]
        return messages[random.randint(0, len(messages) - 1)]

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

        if i > 0 and i < len(actividades):
            if actividades[i]['RESPONSABLE'] == actividadesPast:
                todosLosMensajes+=f"\t{actividades[i]['ACTIVIDAD']}\n\n"
            else: 
                todosLosMensajes += messageGenerico(actividades[i], get_saludo(actividades[i]))
            if(actividadesNext!=actividades[i]['RESPONSABLE'] ):
                todosLosMensajes+=f"\n{mensajeFinalRandom()}\n\n"
                todosLosMensajes += "-" * 200
    todosLosMensajes += messageFinal

    # Guardar los mensajes en un archivo de texto
    guardar_en_txt(todosLosMensajes, "../salida.txt")

    print("¡Texto guardado en el archivo salida.txt!")