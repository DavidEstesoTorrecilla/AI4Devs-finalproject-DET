"""
Router para gestión de Facturas
Endpoint: GET /api/v1/facturas - Listar facturas
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.factura import FacturaResponse
from typing import List, Optional

router = APIRouter()

@router.get("/facturas", response_model=List[FacturaResponse])
async def listar_facturas(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Lista las facturas generadas.
    
    Autorización: Token JWT (Usuario Autenticado)
    """
    query = db.query(models.Factura)
    
    if estado:
        query = query.filter(models.Factura.estado == estado)
    
    facturas = query.offset(skip).limit(limit).all()
    
    return facturas
