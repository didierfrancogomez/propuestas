---
titulo: "Diseño Datos RAG / Knowledge / Memory"
id: 5900140571
espacio: AFGLYP
version: 2
actualizado: 2026-05-11T14:53:12.798Z
actualizado_por: "Junior Millan Perez"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > Mapa de Dominios"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5900140571
---

# Diseño Datos RAG / Knowledge / Memory

Este documento define el diseño del paquete de datos que habilita RAG, Knowledge y Memory. Separa responsabilidades entre capas de datos, informacion, conocimiento y memoria, estableciendo limites claros con el core agentico y las capas transversales de gobierno, seguridad y observabilidad.

**Problema que resuelve:** sin esta separacion, los agentes acceden directamente a fuentes sin control, el conocimiento no se versiona ni evalua, la memoria crece sin politica de retencion, y no existe evidencia para promover a produccion.

**Beneficios:** separacion clara dato/informacion/conocimiento/memoria; gobierno por diseno (owner, version, contrato, evaluacion); seguridad (PII, DLP, Injection en 3 puntos); trazabilidad E2E con OpenTelemetry; escalabilidad (nuevos dominios sin modificar core); evidencia para produccion (Quality Gates, Evaluations, baselines).

## Contexto

El foco es definir el paquete que habilita: RAG como capacidad gobernada; Knowledge como producto versionado; Memory como capacidad controlada; separacion de responsabilidades; definiciones de implementacion; gobierno, seguridad y observabilidad; evidencias para produccion.

## Principios de Diseño

1. Separacion clara entre datos, informacion, conocimiento y memoria.
2. RAG como capacidad gobernada, no integracion aislada.
3. Knowledge como producto versionado, evaluado, con owner y contrato.
4. Memory como capacidad controlada, auditable, dependiente del caso de uso.
5. Agentes desacoplados de fuentes internas; consumen via servicios gobernados.
6. Conocimiento, embeddings, indices y memoriañ

## Definicion Conceptual

| Concepto | Definicion | Ejemplo | Cuando aplica | Cuando NO aplica |
| --- | --- | --- | --- | --- |
| Producto de datos | Dataset gobernado con owner, SLA y contrato. | Tabla Gold polizas vigentes | Multiples consumidores, calidad garantizada | Dato de uso unico sin SLA |
| Producto de informacion | API/servicio con logica de negocio sobre datos gobernados. | API "Resumen cliente" | Reglas estables y reutilizables | Consulta ad-hoc sin logica |
| Producto de conocimiento | Docs/indices curados, chunkeados, embebidos, con ontologia, accesible por RAG/MCP. | Indice "Autorizaciones EPS" | Contenido no estructurado, multiples agentes, busqueda semantica | Dato estructurado consultable via SQL/API |
| Dominio de conocimiento | Agrupacion de Knowledge Products con gobierno avanzado. | Dominio "Seguros Voluntarios" (3 indices + ontologia) | 2+ agentes, reuso cross-agent, trazabilidad avanzada | Un solo indice aislado sin reuso |
| RAG | Capacidad que permite recuperar contexto de Knowledge Products para fundamentar respuestas. | Agente consulta normativa antes de responder | Agente necesita contexto no parametrico | Agente solo ejecuta tools sin contexto documental |
| Memory | Persistencia de estado de interacciones, decisiones y preferencias. | Historial conversacion, preferencias usuario | Continuidad entre turnos/sesiones | Interaccion stateless |

**Criterio clave:** No siempre se necesita un dominio de conocimiento. Si el agente solo necesita un dato estructurado, basta con el path directo (API/Data Product) que ya existe en la arquitectura base.

## Separacion de Responsabilidades por Capa

| Capa | Responsabilidad | Incluye | NO incluye | Dueño | Controles |
| --- | --- | --- | --- | --- | --- |
| Data Layer | Mover, almacenar, gobernar datos | Fuentes, Data Lake (B/S/G), ETL, Data Products | Embeddings, indices, memoria, logica agentes | DataOps | Linaje, calidad, clasificacion, RBAC, Catalog |
| Information Domain | Agrupar fuentes y productos bajo contexto de negocio | Sources, Data Products, Knowledge Products, Stores, Pipeline, Exposure | Runtime agentes, orquestacion, memoria | Domain Owner | Ownership, contratos, versionamiento, Catalog |
| Knowledge Layer | Transformar datos en productos de conocimiento | Pipeline (Ingestion, Cleaning, Chunking, Enrichment, Embeddings, Indexing, QG). Knowledge Products. | Logica agentes, memoria, datos Tx crudos | Domain Owner + Arq IA | Quality Gates, versionamiento, evaluacion, allowlist, PII, Catalog |
| RAG Layer (runtime) | Recuperar contexto relevante para agentes | RAG Orchestrator, Query Routing, Retrieval, Re-ranking, Runtime QG, Grounding, Citacion | Ingesta, creacion indices, almacenamiento, logica negocio | Arq IA | QG runtime, observabilidad retrieval, groundedness, trazabilidad chunks |
| Memory Layer | Persistir estado de interacciones | Conversacional, Semantica, Operacional, Usuario. Politicas retencion. Controles escritura. | Knowledge Products, indices RAG, datos Tx, historico auditorias | Arq IA + Seguridad | PII, Injection Filter, TTL, derecho olvido, aislamiento, consentimiento |
| Agentic Core | Razonar, planear, orquestar | Orchestrator, Agents, Session, Tools, Prompt Runtime, Memory Access | Ingesta, indices, almacenamiento conocimiento, gobierno datos | Arq IA | Guardrails E/S, observabilidad agente, Prompt Mgmt |
| Tool/MCP Layer | Exponer capacidades como herramientas | Domain MCP Tools, MCP Servers, MCP Gateway | Logica negocio completa, almacenamiento | Arq IA + Domain | Allowlist, RBAC, auditoria invocaciones |
| Gateway Layer | Controlar acceso y routing | API Gateway, LLM Gateway, MCP Gateway | Logica negocio, almacenamiento | Plataforma | Auth, rate limit, logging, cost tracking |
| Security Layer | Proteger flujo datos/conocimiento/memoria | IDP, Identity, Auth, RBAC, Secrets, AI Security (PII, DLP, Content Safety, Injection, Intent) | Logica negocio | Seguridad | Controles en 3 puntos: ingreso, pre-RAG, pre-memoria |
| Governance Layer | Gobernar ciclo de vida | Catalog, Prompt Lifecycle, Evaluations, FinOps, Ownership, Contratos, Versionamiento | Ejecucion agentes | Gobierno IA | Catalog actualizado, evaluaciones baseline, aprobaciones |
| Observability Layer | Visibilidad completa | Metrics, Logs, Traces, Retrieval metrics, Memory ops, Guardrail events, Cost/tokens | Logica negocio | SRE/Plataforma | Dashboards, alertas, correlacion trace_id |

## Diseno de RAG

| Etapa | Responsabilidad | Componentes minimos | Tecnologia sugerida | Quality Gate | Evidencia requerida |
| --- | --- | --- | --- | --- | --- |
| Fuentes | Identificar y aprobar origenes | Source Registry, Allowlist | Catalog (Purview/Unity) | Source in Allowlist | Registro en Catalog con owner |
| Ingesta (Bronze) | Extraer y depositar raw | Connector, Storage | Azure Data Factory / Container Apps Job | Archivo depositado sin corrupcion | Log de ingesta exitosa |
| Limpieza/Normalizacion (Silver) | OCR, normalizacion, dedup | Document Intelligence, Normalizer | Azure Document Intelligence | PII Scan pass, Source Trust pass | Reporte PII = 0 criticos |
| Chunking | Dividir documentos en fragmentos semanticos | Chunker con estrategia versionada | LangChain splitters (semantic/recursive) | Chunk size dentro de rango, overlap configurado | Version de estrategia registrada |
| Enriquecimiento semantico | Agregar metadata (domain, acl, source, timestamp) | Enricher | Pipeline custom | Metadata completa | Schema validation pass |
| Embeddings (Gold) | Calcular vectores | Embedding Service versionado | Azure OpenAI text-embedding-3-large | Modelo y version registrados | Version en Catalog |
| Indexacion | Crear/actualizar indice vectorial | Index Builder | Azure AI Search (HNSW + hybrid) | Index creado, campos homogeneos | Indice publicado en Catalog |
| Quality Gates ingesta | Validar antes de publicar | QG Engine | Reglas + Presidio + Allowlist | Allowlist OK, PII OK, Schema OK, Dedup OK | Reporte QG aprobado |
| Publicacion | Registrar como Knowledge Product | Catalog entry | Purview / Unity Catalog | Owner, version, contrato, ACL definidos | Entrada en Catalog |
| Recuperacion (runtime) | Buscar chunks relevantes | RAG Orchestrator | Azure AI Search (hybrid + rerank) | top_chunk_score >= umbral | Traza con scores |
| Re-ranking | Reordenar por relevancia | Reranker | Azure AI Search semantic ranker | Top-k estable | Scores en traza |
| Runtime Quality Gates | Validar contexto antes de enviar al LLM | QG Runtime | Reglas + Content Safety | Score OK, source in allowlist, PII clean, injection pass | Evento en observabilidad |
| Grounding/Citacion | Vincular respuesta con fuentes | Citation builder | Custom (metadata de chunks) | Respuesta con citacion valida | % respuestas con citacion |
| Evaluacion | Medir calidad de recuperacion | Eval Engine | MLflow + LLM-as-Judge | Baseline superado | Reporte de evaluacion con metricas |
| Versionamiento | Controlar cambios | Version registry | Catalog + Git tags | Cambio chunking/embedding = MAJOR | Historial de versiones |
| Rollback | Revertir indice a version anterior | Index versioning | Azure AI Search (alias de indice) | Rollback exitoso sin downtime | Log de rollback |

## Diseno de Knowledge

| Elemento | Responsabilidad | Implementacion sugerida | Gobierno requerido | Evidencia |
| --- | --- | --- | --- | --- |
| Knowledge Preparation Pipeline | Transformar datos en conocimiento consumible | Container Apps Job / Databricks (segun volumen) | Pipeline registrado, schedule definido, owner asignado | Ejecucion exitosa en log |
| Knowledge Product | Unidad minima de conocimiento gobernado | Indice AI Search + metadata en Catalog + tool MCP | Owner, version (semver), contrato (schema), ACL, allowlist fuentes, SLA actualizacion | Entrada en Catalog con todos los campos |
| Knowledge Domain | Agrupacion de KPs con gobierno avanzado | Namespace logico en Catalog + ontologia compartida | Domain Owner, evaluacion cross-KP, reuso documentado | 2+ agentes consumiendo, evaluacion publicada |
| Semantic Indexes | Indices vectoriales por dominio/grupo/acceso | Azure AI Search (1 indice por KP, patron Insuregent) | Versionamiento, rollback, campos homogeneos | Indice activo con version registrada |
| Embeddings Store | Almacenar vectores con version | Azure AI Search (integrado en indice) | Version de modelo de embedding registrada | Modelo + version en Catalog |
| Curated Document Collections | Documentos fuente curados (Gold) | ADLS Gen2 (Gold layer) | Linaje, clasificacion, retencion | Documentos trazables a fuente original |
| Business Ontologies | Relaciones semanticas del dominio | Opcional: Graph DB o metadata enriquecida | Owner, versionamiento | Ontologia documentada (si aplica) |
| Enriched Metadata | Metadata semantica de chunks | Campos en indice (domain, acl, source, version, ts) | Schema estandarizado | Schema validation en QG |
| Knowledge APIs / MCP Tools | Exponer KP a agentes | MCP Server (1 tool por KP/dominio) | Registrado en MCP Gateway, allowlist | Tool activo y consumible |
| Data & Knowledge Catalog | Descubrimiento, linaje, gobierno | Microsoft Purview o Unity Catalog | Actualizado, con owners y versiones | Catalog con cobertura >= 90% de KPs |
| Evaluacion de Knowledge | Medir calidad del conocimiento | MLflow + dataset por dominio | Baseline definido, evaluacion periodica | Reporte de evaluacion publicado |

**Cuando se justifica crear un Knowledge Domain:**

- 2+ agentes o casos de uso consumen el mismo conocimiento.
- Se requiere busqueda semantica / RAG.
- Se necesita trazabilidad avanzada.
- Se requiere versionamiento formal.
- Se necesitan Quality Gates y evaluaciones formales.

**Cuando NO se justifica:**

- Un solo agente consume un dato estructurado via API.
- No hay busqueda semantica involucrada.
- Basta con consumir un Data Product existente via path directo.

## Diseno de Memory

| Tipo | Descripcion | Uso permitido | Riesgo principal | Control requerido | Tecnologia | Prioridad |
| --- | --- | --- | --- | --- | --- | --- |
| Conversacional (STM) | Historial del hilo, checkpoints, buffer summarization | Continuidad dentro de sesion | PII en conversacion, retencion excesiva | TTL configurable, PII redaction, aislamiento usuario | Cosmos DB | Obligatorio |
| Semantica (LTM) | Hechos estables persistidos como embeddings | Recordar preferencias/hechos entre sesiones | PII en embeddings, reidentificacion, memory poisoning | Injection Filter pre-escritura, PII scan, consentimiento, TTL | Azure AI Search (coleccion dedicada) o Cosmos vector | Obligatorio |
| Operacional | Estado del grafo de agentes, reintentos, resultados tools | Resume de ejecucion, debugging | Contaminacion por injection, datos sensibles en trazas | TTL corto (7d), no exponer a usuario, PII redaction | Cosmos DB (checkpoints LangGraph) | Obligatorio |
| De usuario (perfil) | Preferencias, rol, consentimientos | Personalizacion, RBAC contextual | Privacidad, consentimiento, derecho al olvido | Base canonica con RBAC, consentimiento explicito, borrado auditable | Base de usuario corporativa | Recomendado |
| Session Cache | Cache de sesion para velocidad | Reducir latencia en consultas repetidas | Datos stale, inconsistencia | TTL corto, invalidacion explicita | Azure Redis | Opcional |

**Controles obligatorios antes de ambiente productivo (memoria):**

1. PII Detection/Redaction en escritura y lectura.
2. Prompt Injection Filter antes de escribir en LTM.
3. Politica de retencion (TTL) por tipo aprobada por seguridad/juridica.
4. Aislamiento por tenant/usuario (particion logica o fisica).
5. Derecho al olvido auditable (borrado verificable con evento).
6. Versionamiento del esquema de memoria.
7. Trazabilidad E2E: cada R/W en traza OpenTelemetry.
8. Consentimiento explicito para memoria de usuario.
9. Clasificacion de informacion almacenada.
10. Encriptacion at-rest y in-transit.

## Relacion con el Core Agentico

| Componente | Pertenece a RAG/Knowledge/Memory | Pertenece al Core Agentico | Relacion | Limite arquitectonico |
| --- | --- | --- | --- | --- |
| RAG Orchestrator | Si (RAG runtime) | No (es tool consumido) | Agente invoca via MCP tool | Agente NO accede directo al indice |
| Knowledge Products | Si (Knowledge) | No | RAG Orchestrator los consulta | Agente NO escribe en Knowledge |
| Knowledge Preparation Pipeline | Si (Knowledge) | No | Produce Knowledge Products | Pipeline independiente del runtime de agentes |
| Memory Writer Service | Si (Memory) | No (es servicio consumido) | Agente escribe via servicio con guardrails | Agente NO escribe directo en store |
| Orchestrator Agent | No | Si | Consume RAG y Memory via tools/services | No contiene logica de indexacion ni embedding |
| LLM Gateway | No | No (Gateway Layer) | Agente llama LLM via Gateway | Agente NO llama LLM directo |
| Prompt Management | No | No (Governance) | Agente consume prompts versionados | Prompts gobernados externamente |
| MCP Gateway | No | No (Gateway Layer) | Registra y controla tools | Allowlist y policy centralizados |
| Tools / MCP Servers | Parcial (RAG tool es MCP) | Parcial (tools de negocio) | RAG Orchestrator es un MCP Server | Cada tool tiene scope definido |
| Data & Knowledge Catalog | Si (Governance) | No | Registra KPs y versiones | Catalog es transversal, no del core |

## Gobierno, Seguridad y Observabilidad

| Control | Aplica a | Objetivo | Evidencia requerida | Responsable |
| --- | --- | --- | --- | --- |
| Source Allowlist | RAG ingesta | Solo fuentes aprobadas llegan al indice | Lista aprobada en Catalog | Domain Owner |
| PII Detection/Redaction | RAG ingesta + Memory escritura | No almacenar PII sin control | Reporte PII = 0 criticos | Seguridad |
| DLP | Flujo completo | Prevenir fuga de datos sensibles | Politica DLP activa | Seguridad |
| Prompt Injection Protection | Ingreso usuario + pre-memoria | Evitar manipulacion de agentes/memoria | Prueba red-team aprobada | Seguridad IA |
| Content Safety | Entrada/salida agente | Filtrar contenido toxico/danino | Filtro activo con metricas | Seguridad IA |
| RBAC / ACL | Knowledge Products + Memory | Control de acceso por rol/grupo | ACL definido por KP | Domain Owner + Seguridad |
| Versionamiento embeddings | Knowledge | Trazabilidad y rollback | Version registrada en Catalog | Arq IA |
| Versionamiento indices | Knowledge | Rollback sin downtime | Alias de indice + historial | Arq IA |
| Versionamiento chunking | Knowledge | Reproducibilidad | Estrategia versionada (semver) | Arq IA |
| Versionamiento prompts | Governance | Ciclo de vida DRAFT/ACTIVE/DEPRECATED | Prompt en Catalog con estado | Gobierno IA |
| Versionamiento memoria | Memory | Schema evolution controlado | Schema version registrado | Arq IA |
| Evaluaciones (LLM-as-Judge) | RAG + Knowledge | Medir calidad antes de produccion | Reporte con metricas baseline | Gobierno IA |
| Retencion memoria | Memory | No retener mas de lo necesario | Politica TTL aprobada | Seguridad + Juridica |
| Derecho al olvido | Memory usuario | Borrado verificable | API de borrado + evento auditoria | Seguridad |
| Trazabilidad E2E | Todo el paquete | Correlacionar ingesta-retrieval-agente-memoria | trace_id en todas las operaciones | Observabilidad |
| Metricas RAG | RAG runtime | Medir calidad de recuperacion | Dashboard con recall@k, MRR, groundedness, latencia | Observabilidad |
| Metricas Memory | Memory | Monitorear uso y anomalias | R/W rate, PII hits, violaciones retencion | Observabilidad |
| FinOps | RAG + LLM | Controlar costos | Costo/request, tokens in/out | FinOps |

**Metricas :**

- Calidad recuperacion: top_k_hit_rate, recall@k, MRR, top_chunk_score.
- Groundedness: % respuestas con citacion valida, faithfulness_score.
- Relevancia: answer_relevance, context_precision, context_recall.
- Operacion: latencia p50/p95/p99, costo/request, tokens in/out.
- Gobierno: errores guardrails, eventos DLP, fuentes fuera allowlist.
- Memoria: R/W rate, PII detections, violaciones retencion, poisoning sospechoso.

**Evidencia para pasar de desarrollo a produccion:**

1. Quality Gates ingesta aprobados (PII=0, allowlist=100%, schema OK).
2. Baseline Evaluations publicado (relevancia, groundedness, faithfulness).
3. Red-team Prompt Injection aprobado.
4. Knowledge Product registrado en Catalog (owner, version, ACL, contrato).
5. Dashboard observabilidad activo con metricas del paquete.
6. Politica retencion memoria aprobada por seguridad/juridica.
7. Pipeline CI/CD con gates de evaluacion y seguridad.

## Stack Tecnologico V 0.5

| Tecnologia | Capa | Necesidad que resuelve | Razon tecnica | Riesgo mitigado | Prioridad | Dependencias |
| --- | --- | --- | --- | --- | --- | --- |
| Azure AI Search | Knowledge / RAG | Vector store + busqueda hibrida + reranking | Estandar corporativo (H1). HNSW + keyword + semantic ranker integrado. | Fragmentacion de soluciones vectoriales | Obligatorio | Embedding Service |
| Azure OpenAI text-embedding-3-large | Knowledge | Generacion de embeddings | 3072 dimensiones, ya en uso (Insuregent). Versionable. | Inconsistencia de embeddings | Obligatorio | Azure OpenAI subscription |
| Cosmos DB | Memory | Memoria conversacional + operacional | Ya en uso (Insuregent). Particionable por tenant. TTL nativo. | Memoria sin gobierno de retencion | Obligatorio | Azure subscription |
| ADLS Gen2 | Data / Knowledge | Data Lake (Bronze/Silver/Gold) + Document Store | Estandar corporativo. Medallion. Cold tier. | Datos sin linaje ni capas | Obligatorio | Azure subscription |
| Azure Document Intelligence | Knowledge (Pipeline) | OCR + extraccion estructurada | Integrado con Azure. Soporta PDFs complejos. | Documentos no procesables | Obligatorio | Azure subscription |
| Microsoft Purview / Unity Catalog | Governance | Catalog de datos y conocimiento | Linaje, clasificacion, RBAC, descubrimiento. | Knowledge sin gobierno | Recomendado | Licenciamiento |
| Azure Redis Cache | Memory (Session) | Cache de sesion para velocidad | Reduce latencia en consultas repetidas. TTL nativo. | Latencia alta en sesiones frecuentes | Opcional | Azure subscription |
| LiteLLM | Gateway | LLM Gateway (PIL) multi-backend | Routing, auth, rate limit, cost tracking. Evita lock-in. | Vendor lock-in a un PIM | Recomendado | Despliegue propio |
| MLflow | Governance / Evaluations | Experiment tracking + evaluaciones | Estandar industria. Integra con Databricks. | Evaluaciones sin registro | Recomendado | Databricks o standalone |
| OpenTelemetry + OpenLLMetry | Observability | Trazas E2E vendor-neutral | Estandar industria. Correlacion trace_id. | Sin visibilidad del flujo | Obligatorio | Collector + backend (Dynatrace/AppInsights) |
| Databricks | Data (ETL avanzado) | Procesamiento Silver/Gold a escala | Ya en produccion para ML (8 modelos). Spark para volumenes grandes. | Pipeline no escalable | Recomendado (volumenes altos) | Licenciamiento Databricks |
| Azure Container Apps Job | Knowledge (Pipeline) | Ejecucion programada de ingesta | Patron Insuregent. Serverless, schedule | Pipeline sin automatizacion | Obligatorio | Azure subscription |
| MongoDB Atlas | Memory / Data | Memoria largo plazo, streaming non-relational | Flexible schema. | N/A | Futuro (evaluar vs Cosmos) | Licenciamiento MongoDB |
| Striim (CDC) | Data | CDC desde transaccionales | Presente en referencia. Util para memoria operacional real-time. | N/A | Opcional (caso especifico) | Licenciamiento Striim |
| Knowledge Graph (Graph DB) | Knowledge | Relaciones entre entidades | Alto valor en dominios con interrelacion fuerte. | N/A | Futuro (esperar caso) | Ontologia definida |
