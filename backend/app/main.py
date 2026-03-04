from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.controllers.approval_controller import router as approval_router
from app.config.database import engine, SessionLocal
from app.domain import models
from app.repositories.estado_repository import inicializar_estados

# 1. Crea las tablas en MySQL si no existen
models.Base.metadata.create_all(bind=engine)

# 2. Inicializamos los estados base (Seeder)
db = SessionLocal()
try:
    inicializar_estados(db)
finally:
    db.close()

# 3. Inicializa la API
app = FastAPI(
    title="Campus360 - Módulo de Aprobaciones",
    version="1.0.0"
)

app.include_router(approval_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"mensaje": "API Operativa - MySQL Conectado"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], # URL de tu frontend en Vite
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)