from lectorFor12 import *
from redactoresMensajeFor12N import *  
from redactorMensajesConPrevias import *

def ejecutar_redactor():
    while True:
        print("\n" + "="*40)
        print("REDACTOR DE MENSAJES FOR12")
        print("="*40)
        
        # 1. Selección del archivo (Movemos esto aquí para que pida un archivo nuevo cada vez)
        resultado_tipo = tipoFor12d()
        
        # Validamos si se seleccionó un archivo o se canceló
        if resultado_tipo is None or resultado_tipo[1] is None:
            print("No se seleccionó ningún archivo.")
        else:
            conPrevias, Documento = resultado_tipo
            
            # 2. Solicitud de datos
            cdc = input("Por favor introduzca el CDC del ticket: ")

            # 3. Procesamiento
            if conPrevias:
                redactorFor12dActividadesPrevias(Documento, cdc)
            else:
                redactorFor12dNormal(Documento, cdc)
            
            print("\nProceso finalizado con éxito.")

        # 4. Pregunta de continuidad
        continuar = input("\n¿Desea redactar los mensajes de otro plan de trabajo? (s/n): ").lower()
        if continuar != 's':
            print("Cerrando el programa...")
            break

if __name__ == "__main__":
    ejecutar_redactor()