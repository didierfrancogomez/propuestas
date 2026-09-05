---
titulo: "ADRs de Implementación"
id: 6244532291
espacio: AFGLYP
version: 2
actualizado: 2026-08-28T20:37:38.369Z
actualizado_por: "Diego Fernando Gomez Alvarez"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > Arquitectura de implementación"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6244532291
---

# ADRs de Implementación

# ADR-2026-001 APIM como Gateway para el control plane

| Campo | Contenido |
| --- | --- |
| Identificador | ADR-2026-001 |
| Estado | `[Propuesto]` Preferencia técnica por APIM, pendiente de ratificación estratégica |
| Fecha | 2026-08-19 |
| Decisión | Adoptar APIM como capa de API / AI Gateway del Control Plane agéntico y mantener APIGEE como estándar para APIs de negocio y exposición a aliados |
| Justificación principal | Las cargas agénticas residen en Azure; APIM se integra mejor con Entra ID, Sentinel, A2A y el gobierno centralizado de MCP |
| Consecuencias | Se administra un segundo API Manager, se exige alta resiliencia, automatización de onboarding y construcción de aceleradores operativos para IA |
| Decisiones abiertas | Ratificación estratégica, modelo operativo, postura multicloud, exposición a aliados y adopción de AI Security |
