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

def crear_solicitud(db: Session, tipo_tramite: str, solicitante: str, descripcion: str): 
    """
    Persiste una nueva solicitud integrando Inversión de Dependencias (DIP).
    Recibe la estrategia resuelta para no violar el principio Abierto/Cerrado (OCP).
    """
    estado_inicial = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.PENDIENTE).first()
    
    if not estado_inicial:
        raise Exception("Estados no inicializados en BD.")

    nueva_solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite=tipo_tramite,
        solicitante=solicitante,
        descripcion=descripcion,
        estado_inicial_id=estado_inicial.idEstado
    )
    
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    
    return nueva_solicitud


def listar_solicitudes_por_aprobar(db: Session):
    """Obtiene solicitudes para la bandeja general (Pendientes, Por Aprobar y Observados)."""
    
    estados_requeridos = [
        "PENDIENTE", 
        "POR_APROBAR", 
        "OBSERVADO"
    ]

    objetos_estado = db.query(Estado).filter(Estado.tipoEstado.in_(estados_requeridos)).all()
    ids_validos = [e.idEstado for e in objetos_estado]
    
    return db.query(Solicitud).filter(Solicitud.estado_id.in_(ids_validos)).all()


def actualizar_estado(db: Session, solicitud_id: int, nuevo_estado_str: str, comentario: str):
    """
    Ejecuta el dictamen final. Garantiza la Integridad Transaccional al actualizar 
    la entidad, el historial y la auditoría en una única transacción atómica.
    """
    
    # 1. Buscamos la solicitud en MySQL
    solicitud = db.query(Solicitud).filter(Solicitud.idSolicitud == solicitud_id).first()
    if not solicitud:
        return None # No se encontró

    # 2. Buscamos el ID del nuevo estado ("APROBADO", "RECHAZADO", etc.)
    nuevo_estado = db.query(Estado).filter(Estado.tipoEstado == nuevo_estado_str).first()
    if not nuevo_estado:
        raise Exception("El estado proporcionado no existe en el catálogo.")

    # 3. Actualizamos la llave foránea de la solicitud
    solicitud.estado_id = nuevo_estado.idEstado

    # 4. Insertamos en la tabla HistorialDecision (Relación 1 a N)
    nuevo_historial = HistorialDecision(
        solicitud_id=solicitud.idSolicitud,
        usuario_id="Aprobador_Logueado", # Dato simulado para el MVP
        accion=f"Dictamen: {nuevo_estado_str}",
        comentario=comentario,
        fecha=datetime.now()
    )
    db.add(nuevo_historial)

    # 5. Insertamos en la tabla LogAuditoria (Bitácora independiente)
    nuevo_log = LogAuditoria(
        usuario="Aprobador_Logueado", # Dato simulado para el MVP
        endpoint=f"POST /api/v1/approvals/{solicitud_id}/verdict",
        timestamp=datetime.now()
    )
    db.add(nuevo_log)

    # 6. Guardamos los cambios físicos en la base de datos de manera transaccional
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
    estado_observado = db.query(Estado).filter(Estado.tipoEstado == EstadoSolicitud.OBSERVADO).first()
    
    # 2. CREAMOS LA LISTA DE PERMITIDOS
    estados_validos = [estado_pendiente.idEstado, estado_observado.idEstado]
    
    # 3. CAMBIO CLAVE: Ahora permitimos PENDIENTE u OBSERVADO
    if solicitud.estado_id not in estados_validos:
        raise Exception("Conflicto: Solo se pueden evaluar solicitudes en estado PENDIENTE u OBSERVADO.")

    # --- BIFURCACIÓN DEL FLUJO DEL SECRETARIO ---
    if payload.checklist_valido:
        # Camino Feliz: Todo conforme, pasa al Jefe
        nuevo_estado_str = EstadoSolicitud.POR_APROBAR
        accion_log = "Derivación a Jefatura"
        comentario_final = "Revisión técnica conforme."
    else:
        # Camino Alterno: Faltan requisitos, se devuelve al alumno
        nuevo_estado_str = EstadoSolicitud.OBSERVADO
        accion_log = "Observación en Revisión Técnica"
        comentario_final = payload.comentario

    # Buscamos el ID del nuevo estado decidido
    nuevo_estado = db.query(Estado).filter(Estado.tipoEstado == nuevo_estado_str).first()
    solicitud.estado_id = nuevo_estado.idEstado

    # Registramos la acción en el historial
    nuevo_historial = HistorialDecision(
        solicitud_id=solicitud.idSolicitud,
        usuario_id="Secretario_Logueado",
        accion=accion_log,
        comentario=comentario_final,
        fecha=datetime.now()
    )
    db.add(nuevo_historial)
    
    # Registramos en Auditoría
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
    """Obtiene las solicitudes que ya fueron procesadas (Estados Finales)."""
    estados_finales = [EstadoSolicitud.APROBADO, EstadoSolicitud.RECHAZADO, EstadoSolicitud.OBSERVADO]
    estados_db = db.query(Estado).filter(Estado.tipoEstado.in_(estados_finales)).all()
    ids_estados = [e.idEstado for e in estados_db]
    
    return db.query(Solicitud).filter(Solicitud.estado_id.in_(ids_estados)).all()


def obtener_detalle(db: Session, solicitud_id: int):
    """Obtiene una solicitud específica por su ID."""
    return db.query(Solicitud).filter(Solicitud.idSolicitud == solicitud_id).first()