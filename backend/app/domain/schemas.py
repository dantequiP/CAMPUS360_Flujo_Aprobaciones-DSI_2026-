from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo

# --- RESPUESTAS (OUTPUTS) ---
class SolicitudDTO(BaseModel):
    """Estructura de datos pública enviada al cliente (Frontend) para listar solicitudes."""
    id: int
    alumno: str          
    tipo_tramite: str    
    estado: str          
    prioridad: str       
    semaforo_sla: str    

    # Sintaxis actualizada para Pydantic V2
    model_config = ConfigDict(from_attributes=True)


# --- PETICIONES (INPUTS) ---
class DictamenInput(BaseModel):
    """Payload requerido para que un Aprobador registre su decisión final sobre un trámite."""
    decision: str       
    comentario: str = "" 
    
    # Sintaxis actualizada para Pydantic V2
    @field_validator('comentario')
    @classmethod
    def validar_comentario_obligatorio(cls, v: str, info: ValidationInfo):
        decision = info.data.get('decision')
        if decision in ['OBSERVADO', 'RECHAZADO']:
            if not v or len(v.strip()) < 5:
                raise ValueError("RN3: El comentario es obligatorio y debe explicar el motivo (mín. 5 caracteres).")
        return v


class DerivacionInput(BaseModel):
    """Payload exclusivo para el perfil Secretario al evaluar trámites PENDIENTES."""
    area_destino: str
    checklist_valido: bool 
    comentario: str = ""   

    # Sintaxis actualizada para Pydantic V2
    @field_validator('comentario')
    @classmethod
    def validar_comentario_secretario(cls, v: str, info: ValidationInfo):
        checklist = info.data.get('checklist_valido')
        if checklist is False:
            if not v or len(v.strip()) < 5:
                raise ValueError("RN3: El comentario es obligatorio al observar por falta de requisitos.")
        return v