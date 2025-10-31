"""
Router para Dashboard y KPIs
Endpoint: GET /api/v1/dashboard/resumen - Obtener KPIs del dashboard
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.db import models
from app.schemas.factura import DashboardResumenResponse
from decimal import Decimal

router = APIRouter()

@router.get("/dashboard/resumen", response_model=DashboardResumenResponse)
async def obtener_resumen_dashboard(
    db: Session = Depends(get_db)
):
    """
    Obtiene los KPIs agregados para el dashboard del Manager.
    Calculados por el Agente CDAO.
    
    Autorización: Token JWT (Usuario Autenticado)
    """
    # Contar leads por estado
    leads_nuevos = db.query(models.Lead).filter(
        models.Lead.estado == "NUEVO"
    ).count()
    
    leads_enriquecidos = db.query(models.Lead).filter(
        models.Lead.estado == "ENRIQUECIDO"
    ).count()
    
    # Contar oportunidades activas
    oportunidades_activas = db.query(models.Oportunidad).filter(
        models.Oportunidad.etapa.in_(["CONTACTO_INICIAL", "PROPUESTA"])
    ).count()
    
    # Contar oportunidades cerradas
    oportunidades_cerradas = db.query(models.Oportunidad).filter(
        models.Oportunidad.etapa == "CERRADA_GANADA"
    ).count()
    
    # Calcular valor del pipeline
    valor_pipeline_result = db.query(
        func.sum(models.Oportunidad.valor_estimado)
    ).filter(
        models.Oportunidad.etapa.in_(["CONTACTO_INICIAL", "PROPUESTA"])
    ).scalar()
    
    valor_pipeline = valor_pipeline_result if valor_pipeline_result else Decimal("0")
    
    # Calcular tasa de conversión
    total_oportunidades = db.query(models.Oportunidad).count()
    tasa_conversion = (
        (oportunidades_cerradas / total_oportunidades * 100)
        if total_oportunidades > 0 else 0.0
    )
    
    # Calcular valor promedio
    valor_promedio = (
        valor_pipeline / oportunidades_activas
        if oportunidades_activas > 0 else Decimal("0")
    )
    
    return DashboardResumenResponse(
        leads_nuevos=leads_nuevos,
        leads_enriquecidos=leads_enriquecidos,
        oportunidades_activas=oportunidades_activas,
        oportunidades_cerradas=oportunidades_cerradas,
        valor_pipeline=valor_pipeline,
        tasa_conversion=round(tasa_conversion, 2),
        valor_promedio_oportunidad=valor_promedio
    )
