from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_smoke_servidor_enciende():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Bienvenido al API del Grupo 4 - Campus360 (Estado: OPERATIVO)"}