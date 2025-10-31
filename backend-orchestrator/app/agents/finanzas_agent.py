"""
Agente Financiero
Responsable de:
1. Generar facturas cuando se ganan oportunidades
2. Calcular montos y aplicar descuentos
3. Gestionar el estado de facturas
4. Reportar métricas financieras
"""
import os
import asyncio
import httpx
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
from datetime import datetime, timedelta
from decimal import Decimal

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

class GenerarFacturasBehaviour(CyclicBehaviour):
    """Comportamiento que genera y gestiona facturas"""
    
    async def run(self):
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                body = json.loads(msg.body)
                action = body.get("action")
                oportunidad_id = body.get("oportunidad_id")
                
                if action == "generar_factura":
                    await self.generar_factura(oportunidad_id)
                    
            except Exception as e:
                print(f"[Finanzas] Error procesando mensaje: {e}")
    
    async def generar_factura(self, oportunidad_id: str):
        """
        Genera una factura a partir de una oportunidad ganada
        """
        print(f"[Finanzas] Generando factura para oportunidad {oportunidad_id}")
        
        try:
            async with httpx.AsyncClient() as client:
                # 1. Obtener datos de la oportunidad
                response = await client.get(
                    f"{GATEWAY_URL}/api/v1/oportunidades/{oportunidad_id}"
                )
                
                if response.status_code != 200:
                    print(f"[Finanzas] Error obteniendo oportunidad")
                    return
                
                oportunidad = response.json()
                
                # 2. Obtener datos de la empresa
                empresa_response = await client.get(
                    f"{GATEWAY_URL}/api/v1/empresas/{oportunidad['empresa_id']}"
                )
                
                if empresa_response.status_code != 200:
                    print(f"[Finanzas] Error obteniendo empresa")
                    return
                
                empresa = empresa_response.json()
                
                # 3. Calcular montos
                subtotal = float(oportunidad.get("valor_estimado", 0))
                descuento = self.calcular_descuento(oportunidad)
                iva = (subtotal - descuento) * 0.21  # IVA 21%
                total = subtotal - descuento + iva
                
                # 4. Generar número de factura
                numero_factura = await self.generar_numero_factura()
                
                # 5. Crear la factura
                factura_data = {
                    "numero": numero_factura,
                    "oportunidad_id": oportunidad_id,
                    "empresa_id": oportunidad["empresa_id"],
                    "fecha_emision": datetime.now().isoformat(),
                    "fecha_vencimiento": (datetime.now() + timedelta(days=30)).isoformat(),
                    "subtotal": subtotal,
                    "descuento": descuento,
                    "iva": iva,
                    "total": total,
                    "estado": "emitida",
                    "metodo_pago": empresa.get("metodo_pago_preferido", "transferencia"),
                    "condiciones_pago": "30 días",
                    "observaciones": f"Factura generada automáticamente para {oportunidad['titulo']}"
                }
                
                factura_response = await client.post(
                    f"{GATEWAY_URL}/api/v1/facturas",
                    json=factura_data
                )
                
                if factura_response.status_code == 201:
                    factura = factura_response.json()
                    print(f"[Finanzas] Factura {numero_factura} generada exitosamente")
                    
                    # Crear tarea de seguimiento de pago
                    await self.crear_tarea_seguimiento_pago(factura["id"])
                else:
                    print(f"[Finanzas] Error creando factura: {factura_response.status_code}")
                    
        except Exception as e:
            print(f"[Finanzas] Error generando factura: {e}")
    
    def calcular_descuento(self, oportunidad: dict) -> float:
        """
        Calcula el descuento aplicable basado en reglas de negocio
        """
        descuento = 0.0
        valor = float(oportunidad.get("valor_estimado", 0))
        
        # Ejemplo: Descuento por volumen
        if valor > 50000:
            descuento = valor * 0.15  # 15% descuento
        elif valor > 25000:
            descuento = valor * 0.10  # 10% descuento
        elif valor > 10000:
            descuento = valor * 0.05  # 5% descuento
        
        return descuento
    
    async def generar_numero_factura(self) -> str:
        """
        Genera un número de factura único secuencial
        """
        try:
            async with httpx.AsyncClient() as client:
                # Obtener última factura para generar número secuencial
                response = await client.get(f"{GATEWAY_URL}/api/v1/facturas?limit=1&sort=desc")
                
                if response.status_code == 200:
                    facturas = response.json()
                    if facturas:
                        ultimo_numero = facturas[0].get("numero", "F-0000")
                        numero = int(ultimo_numero.split("-")[1]) + 1
                        return f"F-{numero:04d}"
                
                # Si no hay facturas previas, empezar desde 1
                return "F-0001"
                
        except Exception as e:
            print(f"[Finanzas] Error generando número de factura: {e}")
            # Generar número aleatorio como fallback
            import random
            return f"F-{random.randint(1000, 9999)}"
    
    async def crear_tarea_seguimiento_pago(self, factura_id: str):
        """
        Crea una tarea para hacer seguimiento del pago de la factura
        """
        try:
            async with httpx.AsyncClient() as client:
                tarea = {
                    "factura_id": factura_id,
                    "agente": "finanzas",
                    "tipo": "seguimiento_pago",
                    "descripcion": f"Seguimiento de pago de factura {factura_id}",
                    "prioridad": "alta",
                    "estado": "pendiente"
                }
                
                await client.post(
                    f"{GATEWAY_URL}/api/v1/tareas",
                    json=tarea
                )
                print(f"[Finanzas] Tarea de seguimiento de pago creada")
                
        except Exception as e:
            print(f"[Finanzas] Error creando tarea: {e}")


class AgenteFinanzas(Agent):
    """
    Agente Financiero - Gestiona facturas y pagos
    """
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
    
    async def setup(self):
        """Configuración inicial del agente"""
        print(f"[Finanzas] Agente iniciado: {self.jid}")
        
        behaviour = GenerarFacturasBehaviour()
        self.add_behaviour(behaviour)
    
    async def generar_factura(self, oportunidad_id: str):
        """
        Método público llamado desde el API para generar una factura
        """
        msg = Message(to=str(self.jid))
        msg.body = json.dumps({
            "action": "generar_factura",
            "oportunidad_id": oportunidad_id
        })
        await self.send(msg)
