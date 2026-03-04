"""
Capa de Servicios: Lógica Creacional (Factory Pattern).
Desacopla la instanciación compleja de la entidad principal (Solicitud), 
centralizando su ensamblaje y asegurando el cumplimiento estricto de SOLID.
"""
from app.domain.models import Solicitud
from app.services.sla_strategy import SlaStrategy, TramiteRegularStrategy, TramiteUrgenteStrategy

class SolicitudFactory:
    """
    Patrón Creacional Factory: Ensambla la entidad 'Solicitud' integrando 
    las reglas del negocio antes de su persistencia en la base de datos.
    """
    
    @staticmethod
    def crear_solicitud(tipo_tramite: str, solicitante: str, descripcion: str, estado_inicial_id: int) -> Solicitud:
        # Decidimos qué estrategia usar basándonos en el nombre del trámite
        estrategia: SlaStrategy
        if "Extemporánea" in tipo_tramite or "Urgente" in tipo_tramite:
            estrategia = TramiteUrgenteStrategy()
        else:
            estrategia = TramiteRegularStrategy()

        """
        Construye el Aggregate Root inyectando la estrategia de SLA resuelta (DIP).
        Asegura que la entidad nazca con su prioridad y tiempos correctamente calculados.
        """
        nueva_solicitud = Solicitud(
            tipoSolicitud=tipo_tramite,
            solicitante=solicitante,
            descripcion=descripcion,
            estado_id=estado_inicial_id,
            slaObjetivo=estrategia.calcular_sla(),
            prioridad=estrategia.obtener_prioridad(),
            adjuntos=[] 
        )
        return nueva_solicitud