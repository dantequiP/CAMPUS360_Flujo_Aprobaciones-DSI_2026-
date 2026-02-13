from fastapi import FastAPI
from app.controllers.approval_controller import router as approval_router

# Creamos la aplicación FastAPI
app = FastAPI(
    title="Campus360 - Módulo de Aprobaciones",
    description="API para la gestión de flujo de aprobaciones (Grupo 4)",
    version="1.0.0"
)

# Conectamos las rutas del controlador
app.include_router(approval_router, prefix="/api/v1", tags=["Aprobaciones"])

# Endpoint de prueba (Health Check)
@app.get("/")
def home():
    return {"mensaje": "Bienvenido al API del Grupo 4 - Campus360"}