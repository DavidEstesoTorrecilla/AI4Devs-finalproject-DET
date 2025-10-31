# Estructura del Proyecto Organis.AI (EMASAI)

## 📁 Descripción General

Este documento describe la estructura completa del proyecto **Organis.AI** (nombre comercial: **EMASAI**), un sistema Multi-Agente de IA para automatización del ciclo de ventas B2B.

## 🏗️ Arquitectura del Proyecto

```
AI4Devs-finalproject-DET/
│
├── backend-gateway/              # Gateway API REST (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Punto de entrada FastAPI
│   │   ├── db/
│   │   │   ├── database.py      # Configuración SQLAlchemy
│   │   │   └── models.py        # Modelos ORM (empresas, contactos, leads, etc.)
│   │   ├── routers/
│   │   │   ├── leads.py         # CRUD de leads
│   │   │   ├── oportunidades.py # CRUD de oportunidades
│   │   │   ├── facturas.py      # CRUD de facturas
│   │   │   └── dashboard.py     # Métricas y estadísticas
│   │   ├── schemas/
│   │   │   ├── lead.py          # Schemas Pydantic
│   │   │   ├── oportunidad.py
│   │   │   └── factura.py
│   │   └── services/
│   │       └── orchestrator_client.py  # Cliente HTTP para Orchestrator
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── backend-orchestrator/         # Orchestrator Multi-Agente (SPADE)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Punto de entrada SPADE + FastAPI
│   │   ├── api.py               # Endpoints de control del orchestrator
│   │   └── agents/
│   │       ├── __init__.py
│   │       ├── marketing_agent.py   # Agente de Marketing
│   │       ├── cdao_agent.py        # Agente CDAO (enriquecimiento)
│   │       ├── ventas_agent.py      # Agente de Ventas
│   │       └── finanzas_agent.py    # Agente Financiero
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── apps/
│   └── frontend/                 # Frontend React + Vite
│       ├── src/
│       │   ├── components/      # Componentes reutilizables
│       │   ├── features/        # Features por módulo
│       │   │   ├── auth/
│       │   │   ├── leads/
│       │   │   ├── machines/
│       │   │   └── alerts/
│       │   ├── hooks/           # Custom hooks
│       │   ├── stores/          # Estado global
│       │   └── lib/             # Utilidades
│       ├── package.json
│       ├── vite.config.ts
│       └── tailwind.config.js
│
├── external-services/
│   └── surfsense/               # Servicio RAG (pendiente integración)
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile.backend   # (obsoleto - usar backend-gateway/Dockerfile)
│   │   └── Dockerfile.frontend
│   └── scripts/
│       ├── setup-local.sh
│       └── setup-local.bat
│
├── packages/
│   └── shared-types/            # Tipos TypeScript compartidos
│       ├── src/
│       │   └── index.ts
│       └── package.json
│
├── docs/                        # Documentación
│   ├── api/
│   ├── architecture/
│   └── screenshots/
│
├── Documentacion/               # Documentación de diseño
│   ├── prompts_documentacion1.md
│   └── SSD EMASAIv2.md         # Documento de diseño principal
│
├── docker-compose.yml           # Orquestación de servicios
├── pnpm-workspace.yaml          # Configuración workspace monorepo
├── package.json                 # Root package.json
└── readme.md                    # Documentación principal

```

## 🔧 Servicios Docker

### Servicios en `docker-compose.yml`:

1. **postgres**: PostgreSQL 15 con extensión pgvector para RAG
2. **xmpp**: Servidor ejabberd para comunicación entre agentes SPADE
3. **gateway**: API REST FastAPI (puerto 8000)
4. **orchestrator**: Sistema Multi-Agente SPADE (puerto 8001)
5. **frontend**: React + Vite (puerto 5173)

## 🤖 Agentes SPADE

### 1. Agente de Marketing (`marketing_agent.py`)
**Responsabilidades:**
- Recibir nuevos leads desde formularios, API externa, etc.
- Validar información básica (email, nombre de empresa)
- Detectar duplicados
- Enviar al Agente CDAO para enriquecimiento

**Comportamientos SPADE:**
- `ProcesarLeadsBehaviour`: Recibe mensajes sobre nuevos leads y los valida

**Comunicación:**
- Recibe: Comandos desde Gateway API (`/orchestrator/enriquecer-lead`)
- Envía: Mensajes XMPP al Agente CDAO

### 2. Agente CDAO (`cdao_agent.py`)
**Responsabilidades:**
- Enriquecer leads con información externa (SurfSense RAG)
- Analizar viabilidad comercial del lead
- Crear oportunidades de venta si el lead es viable
- Enviar al Agente de Ventas

**Comportamientos SPADE:**
- `EnriquecerLeadsBehaviour`: Procesa leads, consulta SurfSense, crea oportunidades

**Comunicación:**
- Recibe: Mensajes XMPP del Agente de Marketing
- Envía: Mensajes XMPP al Agente de Ventas

### 3. Agente de Ventas (`ventas_agent.py`)
**Responsabilidades:**
- Gestionar pipeline de oportunidades
- Actualizar etapas del proceso comercial
- Calcular probabilidad de cierre según etapa
- Notificar oportunidades ganadas al Agente Financiero

**Comportamientos SPADE:**
- `GestionarOportunidadesBehaviour`: Gestiona ciclo de vida de oportunidades

**Comunicación:**
- Recibe: Mensajes XMPP del Agente CDAO
- Envía: Mensajes XMPP al Agente Financiero

### 4. Agente Financiero (`finanzas_agent.py`)
**Responsabilidades:**
- Generar facturas automáticamente cuando se gana una oportunidad
- Calcular descuentos según reglas de negocio
- Aplicar IVA y calcular totales
- Generar número de factura secuencial

**Comportamientos SPADE:**
- `GenerarFacturasBehaviour`: Genera y gestiona facturas

**Comunicación:**
- Recibe: Mensajes XMPP del Agente de Ventas y comandos desde Gateway

## 📊 Base de Datos

### Modelos principales (`backend-gateway/app/db/models.py`):

1. **Empresa**: Información de empresas cliente
2. **Contacto**: Personas de contacto en empresas
3. **Lead**: Leads captados (antes de cualificar)
4. **Oportunidad**: Oportunidades de venta cualificadas
5. **Factura**: Facturas generadas
6. **TareaAgente**: Tareas asignadas a agentes

### Relaciones:
- Empresa 1:N Contacto
- Empresa 1:N Lead
- Lead 1:1 Oportunidad
- Oportunidad 1:1 Factura
- Oportunidad 1:N TareaAgente

## 🔄 Flujo de Datos

### Flujo principal de un lead:

```
1. Lead ingresa al sistema
   ↓ (Gateway POST /api/v1/leads)
   
2. Gateway notifica al Orchestrator
   ↓ (HTTP POST /orchestrator/enriquecer-lead)
   
3. Agente Marketing valida el lead
   ↓ (XMPP message)
   
4. Agente CDAO enriquece con SurfSense
   ↓ (HTTP call to SurfSense)
   
5. CDAO crea oportunidad si viable
   ↓ (HTTP POST a Gateway + XMPP message)
   
6. Agente Ventas gestiona pipeline
   ↓ (Updates via Gateway API)
   
7. Si oportunidad es ganada
   ↓ (XMPP message)
   
8. Agente Finanzas genera factura
   ↓ (HTTP POST a Gateway)
```

## 🌐 APIs

### Gateway API (Puerto 8000):

**Endpoints principales:**
- `POST /api/v1/leads` - Crear nuevo lead
- `GET /api/v1/leads/{id}` - Obtener lead
- `PATCH /api/v1/leads/{id}` - Actualizar lead
- `GET /api/v1/oportunidades` - Listar oportunidades
- `PATCH /api/v1/oportunidades/{id}` - Actualizar oportunidad
- `POST /api/v1/facturas` - Crear factura
- `GET /api/v1/dashboard/metricas` - Métricas del dashboard

### Orchestrator API (Puerto 8001):

**Endpoints de control:**
- `POST /api/v1/orchestrator/enriquecer-lead` - Iniciar enriquecimiento
- `POST /api/v1/orchestrator/oportunidad-ganada` - Notificar venta ganada
- `GET /health` - Health check de agentes
- `GET /` - Estado del sistema

## 🚀 Próximos Pasos

### Pendientes de implementación:

1. **Frontend actualizado**:
   - Dashboard de ventas con pipeline visual
   - Componentes para leads, oportunidades, facturas
   - Actualizar shared-types con entidades correctas

2. **Integración SurfSense**:
   - Implementar cliente en `external-services/surfsense/`
   - Configurar embeddings para RAG
   - API de enriquecimiento de empresas

3. **Migraciones de base de datos**:
   - Configurar Alembic para SQLAlchemy
   - Scripts de inicialización de datos

4. **Testing**:
   - Tests unitarios de agentes
   - Tests de integración de API
   - Tests E2E de flujo completo

5. **Documentación**:
   - Swagger/OpenAPI para APIs
   - Diagramas de arquitectura actualizados
   - Guía de desarrollo

## 📝 Notas Importantes

- **EMASAI** es el nombre comercial, **Organis.AI** es el nombre técnico del proyecto
- Los agentes se comunican mediante **XMPP** (protocolo SPADE)
- El Gateway expone API REST para el frontend
- El Orchestrator coordina los agentes pero también expone API de control
- SurfSense es el servicio externo de RAG para enriquecimiento

## 🔐 Seguridad

- Variables de entorno en archivos `.env` (no commitear!)
- CORS configurado en Gateway y Orchestrator
- Autenticación JWT pendiente de implementar
- HTTPS en producción (configurar reverse proxy)

---

**Última actualización**: [Fecha]
**Versión**: 1.0.0
