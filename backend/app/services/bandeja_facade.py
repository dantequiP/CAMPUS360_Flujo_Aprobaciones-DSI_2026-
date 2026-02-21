from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories import solicitud_repository
from app.domain.schemas import SolicitudDTO

class BandejaAprobacionFacade:
    """
    Fachada que simplifica la lógica compleja de obtener, clasificar 
    y ordenar la bandeja de pendientes del Aprobador.
    """
    def __init__(self, db: Session):
        self.db = db

    def obtener_bandeja_ordenada(self) -> list[SolicitudDTO]:
        # 1. Obtener datos crudos del repositorio
        solicitudes_db = solicitud_repository.listar_solicitudes_por_aprobar(self.db)
        
        # 2. Mapear a DTOs y calcular Semáforo
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

        # 3. Lógica de Ordenamiento del Negocio (Primero Urgentes, luego por fecha de SLA)
        # Priority mapping: ALTA = 1, NORMAL = 2, BAJA = 3
        priority_order = {"ALTA": 1, "NORMAL": 2, "BAJA": 3}
        
        # Ordenamos la lista DTO antes de enviarla
        dto_list.sort(key=lambda x: (priority_order.get(x.prioridad, 99), x.semaforo_sla == "VERDE"))

        return dto_list