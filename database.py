from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

# 1. El "puente" hacia tu contenedor PostgreSQL
URL_DB = "postgresql://admin:root@127.0.0.1:5432/matriculas_alpr"
motor = create_engine(URL_DB)

# 2. La clase base de SQLAlchemy
Base = declarative_base()

# 3. El diseño arquitectónico de nuestra tabla
class RegistroPlaca(Base):
    __tablename__ = "registro_placas"

    id = Column(Integer, primary_key=True, index=True)
    placa_texto = Column(String(20), nullable=False)   # La matrícula leída (Ej: ABC-123)
    confianza_ia = Column(Float)                       # Qué tan segura está la IA (Ej: 98.5%)
    ruta_imagen = Column(String(255))                  # Dónde guardaremos la foto del auto
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now()) # Hora automática

# 4. Orden de ejecución para construir la tabla
if __name__ == "__main__":
    print("=== CONSTRUYENDO LA ESTRUCTURA DE LA BASE DE DATOS ===")
    # Esta línea revisa qué tablas faltan y las crea dentro de PostgreSQL
    Base.metadata.create_all(bind=motor)
    print("¡Tabla 'registro_placas' creada exitosamente y lista para recibir datos!")