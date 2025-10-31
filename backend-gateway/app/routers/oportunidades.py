"""
Router para gestión de Oportunidades
Endpoints:
- GET /api/v1/oportunidades - Listar oportunidades
- PATCH /api/v1/oportunidades/{id} - Actualizar etapa
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.oportunidad import (
    OportunidadResponse,
    OportunidadUpdateRequest,
    OportunidadUpdateResponse
)
from app.services.orchestrator_client import OrquestradorClient
from typing import List, Optional
import uuid

router = APIRouter()

@router.get("/oportunidades", response_model=List[OportunidadResponse])
async def listar_oportunidades(
    etapa: Optional[str] = Query(None, description="Filtrar por etapa"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Lista las oportunidades para el pipeline.
    Permite filtros por etapa via query params.
    
    Autorización: Token JWT (Usuario Autenticado)
    """
    query = db.query(models.Oportunidad)
    
    if etapa:
        query = query.filter(models.Oportunidad.etapa == etapa)
    
    oportunidades = query.offset(skip).limit(limit).all()
    
    return oportunidades

@router.patch("/oportunidades/{oportunidad_id}", response_model=OportunidadUpdateResponse)
async def actualizar_oportunidad(
    oportunidad_id: uuid.UUID,
    update_data: OportunidadUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza la etapa de una oportunidad.
    Si la etapa es 'CERRADA_GANADA', dispara el Agente Financiero.
    
    Autorización: Token JWT (Usuario Autenticado)
    """
    oportunidad = db.query(models.Oportunidad).filter(
        models.Oportunidad.id == oportunidad_id
    ).first()
    
    if not oportunidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oportunidad no encontrada"
        )
    
    # Actualizar etapa
    oportunidad.etapa = update_data.etapa
    db.commit()
    db.refresh(oportunidad)
    
    # Si es CERRADA_GANADA, notificar al Agente Financiero
    if update_data.etapa == "CERRADA_GANADA":
        try:
            orchestrator = OrquestradorClient()
            await orchestrator.notificar_cierre_ganado(str(oportunidad_id))
        except Exception as e:
            print(f"Error al comunicar con orquestador: {e}")
    
    return OportunidadUpdateResponse(
        id=oportunidad.id,
        etapa=oportunidad.etapa,
        message="Oportunidad actualizada exitosamente"
    )
