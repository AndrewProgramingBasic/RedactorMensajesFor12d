import random
from .utils import *

def detectar_tipo_web(libro):
    """Restauración de tipoFor12d: detecta si el formato tiene actividades previas"""
    try:
        hoja = libro['Plan de trabajo']
        numCelda = 1
        for fila in hoja.iter_rows():
            if numCelda >= 7:
                if not isinstance(fila[0].value, int):
                    return True # Tiene previas
                else:
                    return False # Es normal
            numCelda += 1
    except:
        return False

def for12Data(libro):
    """Lectura estándar del FOR12 sin previas"""
    nameCampos = []
    rows = []
    hoja = libro['Plan de trabajo']
    numFila = 1
    campos_crudos = []

    for fila in hoja.iter_rows():
        if numFila == 5:
            campos_crudos = [celda.value for celda in fila]
            nameCampos = limpiar_campos(campos_crudos)
        elif numFila >= 7:
            if not isinstance(fila[0].value, int):
                numFila += 1
                continue
            diccionario = {}
            valores_fila = [celda.value for i, celda in enumerate(fila) 
                           if i < len(campos_crudos) and campos_crudos[i] is not None]
            for i, valor in enumerate(valores_fila):
                if i < len(nameCampos):
                    diccionario[nameCampos[i]] = valor
            if diccionario: rows.append(diccionario)
        numFila += 1
    
    return [eliminar_vacios(rows), obtener_datos_generales(libro)]

def conActividadesPrevias(libro):
    """Lógica original de split entre Previas y Ventana"""
    nameCampos = []
    rows_previas = []
    hoja = libro['Plan de trabajo']
    numFilaContador = 1
    breakear = False
    campos_originales_con_none = []

    for fila in hoja.iter_rows():
        if breakear: break
        if numFilaContador == 5:
            campos_originales_con_none = [celda.value for celda in fila]
            nameCampos = limpiar_campos(campos_originales_con_none)
        elif numFilaContador >= 8:
            try:
                if fila[0].value is None: raise ValueError
                int(fila[0].value)
            except:
                breakear = True
                break
            
            diccionario = {}
            valores_fila = [celda.value for i, celda in enumerate(fila) 
                           if i < len(campos_originales_con_none) and campos_originales_con_none[i] is not None]
            for i, valor in enumerate(valores_fila):
                if i < len(nameCampos): diccionario[nameCampos[i]] = valor
            if diccionario: rows_previas.append(diccionario)
        numFilaContador += 1

    ventanaActividades = actividadesVentana(numFilaContador, libro, nameCampos, campos_originales_con_none)
    return [ventanaActividades, eliminar_vacios(rows_previas), obtener_datos_generales(libro)]

def actividadesVentana(numFilaInicio, libro, nameCamposLimpios, camposOriginales):
    rows_ventana = []
    hoja = libro['Plan de trabajo']
    for fila in hoja.iter_rows(min_row=numFilaInicio):
        if isinstance(fila[0].value, int):
            diccionario = {}
            valores_fila = [celda.value for i, celda in enumerate(fila) 
                           if i < len(camposOriginales) and camposOriginales[i] is not None]
            for i, valor in enumerate(valores_fila):
                if i < len(nameCamposLimpios): diccionario[nameCamposLimpios[i]] = valor
            if diccionario: rows_ventana.append(diccionario)
    return eliminar_vacios(rows_ventana)

# Mensajería Aleatoria Original
def mensajeFinalRandom():
    return random.choice(["Agradezco sus comentarios y solicito el envío de las evidencias.", "Quedo atento a sus comentarios y a la recepción de las evidencias."])

def mensajeContinuidadRandom():
    return random.choice(["dando continuidad con la For12D,", "continuando con el trabajo,"])

def mensajeFinActividades():
    return random.choice(["Se confirma la ejecución exitosa de todas las actividades: ", "Se valida la correcta ejecución: "])