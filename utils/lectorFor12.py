import openpyxl
from tkinter import filedialog
import tkinter as tk

def for12Data():
    # Crear una instancia de la ventana Tkinter y ocultarla
    root = tk.Tk()
    root.withdraw()

    # Abrir el diálogo de selección de archivo Excel
    nombre_libro = filedialog.askopenfilename()

    # Lista para almacenar los nombres de los campos
    nameCampos = []
    # Lista para almacenar los datos de las filas
    rows = []
    # Diccionario para almacenar los datos generales
    datosGenerales = {}

    try:
        # Cargar el libro de trabajo Excel
        libro = openpyxl.load_workbook(nombre_libro)
        # Seleccionar la hoja 'Plan de trabajo'
        hoja = libro['Plan de trabajo']
        numCelda = 1

        # Iterar sobre las filas de la hoja 'Plan de trabajo'
        for fila in hoja.iter_rows():
            if numCelda == 5:
                # Almacenar los nombres de los campos en la lista nameCampos
                for celda in fila:
                    nameCampos.append(celda.value)
            elif numCelda >= 7:
                numCelda = 0
                diccionario = {}
                # Crear un diccionario para almacenar los datos de cada fila
                contador=1
                for celda in fila:
                    if(contador==1 and celda.value==None):
                        numCelda+=1
                        break
                    if(contador==1):
                        pass
                    diccionario[nameCampos[numCelda]] = celda.value
                    numCelda += 1
                    contador+=1
                rows.append(diccionario)
            numCelda += 1

        # Seleccionar la hoja 'Datos Generales'
        hoja = libro['Datos Generales']
        numCelda = 1
        acum1 = 1

        # Iterar sobre las filas de la hoja 'Datos Generales'
        for fila in hoja.iter_rows():
            if acum1 == 17:
                # Almacenar el nombre en el diccionario datosGenerales
                for celda in fila:
                    datosGenerales["name"] = celda.value
                    break
            if acum1 == 20:
                # Almacenar la justificación en el diccionario datosGenerales
                for celda in fila:
                    datosGenerales["justify"] = celda.value
                    break
            acum1 += 1

        # Devolver las listas de datos y el diccionario de datos generales


        return [eliminar_vacios(rows), datosGenerales]
    except:
        # Manejar el caso en que el archivo no se encuentre
        print(f"Error inesperado, al leer el archivo")
        exit()

def conActividadesPrevias():
        # Crear una instancia de la ventana Tkinter y ocultarla
    root = tk.Tk()
    root.withdraw()

    # Abrir el diálogo de selección de archivo Excel
    nombre_libro = filedialog.askopenfilename()

    # Lista para almacenar los nombres de los campos
    nameCampos = []
    # Lista para almacenar los datos de las filas
    rows = []
    # Diccionario para almacenar los datos generales
    datosGenerales = {}


    # Cargar el libro de trabajo Excel
    libro = openpyxl.load_workbook(nombre_libro)
    # Seleccionar la hoja 'Plan de trabajo'
    hoja = libro['Plan de trabajo']
    numCelda = 1
    breakear = False
    numFila=1
    contBool = 0
    # Iterar sobre las filas de la hoja 'Plan de trabajo'
    for fila in hoja.iter_rows():
        numFila+=1
        if breakear:
            break
        if numCelda == 5:
            # Almacenar los nombres de los campos en la lista nameCampos
            for celda in fila:
                nameCampos.append(celda.value)
                print(celda.value)
        elif numCelda >= 8:
            numCelda = 0
            diccionario = {}
            # Crear un diccionario para almacenar los datos de cada fila
            contador=1
            for celda in fila:
                if(contador==1 and celda.value==None):
                    numCelda+=1
                    if contBool == 0:
                        breakear = True
                        contBool += 1
                    break
                if(contador==1):
                    pass
                if nameCampos[numCelda] == "FECHA Y HORA FIN":
                    pass
                    
                diccionario[nameCampos[numCelda]] = celda.value
                numCelda += 1
                contador+=1
            rows.append(diccionario)
        numCelda += 1
    actividadesVentana(numFila, libro, nameCampos)
    # Seleccionar la hoja 'Datos Generales'
    hoja = libro['Datos Generales']
    numCelda = 1
    acum1 = 1

    # Iterar sobre las filas de la hoja 'Datos Generales'
    for fila in hoja.iter_rows():
        if acum1 == 17:
            # Almacenar el nombre en el diccionario datosGenerales
            for celda in fila:
                datosGenerales["name"] = celda.value
                break
        if acum1 == 20:
            # Almacenar la justificación en el diccionario datosGenerales
            for celda in fila:
                datosGenerales["justify"] = celda.value
                break
        acum1 += 1

    # Devolver las listas de datos y el diccionario de datos generales


    return [eliminar_vacios(rows), datosGenerales]

def eliminar_vacios(rows):
    formateados=[]
    for row in rows:
        if(row):
            formateados.append(row)
    return(formateados)

def actividadesVentana(numFila, archivo, nameCampos):
    # Lista para almacenar los datos de las filas
    rows = []

    
    # Seleccionar la hoja 'Plan de trabajo'
    hoja = archivo['Plan de trabajo']
    numCelda = 1
    # Iterar sobre las filas de la hoja 'Plan de trabajo'
    for fila in hoja.iter_rows():
        if numCelda >= numFila:

            numCelda = 0

            diccionario = {}
            # Crear un diccionario para almacenar los datos de cada fila
            contador=1
            for celda in fila:
                if(contador==2 and celda.value==None):
                    numCelda+=1
                    break
                if(contador==1):
                    pass
                diccionario[nameCampos[numCelda]] = celda.value
                numCelda += 1
                contador+=1
            rows.append(diccionario)
        numCelda += 1


    # Devolver las listas de datos y el diccionario de datos generales


    return [eliminar_vacios(rows)]
