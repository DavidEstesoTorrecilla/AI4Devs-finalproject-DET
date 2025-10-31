# 📚 Documentación de Organis.AI (EMASAI)

Índice completo de la documentación del proyecto.

## 📋 Documentos Principales

### [SSD_EMASAI.md](./SSD_EMASAI.md)
**Software System Design** - Documento de diseño principal del sistema.
- Descripción general del producto
- Arquitectura del sistema
- Modelo de datos
- Especificación de API
- Historias de usuario
- Flujos de trabajo

### [ESTRUCTURA_PROYECTO.md](./ESTRUCTURA_PROYECTO.md)
Descripción completa de la estructura del proyecto:
- Arquitectura de carpetas
- Servicios Docker
- Agentes SPADE y sus responsabilidades
- Base de datos y modelos
- Flujo de datos entre componentes
- APIs disponibles

### [ESTRUCTURA_GENERADA.md](./ESTRUCTURA_GENERADA.md)
Documento de la estructura generada inicialmente (referencia histórica).

## 🏗️ Arquitectura

### Diagramas C4

#### [Diagrama arquitectura C4 Nivel 1.pdf](./architecture/Diagrama%20arquitectura%20C4%20Nivel%201.pdf)
Vista de contexto del sistema - Actores externos y sistema principal.

#### [Diagrama arquitectura C4 Nivel 2.pdf](./architecture/Diagrama%20arquitectura%20C4%20Nivel%202.pdf)
Vista de contenedores - Componentes técnicos principales:
- Backend Gateway (FastAPI)
- Backend Orchestrator (SPADE)
- Frontend (React)
- PostgreSQL + pgvector
- Servidor XMPP
- SurfSense RAG

### Diagramas de Secuencia

#### [Diagrama actualizar etapa y cerrar oportunidad.pdf](./architecture/Diagrama%20actualizar%20etapa%20y%20cerrar%20oportunidad.pdf)
Flujo de actualización de etapas de oportunidades y cierre de ventas.

#### [Diagrama de secuencia para generar borrador de Factura.pdf](./architecture/Diagrama%20de%20secuencia%20para%20generar%20borrador%20de%20Factura.pdf)
Proceso de generación automática de facturas cuando se gana una oportunidad.

#### [Diagrama de Secuencia para Visualizar Dashboard.pdf](./architecture/Diagrama%20de%20Secuencia%20para%20Visualizar%20Dashboard.pdf)
Carga de datos y visualización del dashboard de métricas.

## 🔧 Desarrollo

### [PROMPTS_DOCUMENTACION.md](./PROMPTS_DOCUMENTACION.md)
Registro de prompts utilizados para generar la documentación del proyecto.

### [REDIS_GUIDE.md](./REDIS_GUIDE.md)
Guía completa de uso de Redis Cache:
- Configuración y variables de entorno
- Patrones de uso en código
- Estrategias de cache y TTLs
- Monitoreo y troubleshooting

## 📖 Recursos de Referencia

### [Resumen Completo de Departamentos de una Empresa Moderna.pdf](./Resumen%20Completo%20de%20Departamentos%20de%20una%20Empresa%20Moderna.pdf)
Contexto empresarial para entender los roles y departamentos que interactúan con el sistema.

## 📁 Estructura de Carpetas

```
docs/
├── README.md                              # Este archivo
├── SSD_EMASAI.md                          # Diseño del sistema
├── ESTRUCTURA_PROYECTO.md                 # Estructura técnica
├── ESTRUCTURA_GENERADA.md                 # Referencia histórica
├── PROMPTS_DOCUMENTACION.md               # Prompts de desarrollo
├── Resumen Completo de Departamentos...   # Contexto empresarial
│
├── api/                                   # Documentación de API
│   └── (Pendiente: Especificaciones OpenAPI/Swagger)
│
├── architecture/                          # Diagramas de arquitectura
│   ├── Diagrama arquitectura C4 Nivel 1.pdf
│   ├── Diagrama arquitectura C4 Nivel 2.pdf
│   ├── Diagrama actualizar etapa y cerrar oportunidad.pdf
│   ├── Diagrama de secuencia para generar borrador de Factura.pdf
│   └── Diagrama de Secuencia para Visualizar Dashboard.pdf
│
└── screenshots/                           # Capturas de pantalla
    └── (Pendiente: Screenshots del producto)
```

## 🚀 Inicio Rápido

1. **Para entender el proyecto**: Lee [SSD_EMASAI.md](./SSD_EMASAI.md)
2. **Para desarrollar**: Consulta [ESTRUCTURA_PROYECTO.md](./ESTRUCTURA_PROYECTO.md)
3. **Para arquitectura**: Revisa los diagramas en [architecture/](./architecture/)
4. **Para APIs**: Visita [api/](./api/) (pendiente de completar)

## 📝 Notas

- La documentación se actualiza continuamente durante el desarrollo
- Los diagramas están en formato PDF (herramienta: Draw.io / Lucidchart)
- La especificación de API se generará automáticamente desde el código (OpenAPI/Swagger)

---

**Proyecto**: Organis.AI (Nombre comercial: EMASAI)  
**Versión**: 1.0.0  
**Última actualización**: 31 de octubre de 2025
