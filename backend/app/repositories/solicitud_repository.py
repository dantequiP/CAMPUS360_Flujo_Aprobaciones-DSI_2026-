from sqlalchemy.orm import Session
from datetime import datetime

from app.domain.models import Solicitud, Estado
from app.domain.enums import EstadoSolicitud
from app.services.solicitud_factory import SolicitudFactory

def crear_solicitud(db: Session, tipo_tramite: str, solicitante: str):
    """Crea una solicitud delegando el ensamblaje y SLA al Patrón Factory."""
    
    # Usamos el Enum para evitar Magic Strings
    estado_inicial = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.POR_APROBAR).first()
    
    if not estado_inicial:
        raise Exception("Estados no inicializados en BD.")

    # ¡LA MAGIA DE LOS PATRONES!
    # Delegamos la lógica de instanciación y el cálculo matemático (Strategy) a la Fábrica
    nueva_solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite=tipo_tramite,
        solicitante=solicitante,
        estado_inicial_id=estado_inicial.idEstado
    )
    
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    
    return nueva_solicitud


def listar_solicitudes_por_aprobar(db: Session):
    """Obtiene todas las solicitudes que están en la bandeja del Aprobador."""
    
    # Aplicamos el Enum aquí también para evitar cadenas quemadas
    estado_por_aprobar = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.POR_APROBAR).first()
    
    return db.query(Solicitud).filter(Solicitud.estado_id == estado_por_aprobar.idEstado).all()


def actualizar_estado(db: Session, solicitud_id: int, nuevo_estado_str: str, comentario: str):
    """Actualiza el estado de una solicitud y guarda el log de auditoría."""
    
    # 1. Buscamos la solicitud en MySQL
    solicitud = db.query(Solicitud).filter(Solicitud.idSolicitud == solicitud_id).first()
    if not solicitud:
        return None # No se encontró

    # 2. Buscamos el ID del nuevo estado ("APROBADO", "RECHAZADO", etc.)
    nuevo_estado = db.query(Estado).filter(Estado.tipoEstado == nuevo_estado_str).first()
    if not nuevo_estado:
        raise Exception("El estado proporcionado no existe en el catálogo.")

    # 3. Actualizamos la llave foránea
    solicitud.estado_id = nuevo_estado.idEstado

    # 4. Agregamos el movimiento al historial (Auditoría)
    evento = {
        "fecha": str(datetime.now()), 
        "accion": f"Dictamen: {nuevo_estado_str}", 
        "comentario": comentario
    }
    
    # Clonamos la lista actual, agregamos el evento y reasignamos (necesario en JSON de SQLAlchemy)
    historial_actual = list(solicitud.historial) if solicitud.historial else []
    historial_actual.append(evento)
    solicitud.historial = historial_actual

    # 5. Guardamos los cambios físicos en la base de datos
    db.commit()
    db.refresh(solicitud)
    
    return solicitud