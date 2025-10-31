"""
Agente CDAO (Chief Data & Analytics Officer)
Responsable de:
1. Enriquecer leads con información externa (SurfSense)
2. Analizar viabilidad comercial
3. Crear oportunidades de venta
4. Enviar al Agente de Ventas
"""
import os
import asyncio
import httpx
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

# URLs de servicios externos
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")
SURFSENSE_URL = os.getenv("SURFSENSE_URL", "http://localhost:8002")

class EnriquecerLeadsBehaviour(CyclicBehaviour):
    """Comportamiento que enriquece leads con información externa"""
    
    async def run(self):
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                body = json.loads(msg.body)
                action = body.get("action")
                lead_id = body.get("lead_id")
                
                if action == "enriquecer_lead":
                    await self.enriquecer_lead(lead_id)
                    
            except Exception as e:
                print(f"[CDAO] Error procesando mensaje: {e}")
    
    async def enriquecer_lead(self, lead_id: str):
        """
        Enriquece el lead usando SurfSense y crea una oportunidad si procede
        """
        print(f"[CDAO] Enriqueciendo lead {lead_id}")
        
        try:
            async with httpx.AsyncClient() as client:
                # 1. Obtener datos del lead
                lead_response = await client.get(f"{GATEWAY_URL}/api/v1/leads/{lead_id}")
                if lead_response.status_code != 200:
                    print(f"[CDAO] Error obteniendo lead")
                    return
                
                lead = lead_response.json()
                empresa_nombre = lead.get("empresa")
                
                # 2. Consultar SurfSense para enriquecer información
                info_enriquecida = await self.consultar_surfsense(empresa_nombre, lead.get("sitio_web"))
                
                # 3. Actualizar lead con información enriquecida
                await self.actualizar_lead_enriquecido(lead_id, info_enriquecida)
                
                # 4. Analizar viabilidad y crear oportunidad
                if self.es_oportunidad_viable(lead, info_enriquecida):
                    oportunidad_id = await self.crear_oportunidad(lead, info_enriquecida)
                    
                    # 5. Enviar al Agente de Ventas
                    await self.enviar_a_ventas(oportunidad_id)
                else:
                    await self.actualizar_lead_estado(lead_id, "descartado", "No cumple criterios de viabilidad")
                    
        except Exception as e:
            print(f"[CDAO] Error enriqueciendo lead: {e}")
    
    async def consultar_surfsense(self, empresa: str, sitio_web: str = None) -> dict:
        """
        Consulta SurfSense para obtener información adicional de la empresa
        """
        print(f"[CDAO] Consultando SurfSense para {empresa}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "empresa": empresa,
                    "sitio_web": sitio_web
                }
                
                response = await client.post(
                    f"{SURFSENSE_URL}/api/enrich",
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"[CDAO] SurfSense respondió con error: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"[CDAO] Error consultando SurfSense: {e}")
            return {}
    
    def es_oportunidad_viable(self, lead: dict, info_enriquecida: dict) -> bool:
        """
        Analiza si el lead cumple criterios para convertirse en oportunidad
        """
        # Criterios básicos de viabilidad
        tiene_email = bool(lead.get("email"))
        tiene_empresa = bool(lead.get("empresa"))
        tiene_enriquecimiento = bool(info_enriquecida)
        
        # Aquí se pueden añadir más criterios basados en la información enriquecida
        # Por ejemplo: tamaño de empresa, industria, ubicación, etc.
        
        return tiene_email and tiene_empresa
    
    async def actualizar_lead_enriquecido(self, lead_id: str, info_enriquecida: dict):
        """Actualiza el lead con la información enriquecida"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "estado": "enriquecido",
                    "datos_enriquecidos": json.dumps(info_enriquecida)
                }
                
                await client.patch(
                    f"{GATEWAY_URL}/api/v1/leads/{lead_id}",
                    json=payload
                )
                print(f"[CDAO] Lead {lead_id} enriquecido exitosamente")
                
        except Exception as e:
            print(f"[CDAO] Error actualizando lead: {e}")
    
    async def crear_oportunidad(self, lead: dict, info_enriquecida: dict) -> str:
        """
        Crea una oportunidad de venta a partir del lead enriquecido
        """
        try:
            async with httpx.AsyncClient() as client:
                # Preparar datos de la oportunidad
                oportunidad_data = {
                    "lead_id": lead["id"],
                    "empresa_id": lead.get("empresa_id"),
                    "titulo": f"Oportunidad - {lead.get('empresa', 'Sin nombre')}",
                    "descripcion": f"Generada automáticamente desde lead {lead['id']}",
                    "valor_estimado": self.estimar_valor(info_enriquecida),
                    "probabilidad": 0.3,  # Probabilidad inicial
                    "etapa": "prospección",
                    "fuente": lead.get("fuente", "desconocido")
                }
                
                response = await client.post(
                    f"{GATEWAY_URL}/api/v1/oportunidades",
                    json=oportunidad_data
                )
                
                if response.status_code == 201:
                    oportunidad = response.json()
                    print(f"[CDAO] Oportunidad creada: {oportunidad['id']}")
                    return oportunidad["id"]
                else:
                    print(f"[CDAO] Error creando oportunidad: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"[CDAO] Error creando oportunidad: {e}")
            return None
    
    def estimar_valor(self, info_enriquecida: dict) -> float:
        """
        Estima el valor de la oportunidad basándose en la información enriquecida
        """
        # Valor base
        valor = 10000.0
        
        # Ajustar según información disponible
        if info_enriquecida.get("tamaño_empresa") == "grande":
            valor *= 3
        elif info_enriquecida.get("tamaño_empresa") == "mediana":
            valor *= 1.5
        
        return valor
    
    async def enviar_a_ventas(self, oportunidad_id: str):
        """Notifica al Agente de Ventas sobre la nueva oportunidad"""
        print(f"[CDAO] Enviando oportunidad {oportunidad_id} a Ventas")
        
        ventas_jid = self.agent.ventas_jid
        
        msg = Message(to=ventas_jid)
        msg.set_metadata("performative", "inform")
        msg.body = json.dumps({
            "action": "nueva_oportunidad",
            "oportunidad_id": oportunidad_id
        })
        
        await self.send(msg)
    
    async def actualizar_lead_estado(self, lead_id: str, estado: str, motivo: str = None):
        """Actualiza el estado de un lead"""
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
            print(f"[CDAO] Error actualizando estado: {e}")


class AgenteCDAO(Agent):
    """
    Agente CDAO - Chief Data & Analytics Officer
    Enriquece leads y crea oportunidades
    """
    
    def __init__(self, jid, password, ventas_jid=None):
        super().__init__(jid, password)
        self.ventas_jid = ventas_jid
    
    async def setup(self):
        """Configuración inicial del agente"""
        print(f"[CDAO] Agente iniciado: {self.jid}")
        
        behaviour = EnriquecerLeadsBehaviour()
        self.add_behaviour(behaviour)
