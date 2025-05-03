# 🧠 Scan&Care – Segmentación Médica y Generación de STL 3D

**Scan&Care** es una plataforma web desarrollada en Flask que permite a profesionales de la salud y estudiantes:

- Subir estudios médicos DICOM comprimidos en `.zip`
- Ajustar umbrales para segmentación personalizada o elegir presets
- Visualizar un corte axial del estudio
- Descargar el modelo 3D segmentado en formato `.stl`

---

## 🌐 Versión en línea
> Puedes visitar la plataforma desplegada en:  
https://scan-and-care.onrender.com *(ejemplo – se activa tras despliegue)*

---

## 🚀 ¿Cómo usar?

1. Accede al sitio.
2. Sube un archivo `.zip` con imágenes médicas DICOM.
3. Selecciona el tipo de tejido a segmentar:
   - Hueso
   - Tejido blando
   - Contraste
   - Personalizado (con umbral manual)
4. Observa el corte axial central.
5. Haz clic en "Procesar y Descargar STL".

---

## 🧪 Funcionalidades

- [x] Subida de archivo `.zip` con múltiples DICOM
- [x] Segmentación por umbral ajustable
- [x] Presets de tejido (óseo, blando, contraste)
- [x] Vista previa del corte axial
- [x] Exportación automática a archivo STL
- [ ] Visualización 3D del STL *(futuro)*
- [ ] Navegación por slices DICOM *(futuro)*

---

## 🛠️ Instalación local

```bash
git clone https://github.com/tu_usuario/scan-and-care.git
cd scan-and-care
pip install -r requirements.txt
python app.py
