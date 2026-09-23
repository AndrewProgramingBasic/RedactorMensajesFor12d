import os
import sys
import traceback
import openpyxl

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from utils.lector_web import detectar_tipo_web
    from utils.redactores import redactorFor12dNormal, redactorFor12dActividadesPrevias
    from utils.utils import obtener_datos_generales, limpiar_nombre_archivo
except ImportError:
    from lector_web import detectar_tipo_web
    from redactores import redactorFor12dNormal, redactorFor12dActividadesPrevias
    from utils import obtener_datos_generales, limpiar_nombre_archivo

def main():
    print("=" * 60)
    print("      REDACTOR DE MENSAJES FOR12 (MODO CONSOLA)")
    print("=" * 60)
    
    # Directorios estándar
    dir_for12 = os.path.join(ROOT_DIR, "FOR12")
    dir_cdc = os.path.join(ROOT_DIR, "CDC")
    os.makedirs(dir_cdc, exist_ok=True)
    
    archivos_disponibles = []
    if os.path.exists(dir_for12):
        archivos_disponibles = [f for f in os.listdir(dir_for12) if f.lower().endswith('.xlsx')]
        
    archivo_a_procesar = None
    if archivos_disponibles:
        print("\nArchivos encontrados en la carpeta FOR12:")
        for idx, nombre in enumerate(archivos_disponibles, 1):
            print(f"  [{idx}] {nombre}")
        print(f"  [0] Introducir ruta manual")
        
        eleccion = input("\nSeleccione el número del archivo (o Enter para el primero): ").strip()
        if eleccion == "" or eleccion == "1":
            archivo_a_procesar = os.path.join(dir_for12, archivos_disponibles[0])
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(archivos_disponibles):
            archivo_a_procesar = os.path.join(dir_for12, archivos_disponibles[int(eleccion) - 1])
            
    if not archivo_a_procesar:
        ruta_manual = input("\nPor favor, introduzca la ruta completa del archivo Excel (.xlsx): ").strip('\"\' ')
        if not os.path.exists(ruta_manual):
            print(f"[ERROR] El archivo '{ruta_manual}' no existe.")
            return
        archivo_a_procesar = ruta_manual
        
    cdc = input("Por favor introduzca el número de CDC del ticket: ").strip()
    if not cdc:
        cdc = "000000"
        
    print(f"\n[INFO] Cargando libro: {os.path.basename(archivo_a_procesar)}")
    try:
        libro = openpyxl.load_workbook(archivo_a_procesar, data_only=True)
        tiene_previas = detectar_tipo_web(libro)
        generales = obtener_datos_generales(libro)
        
        print(f"[INFO] Tipo detectado: {'Con actividades previas' if tiene_previas else 'Normal (sin previas)'}")
        print(f"[INFO] Nombre de la actividad: {generales.get('name')}")
        print(f"[INFO] Responsable: {generales.get('owner')}")
        
        if tiene_previas:
            resultado = redactorFor12dActividadesPrevias(libro, cdc)
        else:
            resultado = redactorFor12dNormal(libro, cdc)
            
        nombre_f = f"{cdc}_{limpiar_nombre_archivo(generales['name'])}.txt"
        ruta_salida = os.path.join(dir_cdc, nombre_f)
        with open(ruta_salida, "w", encoding="utf-8-sig") as f:
            f.write(resultado)
            
        ruta_salida_txt = os.path.join(ROOT_DIR, "salida.txt")
        with open(ruta_salida_txt, "w", encoding="utf-8-sig") as f:
            f.write(resultado)
            
        print("\n" + "=" * 60)
        print(f"¡ÉXITO! Mensajes generados correctamente.")
        print(f"Archivo guardado en: {ruta_salida}")
        print(f"Copia guardada en:   {ruta_salida_txt}")
        print("=" * 60)

    except Exception as e:
        print("\n" + "!" * 60)
        print(f"[ERROR CRÍTICO DURANTE EL PROCESAMIENTO]")
        traceback.print_exc()
        print("!" * 60)

if __name__ == "__main__":
    main()

