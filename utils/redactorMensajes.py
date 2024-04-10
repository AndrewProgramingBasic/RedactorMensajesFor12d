from lectorFor12 import *
from redactoresMensajeFor12N import *  
from redactorMensajesConPrevias import *

# Obtener datos de la función for12Data
[conPrevias,Documento]=tipoFor12d()
cdc = input("Por favor introduzca el cdc del ticket de la for12d: ")
if(conPrevias):
    redactorFor12dActividadesPrevias(Documento,cdc)
else:
    redactorFor12dNormal(Documento,cdc)
# Obtener hora de inicio y fin de las actividades


