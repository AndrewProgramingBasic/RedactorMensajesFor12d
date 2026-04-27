from flask import Flask, request, render_template, send_file
import openpyxl
import io
from utils.lector_web import detectar_tipo_web
from utils.redactores import redactorFor12dNormal, redactorFor12dActividadesPrevias
from utils.utils import obtener_datos_generales, limpiar_nombre_archivo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No hay archivo"
        
        file = request.files['file']
        cdc_number = request.form.get('cdc', '000000')
        
        if file and file.filename != '':
            # Cargamos el libro
            libro = openpyxl.load_workbook(file, data_only=True)
            
            # Detectamos tipo y obtenemos datos generales para el nombre del archivo
            tiene_previas = detectar_tipo_web(libro)
            generales = obtener_datos_generales(libro)
            
            # Generamos el contenido del texto
            if tiene_previas:
                resultado_texto = redactorFor12dActividadesPrevias(libro, cdc_number)
            else:
                resultado_texto = redactorFor12dNormal(libro, cdc_number)
            
            # --- LÓGICA DE DESCARGA ---
            # Creamos el nombre del archivo tal como lo tenías antes
            nombre_f = f"{cdc_number}_{limpiar_nombre_archivo(generales['name'])}.txt"
            
            # Convertimos el string a bytes usando UTF-8 con BOM (sig) para compatibilidad con Windows
            buffer = io.BytesIO()
            buffer.write(resultado_texto.encode('utf-8-sig'))
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=nombre_f,
                mimetype='text/plain'
            )

    return render_template('index.html', resultado=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)