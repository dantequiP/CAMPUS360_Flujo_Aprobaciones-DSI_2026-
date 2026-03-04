"""
Capa de Infraestructura: Modelos ORM (Persistencia).
Mapea las entidades del Dominio (Diagrama de Clases UML) a tablas físicas en MySQL.
Garantiza la integridad referencial y la trazabilidad de las transacciones.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base

class Estado(Base):
    """
    Entidad paramétrica. Almacena el catálogo de estados permitidos 
    para la máquina de estados transicional.
    """
    __tablename__ = "estados"

    idEstado = Column(Integer, primary_key=True, autoincrement=True)
    tipoEstado = Column(String(50), unique=True, nullable=False) 

    solicitudes = relationship("Solicitud", back_populates="estado_actual")


class Solicitud(Base):
    """
    Entidad Transaccional Core (Root Aggregate). 
    Almacena los datos principales del trámite y el SLA calculado dinámicamente.
    """
    __tablename__ = "solicitudes"

    idSolicitud = Column(Integer, primary_key=True, autoincrement=True)
    tipoSolicitud = Column(String(100), nullable=False)
    descripcion = Column(String(1000), nullable=True) # NUEVO ATRIBUTO: ALTER TABLE solicitudes ADD COLUMN descripcion VARCHAR(1000);
    fechaCreacion = Column(DateTime, default=datetime.now)
    prioridad = Column(String(20), default="NORMAL")
    slaObjetivo = Column(DateTime, nullable=False)
    solicitante = Column(String(100), nullable=False)
    
    # Se utiliza JSON para optimizar el almacenamiento del MVP
    adjuntos = Column(JSON, default=list)

    estado_id = Column(Integer, ForeignKey("estados.idEstado"), nullable=False)
    estado_actual = relationship("Estado", back_populates="solicitudes")
    
    # Relación 1:N para garantizar el historial de dictámenes
    historial_decisiones = relationship("HistorialDecision", back_populates="solicitud")



class HistorialDecision(Base):
    """
    Entidad de Trazabilidad Operativa (Relación 1 a N con Solicitud).
    Registra quién, cuándo y por qué (comentario) se cambió de estado.
    """
    __tablename__ = "historial_decisiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.idSolicitud"), nullable=False)
    usuario_id = Column(String(50), nullable=False, default="Sistema/Admin") # Mock para MVP
    accion = Column(String(100), nullable=False)
    comentario = Column(String(500), nullable=True)
    fecha = Column(DateTime, default=datetime.now)

    solicitud = relationship("Solicitud", back_populates="historial_decisiones")


class LogAuditoria(Base):
    """
    Entidad de Auditoría de Sistemas (Bitácora inmutable).
    Registra las peticiones críticas a nivel de API para cumplir con seguridad.
    """
    __tablename__ = "log_auditoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, default="Sistema/Admin")
    endpoint = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)