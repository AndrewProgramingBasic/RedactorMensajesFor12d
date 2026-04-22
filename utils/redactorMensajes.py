from lectorFor12 import *
from redactoresMensajeFor12N import *  
from redactorMensajesConPrevias import *

# Obtener datos de la función for12Data
[conPrevias, Documento] = tipoFor12d()

# --- NUEVAS SOLICITUDES DE DATOS ---
cdc = input("Por favor introduzca el cdc del ticket: ")
datos_ejecutante = input("Introduzca los datos del Ejecutante: ")

if(conPrevias):
    redactorFor12dActividadesPrevias(Documento, cdc, datos_ejecutante)
else:
    redactorFor12dNormal(Documento, cdc, datos_ejecutante)