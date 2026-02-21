from sqlalchemy.orm import Session
from app.domain.models import Estado

def inicializar_estados(db: Session):
    """
    Verifica si los estados base existen. Si no, los crea.
    Esto es el 'Seeder' de nuestra base de datos.
    """
    estados_base = ["PENDIENTE", "POR_APROBAR", "APROBADO", "OBSERVADO", "RECHAZADO"]
    
    # Revisamos si ya hay algún estado en la base de datos
    cantidad_actual = db.query(Estado).count()
    
    if cantidad_actual == 0:
        print("Creando estados iniciales en la base de datos...")
        for nombre_estado in estados_base:
            nuevo_estado = Estado(tipoEstado=nombre_estado)
            db.add(nuevo_estado)
        
        # Confirmamos los cambios en MySQL
        db.commit()
        print("¡Estados creados exitosamente!")
    else:
        print("Los estados ya estaban inicializados.")