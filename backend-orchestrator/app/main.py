"""
EMASAI (Organis.AI) - Backend Orchestrator
Sistema Multi-Agente basado en SPADE
"""
import asyncio
import os
from spade import quit_spade
from app.agents.marketing_agent import AgenteMarketing
from app.agents.cdao_agent import AgenteCDAO
from app.agents.ventas_agent import AgenteVentas
from app.agents.finanzas_agent import AgenteFinanzas
from fastapi import FastAPI
from app.api import router, set_agentes

# FastAPI app para recibir comandos del Gateway
app = FastAPI(
    title="EMASAI Orchestrator",
    description="Orquestador Multi-Agente para Sistema de Ventas con IA",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

# Variables globales para los agentes
agentes = {}

async def iniciar_agentes():
    """Inicializa y arranca todos los agentes SPADE"""
    
    # Configuración XMPP (se puede usar servidor local o público)
    xmpp_server = os.getenv("XMPP_SERVER", "localhost")
    xmpp_password = os.getenv("XMPP_PASSWORD", "password123")
    
    # Calcular JIDs de cada agente
    marketing_jid = f"marketing@{xmpp_server}"
    cdao_jid = f"cdao@{xmpp_server}"
    ventas_jid = f"ventas@{xmpp_server}"
    finanzas_jid = f"finanzas@{xmpp_server}"
    
    # Crear agentes con referencias entre ellos para comunicación
    agentes['marketing'] = AgenteMarketing(
        marketing_jid,
        xmpp_password,
        cdao_jid=cdao_jid
    )
    
    agentes['cdao'] = AgenteCDAO(
        cdao_jid,
        xmpp_password,
        ventas_jid=ventas_jid
    )
    
    agentes['ventas'] = AgenteVentas(
        ventas_jid,
        xmpp_password,
        finanzas_jid=finanzas_jid
    )
    
    agentes['finanzas'] = AgenteFinanzas(
        finanzas_jid,
        xmpp_password
    )
    
    # Inyectar agentes en el router de API para que puedan ser llamados
    set_agentes(agentes)
    
    # Iniciar todos los agentes
    for nombre, agente in agentes.items():
        await agente.start()
        print(f"✅ Agente {nombre.upper()} iniciado")
    
    print("🚀 Sistema Multi-Agente EMASAI operativo")

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de FastAPI"""
    await iniciar_agentes()

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de FastAPI"""
    print("🛑 Deteniendo agentes...")
    for agente in agentes.values():
        await agente.stop()
    quit_spade()

@app.get("/")
async def root():
    return {
        "message": "EMASAI Orchestrator - Sistema Multi-Agente",
        "agentes_activos": list(agentes.keys()),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check del orquestador"""
    estado_agentes = {
        nombre: agente.is_alive()
        for nombre, agente in agentes.items()
    }
    
    return {
        "status": "healthy" if all(estado_agentes.values()) else "degraded",
        "agentes": estado_agentes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
