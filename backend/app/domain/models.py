from datetime import datetime

# Entidades de Dominio: Representan los objetos del negocio y sus reglas internas.
# Se mantienen puras y desacopladas de librerías externas (como Pydantic o FastAPI).

class Solicitud:
    """Representa el trámite académico central, encapsulando su estado y ciclo de vida."""

    def __init__(self, id: int, alumno: str, tipo_tramite: str, estado: str):
        """Inicializa la entidad y registra automáticamente la fecha de creación (Timestamp)."""
        self.id = id
        self.alumno = alumno
        self.tipo_tramite = tipo_tramite
        self.fecha_solicitud = datetime.now() # Regla: La fecha es inmutable al crear el objeto.
        self.estado = estado

    def esta_vencida(self) -> bool:
        """Evalúa si la solicitud ha excedido el tiempo límite de atención (SLA) definido."""
        return False