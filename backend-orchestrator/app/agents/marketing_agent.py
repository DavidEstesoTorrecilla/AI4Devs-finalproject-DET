"""
Agente de Marketing - Primer punto de contacto
Responsable de:
1. Recibir y validar nuevos leads
2. Verificar duplicados
3. Enviar al CDAO para enriquecimiento
"""
import os
import asyncio
import httpx
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

# URL del Gateway
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

class ProcesarLeadsBehaviour(CyclicBehaviour):
    """Comportamiento cíclico que procesa mensajes sobre nuevos leads"""
    
    async def run(self):
        # Esperar mensajes de otros agentes o del sistema
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                body = json.loads(msg.body)
                lead_id = body.get("lead_id")
                action = body.get("action")
                
                if action == "procesar_nuevo_lead":
                    await self.validar_lead(lead_id)
                    
            except Exception as e:
                print(f"[Marketing] Error procesando mensaje: {e}")
    
    async def validar_lead(self, lead_id: str):
        """
        Valida el lead y lo envía al CDAO para enriquecimiento
        """
        print(f"[Marketing] Validando lead {lead_id}")
        
        try:
            async with httpx.AsyncClient() as client:
                # Obtener datos del lead desde el Gateway
                response = await client.get(f"{GATEWAY_URL}/api/v1/leads/{lead_id}")
                
                if response.status_code != 200:
                    print(f"[Marketing] Error obteniendo lead: {response.status_code}")
                    return
                
                lead_data = response.json()
                
                # Validaciones básicas
                if not lead_data.get("email"):
                    print(f"[Marketing] Lead sin email válido")
                    await self.actualizar_lead_estado(lead_id, "rechazado", "Email no válido")
                    return
                
                # Enviar mensaje al CDAO para enriquecimiento
                await self.enviar_a_cdao(lead_id)
                
        except Exception as e:
            print(f"[Marketing] Error validando lead: {e}")
    
    async def enviar_a_cdao(self, lead_id: str):
        """Envía el lead al Agente CDAO para enriquecimiento"""
        print(f"[Marketing] Enviando lead {lead_id} al CDAO")
        
        # Obtener JID del agente CDAO
        cdao_jid = self.agent.cdao_jid
        
        msg = Message(to=cdao_jid)
        msg.set_metadata("performative", "request")
        msg.body = json.dumps({
            "action": "enriquecer_lead",
            "lead_id": lead_id
        })
        
        await self.send(msg)
    
    async def actualizar_lead_estado(self, lead_id: str, estado: str, motivo: str = None):
        """Actualiza el estado de un lead en el Gateway"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {"estado": estado}
                if motivo:
                    payload["observaciones"] = motivo
                    
                await client.patch(
                    f"{GATEWAY_URL}/api/v1/leads/{lead_id}",
                    json=payload
                )
        except Exception as e:
            print(f"[Marketing] Error actualizando estado del lead: {e}")


class AgenteMarketing(Agent):
    """
    Agente de Marketing - Punto de entrada de leads
    """
    
    def __init__(self, jid, password, cdao_jid=None):
        super().__init__(jid, password)
        self.cdao_jid = cdao_jid
    
    async def setup(self):
        """Configuración inicial del agente"""
        print(f"[Marketing] Agente iniciado: {self.jid}")
        
        # Añadir comportamiento cíclico
        behaviour = ProcesarLeadsBehaviour()
        self.add_behaviour(behaviour)
    
    async def procesar_nuevo_lead(self, lead_id: str):
        """
        Método público llamado desde el API para procesar un nuevo lead
        """
        # Enviarse un mensaje a sí mismo para procesarlo en el comportamiento
        msg = Message(to=str(self.jid))
        msg.body = json.dumps({
            "action": "procesar_nuevo_lead",
            "lead_id": lead_id
        })
        await self.send(msg)
