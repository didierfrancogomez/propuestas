---
titulo: "Agentic Runtime"
id: 5838045207
espacio: AFGLYP
version: 6
actualizado: 2026-07-03T21:53:04.055Z
actualizado_por: "Helbert Sebastian Cubillos Avila"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > Blueprint de Capacidades Arquitectura Agéntica > Agentic Platform > Domain Layer"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5838045207
---

# Agentic Runtime

El Agentic Runtime v2 separa con claridad las capacidades de coordinación, memoria y conocimiento respecto del gobierno, el acceso a tools y la exposición de capacidades de dominio. El objetivo es que el runtime conserve foco en la ejecución agéntica, mientras que las capas de Domain Capabilities e Information Domain proporcionan servicios especializados, gobernados y reutilizables.

## 5.1. Rol arquitectónico

Constituye el núcleo técnico de la arquitectura agéntica. Es la capa donde se ejecuta la lógica central que permite diseñar, orquestar, ejecutar y gobernar agentes de forma estandarizada, desacoplada y escalable. A su vez, es la capa encargada de gestionar el runtime, prompts, memoria y conocimiento del agente. No debe asumir responsabilidades propias de:

- La experiencia de usuario.
- La identidad corporativa.
- El gobierno enterprise de apis.
- La observabilidad de infraestructura.
- La ingeniería de datos del dominio.

Su responsabilidad es proporcionar una base común para que agentes simples o múltiples agentes operen de manera segura, gobernada y reusable.

## 5.2. Responsabilidades principales

Las responsabilidades principales del Agent Runtime son:

- Gestionar sesiones y estado de ejecución.
- Coordinar razonamiento, tool use y resolución de pasos.
- Recuperar y persistir contexto mediante la capa de memoria.
- Consumir conocimiento empresarial de forma controlada.
- Interactuar con tools y capacidades expuestas mediante MCP.
- Soportar ejecución síncrona y asíncrona.
- Emitir trazabilidad, métricas y eventos operacionales.

## 5.3.Marco de prácticas y lineamientos Agent Runtime

| **Principio** | **Implicación de diseño** | **Resultado esperado** |
| --- | --- | --- |
| Prompts como código | Los prompts se versionan, evalúan y promueven como artefactos independientes del runtime, con rollback y evidencia de cambio. | Mayor trazabilidad y releases seguros. |
| Retrieval desacoplado del agente | El agente consume knowledge products, retrieval APIs o MCP, no accede de forma directa y arbitraria a repositorios del dominio. | Menor acoplamiento y mejor gobierno del dato. |
| Memoria con tipologías explícitas | Se separa session state, working memory, memoria episódica y memoria durable, cada una con políticas de retención y acceso. | Contexto más preciso, auditable y reusable. |
| Tools por contrato | Toda acción se expone por MCP o APIs gobernadas, con autorización contextual, cuotas y confirmaciones para acciones sensibles. | Operación segura y consistente entre agentes. |
| Datos como productos de dominio | Los datasets RAG, colecciones curadas, índices semánticos y ontologías tienen owner, calidad y controles de acceso explícitos. | Grounding confiable y evolución independiente del dominio. |
| Observabilidad y evaluaciones obligatorias | Cada release debe incorporar trazas, logs, métricas de calidad/costo y datasets de evaluación para regresión. | Operación gobernada y mejora continua. |
| Security y FinOps en la ruta de ejecución | Las políticas de DLP, PII redaction, quotas y routing de modelos se aplican en gateways y hooks del runtime. | Riesgo y costo controlados por diseño. |

Tabla 1 – Marco de prácticas y lineamientos Agentic Runtime

## 5.4. Patrones internos del Runtime

**Runtime centrado en Orchestrator Agent**

El patrón base del Runtime consiste en un Orchestrator Agent que:

- Recibe la intención, solicitud o tarea.
- Determina el flujo de ejecución.
- Selecciona tools y capacidades.
- Resuelve memoria y contexto.
- Consume productos y servicios de dominio.
- Coordina subagentes cuando la tarea requiere especialización.

**Tool use gobernado**

Las tools no deben ser invocadas directamente desde prompts sin mediación de contratos y políticas. La resolución de herramientas debe apoyarse en:

- Registries
- Contratos
- Autorizaciones
- Controles de observabilidad
- Políticas de uso

**Retrieval desacoplado del agente**

El agente no debería conectarse de forma directa a cualquier repositorio o base de datos. El acceso al conocimiento debe realizarse preferentemente a través de:

- Productos de conocimiento
- Índices semánticos
- Retrieval apis
- Mcps de dominio

Esto mejora seguridad, calidad de grounding y evolución independiente del dominio.

# 6. Patrones de implementación

La versión 2 de la arquitectura no sustituye el patrón de agente singular, lo complementa como un patrón de implementación para tareas donde la especialización, la separación de responsabilidades o la necesidad de control adicional justifican el costo y la complejidad operacional.

| **Rol** | **Responsabilidad principal** | **Cuándo usarlo** | **Owner del ciclo** |
| --- | --- | --- | --- |
| Orchestrator | Recibe la tarea, decide el flujo, controla estado, aplica políticas y consolida la respuesta final. | Siempre que exista coordinación de pasos, tools o subagentes. | Platform / equipo del agente |
| Planner / Router | Descompone la tarea, define el plan y selecciona el patrón o agente especialista adecuado. | Casos complejos, multietapa o con múltiples fuentes. | Platform / dominio |
| Specialist Agent | Ejecuta subtareas acotadas: retrieval, análisis, clasificación, composición o acción. | Cuando conviene encapsular expertise y reducir complejidad individual. | Dominio o capability owner |
| Reviewer / Safety Agent | Valida formato, cumplimiento, grounding, riesgo o preparación antes de devolver o ejecutar. | Tareas críticas, regulatorias o con alto impacto. | Security / calidad / dominio |
| Human Supervisor | Aprueba, corrige o confirma acciones sensibles y alimenta aprendizaje operacional. | Operaciones críticas, umbrales de riesgo altos o degradaciones. | Negocio / operación |

Tabla 2 – Roles en el Agentic Runtime

## 6.1 Roles multiagente

### 6.1.1 Orchestrator

El **orchestrator** es el responsable del flujo completo. Su función no es hacer todo, sino coordinar el trabajo.

Responsabilidades:

- Recibir la solicitud inicial desde API, canal digital, evento o sistema externo.
- Crear o recuperar el contexto de ejecución.
- Definir el flujo general de trabajo.
- Invocar al planner/router cuando se requiere descomposición o enrutamiento.
- Delegar tareas a especialistas.
- Controlar handoffs entre agentes o capacidades.
- Aplicar límites de iteración, tiempo, costo y número de herramientas.
- Consolidar el resultado final.
- Garantizar trazabilidad de cada decisión, herramienta y transición.

Este rol se materializa principalmente en el **Planeador / Orquestador** del Agent Core, implementado con LangGraph / LangChain, donde se modela el flujo como grafo de estados y se controla la decisión de uso de herramientas, memoria, prompts, políticas y LLM.

note31c850379448
**Handoff**: proceso mediante el cual un agente de IA transfiere la responsabilidad de una tarea, el contexto de la conversación y el control a otro agente especializado

**Handoff**: proceso mediante el cual un agente de IA transfiere la responsabilidad de una tarea, el contexto de la conversación y el control a otro agente especializado

### 6.1.2 Planner / Router

El **planner/router** convierte una intención en un plan ejecutable. Puede estar embebido en el orchestrator o implementarse como nodo lógico separado dentro del grafo.

Responsabilidades:

- Interpretar la intención y clasificar el tipo de tarea.
- Decidir si el flujo requiere agente singular, rol especializado, especialista externo o intervención humana.
- Dividir el objetivo en subtareas.
- Seleccionar rutas de ejecución.
- Determinar qué herramientas o especialistas se requieren.
- Definir condiciones de handoff.
- Decidir si el flujo debe ser síncrono, asincrónico o event-driven.

Este rol debe favorecer decisiones explícitas, no implícitas. Cada decisión de ruta debe quedar registrada en telemetría y auditoría.

### 6.1.3 Specialist

El **specialist** es un agente, nodo o capacidad especializada en un dominio o tarea específica.

Ejemplos:

- Especialista documental.
- Especialista legal.
- Especialista médico.
- Especialista comercial.
- Especialista de integración con sistemas core.
- Especialista RAG.
- Especialista de validación determinística.
- Especialista de extracción estructurada.
- Especialista de cálculo o simulación.

Responsabilidades:

- Ejecutar una tarea acotada.
- Usar únicamente las herramientas autorizadas para su rol.
- Retornar resultados estructurados.
- No decidir fuera de su dominio.
- No ejecutar acciones sensibles sin autorización del orquestador o revisor.
- Exponer métricas de éxito, error, latencia y uso de herramientas.

El specialist no debe convertirse en un “mini-orquestador” sin control. Si un especialista requiere delegar a otros especialistas, debe regresar el control al orchestrator.

### 6.1.4 Reviewer / Safety

El **reviewer/safety** es el rol de control antes de una salida o acción relevante.

Responsabilidades:

- Validar si la respuesta cumple el objetivo.
- Revisar consistencia con fuentes, políticas y reglas de negocio.
- Detectar posibles alucinaciones, fuga de información, sesgos o contenido no permitido.
- Validar estructura de respuesta.
- Revisar si una acción propuesta requiere aprobación humana.
- Aplicar guardrails antes y después de la invocación al LLM.
- Registrar la evaluación y decisión.

Este rol se implementa con una combinación de validaciones determinísticas, políticas, guardrails, evaluación automática y revisión humana según criticidad. La arquitectura de implementación ya define un componente **Role Policy and GuardRails** para validar permisos, reglas de ejecución y restricciones de herramientas, y separarlo del planeador para permitir auditoría independiente y evolución hacia motores de política como Casbin u OPA.

### 6.1.5 Human Supervisor

El **human supervisor** es el responsable humano que interviene cuando la autonomía del sistema no debe ser completa.

Responsabilidades:

- Aprobar acciones de alto impacto.
- Resolver ambigüedades que el agente no puede decidir.
- Corregir resultados.
- Revisar excepciones.
- Autorizar handoffs sensibles.
- Suspender o retirar un agente.
- Actuar como owner funcional o técnico del agente.

En la arquitectura de referencia ya aparece el **Usuario Owner** como actor clave para configuración, supervisión y activación de casos de uso, reforzando el rol de gobierno funcional en el marco AI-First.

---

## 6.3. Patrón Multi-Agent tipo orchestrator-worker

**Definición**

Patrón donde un orquestador central recibe la solicitud, decide el plan, delega subtareas a workers o especialistas, consolida resultados y controla la respuesta final.

**Aplicabilidad**

Este patrón es apropiado para:

- Tareas complejas que requieren especialización.
- Procesamiento sobre múltiples fuentes o dominios.
- Se necesita controlar permisos y herramientas por rol.
- Se requiere evitar coordinación libre entre agentes.
- Separación explícita entre planeación y ejecución.
- Se requiere trazabilidad centralizada.
- Escenarios donde subagentes encapsulan capacidades diferenciadas.

**Cómo Implementarlo**

En la primera versión, el patrón se debe implementar como orquestación centralizada dentro del Agent Runtime, usando LangGraph como grafo de estados. Los workers pueden ser nodos lógicos, tools especializadas o servicios MCP privados. No necesariamente deben desplegarse como agentes independientes desde el inicio.

Implementación sugerida:

- Orchestrator: Planeador / Orquestador.
- Workers: nodos especializados del grafo o tools expuestas por MCP Privado.
- Router: Enrutador de Tools.
- Validaciones: Role Policy and GuardRails.
- Memoria: Manejador de Sesión + Memory Manager.
- Observabilidad: OpenTelemetry.
- Integración: APIs gobernadas, MCP o mensajería.

**Ejemplos de implementación:**

- Atención de solicitudes complejas sobre pólizas, donde se requieren especialistas de producto, reclamaciones, documentos y reglas.
- Análisis de un caso de siniestro donde se consultan documentos, historial, reglas, coberturas y sistemas transaccionales.
- Asistente interno de soporte experto que enruta entre conocimiento legal, médico, comercial y operativo.

## 6.4. Patrón Multi-Agent planner-executor-reviewer

**Definición**

Patrón donde el flujo se divide en tres momentos: planear, ejecutar y revisar.

- **Planner:** diseña el plan.
- **Executor:** ejecuta herramientas o subtareas.
- **Reviewer:** valida resultado, seguridad, cumplimiento y calidad.

**Aplicabilidad**

Este patrón es apropiado para:

- La tarea requiere varios pasos.
- El resultado puede afectar decisiones de negocio.
- Se requiere explicar o auditar el proceso.
- Hay riesgo de respuestas incorrectas o incompletas.
- Se necesita separar quien propone de quien valida.

**Roles**

- Planner: descompone la tarea y propone el plan de ejecución.
- Executor: realiza consultas, retrieval y acciones.
- Reviewer: valida consistencia, seguridad, calidad y cumplimiento de políticas.

**Alineación con la arquitectura**

Este patrón se soporta de manera natural con:

- Orchestrator Agent como coordinador.
- Sub Agents especializados.
- Evaluations y Guardrails en el Control Plane.
- Memory Layer para continuidad.
- Domain Products y Domain APIs como fuentes externas.

**Como implementarlo:**

En la primera versión, el patrón se debe implementar como **orquestación centralizada dentro del Agent Core**, usando LangGraph como grafo de estados. Los workers pueden ser nodos lógicos, tools especializadas o servicios MCP privados. No necesariamente deben desplegarse como agentes independientes desde el inicio.

Este patrón debe ser considerado **obligatorio para flujos de riesgo medio o alto**.

Implementación sugerida:

1. El planner construye un plan estructurado.
2. El executor invoca herramientas, APIs, RAG o MCP.
3. El reviewer valida:

      - fuentes usadas,
      - restricciones de rol,
      - formato de salida,
      - reglas de negocio,
      - seguridad,
      - necesidad de aprobación humana.
4. Si falla la revisión, el flujo puede:

      - corregirse automáticamente,
      - pedir más información,
      - escalar a supervisor humano,
      - detenerse.

> **[INFO]**
> El reviewer puede usar validaciones determinísticas, reglas de negocio, guardrails, evaluaciones con LLM-as-a-judge o revisión humana

**Ejemplos de implementación:**

- Generación de conceptos técnicos o legales.
- Recomendaciones comerciales con impacto en cliente.
- Validación documental para procesos de reembolso, reclamación o suscripción.
- Generación de respuestas para asesores donde se requiere consistencia normativa.

## 6.5. Patrón asíncrono orientado a eventos

**Definición**

Patrón donde el agente no se activa únicamente por una petición síncrona de usuario, sino por eventos de negocio o técnicos.

Un evento puede iniciar, continuar o cerrar una ejecución agéntica.

**Aplicabilidad**

Es pertinente para:

- El proceso es asincrónico.
- La tarea puede tardar más que una interacción request/response.
- El agente debe reaccionar a cambios de estado.
- Se requiere desacoplar sistemas.
- Hay integración con flujos empresariales o core transaccional.
- Se necesita resiliencia mediante reintentos y DLQ.

**Como implementarlo:**

La arquitectura de implementación ya contempla un **Event Listener** que consume eventos desde broker, habilita retries, DLQ y procesamiento idempotente, permitiendo que el agente sea reactivo y no solo request/response.

Implementación sugerida:

- El sistema dueño del proceso publica el evento.
- El agente consume el evento mediante Event Listener.
- El orchestrator crea una ejecución correlacionada.
- El planner decide la ruta.
- Los specialists ejecutan tareas.
- El reviewer valida salida o acción.
- El resultado se publica como evento, se persiste o se comunica al canal correspondiente.

**Ejemplos de implementación**:

- Evento de radicación de PQR.
- Evento de recepción de documento.
- Evento de cambio de estado de una reclamación.
- Evento de actualización de póliza.
- Evento de alerta operativa o técnica.
- Evento de disponibilidad de un resultado de análisis.

# 7. Lifecycle multiagente

## 7.1 Registro

Todo agente, rol o especialista debe registrarse antes de operar.

Artefacto sugerido: **Agent Manifest**.

Contenido mínimo:

- Nombre del agente o especialista.
- Owner funcional.
- Owner técnico.
- Dominio de negocio.
- Propósito.
- Nivel de agencia esperado.
- Patrón usado.
- Herramientas permitidas.
- Fuentes de conocimiento permitidas.
- Datos que puede consumir.
- Acciones que puede ejecutar.
- Reglas de handoff.
- Políticas de revisión.
- Criterios de escalamiento humano.
- Métricas mínimas.
- Riesgos identificados.
- Vigencia y fecha de revisión.

Decisión de gate:

- ¿Está registrado en inventario?
- ¿Tiene owner?
- ¿Tiene IdAPM o identificación equivalente?
- ¿Usa tecnologías permitidas por LBA?
- ¿Tiene matriz de riesgo?
- ¿Tiene trazabilidad y monitoreo definidos?

La LBA exige que toda aplicación o componente tecnológico en uso tenga responsable e identificación asociada; además, nuevas tecnologías deben pasar por aprobación de arquitectura técnica.

---

## 7.2 Ejecución

La ejecución inicia por petición de usuario, API, evento o tarea programada.

Durante la ejecución deben cumplirse estas reglas:

- Toda ejecución debe tener correlation ID.
- Toda decisión relevante debe quedar trazada.
- Toda herramienta debe invocarse con identidad propagada.
- Toda respuesta debe generarse con contexto controlado.
- Toda acción sensible debe pasar por reviewer o supervisor humano.
- Todo error debe clasificarse: técnico, funcional, seguridad, datos, modelo o herramienta.
- Toda ejecución debe tener límites de tiempo, costo, tokens, reintentos y herramientas.

Decisión de gate:

- ¿El agente puede continuar autónomamente?
- ¿Debe pedir más información?
- ¿Debe delegar a un especialista?
- ¿Debe escalar a humano?
- ¿Debe detenerse por política, riesgo o baja confianza?

---

## 7.3 Handoff

El handoff es la transferencia controlada de una tarea entre agentes, roles, herramientas o humanos.

Tipos de handoff:

- De orchestrator a specialist.
- De specialist a orchestrator.
- De executor a reviewer.
- De agente a supervisor humano.
- De flujo síncrono a flujo asincrónico.
- De agente a sistema transaccional mediante MCP o API.

Reglas mínimas:

- El handoff debe tener motivo explícito.
- Debe transferir contexto mínimo necesario, no todo el historial.
- Debe preservar identidad, permisos y trazabilidad.
- Debe declarar qué espera recibir de vuelta.
- Debe tener timeout.
- Debe tener ruta de fallback.
- Debe registrar resultado.

Decisión de gate:

- ¿El especialista está autorizado para esta tarea?
- ¿El contexto transferido contiene datos sensibles?
- ¿El handoff requiere aprobación humana?
- ¿El flujo puede perder contexto o duplicar acciones?
- ¿Existe idempotencia si se reintenta?

---

## 7.4 Monitoreo

El monitoreo no es opcional. En sistemas con autonomía, la observabilidad es un control de gobierno.

Métricas mínimas:

- Tasa de éxito de tarea.
- Tasa de uso exitoso de herramientas.
- Tasa de handoff.
- Tasa de escalamiento humano.
- Tasa de rechazo por guardrails.
- Latencia por agente o especialista.
- Costo por ejecución.
- Tokens consumidos.
- Errores por herramienta.
- Errores por integración.
- Hallucination rate o métrica equivalente cuando aplique.
- Incidentes de seguridad.
- Drift de comportamiento.
- Satisfacción o feedback de usuario.

La arquitectura de referencia posiciona observabilidad como habilitador transversal para operación, evaluación, calidad y mejora continua; también exige que los resultados de evaluaciones sean documentados, versionados y auditables.

Decisión de gate:

- ¿El agente mantiene desempeño aceptable?
- ¿Está aumentando el costo?
- ¿Está escalando demasiado a humano?
- ¿Está usando herramientas incorrectas?
- ¿Tiene más rechazos de seguridad?
- ¿Debe ajustarse prompt, política, herramienta, fuente o modelo?

---

## 7.5 Retiro

El retiro aplica cuando un agente, especialista, herramienta o patrón ya no debe operar.

Causales:

- No tiene owner.
- No tiene uso.
- Incumple LBA.
- Incumple políticas de seguridad.
- Presenta riesgo residual no aceptado.
- Su desempeño cae por debajo del umbral.
- Fue reemplazado por una capacidad corporativa.
- Tiene fuentes obsoletas.
- Usa modelo, librería o plataforma no autorizada.
- No cuenta con trazabilidad suficiente.

Actividades de retiro:

- Deshabilitar endpoint, evento o canal.
- Revocar permisos.
- Retirar secretos.
- Archivar configuración, prompts y trazas requeridas.
- Preservar evidencia para auditoría.
- Informar a owners y consumidores.
- Actualizar inventario.
- Ejecutar plan de reemplazo si aplica.

La LBA ya define consecuencias para incumplimiento tecnológico y retiro de componentes sin responsable u operación reciente; ese principio debe extenderse al gobierno de agentes.

# 8. Guía de implementación para equipos

## 8.1 Regla base

Antes de diseñar multiagente, el equipo debe responder:

1. ¿Realmente necesito un agente?
2. ¿El agente debe actuar o solo responder?
3. ¿El error tiene impacto alto?
4. ¿Tengo operación, monitoreo, seguridad y rollback?
5. ¿La complejidad exige múltiples especialistas?

## 8.2 Implementación recomendada por madurez

| Nivel | Implementación | Uso recomendado |
| --- | --- | --- |
| Nivel 1 | Agente singular | Casos acotados, pocas herramientas, alta trazabilidad |
| Nivel 2 | Agente singular con roles | Mismo runtime, comportamiento especializado por rol |
| Nivel 3 | Orchestrator–Worker lógico | Especialistas como nodos/tools dentro del mismo Agent Core |
| Nivel 4 | Planner–Executor–Reviewer | Flujos con validación independiente y riesgo medio/alto |
| Nivel 5 | Event-driven multiagent | Procesos asincrónicos, eventos de negocio, handoff y monitoreo avanzado |

## 8.3 Mapa de decisión de patrones

<!-- [macro: mermaid (size=large, isEditable=true, diagramCode=flowchart TD
  A[Inicio: caso de uso] --> B{Reglas claras y determinísticas?}
  B -- Sí --> C[Aplicación tradicional / workflow]
  B -- No --> D{Solo responder o resumir?}
  D -- Sí --> E[IA generativa simple / RAG]
  D -- No --> F{Requiere actuar en varios pasos?}
  F -- No --> E
  F -- Sí --> G{Complejidad alta o múltiples dominios?}
  G -- No --> H[Agente Singular]
  G -- Sí --> I{Requiere revisión independiente?}
  I -- Sí --> J[Planner-Executor-Reviewer]
  I -- No --> K[Orchestrator-Worker]
  G --> L{Activación por eventos?}
  L -- Sí --> M[Event-Driven], caption=default2026-05-11T21:06:20.266Zmermaid)] -->

## 8.4 Stack de referencia

Alinear con la arquitectura de implementación:

- Runtime en contenedores sobre AKS.
- API Adapter con FastAPI.
- Event Listener para consumo asincrónico.
- Planeador / Orquestador con LangGraph / LangChain.
- Prompt Builder separado.
- LLM Client vía LLM Gateway.
- Tool Router separado del cliente MCP.
- MCP Privado para herramientas del dominio.
- Role Policy and GuardRails.
- Session & Context Manager.
- Memory Manager sobre Cosmos DB.
- Resiliencia con timeouts, retries y backoff.
- Telemetría con OpenTelemetry.
- Auditoría end-to-end.

La LBA debe ser usada como control de selección tecnológica: tecnologías verdes se pueden usar, amarillas requieren restricción y tecnologías rojas no deben incorporarse en nuevas soluciones.

---

# 9. Decisiones de Arquitectura para la implementación de agentes

## ADR-001: Patrón multiagente seleccionado para primera implementación

## Estado

Propuesto.

## Contexto

SURA ya cuenta con una arquitectura de referencia centrada inicialmente en agente singular, con capacidades de orquestación, memoria, herramientas, seguridad, observabilidad e integración. Esta decisión reduce complejidad operativa y permite consolidar prácticas antes de evolucionar hacia multiagente.

Sin embargo, los retos de negocio identificados —gestión de conocimiento distribuido, soporte experto, atención multicanal, IT for IT y procesos de suscripción/reclamación— anticipan escenarios donde se requerirá especialización por dominio, revisión independiente y coordinación de tareas.

## Decisión

Se selecciona como primer patrón multiagente soportado el patrón **Orchestrator–Worker**, implementado inicialmente como **multiagente lógico dentro de un Agent Runtime centralizado**.

Esto significa:

- Un orchestrator central mantiene el control.
- Los workers se implementan como nodos especializados, tools, chains o capacidades MCP.
- No se habilita inicialmente coordinación libre entre agentes.
- No se habilita inicialmente agent-to-agent autónomo sin orquestador.
- El handoff siempre pasa por reglas explícitas.
- La observabilidad se centraliza en el orchestrator.
- La revisión/safety se incorpora como etapa obligatoria según riesgo.

## Alternativas consideradas

### Agentes colaborativos libres

Descartado para primera versión porque incrementa complejidad de monitoreo, riesgo de loops, pérdida de contexto, duplicidad de acciones y dificultad de auditoría.

### Multiagente distribuido desde el inicio

Descartado para primera versión porque exige mayor madurez en identidad de agentes, contratos de handoff, observabilidad distribuida, gobierno de costos y operación.

### Mantener únicamente agente singular

No se descarta, pero se considera insuficiente como ruta de evolución para casos complejos que requieren especialización.

## Consecuencias

Positivas:

- Facilita trazabilidad.
- Reduce complejidad inicial.
- Permite reutilizar la arquitectura actual.
- Permite evolucionar gradualmente.
- Facilita gobierno de herramientas y permisos.
- Reduce riesgo de comportamiento emergente no controlado.

Negativas:

- Menor autonomía entre especialistas.
- El orchestrator puede convertirse en cuello de botella.
- Puede requerir refactor posterior si los especialistas crecen demasiado.
- La concurrencia inicial puede ser limitada.

## Criterios de aplicación

Usar Orchestrator–Worker cuando:

- Hay más de un dominio especializado.
- Hay varias herramientas o APIs.
- Se requiere consolidación de resultados.
- Se requiere trazabilidad central.
- Se requiere handoff controlado.
- El caso no justifica aún agentes distribuidos independientes.

No usar multiagente cuando:

- El flujo es lineal.
- Hay una sola tarea.
- No hay especialización real.
- La solución solo responde preguntas.
- La trazabilidad se puede resolver con agente singular.

---

## ADR-002: Estrategia de supervisión y revisión para patrones multiagente

## Estado

Propuesto.

## Contexto

Los sistemas de agentes en SURA deben operar bajo criterios de seguridad, cumplimiento, trazabilidad, evaluación continua y control humano cuando aplique. La arquitectura de referencia prioriza trazabilidad, cumplimiento, seguridad, mantenibilidad, eficiencia y adaptabilidad. Además, la matriz de riesgos se define como gate formal para evaluar, mitigar y monitorear iniciativas de IA.

Los patrones multiagente incrementan el riesgo porque introducen delegación, handoff, uso de múltiples herramientas, posible pérdida de contexto y decisiones distribuidas.

## Decisión

Se adopta una estrategia de supervisión basada en tres niveles:

### Nivel 1: Revisión automática determinística

Aplica para todos los agentes.

Incluye:

- Validación de esquema de entrada y salida.
- Validación de permisos.
- Validación de herramientas permitidas.
- Validación de límites de costo, tokens, tiempo y reintentos.
- Validación de fuentes autorizadas.
- Validación de políticas de datos.
- Registro de decisiones y acciones.

### Nivel 2: Reviewer/Safety agent o nodo de revisión

Aplica para flujos de riesgo medio, respuestas complejas o uso de múltiples herramientas.

Incluye:

- Evaluación de consistencia.
- Revisión de groundedness frente a fuentes.
- Revisión de seguridad.
- Revisión de formato.
- Revisión de completitud.
- Evaluación automática con criterios definidos.
- Reintento o corrección controlada.

### Nivel 3: Human Supervisor

Aplica para acciones de alto impacto o riesgo alto.

Incluye:

- Aprobación antes de ejecutar acciones sensibles.
- Revisión de decisiones con impacto legal, financiero, reputacional, salud o datos personales.
- Resolución de ambigüedad.
- Aprobación de excepciones.
- Suspensión o retiro del agente.

## Reglas de escalamiento humano

Escalar a supervisor humano cuando:

- El riesgo residual no es aceptable.
- El agente propone una acción irreversible.
- Hay impacto económico relevante.
- Hay impacto legal, médico, reputacional o de cumplimiento.
- Hay baja confianza en el resultado.
- Hay conflicto entre fuentes.
- Hay intento de acceso no autorizado.
- Hay datos sensibles no necesarios para la tarea.
- El reviewer rechaza dos veces el resultado.
- El agente supera límites de iteración o costo.
- El usuario solicita revisión humana.

## Consecuencias

Positivas:

- Reduce riesgo operacional.
- Aumenta confianza y auditabilidad.
- Permite adopción gradual de autonomía.
- Alinea multiagente con gobierno corporativo.
- Facilita explicar decisiones ante auditoría.

Negativas:

- Puede aumentar latencia.
- Puede aumentar costo.
- Requiere diseño de interfaces para supervisores.
- Requiere definir owners y responsables.
- Puede generar fricción si se exige revisión humana en exceso.

## Decisión adicional

La supervisión humana no debe ser genérica. Cada agente debe declarar en su Agent Manifest:

- Qué acciones puede ejecutar sin aprobación.
- Qué acciones requieren aprobación.
- Qué acciones están prohibidas.
- Qué rol humano aprueba.
- Qué evidencia debe presentarse al supervisor.
- Qué ocurre si no hay respuesta humana.
- Cuánto tiempo espera antes de expirar.

---

# 10. Patrones incluidos como referencia

Los capítulos anteriores definieron una ruta de adopción progresiva para definición de agentes: primero decidir si realmente se necesita un agente, luego elegir entre agente singular, agente con roles o multiagente, y finalmente definir controles de seguridad, memoria, herramientas, observabilidad, prompts y evaluación.

La decisión arquitectónica más importante es evitar que multiagente sea el punto de partida por moda. La arquitectura debe crecer por necesidad: cuando la complejidad, la especialización, el riesgo o la asincronía lo justifiquen.

Estas plantillas convierten esa definición en referencias ejecutables. Cada patrón muestra una forma mínima de implementar el concepto sin depender de infraestructura real. Por eso usan mocks para LLM, MCP, memoria y eventos. El objetivo es que los equipos entiendan el flujo, los contratos y los criterios de aceptación antes de conectar capacidades productivas.

> **[Archivo adjunto]** [agent-blueprint-cli-archetype-v2.zip](../../../../../recursos/5838045207/agent-blueprint-cli-archetype-v2.zip)

## 10.1 Agente Singular

Es el patrón base. Un único orquestador recibe la solicitud, valida políticas, consulta memoria, usa herramientas autorizadas y genera la respuesta.

Debe usarse cuando el caso es acotado, tiene pocas herramientas, requiere trazabilidad alta y no necesita handoff.

<!-- [macro: mermaid (size=large, isEditable=true, diagramCode=sequenceDiagram
  participant U as Usuario/Canal
  participant O as Orquestador Singular
  participant P as Policy/GuardRails
  participant M as Memoria
  participant T as MCP/Tool
  participant L as LLM Gateway

  U->>O: AgentRequest
  O->>P: validar entrada y permisos
  O->>M: leer/escribir contexto
  O->>T: knowledge_search
  O->>L: completar respuesta con prompt versionado
  O-->>U: AgentResponse + trace, caption=default2026-05-11T06:17:21.127Zmermaid)] -->

### Paquete de referencia:

> **[Archivo adjunto]** [01_singular_agent_v2.zip](../../../../../recursos/5838045207/01_singular_agent_v2.zip)

> **[Archivo adjunto]** [01_singular_agent.zip](../../../../../recursos/5838045207/01_singular_agent.zip)

---

## 10.2 Orchestrator-Worker

Es el primer patrón recomendado para multiagente controlado. El orquestador conserva el control y delega tareas a workers especializados.

Debe usarse cuando hay varios dominios, varias herramientas, necesidad de handoff controlado o crecimiento modular.

<!-- [macro: mermaid (size=large, isEditable=true, diagramCode=flowchart LR
  U[Usuario / Sistema] --> O[Orchestrator]
  O --> R[Router]
  R --> W1[Worker Conocimiento]
  R --> W2[Worker Casos]
  W1 --> O
  W2 --> O
  O --> RV[Reviewer opcional]
  RV --> RESP[Respuesta], caption=default2026-05-11T06:22:34.922Zmermaid)] -->

### Paquete de referencia:

> **[Archivo adjunto]** [02_orchestrator_worker_v2.zip](../../../../../recursos/5838045207/02_orchestrator_worker_v2.zip)

> **[Archivo adjunto]** [02_orchestrator_worker.zip](../../../../../recursos/5838045207/02_orchestrator_worker.zip)

---

## 10.3 Planner-Executor-Reviewer

Este patrón separa la responsabilidad de planear, ejecutar y revisar. Es el más útil cuando hay riesgo, necesidad de evidencia o posibilidad de acciones sensibles.

Debe usarse cuando una respuesta o acción requiere validación independiente antes de entregarse o ejecutarse.

<!-- [macro: mermaid (size=large, isEditable=true, diagramCode=flowchart TD
  REQ[Solicitud] --> P[Planner]
  P --> PLAN[Plan estructurado]
  PLAN --> E[Executor]
  E --> EV[Evidencia]
  EV --> R[Reviewer]
  R -->|Aprobado| OK[Responder]
  R -->|Riesgo alto| H[Human Supervisor]
  R -->|Rechazado| STOP[Detener / corregir], caption=default2026-05-11T06:25:56.400Zmermaid)] -->

### Paquete de referencia:

> **[Archivo adjunto]** [03_planner_executor_reviewer_v2.zip](../../../../../recursos/5838045207/03_planner_executor_reviewer_v2.zip)

> **[Archivo adjunto]** [03_planner_executor_reviewer.zip](../../../../../recursos/5838045207/03_planner_executor_reviewer.zip)

---

## 10.4 Event-Driven Agent

Este patrón permite que el agente sea activado por eventos, no solo por solicitudes de usuario. Es clave para flujos asincrónicos, radicaciones, recepción de documentos, cambios de estado o integración con procesos core.

<!-- [macro: mermaid (size=large, isEditable=true, diagramCode=sequenceDiagram
  participant Producer as Sistema productor
  participant Broker as Broker
  participant Agent as Event Listener + Agent
  participant Tool as MCP/Tool
  participant Consumer as Consumidor

  Producer->>Broker: EventEnvelope
  Agent->>Broker: consume
  Agent->>Tool: consulta o acción autorizada
  Agent->>Broker: agent.result.created
  Broker->>Consumer: resultado, caption=default2026-05-11T06:27:19.300Zmermaid)] -->

### Paquete de referencia:

> **[Archivo adjunto]** [04_event_driven_v2.zip](../../../../../recursos/5838045207/04_event_driven_v2.zip)

> **[Archivo adjunto]** [04_event_driven.zip](../../../../../recursos/5838045207/04_event_driven.zip)
