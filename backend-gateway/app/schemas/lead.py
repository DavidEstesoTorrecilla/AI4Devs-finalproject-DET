"""
Schemas Pydantic para Leads
Basados en la especificación de la documentación
"""
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime

class LeadCreateRequest(BaseModel):
    """Schema para crear un nuevo lead (POST /api/v1/leads)"""
    nombre_crudo: str
    email_crudo: EmailStr
    empresa_crudo: Optional[str] = None
    origen: Optional[str] = None

class LeadCreateResponse(BaseModel):
    """Respuesta al crear un lead"""
    lead_id: UUID4
    status: str  # "processing"
    message: str

    class Config:
        from_attributes = True

class LeadResponse(BaseModel):
    """Schema para respuesta de lead"""
    id: UUID4
    estado: str
    origen: Optional[str]
    nombre_crudo: str
    email_crudo: str
    empresa_crudo: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
