# app.py
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import zipfile
import uuid
import secrets
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
from procesador import procesar_dicom_y_generar_stl

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
EXPORT_FOLDER = os.path.join(os.getcwd(), 'exports')
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    imagen_preview = None
    ruta_stl = None

    if request.method == 'POST':
        archivo = request.files.get('archivo')

        if not archivo:
            flash('No se seleccionó ningún archivo.')
            return redirect(request.url)

        if archivo.filename.endswith('.zip'):
            id_sesion = str(uuid.uuid4())
            ruta_zip = os.path.join(UPLOAD_FOLDER, f"{id_sesion}.zip")
            archivo.save(ruta_zip)

            carpeta_dicom = os.path.join(UPLOAD_FOLDER, id_sesion)
            os.makedirs(carpeta_dicom, exist_ok=True)

            with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                zip_ref.extractall(carpeta_dicom)

            dicom_paths = []
            for root, _, files in os.walk(carpeta_dicom):
                for file in files:
                    if file.lower().endswith(".dcm"):
                        dicom_paths.append(os.path.join(root, file))

            if not dicom_paths:
                flash('No se encontraron archivos DICOM en el ZIP.')
                return redirect(request.url)

            try:
                reader = sitk.ImageSeriesReader()
                reader.SetFileNames(dicom_paths)
                image = reader.Execute()
                array = sitk.GetArrayFromImage(image)

                central_slice = array[array.shape[0] // 2, :, :]
                plt.imshow(central_slice, cmap='gray')
                preview_name = f"preview_{id_sesion}.png"
                ruta_preview = os.path.join(STATIC_FOLDER, preview_name)
                plt.axis('off')
                plt.savefig(ruta_preview, bbox_inches='tight', pad_inches=0)
                plt.close()
                imagen_preview = preview_name

                ruta_stl = procesar_dicom_y_generar_stl(dicom_paths, EXPORT_FOLDER, id_sesion)

            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)

        else:
            flash('El archivo debe estar en formato .zip con imágenes DICOM dentro.')
            return redirect(request.url)

    return render_template('index.html', imagen_preview=imagen_preview, ruta_stl=ruta_stl)

@app.route('/descargar/<filename>')
def descargar(filename):
    ruta = os.path.join(EXPORT_FOLDER, filename)
    if os.path.exists(ruta):
        return send_file(ruta, as_attachment=True)
    else:
        flash('Archivo STL no encontrado.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
