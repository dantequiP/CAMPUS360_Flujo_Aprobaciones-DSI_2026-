from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Definimos una solicitud basica
class Solicitud(BaseModel):
    id: int
    alumno: str
    tipo_tramite: str
    fecha_solicitud: datetime
    estado: str
    prioridad: str