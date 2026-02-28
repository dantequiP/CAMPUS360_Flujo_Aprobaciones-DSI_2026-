from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cadena de conexión a MySQL local
# Formato: mysql+pymysql://usuario:password@localhost:3306/nombre_bd
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/campus360"

# Motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para tus modelos
Base = declarative_base()

# Dependencia para usar en los controladores (Inyección de dependencias)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()