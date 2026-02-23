"""
Capa de Presentación: Controladores API (API Layer)
Orquesta las peticiones HTTP y mapea los Casos de Uso (CU) del sistema, 
delegando la lógica de negocio a la Capa de Servicios para cumplir con SOLID (SRP).
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# Importamos esquemas (DTOs) e inyección de dependencias
from app.domain.schemas import SolicitudDTO, DictamenInput, DerivacionInput
from app.config.database import get_db
from app.services.bandeja_facade import BandejaAprobacionFacade
from app.repositories import solicitud_repository

router = APIRouter()

@router.get("/approvals/pending", response_model=List[SolicitudDTO])
def listar_pendientes(db: Session = Depends(get_db)):
    """
    CU-01: Listar Bandeja de Pendientes.
    Patrón Estructural: Utiliza BandejaAprobacionFacade para encapsular la lógica 
    compleja de ordenamiento por SLA y cálculo del semáforo.
    """
    fachada = BandejaAprobacionFacade(db)
    return fachada.obtener_bandeja_ordenada()


@router.post("/approvals/{id}/verdict")
def registrar_dictamen(id: int, payload: DictamenInput, db: Session = Depends(get_db)):
    """
    CU-02: Registrar Dictamen (Aprobar/Rechazar).
    Ejecuta el cambio de estado definitivo. El payload (DictamenInput) impone 
    el cumplimiento de la RN-03 (Comentario obligatorio) mediante Pydantic.
    """
    if payload.decision not in ["APROBADO", "RECHAZADO", "OBSERVADO"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    try:
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


@router.get("/approvals/history")
def consultar_historial(db: Session = Depends(get_db)):
    """
    CU-03: Consultar Historial de Decisiones.
    Recupera y formatea las solicitudes que ya han alcanzado un estado resolutivo.
    """
    solicitudes_historicas = solicitud_repository.consultar_historial(db)
    
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


@router.post("/workflow/{id}/escalate")
def evaluar_secretaria(id: int, payload: DerivacionInput, db: Session = Depends(get_db)):
    """
    CU-04: Evaluar Solicitud (Derivar a Jefatura).
    Exclusivo para el perfil 'Secretario'. Transiciona una solicitud PENDIENTE 
    aplicando la regla RN-06 y RN-03 mediante el DTO DerivacionInput.
    """
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


@router.get("/approvals/{id}/detail")
def ver_detalle_solicitud(id: int, db: Session = Depends(get_db)):
    """
    CU-05: Ver Detalle Consolidado.
    Recupera la entidad Solicitud junto con sus relaciones ORM 
    (Historial y Auditoría) de forma consolidada.
    """
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
        "auditoria_decisiones": [
            {"accion": h.accion, "comentario": h.comentario, "fecha": h.fecha, "actor": h.usuario_id}
            for h in solicitud.historial_decisiones
        ]
    }


@router.post("/approvals/test-seed")
def crear_solicitud_prueba(tipo_tramite: str = "Rectificación de Nota", alumno: str = "Gustavo", db: Session = Depends(get_db)):
    """
    Endpoint de Utilidad: Crea datos de prueba demostrando el uso de los 
    patrones Factory (Creacional) y Strategy (Comportamiento) aplicados a la persistencia.
    """
    try:
        nueva_solicitud = solicitud_repository.crear_solicitud(
            db=db, 
            tipo_tramite=tipo_tramite, 
            solicitante=alumno
        )
        return {
            "mensaje": "¡Solicitud creada en MySQL exitosamente!", 
            "id_generado": nueva_solicitud.idSolicitud,
            "prioridad_asignada": nueva_solicitud.prioridad, 
            "estado": nueva_solicitud.estado_actual.tipoEstado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))