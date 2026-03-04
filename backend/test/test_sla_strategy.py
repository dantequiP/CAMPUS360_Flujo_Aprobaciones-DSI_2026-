
from app.services.sla_strategy import TramiteRegularStrategy
from app.services.sla_strategy import TramiteUrgenteStrategy
from datetime import datetime, timedelta

##prueba unitaria 1

def test_calcular_sla_regular_72_horas():
    """
    Prueba unitaria exclusiva para el método calcular_sla 
    de la clase TramiteRegularStrategy.
    """
   
    estrategia = TramiteRegularStrategy()
    margen_error = 5  # segundos de tolerancia para la ejecución
    
    tiempo_esperado = datetime.now() + timedelta(hours=72)
    
    resultado = estrategia.calcular_sla()
    
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
    
    estrategia = TramiteUrgenteStrategy()
    
    resultado = estrategia.calcular_sla()

    tiempo_esperado = datetime.now() + timedelta(hours=24)
    diferencia = abs(resultado - tiempo_esperado)
 
    assert diferencia < timedelta(seconds=1)

##--------------------------------

# Prueba unitaria 4
def test_obtener_prioridad_devuelve_alta():
   
    estrategia = TramiteUrgenteStrategy()
    resultado_esperado = "ALTA"

    resultado = estrategia.obtener_prioridad()
 
    assert resultado == resultado_esperado
