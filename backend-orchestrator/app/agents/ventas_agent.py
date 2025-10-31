"""
Agente de Ventas
Responsable de:
1. Gestionar el pipeline de oportunidades
2. Actualizar etapas del proceso de venta
3. Notificar cuando una oportunidad es ganada
4. Coordinar con el Agente Financiero
"""
import os
import asyncio
import httpx
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
from datetime import datetime, timedelta

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

class GestionarOportunidadesBehaviour(CyclicBehaviour):
    """Comportamiento que gestiona el ciclo de vida de oportunidades"""
    
    async def run(self):
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                body = json.loads(msg.body)
                action = body.get("action")
                oportunidad_id = body.get("oportunidad_id")
                
                if action == "nueva_oportunidad":
                    await self.iniciar_seguimiento(oportunidad_id)
                elif action == "actualizar_etapa":
                    nueva_etapa = body.get("etapa")
                    await self.actualizar_etapa(oportunidad_id, nueva_etapa)
                    
            except Exception as e:
                print(f"[Ventas] Error procesando mensaje: {e}")
    
    async def iniciar_seguimiento(self, oportunidad_id: str):
        """
        Inicia el seguimiento de una nueva oportunidad
        """
        print(f"[Ventas] Iniciando seguimiento de oportunidad {oportunidad_id}")
        
        try:
            async with httpx.AsyncClient() as client:
                # Obtener datos de la oportunidad
                response = await client.get(
                    f"{GATEWAY_URL}/api/v1/oportunidades/{oportunidad_id}"
                )
                
                if response.status_code == 200:
                    oportunidad = response.json()
                    
                    # Crear tarea para el seguimiento
                    await self.crear_tarea_seguimiento(oportunidad)
                    
                    # Actualizar probabilidad según etapa
                    await self.recalcular_probabilidad(oportunidad_id, oportunidad["etapa"])
                    
        except Exception as e:
            print(f"[Ventas] Error iniciando seguimiento: {e}")
    
    async def actualizar_etapa(self, oportunidad_id: str, nueva_etapa: str):
        """
        Actualiza la etapa de una oportunidad y realiza acciones correspondientes
        """
        print(f"[Ventas] Actualizando oportunidad {oportunidad_id} a etapa {nueva_etapa}")
        
        try:
            async with httpx.AsyncClient() as client:
                # Actualizar etapa en el Gateway
                payload = {"etapa": nueva_etapa}
                
                response = await client.patch(
                    f"{GATEWAY_URL}/api/v1/oportunidades/{oportunidad_id}",
                    json=payload
                )
                
                if response.status_code == 200:
                    # Recalcular probabilidad según nueva etapa
                    await self.recalcular_probabilidad(oportunidad_id, nueva_etapa)
                    
                    # Si la oportunidad fue ganada, notificar a Finanzas
                    if nueva_etapa == "ganada":
                        await self.notificar_oportunidad_ganada(oportunidad_id)
                    
        except Exception as e:
            print(f"[Ventas] Error actualizando etapa: {e}")
    
    async def recalcular_probabilidad(self, oportunidad_id: str, etapa: str):
        """
        Recalcula la probabilidad de éxito según la etapa
        """
        # Mapeo de etapas a probabilidades
        probabilidades = {
            "prospección": 0.1,
            "calificación": 0.25,
            "propuesta": 0.5,
            "negociación": 0.75,
            "ganada": 1.0,
            "perdida": 0.0
        }
        
        nueva_probabilidad = probabilidades.get(etapa, 0.1)
        
        try:
            async with httpx.AsyncClient() as client:
                await client.patch(
                    f"{GATEWAY_URL}/api/v1/oportunidades/{oportunidad_id}",
                    json={"probabilidad": nueva_probabilidad}
                )
                print(f"[Ventas] Probabilidad actualizada a {nueva_probabilidad}")
                
        except Exception as e:
            print(f"[Ventas] Error actualizando probabilidad: {e}")
    
    async def crear_tarea_seguimiento(self, oportunidad: dict):
        """
        Crea una tarea de seguimiento para la oportunidad
        """
        try:
            async with httpx.AsyncClient() as client:
                tarea = {
                    "oportunidad_id": oportunidad["id"],
                    "agente": "ventas",
                    "tipo": "seguimiento",
                    "descripcion": f"Seguimiento de oportunidad {oportunidad['titulo']}",
                    "prioridad": "media",
                    "estado": "pendiente"
                }
                
                await client.post(
                    f"{GATEWAY_URL}/api/v1/tareas",
                    json=tarea
                )
                print(f"[Ventas] Tarea de seguimiento creada")
                
        except Exception as e:
            print(f"[Ventas] Error creando tarea: {e}")
    
    async def notificar_oportunidad_ganada(self, oportunidad_id: str):
        """
        Notifica al Agente Financiero que una oportunidad fue ganada
        """
        print(f"[Ventas] Notificando oportunidad ganada {oportunidad_id} a Finanzas")
        
        finanzas_jid = self.agent.finanzas_jid
        
        msg = Message(to=finanzas_jid)
        msg.set_metadata("performative", "inform")
        msg.body = json.dumps({
            "action": "generar_factura",
            "oportunidad_id": oportunidad_id
        })
        
        await self.send(msg)


class AgenteVentas(Agent):
    """
    Agente de Ventas - Gestiona el pipeline comercial
    """
    
    def __init__(self, jid, password, finanzas_jid=None):
        super().__init__(jid, password)
        self.finanzas_jid = finanzas_jid
    
    async def setup(self):
        """Configuración inicial del agente"""
        print(f"[Ventas] Agente iniciado: {self.jid}")
        
        behaviour = GestionarOportunidadesBehaviour()
        self.add_behaviour(behaviour)
