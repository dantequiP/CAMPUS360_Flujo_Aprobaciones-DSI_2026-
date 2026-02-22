from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base

class Estado(Base):
    """Catálogo de estados permitidos."""
    __tablename__ = "estados"

    idEstado = Column(Integer, primary_key=True, autoincrement=True)
    tipoEstado = Column(String(50), unique=True, nullable=False) 

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
    
    # Lo dejamos como JSON para no complicar el MVP con tabla de archivos
    adjuntos = Column(JSON, default=list)

    estado_id = Column(Integer, ForeignKey("estados.idEstado"), nullable=False)
    estado_actual = relationship("Estado", back_populates="solicitudes")
    
    # NUEVA RELACIÓN: 1 Solicitud tiene N decisiones en su historial
    historial_decisiones = relationship("HistorialDecision", back_populates="solicitud")


# ==========================================
# NUEVAS TABLAS SEGÚN TU DIAGRAMA DE CLASES
# ==========================================

class HistorialDecision(Base):
    """Registra los comentarios y acciones directas sobre la solicitud."""
    __tablename__ = "historial_decisiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.idSolicitud"), nullable=False)
    usuario_id = Column(String(50), nullable=False, default="Sistema/Admin") # MVP quemado
    accion = Column(String(100), nullable=False)
    comentario = Column(String(500), nullable=True)
    fecha = Column(DateTime, default=datetime.now)

    solicitud = relationship("Solicitud", back_populates="historial_decisiones")


class LogAuditoria(Base):
    """Bitácora inmutable de transacciones del sistema (Auditoría)."""
    __tablename__ = "log_auditoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, default="Sistema/Admin")
    endpoint = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)