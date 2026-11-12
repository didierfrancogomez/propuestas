---
titulo: "Modelo de auditoría de decisiones Agentica PoC"
id: 6076301318
espacio: AFGLYP
version: 3
actualizado: 2026-07-03T14:36:08.049Z
actualizado_por: "Johan Sebastian Murcia Prieto"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > PoC Implementación Capacidades Plataforma Agentica - Control Plane"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6076301318
---

# Modelo de auditoría de decisiones Agentica PoC

<!-- [macro: tabla de contenido] -->

# 1. Contexto general

La PoC busca validar una base gobernada para agentes de IA mediante un caso de uso de decisión AI First que permita evaluar si una iniciativa debe resolverse con una solución tradicional, IA predictiva, IA generativa o un patrón agéntico. En este escenario, la auditoría no es solo un registro técnico: es el mecanismo que permite reconstruir la decisión, demostrar que se aplicaron controles, evidenciar la participación humana y explicar por qué se llegó a una recomendación determinada.

# 2. Alcance

Aplica al canal web/chat, API/AI Gateway, runtime agéntico, orquestador, workers, LLM Gateway, prompts, MCP/tools, memoria, seguridad, observabilidad y generación de evidencia.

# 3. Objetivo

Definir los eventos, atributos mínimos y criterios de auditoría que deben capturarse durante la PoC para reconstruir decisiones AI First de extremo a extremo.

# 4. Reglas mínimas de captura y retención

- Guardar siempre identificadores de correlación, estado, resultado, errores y versiones. Evitar guardar el texto completo de prompts, respuestas o documentos si contienen información sensible.
- Cuando exista información sensible o regulada, registrar la clasificación y el resultado DLP/PII. Si se envía información al modelo, registrar si fue enmascarada o minimizada.
- Cada worker debe abrir un span propio y cada tool call debe quedar como span hijo, con latencia, resultado, error y tool call.
- Registrar los estados del proceso ejecutado por el modelo.
- Los tableros de observabilidad deben permitir filtrar por request_id, user_id hash, modelo, worker, tool y estado.

# 5. Principios del diseño de auditoría

El modelo de auditoría debe cubrir la interacción entre usuario, sesión, solicitud, orquestador, workers, modelo, prompt, matriz determinística, tools/MCP, guardrails, resultado, entre otros componentes. La captura debe estar alineada con observabilidad E2E, seguridad, calidad y gobierno, evitando depender únicamente del texto generado por el LLM.

| **Necesidad de auditoría** | **Qué debe responder** |
| --- | --- |
| Trazabilidad | Quién ejecutó la acción, cuándo ocurrió, qué agente o worker participó y cómo se correlaciona la ejecución completa. |
| Seguridad | Si el usuario estaba autenticado y autorizado, si intentó usar una tool no permitida, si hubo PII, prompt injection o bloqueo por guardrail. |
| Calidad y explicabilidad | Si el score fue reproducible, qué versión de matriz y prompt se usó, qué supuestos se aplicaron y si la justificación está alineada con los criterios. |
| Operación y resiliencia | Latencia, errores, timeouts, reintentos, estado del proceso y capacidad de continuar ante fallos parciales. |
| FinOps inicial | Modelo, proveedor, tokens usados y costo estimado por evaluación, worker o tool call. |

# 6. Catálogo de campos mínimos de auditoría

Esta definición se basa en los lineamientos establecidos en AI First, de los cuales se seleccionaron 18 atributos o campos que permiten conservar la trazabilidad, seguridad y calidad en el end to end de la plataforma agéntica acotada al alcance de la PoC. Sin embargo, es importante resaltar que esta es la primera versión del modelo y busca asentar una base inicial que deberá mejorar de forma progresiva, de acuerdo con las características de cada caso de uso.

| **N.** | **Campo mínimo** | **Categoría de auditoría** | **Importancia para seguridad, calidad y trazabilidad** |
| --- | --- | --- | --- |
| 1 | user_id | Identidad y acceso | Permite saber quién ejecutó la acción, asociar responsabilidad y validar acceso. |
| 2 | service.name | Contexto de servicio | Identifica la aplicación, agente o microservicio que generó el evento. |
| 3 | request_id | Correlación E2E | Une canal, gateway, runtime, worker, modelo, tool y evidencia de la decisión. |
| 4 | span_id | Correlación E2E | Diferencia pasos internos: orquestador, worker, LLM, tool, memoria y reporte. |
| 5 | operation.name | Flujo de negocio | Indica el tipo de uso: chat, embeddings, scoring, tool_call o aprobación HITL. |
| 6 | env | Gobierno operacional | Separa laboratorio, pruebas y producción; evita mezclar evidencia de ambientes. |
| 7 | request.model | Modelo y FinOps | Audita el modelo solicitado, fallback, versión y consistencia de resultados. |
| 8 | provider.name | Modelo y proveedor | Identifica el proveedor utilizado: Azure, GCP, OCI u otro, para gobierno y costos. |
| 9 | client.operation.duration | Calidad y rendimiento | Mide la latencia por operación y valida metas p95 de conversación o evaluación. |
| 10 | client.token.usage | FinOps y capacidad | Controla el consumo total de tokens por usuario, evaluación y agente. |
| 11 | usage.input_tokens | FinOps y calidad | Mide los tokens enviados al modelo; ayuda a detectar prompts excesivos o posibles fugas de datos. |
| 12 | usage.output_tokens | FinOps y calidad | Mide los tokens generados; apoya el control de costo, latencia y longitud de respuesta. |
| 13 | order.status | Estado de decisión | Evidencia estados como pending, processing, completed, approved, rejected o cancelled. |
| 14 | tool.call.count | Tools/MCP | Controla el uso de tools y ayuda a detectar loops, abuso o invocaciones no autorizadas. |
| 15 | tool.latency | Tools/MCP | Mide la latencia por tool/MCP y detecta cuellos de botella en matriz, retrieval o archivos. |
| 16 | tool.error.rate | Seguridad y resiliencia | Identifica herramientas inestables, errores de autorización o resultados no confiables. |
| 17 | tool.timeout.rate | Resiliencia | Valida degradación controlada, retries y límites de tiempo por worker/tool. |
| 18 | error.type | Errores y cumplimiento | Clasifica fallas: auth, policy, prompt_injection, DLP, model, tool, timeout o data. |

# 7. Referencias y alineación

El modelo de auditoría se definió con base en los documentos de referencia de la estrategia **AI First**, arquitectura agéntica, seguridad y observabilidad E2E.

- [Blueprint de Capacidades Arquitectura Agéntica](../../../paginas/Arquitectura-Plataforma-Agentica/Blueprint-de-Capacidades-Arquitectura-Agentica.md)
- [PoC Implementación Capacidades Plataforma Agentica - Control Plane](../../../paginas/Arquitectura-Plataforma-Agentica/PoC-Implementacion-Capacidades-Plataforma-Agentica-Control-Plane.md)
- [Lineamientos Técnicos de Seguridad para esquemas Human in the Loop (HITL) y Auditoría en Plataformas de IA](https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/)
- [Mínimos de Observabilidad para IA First](https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/)

Estos lineamientos permitieron alinear los eventos y atributos mínimos con los objetivos de trazabilidad, gobierno, calidad y cumplimiento de la PoC.
