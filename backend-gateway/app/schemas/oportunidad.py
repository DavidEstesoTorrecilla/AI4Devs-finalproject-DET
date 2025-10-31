"""
Schemas Pydantic para Oportunidades
"""
from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

class OportunidadResponse(BaseModel):
    """Schema para respuesta de oportunidad"""
    id: UUID4
    contacto_id: UUID4
    etapa: str
    valor_estimado: Optional[Decimal]
    dossier_inteligencia: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OportunidadUpdateRequest(BaseModel):
    """Schema para actualizar etapa de oportunidad (PATCH /api/v1/oportunidades/{id})"""
    etapa: str  # CONTACTO_INICIAL, PROPUESTA, CERRADA_GANADA, CERRADA_PERDIDA

class OportunidadUpdateResponse(BaseModel):
    """Respuesta al actualizar oportunidad"""
    id: UUID4
    etapa: str
    message: Optional[str]

    class Config:
        from_attributes = True
