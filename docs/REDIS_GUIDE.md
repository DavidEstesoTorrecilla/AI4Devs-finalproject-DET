# 🔴 Redis Cache - Guía de Uso

## Descripción

Redis se utiliza en EMASAI para:
- **Cache de leads y oportunidades**: Reducir consultas a PostgreSQL
- **Cache de resultados SurfSense**: Evitar consultas repetidas al servicio externo (costosas)
- **Sesiones de usuario**: (Futuro) Almacenar tokens JWT y sesiones activas

## Configuración

### Variables de Entorno

**Gateway (.env):**
```env
REDIS_URL=redis://:organis_redis_password@localhost:6379/0
REDIS_TTL=3600  # 1 hora
```

**Orchestrator (.env):**
```env
REDIS_URL=redis://:organis_redis_password@localhost:6379/1
REDIS_TTL=7200  # 2 horas
```

> **Nota**: Usamos bases de datos diferentes (0 y 1) para separar los cachés.

## Uso en el Código

### 1. Cache de Leads

```python
from app.services.redis_client import cache_lead, get_cached_lead, invalidate_pattern

# Obtener lead con cache
@router.get("/leads/{lead_id}")
async def get_lead(lead_id: str, db: Session = Depends(get_db)):
    # Intentar obtener del cache
    cached = await get_cached_lead(lead_id)
    if cached:
        return cached
    
    # Si no está en cache, consultar BD
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead_dict = {
        "id": str(lead.id),
        "empresa": lead.empresa.nombre,
        "contacto": lead.contacto.email,
        "estado": lead.estado,
        # ... más campos
    }
    
    # Guardar en cache
    await cache_lead(lead_id, lead_dict)
    
    return lead_dict

# Invalidar cache cuando se actualiza
@router.patch("/leads/{lead_id}")
async def update_lead(lead_id: str, data: LeadUpdate, db: Session = Depends(get_db)):
    # Actualizar en BD
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    # ... actualizar campos ...
    db.commit()
    
    # Invalidar cache de este lead
    await delete_cache(f"lead:{lead_id}")
    
    # O invalidar todos los leads si es necesario
    await invalidate_pattern("lead:*")
    
    return {"message": "Lead updated"}
```

### 2. Cache de Resultados SurfSense

```python
from app.services.redis_client import cache_surfsense_result, get_cached_surfsense_result

# En el Agente CDAO
async def enriquecer_con_surfsense(self, empresa_nombre: str) -> dict:
    # Verificar cache primero (SurfSense puede ser costoso)
    cached = await get_cached_surfsense_result(empresa_nombre)
    if cached:
        print(f"[CDAO] Usando resultado cacheado para {empresa_nombre}")
        return cached
    
    # Si no está cacheado, consultar SurfSense
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SURFSENSE_URL}/enrich",
            json={"empresa": empresa_nombre}
        )
        result = response.json()
    
    # Cachear resultado por 2 horas
    await cache_surfsense_result(empresa_nombre, result, ttl=7200)
    
    return result
```

### 3. Funciones Disponibles

#### Operaciones Básicas

```python
from app.services.redis_client import get_cache, set_cache, delete_cache

# Guardar cualquier dato
await set_cache("mi_clave", {"dato": "valor"}, ttl=300)

# Obtener dato
data = await get_cache("mi_clave")

# Eliminar clave
await delete_cache("mi_clave")
```

#### Operaciones Específicas

```python
# Leads
await cache_lead(lead_id, lead_data)
lead = await get_cached_lead(lead_id)

# Oportunidades
await cache_oportunidad(oportunidad_id, oportunidad_data)
oportunidad = await get_cached_oportunidad(oportunidad_id)

# SurfSense
await cache_surfsense_result(empresa_name, result)
result = await get_cached_surfsense_result(empresa_name)
```

#### Invalidación Masiva

```python
from app.services.redis_client import invalidate_pattern

# Invalidar todos los leads
await invalidate_pattern("lead:*")

# Invalidar todas las oportunidades
await invalidate_pattern("oportunidad:*")

# Invalidar resultados de SurfSense
await invalidate_pattern("surfsense:*")
```

## Patrones de Clave

El sistema usa estos patrones de clave:

```
lead:<uuid>                    # Cache de lead individual
oportunidad:<uuid>             # Cache de oportunidad individual
surfsense:<empresa_normalizada> # Cache de resultado SurfSense
user:session:<token>           # (Futuro) Sesiones de usuario
```

## Monitoreo

### Verificar Conexión

```bash
# Conectar a Redis CLI
docker exec -it organis-redis redis-cli -a organis_redis_password

# Ver todas las claves
KEYS *

# Ver claves de leads
KEYS lead:*

# Ver TTL de una clave
TTL lead:123e4567-e89b-12d3-a456-426614174000

# Ver valor de una clave
GET lead:123e4567-e89b-12d3-a456-426614174000

# Ver estadísticas
INFO stats

# Limpiar base de datos (¡cuidado!)
FLUSHDB
```

### Métricas de Performance

```python
# Health check incluye estado de Redis
GET /health

# Respuesta:
{
    "status": "healthy",
    "database": "connected",
    "redis": "connected"
}
```

## Estrategia de Cache

### TTLs Recomendados

| Tipo de Dato | TTL | Razón |
|--------------|-----|-------|
| Lead | 1 hora (3600s) | Cambia frecuentemente |
| Oportunidad | 1 hora (3600s) | Cambia con cada etapa |
| Resultado SurfSense | 2 horas (7200s) | Costoso de obtener, cambia poco |
| Dashboard Metrics | 5 minutos (300s) | Necesita frescura |
| Sesión Usuario | 30 minutos (1800s) | Seguridad |

### Cuándo Invalidar

```python
# Invalidar cache cuando:
# 1. Se actualiza un registro
@router.patch("/leads/{id}")
async def update_lead(...):
    # ... actualizar BD ...
    await delete_cache(f"lead:{id}")
    
# 2. Se crea un registro relacionado
@router.post("/oportunidades")
async def create_oportunidad(...):
    # ... crear oportunidad ...
    # Invalidar cache del lead asociado
    await delete_cache(f"lead:{lead_id}")
    
# 3. Operaciones masivas
@router.post("/leads/import")
async def import_leads(...):
    # ... importar leads ...
    # Invalidar todos
    await invalidate_pattern("lead:*")
```

## Troubleshooting

### Redis no conecta

```bash
# Verificar que el contenedor esté corriendo
docker ps | grep redis

# Ver logs de Redis
docker logs organis-redis

# Reiniciar Redis
docker-compose restart redis
```

### Cache no funciona

```python
# Agregar logs para debug
async def get_lead(lead_id: str):
    cached = await get_cached_lead(lead_id)
    if cached:
        print(f"✅ Cache HIT para lead {lead_id}")
        return cached
    else:
        print(f"❌ Cache MISS para lead {lead_id}")
        # ... consultar BD ...
```

### Limpiar cache manualmente

```bash
# Conectar a Redis
docker exec -it organis-redis redis-cli -a organis_redis_password

# Limpiar todas las claves de leads
EVAL "return redis.call('del', unpack(redis.call('keys', 'lead:*')))" 0

# O desde Python
from app.services.redis_client import invalidate_pattern
await invalidate_pattern("lead:*")
```

## Best Practices

1. **Siempre usar TTL**: No dejar claves eternas
2. **Invalidar al actualizar**: Mantener consistencia con BD
3. **Cachear lecturas frecuentes**: No todo necesita cache
4. **Monitorear hit rate**: Si es <50%, revisar estrategia
5. **Usar patrones consistentes**: Facilita debugging

## Referencias

- [Redis Commands](https://redis.io/commands/)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [Caching Patterns](https://redis.io/docs/manual/patterns/)

---

**Última actualización**: 31 de octubre de 2025
