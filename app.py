import os
import io
import traceback
from flask import Flask, request, render_template, send_file
import openpyxl
from utils.lector_web import detectar_tipo_web
from utils.redactores import redactorFor12dNormal, redactorFor12dActividadesPrevias
from utils.utils import obtener_datos_generales, limpiar_nombre_archivo

app = Flask(__name__)
app.secret_key = "redactor_for12d_secret_key"
# Versión actualizada con formato limpio de actividades y despedidas


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("\n[ERROR] No se recibió ningún archivo en la petición.")
            return render_template('index.html', error="No se seleccionó ningún archivo.")
        
        file = request.files['file']
        cdc_number = request.form.get('cdc', '000000').strip()
        
        if not file or file.filename == '':
            print("\n[ERROR] El archivo seleccionado está vacío.")
            return render_template('index.html', error="Debes seleccionar un archivo Excel (.xlsx).")
            
        print("\n" + "="*60)
        print(f"[INFO] Procesando archivo: {file.filename}")
        print(f"[INFO] Número CDC: {cdc_number}")
        
        try:
            # Cargamos el libro directamente desde la memoria
            in_memory = io.BytesIO(file.read())
            libro = openpyxl.load_workbook(in_memory, data_only=True)
            
            # Detectamos tipo y datos generales
            tiene_previas = detectar_tipo_web(libro)
            generales = obtener_datos_generales(libro)
            
            print(f"[INFO] Tipo detectado: {'Con actividades previas' if tiene_previas else 'Normal (sin previas)'}")
            print(f"[INFO] Nombre del trabajo: {generales.get('name')}")
            print(f"[INFO] Responsable: {generales.get('owner')}")
            
            # Generamos el contenido del texto
            if tiene_previas:
                resultado_texto = redactorFor12dActividadesPrevias(libro, cdc_number)
            else:
                resultado_texto = redactorFor12dNormal(libro, cdc_number)
            
            if not resultado_texto or resultado_texto.strip() == "Error":
                raise ValueError("No se pudieron generar los mensajes (resultado vacío o con error).")
            
            # Guardamos copia en la carpeta CDC
            os.makedirs("CDC", exist_ok=True)
            nombre_f = f"{cdc_number}_{limpiar_nombre_archivo(generales['name'])}.txt"
            ruta_cdc = os.path.join("CDC", nombre_f)
            with open(ruta_cdc, "w", encoding="utf-8-sig") as f_cdc:
                f_cdc.write(resultado_texto)
            print(f"[INFO] Copia guardada localmente en: {ruta_cdc}")
            
            # Guardamos copia en salida.txt
            try:
                with open("salida.txt", "w", encoding="utf-8-sig") as f_salida:
                    f_salida.write(resultado_texto)
            except Exception as e:
                print(f"[WARN] No se pudo escribir en salida.txt: {e}")
            
            print(f"[ÉXITO] Archivo generado correctamente: {nombre_f}")
            print("="*60 + "\n")
            
            # Retornamos el archivo para descarga directa
            buffer = io.BytesIO()
            buffer.write(resultado_texto.encode('utf-8-sig'))
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=nombre_f,
                mimetype='text/plain'
            )

        except Exception as e:
            print("\n" + "!"*60)
            print(f"[ERROR CRÍTICO] Falló el procesamiento del archivo '{file.filename}':")
            traceback.print_exc()
            print("!"*60 + "\n")
            return render_template('index.html', error=f"Ocurrió un error al procesar el archivo: {str(e)}")

    return render_template('index.html', error=None)

if __name__ == '__main__':
    print("\nIniciando servidor Redactor de Mensajes FOR12 en http://localhost:5000")
    print("Monitoreando solicitudes y errores en tiempo real...\n")
    app.run(debug=True, port=5000)