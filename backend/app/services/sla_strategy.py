from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# 1. La Interfaz (Clase Base)
class SlaStrategy(ABC):
    @abstractmethod
    def calcular_sla(self) -> datetime:
        pass
    
    @abstractmethod
    def obtener_prioridad(self) -> str:
        pass

# 2. Estrategia 1: Trámites Regulares (ej. Rectificación de Nota)
class TramiteRegularStrategy(SlaStrategy):
    def calcular_sla(self) -> datetime:
        return datetime.now() + timedelta(hours=72) # 3 días
    
    def obtener_prioridad(self) -> str:
        return "NORMAL"

# 3. Estrategia 2: Trámites Urgentes (ej. Matrícula Extemporánea)
class TramiteUrgenteStrategy(SlaStrategy):
    def calcular_sla(self) -> datetime:
        return datetime.now() + timedelta(hours=24) # 1 día
    
    def obtener_prioridad(self) -> str:
        return "ALTA"
    
class SlaStrategyResolver:
    """Clase encargada de resolver e instanciar la estrategia adecuada según el trámite."""
    
    @staticmethod
    def resolver(tipo_tramite: str) -> SlaStrategy:
        if "Extemporánea" in tipo_tramite or "Urgente" in tipo_tramite:
            return TramiteUrgenteStrategy()
        return TramiteRegularStrategy()