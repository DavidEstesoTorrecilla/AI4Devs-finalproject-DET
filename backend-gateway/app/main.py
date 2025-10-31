"""
EMASAI (Organis.AI) - API Gateway
FastAPI application entry point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import leads, oportunidades, facturas, dashboard
from app.db.database import engine
from app.db import models
from app.services.redis_client import get_redis_client, close_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación
    """
    # Startup: Inicializar conexiones
    print("🚀 Iniciando EMASAI Gateway...")
    
    # Crear tablas en la base de datos
    models.Base.metadata.create_all(bind=engine)
    
    # Inicializar cliente Redis
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        print("✅ Redis conectado exitosamente")
    except Exception as e:
        print(f"⚠️ Redis no disponible: {e}")
    
    yield
    
    # Shutdown: Cerrar conexiones
    print("🛑 Cerrando conexiones...")
    await close_redis_client()

app = FastAPI(
    title="EMASAI API",
    description="Sistema Multi-Agente para Automatización de Ventas con IA",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(leads.router, prefix="/api/v1", tags=["leads"])
app.include_router(oportunidades.router, prefix="/api/v1", tags=["oportunidades"])
app.include_router(facturas.router, prefix="/api/v1", tags=["facturas"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["dashboard"])

@app.get("/")
async def root():
    return {
        "message": "EMASAI API - Sistema Multi-Agente para Ventas",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check con estado de dependencias"""
    health_status = {
        "status": "healthy",
        "database": "connected",
        "redis": "unknown"
    }
    
    # Verificar Redis
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        health_status["redis"] = "connected"
    except Exception as e:
        health_status["redis"] = "disconnected"
        health_status["status"] = "degraded"
    
    return health_status
