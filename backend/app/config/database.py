"""
Capa de Infraestructura: Configuración de la persistencia de datos (MySQL).
Aísla los detalles técnicos de la conexión a la base de datos del resto del sistema.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cadena de conexión a MySQL local
# Formato: mysql+pymysql://usuario:password@localhost:3306/nombre_bd
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/campus360"

# Motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM (Entity mapping)
Base = declarative_base()

def get_db():
    """
    Inyección de Dependencia (DIP): Provee una sesión de base de datos aislada 
    por cada petición HTTP y garantiza la liberación de recursos al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
