from fastapi import FastAPI
from app.controllers.approval_controller import router as approval_router

# Punto de Entrada de la Aplicación (Entry Point):
# Inicializa el servidor ASGI, configura la documentación automática (Swagger) y registra las rutas.

app = FastAPI(
    title="Campus360 - Módulo de Aprobaciones",
    description="API REST para la gestión del flujo de aprobaciones (Grupo 4).",
    version="1.0.0" # Versión semántica del API.
)

# Registro de Controladores (Routing):
# Conecta la Capa de Presentación (Controllers) con el núcleo de la aplicación bajo el prefijo estandarizado.
app.include_router(approval_router, prefix="/api/v1")

# Endpoint de Diagnóstico (Health Check):
# Permite a los balanceadores de carga o administradores verificar si el servicio está operativo.
@app.get("/")
def home():
    return {"mensaje": "Bienvenido al API del Grupo 4 - Campus360 (Estado: OPERATIVO)"}