import os
import io
import traceback
from flask import Flask, request, render_template, send_file, jsonify
import openpyxl
from utils.lector_web import detectar_tipo_web, conActividadesPrevias, for12Data
from utils.redactores import redactorFor12dNormal, redactorFor12dActividadesPrevias, generar_redaccion_estructurada
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


@app.route('/api/redactar', methods=['POST'])
@app.route('/api', methods=['POST'])
def api_redactar():
    """
    Endpoint API híbrido:
    - Permite recibir multipart/form-data con archivo Excel ('file') y parámetros ('cdc', etc.).
    - Permite recibir application/json con datos estructurados ('cdc', 'generales', 'actividades', 'previas').
    - Procesa en memoria sin guardar en disco.
    - Devuelve JSON con el resultado unificado y el desglose estructurado.
    """
    try:
        cdc = "000000"
        generales = {}
        actividades = []
        previas = []
        tipo = "normal"

        # Caso 1: Archivo Excel subido vía multipart/form-data
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            in_memory = io.BytesIO(file.read())
            libro = openpyxl.load_workbook(in_memory, data_only=True)
            
            tiene_previas = detectar_tipo_web(libro)
            if tiene_previas:
                actividades, previas, generales = conActividadesPrevias(libro)
                tipo = "con_actividades_previas"
            else:
                actividades, generales = for12Data(libro)
                previas = []
                tipo = "normal"
            
            # CDC desde el form-data si existe
            if request.form.get('cdc'):
                cdc = request.form.get('cdc', '').strip() or cdc

            # Overrides opcionales desde form-data
            if request.form.get('name'):
                generales['name'] = request.form.get('name').strip()
            if request.form.get('justify'):
                generales['justify'] = request.form.get('justify').strip()
            if request.form.get('owner'):
                generales['owner'] = request.form.get('owner').strip()
                
            # O si se incluye un JSON complementario en un campo 'data' del form-data
            if request.form.get('data'):
                try:
                    import json
                    json_override = json.loads(request.form.get('data'))
                    if isinstance(json_override, dict):
                        if json_override.get('cdc'):
                            cdc = str(json_override.get('cdc')).strip()
                        if json_override.get('generales'):
                            generales.update(json_override.get('generales'))
                        if json_override.get('actividades'):
                            actividades = json_override.get('actividades')
                        if json_override.get('previas'):
                            previas = json_override.get('previas')
                except Exception as json_err:
                    print(f"[WARN] No se pudo parsear el campo 'data' JSON: {json_err}")

        # Caso 2: Petición enviada como application/json
        elif request.is_json or (request.content_type and 'application/json' in request.content_type):
            body = request.get_json(silent=True) or {}
            cdc = str(body.get('cdc', '000000')).strip()
            generales = body.get('generales')
            if not generales or not isinstance(generales, dict):
                generales = {
                    "name": body.get("name") or body.get("nombre") or body.get("trabajo"),
                    "justify": body.get("justify") or body.get("justificacion"),
                    "owner": body.get("owner") or body.get("responsable")
                }
            actividades = body.get('actividades') or body.get('ventana') or []
            previas = body.get('previas') or body.get('actividades_previas') or []
            tipo = "con_actividades_previas" if previas else "normal"

        # Caso 3: Form-data sin archivo, pero con campos de texto / json
        elif request.form:
            cdc = request.form.get('cdc', '000000').strip()
            generales = {
                "name": request.form.get('name') or request.form.get('nombre'),
                "justify": request.form.get('justify') or request.form.get('justificacion'),
                "owner": request.form.get('owner') or request.form.get('responsable')
            }
            if request.form.get('data'):
                import json
                try:
                    parsed = json.loads(request.form.get('data'))
                    if isinstance(parsed, dict):
                        actividades = parsed.get('actividades') or []
                        previas = parsed.get('previas') or []
                except Exception:
                    pass
        else:
            return jsonify({
                "status": "error",
                "message": "No se recibieron datos válidos. Debe enviar un archivo Excel (multipart/form-data) o un payload JSON con 'actividades' y 'generales'."
            }), 400

        if not actividades:
            return jsonify({
                "status": "error",
                "message": "No se encontraron actividades de ventana para procesar."
            }), 400

        # Procesar la redacción en memoria
        redaccion = generar_redaccion_estructurada(
            generales=generales,
            actividades=actividades,
            previas=previas,
            cdc=cdc
        )

        return jsonify({
            "status": "success",
            "tipo": "con_actividades_previas" if previas else "normal",
            "cdc": cdc,
            "datos_extraidos": {
                "generales": redaccion["generales"],
                "actividades": redaccion["actividades"],
                "previas": redaccion["previas"]
            },
            "resultado_texto": redaccion["resultado_texto"],
            "mensajes": redaccion["desglose"]
        }), 200

    except Exception as e:
        print("[ERROR] Error en /api/redactar:")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    print("\nIniciando servidor Redactor de Mensajes FOR12 en http://localhost:5000")
    print("Monitoreando solicitudes y errores en tiempo real...\n")
    app.run(debug=True, port=5000)