"""
Capa de Infraestructura: Repositorios (Repository Pattern).
Abstrae las consultas SQL y la persistencia del ORM. Centraliza las operaciones
de la base de datos y garantiza la Integridad Transaccional (propiedades ACID).
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.domain.schemas import DerivacionInput

from app.domain.models import Solicitud, Estado, HistorialDecision, LogAuditoria
from app.domain.enums import EstadoSolicitud

from app.services.solicitud_factory import SolicitudFactory
from app.services.sla_strategy import SlaStrategyResolver

def crear_solicitud(db: Session, tipo_tramite: str, solicitante: str):
    """
    Persiste una nueva solicitud integrando Inversión de Dependencias (DIP).
    Recibe la estrategia resuelta para no violar el principio Abierto/Cerrado (OCP).
    """
    estado_inicial = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.PENDIENTE).first()
    
    if not estado_inicial:
        raise Exception("Estados no inicializados en BD.")

    estrategia_seleccionada = SlaStrategyResolver.resolver(tipo_tramite)

    nueva_solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite=tipo_tramite,
        solicitante=solicitante,
        estado_inicial_id=estado_inicial.idEstado,
        estrategia=estrategia_seleccionada
    )
    
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    
    return nueva_solicitud


def listar_solicitudes_por_aprobar(db: Session):
    """Obtiene la colección de trámites listos para el dictamen del Aprobador."""
    estado_por_aprobar = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.POR_APROBAR).first()
    return db.query(Solicitud).filter(Solicitud.estado_id == estado_por_aprobar.idEstado).all()


def actualizar_estado(db: Session, solicitud_id: int, nuevo_estado_str: str, comentario: str):
    """
    Ejecuta el dictamen final. Garantiza la Integridad Transaccional al actualizar 
    la entidad, el historial y la auditoría en una única transacción atómica.
    """
    solicitud = db.query(Solicitud).filter(Solicitud.idSolicitud == solicitud_id).first()
    if not solicitud:
        return None

    nuevo_estado = db.query(Estado).filter(Estado.tipoEstado == nuevo_estado_str).first()
    if not nuevo_estado:
        raise Exception("El estado proporcionado no existe en el catálogo.")

    solicitud.estado_id = nuevo_estado.idEstado

    nuevo_historial = HistorialDecision(
        solicitud_id=solicitud.idSolicitud,
        usuario_id="Aprobador_Logueado", 
        accion=f"Dictamen: {nuevo_estado_str}",
        comentario=comentario,
        fecha=datetime.now()
    )
    db.add(nuevo_historial)

    nuevo_log = LogAuditoria(
        usuario="Aprobador_Logueado", 
        endpoint=f"POST /api/v1/approvals/{solicitud_id}/verdict",
        timestamp=datetime.now()
    )
    db.add(nuevo_log)

    db.commit()
    db.refresh(solicitud)
    
    return solicitud


def derivar_solicitud(db: Session, solicitud_id: int, payload: DerivacionInput):
    """
    Transición técnica (RN-06). Bifurca el flujo del Secretario hacia Jefatura 
    (Camino Feliz) o devuelve la solicitud al alumno (Flujo Alterno).
    """
    solicitud = db.query(Solicitud).filter(Solicitud.idSolicitud == solicitud_id).first()
    if not solicitud:
        return None

    estado_pendiente = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.PENDIENTE).first()
    
    if solicitud.estado_id != estado_pendiente.idEstado:
        raise Exception("Conflicto: Solo se pueden evaluar solicitudes en estado PENDIENTE.")

    if payload.checklist_valido:
        nuevo_estado_str = EstadoSolicitud.POR_APROBAR
        accion_log = "Derivación a Jefatura"
        comentario_final = "Revisión técnica conforme."
    else:
        nuevo_estado_str = EstadoSolicitud.OBSERVADO
        accion_log = "Observación en Revisión Técnica"
        comentario_final = payload.comentario

    nuevo_estado = db.query(Estado).filter(Estado.tipoEstado == nuevo_estado_str).first()
    solicitud.estado_id = nuevo_estado.idEstado

    nuevo_historial = HistorialDecision(
        solicitud_id=solicitud.idSolicitud,
        usuario_id="Secretario_Logueado",
        accion=accion_log,
        comentario=comentario_final,
        fecha=datetime.now()
    )
    db.add(nuevo_historial)
    
    nuevo_log = LogAuditoria(
        usuario="Secretario_Logueado",
        endpoint=f"POST /api/v1/workflow/{solicitud_id}/escalate",
        timestamp=datetime.now()
    )
    db.add(nuevo_log)

    db.commit()
    db.refresh(solicitud)
    return solicitud


def consultar_historial(db: Session):
    """Filtra y retorna únicamente los trámites que alcanzaron estados resolutivos."""
    estados_finales = [EstadoSolicitud.APROBADO, EstadoSolicitud.RECHAZADO, EstadoSolicitud.OBSERVADO]
    estados_db = db.query(Estado).filter(Estado.tipoEstado.in_(estados_finales)).all()
    ids_estados = [e.idEstado for e in estados_db]
    
    return db.query(Solicitud).filter(Solicitud.estado_id.in_(ids_estados)).all()


def obtener_detalle(db: Session, solicitud_id: int):
    """Recupera la entidad raíz (Aggregate Root) con todas sus relaciones resueltas."""
    return db.query(Solicitud).filter(Solicitud.idSolicitud == solicitud_id).first()