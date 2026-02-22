from pydantic import BaseModel, validator
from typing import Optional

# DTOs (Data Transfer Objects): Definen estrictamente qué datos entran y salen de la API.
# Actúan como contrato de interfaz y barrera de validación automática.

# --- RESPUESTAS (OUTPUTS) ---
class SolicitudDTO(BaseModel):
    """Estructura de datos pública enviada al cliente (Frontend) para listar solicitudes."""
    id: int
    alumno: str          # Mapeado desde 'solicitante'
    tipo_tramite: str    # Mapeado desde 'tipoSolicitud'
    estado: str          # Mapeado desde la relación con 'Estado'
    prioridad: str       # Calculada por la Estrategia (ALTA/NORMAL)
    semaforo_sla: str    # Indicador visual de urgencia (ROJO/VERDE)

    class Config:
        from_attributes = True # Permite a Pydantic leer datos directamente de modelos SQLAlchemy


# --- PETICIONES (INPUTS) ---
class DictamenInput(BaseModel):
    """Payload requerido para que un Aprobador registre su decisión final sobre un trámite."""
    decision: str       # Valores esperados: "APROBADO", "RECHAZADO", "OBSERVADO"
    comentario: str = "" # Por defecto vacío para poder validarlo dinámicamente
    
    # Validaciones Automáticas (Reglas de Negocio)
    @validator('comentario')
    def validar_comentario_obligatorio(cls, v, values):
        # Extraemos la decisión que el usuario envió en el JSON
        decision = values.get('decision')
        
        # RN3: Si la decisión es negativa o devuelve el trámite, exigimos justificación
        if decision in ['OBSERVADO', 'RECHAZADO']:
            if not v or len(v.strip()) < 5:
                raise ValueError("RN3: El comentario es obligatorio y debe explicar el motivo (mín. 5 caracteres).")
        return v


class DerivacionInput(BaseModel):
    """Payload exclusivo para el perfil Secretario al evaluar trámites PENDIENTES."""
    area_destino: str
    checklist_valido: bool # True = Pasa a POR_APROBAR / False = Devuelto como OBSERVADO
    comentario: str = ""   # Obligatorio si checklist_valido es False

    @validator('comentario')
    def validar_comentario_secretario(cls, v, values):
        checklist = values.get('checklist_valido')
        # RN3: Si el secretario marca el checklist como inválido, DEBE justificarlo
        if checklist is False:
            if not v or len(v.strip()) < 5:
                raise ValueError("RN3: El comentario es obligatorio al observar por falta de requisitos.")
        return v