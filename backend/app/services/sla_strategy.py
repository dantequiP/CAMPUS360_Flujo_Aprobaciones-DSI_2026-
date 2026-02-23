"""
Capa de Servicios: Lógica de Comportamiento (Strategy Pattern).
Aplica el Patrón Strategy para el cálculo dinámico de Acuerdos de Nivel 
de Servicio (SLA) y prioridades. Garantiza el principio Abierto/Cerrado (OCP).
"""
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class SlaStrategy(ABC):
    """
    Contrato base (Interfaz). Define la familia de algoritmos 
    intercambiables para el cálculo de SLAs operativos.
    """
    @abstractmethod
    def calcular_sla(self) -> datetime:
        pass
    
    @abstractmethod
    def obtener_prioridad(self) -> str:
        pass


class TramiteRegularStrategy(SlaStrategy):
    """Estrategia Concreta: Trámites estándar con SLA de 72 horas (Prioridad NORMAL)."""
    def calcular_sla(self) -> datetime:
        return datetime.now() + timedelta(hours=72)
    
    def obtener_prioridad(self) -> str:
        return "NORMAL"


class TramiteUrgenteStrategy(SlaStrategy):
    """Estrategia Concreta: Trámites críticos con SLA de 24 horas (Prioridad ALTA)."""
    def calcular_sla(self) -> datetime:
        return datetime.now() + timedelta(hours=24)
    
    def obtener_prioridad(self) -> str:
        return "ALTA"
    

class SlaStrategyResolver:
    """
    Inyector de Dependencias Estático. Desacopla la selección de la estrategia 
    del Factory, asegurando que la infraestructura cumpla con OCP y DIP.
    """
    @staticmethod
    def resolver(tipo_tramite: str) -> SlaStrategy:
        if "Extemporánea" in tipo_tramite or "Urgente" in tipo_tramite:
            return TramiteUrgenteStrategy()
        return TramiteRegularStrategy()