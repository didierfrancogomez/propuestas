# Contexto de la solución — Arquitectura de Gestores SURA

> Documento interno de trabajo (no se entrega al cliente). Es la **fuente de verdad** de las
> decisiones de negocio y de diseño que se dibujan en el diagrama. Si el diagrama y este
> documento no coinciden, se resuelve aquí primero y luego se ajusta el diagrama.
> Cómo iterar sobre él: ver `AGENTS.md` en esta misma carpeta.

- **Diagrama vigente:** `Arquitectura_Gestores_SURA_v6_3.drawio` (copia de la v6_2, que queda como histórico).
- **Insumo de referencia (solo lectura):** `resources/Arquitectura-Gestores consolidado.drawio`.
- **Lineamientos del cliente:** `SURA/lineamientos-sura/` (ver §8).
- **Precedencia (vigente):** por ahora **prevalecen las reglas de las dos páginas de detalle**,
  *Detalle: Gestor Solicitud* y *Detalle: Gestor Evaluación (Release 1)*. Si otra página
  (Vista general, Release final, Juez, Duplicados, etc.) las contradice, mandan las de detalle,
  y la otra página se marca como pendiente de alinear.
- **Alcance del diagrama (vigente):** el diagrama muestra la **arquitectura completa** que soporta la solución. El cronograma (sprints y Qs) solo **organiza la implementación** por etapas. Que un componente no tenga HU en un sprint no lo saca del diagrama. Se usa el cronograma para detectar lo que **falta** en la arquitectura, nunca para recortarla.
- **Última actualización:** 2026-11-12 · línea base levantada de las páginas *Detalle: Gestor Solicitud* y *Detalle: Gestor Evaluación (Release 1)* de la v6_3.

---

## 1. Páginas del diagrama v6_3

| # | Página | Estado en este contexto |
|---|---|---|
| 1 | Vista general | **Rehecha 2026-11-12** con 7 capas y los componentes de los detalles (§9.6) |
| 2 | **Detalle: Gestor Solicitud** | Levantada (§3) |
| 3 | canales con core | Alineada con *Detalle: Gestor Solicitud* (2026-11-12) |
| 4 | Page-11 | Borrador sin nombre, pendiente |
| 5 | **Detalle: Gestor Evaluación (Release 1)** | Levantada (§4) |
| 6 | Gestor Evaluación Release final | Pendiente |
| 7 | Juez del microservicio | Pendiente |
| 8 | Dónde vive la IA y cómo escala | Pendiente |
| 9 | Duplicados por servicio | Pendiente |
| 10 | Glosario: qué es cada cosa | Referencia de capas C1–C7 (§2.2) |
| 11 | estructuras de mensajes de trazabilidad | Pendiente |

---

## 2. Actores, dominios y vocabulario

### 2.1 Dominios (contenedores del diagrama)

| Dominio | Qué es | Responsabilidad en la solución |
|---|---|---|
| **Canales** | SVP, AVA, Portal prestador | Por donde entra la solicitud. Son el front del usuario final: **consultan el estado** en Siniestro integral (vía Apigee) y **le notifican** al usuario. No tienen IA. |
| **Apigee** | API Gateway corporativo | Única puerta entre dominios (canales → core, core → orquestador, gestores → orquestador). |
| **Siniestro integral** | Proceso de negocio del core que recibe la solicitud | Crea el siniestro padre, encola el comando al gestor y consume el resultado. **Administra los estados del proceso general** y los actualiza con el detalle de la respuesta de cada gestor. Es dueño del **Gestor documental de autorizaciones**. |
| **Gestor documental de autorizaciones** | Componente de Siniestro integral (Blob, acceso por `apiG`) | Repositorio de los documentos de la solicitud: los canales y el siniestro integral **publican**; el Gestor Solicitud **consulta en línea (síncrono)**, sin copiar a un almacenamiento propio. |
| **Orquestador de integración** | Capa de mensajería entre el core y los gestores | Recibe **mensajes HTTP** (vía Apigee), **responde de inmediato que los recibió (ACK)** y los **encola** (topic → cola). Aplica **seguridad** y **trazabilidad** a cada mensaje. Decide si el mensaje va a la cola del gestor o a una persona, y devuelve los resultados al core por topics. |
| **Gestor Solicitud** | Microservicio agéntico (AKS · LangGraph) | Recibe documentos, los clasifica, extrae datos con IA, los valida con un juez y devuelve un resultado. |
| **Gestor Evaluación** | Microservicio agéntico (AKS · LangGraph) | Arma el contexto del caso, evalúa pertinencia médica, valida con un juez y recomienda aprobar o rechazar. |
| **Plataforma agéntica – Runtime agéntico** | AKS + orquestador/agente | Dónde corre el agente de cada gestor. |
| **Plataforma agéntica – Control plane** | LLM Gateway (Azure OpenAI o Gemini, por decidir) | Único acceso a modelos. |
| **Core ADR** | Core de autorizaciones | Ejecuta reglas duras, decide la autorización final, escala a bandeja Konecta. |
| **Core Salud Voluntarios** | Inicialmente GlobalWeb | Crea el radicado de la solicitud. |
| **Konecta** | Operación humana externa | Bandeja de revisión humana. |
| **Torre de control** | Componente **transversal** con **Kafka interno** | **Todos** los componentes (canales, Siniestro integral, orquestador de integración, gestores, Core ADR y Core Salud) le envían la **trazabilidad** de lo que pasa en su proceso al gestionar la solicitud. Arma el flujo end to end y alimenta el tablero y el copiloto, que pueden pedir acciones al core. |

### 2.2 Capas de la arquitectura de referencia (etiqueta `Cx` en los íconos)

Tomadas de la página *Glosario: qué es cada cosa*: **C1** consumidores y superficies · **C2** identidad, acceso y contexto · **C3** gateways (LLM Gateway, MCP Gateway) · **C4** runtime / procesamiento / modelos / workflow · **C5** colas y servicios de datos · **C6** almacenamiento · **C7** evaluación (juez, evals).

### 2.3 Vocabulario obligatorio

Se usa la terminología de `propuestas/CLAUDE.md`: **core** (o SuraHis), **LLM Gateway**, **runtime agéntico**, **LLM-as-a-judge** (en el diagrama: "Juez del microservicio"), **human-in-the-loop (HITL)**, **siniestro padre**, **bandeja**, **radicado**. Un *comando* encola trabajo (cola); un *evento* informa un hecho (Kafka). Ver §8.

---

## 3. Gestor Solicitud — reglas de negocio

**Propósito:** convertir los documentos de una solicitud (orden, historia clínica, factura) en datos estructurados con confianza y evidencia, para que el core radique la solicitud o la pase a una persona.

### 3.1 Flujo de punta a punta

1. **Entrada por canales.** La solicitud llega desde SVP, AVA o Portal prestador → Apigee → *Siniestro integral*.
2. **Siniestro integral** (según la pestaña *canales con core*): `Orquestador` (retorna al canal el **id de trazabilidad = id del siniestro padre**) → `Crear siniestro padre` → **queue nueva solicitud** → `Validación inicial del documento` (seguridad, acceso al documento; punteada: contenido por detallar):
   - **Sí** → ✔ *Documento válido* → `Encolar comando para gestor` → Apigee, con el **id del siniestro padre**.
   - **No** → ⏳ *Documento no válido: flujo pendiente de definir* (P-06).
3. **Orquestador de integración:** `Recibir comando de encolamiento` → `decide enviar a queue o humano` → *Topic de gestor de solicitudes* → **cola del gestor**.
   - En paralelo, los **canales** y el **siniestro integral** publican los documentos en el **Gestor documental de autorizaciones** (componente de Siniestro integral) a través de `apiG`.
4. **Gestor Solicitud — A. Recepción:** el orquestador del runtime lee la configuración (qué documentos esperar según el tipo de solicitud), y **consulta los documentos de forma síncrona en el gestor documental de Siniestro integral** (vía `apiG`). El gestor no tiene almacenamiento de archivos propio.
5. **Gestor Solicitud — B. Extracción con IA + juez:** cola interna `q.extraccion` → Document Intelligence (texto + % confianza) → **Clasificador de páginas** (Orden · HC · Factura · Vacío) → extractores especializados (**HC**, **Órdenes**: CUPS, cantidad…, **Facturas**) → **Homologador de códigos** (agente; consulta la tabla de homologación vigente en sistemas SURA vía **MCP Gateway**) → **Validador de salida** (código, sin IA) → **Juez del microservicio** → decisión.
6. **Salidas del gestor** (siempre hacia el core, vía Apigee → orquestador):
   - ✔ **Solicitud lista** (③): datos extraídos + confianza + evidencia + nota del juez.
   - ⚠ **Requiere revisión** (③b): faltan datos o el juez no aprobó; dice qué revisar.
   - ⚠ **Archivo no procesable**: dañado o protegido con clave; responde **requiere revisión humana: fallo en la validación de archivos de entrada** y sale por el mismo Apigee de salida que ③b.
7. **Orquestador → core:** `Documento procesado satisfactoriamente` / `Documento no procesado satisfactoriamente` → *Topic de gestor de solicitudes* → **Cola del resultado de procesamiento** (en Siniestro integral).
8. **Siniestro integral consume el resultado**, **marca el estado** de la solicitud con el detalle de la respuesta del gestor (*Actualiza el estado de la solicitud*), y los **canales consultan ese estado** (vía Apigee) para notificar al usuario final. Además:
   - Si el gestor lo encontró válido → `complementa y valida` → **Crear radicado** (Core Salud Voluntarios).
   - Si no se procesó → **Escalar a HITL** → crea radicado y **escala a bandeja Konecta** (Core ADR → Konecta).

### 3.2 Reglas

| ID | Regla |
|---|---|
| RN-SOL-01 | El core activa el gestor; el gestor **nunca** habla con otros gestores. |
| RN-SOL-23 | Después de extraer, el gestor **homologa los códigos** (CUPS, CIE-10, códigos propios del prestador) a los **códigos oficiales SURA**, usando la **tabla de homologación vigente** que consulta como tool vía **MCP Gateway**. Por cada código registra la versión de la tabla, la regla aplicada y la evidencia. Si no hay equivalencia, marca el dato **pendiente de revisión** y no asigna una homologación incorrecta. Si hay varias equivalencias, aplica las reglas de priorización y el diagnóstico asociado (HU-03-013). |
| RN-SOL-24 | La salida del gestor lleva **el detalle de la respuesta**. Cuando hay un fallo de archivo, informa la **causa concreta**: ilegible, corrupto, formato no permitido, vacío, con contraseña, error de OCR o tipo no identificado (HU-03-009). El gestor **no** habla con el canal ni con el usuario. |
| RN-SOL-21 | **Entrada:** el gestor se activa **siempre** con un **mensaje en su cola RabbitMQ**, que envía el **orquestador de integración** (topic de gestor de solicitudes → cola del gestor). No hay API de entrada. |
| RN-SOL-22 | **Salida:** el gestor responde con **mensajes JSON por HTTP** al **orquestador de integración** (vía Apigee). El orquestador los encola en un **topic**, y el topic los entrega a la **cola que lee Siniestro integral**. Aplica a ③, ③b y ⚠. |
| RN-SOL-02 | El gestor sale **siempre** con uno de tres resultados: lista (③), requiere revisión (③b) o archivo no procesable (⚠). |
| RN-SOL-03 | Un archivo se marca **no procesable** si falla **2 veces** (dañado o con clave). |
| RN-SOL-04 | Los documentos esperados dependen de la **configuración por tipo de solicitud**; no están cableados en el código. |
| ~~RN-SOL-05~~ | *Eliminada 2026-11-12:* el gestor ya no tiene Blob de entrada temporal (ver RN-SOL-18). |
| RN-SOL-06 | Cada página se clasifica (Orden, HC, Factura, Vacío) y se extrae con el **extractor de su tipo**. |
| RN-SOL-07 | Antes del juez, un **validador con código** revisa campos, CUPS, paciente y el cruce con el OCR. |
| RN-SOL-08 | Si falta algo **o** el juez no aprueba → *requiere revisión*; si no → *solicitud lista*. |
| RN-SOL-09 | Con resultado válido, el core complementa, valida y **crea el radicado**. |
| RN-SOL-10 | Con resultado no procesado, se escala a HITL: se crea el radicado y se envía a **bandeja Konecta**. |
| RN-SOL-11 | El gestor registra su **auditoría propia** en Cosmos DB (qué hizo cada paso, qué decidió el juez y con qué evidencia); solo registra. |
| RN-SOL-12 | Envía su trazabilidad al Kafka interno de la Torre de control (RN-TRV-15): `solicitud.recibida`, `documentos.validados`, `documentos.leídos`, `resultado.enviado`. |
| RN-SOL-13 | El **siniestro padre se crea primero**, siempre; la validación inicial ocurre **después**, de forma asíncrona tras la `queue nueva solicitud`. Toda solicitud deja traza aunque luego se rechace. |
| RN-SOL-14 | El orquestador del siniestro integral **retorna al canal el id de trazabilidad** (id del siniestro padre) al recibir la solicitud. |
| RN-SOL-15 | La validación inicial revisa el **documento**: seguridad y acceso al documento. |
| RN-SOL-16 | El comando al gestor lleva el **id del siniestro padre** y los datos de cada solicitud; se encola **un comando por solicitud** (una a una). |
| RN-SOL-17 | Los documentos viven en el **Gestor documental de autorizaciones**, que es de **Siniestro integral**. Canales y siniestro integral publican ahí; el comando lleva **referencias** a los documentos, no los archivos. |
| RN-SOL-18 | El Gestor Solicitud **consulta los documentos directamente en Siniestro integral, de forma síncrona** (gestor documental vía `apiG`). **No los copia** ni tiene almacenamiento de archivos propio; no es dueño del repositorio documental. |
| RN-SOL-20 | Un **archivo no procesable** (dañado o con clave, tras 2 intentos) se responde al core como **requiere revisión humana**, con motivo **fallo en la validación de archivos de entrada**, por el **Apigee de salida** (mismo camino que ③b: orquestador de integración → "Documento no procesado satisfactoriamente" → Siniestro integral → HITL). |
| RN-SOL-19 | La validación inicial tiene dos salidas: **válido** → se encola el comando al gestor; **no válido** → flujo **pendiente de definir** (P-06). Solo el documento válido llega al gestor. |

### 3.3 Contrato de entrada / salida

| Entrada / salida | Por dónde | Qué viaja |
|---|---|---|
| ① Entrada | Mensaje en la cola RabbitMQ del gestor (orquestador de integración → topic de gestor de solicitudes → cola del gestor) | id del siniestro padre (trazabilidad), id solicitud, referencias a los documentos en el gestor documental (orden + HC), tipo de solicitud, consumidor · un mensaje por solicitud |
| ② Paso interno | cola interna `q.extraccion` | id solicitud, páginas válidas (leídas en línea del gestor documental de Siniestro integral) |
| ③ Solicitud lista | JSON por HTTP al orquestador de integración (vía Apigee) → topic → cola que lee Siniestro integral | datos extraídos, confianza por campo, evidencia, nota del juez |
| ③b Requiere revisión | igual que ③ | qué falta o qué no aprobó el juez; el core asigna a una persona |
| ⚠ No procesable | igual que ③ | respuesta **requiere revisión humana** · motivo: fallo en la validación de archivos de entrada · **causa detallada**: ilegible, corrupto, formato no permitido, vacío, con contraseña, error de OCR o tipo no identificado |

### 3.3b Información que necesita el gestor según el cronograma (insumo del cliente)

Fuente: `resources/Cronograma implementación.xlsx`, pestañas *Backlog General* (épica EP-03 Gestor de Solicitud, más las HU de Siniestro Integral que lo alimentan) y *Sprint 3Q4*. Es de solo lectura; aquí solo se resume.

| Qué necesita | De dónde viene | HU / fila |
|---|---|---|
| **id del siniestro padre** (llave para todo) | Mensaje de entrada | Backlog fila 57 |
| **Referencia a los documentos** (o la ruta derivable del siniestro padre) | Mensaje de entrada / Siniestro integral | filas 43, 44 |
| **Datos mínimos de la presolicitud y radicado temporal** | Siniestro integral | Sprint 3Q4 #2; filas 40, 53 |
| **Documentos** (PDF, JPG, JPEG, PNG; un PDF con varios tipos o un archivo por documento, a veces ya marcado con su tipo por el prestador) | Repositorio documental administrado por Siniestro integral | filas 50, 57; HU-03-003, HU-03-004 |
| **Catálogo de tipos documentales** y su asociación con agentes y esquemas (configurable, sin cambiar código) | Configuración propia (Analítica) | fila 60 |
| **Esquema de campos por tipo documental**: orden médica (CUPS, CIE-10, médico, IPS…), HC (edad, sexo, antecedentes…), diagnósticos, procedimientos y medicamentos | Configuración propia (Analítica + negocio) | fila 61; HU-03-012; Sprint 3Q4 #3, #4 |
| **Tabla de homologación vigente**, catálogo maestro de procedimientos SURA y reglas de priorización | Sistemas SURA (candidato natural a tool del **MCP Gateway**) | HU-03-013 |
| **Umbral de confianza** que separa "lista" de "requiere revisión" | Negocio | Sprint 3Q4 #5 |
| **Set de validación** de órdenes médicas e HC (golden set) | Negocio + Analítica | Sprint 3Q4, fila 16 |
| **Catálogo de causas de error** (ilegible, corrupto, formato no permitido, vacío, con clave, error de OCR, tipo no identificado) | Negocio | HU-03-009 |
| **Reintentos, cola de mensajes fallidos y tiempo máximo de respuesta** | Operación / Siniestro integral | filas 45, 65 |

**Qué devuelve (fila 62):** datos extraídos, clasificación, campos incompletos y explicación. Por cada dato: documento origen, confianza y, para los códigos, el código SURA homologado y su trazabilidad (HU-03-012, HU-03-013). Lo entrega a Siniestro integral (filas 63, 69), y el Gestor Evaluación lo lee desde ahí (fila 79).

**Diferencias con el diagrama, para discutir (no se cambia nada todavía):**
- ~~D-01~~: la homologación de códigos (HU-03-013) no estaba dibujada. **Resuelta 2026-11-12** (RN-SOL-23).
- ~~D-02~~: el diagrama tiene **Extractor Facturas**, pero ninguna HU del MVP habla de facturas. **Resuelta 2026-11-12:** se mantiene, porque el diagrama es la arquitectura completa. Su implementación la ubica el cronograma. Para conversar en sesión, no para el entregable: hoy el backlog no tiene la HU de facturas.
- ~~D-03~~: HU-03-009 pide informar al prestador la causa del error y permitir reemplazar el archivo. **Resuelta 2026-11-12:** el gestor manda la causa en su respuesta (RN-SOL-24), Siniestro integral marca el estado (RN-TRV-11) y el canal lo consulta y notifica al prestador (RN-TRV-12). RN-SOL-20 sigue vigente.
- D-04: el prestador puede **marcar el tipo documental** al cargar (HU-03-004 CA02); el clasificador podría usarlo como dato de entrada. **Fuera del alcance de este diagrama (decisión 2026-11-12):** no se resuelve aquí. El diagrama no cambia.

### 3.4 El juez del microservicio (diseño de costo)

1. Chequeos con código primero (gratis): campos, formatos, cruce OCR vs extracción, coherencia orden ↔ HC.
2. Modelo pequeño (GPT-5 nano o equivalente) solo con el resultado + fragmentos de evidencia, nunca el documento completo; la rúbrica fija se cachea.
3. Escala a un modelo mayor solo si duda (≈ 5–10 % de los casos).
4. Rúbrica propia por microservicio y por escenario (tipo de solicitud), versionada y configurable. Costo estimado ≈ US$ 0,0001 por solicitud.

---

## 4. Gestor Evaluación (Release 1) — reglas de negocio

**Propósito:** recomendar si una solicitud es pertinente (aprobar / rechazar) y si necesita una persona, con evidencia. **Recomienda; las reglas duras y la aprobación final están en el core.**

### 4.1 Flujo de punta a punta

1. **Core ADR:** `nueva solicitud` → `Ejecuta rules` → `¿autoriza?`
   - **Sí** → fin (no se invoca el gestor).
   - **No autoriza** → Apigee → orquestador.
2. **Orquestador de integración:** `Recibir comando de encolamiento` → `decide enviar a queue o humano`:
   - a la cola → *Topic de gestor de evaluación* → **cola `q.evaluacion`** del gestor;
   - en contingencia → **topic de contingencia** (en Core ADR).
3. **Gestor Evaluación:** el agente (runtime agéntico) arma **1. Contexto del caso** con **una sola consulta al core** (vía Apigee):
   - a. *¿Qué pedir?* — el catálogo local dice, según el servicio (CUPS), qué historial, en qué ventana y qué cláusulas.
   - b. *Una sola llamada al core* — paciente + CUPS + lista de datos que necesita.
   - c. *El core responde* — historial relevante + datos del afiliado + plan y cláusulas que aplican.
   - d. *Expediente del caso* — Cosmos DB, vida corta; lo reutilizan los pasos siguientes sin volver a llamar.
   - El contexto agrupa: **Cobertura**, **Coherencia** e **información de pertinencia** (protocolos, políticas y cláusulas filtrados por el plan del afiliado).
4. **3. Pertinencia médica** (agente): usa el expediente + protocolos; solo vuelve al core si le falta algo puntual.
5. **Juez:** ¿la evidencia sostiene la recomendación? → `¿concepto aprobado?`
   - **Sí** → *Aprobado* → `¿requiere HITL?` → respuesta aprobado.
   - **No** → *Rechazado* → `¿requiere HITL?` → respuesta rechazado.
6. **Notifico la respuesta** → publica respuesta → Apigee → orquestador: `Resultado de evaluar del concepto` → *Topic de gestor de evaluación* → colas en Core ADR: **response aprobado** / **response rechazado** → `¿requiere HITL?` en el core *(por definir con el equipo del core, P-02)*.

### 4.2 Reglas

| ID | Regla |
|---|---|
| RN-EVA-01 | El gestor solo se invoca cuando las **reglas del core no autorizan** automáticamente. |
| RN-EVA-02 | El gestor **recomienda**; la aprobación final y las reglas duras viven en el core. |
| RN-EVA-03 | El contexto se arma con **una sola consulta al core**; el agente solo vuelve a llamar si falta algo puntual. |
| RN-EVA-04 | Qué datos pedir lo define el **catálogo local por servicio (CUPS)**: historial, ventana de tiempo y cláusulas. |
| RN-EVA-05 | El expediente del caso vive en Cosmos DB con **vida corta** y se reutiliza dentro de la evaluación. |
| RN-EVA-06 | El contexto cubre tres dimensiones: **cobertura**, **coherencia** y **pertinencia**. |
| RN-EVA-07 | Toda recomendación pasa por el **juez** antes de salir. |
| RN-EVA-08 | Toda respuesta (aprobada o rechazada) indica si **requiere HITL** y a qué nivel. |
| RN-EVA-09 | Si el orquestador no puede encolar, el comando va al **topic de contingencia**. |
| RN-EVA-10 | Auditoría propia en Cosmos DB: expediente usado, regla aplicada, evidencia, nota del juez, nivel recomendado. |
| RN-EVA-11 | Envía su trazabilidad al Kafka interno de la Torre de control (RN-TRV-15): `evaluación.iniciada`, `duplicada`, `recomendación.enviada`, `escalada.N3/N4`, `decisión.humana` (ver I-03). |
| RN-EVA-12 | El nivel de revisión humana es una **recomendación**: el core puede reasignarlo. |

### 4.3 Contrato de la respuesta

```text
respuesta: aprobado | rechazado
requireHumanInTheLoop: true | false
reason: <motivo estructurado: documental o clínico>
level: N1 (auxiliar) | N2 (médico) | N3 (especialista)
pertinencia: <criticidad>
```

### 4.4 Decisiones de diseño declaradas en la página

1. **Contexto una sola vez:** el paso 1 trae lo que necesitan los pasos siguientes.
2. **Duplicados con código:** las reglas por servicio viven en el catálogo local; aplicarlas no necesita IA.
3. **Nivel de revisión:** el agente deja un motivo estructurado; un clasificador decide el nivel con reglas configurables y solo usa un modelo pequeño si el motivo es ambiguo.

---

## 5. Reglas transversales (aplican a todos los gestores)

| ID | Regla |
|---|---|
| RN-TRV-01 | Entre dominios solo se pasa por **Apigee**. |
| RN-TRV-02 | El core se comunica con los gestores por **comandos encolados** a través del orquestador de integración (message-driven); los gestores informan **hechos** por Kafka (event-driven). |
| RN-TRV-03 | El **LLM Gateway es obligatorio**: ningún componente usa un LLM sin pasar por él. El modelo está por decidir (Azure OpenAI o Gemini). |
| RN-TRV-13 | **Entrada de todo gestor:** siempre un **mensaje en su cola RabbitMQ**, enviado por el **orquestador de integración** (topic del gestor → cola del gestor). Ningún gestor expone una API de entrada. (Generaliza RN-SOL-21.) |
| RN-TRV-14 | **Salida de todo gestor:** **JSON por HTTP** al **orquestador de integración** (vía Apigee). El orquestador lo encola en un topic, y el topic lo entrega a la cola de quien lo consume: **Siniestro integral** para el Gestor Solicitud, **Core ADR** para el Gestor Evaluación. (Generaliza RN-SOL-22.) Las **consultas** que un gestor hace durante su trabajo (documentos, contexto del core) son síncronas y no siguen este camino. |
| RN-TRV-11 | **Siniestro integral administra los estados del proceso general.** Cada respuesta de un gestor llega a Siniestro integral, que marca el estado con su detalle. Ningún gestor cambia estados por su cuenta. |
| RN-TRV-12 | Los **canales** son el front del usuario final: **consultan el estado** en Siniestro integral (vía Apigee) y **notifican** al usuario, por ejemplo la causa de un archivo rechazado para que lo reemplace. Los gestores nunca notifican directamente al usuario. |
| RN-TRV-10 | Los **MCP Gateway** se dibujan en cada gestor como el camino para que sus agentes consulten sistemas SURA como tools. |
| RN-TRV-04 | Cada gestor es un microservicio en **AKS + LangGraph** que **escala según su cola**. |
| RN-TRV-05 | Cada gestor tiene **juez propio**, **auditoría propia** (Cosmos DB) y envía su trazabilidad a la **Torre de control** (RN-TRV-15). |
| RN-TRV-06 | Cuando el resultado no es confiable, la decisión pasa a una persona (**HITL**); la IA no cierra casos dudosos. |
| RN-TRV-07 | El **orquestador de integración** es la única entrada de mensajes entre el core y los gestores: recibe **HTTP** y **encola**. Nadie escribe directo en las colas de otro dominio. |
| RN-TRV-08 | Los servicios del orquestador **responden de inmediato que recibieron el mensaje (ACK)** y lo procesan después en la cola. El emisor no espera el resultado del gestor en la misma llamada: el resultado llega después, como otro mensaje. |
| RN-TRV-09 | La **trazabilidad del orquestador** registra tres momentos de cada mensaje: **1. Recibido** (llegó por HTTP y se respondió el ACK de inmediato), **2. Procesado** (pasó la seguridad y quedó registrado) y **3. Encolado** (quedó en el topic, camino a la cola del destino). Esa trazabilidad va a la Torre de control. *(Por precisar: qué controles de seguridad agrega a los de Apigee y qué id usa para trazar; se presume el id del siniestro padre.)* |
| RN-TRV-16 | **Comandos siempre por RabbitMQ; trazabilidad siempre por Kafka.** Todo lo que le pide trabajo a otro componente viaja como mensaje en una cola RabbitMQ, a través del orquestador de integración. Todo lo que informa qué pasó va al Kafka interno de la Torre de control. No se mezclan. |
| RN-TRV-17 | **Plataforma:** los gestores y el runtime agéntico corren en **AKS** (no en Azure Container Apps), y escalan según su cola (KEDA). La base de datos es **Cosmos DB** (no MongoDB): auditoría propia de cada gestor, expediente del caso, catálogos, rúbricas y estado. |
| RN-TRV-15 | La **Torre de control** es transversal y tiene su propio **Kafka interno**. **Todos los componentes** le envían la trazabilidad de su proceso interno al gestionar la solicitud. Ningún componente depende de otro para reportar lo suyo. |

---

## 6. Preguntas abiertas con negocio

| ID | Pregunta | Dónde aparece | Estado |
|---|---|---|---|
| P-01 | ¿Validamos y rechazamos **antes** o **después** de crear el siniestro padre? | Gestor Solicitud, `Validación inicial` (punteada) | **Cerrada 2026-11-12:** después, como en *canales con core* (RN-SOL-13..16) |
| P-05 | ¿Se incorpora el **Gestor documental de autorizaciones** (publicar / consultar en Blob, vía Apigee) que aparece en *canales con core*, incluida la lectura del gestor desde ese repositorio? | canales con core | **Cerrada 2026-11-12:** sí; es componente de Siniestro integral (RN-SOL-17, 18) |
| P-07 | El *Core publica en Kafka* cuando cambia una regla de duplicidad (pestaña *Duplicados por servicio*). Ese mensaje no es un comando ni trazabilidad, así que RN-TRV-16 no dice por dónde va. ¿Va por RabbitMQ, se resuelve con la exportación diaria, o se admite Kafka para eventos de datos? | Duplicados por servicio | **Pospuesta** (decisión 2026-11-12: no se trabaja por ahora) |
| P-06 | ¿Qué pasa cuando la validación inicial del documento falla (seguridad o acceso)? Por definir: destino de la solicitud (rechazo, HITL/Konecta o reenvío del canal), estado del siniestro padre y aviso al canal. | Gestor Solicitud: caja ⏳ *Documento no válido* | Abierta, **dibujada como pendiente** |
| P-02 | ¿Cómo maneja el core el `requiere HITL` de las respuestas del gestor de evaluación? | Gestor Evaluación, Core ADR | Abierta: se define con el equipo del core |
| P-03 | ¿Qué hace el core con un archivo **no procesable**? En el diagrama no tiene conector de salida. | Gestor Solicitud | **Cerrada 2026-11-12:** responde *requiere revisión humana: fallo en la validación de archivos de entrada* por el Apigee de salida (RN-SOL-20) |
| P-04 | ¿Duplicados sigue siendo un paso del gestor de evaluación en Release 1? | Gestor Evaluación | Abierta (ver I-02) |

## 7. Inconsistencias detectadas en el diagrama (por resolver)

| ID | Inconsistencia | Página |
|---|---|---|
| I-01 | La tabla de entrada/salida dice "API POST /solicitudes → cola q.recepcion" y "API del Core (vía MCP Gateway)", pero el flujo dibujado entra y sale por **Apigee → orquestador → topics**. | **Gestor Solicitud: corregida 2026-11-12** (RN-SOL-21, 22) en *Detalle* y *canales con core*. **Gestor Evaluación: corregida 2026-11-12** (RN-TRV-13, 14) en *Detalle R1* y *Release final*, filas ④, ⑤ y ⑤b. Las filas ⑥ y ⑥b (paso a personas, decisión humana) quedan para I-03/P-02 |
| I-08 | La pestaña borrador *Page-11* tiene 3 cajas "API de solicitudes", que contradicen RN-SOL-21 (no hay API de entrada). | Page-11 · abierta, por confirmar si esa pestaña sigue vigente |
| I-10 | El **Glosario** aún describe el modelo anterior: "Core SURA (SuraHist) · dirige el proceso, decide qué gestor activar", "API Gateway · Azure API Management" (en los detalles es **Apigee**), y no menciona Siniestro integral, el orquestador de integración ni el gestor documental. | Glosario · **cerrada 2026-11-12** |
| I-11 | **Entrada del Gestor Evaluación:** el diagrama dice "id solicitud + datos extraídos" en el mensaje. El backlog dice que recibe el evento con el **id del siniestro padre** (fila 82) y que **lee** los datos extraídos que dejó el Gestor Solicitud **en Siniestro integral** (fila 79). | Evaluación · abierta |
| I-12 | **Orden de la evaluación:** el diagrama dice que el core aplica reglas duras primero y solo invoca al gestor si no autoriza (RN-EVA-01). El backlog dice que el gestor ejecuta **duplicidad → reglas duras → pertinencia** (fila 87) y combina reglas del core con reglas propias (fila 80). El paso de duplicados se borró del diagrama (I-02). | Evaluación · abierta |
| I-13 | **Quién cambia el estado:** el backlog dice que el gestor deja la autorización aprobada en estado "pendiente o lista para coordinación" en el core SuraHis (fila 89). Eso choca con RN-TRV-11 (Siniestro integral administra los estados) y con RN-EVA-02 (el gestor recomienda, el core decide). | Evaluación · abierta |
| I-14 | **Contrato de salida de Evaluación incompleto:** el diagrama tiene aprobado/rechazado + requireHumanInTheLoop + reason + level (N1/N2/N3, ver I-03). El backlog además pide etiqueta y clasificación del resultado (completo, parcial o nulo), criterios cumplidos, limitaciones y motivo de envío a bandeja (fila 75), y una respuesta explícita cuando falta información (fila 95). | Evaluación · abierta |
| I-15 | **Contratos sin esquema:** ningún gestor tiene definido su JSON de entrada y salida campo por campo. En Solicitud faltan el esquema de campos por tipo documental (fila 61, Analítica), el umbral de confianza "lista vs. requiere revisión" (Sprint 3Q4 #5) y los datos mínimos de la presolicitud (Sprint 3Q4 #2). | Ambos · abierta |
| I-09 | El **MCP Gateway** aparece en *Servicios compartidos* del Gestor Solicitud, pero ningún paso del gestor lo usa. | **Cerrada 2026-11-12:** se mantiene dibujado (RN-TRV-10) y ya tiene uso: el homologador de códigos lo consulta (RN-SOL-23) |
| I-02 | El paso **2. Duplicados** ya no está dibujado, pero se menciona en el título, en el expediente ("lo usan Duplicados (2)"), en la auditoría y en los eventos Kafka. | Evaluación |
| I-03 | Niveles de revisión: la respuesta usa **N1/N2/N3** (auxiliar, médico, especialista); notas, eventos y tabla usan **N3/N4**. | Evaluación |
| I-04 | El conector "Sí" sale de *Contexto del caso* a *Pertinencia* sin un rombo de decisión. | Evaluación |
| I-05 | La píldora `→ IA` de evaluación queda suelta junto al detalle del paso 1 y falta la píldora `→ MCP` anunciada en el título. | Evaluación |
| I-06 | La tabla de salida de evaluación menciona ⑤, ⑤b, ⑥ y ⑥b, que no están dibujados en el flujo. | Evaluación |
| I-07 | "Plataforma agéntica - Runtime agéntiico" tiene un error de digitación (se corrige al tocar la página). | Ambas |

---

## 8. Lineamientos del cliente aplicados

| Decisión | Lineamiento | Ruta |
|---|---|---|
| Comandos por cola (orquestador) y hechos por Kafka (torre de control): "*Streams hold truth. Queues do work.*" | EDA: event-driven vs message-driven | `lineamientos-sura/eda-framework/paginas/Marco-de-trabajo-para-arquitecturas-dirigidas-por-eventos-EDA-Framework.md` |
| Diferencia comando / consulta / evento; el emisor de un evento no conoce al consumidor | EDA: glosario (CQRS, conciencia del destinatario) | `lineamientos-sura/eda-framework/paginas/Marco-de-trabajo-para-arquitecturas-dirigidas-por-eventos-EDA-Framework/EDA-Framework-Glosario-y-definiciones-generales.md` |
| Elegir el estilo de integración por escenario | Modelo de decisión de integración | `lineamientos-sura/modelo-decision-integracion/paginas/Modelo-de-decision-y-casos-de-uso-de-integracion.md` y `.../Casos-de-uso-integracion-de-aplicaciones.md` |
| LLM Gateway, runtime agéntico, control plane, juez/evals | Arquitectura de referencia IA-First | `lineamientos-sura/ia-first-confluence/paginas/ARQ-AI-First-Arquitectura-de-referencia/Arquitectura-Agentes-V1.1/Arquitectura-de-Referencia-V1.1.md` y `.../Arquitectura-Plataforma-Agentica/Blueprint-de-Capacidades-Arquitectura-Agentica/` |

Si un cambio se aparta de un lineamiento, se anota aquí con el motivo.

---

## 9. Guía de estilo gráfico del diagrama

Estilo identificado en las páginas de detalle de la v6_3. Todo elemento nuevo debe copiar estos estilos.

> **⭐ Regla de oro del proyecto: un cambio, todas las pestañas.**
> Todo cambio de regla de negocio o de diagrama se aplica en **todas las pestañas** donde
> aparece ese elemento, flujo, texto o contrato, para que el diagrama completo cuente **la
> misma historia**. Un cambio no está terminado mientras exista una pestaña que diga otra
> cosa. Eso incluye los títulos y subtítulos, las tablas de entrada/salida, las notas de diseño,
> las bandas de eventos y el glosario. Si una pestaña no se puede alinear en ese momento,
> se registra como pendiente en §7 y en la bitácora, con la pestaña y el motivo. Nunca se
> deja en silencio.

### 9.1 Lienzo y tipografía

- Fondo blanco (`background=#ffffff`), sin cuadrícula visible, `page=0`.
- Fuente **Helvetica** en todo; texto `#1a1a1a`; texto secundario `#555555`.
- Jerarquía: título de página 20 · subtítulo 13 gris · título de contenedor 15 negrita · etiqueta de sección 13 negrita azul `#0277bd` · ícono 13 · descripción de ícono 11 · actividad 12 · capa `Cx` 10 azul `#0277bd` · píldora 10 negrita.

### 9.2 Elementos (estilos para copiar)

| Elemento | Uso | Estilo |
|---|---|---|
| **Contenedor de dominio** | Canales, core, orquestador, gestor, plataforma | `swimlane;startSize=34;html=1;rounded=1;arcSize=2;fillColor=#eef2f7;swimlaneFillColor=#f7fafc;strokeColor=#0288d1;strokeWidth=3;dashed=1;fontColor=#1a1a1a;fontStyle=1;fontSize=15;fontFamily=Helvetica;` |
| **Actividad de negocio** | Paso de un proceso (155×52) | `text;html=1;whiteSpace=wrap;fontColor=#1a1a1a;fontSize=12;fontFamily=Helvetica;align=center;verticalAlign=middle;fillColor=#f7f7f7;strokeColor=#43a047;rounded=1;spacing=10;` |
| Actividad **por definir** | Paso aún no acordado | La misma + `dashed=1;` y un *callout* con la pregunta |
| Actividad del **core** | Pasos del Core ADR | Igual, con `strokeColor=#333333` |
| **Actor / canal externo** | Canales, Konecta | `fillColor=#fde9cc;strokeColor=#d79b00;strokeWidth=3;fontSize=14` + ícono `Patient_List` |
| **Cola / topic** | RabbitMQ (46×46), etiqueta debajo en negrita | `image;aspect=fixed;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;fontColor=#1a1a1a;fontSize=13;fontFamily=Helvetica;labelBackgroundColor=none;image=https://icons.diagrams.net/assets/sap/1/SAP_SE_RabbitMQ.svg;` |
| **Apigee** | Cada cruce entre dominios | `mxgraph.gcp3.apigee`, 50×48,74, `fillColor=#4285f4` |
| **Componente técnico** | Ícono Azure 44–52 px con etiqueta de 3 líneas | Mismo patrón `image;…` con ícono de `azure2/…`. Etiqueta: `<b>Nombre</b><br><font style="font-size:11px">qué hace</font><br><font style="font-size:10px" color="#0277bd">Cx · rol</font>` |
| **Decisión** | Rombo con pregunta | `rhombus;…fillColor=#fff7d6;strokeColor=#d6b656;fontSize=13` (≈190×104) |
| **Resultado OK** | ✔ salida exitosa (300×64) | `rounded=1;fillColor=#e8f5e3;strokeColor=#43a047;strokeWidth=2;fontSize=13` |
| **Resultado a revisión** | ⚠ salida que va a persona | `fillColor=#fde9cc;strokeColor=#d79b00;strokeWidth=2` |
| **Resultado error** | ⚠ falla técnica | `fillColor=#fdeaea;strokeColor=#d9534f;strokeWidth=2` |
| **Persistencia propia / modelos** | Auditoría Cosmos DB, grupo de modelos, catálogo, expediente | `rounded=1;fillColor=#f4edfa;strokeColor=#8e5cc4;strokeWidth=2;fontSize=13` |
| **Eventos Kafka** | Banda de eventos hacia la torre de control | `rounded=1;fillColor=#fdf0db;strokeColor=#e08a1e;strokeWidth=2;fontSize=13` |
| **Llamada al core** | Pasos que consultan al core | `fillColor=#fdf0db` o `#fde9cc` con `strokeColor=#d79b00;strokeWidth=2` |
| **Píldora** | `→ IA` (usa modelo), `→ MCP` (consulta al core) | `rounded=1;arcSize=50;html=1;fillColor=#e1f5fe;strokeColor=#0288d1;fontColor=#0277bd;fontSize=10;fontStyle=1;fontFamily=Helvetica;strokeWidth=1.5;` (58×18) |
| **Píldora `→ Torre de control`** | El componente envía su trazabilidad al Kafka interno de la Torre de control. Va en la esquina superior derecha del contenedor (125×18) | `rounded=1;arcSize=50;html=1;fillColor=#fdf0db;strokeColor=#e08a1e;fontColor=#b35c00;fontSize=10;fontStyle=1;fontFamily=Helvetica;strokeWidth=1.5;` |
| **Torre de control** | Contenedor de dominio "Torre de control · transversal" (1022×300): Kafka interno (estilo de eventos) → *Ve el flujo end to end* → *Tablero + copiloto* (estilo morado) | Estilos de contenedor de dominio, eventos Kafka y persistencia propia de esta tabla |
| **Trazabilidad del orquestador** | Caja morada "Trazabilidad del mensaje" (420×95) dentro del orquestador, con 3 pasos blancos de borde morado: 1. Recibido → 2. Procesado → 3. Encolado | Persistencia propia + pasos `fillColor=#ffffff;strokeColor=#8e5cc4;fontSize=11` |
| **Sub-detalle** | Recuadro que explica un paso | `rounded=1;dashed=1;fillColor=none;strokeColor=#d79b00;fontSize=12;fontStyle=1` con título en la esquina |
| **Etiqueta de sección** | "A. RECEPCIÓN…", "B. EXTRACCIÓN…" | `text;…fontSize=13;align=left` con `<font color="#0277bd"><b>…</b></font>` |
| **Pregunta abierta** | Duda para negocio o el core | `shape=wedgeCallout;whiteSpace=wrap;html=1;` |
| **Salida exitosa de un paso** | ✔ resultado positivo de una validación del proceso (155×52) | `rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f5e3;strokeColor=#43a047;strokeWidth=2;fontColor=#1a1a1a;fontSize=12;fontFamily=Helvetica;` · texto `<b>✔ Título</b><br><font style="font-size:11px">qué sigue</font>` · conector verde `#43a047` grosor 2 con etiqueta "Sí" |
| **Flujo pendiente de definir** | ⏳ salida que existe pero cuyo destino aún no se acuerda (222×60) | `rounded=1;whiteSpace=wrap;html=1;fillColor=#fde9cc;strokeColor=#d79b00;strokeWidth=2;dashed=1;fontColor=#1a1a1a;fontSize=12;fontFamily=Helvetica;` · texto `<b>⏳ Título</b><br><font style="font-size:11px">flujo pendiente de definir</font>` · conector ámbar `#d79b00` grosor 2 **punteado** con etiqueta "No" · siempre enlazado a una pregunta abierta P-xx |
| **Nota de diseño** | "Cómo funciona el juez", "Tres decisiones de diseño" | Texto en caja `fillColor=#f7f7f7`, borde verde o dorado, abajo a la derecha (≈850×230) |
| **Tabla de entrada/salida** | Contrato del gestor | Tabla HTML: `border="1" cellpadding="4"`, encabezados `background:#dae8fc`, columnas *Entrada / salida · Por dónde · Qué viaja*, abajo a la izquierda (≈1180 de ancho) |

### 9.3 Conectores

Todos `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;`.

| Tipo | Color | Grosor | Uso |
|---|---|---|---|
| Flujo de negocio entre dominios | `#333333` | 1 | Canales → Apigee → core → orquestador; sin etiqueta salvo condición |
| Flujo técnico interno | `#7a8496` | 2, `endArrow=block` | Pasos dentro del gestor |
| Camino feliz | `#43a047` | 2 | ② OK, ③ resultado, decisión "No/Sí" exitosa |
| A revisión / integración | `#d79b00` | 2 | ① integración, ③b requiere revisión |
| Error | `#d9534f` | 2 | "falla 2 veces" |
| Hacia el modelo | `#0288d1` | 2 | Modelos → LLM Gateway; contexto → pertinencia |

Las entradas y salidas del gestor se numeran con círculos (① ② ③ ③b ⚠ ④ ⑤ ⑥) y esos mismos números aparecen en la tabla de entrada/salida y en el subtítulo.

### 9.4 Composición de una página de detalle

1. **Título + subtítulo** arriba a la izquierda. En el Gestor Solicitud el título es **"Proceso end to end del Gestor de Solicitud"** y el subtítulo narra el recorrido completo: canal → Siniestro integral → orquestador → gestor → orquestador → Siniestro integral → canal. Debe decir qué entra (①), qué sale (③ ③b ⚠) y qué significan las píldoras. El Gestor Evaluación conserva por ahora "Microservicio GESTOR EVALUACIÓN — por dentro".
2. **Franjas de arriba a abajo** según el recorrido: Canales → proceso del core → Orquestador de integración → **Microservicio** → Plataforma agéntica (control plane). Core ADR, Core Salud y Konecta a la derecha.
3. Dentro del microservicio: secciones **A., B., …** de izquierda a derecha; resultados al final del flujo; abajo, **auditoría propia** (morado) y **eventos Kafka** (naranja); a la derecha, *Servicios compartidos (fuera del microservicio)*.
4. Pie: **tabla de entrada/salida** a la izquierda y **nota de diseño** a la derecha.

### 9.6 Capas de la Vista general

La *Vista general* es el resumen de toda la arquitectura. Usa capas horizontales con la etiqueta vertical a la izquierda y solo componentes que existen en las páginas de detalle:

1. **Canales:** SVP · AVA · Portal prestador · Apigee. Radican, consultan el estado y notifican.
2. **Siniestro integral:** orquestador (id de trazabilidad) → siniestro padre → validación inicial → encola el comando · cola de resultados → actualiza el estado → radica o escala · gestor documental de autorizaciones. Dirige el proceso y sus estados.
3. **Orquestador de integración:** recibe HTTP → ACK → procesa (seguridad, trazabilidad) → decide → encola → cola del destino · topic de contingencia · trazabilidad del mensaje.
4. **Gestores (microservicios):** una tarjeta por gestor (Entra · Hace · Responde · Auditoría · píldoras) y, debajo, la **plataforma agéntica compartida**: runtime agéntico, LLM Gateway (obligatorio), MCP Gateway y Document Intelligence.
5. **Cores:** Core ADR · Core Salud Voluntarios (GlobalWeb) · Konecta.
6. **Torre de control (transversal):** Kafka interno → flujo end to end → tablero + copiloto → pide acciones al core.
7. **Cómo se lee:** tabla *Auditoría de cada gestor vs Torre de control* y *Contrato igual para todos los gestores*.

Si cambia una regla que afecta un componente, la Vista general se actualiza en el mismo cambio (regla de oro).

### 9.5 Buenas prácticas identificadas

1. **Una página por microservicio "por dentro"**, con la misma estructura, para comparar gestores lado a lado.
2. **La caja punteada delimita la propiedad:** todo lo que está dentro es del microservicio; lo compartido se dibuja fuera.
3. **El color dice el tipo, no decora:** verde = camino feliz, ámbar = revisión o integración, rojo = error, morado = datos propios y modelos, naranja = eventos, azul = plataforma y dominios.
4. **Cada ícono declara su capa** (`Cx`) de la arquitectura de referencia, para trazarlo a los lineamientos IA-First.
5. **Íconos oficiales** (Azure, GCP Apigee, RabbitMQ) en lugar de cajas genéricas para componentes técnicos; cajas de texto para pasos de negocio.
6. **Resultados explícitos y finitos:** cada gestor declara sus salidas posibles con ✔/⚠ y su color.
7. **Números de paso compartidos** entre conectores, tabla y subtítulo.
8. **Las dudas se dibujan:** actividad punteada + *callout* con la pregunta para negocio, en vez de inventar la respuesta. Si lo que falta es el **destino** de una salida, se dibuja la caja ⏳ *flujo pendiente de definir* con conector punteado, para que el camino no quede mudo.
9. **Notas de diseño en el lienzo:** el porqué (costo del juez, contexto una sola vez) queda junto al diagrama.
10. **Lenguaje de negocio en las etiquetas** ("Solicitud lista", "Requiere revisión") y detalle técnico en letra pequeña.
12. **Los títulos de contenedor son solo el nombre del componente** (por ejemplo "Orquestador de integración"). Cómo funciona va adentro, dibujado, no en el título.
13. **Las relaciones transversales se marcan con píldoras, no con flechas:** `→ IA`, `→ MCP` y `→ Torre de control` dicen a qué servicio compartido habla cada componente, sin cruzar el diagrama de líneas.
11. **Conectores ortogonales sin cruces innecesarios;** las etiquetas van sobre el conector, en el color de su tipo.

---

## 10. Bitácora de cambios

| Fecha | Cambio | Reglas afectadas | Páginas tocadas |
|---|---|---|---|
| 2026-11-12 | Línea base: se levantan reglas, contratos, estilo y pendientes de *Detalle: Gestor Solicitud* y *Detalle: Gestor Evaluación (Release 1)*. | Todas (creación) | Ninguna (solo lectura) |
| 2026-11-12 | Decisión del usuario: por ahora prevalecen las reglas de las dos páginas de detalle sobre el resto del diagrama. | Precedencia (encabezado) | Ninguna |
| 2026-11-12 | P-01 resuelta según *canales con core*: orquestador que retorna id de trazabilidad, siniestro padre primero, `queue nueva solicitud`, validación inicial del documento después, comando con id del siniestro padre (uno por solicitud). Se abren P-05 y P-06. | RN-SOL-13, 14, 15, 16; contrato ① | Detalle: Gestor Solicitud (siniestro integral, 2 callouts, tabla de entrada/salida) |
| 2026-11-12 | P-05 resuelta: se incorpora el Gestor documental de autorizaciones como componente de Siniestro integral (publicar / consultar en Blob vía `apiG`); canales y siniestro integral publican, el Gestor Solicitud consulta desde su Blob de entrada. | RN-SOL-17, 18; dominios §2.1; flujo §3.1; contrato ① | Detalle: Gestor Solicitud (contenedor "Siniestro integral · Gestor documental de autorizaciones", `apiG`, 3 conectores, tabla de entrada/salida) |
| 2026-11-12 | Se dibujan las dos salidas de la validación inicial: ✔ *Documento válido* → encolar comando (que baja una fila) y ⏳ *Documento no válido: flujo pendiente de definir*. Nuevos elementos en la guía de estilo: salida exitosa de un paso y flujo pendiente de definir. | RN-SOL-19; P-06 (sigue abierta); §9.2 y §9.5 | Detalle: Gestor Solicitud (siniestro integral) |
| 2026-11-12 | Se quita el Blob de entrada del Gestor Solicitud: la consulta de archivos se hace directamente a Siniestro integral (gestor documental vía `apiG`) de forma síncrona, desde el orquestador del gestor. | RN-SOL-05 eliminada; RN-SOL-18; flujo §3.1 paso 4; contrato ② | Detalle: Gestor Solicitud (Blob y 2 conectores eliminados; conector "consulta documentos (síncrona)"; tabla ②). Pendiente de alinear: *canales con core* y *Glosario* aún muestran el Blob (prevalece el detalle) |
| 2026-11-12 | P-03 resuelta: el archivo no procesable responde *faltan datos* y sale hacia el Apigee de salida (el mismo de ③ y ③b), no hacia `apiG` del gestor documental. | RN-SOL-20; flujo §3.1 paso 6; contrato ⚠ | Detalle: Gestor Solicitud (conector ámbar "⚠ faltan datos", texto de la caja ⚠, fila ⚠ de la tabla) |
| 2026-11-12 | Corrección a P-03: la respuesta del archivo no procesable no es *faltan datos* sino **requiere revisión humana**, motivo *fallo en la validación de archivos de entrada*. | RN-SOL-20; flujo §3.1 paso 6; contrato ⚠ | Detalle: Gestor Solicitud (conector "⚠ requiere revisión humana", texto de la caja ⚠, fila ⚠ de la tabla) |
| 2026-11-12 | Se adopta la **regla de oro "un cambio, todas las pestañas"** (§9). Se alinea *canales con core* con el detalle: archivo no procesable → requiere revisión humana; se quita el Blob de entrada y la consulta sale síncrona desde el orquestador; se agregan ✔ *Documento válido* / ⏳ *Documento no válido*; contenedor "Siniestro integral · Gestor documental de autorizaciones"; tabla ① y ②; etiquetas "publica documentos" y "publica"; "Orquestador" con mayúscula; se quitan dos conectores duplicados y una etiqueta suelta "Text". | §9 (regla de oro); RN-SOL-13..20 reflejadas en ambas pestañas | canales con core |
| 2026-11-12 | I-01 resuelta para el Gestor Solicitud. Entrada: siempre un mensaje en la cola RabbitMQ del gestor, enviado por el orquestador de integración. Salida: JSON por HTTP al orquestador de integración, que lo encola en un topic, y el topic lo entrega a la cola que lee Siniestro integral. Se abren I-08 (Page-11) e I-09 (MCP Gateway sin uso). | RN-SOL-21, 22; contratos ①③③b⚠ |
| 2026-11-12 | Rol del orquestador de integración: recibe mensajes HTTP, responde de inmediato que los recibió (ACK) y los encola, con seguridad y trazabilidad. | RN-TRV-07, 08, 09; dominio §2.1 | Título del contenedor "Orquestador de integración · recibe HTTP, responde de inmediato que recibió (ACK) y encola · seguridad y trazabilidad" en las 4 pestañas donde aparece: Detalle Solicitud, canales con core, Detalle Evaluación R1, Evaluación Release final |
| 2026-11-12 | Gateways: el MCP Gateway se mantiene dibujado y el LLM Gateway es obligatorio para usar LLMs. Se levanta del cronograma la información que necesita el Gestor Solicitud (§3.3b) y se registran las diferencias D-01..D-04. | RN-TRV-03, RN-TRV-10; I-09 cerrada; §3.3b | Ninguna (el diagrama ya tenía ambos gateways) |
| 2026-11-12 | D-01 resuelta: se dibuja el **Homologador de códigos** entre los extractores y el validador, con la píldora `→ MCP` y un conector punteado azul "consulta tabla de homologación" hacia el MCP Gateway. Validador, juez, rombo y resultados se corren 170 px a la derecha. La leyenda del subtítulo explica `→ MCP`. La etiqueta de ③b se mueve sobre su conector para no tapar "Servicios compartidos". | RN-SOL-23; flujo §3.1 paso 5; D-01; I-09 | *Detalle: Gestor Solicitud* y *canales con core* (las dos con el mismo cambio) |
| 2026-11-12 | Principio de alcance: el diagrama es la arquitectura completa y el cronograma solo organiza la implementación. D-02 resuelta: el Extractor Facturas se mantiene. | Encabezado (alcance); D-02 | Ninguna |
| 2026-11-12 | D-03 resuelta. La salida del gestor lleva el detalle de la respuesta (causa concreta del fallo de archivo). Siniestro integral administra los estados y los marca con ese detalle. Los canales consultan el estado y notifican al usuario. | RN-SOL-24; RN-TRV-11, 12; dominios §2.1; flujo §3.1 paso 8; contrato ⚠ | *Detalle: Gestor Solicitud* y *canales con core*: nueva actividad "Actualiza el estado de la solicitud" en Siniestro integral (conector "marca" desde la cola de resultado), conector punteado Canales ↔ estado "consulta el estado (vía Apigee) y notifica al usuario", texto de la caja ⚠ y fila ⚠ de la tabla con la causa detallada |
| 2026-11-12 | D-04 (uso del tipo documental que marca el prestador) se declara fuera del alcance de este diagrama. | D-04 | Ninguna |
| 2026-11-12 | El **Gestor documental de autorizaciones** se dibuja **dentro** del contenedor Siniestro integral (antes estaba al lado, con prefijo en el nombre). Siniestro integral se ensancha a 2320. La caja queda de 310 × 193, arriba a la derecha, con título "Gestor documental de autorizaciones". El conector "consulta documentos (síncrona)" se reencamina por el borde para no cruzarla. | Dominios §2.1 (sin cambio de regla, solo visual) | *Detalle: Gestor Solicitud* y *canales con core* |
| 2026-11-12 | El título de las páginas del Gestor Solicitud pasa de "Microservicio GESTOR SOLICITUD — por dentro" a **"Proceso end to end del Gestor de Solicitud"**, con un subtítulo que narra el recorrido completo del canal al estado final. | §9.4 | *Detalle: Gestor Solicitud* y *canales con core* |
| 2026-11-12 | Decisiones de plataforma: **AKS** en lugar de Azure Container Apps y **Cosmos DB** en lugar de MongoDB. Regla de mensajería: **comandos siempre por RabbitMQ, trazabilidad siempre por Kafka**. | RN-TRV-04, RN-TRV-05, RN-SOL-11, RN-EVA-05, RN-EVA-10 (texto); RN-TRV-16, RN-TRV-17 nuevas; P-07 | Las 4 pestañas de gestores (títulos de contenedor y auditoría/expediente), Vista general (nota de gestores, runtime, contrato, auditorías, subtítulo), Juez (catálogo de rúbricas, veredicto → trazabilidad a la Torre de control), Dónde vive la IA (título, AKS, Cosmos DB con su ícono), Duplicados (catálogo en Cosmos DB con su ícono), Glosario (filas de runtime, estado, auditoría, catálogo y regla RabbitMQ/Kafka) |
| 2026-11-12 | **Glosario alineado (I-10).** Cambios por fila: C1 consumidores (canales SVP · AVA · Portal prestador, Konecta, tablero de la Torre; consultan estado y notifican). API Gateway → **Apigee** (y apiG del gestor documental). LLM Gateway **obligatorio**. MCP Gateway con ejemplos de uso. Domain APIs → Core ADR, Core Salud / GlobalWeb, tabla de homologación. "Coordinador y perfil de proceso" → **Proceso general y estados = Siniestro integral**. "Core SURA (SuraHist) dirige el proceso" → **Cores SURA**: Core ADR y Core Salud aplican reglas, autorizan y radican. Object storage → **gestor documental de Siniestro integral**, sin copias en los gestores. Filas nuevas: **Orquestador de integración** (C3) y **Homologador de códigos** (C4). | I-10 | Glosario |
| 2026-11-12 | **Vista general rehecha.** Las capas anteriores (Canales · Core SURA dirige el proceso · Gestores · Eventos · Torre de control · Cómo se lee) y sus componentes (Proveedor/Cliente, API Management, CORE SURA SuraHist) ya no correspondían. Quedan 7 capas con los componentes de los detalles: Canales · Siniestro integral · Orquestador de integración · Gestores + plataforma agéntica compartida · Cores · Torre de control · Cómo se lee. Se conservan la tabla *Auditoría vs Torre de control* y el *Contrato*, cuyo punto 4 ahora dice que el gestor envía su trazabilidad a la Torre de control. Se abre I-10 (Glosario desalineado). | §9.6; I-10 | Vista general |
| 2026-11-12 | El contenedor del orquestador vuelve a llamarse solo **"Orquestador de integración"**. Adentro se dibuja la caja **Trazabilidad del mensaje**: 1. Recibido (HTTP · ACK inmediato) → 2. Procesado (seguridad · registro) → 3. Encolado (topic → cola del destino). En *Release final* el orquestador crece a 360 de alto para que la caja no cruce un conector. | RN-TRV-09; §9.2, §9.5 | Detalle Solicitud, canales con core, Detalle Evaluación R1, Evaluación Release final |
| 2026-11-12 | Nueva **Torre de control transversal con Kafka interno**: todos los componentes le envían su trazabilidad. Se agrega el contenedor "Torre de control · transversal" (Kafka interno → flujo end to end → tablero + copiloto) y la píldora `→ Torre de control` en canales, Siniestro integral, orquestador (caja de trazabilidad), Core ADR, Core Salud y CORE SURA. Las bandas "Publica eventos en Kafka" de los gestores pasan a "Envía su trazabilidad a la Torre de control (Kafka interno)". La leyenda de píldoras se completa en los subtítulos. | RN-TRV-15; RN-TRV-05, RN-SOL-12, RN-EVA-11; dominio §2.1; §9.2, §9.5 | Detalle Solicitud y canales con core (5 píldoras cada una), Detalle Evaluación R1 (2), Evaluación Release final (3); *Vista general* (banda KAFKA → "KAFKA interno de la Torre de control"); *Glosario* (filas C5 Events y C1 Torre de Control) |
| 2026-11-12 | I-01 resuelta para el Gestor Evaluación, y la entrada y salida pasan a ser reglas de **todos** los gestores. Los textos ya coinciden con lo dibujado. | RN-TRV-13, 14; I-01 | *Detalle: Gestor Evaluación (R1)* y *Gestor Evaluación Release final*: subtítulo, tabla (④ ⑤ ⑤b), "cola q.evaluacion (RabbitMQ)", conectores "publica respuesta", "⑤ recomendación" y "⑤b duplicada" con "· JSON/HTTP". *Vista general*: "Contrato igual para todos los gestores" (pasos 1 y 3), las 5 tarjetas "Se activa: mensaje en su cola RabbitMQ (orquestador de integración)", conector "activa (orquestador)". *Glosario*: filas C4 "Microservicio gestor" y "Gestor (módulo)" | *Detalle: Gestor Solicitud* y *canales con core*: subtítulo, tabla de entrada/salida, etiqueta "Cola del gestor (RabbitMQ)", conectores ③/③b/⚠ con "· JSON/HTTP" |
