from flask import Flask, render_template, request, send_file, flash
import openpyxl
import io
import os
from utils.lectorFor12 import for12Data, conActividadesPrevias, tipoFor12d_web
from redactoresMensajeFor12N import procesar_normal_web
from redactorMensajesConPrevias import procesar_previas_web

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No hay archivo"
        
        file = request.files['file']
        cdc = request.form.get('cdc')
        
        if file.filename == '':
            return "Archivo no seleccionado"

        if file and cdc:
            # Leer el archivo directamente desde la memoria (Stream)
            in_memory_file = io.BytesIO(file.read())
            libro = openpyxl.load_workbook(in_memory_file, data_only=True)
            
            # Lógica para detectar si es con previas (basado en tu tipoFor12d)
            # Adaptamos tipoFor12d para que reciba el libro ya abierto
            es_con_previas = detectar_tipo_web(libro)
            
            if es_con_previas:
                resultado_txt = procesar_previas_web(libro, cdc)
            else:
                resultado_txt = procesar_normal_web(libro, cdc)
            
            # Devolver el archivo para descarga inmediata
            mem = io.BytesIO()
            mem.write(resultado_txt.encode('utf-8-sig'))
            mem.seek(0)
            
            return send_file(
                mem,
                as_attachment=True,
                download_name=f"CDC_{cdc}.txt",
                mimetype='text/plain'
            )

    return render_template('index.html')

def detectar_tipo_web(libro):
    hoja = libro['Plan de trabajo']
    num = 1
    for fila in hoja.iter_rows():
        if num >= 7:
            return not isinstance(fila[0].value, int)
        num += 1
    return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)