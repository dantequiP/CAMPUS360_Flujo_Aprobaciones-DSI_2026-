from app.domain.models import Solicitud
from app.services.sla_strategy import SlaStrategy, TramiteRegularStrategy, TramiteUrgenteStrategy

class SolicitudFactory:
    """Fábrica para crear solicitudes inyectando la estrategia de SLA correcta."""
    
    @staticmethod
    def crear_solicitud(tipo_tramite: str, solicitante: str, estado_inicial_id: int) -> Solicitud:
        # Decidimos qué estrategia usar basándonos en el nombre del trámite
        estrategia: SlaStrategy
        if "Extemporánea" in tipo_tramite or "Urgente" in tipo_tramite:
            estrategia = TramiteUrgenteStrategy()
        else:
            estrategia = TramiteRegularStrategy()

        # Ensamblamos la entidad
        nueva_solicitud = Solicitud(
            tipoSolicitud=tipo_tramite,
            solicitante=solicitante,
            estado_id=estado_inicial_id,
            slaObjetivo=estrategia.calcular_sla(),      # <--- Usamos la estrategia
            prioridad=estrategia.obtener_prioridad(),   # <--- Usamos la estrategia
            adjuntos=[],
            historial=[]
        )
        return nueva_solicitud