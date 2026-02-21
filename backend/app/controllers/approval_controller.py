from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


from app.domain.schemas import SolicitudDTO, DictamenInput, DerivacionInput
from app.config.database import get_db
from app.repositories import solicitud_repository

# Controlador de Aprobaciones: Expone los endpoints REST para gestionar el ciclo de vida de las solicitudes.
# Actúa como la Capa de Presentación, recibiendo peticiones HTTP y delegando a la Capa de Servicios.

router = APIRouter()

# ---------------------------------------------------------
# CU-01: Listar Bandeja de Pendientes (CONECTADO A MYSQL)
# ---------------------------------------------------------
@router.get("/approvals/pending", response_model=List[SolicitudDTO])
def listar_pendientes(db: Session = Depends(get_db)): # <--- Inyección de BD
    """Recupera la bandeja real consultando a la base de datos."""
    
    # 1. Consultamos al Repositorio (Capa de Datos)
    solicitudes_db = solicitud_repository.listar_solicitudes_por_aprobar(db)

    resultado_dto = []
    
    # 2. Mapeamos la Entidad al DTO para el cliente
    for sol in solicitudes_db:
        # Lógica matemática en vivo: Calculamos el color del SLA
        semaforo = "ROJO" if sol.slaObjetivo < datetime.now() else "VERDE"
        
        dto = SolicitudDTO(
            id=sol.idSolicitud,
            alumno=sol.solicitante,
            tipo_tramite=sol.tipoSolicitud,
            estado=sol.estado_actual.tipoEstado, # Magia del ORM (Relación)
            prioridad=sol.prioridad,
            semaforo_sla=semaforo
        )
        resultado_dto.append(dto)

    return resultado_dto

# ----------------------------------------------------------------
# CU-02: Registrar Dictamen (Aprobar/Rechazar) (CONECTADO A MYSQL)
# ----------------------------------------------------------------

@router.post("/approvals/{id}/verdict")
def registrar_dictamen(id: int, payload: DictamenInput, db: Session = Depends(get_db)):
    """Procesa la decisión final y la guarda físicamente en MySQL."""
    
    if payload.decision not in ["APROBADO", "RECHAZADO", "OBSERVADO"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    # Llamamos a nuestra nueva función del repositorio
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

# ---------------------------------------------------------
# CU-05: Ver Detalle Consolidado
# ---------------------------------------------------------

@router.get("/approvals/{id}/detail")
def ver_detalle_solicitud(id: int):
    """Orquesta la obtención de datos externos (Alumno G3) y locales para mostrar la vista completa."""
    return {
        "solicitud_id": id,
        "alumno_datos": {"nombre": "Jose Perez", "codigo": "20210001"},
        "adjuntos": ["http://s3.aws.../certificado.pdf"],
        "historial_observaciones": []
    }



# ---------------------------------------------------------
# CU-04: Derivar a Jefatura (Secretario)
# ---------------------------------------------------------
@router.post("/workflow/{id}/escalate")
def derivar_a_jefatura(id: int, payload: DerivacionInput):
    """Permite al Secretario validar requisitos técnicos y elevar la solicitud a la bandeja de Jefatura."""
    return {
        "mensaje": "Derivación exitosa",
        "estado_anterior": "PENDIENTE",
        "estado_nuevo": "POR APROBAR",
        "asignado_a": payload.area_destino
    }

# ---------------------------------------------------------
# CU-03: Consultar Historial
# ---------------------------------------------------------
@router.get("/approvals/history", response_model=List[SolicitudDTO])
def consultar_historial():
    """Consulta de auditoría para solicitudes finalizadas, permitiendo filtros por fecha y estado."""
    return [
        {
            "id": 99,
            "alumno": "Carlos Ruiz",
            "tipo_tramite": "Reserva Lab",
            "estado": "APROBADO",
            "prioridad": "BAJA",
            "semaforo_sla": "VERDE"
        }
    ]


@router.post("/approvals/test-seed")
def crear_solicitud_prueba(tipo_tramite: str = "Rectificación de Nota", alumno: str = "Gustavo", db: Session = Depends(get_db)):
    """Crea una solicitud de prueba directamente en MySQL."""
    nueva_solicitud = solicitud_repository.crear_solicitud(
        db=db, 
        tipo_tramite=tipo_tramite, 
        solicitante=alumno
    )
    return {
        "mensaje": "¡Solicitud creada en MySQL exitosamente!", 
        "id_generado": nueva_solicitud.idSolicitud,
        "estado": nueva_solicitud.estado_actual.tipoEstado
    }