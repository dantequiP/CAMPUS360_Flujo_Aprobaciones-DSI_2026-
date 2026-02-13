from pydantic import BaseModel
from typing import Optional

# DTOs (Data Transfer Objects): Definen estrictamente qué datos entran y salen de la API.
# Actúan como contrato de interfaz y barrera de validación automática.

# --- RESPUESTAS (OUTPUTS) ---
class SolicitudDTO(BaseModel):
    """Estructura de datos pública enviada al cliente (Frontend) para listar solicitudes."""
    id: int
    alumno: str
    tipo_tramite: str
    estado: str
    prioridad: str      # Calculada en base a reglas de negocio (Alta/Media/Baja).
    semaforo_sla: str   # Indicador visual de urgencia (Rojo/Verde).

# --- PETICIONES (INPUTS) ---

class DictamenInput(BaseModel):
    """Payload requerido para que un Aprobador registre su decisión final sobre un trámite."""
    decision: str       # Valores esperados: "APROBADO", "RECHAZADO", "OBSERVADO".
    comentario: str     # Obligatorio si la decisión es "OBSERVADO".
    usuario_id: int

class DerivacionInput(BaseModel):
    """Payload exclusivo para el perfil Secretario al derivar trámites a Jefatura."""
    area_destino: str
    checklist_valido: bool # Debe ser True para permitir la transición de estado.