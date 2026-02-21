from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

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