from datetime import datetime, timedelta
from app.services.solicitud_factory import SolicitudFactory

##prueba unitaria 5
def test_crear_solicitud_extemporanea_prioridad_alta_y_sla_24h():
    """
    Verifica que al ingresar 'Matricula Extemporánea', la fábrica asigne:
    - Prioridad: ALTA
    - SLA: Aproximadamente 24 horas (Estrategia Urgente)
    """
    # Arrange (Organizar)
    tipo_tramite = "Matricula Extemporánea"
    solicitante = "Usuario"
    estado_id = 1
    margen_error = 5 # segundos
    esperado_sla = datetime.now() + timedelta(hours=24)

    # Act (Actuar)
    nueva_solicitud = SolicitudFactory.crear_solicitud(tipo_tramite, solicitante, estado_id)

    # Assert (Afirmar)
    # 1. Verificamos que la prioridad sea ALTA
    assert nueva_solicitud.prioridad == "ALTA"
    
    # 2. Verificamos que el SLA calculado sea el de la estrategia urgente (24h)
    diferencia = abs((nueva_solicitud.slaObjetivo - esperado_sla).total_seconds())
    assert diferencia < margen_error, f"El SLA ({nueva_solicitud.slaObjetivo}) no corresponde a las 24h esperadas"

    # 3. Verificamos que los datos básicos se hayan asignado correctamente
    assert nueva_solicitud.tipoSolicitud == tipo_tramite
    assert nueva_solicitud.solicitante == solicitante


##prueba unitaria 6
def test_factory_crea_tramite_regular_con_prioridad_normal_y_sla_72h():
    
    tipo_tramite = "Rectificacion de Nota"
    solicitante = "Gustavo"
    estado_inicial_id = 1

    solicitud = SolicitudFactory.crear_solicitud(
        tipo_tramite,
        solicitante,
        estado_inicial_id
    )

    # Validar prioridad
    assert solicitud.prioridad == "NORMAL"

    #  Validar SLA (aproximadamente 72h)
    ahora = datetime.now()
    diferencia = solicitud.slaObjetivo - ahora

    # Permitimos margen de error de algunos segundos
    assert timedelta(hours=71, minutes=59) < diferencia < timedelta(hours=72, minutes=1)
   
