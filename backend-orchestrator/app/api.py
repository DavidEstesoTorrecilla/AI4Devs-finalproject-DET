"""
API REST para recibir comandos del Gateway
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, UUID4

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])

class EnriquecerLeadRequest(BaseModel):
    lead_id: str

class OportunidadGanadaRequest(BaseModel):
    oportunidad_id: str

# Variable global para acceder a los agentes (se inyecta desde main.py)
_agentes = None

def set_agentes(agentes):
    """Inyecta los agentes desde main.py"""
    global _agentes
    _agentes = agentes

@router.post("/enriquecer-lead")
async def enriquecer_lead(request: EnriquecerLeadRequest):
    """
    Endpoint llamado por el Gateway cuando se crea un nuevo lead.
    Inicia el flujo de enriquecimiento.
    """
    if not _agentes or 'marketing' not in _agentes:
        raise HTTPException(status_code=503, detail="Agentes no disponibles")
    
    # Enviar mensaje al Agente de Marketing para que procese el lead
    agente_marketing = _agentes['marketing']
    await agente_marketing.procesar_nuevo_lead(request.lead_id)
    
    return {
        "status": "processing",
        "lead_id": request.lead_id,
        "message": "Lead enviado al Agente de Marketing para enriquecimiento"
    }

@router.post("/oportunidad-ganada")
async def oportunidad_ganada(request: OportunidadGanadaRequest):
    """
    Endpoint llamado por el Gateway cuando una oportunidad es cerrada como ganada.
    Activa al Agente Financiero.
    """
    if not _agentes or 'finanzas' not in _agentes:
        raise HTTPException(status_code=503, detail="Agentes no disponibles")
    
    # Enviar mensaje al Agente Financiero
    agente_finanzas = _agentes['finanzas']
    await agente_finanzas.generar_factura(request.oportunidad_id)
    
    return {
        "status": "processing",
        "oportunidad_id": request.oportunidad_id,
        "message": "Solicitud enviada al Agente Financiero"
    }
