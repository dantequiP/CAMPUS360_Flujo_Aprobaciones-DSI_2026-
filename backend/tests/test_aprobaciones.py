"""
Pruebas Unitarias (Caja Blanca): Módulo de Flujo de Aprobaciones.
Cumple con el requisito RNF6 (Testabilidad). Aisla y valida la lógica core 
del negocio (Patrones y Reglas) sin dependencias de la Base de Datos (Infraestructura).
"""
import pytest
from datetime import datetime, timedelta

from app.services.sla_strategy import TramiteRegularStrategy, TramiteUrgenteStrategy
from app.services.solicitud_factory import SolicitudFactory
from app.domain.schemas import DictamenInput, DerivacionInput

# ==========================================
# PRUEBAS DEL PATRÓN STRATEGY (Cálculo de SLA)
# ==========================================

def test_01_strategy_regular_calcula_sla_correcto():
    """Valida el cálculo algorítmico de SLA (72h) y prioridad NORMAL para trámites estándar."""
    estrategia = TramiteRegularStrategy()
    
    prioridad = estrategia.obtener_prioridad()
    sla = estrategia.calcular_sla()
    
    assert prioridad == "NORMAL"
    assert sla > datetime.now() + timedelta(hours=71) 

def test_02_strategy_urgente_calcula_sla_correcto():
    """Valida el cálculo algorítmico de SLA (24h) y prioridad ALTA para trámites críticos."""
    estrategia = TramiteUrgenteStrategy()
    
    prioridad = estrategia.obtener_prioridad()
    sla = estrategia.calcular_sla()
    
    assert prioridad == "ALTA"
    assert sla < datetime.now() + timedelta(hours=25) 

# ==========================================
# PRUEBAS DEL PATRÓN FACTORY (Ensamblaje)
# ==========================================

def test_03_factory_crea_solicitud_regular():
    """Valida el ensamblaje de la entidad 'Solicitud' inyectando la estrategia base (DIP)."""
    estrategia_mock = TramiteRegularStrategy()
    solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite="Constancia de Notas", 
        solicitante="Juan Perez", 
        estado_inicial_id=1,
        estrategia=estrategia_mock
    )
    assert solicitud.prioridad == "NORMAL"

def test_04_factory_crea_solicitud_urgente():
    """Valida el ensamblaje de la entidad inyectando la estrategia de alta prioridad."""
    estrategia_mock = TramiteUrgenteStrategy()
    solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite="Matrícula Extemporánea", 
        solicitante="Maria Gomez", 
        estado_inicial_id=1,
        estrategia=estrategia_mock
    )
    assert solicitud.prioridad == "ALTA"
    
# ==========================================
# PRUEBAS DE REGLAS DE NEGOCIO (Validaciones DTO)
# ==========================================

def test_05_dictamen_aprobado_permite_comentario_vacio():
    """Verifica el flujo feliz del Aprobador: un dictamen APROBADO no exige justificación."""
    dictamen = DictamenInput(decision="APROBADO", comentario="")
    assert dictamen.decision == "APROBADO"

def test_06_dictamen_observado_exige_comentario():
    """Valida el estricto cumplimiento de RN-03: Exige comentario al Observar/Rechazar."""
    with pytest.raises(ValueError) as excinfo:
        DictamenInput(decision="OBSERVADO", comentario="")
    
    assert "RN-03" in str(excinfo.value)

# ==========================================
# PRUEBAS DEL SECRETARIO (Derivación)
# ==========================================

def test_07_derivacion_conforme_sin_comentario():
    """Verifica el flujo del Secretario: la derivación limpia a Jefatura no exige comentario."""
    derivacion = DerivacionInput(
        area_destino="Jefatura de Sistemas", 
        checklist_valido=True, 
        comentario=""
    )
    assert derivacion.checklist_valido is True

def test_08_derivacion_observada_exige_comentario():
    """Valida el estricto cumplimiento de RN-03 en el DTO exclusivo del Secretario."""
    with pytest.raises(ValueError) as excinfo:
        DerivacionInput(
            area_destino="Jefatura de Sistemas", 
            checklist_valido=False, 
            comentario="Mal"
        )
    
    assert "RN-03" in str(excinfo.value)