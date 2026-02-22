from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.domain.schemas import DerivacionInput

# Importamos nuestros esquemas (DTOs) y dependencias
from app.domain.schemas import SolicitudDTO, DictamenInput
from app.config.database import get_db
from app.services.bandeja_facade import BandejaAprobacionFacade
from app.repositories import solicitud_repository

router = APIRouter()

# ---------------------------------------------------------
# CU-01: Listar Bandeja de Pendientes (USANDO FACADE)
# ---------------------------------------------------------
@router.get("/approvals/pending", response_model=List[SolicitudDTO])
def listar_pendientes(db: Session = Depends(get_db)):
    """Recupera la bandeja real ordenada por prioridad y SLA."""
    # Instanciamos nuestra Fachada y le pedimos la lista ya procesada
    fachada = BandejaAprobacionFacade(db)
    return fachada.obtener_bandeja_ordenada()


# ---------------------------------------------------------
# CU-02: Registrar Dictamen (Aprobar/Rechazar)
# ---------------------------------------------------------
@router.post("/approvals/{id}/verdict")
def registrar_dictamen(id: int, payload: DictamenInput, db: Session = Depends(get_db)):
    """Procesa la decisión final y la guarda físicamente en MySQL."""
    
    if payload.decision not in ["APROBADO", "RECHAZADO", "OBSERVADO"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    try:
        # Usamos el repositorio para actualizar la BD
        solicitud_actualizada = solicitud_repository.actualizar_estado(
            db=db,
            solicitud_id=id,
            nuevo_estado_str=payload.decision,
            comentario=payload.comentario
        )

        if not solicitud_actualizada:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada en MySQL")

        return {
            "mensaje": f"Solicitud {id} procesada exitosamente",
            "nuevo_estado": solicitud_actualizada.estado_actual.tipoEstado,
            "audit_log": "Cambio registrado en MySQL"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# CU-03: Consultar Historial de Decisiones
# ---------------------------------------------------------
@router.get("/approvals/history")
def consultar_historial(db: Session = Depends(get_db)):
    """Lista las solicitudes previamente atendidas (Aprobadas, Rechazadas, Observadas)."""
    solicitudes_historicas = solicitud_repository.consultar_historial(db)
    
    # Formateamos la salida rápidamente 
    return [
        {
            "id": sol.idSolicitud, 
            "tramite": sol.tipoSolicitud, 
            "estado_final": sol.estado_actual.tipoEstado, 
            "alumno": sol.solicitante,
            "fecha_decision": sol.historial_decisiones[-1].fecha if sol.historial_decisiones else None
        } 
        for sol in solicitudes_historicas
    ]


# ---------------------------------------------------------
# CU-04: Evaluar Solicitud (Exclusivo Secretario)
# ---------------------------------------------------------
@router.post("/workflow/{id}/escalate")
def evaluar_secretaria(id: int, payload: DerivacionInput, db: Session = Depends(get_db)):
    """Secretario revisa requisitos: Deriva (POR APROBAR) u Observa (OBSERVADO)."""
    try:
        solicitud = solicitud_repository.derivar_solicitud(db, id, payload)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada en BD.")
        
        accion = "derivada a la Jefatura" if payload.checklist_valido else "observada y devuelta al alumno"
        
        return {
            "mensaje": f"Solicitud {id} validada y {accion} exitosamente.",
            "nuevo_estado": solicitud.estado_actual.tipoEstado
        }
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


# ---------------------------------------------------------
# CU-05: Ver Detalle Consolidado
# ---------------------------------------------------------
@router.get("/approvals/{id}/detail")
def ver_detalle_solicitud(id: int, db: Session = Depends(get_db)):
    """Obtiene la información detallada de una solicitud específica y su auditoría."""
    solicitud = solicitud_repository.obtener_detalle(db, id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")
    
    return {
        "id": solicitud.idSolicitud,
        "alumno": solicitud.solicitante,
        "tramite": solicitud.tipoSolicitud,
        "estado_actual": solicitud.estado_actual.tipoEstado,
        "prioridad": solicitud.prioridad,
        "fecha_creacion": solicitud.fechaCreacion,
        "sla_objetivo": solicitud.slaObjetivo,
        # Mostramos el historial extrayéndolo de las tablas relacionales
        "auditoria_decisiones": [
            {"accion": h.accion, "comentario": h.comentario, "fecha": h.fecha, "actor": h.usuario_id}
            for h in solicitud.historial_decisiones
        ]
    }


# ---------------------------------------------------------
# ENDPOINT TEMPORAL PARA PRUEBAS (FACTORY + STRATEGY)
# ---------------------------------------------------------
@router.post("/approvals/test-seed")
def crear_solicitud_prueba(tipo_tramite: str = "Rectificación de Nota", alumno: str = "Gustavo", db: Session = Depends(get_db)):
    """Crea una solicitud de prueba para verificar los patrones Creacional y de Comportamiento."""
    try:
        # Esto disparará el Factory y el Strategy internamente
        nueva_solicitud = solicitud_repository.crear_solicitud(
            db=db, 
            tipo_tramite=tipo_tramite, 
            solicitante=alumno
        )
        return {
            "mensaje": "¡Solicitud creada en MySQL exitosamente!", 
            "id_generado": nueva_solicitud.idSolicitud,
            "prioridad_asignada": nueva_solicitud.prioridad, # Debería decir ALTA si es urgente
            "estado": nueva_solicitud.estado_actual.tipoEstado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))