# CAMPUS360_Flujo_Aprobaciones-DSI_2026-
Proyecto del curso de Diseño Sistemas de Informacion 2026-0, Modulo G4 Flujo de aprobaciones
Backend construido con **FastAPI + Uvicorn**, persistencia con **SQLAlchemy** y conexión a **MySQL con PyMySQL**, y pruebas con **Pytest**.

---

## Instrucciones de Ejecución
1. Clonar el repositorio
`git clone <URL_DEL_REPOSITORIO>`
`cd CAMPUS360_Flujo_Aprobaciones-DSI_2026-0`

BACKEND

2. Entrar a la carpeta backend: `cd backend`
3. Crear el entorno virtual (venv): `python -m venv .venv`
4. Activar entorno virtual: `.\venv\Scripts\Activate.ps1` 
5. Si PowerShell está bloqueando el entorno virtual: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned` luego cierra y vuelve a abrir PowerShell, regresa a backend e intenta activar otra vez: `cd backend` `.\.venv\Scripts\Activate.ps1`
6. Instalar depedencias `pip install --upgrade pip` `pip install fastapi uvicorn sqlalchemy pymysql pytest`
3. Ejecutar servidor: `uvicorn app.main:app --reload`
4. Ver documentación: Abrir navegador en `http://127.0.0.1:8000/docs`

## FRONTEND
1. Estar dentro de .venv(el entorno virtual) y descargar las dependencias `pip install uvicorn`
2. Descargar dependencia fastapi pip install `fastapi uvicorn`
3. Levantamos el front uvicorn `app.main:app --reload`
4. Abrir navegador en `http://localhost:5173/`

## Ejecutar Pruebas
1. Asegúrate de estar en backend y con el venv activado `cd backend` `.\.venv\Scripts\activate`
2. Ejecutar todas las `pruebas pytest`, sin embargo se recomienda ejecutar las pruebas por archivos por ejemplo `pytest -v test/test_sla_strategy.py`
