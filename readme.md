## Índice

0. [Ficha del proyecto](#0-ficha-del-proyecto)
1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 0. Ficha del proyecto

### **0.1. Tu nombre completo:**
[Tu nombre]

### **0.2. Nombre del proyecto:**
**Organis.AI** (Nombre comercial: **EMASAI**)

### **0.3. Descripción breve del proyecto:**
Sistema Multi-Agente de Inteligencia Artificial para automatización del ciclo de ventas B2B. Utiliza agentes autónomos (Marketing, CDAO, Ventas, Finanzas) que colaboran para captar, enriquecer, cualificar y convertir leads en oportunidades de negocio mediante enriquecimiento automático con RAG (SurfSense) y gestión inteligente del pipeline comercial.

### **0.4. URL del proyecto:**
[URL a completar]

### 0.5. URL o archivo comprimido del repositorio
[Repositorio a completar]

---

## 1. Descripción general del producto

### **1.1. Objetivo:**

**Organis.AI (EMASAI)** es un sistema de automatización de ventas B2B basado en arquitectura Multi-Agente que optimiza el ciclo completo de ventas mediante Inteligencia Artificial.

**Valor que aporta:**
- **Automatización inteligente**: Reduce hasta un 70% el tiempo dedicado a tareas manuales de calificación y seguimiento de leads
- **Enriquecimiento automático**: Utiliza RAG (SurfSense) para obtener información contextual de empresas y contactos desde múltiples fuentes
- **Decisiones basadas en datos**: Los agentes analizan información enriquecida para priorizar oportunidades con mayor probabilidad de éxito
- **Colaboración Multi-Agente**: 4 agentes especializados (Marketing, CDAO, Ventas, Finanzas) trabajan de forma coordinada

**Problemas que soluciona:**
1. **Pérdida de leads por falta de seguimiento**: Sistema automatizado que no pierde ningún lead
2. **Información incompleta**: Enriquecimiento automático de datos de contactos y empresas
3. **Priorización manual ineficiente**: Scoring automático de leads basado en IA
4. **Generación manual de documentos**: Facturas y propuestas generadas automáticamente

**Para quién:**
- Empresas B2B con equipos de ventas de 5-50 personas
- Gerentes de ventas que buscan optimizar su pipeline comercial
- Directores comerciales que necesitan visibilidad y métricas en tiempo real
- Equipos de marketing que quieren maximizar la conversión de leads

### **1.2. Características y funcionalidades principales:**

#### 🤖 **Sistema Multi-Agente Autónomo**
- **Agente de Marketing**: Captura y valida leads desde múltiples fuentes (formularios web, LinkedIn, eventos)
- **Agente CDAO**: Enriquece leads usando SurfSense RAG, analiza viabilidad comercial y crea oportunidades
- **Agente de Ventas**: Gestiona pipeline, actualiza etapas, calcula probabilidades de cierre
- **Agente Financiero**: Genera facturas automáticas, aplica descuentos, gestiona pagos

#### 🔍 **Enriquecimiento Automático con RAG**
- Integración con SurfSense para obtener información de empresas desde múltiples fuentes web
- Enriquecimiento automático: tamaño de empresa, sector, tecnologías utilizadas, noticias recientes
- Base de conocimiento vectorial para consultas contextuales sobre empresas y contactos

#### 📊 **Dashboard de Gestión Comercial**
- Vista de pipeline con etapas: Prospección → Calificación → Propuesta → Negociación → Ganada/Perdida
- Métricas en tiempo real: tasa de conversión, valor promedio, ciclo de venta
- Filtros por fuente, etapa, agente responsable, rango de fechas

#### 💼 **Gestión Inteligente de Oportunidades**
- Scoring automático de leads basado en información enriquecida
- Actualización automática de probabilidad según etapa del pipeline
- Recordatorios y tareas automáticas para seguimiento

#### 📝 **Generación Automática de Documentos**
- Facturas generadas automáticamente cuando se cierra una venta
- Aplicación automática de descuentos según reglas de negocio
- Exportación a PDF con branding personalizado

#### 🔔 **Sistema de Notificaciones**
- Alertas en tiempo real sobre leads nuevos, oportunidades avanzadas, facturas generadas
- Notificaciones de tareas pendientes para agentes comerciales
- Webhooks para integraciones externas

### **1.3. Diseño y experiencia de usuario:**

> Proporciona imágenes y/o videotutorial mostrando la experiencia del usuario desde que aterriza en la aplicación, pasando por todas las funcionalidades principales.

### **1.4. Instrucciones de instalación:**

#### **Requisitos previos:**
- **Python 3.11+** (para backend-gateway y backend-orchestrator)
- **Node.js 18+** y **pnpm 8+** (para frontend)
- **Docker y Docker Compose** (para servicios de infraestructura)
- **Git**

#### **Instalación con Docker Compose (Recomendado):**

```bash
# 1. Clonar el repositorio
git clone [URL_REPOSITORIO]
cd AI4Devs-finalproject-DET

# 2. Configurar variables de entorno
cp backend-gateway/.env.example backend-gateway/.env
cp backend-orchestrator/.env.example backend-orchestrator/.env

# 3. Levantar todos los servicios
docker-compose up -d

# 4. Verificar que todos los servicios estén corriendo
docker-compose ps

# Los servicios estarán disponibles en:
# - Frontend: http://localhost:5173
# - Gateway API: http://localhost:8000
# - Orchestrator API: http://localhost:8001
# - PostgreSQL: localhost:5432
# - XMPP Server: localhost:5222
```

#### **Instalación manual (Desarrollo):**

```bash
# 1. Clonar repositorio
git clone [URL_REPOSITORIO]
cd AI4Devs-finalproject-DET

# 2. Instalar dependencias del Gateway
cd backend-gateway
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt

# 3. Instalar dependencias del Orchestrator
cd ../backend-orchestrator
python -m venv venv
# Activar venv como arriba
pip install -r requirements.txt

# 4. Instalar dependencias del Frontend
cd ../apps/frontend
pnpm install

# 5. Levantar PostgreSQL (con Docker)
docker run -d \
  --name organis-postgres \
  -e POSTGRES_USER=organis_user \
  -e POSTGRES_PASSWORD=organis_password \
  -e POSTGRES_DB=organis_db \
  -p 5432:5432 \
  ankane/pgvector:latest

# 6. Levantar servidor XMPP (ejabberd)
docker run -d \
  --name organis-xmpp \
  -e ERLANG_NODE=ejabberd \
  -e EJABBERD_ADMIN_PASSWORD=admin123 \
  -p 5222:5222 \
  -p 5269:5269 \
  -p 5280:5280 \
  ejabberd/ecs:latest

# 7. Ejecutar migraciones de base de datos
cd backend-gateway
python -m alembic upgrade head

# 8. Iniciar servicios en terminales separadas

# Terminal 1 - Gateway:
cd backend-gateway
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Orchestrator:
cd backend-orchestrator
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Terminal 3 - Frontend:
cd apps/frontend
pnpm dev
```

#### **Verificar instalación:**

```bash
# Health check del Gateway
curl http://localhost:8000/health

# Health check del Orchestrator
curl http://localhost:8001/health

# Acceder al frontend
# Abrir navegador en http://localhost:5173
```

#### **Instalación rápida:**

**Opción 1: Script automático (recomendado)**

```bash
# Windows
.\infrastructure\scripts\setup-local.bat

# Linux/macOS
bash infrastructure/scripts/setup-local.sh
```

**Opción 2: Instalación manual**

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd AI4Devs-finalproject-DET
   ```

2. **Instalar dependencias**
   ```bash
   pnpm install
   ```

3. **Configurar variables de entorno**
   ```bash
   # Copiar archivos de ejemplo
   cp .env.example .env
   cp apps/backend/.env.example apps/backend/.env
   cp apps/frontend/.env.example apps/frontend/.env
   
   # Editar archivos .env con tus valores
   ```

4. **Iniciar servicios Docker**
   ```bash
   docker-compose up -d
   ```

5. **Configurar base de datos**
   ```bash
   # Generar cliente Prisma
   pnpm --filter backend prisma:generate
   
   # Ejecutar migraciones
   pnpm --filter backend prisma:migrate
   
   # (Opcional) Cargar datos de prueba
   pnpm --filter backend prisma:seed
   ```

6. **Iniciar aplicación**
   ```bash
   # Iniciar backend y frontend simultáneamente
   pnpm dev
   
   # O iniciar por separado:
   pnpm dev:backend
   pnpm dev:frontend
   ```

#### **Acceso a la aplicación:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:3001
- **API Documentation (Swagger)**: http://localhost:3001/api/docs
- **Prisma Studio**: `pnpm prisma:studio`

#### **Comandos útiles:**
```bash
# Desarrollo
pnpm dev                    # Iniciar todo
pnpm dev:backend            # Solo backend
pnpm dev:frontend           # Solo frontend

# Testing
pnpm test                   # Ejecutar todos los tests
pnpm test:backend           # Tests del backend
pnpm test:frontend          # Tests del frontend

# Linting y formato
pnpm lint                   # Lint todo el proyecto
pnpm format                 # Formatear código

# Base de datos
pnpm prisma:generate        # Generar cliente Prisma
pnpm prisma:migrate         # Ejecutar migraciones
pnpm prisma:studio          # Abrir Prisma Studio

# Docker
pnpm docker:up              # Iniciar servicios
pnpm docker:down            # Detener servicios
pnpm docker:logs            # Ver logs

# Build
pnpm build                  # Build todo
pnpm build:backend          # Build backend
pnpm build:frontend         # Build frontend
```

#### **Estructura del proyecto:**
```
AI4Devs-finalproject-DET/
├── apps/
│   ├── backend/          # NestJS API
│   └── frontend/         # React + Vite
├── packages/
│   └── shared-types/     # Tipos TypeScript compartidos
├── infrastructure/
│   ├── docker/           # Dockerfiles
│   └── scripts/          # Scripts de utilidad
└── docs/                 # Documentación adicional
```

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**
> Usa el formato que consideres más adecuado para representar los componentes principales de la aplicación y las tecnologías utilizadas. Explica si sigue algún patrón predefinido, justifica por qué se ha elegido esta arquitectura, y destaca los beneficios principales que aportan al proyecto y justifican su uso, así como sacrificios o déficits que implica.


### **2.2. Descripción de componentes principales:**

> Describe los componentes más importantes, incluyendo la tecnología utilizada

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

> Representa la estructura del proyecto y explica brevemente el propósito de las carpetas principales, así como si obedece a algún patrón o arquitectura específica.

### **2.4. Infraestructura y despliegue**

> Detalla la infraestructura del proyecto, incluyendo un diagrama en el formato que creas conveniente, y explica el proceso de despliegue que se sigue

### **2.5. Seguridad**

> Enumera y describe las prácticas de seguridad principales que se han implementado en el proyecto, añadiendo ejemplos si procede

### **2.6. Tests**

> Describe brevemente algunos de los tests realizados

---

## 3. Modelo de Datos

### **3.1. Diagrama del modelo de datos:**

> Recomendamos usar mermaid para el modelo de datos, y utilizar todos los parámetros que permite la sintaxis para dar el máximo detalle, por ejemplo las claves primarias y foráneas.


### **3.2. Descripción de entidades principales:**

> Recuerda incluir el máximo detalle de cada entidad, como el nombre y tipo de cada atributo, descripción breve si procede, claves primarias y foráneas, relaciones y tipo de relación, restricciones (unique, not null…), etc.

---

## 4. Especificación de la API

> Si tu backend se comunica a través de API, describe los endpoints principales (máximo 3) en formato OpenAPI. Opcionalmente puedes añadir un ejemplo de petición y de respuesta para mayor claridad

---

## 5. Historias de Usuario

> Documenta 3 de las historias de usuario principales utilizadas durante el desarrollo, teniendo en cuenta las buenas prácticas de producto al respecto.

**Historia de Usuario 1**

**Historia de Usuario 2**

**Historia de Usuario 3**

---

## 6. Tickets de Trabajo

> Documenta 3 de los tickets de trabajo principales del desarrollo, uno de backend, uno de frontend, y uno de bases de datos. Da todo el detalle requerido para desarrollar la tarea de inicio a fin teniendo en cuenta las buenas prácticas al respecto. 

**Ticket 1**

**Ticket 2**

**Ticket 3**

---

## 7. Pull Requests

> Documenta 3 de las Pull Requests realizadas durante la ejecución del proyecto

**Pull Request 1**

**Pull Request 2**

**Pull Request 3**

