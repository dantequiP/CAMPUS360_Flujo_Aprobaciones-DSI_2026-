from fastapi import APIRouter
from typing import List
from datetime import datetime
from app.domain.models import Solicitud

router = APIRouter()

# --- ENDPOINT STUB (Simulado) ---
# GET /api/v1/solicitudes
# Simula obtener la lista de solicitudes de la base de datos
@router.get("/solicitudes", response_model=List[Solicitud])
def listar_solicitudes():
    # Retornamos una lista fija (DUMMY DATA) para cumplir con el entregable
    return [
        {
            "id": 1, 
            "alumno": "Pedro Ruiz", 
            "tipo_tramite": "Rectificación de Nota", 
            "fecha_solicitud": datetime.now(),
            "estado": "POR APROBAR",
            "prioridad": "ALTA"
        },
        {
            "id": 2, 
            "alumno": "Juan Perez", 
            "tipo_tramite": "Matrícula Extemporánea", 
            "fecha_solicitud": datetime.now(),
            "estado": "PENDIENTE",
            "prioridad": "MEDIA"
        }
    ]