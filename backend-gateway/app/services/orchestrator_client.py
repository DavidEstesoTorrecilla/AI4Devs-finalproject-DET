"""
Cliente para comunicación con el Orquestador MAS (SPADE)
"""
import httpx
import os

class OrquestradorClient:
    """Cliente HTTP para comunicarse con el backend-orchestrator"""
    
    def __init__(self):
        self.base_url = os.getenv(
            "ORCHESTRATOR_URL",
            "http://localhost:8001"
        )
        self.timeout = 30.0
    
    async def solicitar_enriquecimiento(self, lead_id: str):
        """
        Solicita al orquestador que enriquezca un lead.
        Esto activa al Agente de Marketing y luego al CDAO.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/orchestrator/enriquecer-lead",
                json={"lead_id": lead_id}
            )
            response.raise_for_status()
            return response.json()
    
    async def notificar_cierre_ganado(self, oportunidad_id: str):
        """
        Notifica al orquestador que una oportunidad fue cerrada.
        Esto activa al Agente Financiero para generar factura.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/orchestrator/oportunidad-ganada",
                json={"oportunidad_id": oportunidad_id}
            )
            response.raise_for_status()
            return response.json()
