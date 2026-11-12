---
titulo: "Requerimientos no Funcionales"
id: 5822152737
espacio: AFGLYP
version: 1
actualizado: 2026-04-17T21:26:55.761Z
actualizado_por: "Helbert Sebastian Cubillos Avila"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5822152737
---

# Requerimientos no Funcionales

Un conjunto mínimo de NFRs expresados como objetivos cuantificables, por ejemplo:

- **Rendimiento / Latencia**

    - Latencia objetivo por tipo de interacción (chat, acción transaccional, RAG, tool-call).
    - Presupuestos de latencia por capa: canal → orquestador → gateway → LLM → guardrails → respuesta.
    - Reglas de degradación: fallback a LLM, respuesta parcial, modo “no tool-calls”, etc.
- **Costos / FinOps**

    - Presupuesto por caso de uso (costo por conversación, por acción, por 1.000 interacciones).
    - Políticas de ruteo por costo: uso LLM, caching, límites de tokens, batch, top-k, etc.
    - Límites y alertas: cuotas por equipo/agente, controles por ambiente.
- **Cumplimiento, Seguridad y Privacidad**

    - Requisitos de manejo de datos (PII, datos sensibles, retención, residencia de datos).
    - Controles obligatorios: autenticación/autorización (RBAC/ABAC), cifrado, gestión de secretos, DLP, auditoría.
    - Guardrails requeridos (prompt-injection, exfiltración, contenido, políticas de herramientas).
- **Disponibilidad, Resiliencia y Continuidad**

    - SLAs/SLOs (disponibilidad mensual, RTO/RPO si aplica).
    - Comportamiento ante fallas del proveedor LLM, del vector DB, del broker, etc.
    - Estrategias: retries con backoff, circuit breakers, multi-provider, colas, degradación.
- **Observabilidad y Auditoría**

    - Trazabilidad end-to-end (traceID) por conversación/acción.
    - Logging estructurado (inputs/outputs con redacción), métricas y evaluación continua (evals).
    - Evidencia de cumplimiento: quién ejecutó qué, con qué prompt/modelo/versión y resultado.
- **Escalabilidad y Operabilidad**

    - TPS/Concurrencia objetivo y modelo de escalamiento (horizontal, colas, rate limiting).
    - Requisitos de despliegue (IaC, CI/CD, entornos) y operación (runbooks, alertas, on-call).
- **Confiabilidad**

    - Tasa mínima de éxito por tipo de interacción (chat, RAG, etc) y por agente.
    - Umbrales máximos de error funcional y de alucinación.
    - Score mínimo de groundedness en escenarios RAG (Sustentación de la respuesta).
    - Control de regresión y consistencia, variación máxima permitida entre versiones de modelos y prompts ante inputs equivalentes.
