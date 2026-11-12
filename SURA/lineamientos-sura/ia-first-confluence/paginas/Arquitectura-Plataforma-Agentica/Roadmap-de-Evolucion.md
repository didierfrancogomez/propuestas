---
titulo: "Roadmap de Evolución"
id: 5823266837
espacio: AFGLYP
version: 2
actualizado: 2026-04-17T20:23:14.210Z
actualizado_por: "Helbert Sebastian Cubillos Avila"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5823266837
---

# Roadmap de Evolución

# 1. Evolución arquitectura de referencia v2

El roadmap V2 organiza la transición desde el baseline actual hacia una plataforma agéntica reusable. La lógica propuesta es incremental: primero se estabiliza y gobierna el patrón simple, luego se externalizan capacidades reusables de conocimiento, finalmente se habilitan patrones multiagente y capacidades avanzadas de operación.

| **Fase** | **Objetivo** | **Capacidades / entregables principales** | **Workflow / gate de salida** |
| --- | --- | --- | --- |
| F0 - Alineación baseline | Consolidar el As-Is y definir la ruta objetivo. | Inventario de capacidades, restricciones LBA, C4 As-Is, ownership, NFR base y selección del perfil inicial. | Gate: perfil seleccionado y artefactos mínimos aprobados. |
| F1 - Gobernar el patrón simple | Pasar de agente singular aislado a agente singular gobernado. | Registries, observabilidad end-to-end, AI/LLM gateway, prompt management, quotas, guardrails y release control. | Gate: agente productivo con trazabilidad, políticas y operación mínima. |
| F2 - Industrializar Platform & Data | Desacoplar memoria, conocimiento y tools como capacidades compartidas. | Knowledge products, RAG services, memory layer, contracts MCP/APIs, quality evals y access control sobre retrieval. | Gate: reuse comprobable entre dos o más soluciones / dominios. |
| F3 - Escalar a multiagente | Habilitar coordinación especializada y workflows complejos. | Orchestrator V2, planner/reviewer, HITL, async workflows, experimentation, finops y mejora continua. | Gate: patrón multiagente operando con métricas, costo y riesgo controlados. |

Tabla 5 – Evolución arquitectura referencia v2

# 2. Workflows de referencia para la evolución V2

| **Workflow** | **Pasos de referencia** | **Artefactos mínimos** |
| --- | --- | --- |
| Onboarding de agente | Idea de negocio -> modelo de decisión AI First -> matriz de riesgos -> selección de perfil -> C4 / blueprint -> backlog -> despliegue controlado. | Ficha de iniciativa, perfil V2, riesgos, C4, NFR y owner. |
| Publicación de tool / MCP | Diseño de contrato -> revisión de seguridad -> pruebas funcionales -> registro -> publicación -> monitoreo. | Contrato MCP/API, políticas de acceso, versionado y dashboards básicos. |
| Publicación de knowledge product / RAG | Curación -> ingesta -> indexación -> validación de calidad -> ACL -> publicación para consumo. | Owner del producto, fuentes certificadas, índices, métricas de calidad y frescura. |
| Release de prompt / modelo / agente | Cambio -> pruebas/evals -> aprobación -> promoción -> observación post-release -> rollback si aplica. | Versionado, golden sets, evidencia de aprobación y plan de reversa. |
| Operación y mejora continua | Monitoreo -> incidentes / tuning -> nuevas hipótesis -> experimentación -> nueva release. | KPIs operativos, métricas de calidad/costo y registro de decisiones. |

Tabla 6 – Workflows de referencia v2
