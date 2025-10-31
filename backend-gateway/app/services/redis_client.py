"""
Cliente Redis para caché
Gestiona conexión y operaciones de caché para el Gateway
"""
import os
import json
from typing import Optional, Any
import redis.asyncio as redis
from redis.asyncio import Redis

# Configuración
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_TTL = int(os.getenv("REDIS_TTL", "3600"))  # 1 hora por defecto

# Cliente Redis global
_redis_client: Optional[Redis] = None


async def get_redis_client() -> Redis:
    """
    Obtiene o crea el cliente Redis
    """
    global _redis_client
    
    if _redis_client is None:
        _redis_client = await redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    return _redis_client


async def close_redis_client():
    """
    Cierra la conexión de Redis
    """
    global _redis_client
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


async def get_cache(key: str) -> Optional[Any]:
    """
    Obtiene un valor del caché
    
    Args:
        key: Clave del caché
    
    Returns:
        Valor deserializado o None si no existe
    """
    try:
        client = await get_redis_client()
        value = await client.get(key)
        
        if value:
            return json.loads(value)
        
        return None
    except Exception as e:
        print(f"Error obteniendo del caché: {e}")
        return None


async def set_cache(key: str, value: Any, ttl: int = REDIS_TTL) -> bool:
    """
    Guarda un valor en el caché
    
    Args:
        key: Clave del caché
        value: Valor a guardar (debe ser serializable a JSON)
        ttl: Tiempo de expiración en segundos
    
    Returns:
        True si se guardó correctamente
    """
    try:
        client = await get_redis_client()
        serialized = json.dumps(value, default=str)
        await client.setex(key, ttl, serialized)
        return True
    except Exception as e:
        print(f"Error guardando en caché: {e}")
        return False


async def delete_cache(key: str) -> bool:
    """
    Elimina una clave del caché
    
    Args:
        key: Clave a eliminar
    
    Returns:
        True si se eliminó correctamente
    """
    try:
        client = await get_redis_client()
        await client.delete(key)
        return True
    except Exception as e:
        print(f"Error eliminando del caché: {e}")
        return False


async def invalidate_pattern(pattern: str) -> int:
    """
    Invalida todas las claves que coincidan con un patrón
    
    Args:
        pattern: Patrón de búsqueda (ej: "leads:*")
    
    Returns:
        Número de claves eliminadas
    """
    try:
        client = await get_redis_client()
        keys = []
        
        async for key in client.scan_iter(match=pattern):
            keys.append(key)
        
        if keys:
            return await client.delete(*keys)
        
        return 0
    except Exception as e:
        print(f"Error invalidando patrón: {e}")
        return 0


# Funciones de utilidad para casos comunes

async def cache_lead(lead_id: str, lead_data: dict, ttl: int = REDIS_TTL) -> bool:
    """Cachea información de un lead"""
    return await set_cache(f"lead:{lead_id}", lead_data, ttl)


async def get_cached_lead(lead_id: str) -> Optional[dict]:
    """Obtiene un lead del caché"""
    return await get_cache(f"lead:{lead_id}")


async def cache_oportunidad(oportunidad_id: str, oportunidad_data: dict, ttl: int = REDIS_TTL) -> bool:
    """Cachea información de una oportunidad"""
    return await set_cache(f"oportunidad:{oportunidad_id}", oportunidad_data, ttl)


async def get_cached_oportunidad(oportunidad_id: str) -> Optional[dict]:
    """Obtiene una oportunidad del caché"""
    return await get_cache(f"oportunidad:{oportunidad_id}")


async def cache_surfsense_result(empresa_name: str, result: dict, ttl: int = 7200) -> bool:
    """
    Cachea resultado de SurfSense (2 horas por defecto)
    """
    key = f"surfsense:{empresa_name.lower().replace(' ', '_')}"
    return await set_cache(key, result, ttl)


async def get_cached_surfsense_result(empresa_name: str) -> Optional[dict]:
    """
    Obtiene resultado cacheado de SurfSense
    """
    key = f"surfsense:{empresa_name.lower().replace(' ', '_')}"
    return await get_cache(key)
