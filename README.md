# 🚗 Sistema ALPR - Control de Acceso Vehicular con IA

Este proyecto es una aplicación Full-Stack de Reconocimiento Automático de Matrículas. Utiliza **YOLOv8 Nano** para la detección inteligente de vehículos, **EasyOCR** para la extracción de texto, **FastAPI** para el servidor backend, y **PostgreSQL** en Docker para la persistencia de datos.

---

## 🛠️ 1. Prerrequisitos (Entorno VS Code)

Antes de iniciar, asegúrate de tener instalado:
* **Python** (3.11, 3.12 o 3.13)
* **Docker Desktop** (Debe estar abierto y corriendo en segundo plano)
* **Extensiones de VS Code recomendadas:**
    * `Python` (Microsoft)
    * `Live Server` (Ritwick Dey) - *Para abrir el frontend fácilmente*

---

## 🚀 2. Guía de Despliegue (Paso a Paso)

Abre una terminal integrada en VS Code (`Ctrl` + `ñ` o `` Ctrl` + ` ` ``) asegurándote de estar en la carpeta raíz del proyecto, y sigue estos pasos en orden:

### Paso A: Levantar la Base de Datos
Inicia el contenedor de PostgreSQL aislado.
```bash
docker compose up -d

# 1. Crear el entorno
python -m venv venv

# 2. Activar el entorno (Depende de tu terminal)
# -> Si usas Windows (PowerShell/CMD):
.\venv\Scripts\activate
# -> Si usas Linux, WSL o Git Bash:
source venv/bin/activate
(Sabrás que funcionó si ves un (venv) al inicio de tu línea de comandos).

Paso C: Instalar Dependencias
Instala todas las librerías de IA, visión y servidores web exactas del proyecto.

Bash
pip install -r requirements.txt


Paso D: Encender el Servidor Backend
Inicia la API que se encarga de procesar las imágenes con la red neuronal.

Bash
uvicorn main:app --reload


