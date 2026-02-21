from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

# Importamos la Base desde nuestra configuración
from app.config.database import Base

class Estado(Base):
    """Catálogo de estados permitidos."""
    __tablename__ = "estados"

    idEstado = Column(Integer, primary_key=True, autoincrement=True)
    tipoEstado = Column(String(50), unique=True, nullable=False) 

    # Relación inversa
    solicitudes = relationship("Solicitud", back_populates="estado_actual")


class Solicitud(Base):
    """Entidad transaccional principal."""
    __tablename__ = "solicitudes"

    idSolicitud = Column(Integer, primary_key=True, autoincrement=True)
    tipoSolicitud = Column(String(100), nullable=False)
    fechaCreacion = Column(DateTime, default=datetime.now)
    prioridad = Column(String(20), default="NORMAL")
    slaObjetivo = Column(DateTime, nullable=False)
    solicitante = Column(String(100), nullable=False)
    
    # JSON para evitar crear múltiples tablas por ahora (MVP)
    adjuntos = Column(JSON, default=list)
    historial = Column(JSON, default=list)

    # Llave Foránea y Relación
    estado_id = Column(Integer, ForeignKey("estados.idEstado"), nullable=False)
    estado_actual = relationship("Estado", back_populates="solicitudes")