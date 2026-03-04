"""
Capa de Infraestructura: Inicializador de Datos (Seeder).
Automatiza la creación de los registros paramétricos indispensables 
para el funcionamiento de la Máquina de Estados (RN-06).
"""
from sqlalchemy.orm import Session
from app.domain.models import Estado

def inicializar_estados(db: Session):
    """
    Puebla la tabla 'estados' con el catálogo oficial si se encuentra vacía.
    Garantiza que el motor de base de datos esté listo para transaccionar solicitudes.
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