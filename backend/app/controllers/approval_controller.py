from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.domain.schemas import SolicitudDTO, DictamenInput
from app.config.database import get_db
from app.domain.models import Solicitud, Estado
from app.repositories import solicitud_repository

router = APIRouter()

@router.get("/approvals/pending", response_model=List[SolicitudDTO])
def listar_pendientes(db: Session = Depends(get_db)):
    # SMELL 1: Long Method. Todo está mezclado aquí.
    estado_por_aprobar = db.query(Estado).filter(Estado.tipoEstado == "POR_APROBAR").first()
    solicitudes = db.query(Solicitud).filter(Solicitud.estado_id == estado_por_aprobar.idEstado).all()
    
    dto_list = []
    for sol in solicitudes:
        semaforo = "ROJO" if sol.slaObjetivo < datetime.now() else "VERDE"
        dto = SolicitudDTO(
            id=sol.idSolicitud,
            alumno=sol.solicitante,
            tipo_tramite=sol.tipoSolicitud,
            estado="POR_APROBAR", # SMELL 4: Magic String
            prioridad=sol.prioridad,
            semaforo_sla=semaforo
        )
        dto_list.append(dto)

    priority_order = {"ALTA": 1, "NORMAL": 2, "BAJA": 3}
    dto_list.sort(key=lambda x: (priority_order.get(x.prioridad, 99), x.semaforo_sla == "VERDE"))
    return dto_list