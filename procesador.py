import os
import numpy as np
import SimpleITK as sitk
from stl import mesh
from skimage import measure
from scipy.ndimage import binary_closing

def procesar_dicom_y_generar_stl(dicom_file_list, carpeta_exportacion, id_sesion):
    """
    Procesa una lista de archivos DICOM y genera un STL usando segmentación por umbral,
    cerradura morfológica y marching cubes, como en la GUI original.
    """

    # Leer imágenes DICOM desde la lista
    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(dicom_file_list)
    image = reader.Execute()
    array = sitk.GetArrayFromImage(image)

    # Segmentación por umbral (fijo, como en el original)
    umbral_bajo = 300
    umbral_alto = 4000
    segmentacion = np.logical_and(array >= umbral_bajo, array <= umbral_alto)

    # Aplicar cerradura morfológica (igual que en GUI original)
    segmentacion = binary_closing(segmentacion, structure=np.ones((3, 3, 3)))

    # Generar malla con Marching Cubes
    verts, faces, _, _ = measure.marching_cubes(segmentacion.astype(np.float32), level=0.5)

    # Crear archivo STL
    stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = verts[f[j], :]

    nombre_archivo = f"scan_and_care_{id_sesion}.stl"
    ruta_salida = os.path.join(carpeta_exportacion, nombre_archivo)
    stl_mesh.save(ruta_salida)

    return ruta_salida
