from sqlalchemy.orm import Session
from app.domain.models import Solicitud, Estado
from datetime import datetime, timedelta

def crear_solicitud(db: Session, tipo_tramite: str, solicitante: str):
    """
    Patrón Repository: Centraliza la lógica de creación en BD.
    """
    # 1. Buscamos el ID del estado inicial ("POR_APROBAR" o "PENDIENTE" según decidas)
    estado_inicial = db.query(Estado).filter(Estado.tipoEstado == "POR_APROBAR").first()
    
    if not estado_inicial:
        raise Exception("Error crítico: Los estados no están inicializados en la BD.")

    # 2. Regla de Negocio (SLA): Digamos que tienen 48 horas para resolverlo
    fecha_limite = datetime.now() + timedelta(hours=48)

    # 3. Creamos el objeto (Instancia de tu Entidad)
    nueva_solicitud = Solicitud(
        tipoSolicitud=tipo_tramite,
        solicitante=solicitante,
        slaObjetivo=fecha_limite,
        prioridad="NORMAL",
        estado_id=estado_inicial.idEstado, # Vinculamos la llave foránea
        adjuntos=["http://mi-aws.com/doc.pdf"], # Dato de prueba
        historial=[{"accion": "Creado por el Grupo 3", "fecha": str(datetime.now())}] # Dato de prueba
    )

    # 4. Guardamos en MySQL
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud) # Refrescamos para obtener el ID autogenerado
    
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