# Lineamientos SURA (referencia obligatoria)

Insumos oficiales del cliente exportados de su Confluence (espacio AI-First / Plataforma Agéntica).
Todo lo que se haga en la carpeta `SURA/` debe tomar esto como referencia.

## Estructura

- `ia-first-confluence/paginas/` — páginas en Markdown (la forma más cómoda de leerlas)
- `ia-first-confluence/html-original/` — HTML exportado de Confluence
- `ia-first-confluence/storage-format/` — formato nativo de Confluence (.xhtml)
- `ia-first-confluence/recursos/` — imágenes y adjuntos (matrices RACIVD, de decisión y de madurez, catálogo de capacidades IA, arquetipos de agentes .zip)
- `ia-first-confluence/LEEME.md`, `index.html`, `manifest.json` — índice de la exportación

## Páginas clave (en `ia-first-confluence/paginas/`)

**ARQ AI-First — Arquitectura de referencia**
- `ARQ-AI-First-Arquitectura-de-referencia/Arquitectura-Agentes-V1.1/Arquitectura-de-Referencia-V1.1.md`
- `ARQ-AI-First-Arquitectura-de-referencia/Arquitectura-Agentes-V1.1/Arquitectura-de-implementacion-v1.1.md`

**Arquitectura Plataforma Agéntica**
- `Arquitectura-Plataforma-Agentica.md` (página padre)
- Introducción, Visión general, Análisis As-Is, Mapa de Dominios (+ Diseño Datos RAG/Knowledge/Memory)
- Matriz de Madurez, Modelo de toma de decisiones, Roles mínimos y RACIVD
- Requerimientos no Funcionales, Roadmap de Evolución
- Blueprint de Capacidades:
  - Agentic Platform → Control Plane (AI Gateway, AI Security Enforcement, AI/LLM Lifecycle Management, FinOps)
  - Agentic Platform → Domain Layer (Agentic Runtime)
  - Enterprise Shared Capabilities, External Services, External Access & Experience Development
- Arquitectura de implementación (ADRs, análisis de APIM para el control plane, validación de la pila del control plane)
- PoC Capacidades Plataforma Agéntica – Control Plane (+ Modelo de auditoría de decisiones)

**Arquitecturas de referencia Multimodal / Voz / Multiagente (V1.0)**
- `Arquitectura-Referencia-Multimodal-Voz-Multiagente/Arquitectura-de-Referencia-Multiagente-V1.0.md`
- `.../Arquitectura-de-Referencia-Multimodal-V1.0.md` (+ Arquitectura de Implementación Multimodal)
- `.../Arquitectura-de-Referencia-Voz-V1.0.md`

**LIN Infraestructura**
- `LIN-Infraestructura/Separacion-de-Suscripciones-entre-Dominio-de-Agentes-y-Dominio-de-Informacion-Co.md`

## Origen
Movido desde `gestores-sura/estimacin mvp/insumos/iafirst/d6486806-8073-4ba2-af0b-7162c2ff8cfb/`.
