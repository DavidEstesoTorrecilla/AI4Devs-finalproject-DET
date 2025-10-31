"""
Modelos SQLAlchemy basados en el esquema de la documentación
"""
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    sitio_web = Column(String(255))
    sector = Column(String(100))  # Enriquecido por CDAO
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Contacto(Base):
    __tablename__ = "contactos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"))
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    puesto = Column(String(100))  # Enriquecido por CDAO
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estado = Column(String(50), nullable=False, default='NUEVO')  # NUEVO, ENRIQUECIDO, CONVERTIDO, DESCARTADO
    origen = Column(String(100))
    nombre_crudo = Column(String(255))
    email_crudo = Column(String(255))
    empresa_crudo = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Oportunidad(Base):
    __tablename__ = "oportunidades"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contacto_id = Column(UUID(as_uuid=True), ForeignKey("contactos.id"), nullable=False)
    etapa = Column(String(50), nullable=False, default='CONTACTO_INICIAL')  # CONTACTO_INICIAL, PROPUESTA, CERRADA_GANADA, CERRADA_PERDIDA
    valor_estimado = Column(DECIMAL(15, 2))
    dossier_inteligencia = Column(JSON)  # Output de SurfSense/CDAO
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Factura(Base):
    __tablename__ = "facturas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oportunidad_id = Column(UUID(as_uuid=True), ForeignKey("oportunidades.id"), nullable=False)
    estado = Column(String(50), nullable=False, default='BORRADOR')  # BORRADOR, ENVIADA, PAGADA
    monto = Column(DECIMAL(15, 2), nullable=False)
    fecha_emision = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TareaAgente(Base):
    __tablename__ = "tareas_agente"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agente_tipo = Column(String(50), nullable=False)  # MARKETING, CDAO, VENTAS, FINANZAS
    tipo_tarea = Column(String(100), nullable=False)
    estado = Column(String(50), nullable=False)  # INICIADA, COMPLETADA, ERROR
    entidad_relacionada_id = Column(UUID(as_uuid=True))  # ID genérico
    detalles = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
