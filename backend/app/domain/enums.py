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
    PENDIENTE = "PENDIENTE"       # Trámite recién ingresado, a la espera de revisión del Secretario.
    POR_APROBAR = "POR_APROBAR"   # Validado por el Secretario, a la espera del dictamen de Jefatura.
    APROBADO = "APROBADO"         # Dictamen final favorable.
    OBSERVADO = "OBSERVADO"       # Devuelto al alumno por falta de requisitos (Aplica RN-03).
    RECHAZADO = "RECHAZADO"       # Dictamen final desfavorable (Aplica RN-03).