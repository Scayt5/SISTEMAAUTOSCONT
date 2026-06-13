import psycopg2

print("=== INICIANDO PRUEBA DE CONEXIÓN ===")

try:
    # Intentamos conectarnos a la base de datos en Docker
    conexion = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="matriculas_alpr",
        user="admin",
        password="root"
    )

    # Si logramos entrar, pedimos la versión del servidor para confirmar
    cursor = conexion.cursor()
    cursor.execute("SELECT version();")
    version_db = cursor.fetchone()

    print("¡ÉXITO! Conexión perfecta a la base de datos.")
    print(f"Servidor detectado: {version_db[0]}")

    # Cerramos la puerta al salir
    cursor.close()
    conexion.close()

except Exception as error:
    print("🚨 ERROR: No se pudo conectar a la base de datos.")
    print("Detalle del error:", error)