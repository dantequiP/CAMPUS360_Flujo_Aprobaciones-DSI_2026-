from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
API_PREFIX = "/api/v1"


def crear_solicitud_prueba(tipo_tramite: str = "Rectificación de Nota", solicitante: str = "Dante") -> int:
    """
    Crea una solicitud usando el endpoint test-seed para no depender de data previa.
    Retorna el id de la solicitud creada.
    """
    payload = {"tipo_tramite": tipo_tramite, "solicitante": solicitante}
    r = client.post(f"{API_PREFIX}/approvals/test-seed", json=payload)
    assert r.status_code == 200, f"No se pudo crear solicitud: {r.text}"
    data = r.json()

   
    if "id_generado" in data:
        return data["id_generado"]
 
    if "id_solicitud" in data:
        return data["id_solicitud"]
    if "idSolicitud" in data:
        return data["idSolicitud"]
    if "id" in data:
        return data["id"]

    raise AssertionError(f"Respuesta inesperada de test-seed: {data}")



#Pruebas de caja negra

#CN1

def test_cb01_listar_pendientes_responde_200_y_lista():
    r = client.get(f"{API_PREFIX}/approvals/pending")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

#CN2
def test_cb02_crear_solicitud_y_ver_que_aparece_en_detalle():
    solicitud_id = crear_solicitud_prueba("Rectificación de Nota", "Dante")
    r = client.get(f"{API_PREFIX}/approvals/{solicitud_id}/detail")
    assert r.status_code == 200
    data = r.json()

   
    assert data["id"] == solicitud_id
    assert "estado_actual" in data
    assert "auditoria_decisiones" in data
    assert isinstance(data["auditoria_decisiones"], list)

#CN3
def test_cb03_dictamen_aprobado_actualiza_estado():
    solicitud_id = crear_solicitud_prueba("Rectificación de Nota", "Dante")
    r = client.post(
        f"{API_PREFIX}/approvals/{solicitud_id}/verdict",
        json={"decision": "APROBADO", "comentario": "Conforme"}
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("nuevo_estado") == "APROBADO"

#CN4
def test_cb04_dictamen_decision_invalida_debe_fallar():
    """
    Caso negativo confiable: el controller bloquea decisiones fuera del set permitido con 400.
    """
    solicitud_id = crear_solicitud_prueba("Rectificación de Nota", "Dante")
    r = client.post(
        f"{API_PREFIX}/approvals/{solicitud_id}/verdict",
        json={"decision": "INVALIDA"}
    )
    assert r.status_code == 400

#CN5
def test_cb05_dictamen_observado_con_comentario_ok():
    solicitud_id = crear_solicitud_prueba("Rectificación de Nota", "Dante")
    r = client.post(
        f"{API_PREFIX}/approvals/{solicitud_id}/verdict",
        json={"decision": "OBSERVADO", "comentario": "Falta sustento (>=5)."}
    )
    assert r.status_code == 200
    assert r.json().get("nuevo_estado") == "OBSERVADO"

#CN6
def test_cb06_escalate_checklist_valido_deriva_a_por_aprobar():
    """
    DerivacionInput exige area_destino (obligatorio) + checklist_valido.
    """
    solicitud_id = crear_solicitud_prueba("Rectificación de Nota", "Dante")
    r = client.post(
        f"{API_PREFIX}/workflow/{solicitud_id}/escalate",
        json={"area_destino": "JEFATURA", "checklist_valido": True, "comentario": "Checklist OK"}
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("nuevo_estado") == "POR_APROBAR"

#CN7
def test_cb07_escalate_sin_area_destino_falla_validacion():
    """
    Caso negativo confiable: DerivacionInput exige area_destino (obligatorio).
    Si se omite, FastAPI/Pydantic debe retornar 422.
    """
    solicitud_id = crear_solicitud_prueba("Rectificación de Nota", "Dennis")
    r = client.post(
        f"{API_PREFIX}/workflow/{solicitud_id}/escalate",
        json={"checklist_valido": True}  # falta area_destino
    )
    assert r.status_code == 422

#CN8
def test_cb08_detalle_solicitud_inexistente_devuelve_404():
    r = client.get(f"{API_PREFIX}/approvals/999999999/detail")
    assert r.status_code == 404