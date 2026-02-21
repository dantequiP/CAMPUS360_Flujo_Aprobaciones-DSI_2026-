from app.services.solicitud_factory import SolicitudFactory
from sqlalchemy.orm import Session
from app.domain.models import Solicitud, Estado
from datetime import datetime, timedelta
from app.domain.enums import EstadoSolicitud

def crear_solicitud(db: Session, tipo_tramite: str, solicitante: str):
    # SMELL 4: Magic String ("POR_APROBAR")
    estado_inicial = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.POR_APROBAR).first()
    
    # SMELL 2 y 3: Lógica dispersa y condicionales (Sin Strategy ni Factory)
    if "Extemporánea" in tipo_tramite:
        fecha_limite = datetime.now() + timedelta(hours=24)
        prioridad_calc = "ALTA"
    else:
        fecha_limite = datetime.now() + timedelta(hours=72)
        prioridad_calc = "NORMAL"

    nueva_solicitud = Solicitud(
        tipoSolicitud=tipo_tramite,
        solicitante=solicitante,
        slaObjetivo=fecha_limite,
        prioridad=prioridad_calc,
        estado_id=estado_inicial.idEstado,
        adjuntos=[],
        historial=[]
    )
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud

def listar_solicitudes_por_aprobar(db: Session):
    """Obtiene todas las solicitudes que están en la bandeja del Aprobador."""
    estado_por_aprobar = db.query(Estado).filter(Estado.tipoEstado == "POR_APROBAR").first()
    
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