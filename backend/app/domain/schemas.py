"""
Capa de Dominio: Esquemas de Validación y DTOs (Data Transfer Objects).
Desacopla los modelos de persistencia (ORM) de la interfaz de red (JSON).
Aplica validaciones tempranas usando Pydantic para garantizar las Reglas de Negocio.
"""
from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo

# --- RESPUESTAS (OUTPUTS) ---
class SolicitudDTO(BaseModel):
    """
    DTO de Salida: Estructura pública enviada al cliente (Frontend).
    Oculta la complejidad de la BD y expone solo datos procesados (ej. semaforo_sla).
    """
    id: int
    alumno: str          
    tipo_tramite: str    
    estado: str          
    prioridad: str       
    semaforo_sla: str    

    model_config = ConfigDict(from_attributes=True)


# --- PETICIONES (INPUTS) ---
class DictamenInput(BaseModel):
    """
    DTO de Entrada (Aprobador): Payload para registrar la decisión final.
    Implementa ISP (Segregación de Interfaces) al solicitar solo campos pertinentes.
    """
    decision: str       
    comentario: str = "" 
    
    @field_validator('comentario')
    @classmethod
    def validar_comentario_obligatorio(cls, v: str, info: ValidationInfo):
        """Aplica validación estricta de la Regla RN-03 (Comentario obligatorio)."""
        decision = info.data.get('decision')
        if decision in ['OBSERVADO', 'RECHAZADO']:
            if not v or len(v.strip()) < 5:
                raise ValueError("RN-03: El comentario es obligatorio y debe explicar el motivo (mín. 5 caracteres).")
        return v


class DerivacionInput(BaseModel):
    """
    DTO de Entrada (Secretario): Payload para el primer filtro técnico.
    Separa la responsabilidad del Secretario de la del Aprobador.
    """
    area_destino: str
    checklist_valido: bool 
    comentario: str = ""   

    @field_validator('comentario')
    @classmethod
    def validar_comentario_secretario(cls, v: str, info: ValidationInfo):
        """Aplica validación estricta de la Regla RN-03 en caso de requisitos incompletos."""
        checklist = info.data.get('checklist_valido')
        if checklist is False:
            if not v or len(v.strip()) < 5:
                raise ValueError("RN-03: El comentario es obligatorio al observar por falta de requisitos.")
        return v