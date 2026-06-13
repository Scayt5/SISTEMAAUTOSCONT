from sqlalchemy.orm import Session
from database import motor, RegistroPlaca

print("=== INICIANDO PRUEBA DE ESCRITURA EN POSTGRESQL ===")

# Abrimos una sesión de trabajo con la base de datos
with Session(motor) as sesion:

    # 1. Simulamos el resultado que nos entregaría la IA (OpenCV)
    nueva_placa = RegistroPlaca(
        placa_texto="XYZ-987",
        confianza_ia=95.5,
        ruta_imagen="/imagenes/auto_capturado_01.jpg"
    )

    # 2. Guardamos la información en la tabla de PostgreSQL
    sesion.add(nueva_placa)
    sesion.commit() # ¡El commit es lo que hace que el guardado sea permanente!
    print("✅ ¡Placa falsa guardada exitosamente!")

    # 3. Para estar 100% seguros, leemos los datos directamente desde la base de datos
    print("\n--- LEYENDO REGISTROS GUARDADOS ---")
    registros = sesion.query(RegistroPlaca).all()

    for registro in registros:
        print(f"ID: {registro.id} | Placa: {registro.placa_texto} | "
              f"Confianza: {registro.confianza_ia}% | Fecha: {registro.fecha_registro}")

print("\n¡Prueba completada! La bóveda funciona a la perfección.")