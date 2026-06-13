import cv2
import easyocr

print("=== INICIANDO MOTOR DE INTELIGENCIA ARTIFICIAL ===")
print("Cargando red neuronal (puede tardar unos segundos la primera vez)...")

# 1. Inicializar EasyOCR para leer en español e inglés.
# Desactivamos la GPU por ahora para evitar problemas de drivers en WSL
lector = easyocr.Reader(['es', 'en'], gpu=False)

ruta_imagen = "imagenes/placa.webp"

# 2. Leer la imagen con OpenCV
imagen = cv2.imread(ruta_imagen)

if imagen is None:
    print(f"🚨 ERROR: No se encontró la imagen. Verifica que exista en: {ruta_imagen}")
else:
    # 3. Procesamiento de imagen: Convertir a escala de grises
    # A las IA les es mucho más fácil leer bordes sin la distracción del color
    grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    print("✅ Imagen cargada y procesada correctamente por OpenCV.")

    # 4. Leer el texto con la Inteligencia Artificial
    print("⏳ Analizando caracteres con EasyOCR...")
    resultados = lector.readtext(grises)

    if not resultados:
        print("⚠️ La IA no logró detectar ningún texto en la imagen.")
    else:
        print("\n🎯 ¡LECTURA COMPLETADA!")
        print("-" * 40)
        # EasyOCR devuelve una lista con [Coordenadas, Texto, Confianza]
        for (caja, texto, confianza) in resultados:
            # Filtramos textos muy pequeños o "basura" visual exigiendo al menos 30% de confianza
            if confianza > 0.30:
                print(f"Matrícula Detectada: {texto.upper()} | Nivel de Confianza: {confianza * 100:.2f}%")
        print("-" * 40)