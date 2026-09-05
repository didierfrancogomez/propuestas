---
titulo: "Arquitectura de implementación"
id: 6243680318
espacio: AFGLYP
version: 3
actualizado: 2026-08-28T20:46:31.906Z
actualizado_por: "Diego Fernando Gomez Alvarez"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6243680318
---

# Arquitectura de implementación

Esta página consolida la arquitectura de implementación de la Plataforma Agéntica, aterrizando la arquitectura de referencia en un stack tecnológico concreto para el Control Plane y la Capa de Dominio. Su propósito es servir como insumo base para el diseño de soluciones agénticas, con foco en claridad de responsabilidades, trazabilidad tecnológica y decisiones de arquitectura.

> **[INFO]**
> **Contexto del documento fuente.** Gobierno y Arquitectura de TI · Transformación de Arquitectura y Modernización (TAM) · Práctica AI-First · Medellín, Colombia · 2026-08-25

# Resumen ejecutivo

La plataforma no se concibe como una sola herramienta, sino como una capacidad compuesta por servicios especializados que separan con claridad el gobierno transversal del runtime agéntico y de las capacidades de negocio. Esta realización tecnológica parte del stack validado en la PoC del Control Plane y de la decisión arquitectónica de usar Azure API Management (APIM) como capa de API/AI Gateway del frente de IA.

El **Control Plane** concentra gobierno, acceso, seguridad, observabilidad, lifecycle y control de consumo. La **Capa de Dominio** agrupa la ejecución del agente, la exposición de capacidades de negocio y el dominio de información y conocimiento. El runtime agéntico reside en Azure sobre contenedores, mientras que el acceso a modelos se desacopla por medio del LLM Gateway, permitiendo consumo multi-nube sin cambiar el contrato del agente.

| Plano | Capacidad | Realización tecnológica |
| --- | --- | --- |
| Control Plane | AI / A2A / MCP Gateway | Azure API Management (APIM) + Entra ID |
| Control Plane | LLM / Model Gateway | LiteLLM + Azure AI Foundry |
| Control Plane | AI/LLM Lifecycle | Langfuse + PostgreSQL Flexible + ClickHouse interno |
| Control Plane | AI Security Enforcement | Entra ID, APIM policies, Azure AI Content Safety, Microsoft Presidio |
| Capa de Dominio | Agent Runtime | AKS + LangGraph (Python) + MCP interno |
| Capa de Dominio | Application Runtime | Microservicios Java y Python sobre AKS |
| Capa de Dominio | Information Domain | Databricks + Unity Catalog + ADLS + Azure AI Search |
| Capa de Dominio | Memory Layer | Azure Cosmos DB / estado en runtime |
| Transversal | Identidad y secretos | Entra ID, Managed Identity, Azure Key Vault |
| Transversal | Observabilidad | Application Insights, Log Analytics, Azure Monitor |
| Transversal | Experiencia | Azure Static Web App (Angular SPA) |

note3606b44e4235
Esta arquitectura de implementación está acotada al frente de IA y no sustituye la estrategia corporativa de apificación de negocio soportada en Apigee. Ambas capas coexisten con responsabilidades diferenciadas.

Esta arquitectura de implementación está acotada al frente de IA y no sustituye la estrategia corporativa de apificación de negocio soportada en Apigee. Ambas capas coexisten con responsabilidades diferenciadas.

# Contexto y objetivo

## Contexto

La evolución hacia soluciones agénticas introduce una Plataforma Agéntica como núcleo compartido para construir, exponer, operar y gobernar agentes de IA de forma reusable, segura y escalable. La arquitectura de referencia define las capacidades esperadas; esta arquitectura de implementación define cómo se materializan en tecnologías concretas.

## Objetivos

- Aterrizar la arquitectura de referencia en un stack tecnológico concreto y trazable.
- Dar claridad sobre la implementación del Control Plane y la Capa de Dominio.
- Asociar cada capacidad del blueprint a un componente tecnológico, su rol y sus dependencias.
- Documentar topología de despliegue, capacidades transversales y decisiones arquitectónicas.

## Alcance y fuera de alcance

| En alcance | Fuera de alcance |
| --- | --- |
| Realización tecnológica del Control Plane y de la Capa de Dominio. | Diseño detallado de productos de dominio y modelos de datos específicos. |
| Mapeo capacidad a componente, topología y capacidades transversales. | Evaluación económica detallada por licenciamiento y decisión final de adquisición. |
| Patrón de comunicación gobernado por gateways. | Definición cerrada del modelo de operación y segregación de responsabilidades del Control Plane. |
| Coexistencia con la estrategia de apificación de negocio. | Selección de una plataforma dedicada de AI Security como decisión final independiente. |

# Marco de referencia

La Plataforma Agéntica se organiza en dos planos principales: **Control Plane** y **Capa de Dominio**. Esta separación permite distinguir el gobierno transversal de la ejecución agéntica y de la exposición de capacidades y conocimiento del negocio.

## Control Plane

Concentra el gobierno transversal: acceso a modelos, herramientas y agentes; ciclo de vida de prompts y evaluaciones; observabilidad; seguridad específica de IA; y control de costos y cuotas.

## Capa de Dominio

Agrupa el runtime agéntico, la exposición de capacidades de negocio y el dominio de información y conocimiento. El agente orquesta, pero no absorbe la lógica transaccional ni la propiedad de las fuentes de datos.

# Principios de implementación

1. Separación de responsabilidades entre runtime, conocimiento empresarial, tools, modelos y capacidades transversales.
2. Punto único de control mediante gateways y registries compartidos.
3. Gobierno del runtime en Azure; los modelos pueden residir en otras nubes vía LLM Gateway.
4. Trazabilidad extremo a extremo por usuario, canal, sesión, agente, tool, modelo y fuente.
5. Seguridad y cumplimiento desde el diseño, con controles explícitos y verificables.
6. Adopción de estándares abiertos y contratos explícitos como MCP y A2A.
7. Evolución incremental con soluciones productizadas o componibles y topología federada.

# Stack tecnológico de referencia

![image-20260828-204557.png](../../recursos/6243680318/image-20260828-204557.png)

## Topología de despliegue

- **Perímetro y acceso:** experiencia en Static Web App (Angular SPA), autenticación con Entra ID y acceso por HTTPS/REST a través de gateways.
- **Cómputo agéntico:** Agent Runtime y MCP internos desplegados como contenedores sobre AKS, aislados por namespaces.
- **Gateways del Control Plane:** APIM como gateway de entrada, LiteLLM como LLM Gateway y Langfuse para lifecycle de prompts.
- **Dominio de información:** Databricks con Unity Catalog, fuentes en SharePoint y Confluence, almacenamiento en ADLS y publicación en Azure AI Search.
- **Patrón de comunicación:** todo el tráfico hacia modelos, tools y agentes pasa por gateways, incluso entre componentes en el mismo clúster.

# Implementación del Control Plane

## AI Gateway

Es la puerta de entrada obligatoria para el tráfico agéntico. Se implementa sobre APIM, integrando autenticación con Entra ID, cuotas, rate limiting, trazabilidad y gobierno centralizado.

## A2A Gateway

Gestiona registro, descubrimiento y acceso entre agentes mediante A2A Agent APIs sobre APIM. Se habilita selectivamente cuando un caso de uso requiere colaboración real entre agentes, con confianza mutua, validación de identidad, delegación y prevención de bucles.

## MCP Tool Gateway & Registry

Centraliza control de acceso a MCP servers internos y de terceros. Define qué agente accede a qué MCP mediante políticas, roles, cuotas, rate limiting y observabilidad unificada. Se implementa sobre APIM.

Los MCP servers derivados de APIs de negocio se despliegan por fuera del Control Plane, en su propio entorno ligado al dominio. Los MCP internos del agente se despliegan junto al runtime en AKS.

## LLM / Model Gateway

Abstrae y gobierna el acceso a proveedores de modelos con selección, routing, fallback, control de acceso y límites de tokens. Se materializa con LiteLLM como gateway y Azure AI Foundry como proveedor gobernado de modelos y servicios cognitivos. Este desacoplamiento permite consumir modelos externos, por ejemplo en GCP, sin cambiar el contrato de consumo del agente.

## AI/LLM Lifecycle Management

Gestiona prompts, configuraciones, evaluaciones y trazas de calidad como artefactos versionados y trazables. Se implementa con Langfuse, apoyado en PostgreSQL Flexible. ClickHouse se usa únicamente como prerrequisito técnico interno de Langfuse y no debe tratarse como una capacidad independiente de observabilidad.

> **[NOTA]**
> El acceso directo y abierto de equipos a la herramienta de prompts no se recomienda. La contribución y publicación debe realizarse mediante pipeline automatizado, con administración restringida a operadores del Control Plane y con auditoría y versionado.

## FinOps

Gobierna el consumo económico de modelos, tools y capacidades agénticas en dos niveles: enforcement en tiempo real cerca del gateway con límites, budgets, fallback y throttling; y análisis corporativo mediante herramientas de costo cloud para habilitar showback y chargeback por dominio, producto, agente, modelo o entorno.

## AI Security Enforcement

Combina políticas de gateway con servicios especializados. En el gateway se aplican autenticación, autorización contextual, allow-lists, scopes, límites y trazabilidad. Los controles semánticos y de contenido se resuelven con Azure AI Content Safety y Microsoft Presidio.

| Capacidad | Componente | Rol en la implementación |
| --- | --- | --- |
| AI Gateway | Azure API Management | Punto único de acceso gobernado; autenticación, cuotas y trazabilidad. |
| A2A Gateway | APIM (A2A APIs) | Mediación gobernada entre agentes con confianza y delegación. |
| MCP Gateway | APIM (MCP registry) | Control de acceso centralizado a MCP servers. |
| LLM Gateway | LiteLLM | Routing, fallback, límites de tokens y operación multi-modelo. |
| Modelos y cognitivos | Azure AI Foundry | Proveedor gobernado de modelos y servicios de seguridad y contenido. |
| Prompt & Eval | Langfuse + PostgreSQL Flexible | Versionado de prompts, evaluaciones y trazabilidad de calidad. |
| Store interno | ClickHouse | Prerrequisito técnico interno de Langfuse. |
| FinOps | APIM policies + LiteLLM + Cost Management | Enforcement de consumo y análisis de costos. |
| AI Security | Content Safety + Presidio + Entra ID | Guardrails, DLP/PII y autorización contextual. |

# Implementación de la Capa de Dominio

## Agent Runtime

Es la unidad de ejecución del agente. Administra intención, plan, memoria, invocación de herramientas y consolidación de respuesta, sin absorber la lógica transaccional. Se despliega sobre AKS y se construye con LangGraph en Python. Incluye orquestación, frameworks, tools, prompts en runtime y cliente MCP.

Soporta el patrón de agente singular y la evolución hacia patrones multiagente lógicos como orchestrator-worker, planner-executor-reviewer y event-driven.

## Memory Layer

Distingue memoria de corto plazo, sostenida en el runtime, de memoria durable de largo plazo, materializada en Azure Cosmos DB. La memoria del agente se mantiene separada del conocimiento empresarial gobernado.

## Domain Capability Exposure

Las capacidades del dominio se exponen mediante Domain APIs, Domain MCP Tools y Domain Events. No toda API se convierte en MCP; solo aquellas donde la semántica de tool agrega valor.

## Application Runtime

La lógica de negocio del dominio se implementa en microservicios Java y Python sobre AKS. Estos servicios son consumidos y orquestados por el agente, pero continúan siendo propiedad del dominio.

## Information Domain

Convierte información gobernada en conocimiento utilizable por agentes. Se implementa con pipelines en Databricks y Unity Catalog, fuentes en SharePoint y Confluence, almacenamiento en ADLS e índices semánticos/vectoriales en Azure AI Search para grounding y RAG.

| Capacidad | Componente | Rol en la implementación |
| --- | --- | --- |
| Agent Runtime | AKS + LangGraph (Python) | Orquestación cognitiva del agente y tool use gobernado. |
| MCP interno | Internal MCP Servers (AKS) | Herramientas privadas del dominio del agente. |
| Memory Layer | Azure Cosmos DB | Memoria episódica durable; estado activo en runtime. |
| Domain APIs | APIM + APIs de dominio | Exposición síncrona canónica alineada con API-Led. |
| Application Runtime | Microservicios Java / Python (AKS) | Lógica transaccional del negocio. |
| Knowledge Prep | Databricks + Unity Catalog | Ingesta, transformación, embeddings y curaduría. |
| Data stores / fuentes | ADLS · SharePoint · Confluence | Almacenamiento y fuentes del conocimiento. |
| Índices / retrieval | Azure AI Search | Índices semánticos y vectoriales para RAG. |

# Capacidades transversales

## Identidad y autenticación

Entra ID es la plataforma de identidades humanas y no humanas. La autenticación se soporta con OAuth2/OIDC/JWT, mientras que service principals y Managed Identity resuelven identidades técnicas. APIM se integra de forma nativa para habilitar autorización contextual.

## Observabilidad

La observabilidad extremo a extremo se instrumenta con OpenTelemetry y se centraliza en Application Insights, Log Analytics y Azure Monitor. Se preserva evidencia auditable de ejecución sin almacenar el razonamiento interno del modelo.

## Gestión de secretos

Azure Key Vault administra secretos, tokens y credenciales bajo un enfoque zero-trust, complementado con private endpoints y RBAC.

## Experiencia e interacción

La experiencia conversacional se materializa en una Static Web App basada en Angular SPA, desacoplada del plano agéntico y consumiendo la plataforma a través del contrato de interacción y del AI Gateway.

# Mapa de capacidades a componentes tecnológicos

| Plano / capa | Capacidad | Componente | Nube / plano |
| --- | --- | --- | --- |
| Experiencia | Cliente web / Chat | Static Web App (Angular SPA) | Azure |
| Autenticación | Identidad y acceso | Entra ID · App Registration · MS Graph | Azure |
| Control Plane | AI Gateway | Azure API Management | Azure |
| Control Plane | A2A Gateway | APIM (A2A APIs) | Azure |
| Control Plane | Modelos externos | Otros proveedores (Por ejemplo, Vertex AI Generative Models) | GCP, AWS |
| Control Plane | MCP Gateway | APIM (MCP registry) | Azure |
| Control Plane | API/MCP Gateway de negocio | Apigee | GCP |
| Control Plane | LLM Gateway | LiteLLM | Azure (AKS) |
| Control Plane | Modelos y cognitivos | Azure AI Foundry (Models, Content Safety, Presidio) | Azure |
| Control Plane | Prompt & Eval | Langfuse + ClickHouse | Azure (AKS) |
| Control Plane | BD transversal | Azure PostgreSQL Flexible | Azure |
| Dominio | Agent Runtime | AKS + LangGraph (Python) | Azure (AKS) |
| Dominio | MCP interno | Internal MCP Servers | Azure (AKS) |
| Dominio | Application Runtime | Microservicios Java / Python | Azure (AKS) |
| Dominio | Memory durable | Azure Cosmos DB | Azure |
| Dominio | Knowledge Prep | Databricks + Unity Catalog | Azure |
| Dominio | Almacenamiento | Azure Data Lake Storage | Azure |
| Dominio | Fuentes | SharePoint · Confluence | Corporativo |
| Dominio | Índices / retrieval | Azure AI Search | Azure |
| Transversal | Secretos | Azure Key Vault | Azure |
| Transversal | Identidad técnica | Azure Managed Identity | Azure |
| Transversal | Observabilidad | App Insights · Log Analytics · Monitor | Azure |

# Decisiones de arquitectura

## APIM como capa de API/AI Gateway del Control Plane

Se adopta APIM como capa de AI/A2A/MCP Gateway del Control Plane agéntico, manteniendo Apigee como estándar corporativo para APIs de negocio y aliados. La decisión se fundamenta en el gobierno de cargas agénticas en Azure y en la integración nativa de APIM con Entra ID y el ecosistema Microsoft.

## MCP Gateway permanente y MCP servers fuera del Control Plane

El MCP Gateway se confirma como componente permanente del Control Plane para gestión centralizada de acceso. Los MCP servers de negocio viven fuera del Control Plane, ligados al dominio correspondiente.

## LiteLLM y Langfuse como tecnologías open del Control Plane

LiteLLM y Langfuse se seleccionan como tecnologías open para desacoplamiento funcional y flexibilidad. ClickHouse queda restringido a su rol técnico interno dentro de Langfuse y no se considera una plataforma corporativa de observabilidad.

## Runtime agéntico en Azure Container/AKS

El runtime agéntico reside en Azure. Para agentes singulares y livianos puede privilegiarse Azure Container Apps; para escenarios de mayor densidad, multiagente o múltiples MCP servers, AKS es el entorno natural.

# Definiciones abiertas y próximos pasos

1. Ratificar la decisión de gateway en un foro con mandato de estrategia de IA.
2. Cerrar el modelo de operación y sostenibilidad del Control Plane.
3. Definir postura multi-nube y multi-región, así como estrategia de exposición a aliados.
4. Automatizar el onboarding de dominios agénticos y construir aceleradores operativos del AI Gateway.
5. Definir el mecanismo de contribución de prompts vía pipeline y sus controles de acceso.
6. Planificar la incorporación de una capa dedicada de AI Security según madurez y volumen.
7. Publicar una primera versión MVP del Control Plane y evolucionarla de forma incremental.

# Referencias

- Equipo TAM. Blueprint de Capacidades de la Arquitectura Agéntica. SURA.
- Equipo TAM. Control Plane — Definición de capacidades y mapa de gobierno. SURA.
- Equipo TAM. Domain Layer — Runtime, exposición de capacidades y dominio de información. SURA.
- Equipo TAM. AI Gateway — LLM, MCP y A2A Gateway. SURA.
- Equipo TAM. AI/LLM Lifecycle Management. SURA.
- Equipo TAM. AI Security Enforcement. SURA.
- Equipo TAM. FinOps del Control Plane. SURA.
- Equipo TAM. Catálogo de capacidades agénticas. SURA.
- Equipo TAM. Arquitectura de Implementación para la construcción de Agentes de IA (v1.1). SURA.
- Equipo TAM. ADR — APIM vs. Apigee como capa de API/AI Gateway del Control Plane agéntico (v2.1). SURA.
- [Microsoft. Azure API Management policy reference.](https://learn.microsoft.com/azure/api-management/api-management-policies)
- [Microsoft. Azure AI Foundry documentation.](https://learn.microsoft.com/azure/ai-foundry/)
- [Microsoft. Azure AI Content Safety documentation.](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [OWASP Foundation. OWASP Top 10 for Large Language Model Applications.](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
