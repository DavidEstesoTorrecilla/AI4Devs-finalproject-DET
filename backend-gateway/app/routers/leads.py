"""
Router para gestión de Leads
Endpoint: POST /api/v1/leads - Ingestar nuevo lead
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.lead import LeadCreateRequest, LeadCreateResponse, LeadResponse
from app.services.orchestrator_client import OrquestradorClient
import uuid

router = APIRouter()

@router.post("/leads", response_model=LeadCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def crear_lead(
    lead_data: LeadCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Ingesta un nuevo lead (Webhook o Formulario).
    Inicia el flujo de enriquecimiento con el Agente CDAO.
    
    Autorización: API Key / Origen Confiable
    """
    # Crear lead en base de datos
    nuevo_lead = models.Lead(
        id=uuid.uuid4(),
        nombre_crudo=lead_data.nombre_crudo,
        email_crudo=lead_data.email_crudo,
        empresa_crudo=lead_data.empresa_crudo,
        origen=lead_data.origen,
        estado="NUEVO"
    )
    
    db.add(nuevo_lead)
    db.commit()
    db.refresh(nuevo_lead)
    
    # Enviar solicitud al orquestador para enriquecer el lead
    try:
        orchestrator = OrquestradorClient()
        await orchestrator.solicitar_enriquecimiento(str(nuevo_lead.id))
    except Exception as e:
        # Log error pero no bloquear la respuesta
        print(f"Error al comunicar con orquestador: {e}")
    
    return LeadCreateResponse(
        lead_id=nuevo_lead.id,
        status="processing",
        message="Lead recibido y enviado para enriquecimiento"
    )

@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def obtener_lead(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Obtiene información de un lead específico
    """
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead no encontrado"
        )
    
    return lead
