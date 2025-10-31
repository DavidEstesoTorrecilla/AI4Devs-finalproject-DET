"""
Schemas Pydantic para Facturas y Dashboard
"""
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal

class FacturaResponse(BaseModel):
    """Schema para respuesta de factura"""
    id: UUID4
    oportunidad_id: UUID4
    estado: str  # BORRADOR, ENVIADA, PAGADA
    monto: Decimal
    fecha_emision: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardResumenResponse(BaseModel):
    """Schema para el resumen del dashboard (GET /api/v1/dashboard/resumen)"""
    leads_nuevos: int
    leads_enriquecidos: int
    oportunidades_activas: int
    oportunidades_cerradas: int
    valor_pipeline: Decimal
    tasa_conversion: float
    valor_promedio_oportunidad: Decimal

    class Config:
        from_attributes = True
