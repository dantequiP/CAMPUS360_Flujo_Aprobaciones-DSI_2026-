from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.schemas import SolicitudDTO, DictamenInput, DerivacionInput

# Controlador de Aprobaciones: Expone los endpoints REST para gestionar el ciclo de vida de las solicitudes.
# Actúa como la Capa de Presentación, recibiendo peticiones HTTP y delegando a la Capa de Servicios.

router = APIRouter()

# ---------------------------------------------------------
# CU-01: Listar Bandeja de Pendientes
# ---------------------------------------------------------
@router.get("/approvals/pending", response_model=List[SolicitudDTO])
def listar_pendientes():
    """Recupera la bandeja de entrada del Aprobador, priorizando las solicitudes por urgencia (SLA)."""
    # Retornamos DATOS DUMMY (Stub) para simular la respuesta del backend en esta fase de prototipo.
    return [
        {
            "id": 101,
            "alumno": "Jose Perez",
            "tipo_tramite": "Rectificación de Nota",
            "estado": "POR APROBAR",
            "prioridad": "ALTA",
            "semaforo_sla": "ROJO"
        },
        {
            "id": 102,
            "alumno": "Ana Torres",
            "tipo_tramite": "Matrícula Extemporánea",
            "estado": "POR APROBAR",
            "prioridad": "MEDIA",
            "semaforo_sla": "VERDE"
        }
    ]

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
# CU-02: Registrar Dictamen (Aprobar/Rechazar)
# ---------------------------------------------------------
@router.post("/approvals/{id}/verdict")
def registrar_dictamen(id: int, payload: DictamenInput):
    """Procesa la decisión final del Jefe, cambia el estado de la solicitud y dispara notificaciones."""
    if payload.decision not in ["APROBADO", "RECHAZADO", "OBSERVADO"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    return {
        "mensaje": f"Solicitud {id} procesada exitosamente",
        "nuevo_estado": payload.decision,
        "audit_log": "Registrado"
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