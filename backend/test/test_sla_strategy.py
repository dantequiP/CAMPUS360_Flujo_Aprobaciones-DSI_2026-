
from app.services.sla_strategy import TramiteRegularStrategy
from app.services.sla_strategy import TramiteUrgenteStrategy
from datetime import datetime, timedelta

##prueba unitaria 1

def test_calcular_sla_regular_72_horas():
    """
    Prueba unitaria exclusiva para el método calcular_sla 
    de la clase TramiteRegularStrategy.
    """
    # Arrange (Organizar)
    estrategia = TramiteRegularStrategy()
    margen_error = 5  # segundos de tolerancia para la ejecución
    
    # Calculamos el valor esperado localmente para comparar
    tiempo_esperado = datetime.now() + timedelta(hours=72)
    
    # Act (Actuar)
    resultado = estrategia.calcular_sla()
    
    # Assert (Afirmar)
    # Verificamos que la diferencia entre el resultado y el esperado sea mínima
    diferencia = abs((resultado - tiempo_esperado).total_seconds())
    
    assert diferencia < margen_error, f"El SLA calculado ({resultado}) difiere demasiado del esperado ({tiempo_esperado})"

##prueb unitaria 2
def test_tramite_regular_obtener_prioridad_devuelve_normal():
    estrategia = TramiteRegularStrategy()
    
    prioridad = estrategia.obtener_prioridad()
    
    assert prioridad == "NORMAL"
##--------------------------------
# Prueba unitaria 3
def test_calcular_sla_devuelve_24_horas_adicionales():
    # 1. Arrange (Preparar)
    estrategia = TramiteUrgenteStrategy()
    
    # 2. Act (Actuar)
    resultado = estrategia.calcular_sla()
    
    # 3. Assert (Verificar)
    tiempo_esperado = datetime.now() + timedelta(hours=24)
    diferencia = abs(resultado - tiempo_esperado)
    
    # Se Verifica que la diferencia sea de menos de 1 segundo
    assert diferencia < timedelta(seconds=1)

##--------------------------------
# Prueba unitaria 4
def test_obtener_prioridad_devuelve_alta():
    # 1. Arrange (Preparar)
    estrategia = TramiteUrgenteStrategy()
    resultado_esperado = "ALTA"
    
    # 2. Act (Actuar)
    resultado = estrategia.obtener_prioridad()
    
    # 3. Assert (Verificar)
    assert resultado == resultado_esperado
