from app.domain.models import Solicitud
from app.services.sla_strategy import SlaStrategy

class SolicitudFactory:
    """Fábrica que ensambla solicitudes. Ahora cumple 100% con OCP y DIP."""
    
    @staticmethod
    def crear_solicitud(tipo_tramite: str, solicitante: str, estado_inicial_id: int, estrategia: SlaStrategy) -> Solicitud:
        # Ensamblamos la entidad directamente usando la estrategia inyectada
        nueva_solicitud = Solicitud(
            tipoSolicitud=tipo_tramite,
            solicitante=solicitante,
            estado_id=estado_inicial_id,
            slaObjetivo=estrategia.calcular_sla(),
            prioridad=estrategia.obtener_prioridad(),
            adjuntos=[] 
        )
        return nueva_solicitud