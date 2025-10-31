"""
Agentes SPADE para el sistema Organis.AI
"""
from .marketing_agent import AgenteMarketing
from .cdao_agent import AgenteCDAO
from .ventas_agent import AgenteVentas
from .finanzas_agent import AgenteFinanzas

__all__ = [
    'AgenteMarketing',
    'AgenteCDAO',
    'AgenteVentas',
    'AgenteFinanzas'
]
