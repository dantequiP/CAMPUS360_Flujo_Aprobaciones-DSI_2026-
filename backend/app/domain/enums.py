"""
Capa de Dominio: Enumeraciones (Value Objects).
Centraliza la máquina de estados del Flujo de Aprobaciones.
Evita el uso de 'magic strings' y garantiza la integridad de los datos en toda la aplicación.
"""
from enum import Enum

class EstadoSolicitud(str, Enum):
    """
    Representa el ciclo de vida exacto de un trámite según el modelo de negocio (RN-06).
    """
    PENDIENTE = "PENDIENTE"
    POR_APROBAR = "POR_APROBAR"
    APROBADO = "APROBADO"
    OBSERVADO = "OBSERVADO"
    RECHAZADO = "RECHAZADO"