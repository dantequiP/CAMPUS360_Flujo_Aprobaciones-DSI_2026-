"""
Capa de Servicios: Lógica de Orquestación.
Aplica el Patrón Estructural Facade para encapsular reglas de negocio complejas,
liberando a los controladores (Capa API) de responsabilidades de transformación de datos (SRP).
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories import solicitud_repository
from app.domain.schemas import SolicitudDTO

class BandejaAprobacionFacade:
    """
    Patrón Facade: Oculta la complejidad de interactuar con repositorios, 
    mapear entidades ORM a DTOs y calcular métricas dinámicas operativas (SLA).
    """
    def __init__(self, db: Session):
        self.db = db

    def obtener_bandeja_ordenada(self) -> list[SolicitudDTO]:
        """
        Orquesta la construcción de la bandeja. Aplica reglas de ordenamiento 
        del negocio: Prioridad estricta y control de vencimiento de SLA (Semáforo).
        """
        # 1. Obtener datos crudos de la capa de persistencia
        solicitudes_db = solicitud_repository.listar_solicitudes_por_aprobar(self.db)
        
        # 2. Mapear a DTOs y calcular Semáforo Dinámico en tiempo de ejecución
        dto_list = []
        for sol in solicitudes_db:
            semaforo = "ROJO" if sol.slaObjetivo < datetime.now() else "VERDE"
            
            dto = SolicitudDTO(
                id=sol.idSolicitud,
                alumno=sol.solicitante,
                tipo_tramite=sol.tipoSolicitud,
                estado=sol.estado_actual.tipoEstado,
                prioridad=sol.prioridad,
                semaforo_sla=semaforo
            )
            dto_list.append(dto)

        # 3. Lógica de Ordenamiento del Negocio (Primero Urgentes, luego SLA)
        priority_order = {"ALTA": 1, "NORMAL": 2, "BAJA": 3}
        
        # Ordenamos: Primero por prioridad jerárquica, luego por riesgo de SLA (Rojo primero)
        dto_list.sort(key=lambda x: (priority_order.get(x.prioridad, 99), x.semaforo_sla == "VERDE"))

        return dto_list