---
titulo: "Roles mínimos y RACIVD"
id: 5823299591
espacio: AFGLYP
version: 3
actualizado: 2026-04-23T20:36:16.765Z
actualizado_por: "Helbert Sebastian Cubillos Avila"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5823299591
---

# Roles mínimos y RACIVD

Se recomienda usar RACIVD y no RACI plana, la cual es una herramienta de gestión que define y clarifica roles y responsabilidades dentro de un proyecto o proceso, ampliando el modelo tradicional RACI con dos roles adicionales; porque el ciclo de vida descrito tiene gates, validaciones y decisiones explícitas en Caracterización.

| **Sigla** | **Nombre** | **Uso en esta propuesta** |
| --- | --- | --- |
| **R** | Responsible | Ejecuta la actividad o produce el entregable. |
| **A** | Accountable | Responde por el resultado final. |
| **C** | Consulted | Debe ser consultado por su criterio funcional, técnico o de control. |
| **I** | Informed | Debe mantenerse informado, sin ejecutar. |
| **V** | Validate / Verify | Valida riesgos, seguridad, calidad o cumplimiento metodológico. |
| **D** | Decide | Toma la decisión estructural o de continuidad en un gate formal. |

# 1. Roles candidatos

| **Código** | **Rol** | **Descripción** | **Etapas foco** |
| --- | --- | --- | --- |
| **SP** | Sponsor / Business Owner | Patrocina la iniciativa, habilita prioridad y funding. | Ideación, gates relevantes, cierre |
| **PO** | Product Owner | Responsable del valor funcional y priorización. | Todo el ciclo |
| **BN** | Analista de negocio / funcional | Estructura contexto, problema, métricas, proceso y backlog funcional. | Ideación a Estructuración |
| **UO** | Usuario Owner / líder de dominio | Representa el área que recibirá la solución en operación. | Ideación, Implementación, Producción |
| **MGI** | Equipo Modelo de Gestión de Iniciativas | Facilita el flujo metodológico de ideación, caracterización y estructuración. | Ideación, Caracterización, Estructuración |
| **AIA** | AI Architect | Define patrón agéntico y decisiones de arquitectura IA. | Caracterización, Estructuración |
| **AS** | Arquitecto de solución | Aterriza diseño técnico e integraciones. | Caracterización, Estructuración |
| **DL** | Delivery Lead / PM / Scrum Master | Coordina plan, secuencia, backlog y seguimiento. | Caracterización, Estructuración, cierre |
| **CIA** | Comité de IA Responsable | Instancia que interviene cuando la evaluación de riesgo da score alto. | Caracterización |
| **ETI** | Equipos técnicos de acompañamiento | Equipos técnicos que apoyan caracterización, estructuración e implementación. | Caracterización a Implementación |
| **TL** | Tech Lead | Lidera la ejecución técnica del delivery. | Estructuración, Implementación |
| **DATA** | Data Team / Data Engineer | Habilita fuentes, RAG, índices, datos y conocimiento. | Caracterización a Implementación |
| **UX** | UX / UI | Diseña experiencia y flujo de interacción. | Caracterización, Estructuración, Implementación |
| **SEC** | Seguridad / Cyber | Define y valida controles, identidad y riesgos técnicos. | Caracterización a Producción |
| **CAI** | Comunidad AI First | Espacio de alineación, aprendizaje y revisión sobre prácticas y decisiones AI First. | Caracterización, Estructuración |
| **QA** | QA / Pruebas | Asegura estrategia y ejecución de pruebas. | Implementación |
| **DEV** | Desarrollo | Construye la solución y sus integraciones. | Implementación, Hypercare |
| **PLT** | Plataforma / DevOps | Gestiona CI/CD, infraestructura y despliegue. | Implementación, Producción |
| **SRE** | SRE / Operaciones / Observabilidad | Asegura monitoreo, estabilización y operación técnica. | Implementación, Producción |

# 2. Etapas, entregables y gates complementados

| **Etapa** | **Entregables / actividades clave** | **Gate** | **Lógica de decisión** | **Roles foco** |
| --- | --- | --- | --- | --- |
| **Ideación** | Problema/oportunidades, métricas, alcance, propósito, proceso actual/ideal, riesgos iniciales. | Paso a Caracterización | Se valida si existe problema real, valor y continuidad básica. | SP, PO, BN, UO, MGI |
| **Caracterización** | Contexto, plan de entregas, mapa de actores, flujo, tallaje/dimensión, matrices. | Paso a Estructuración | Se ejecutan tres matrices: tipo de solución, Low/Pro Code y riesgos. Si el score es alto, escala a Comité IA Responsable. | MGI, PO, BN, AIA, SEC, GIA, CIA, ETI |
| **Estructuración** | Impact/Story mapping, diseño técnico/arquitectónico, backlog, sprint 0, plan de trabajo (tiempo, costo, personas/roles). | Paso a Implementación | Se valida si la iniciativa ya es ejecutable con diseño, capacidad y plan. | DL, AIA, AS, TL, PO, ETI |
| **Implementación** | Desarrollo, pruebas, despliegues, readiness de producción. | Go / No-go a Producción | Se valida calidad, seguridad, despliegue y preparación técnica. | TL, DEV, QA, PLT, SRE, SEC, PO |
| **Producción / Estabilización** | Entrega a operación, entrega al dominio, monitoreo, cierre. | Paso a operación regular | La solución se estabiliza y se transfiere a operación y dominio. | SRE, PLT, UO, PO, DEV, TL |

Para la aplicación de la Matriz RACIVD de Roles y Responsabilidades ver el archivo
> **[Archivo adjunto]** [Matriz_RACIVD_Ciclo_Vida_Iniciativa_v1.4.xlsx](../../recursos/5823299591/Matriz_RACIVD_Ciclo_Vida_Iniciativa_v1.4.xlsx)
