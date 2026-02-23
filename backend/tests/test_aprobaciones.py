import pytest
from datetime import datetime, timedelta

# Importamos las clases que vamos a testear (Aisladas de la Base de Datos)
from app.services.sla_strategy import TramiteRegularStrategy, TramiteUrgenteStrategy
from app.services.solicitud_factory import SolicitudFactory
from app.domain.schemas import DictamenInput, DerivacionInput

# ==========================================
# PRUEBAS DEL PATRÓN STRATEGY (Cálculo de SLA)
# ==========================================

def test_01_strategy_regular_calcula_sla_correcto():
    """Prueba 1: Verifica que un trámite regular asigne 72h y prioridad NORMAL."""
    estrategia = TramiteRegularStrategy()
    
    prioridad = estrategia.obtener_prioridad()
    sla = estrategia.calcular_sla()
    
    assert prioridad == "NORMAL"
    assert sla > datetime.now() + timedelta(hours=71) # Comprueba que sumó ~72h

def test_02_strategy_urgente_calcula_sla_correcto():
    """Prueba 2: Verifica que un trámite urgente asigne 24h y prioridad ALTA."""
    estrategia = TramiteUrgenteStrategy()
    
    prioridad = estrategia.obtener_prioridad()
    sla = estrategia.calcular_sla()
    
    assert prioridad == "ALTA"
    assert sla < datetime.now() + timedelta(hours=25) # Comprueba que sumó ~24h

# ==========================================
# PRUEBAS DEL PATRÓN FACTORY (Ensamblaje)
# ==========================================
def test_03_factory_crea_solicitud_regular():
    """Prueba 3: Verifica que la Fábrica ensamble bien usando la estrategia inyectada."""
    estrategia_mock = TramiteRegularStrategy()
    solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite="Constancia de Notas", 
        solicitante="Juan Perez", 
        estado_inicial_id=1,
        estrategia=estrategia_mock
    )
    assert solicitud.prioridad == "NORMAL"

def test_04_factory_crea_solicitud_urgente():
    """Prueba 4: Verifica el ensamblaje con estrategia urgente inyectada."""
    estrategia_mock = TramiteUrgenteStrategy()
    solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite="Matrícula Extemporánea", 
        solicitante="Maria Gomez", 
        estado_inicial_id=1,
        estrategia=estrategia_mock
    )
    assert solicitud.prioridad == "ALTA"
    
# ==========================================
# PRUEBAS DE REGLAS DE NEGOCIO (Validaciones)
# ==========================================

def test_05_dictamen_aprobado_permite_comentario_vacio():
    """Prueba 5: Validar que APROBADO no exige comentario (Camino feliz)."""
    # Si no lanza error, la prueba pasa
    dictamen = DictamenInput(decision="APROBADO", comentario="")
    assert dictamen.decision == "APROBADO"

def test_06_dictamen_observado_exige_comentario():
    """Prueba 6: Validar RN3 (Comentario Obligatorio al observar o rechazar)."""
    with pytest.raises(ValueError) as excinfo:
        # Intentamos forzar un error enviando OBSERVADO sin justificación
        DictamenInput(decision="OBSERVADO", comentario="")
    
    # Verificamos que Pydantic bloqueó la acción por la regla RN3
    assert "RN3" in str(excinfo.value)


# ==========================================
# PRUEBAS DEL SECRETARIO (Derivación)
# ==========================================

def test_07_derivacion_conforme_sin_comentario():
    """Prueba 7: Validar que el Secretario puede derivar (checklist True) sin justificar."""
    # Camino feliz: Checklist válido, comentario vacío. No debería lanzar error.
    derivacion = DerivacionInput(
        area_destino="Jefatura de Sistemas", 
        checklist_valido=True, 
        comentario=""
    )
    assert derivacion.checklist_valido is True

def test_08_derivacion_observada_exige_comentario():
    """Prueba 8: Validar RN3 en Secretario (checklist False exige comentario)."""
    with pytest.raises(ValueError) as excinfo:
        # Forzamos el error: Checklist inválido y un comentario muy corto ("Mal")
        DerivacionInput(
            area_destino="Jefatura de Sistemas", 
            checklist_valido=False, 
            comentario="Mal"
        )
    
    # Verificamos que Pydantic nos bloquee protegiendo la Regla de Negocio 3
    assert "RN3" in str(excinfo.value)