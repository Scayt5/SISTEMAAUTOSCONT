import cv2
import easyocr
import shutil
import os
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import motor, Base, RegistroPlaca
from ultralytics import YOLO # <-- NUEVA IMPORTACIÓN

Base.metadata.create_all(bind=motor)

app = FastAPI(title="Sistema ALPR", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

print("⏳ Cargando motor de IA (EasyOCR)...")
lector = easyocr.Reader(['es', 'en'], gpu=False)
print("✅ Motor IA listo.")

print("⏳ Cargando Francotirador (YOLOv8 Nano)...")
detector_yolo = YOLO('yolov8n.pt') # <-- NUEVO: Se descargará automáticamente la primera vez (6MB)
print("✅ Francotirador en posición.")

# 4. Dependencia para abrir y cerrar la sesión de la base de datos de forma segura
def obtener_bd():
    bd = Session(motor)
    try:
        yield bd
    finally:
        bd.close()

# 5. Ruta de diagnóstico para verificar que el servidor responda
@app.get("/")
def leer_raiz():
    return {
        "estado": "Servidor Online",
        "mensaje": "API ALPR en funcionamiento y lista para procesar imágenes."
    }

# 6. Endpoint Principal: Recibe la foto desde el frontend, aplica IA y guarda en DB
@app.post("/procesar-placa")
async def procesar_placa(imagen: UploadFile = File(...), bd: Session = Depends(obtener_bd)):

    # Asegurar que la carpeta 'imagenes' exista
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    # A. Guardar el archivo recibido físicamente en el servidor
    ruta_guardado = f"imagenes/{imagen.filename}"
    with open(ruta_guardado, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    # B. Procesamiento de la imagen
    img_cv2 = cv2.imread(ruta_guardado)
    if img_cv2 is None:
        return {"error": "🚨 No se pudo procesar la imagen."}

    # --- NUEVO: El Francotirador actúa ---
    # YOLO busca vehículos o elementos principales en la imagen
    resultados_yolo = detector_yolo(img_cv2)
    cajas = resultados_yolo[0].boxes

    # Si YOLO encontró algo, recortamos la zona de mayor confianza
    if len(cajas) > 0:
        # Extraemos las coordenadas de la caja (x1, y1 = arriba-izq | x2, y2 = abajo-der)
        x1, y1, x2, y2 = map(int, cajas[0].xyxy[0])

        # OpenCV usa la magia de las matrices para "recortar" la foto
        img_recortada = img_cv2[y1:y2, x1:x2]
    else:
        # Si la foto es confusa y no detecta nada, usamos la imagen completa como respaldo
        img_recortada = img_cv2
    # ------------------------------------

    # Convertimos a escala de grises SOLO el recorte limpio
    grises = cv2.cvtColor(img_recortada, cv2.COLOR_BGR2GRAY)

    # C. Análisis de caracteres con EasyOCR (ahora es mucho más rápido y preciso)
    resultados = lector.readtext(grises)

    placa_detectada = ""
    confianza_promedio = 0.0

    if resultados:
        # Filtramos lecturas válidas con más del 30% de confianza
        textos = [res[1] for res in resultados if res[2] > 0.30]
        confianzas = [res[2] for res in resultados if res[2] > 0.30]

        # Unimos los fragmentos detectados en una sola cadena limpia
        placa_detectada = "".join(textos).upper().strip()
        if confianzas:
            confianza_promedio = sum(confianzas) / len(confianzas)
    else:
        placa_detectada = "NO_DETECTADA"

    # D. Persistencia de datos: Guardar el resultado en la base de datos de Docker
    # D. Persistencia de datos: Guardar el resultado en la bóveda de PostgreSQL
    nuevo_registro = RegistroPlaca(
        placa_texto=placa_detectada,
        # Envolvemos la variable en float() para limpiarla del formato NumPy
        confianza_ia=round(float(confianza_promedio) * 100, 2),
        ruta_imagen=ruta_guardado
    )
    bd.add(nuevo_registro)
    bd.commit()
    bd.refresh(nuevo_registro)

    # E. Respuesta estructurada enviada de vuelta al Frontend (index.html)
    return {
        "estado": "Éxito",
        "datos_alpr": {
            "id_bd": nuevo_registro.id,
            "matrícula": nuevo_registro.placa_texto,
            "precisión_ia": f"{nuevo_registro.confianza_ia}%",
            "archivo": nuevo_registro.ruta_imagen
        }
    }
# 7. Endpoint del Historial: Lee la bóveda y devuelve los últimos registros
@app.get("/historial")
def obtener_historial(bd: Session = Depends(obtener_bd)):
    # Buscamos en la tabla ordenando del más reciente al más antiguo (límite de 20 para no saturar)
    registros = bd.query(RegistroPlaca).order_by(RegistroPlaca.id.desc()).limit(20).all()

    # Empaquetamos la información en una lista limpia
    historial = []
    for reg in registros:
        historial.append({
            "id": reg.id,
            "placa": reg.placa_texto,
            "confianza": reg.confianza_ia,
            # Formateamos la fecha si existe, si no, ponemos "Reciente"
            "fecha": reg.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if reg.fecha_registro else "Reciente",
            "imagen": reg.ruta_imagen
        })

    return historial