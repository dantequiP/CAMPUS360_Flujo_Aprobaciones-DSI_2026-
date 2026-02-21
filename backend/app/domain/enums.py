from enum import Enum

class EstadoSolicitud(str, Enum):
    PENDIENTE = "PENDIENTE"
    POR_APROBAR = "POR_APROBAR"
    APROBADO = "APROBADO"
    OBSERVADO = "OBSERVADO"
    RECHAZADO = "RECHAZADO"