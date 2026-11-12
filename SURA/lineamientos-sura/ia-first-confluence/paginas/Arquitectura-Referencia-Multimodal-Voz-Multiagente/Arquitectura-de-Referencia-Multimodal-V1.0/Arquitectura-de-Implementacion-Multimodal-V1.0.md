---
titulo: "Arquitectura de Implementacion Multimodal V1.0"
id: 6232735751
espacio: AFGLYP
version: 1
actualizado: 2026-08-26T13:39:56.634Z
actualizado_por: "Junior Millan Perez"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Referencia [Multimodal - Voz - Multiagente] > Arquitectura de Referencia Multimodal V1.0"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6232735751
---

# Arquitectura de Implementacion Multimodal V1.0

## Marco normativo y documentos relacionados

| Documento | Relación |
| --- | --- |
| `Arquitectura de Referencia Multimodal V1.0` | Marco normativo del canal |
| `Arquitectura de Referencia Voz V1.0` | Marco normativo de la modalidad de audio |
| `Arquitectura de Referencia Multiagente V1.0` | Modelo de orquestación y propagación de identidad |
| `Arquitectura de Referencia V1.1` | Convenciones, principios y atributos de calidad |
| `AI Gateway`, `AI Security Enforcement`, `AI-LLM Lifecycle Management`, `FinOps` | Capacidades transversales de cumplimiento obligatorio |
| `Blueprint de Capacidades Arquitectura Agéntica` | Capacidades objetivo de plataforma |

---

# 1. Alcance, límites y supuestos

## 1.1 Alcance de la implementación

**Formatos habilitados y ruta de procesamiento:**

| Modalidad | Formatos | Ruta |
| --- | --- | --- |
| Texto directo | — | Sin transformación |
| Texto plano | `.txt`, `.csv`, `.md` | Decodificación con detección de codificación |
| Documento ofimático | `.docx` | Extracción estructurada |
| Documento portátil nativo | `.pdf` con capa de texto | Extracción de capa de texto |
| Documento portátil escaneado | `.pdf` sin capa de texto | OCR por página |
| Audio | `webm/opus`, `mp4/aac` | Definido en `Arquitectura de Implementación Voz V1.0`. Aquí se especifica su integración con el pipeline común |

**Elementos construidos en este alcance:** pipeline de ingesta con validación, escaneo de malware, extracción, sanitización, detección de PII y moderación; ruta síncrona y asíncrona con límites cuantificados; caché de artefactos; modelo de persistencia y ciclo de vida; contratos de interfaz, códigos de error y eventos; topología de despliegue; observabilidad con umbrales; estrategia de pruebas y plan de construcción.

## 1.2 Límites de la implementación

Además de las exclusiones del marco normativo, esta implementación acota dos capacidades cuya ausencia produce un efecto cuantificado en este documento.

| Límite | Efecto |
| --- | --- |
| **Sin recuperación aumentada**: chunking, embeddings, índice y retrieval | El texto extraído se entrega íntegro al contexto del modelo. La ventana de contexto pasa a ser el techo de tamaño de documento del sistema, cuantificado en 9.4 y registrado como R-M-01 |
| **Sin citación a página o región** | La respuesta del agente no ancla sus afirmaciones a una ubicación del documento origen. Registrado como R-M-02 |

La decisión implementada entre capa de texto y OCR se resuelve por página en 9.5. Los formatos no habilitados se rechazan por lista blanca según 9.1.

## 1.3 Supuestos

| ID | Supuesto |
| --- | --- |
| S-M-01 | La nube de destino es **Azure**. El gateway, la identidad, el almacenamiento, el gobierno del dato y la observabilidad del despliegue residen en esa nube |
| S-M-02 | El idioma predominante de los documentos es **español**, con presencia minoritaria de inglés |
| S-M-03 | El Agent Runtime expone `POST /invoke` y **opera sin lógica específica de modalidad**: recibe el texto extraído de un archivo por el mismo campo que el chat directo |
| S-M-04 | Existe un servicio corporativo de escaneo de malware consumible por API o por integración con el almacenamiento |
| S-M-05 | El enlace de subida efectivo del usuario es de al menos **3 Mbps** |
| S-M-06 | Los usuarios son internos y autenticados con Entra ID |
| S-M-07 | Existe un broker de mensajería corporativo disponible para el dominio |
| S-M-08 | Los documentos adjuntos son aportados por el propio usuario como contexto de su consulta, no ingeridos masivamente desde repositorios |

---

# 2. Requisitos no funcionales cuantificados

## 2.1 Objetivos de negocio

Los objetivos cuantitativos de negocio se establecen tras la primera ejecución con datos reales. Hasta entonces quedan declarados como pendientes, con la fuente de dato que los cierra. Sin estos valores no es posible dimensionar la topología de la sección 8 ni validar el presupuesto de latencia de 2.3.

| ID | RNF | Métrica | Valor | Fuente de dato requerida |
| --- | --- | --- | --- | --- |
| P-M-01 | Concurrencia | Ingestas simultáneas en pico | `[PENDIENTE DE DEFINIR]` | Proyección de adopción del owner funcional |
| P-M-02 | Volumen | Documentos por día y por modalidad | `[PENDIENTE DE DEFINIR]` | Proyección por caso de uso del owner funcional |
| P-M-03 | Perfil documental | Distribución real de tamaño, páginas y proporción de PDF escaneado | `[PENDIENTE DE DEFINIR]` | **Muestra de documentos reales.** Determina el dimensionamiento de OCR |
| P-M-04 | Latencia de procesamiento | p95 desde binario disponible hasta texto normalizado | `[PENDIENTE DE DEFINIR]` | Compromiso de experiencia del owner funcional |
| P-M-05 | Disponibilidad | Objetivo mensual del canal | `[PENDIENTE DE DEFINIR]` | Criticidad del caso de uso y Matriz de Riesgos |
| P-M-06 | Costo objetivo | Costo por documento procesado y presupuesto mensual | `[PENDIENTE DE DEFINIR]` | FinOps. El OCR y los tokens de contexto dominan el costo |
| P-M-07 | Calidad de extracción | Cobertura y exactitud mínimas por formato | `[PENDIENTE DE DEFINIR]` | Primera ejecución del set de evaluación. Sección 13.4 |
| P-M-08 | Retención | Días de conservación de binario, texto extraído y caché | `[PENDIENTE DE DEFINIR]` | Gobierno del dato y requisito regulatorio |

## 2.2 Parámetros de ingeniería con valor concreto

| Parámetro | Valor | Sección |
| --- | --- | --- |
| Tamaño máximo por archivo, ruta síncrona | 10 MB | 9.2 |
| Tamaño máximo por archivo, ruta asíncrona | 50 MB | 9.2 |
| Umbral de subida directa a almacenamiento | > 10 MB | 6.2 |
| Páginas máximas en ruta síncrona, PDF nativo | 50 | 9.3 |
| Páginas máximas en ruta síncrona, con OCR | 5 | 9.3 |
| Páginas máximas absolutas | 300 | 9.3 |
| Umbral de clasificación de página escaneada | < 100 caracteres por página | 9.5 |
| TTL del caché de artefactos | 7 días | 9.7 |
| Reintentos ante fallo transitorio | 2 | 10.4 |
| Archivos adjuntos por mensaje | 5 | 9.2 |

## 2.3 Presupuesto de latencia

Como el objetivo de negocio está pendiente (P-M-04), el presupuesto se construye contra un **objetivo técnico de referencia** que debe ser ratificado.

**Separación deliberada entre subida y procesamiento.** La subida es visible para el usuario mediante barra de progreso y su duración depende de su enlace; el procesamiento es una espera opaca. Se presupuestan por separado porque su tolerancia percibida es distinta.

### Subida (informativa, acotada por timeout)

| Tamaño | Tiempo a 3 Mbps efectivos (S-M-05) | Ruta |
| --- | --- | --- |
| 500 KB | 1,3 s | Síncrona vía APIM |
| 2 MB | 5,3 s | Síncrona vía APIM |
| 10 MB | 26,6 s | Síncrona vía APIM, en el límite |
| 50 MB | 133 s | **Asíncrona con subida directa al almacenamiento.** Ver 6.2 |

### Procesamiento — objetivo técnico de referencia: 8.000 ms p95

Escenario de cálculo: PDF nativo de 50 páginas, ruta síncrona, sin acierto de caché.

| Tramo | Componente | p50 | p95 | Justificación |
| --- | --- | --- | --- | --- |
| T1 | APIM: JWT, cuotas, límite de tamaño | 30 ms | 70 ms | Políticas en memoria |
| T2 | Escaneo de malware | 400 ms | 1.200 ms | Llamada a servicio externo sobre el binario completo |
| T3 | Validación de tipo real y de estructura | 40 ms | 100 ms | Lectura de *magic bytes* y apertura del contenedor |
| T4 | Consulta de caché | 15 ms | 40 ms | Búsqueda por SHA-256 |
| T5 | Extracción de texto | 900 ms | 2.500 ms | Extracción de capa de texto sobre 50 páginas |
| T6 | Clasificación por página y decisión de OCR | 20 ms | 50 ms | Conteo de caracteres por página |
| T7 | Sanitización y normalización | 120 ms | 300 ms | Normalización Unicode y filtrado sobre el texto completo |
| T8 | Detección de PII | 350 ms | 900 ms | Llamada a servicio especializado |
| T9 | Moderación de entrada | 300 ms | 800 ms | Llamada a servicio de guardrails |
| T10 | Verificación del límite de contexto | 10 ms | 30 ms | Conteo de caracteres y tokens estimados |
| T11 | Persistencia del artefacto y emisión de traza | 80 ms | 200 ms | Escritura de metadata y span |
| T12 | Entrega al Agent Runtime | 30 ms | 80 ms | Llamada interna |
| — | **Total** | **2.295 ms** | **6.270 ms** | Dentro del objetivo de 8.000 ms |

**Holgura disponible:** 1.730 ms sobre p95. Los tramos dominantes son T5 (extracción) y T2 (malware).

### Ruta con acierto de caché

El acierto omite T2, T5, T6 y T7, pero **no omite T8 ni T9**: la detección de PII y la moderación se reevalúan siempre para el usuario solicitante (ver 11.6).

| Total con acierto de caché | p50 | p95 |
| --- | --- | --- |
| T1+T3+T4+T8+T9+T11+T12 | 845 ms | 2.190 ms |

Reducción del 65 % sobre el p95. Es la justificación cuantitativa del caché de 9.7.

### Ruta con OCR

El OCR procesa entre 0,5 s y 2 s por página según motor y calidad del escaneo. Un documento escaneado de 50 páginas consume entre 25 s y 100 s solo en T5, muy por encima del objetivo síncrono. **De ahí el límite de 5 páginas para OCR síncrono** de 9.3: 5 páginas equivalen a entre 2,5 s y 10 s, el máximo compatible con el presupuesto.

---

# 3. Diagrama de componentes

## 3.1 Vista de componentes

Capa Transversal

Ruta asincrona

Plataforma de capacidades de IA

Capa de Agent Runtime

Normalizacion y control

Capa de Transformacion de Canal

Pipeline de Ingesta

Capa de Gateway

Capa de Experiencia

## 3.2 Responsabilidades y contratos

| Componente | Responsabilidad única | Contrato expuesto |
| --- | --- | --- |
| Frontend Angular | Capturar el input en su modalidad original. **No extrae ni transforma** | Interfaz de usuario |
| Azure APIM | Punto único de entrada. AuthN/AuthZ, cuotas por canal, límite de tamaño, enrutamiento, propagación de identidad | `POST /v1/files/*`, `POST /v1/chat/*` |
| Modality Router | Decidir el pipeline a partir del **tipo real**, no del declarado | API interna |
| Malware Scanner | Bloquear binarios maliciosos **antes de toda extracción** | Integración con servicio corporativo |
| Validator | Verificar tipo real, integridad estructural y límites | API interna |
| Artifact Cache | Evitar reprocesar el mismo binario | API interna |
| File Text Extractor | Extraer texto y **encapsular al motor de extracción** | `POST /internal/extract` |
| OCR Engine | Reconocer texto en páginas sin capa de texto | API interna |
| Speech Processor | Convertir audio a texto | `POST /internal/speech/transcribe` |
| Sanitizer | Neutralizar el contenido no confiable antes del contexto del modelo | API interna |
| PII Detection | Detectar y redactar información personal | Servicio especializado |
| Content Moderation | Moderar entrada y salida | Servicio de guardrails |
| Context Guard | Impedir que el texto exceda la ventana de contexto. **Hace explícito el techo de 9.4** | API interna |
| Ingest Worker | Procesar la ruta asíncrona | Consumidor del broker |
| Agent Runtime | Razonar sobre texto. **No conoce la modalidad de origen** | `POST /invoke` + `agent-card.json` |

**Orden obligatorio del pipeline.** Ningún contenido alcanza el Agent Runtime sin haber atravesado Sanitizer, PII Detection, Content Moderation y Context Guard, en ese orden. La consecuencia de alterarlo se detalla en 11.7.

## 3.3 Matriz modalidad → motor → endpoint

| Modalidad | Formatos | Componente | Motor | Endpoint | Salida |
| --- | --- | --- | --- | --- | --- |
| Texto directo | — | — | — | `POST /v1/chat/message` | Texto |
| Texto plano | `.txt`, `.csv`, `.md` | File Text Extractor | Decodificador con detección de codificación | `POST /v1/files/upload` | Texto |
| Documento ofimático | `.docx` | File Text Extractor | Motor de extracción estructurada. D-M-02 | `POST /v1/files/upload` | Texto |
| PDF nativo | `.pdf` con capa de texto | File Text Extractor | Extractor de capa de texto. D-M-02 | `POST /v1/files/upload` | Texto |
| PDF escaneado | `.pdf` sin capa de texto | File Text Extractor + OCR Engine | Motor OCR. D-M-03 | `POST /v1/files/upload` | Texto |
| Audio | `webm/opus`, `mp4/aac` | Speech Processor | Proveedor STT. D-V-01 del documento de Voz | `POST /v1/voice/message` | Texto |
| Razonamiento | — | Agent Runtime | Modelo de lenguaje. D-M-01 | `POST /invoke` | Texto |

Toda modalidad converge en un único endpoint de razonamiento. Incorporar una modalidad nueva consiste en añadir una fila a esta matriz: un motor y una ruta de transformación. No requiere modificar el Agent Runtime ni su contrato.

---

# 4. Stack tecnológico

## 4.1 Componentes con decisión cerrada

| Componente | Producto elegido | Justificación | Alternativa descartada |
| --- | --- | --- | --- |
| SPA de captura | Angular con `FileReader` y `MediaRecorder` | APIs nativas del navegador, sin dependencias externas | Librerías de carga de terceros: amplían la superficie de dependencia sin beneficio |
| Autenticación | MSAL para Entra ID | Estándar corporativo de identidad. Permite propagar el JWT del usuario en toda la cadena | Autenticación propia del canal: rompe la propagación de identidad |
| Gateway | Azure API Management | Punto único de entrada y de aplicación de gobierno. Soporta token-limit y cuotas por canal | Ingress directo al backend: elimina el punto único de control |
| Runtime del agente | Python + LangGraph | Orquestación por grafo de estados con control explícito de iteraciones y límites | Lógica de canal embebida en el agente: introduce dependencia de modalidad |
| Acceso a modelos | LLM Gateway | Abstracción obligatoria del proveedor. Habilita routing, fallback y control de consumo | Invocación directa al proveedor desde el agente: acopla el runtime al vendor |
| Herramientas | MCP Gateway sobre Azure API Management | Soporte nativo de registro y exposición de servidores MCP | Desarrollo a la medida: duplica gobierno y trazabilidad |
| Observabilidad | OpenTelemetry con Traceloop, exportación a Dynatrace | Traza distribuida con propagación de `traceId`, `spanId` y `correlationId` | Telemetría propia del canal: rompe la traza extremo a extremo |
| Lifecycle y evals | Langfuse | Gestión versionada de prompts, datasets y scores, con despliegue por etiqueta | Alternativas equivalentes de mercado: no aportan diferencia funcional sobre este alcance |
| Gobierno del dato | Governance API | Clasificación, ACL heredada y retención aplicadas por política central | Política embebida por componente: produce criterios divergentes |
| Almacenamiento de binarios | Azure Blob Storage | Cifrado en reposo, ACL heredada y acceso por identidad administrada | Persistencia en base de datos: inadecuada para binarios |
| Mensajería asíncrona | Broker de mensajería corporativo | Desacopla la ruta asíncrona de la petición del usuario | Procesamiento síncrono de documentos grandes: excede el timeout del gateway |

## 4.2 Componentes con decisión pendiente

### D-M-01 — Modelo de lenguaje y ventana de contexto · **Bloqueante**

El modelo de razonamiento se consume a través del LLM Gateway. La selección del modelo concreto y de su ventana de contexto está abierta.

**Por qué es bloqueante en este canal:** en ausencia de recuperación aumentada, **la ventana de contexto del modelo es el límite duro de tamaño de documento del sistema** (sección 9.4). Sin ese valor no se puede fijar el límite operativo ni comunicar al usuario qué documentos son procesables.

**Criterio:** tamaño de ventana de contexto, calidad de comprensión sobre documentos largos en español, costo por millón de tokens de entrada, disponibilidad en la región elegida y consistencia con el resto de agentes del dominio.

### D-M-02 — Motor de extracción documental · **Bloqueante**

El motor de extracción documental no está seleccionado.

| Opción | A favor | En contra |
| --- | --- | --- |
| **Apache Tika** | Amplia cobertura de formatos con un único componente | Requiere runtime Java: **el Agent Runtime es Python**, por lo que implica un servicio separado con su propio ciclo de despliegue |
| **Librerías Python especializadas** (una por formato) | Mismo lenguaje que el resto del backend. Control fino sobre la extracción de PDF y DOCX | Una dependencia por formato; el mantenimiento crece con cada formato nuevo |
| **Servicio administrado de análisis documental** | Sin operación propia. OCR y extracción en el mismo servicio | Costo por página, dependencia de proveedor, envío del documento a un servicio externo |

**Criterio:** cobertura de formatos requeridos, fidelidad de extracción de tablas y estructura, huella operativa, costo, y compatibilidad con el runtime de ejecución.

**Consecuencia:** la opción de servicio administrado resolvería simultáneamente D-M-02 y D-M-03, a costa de un modelo de costo por página y de una dependencia externa adicional que debe evaluarse frente a gobierno del dato.

### D-M-03 — Motor de OCR · **Bloqueante si hay PDF escaneado**

El motor de OCR no está seleccionado.

| Opción | A favor | En contra |
| --- | --- | --- |
| Servicio administrado de reconocimiento documental | Alta precisión en español, sin operación propia, salida estructurada | Costo por página, envío del documento a servicio externo |
| Motor OCR autoalojado | Sin costo por página, el documento no sale del perímetro | Menor precisión en documentos degradados, operación propia, mayor latencia |

**Criterio:** precisión en español sobre una muestra real de documentos escaneados, costo por página frente al volumen de P-M-03, latencia, soporte de *private endpoint* y residencia del dato.

**Dependencia crítica:** este criterio **no se puede evaluar sin P-M-03**, la muestra real de documentos. Sin ella, la decisión se toma a ciegas.

### D-M-04 a D-M-08

| ID | Decisión | Opciones | Criterio |
| --- | --- | --- | --- |
| D-M-04 | Servicio de escaneo de malware | Escaneo integrado del almacenamiento · servicio corporativo por API · producto de terceros | Cobertura de formatos, latencia añadida al tramo T2, integración con el SIEM corporativo |
| D-M-05 | Servicio de detección y redacción de PII | Servicio administrado de lenguaje · plataforma corporativa de DLP · combinación | Precisión en español, categorías cubiertas, latencia, integración con el marco corporativo. Ver `AI Security Enforcement.md` |
| D-M-06 | Servicio de moderación y guardrails | Servicio administrado de seguridad de contenido · guardrails del proveedor de modelos | Detección de ataques indirectos por documento, latencia, cobertura de categorías |
| D-M-07 | Región de despliegue | Regiones candidatas de Azure | Residencia del dato, disponibilidad de los servicios de OCR y PII, latencia, consistencia con el resto del despliegue |
| D-M-08 | Runtime de despliegue del pipeline | AKS · Container Apps · App Service | Perfil de carga intensivo en CPU y memoria de la extracción, escalado dirigido por cola, capacidad operativa |
| D-M-09 | Base de datos del dominio | Motores administrados disponibles en la región | Bloquea la materialización de la sección 7 |
| D-M-10 | Almacén del caché de artefactos | Caché distribuida · base de datos · almacenamiento de objetos | Tamaño del texto extraído, latencia de lectura, TTL nativo, costo |

## 4.3 Componentes explícitamente descartados

| Descartado | Razón |
| --- | --- |
| Extracción de texto en el navegador | Centraliza el gobierno en el backend y evita procesamiento de contenido sensible en el cliente |
| Subida de archivos grandes a través de APIM | El gateway no es una ruta de datos masivos. Ver 6.2 |
| Truncado silencioso de documentos que exceden el contexto | Produce respuestas fundadas en un fragmento que el usuario desconoce. Ver 9.4 |
| Extracción sin escaneo de malware previo | Abrir un documento no escaneado expone al motor de extracción. Ver 11.3 |
| Caché compartido entre ámbitos de aislamiento sin revalidar autorización | Vector de fuga de información entre usuarios. Ver 11.6 |
| Confianza en la extensión o en el `Content-Type` declarado | Ambos son controlados por el cliente. Ver 9.5 |

---

# 5. Diagramas de secuencia

## 5.1 SD-M-01 · Flujo feliz, PDF nativo, ruta síncrona

Agent RuntimeContext GuardModerationPII DetectionSanitizerFile Text ExtractorArtifact CacheValidatorMalware ScannerModality RouterAzure APIMFrontendUsuarioAgent RuntimeContext GuardModerationPII DetectionSanitizerFile Text ExtractorArtifact CacheValidatorMalware ScannerModality RouterAzure APIMFrontendUsuarioAdjunta PDF y escribe su pregunta1Valida extension y tamano en cliente2POST /v1/files/upload, JWT, Idempotency-Key3Valida JWT, cuota de canal y tamano4Enruta5Escanea el binario6Limpio7Valida tipo real por magic bytes y estructura8Valido. PDF, 42 paginas, 3.1 MB9Consulta por SHA-256 + version de extractor10Fallo de cache11Extrae12Clasifica por pagina: capa de texto presente13Texto, 84.300 caracteres, cobertura 42/4214Sanitiza15NFKC, invisibles, bidi, metadatos, texto oculto16Texto sanitizado + hallazgos17Detecta PII18Sin PII no autorizada19Modera la entrada20Aprobado21Verifica el limite de contexto2284.300 caracteres, dentro del limite23Almacena el artefacto y su texto24POST /invoke con pregunta + texto del documento25Modera la salida26Aprobado27Respuesta en texto2820029Muestra la respuesta30

## 5.2 SD-M-02 · PDF escaneado con OCR, ruta asíncrona

Blob StorageOCR EngineFile Text ExtractorIngest WorkerBrokerValidatorModality RouterAPIMFrontendBlob StorageOCR EngineFile Text ExtractorIngest WorkerBrokerValidatorModality RouterAPIMFrontend78 paginas sin capa de texto,2 paginas con capa de textoPOST /v1/files/upload, PDF de 80 paginas1Enruta2Valida380 paginas mayor que el limite sincrono de OCR4Persiste el binario en el contenedor temporal5Publica ingest.document.requested6202 Accepted, jobId, pollUrl7202 jobId8Muestra progreso9Consume10Extrae11Clasifica por pagina12OCR sobre las 78 paginas13Texto reconocido + confianza por pagina14Texto consolidado, cobertura 80/8015Sanitiza, detecta PII, modera, verifica contexto16Borra el binario temporal17Publica ingest.document.completed18GET /v1/files/job/jobId19200 completed, artifactId, metricas de extraccion20POST /v1/chat/message con artifactId21200 respuesta del agente22

## 5.3 SD-M-03 · Documento que excede el límite de contexto

Context GuardFile Text ExtractorModality RouterFrontendUsuarioContext GuardFile Text ExtractorModality RouterFrontendUsuarioLa respuesta incluye: caracteres extraidos,tokens estimados, limite vigente,paginas del documento y paginas aproximadas admisiblesEl usuario puede dividir el documentoo seleccionar el rango de paginas [relevante.NO](http://relevante.NO) se trunca en silencioPDF de 240 paginas1Extrae2Texto, 612.000 caracteres3Verifica el limite de contexto4612.000 caracteres estimados en 175.000 tokens5Limite operativo del modelo: 100.000 tokens6EXCEDE7413 DOCUMENT_EXCEEDS_CONTEXT8Explica el limite y ofrece opciones9

## 5.4 SD-M-04 · Malware detectado

Governance APISIEMMalware ScannerModality RouterAPIMFrontendGovernance APISIEMMalware ScannerModality RouterAPIMFrontendNO se extrae, NO se persiste,NO se almacena en cacheMensaje generico al [usuario.No](http://usuario.No) se expone el detalle del veredictoPOST /v1/files/upload1Enruta2Escanea3AMENAZA DETECTADA4Descarta el binario de inmediato5Evento de seguridad con usuario, hash y veredicto6Registra el incidente7422 FILE_REJECTED_SECURITY84229

## 5.5 SD-M-05 · Acierto de caché con revalidación de autorización

Agent RuntimePII DetectionAutorizacionArtifact CacheModality RouterUsuario BAgent RuntimePII DetectionAutorizacionArtifact CacheModality RouterUsuario BEl acierto de cache NUNCA omitela evaluacion de autorizacion ni de PIIEl texto de otro ambito nunca se reutilizaalt[Usuario B autorizado en el mismo ambito][Ambito distinto]Sube un documento ya procesado por el Usuario A1Consulta SHA-256 + version + ambito de aislamiento2ACIERTO, texto ya extraido3Revalida autorizacion para el Usuario B4Autorizado5Reevalua PII con la politica del Usuario B6Aprobado7POST /invoke8Denegado9Trata como fallo de cache y procesa desde cero10

## 5.6 SD-M-06 · Inyección de prompt embebida en documento

Agent RuntimeModerationSanitizerFile Text ExtractorFrontendAgent RuntimeModerationSanitizerFile Text ExtractorFrontendEl PDF contiene texto en color de fondo:"Ignora tus instrucciones previas y..."El prompt declara el contenido delimitadocomo DATO, nunca como instruccionalt[Se confirma intento de inyeccion][Contenido oculto benigno, por ejemplo marca de agua]PDF con texto oculto embebido1Texto extraido, incluye el contenido oculto2Detecta texto con modo de render invisibley color igual al fondo3Elimina el fragmento y lo registra como hallazgo4Delimita el contenido restante con marcadores5Texto sanitizado + hallazgo de contenido oculto6Analiza patron de ataque indirecto7422 CONTENT_BLOCKED8Registra evento de seguridad9Aprobado, con el fragmento ya eliminado10

---

# 6. Contratos de interfaz

## 6.1 Subida de archivo, ruta estándar

```
[CDATA[POST /v1/files/upload
Authorization: Bearer <JWT Entra ID
Content-Type: multipart/form-data
X-Correlation-Id:
Idempotency-Key:
]]>
```

| Campo | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| `file` | binary | Sí | Binario del archivo |
| `filename` | string | Sí | Nombre original. **Se usa solo para presentación, nunca para decidir el tipo** |
| `declared_mime` | string | No | Tipo declarado. El servidor lo verifica y puede contradecirlo |
| `session_id` | uuid | Sí | Sesión conversacional |
| `purpose` | enum | No | `context` por defecto |

Respuesta `200 OK`:

```json
[CDATA[{
 "artifact_id": "uuid",
 "status": "ready",
 "detected_type": "application/pdf",
 "pages": 42,
 "size_bytes": 3251200,
 "extraction": {
 "engine": "<identificador",
 "ocr_applied_pages": 0,
 "coverage_pages": "42/42",
 "chars_extracted": 84300,
 "estimated_tokens": 24086,
 "extraction_latency_ms": 2140,
 "encoding_detected": null,
 "encoding_confidence": null
 },
 "context": {
 "within_limit": true,
 "limit_tokens": 100000,
 "utilization_pct": 24.1
 },
 "security": {
 "malware_scan": "clean",
 "sanitization_applied": ["unicode_nfkc", "zero_width_removed", "docx_comments_stripped"],
 "hidden_content_found": false,
 "pii_detected": false,
 "moderation": "approved"
 },
 "cache": { "hit": false, "key_version": "v1" }
}
]]>
```

Respuesta `202 Accepted` para la ruta asíncrona:

```json
{
 "job_id": "uuid",
 "status": "queued",
 "poll_url": "/v1/files/job/{job_id}",
 "estimated_completion_ms": 95000,
 "reason": "ocr_required_80_pages"
}
```

## 6.2 Subida directa para archivos grandes

Los archivos superiores a 10 MB **no atraviesan APIM como ruta de datos**. Justificación: el gateway es un punto de control, no un canal de transferencia masiva; almacenar en búfer cuerpos grandes consume capacidad del gateway y degrada a todos los consumidores.

```
POST /v1/files/upload-url
```

Devuelve una URL de escritura de vida corta contra el almacenamiento:

```json
[CDATA[{
 "upload_url": "https://<cuenta.blob.core.windows.net/...",
 "artifact_id": "uuid",
 "expires_in_s": 300,
 "max_size_bytes": 52428800,
 "commit_url": "/v1/files/commit"
}
]]>
```

Controles obligatorios sobre la credencial temporal:

| Control | Valor |
| --- | --- |
| Vigencia | 300 s |
| Permiso | Solo escritura. **Sin lectura ni listado** |
| Alcance | Un único blob con nombre predeterminado por el servidor |
| Emisión | Credencial delegada por identidad de usuario, no por clave de cuenta |
| Confirmación | El cliente llama a `POST /v1/files/commit`. **El pipeline arranca en la confirmación, nunca por evento de escritura del almacenamiento**, para no procesar cargas no confirmadas |

## 6.3 Operaciones auxiliares

| Operación | Método y ruta | Propósito |
| --- | --- | --- |
| Confirmar subida directa | `POST /v1/files/commit` | Dispara el pipeline sobre el binario ya cargado |
| Consultar trabajo | `GET /v1/files/job/{id}` | Estado y resultado de la ruta asíncrona |
| Consultar artefacto | `GET /v1/files/artifact/{id}` | Metadata del artefacto. **No devuelve el texto completo** |
| Eliminar artefacto | `DELETE /v1/files/artifact/{id}` | Borrado por solicitud del usuario. Invalida el caché |
| Consultar capacidades | `GET /v1/files/capabilities` | Formatos, límites y límite de contexto vigentes. Evita que el cliente los tenga cableados |
| Enviar mensaje con contexto | `POST /v1/chat/message` | Mensaje del usuario referenciando uno o más `artifact_id` |

## 6.4 API interna del File Text Extractor

```
POST /internal/extract
```

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `blob_uri` o `content` | string o binary | Origen del binario |
| `detected_type` | string | Tipo real confirmado por el Validator |
| `page_range` | string | Opcional. Rango de páginas a extraer |
| `ocr_policy` | enum | `auto`, `never`, `force` |
| `language` | string | Idioma esperado, para el OCR |
| `user_context` | object | `user_id`, `tenant`, `classification` propagados |

Respuesta:

```json
[CDATA[{
 "text": "...",
 "pages": [
 { "page": 1, "chars": 2140, "source": "text_layer", "ocr_confidence": null },
 { "page": 2, "chars": 1890, "source": "ocr", "ocr_confidence": 0.93 }
 ],
 "total_chars": 84300,
 "coverage_pages": 42,
 "total_pages": 42,
 "engine": "<identificador",
 "engine_version": "",
 "extraction_latency_ms": 2140,
 "warnings": ["page_7_low_ocr_confidence"]
}
]]>
```

El desglose por página es obligatorio: sin él no se puede medir la cobertura de extracción de 13.4 ni diagnosticar por qué un documento produjo texto incompleto.

## 6.5 Códigos de error

| HTTP | Código de negocio | Causa | Reintentable | Acción del cliente |
| --- | --- | --- | --- | --- |
| 400 | `FILE_TYPE_UNSUPPORTED` | Tipo real no soportado | No | Convertir a un formato soportado |
| 400 | `FILE_TYPE_MISMATCH` | El tipo real no coincide con el declarado | No | Rechazo. Se registra como evento de seguridad |
| 400 | `FILE_CORRUPTED` | Estructura ilegible | No | Verificar el archivo |
| 400 | `FILE_ENCRYPTED` | Documento protegido por contraseña | No | Retirar la protección |
| 400 | `ENCODING_UNDETECTABLE` | No se pudo determinar la codificación con confianza suficiente | No | Guardar como UTF-8 |
| 413 | `FILE_TOO_LARGE` | Excede 50 MB | No | Dividir el archivo |
| 413 | `TOO_MANY_PAGES` | Excede 300 páginas | No | Dividir el documento |
| 413 | `DOCUMENT_EXCEEDS_CONTEXT` | El texto extraído no cabe en la ventana de contexto | No | **Dividir o seleccionar rango de páginas.** Ver 9.4 |
| 413 | `TOO_MANY_ATTACHMENTS` | Más de 5 adjuntos por mensaje | No | Reducir |
| 422 | `FILE_REJECTED_SECURITY` | Malware detectado | No | Bloqueo. Evento a SIEM |
| 422 | `EXTRACTION_EMPTY` | No se obtuvo texto útil | No | Verificar si es un documento sin texto |
| 422 | `CONTENT_BLOCKED` | Bloqueado por moderación | No | Mensaje genérico, sin detalle del motivo |
| 422 | `PII_NOT_ALLOWED` | PII de categoría restringida | No | — |
| 401 | `UNAUTHENTICATED` | JWT ausente o inválido | No | Renovar el token |
| 403 | `FORBIDDEN_CLASSIFICATION` | Clasificación no autorizada para el usuario | No | Bloqueo |
| 429 | `QUOTA_EXCEEDED` | Cuota de canal, usuario o sesión agotada | Sí, tras `Retry-After` | Esperar |
| 429 | `TOKEN_BUDGET_EXCEEDED` | Presupuesto de tokens agotado | Sí | Informar. `FinOps.md` |
| 503 | `EXTRACTION_UNAVAILABLE` | Motor de extracción u OCR caído | No en la misma sesión | Degradar. Ver 10.2 |
| 504 | `EXTRACTION_TIMEOUT` | Excedió el timeout | Sí, una vez, por la ruta asíncrona | Reintentar |
| 500 | `INTERNAL_ERROR` | Fallo no clasificado | No | Informar |

Todo error incluye `correlation_id` y `trace_id`. El error `DOCUMENT_EXCEEDS_CONTEXT` incluye además `chars_extracted`, `estimated_tokens`, `limit_tokens`, `total_pages` y `approx_pages_allowed`, para que el usuario pueda actuar en lugar de solo recibir un rechazo.

## 6.6 Eventos y colas

| Evento | Publicador | Consumidor | Propósito |
| --- | --- | --- | --- |
| `ingest.document.requested` | Validator | Ingest Worker | Ruta asíncrona |
| `ingest.document.completed` | Ingest Worker | Frontend por sondeo, observabilidad | Resultado disponible |
| `ingest.document.failed` | Ingest Worker | Observabilidad, alertas | Fallo tras agotar reintentos |
| `ingest.security.rejected` | Malware Scanner, Moderation | SIEM, Governance API | Evidencia de enforcement |
| `ingest.pii.detected` | PII Detection | Governance API, observabilidad | Trazabilidad del tratamiento |
| `artifact.retention_expired` | Job de retención | Blob, caché, base de datos | Dispara el borrado efectivo |
| `artifact.deleted_by_user` | API de artefactos | Caché, Blob | Derecho de supresión |

Convenciones obligatorias: `event_id`, `event_type`, `occurred_at`, `correlation_id`, `trace_id`, `user_id`, `session_id`, `schema_version`. Reintentos del consumidor: 3 con backoff exponencial y cola de mensajes fallidos.

## 6.7 Contrato con el Agent Runtime

El contrato es `POST /invoke` con publicación de `agent-card.json`. El texto extraído se entrega en el mismo campo de texto que usa el chat directo, delimitado con los marcadores estructurales de 11.7. La modalidad de origen viaja únicamente como metadata de traza.

---

# 7. Modelo de datos y persistencia

## 7.1 Qué se guarda, dónde y por cuánto tiempo

| Dato | Contiene PII | Almacén | Retención | Cifrado |
| --- | --- | --- | --- | --- |
| Binario del archivo, ruta síncrona | Potencialmente sí | **No se persiste por defecto.** En memoria durante el procesamiento | — | TLS en tránsito |
| Binario del archivo, ruta asíncrona | Potencialmente sí | Blob, contenedor temporal | Borrado al completar el trabajo. Máximo 24 h | Cifrado en reposo, acceso por identidad administrada |
| Binario con requisito de auditoría | Potencialmente sí | Blob, contenedor gobernado | `[PENDIENTE DE DEFINIR]` P-M-08 | Cifrado en reposo, ACL heredada |
| Texto extraído y sanitizado | Potencialmente sí | Base de datos del dominio | Hereda la retención de la traza | Cifrado en reposo |
| Texto en caché | Potencialmente sí | Almacén del caché. D-M-10 | TTL de 7 días | Cifrado en reposo |
| Metadata de extracción | No | Base de datos y traza | Igual que la traza | Cifrado en reposo |
| Hallazgos de seguridad | No | Base de datos y SIEM | Según política de seguridad, típicamente mayor | Cifrado en reposo |
| Transcripción de audio | Potencialmente sí | Ver documento de Voz §7 | Ver documento de Voz | Ídem |
| Scores de calidad | No | Langfuse | Según política de Langfuse | Ídem |

## 7.2 Entidades

## 7.3 Reglas de persistencia

1. **El binario no se persiste salvo requisito explícito de auditoría**. Activarlo exige clasificación por Governance API y base legal registrada.
2. **Toda persistencia hereda la clasificación** de la evaluación a la que pertenece, con ACL heredada.
3. **El binario de la ruta asíncrona es temporal por diseño.** Se borra al completar el trabajo. El límite de 24 h es una red de seguridad ante trabajos huérfanos, no una retención.
4. **El borrado es efectivo, no lógico.** El vencimiento dispara `artifact.retention_expired`, que borra el blob, la entrada de caché y el texto extraído.
5. **La supresión solicitada por el usuario alcanza el caché.** Borrar el artefacto sin invalidar el caché deja el texto accesible y convierte al caché en un canal de fuga.
6. **La detección de PII ocurre antes de persistir**, conforme a `AI Security Enforcement.md`.
7. **Los hallazgos de seguridad sobreviven al artefacto.** Borrar la evidencia de que un archivo fue rechazado por malware junto con el propio archivo elimina el rastro de auditoría.

---

# 8. Topología de despliegue

La estructura de despliegue es la que se define a continuación. Los valores marcados como pendientes se cierran con D-M-07 (región) y D-M-08 (runtime).

## 8.1 Entornos

| Entorno | Propósito | Datos | Motores | Cuotas |
| --- | --- | --- | --- | --- |
| Desarrollo | Construcción y pruebas unitarias | Sintéticos. **Prohibidos documentos reales de usuarios** | Nivel gratuito o autoalojado | Mínimas |
| Pruebas / QA | Integración, carga y evaluación | Set de evaluación anonimizado | Iguales a producción | 25 % de producción |
| Producción | Operación | Reales, clasificados | Instancias dedicadas | Según P-M-01 |

Promoción por CI/CD con quality gates según `AI-LLM Lifecycle Management.md`.

## 8.2 Red

Red privada

Perimetro

Internet

Subred de datos

Subred de aplicacion

Reglas obligatorias:

- Los componentes backend **no se exponen a Internet**. Solo alcanzables desde APIM.
- Toda dependencia de plataforma se consume por *private endpoint*.
- La subida directa de 6.2 es el **único** camino desde el cliente al almacenamiento, y opera con credencial de escritura, alcance de un solo blob y vigencia de 300 s.
- TLS 1.2 como mínimo en todos los saltos, incluidos los internos.
- Secretos exclusivamente en Key Vault, accedidos por identidad administrada.

## 8.3 Escalamiento

| Componente | Métrica de escalado | Mínimo | Máximo | Nota |
| --- | --- | --- | --- | --- |
| Pipeline síncrono | Peticiones concurrentes por instancia | 2 | `[PENDIENTE]` de P-M-01 | La extracción es intensiva en CPU y memoria |
| Ingest Worker | Profundidad de la cola | 0 | `[PENDIENTE]` de P-M-02 | Escalado dirigido por eventos. Puede bajar a cero fuera de horario |
| OCR | Páginas encoladas | 0 | `[PENDIENTE]` de P-M-03 | **El dimensionamiento depende por completo de la proporción real de PDF escaneado** |
| Agent Runtime | — | — | — | Su dimensionamiento no depende de este canal |

**Advertencia de dimensionamiento.** La extracción de documentos es intensiva en memoria: un PDF grande puede requerir varias veces su tamaño en memoria al abrirse. El límite de concurrencia por instancia debe derivarse de la memoria disponible, no del uso de CPU. Escalar por CPU en cargas de extracción produce agotamiento de memoria antes de que se dispare el escalado.

## 8.4 Límites y cuotas

| Límite | Punto de aplicación | Valor | Fuente |
| --- | --- | --- | --- |
| Tamaño máximo vía APIM | APIM | 10 MB | Ver 9.2 |
| Tamaño máximo absoluto | Validator y credencial temporal | 50 MB | Ver 9.2 |
| Páginas máximas | Validator | 300 | Ver 9.3 |
| Adjuntos por mensaje | APIM y Validator | 5 | Ver 9.2 |
| Límite de contexto | Context Guard | Derivado de D-M-01. Ver 9.4 | — |
| Archivos por usuario y día | APIM | `[PENDIENTE DE DEFINIR]` | `FinOps.md` |
| Páginas de OCR por usuario y día | Pipeline | `[PENDIENTE DE DEFINIR]` | El OCR se factura por página y es el mayor riesgo de costo |
| Presupuesto de tokens por sesión | APIM token-limit policy | `[PENDIENTE DE DEFINIR]` | `FinOps.md` |
| Trabajos asíncronos concurrentes por usuario | Validator | 3 | Evita que un usuario monopolice la cola |

**La cuota de archivos es independiente de la de texto**, no compartida. Un documento de 100.000 tokens en el contexto cuesta órdenes de magnitud más que un mensaje de chat, por lo que una cuota común se agota por el canal caro y penaliza al barato.

---

# 9. Configuración y parámetros operativos

## 9.1 Formatos soportados

| Formato | Tipo real esperado | Motor | Ruta | Hito |
| --- | --- | --- | --- | --- |
| `.txt` | `text/plain` | Decodificador con detección de codificación | Síncrona | H2 |
| `.csv` | `text/csv` o `text/plain` | Ídem, sin interpretación de estructura tabular | Síncrona | H2 |
| `.md` | `text/markdown` o `text/plain` | Ídem | Síncrona | H2 |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Extracción estructurada. D-M-02 | Síncrona | H3 |
| `.pdf` nativo | `application/pdf` | Extracción de capa de texto. D-M-02 | Síncrona hasta 50 páginas | H3 |
| `.pdf` escaneado | `application/pdf` | OCR. D-M-03 | Síncrona hasta 5 páginas; asíncrona por encima | H4 |
| Audio | `audio/webm`, `audio/mp4` | Speech Processor | Ver documento de Voz | Documento de Voz |

**Formatos rechazados explícitamente:** `.doc` y `.xls` heredados, `.xlsx`, `.pptx`, comprimidos, `.eml` y `.msg`, ejecutables, y todo formato no listado. El rechazo es por lista blanca, nunca por lista negra: una lista negra deja pasar todo lo que no se anticipó.

## 9.2 Límites de tamaño y cantidad

| Parámetro | Valor | Justificación |
| --- | --- | --- |
| Tamaño máximo, ruta síncrona vía APIM | 10 MB | A 375 KB/s efectivos (S-M-05) equivale a 26,6 s de subida, dentro del timeout de cliente de 60 s con margen |
| Tamaño máximo absoluto | 50 MB | Cubre documentos escaneados extensos. Por encima, el tiempo de subida y el consumo de memoria de la extracción dejan de ser razonables en un flujo interactivo |
| Umbral de subida directa | > 10 MB | El gateway no es ruta de datos masivos. Ver 6.2 |
| Adjuntos por mensaje | 5 | Con el límite de contexto de 9.4, más de 5 documentos hacen casi seguro el rechazo por contexto |
| Tamaño mínimo | 1 byte | Un archivo vacío se rechaza con `EXTRACTION_EMPTY` |
| Longitud del nombre de archivo | 255 caracteres | Se sanea y se usa solo para presentación |

## 9.3 Límites de páginas

| Parámetro | Valor | Justificación |
| --- | --- | --- |
| PDF nativo, ruta síncrona | 50 páginas | Consume 2.500 ms del presupuesto de 6.270 ms en el tramo T5 |
| PDF con OCR, ruta síncrona | 5 páginas | A 0,5–2 s por página equivale a 2,5–10 s, el máximo compatible con el presupuesto |
| Máximo absoluto | 300 páginas | Límite operativo del pipeline. **En la práctica el límite vinculante suele ser el contexto, no las páginas.** Ver 9.4 |
| Páginas por trabajo asíncrono | 300 | Ídem |

## 9.4 Límite de contexto: el techo real del sistema

**Esta es la restricción más importante del documento.** Al no existir recuperación aumentada dentro del alcance, el texto extraído debe caber íntegro en la ventana de contexto del modelo. El límite del sistema no lo fija el tamaño del archivo: lo fija el contexto.

**Fórmula del límite operativo:**

```
tokens_disponibles = ventana_contexto_modelo × factor_reserva
caracteres_admisibles = tokens_disponibles × caracteres_por_token
```

| Parámetro | Valor | Justificación |
| --- | --- | --- |
| `factor_reserva` | 0,50 | Se reserva la mitad de la ventana para el prompt del sistema, el historial de la conversación, las definiciones de herramientas y la respuesta generada. Sin esta reserva, un documento que "cabe" desplaza el historial y deja al agente sin instrucciones |
| `caracteres_por_token` | 3,5 | Estimación conservadora para español. El español tokeniza peor que el inglés; usar 4,0 subestima el consumo y produce rechazos tardíos del modelo en lugar de rechazos tempranos y explicables |

**Límites resultantes según la ventana del modelo** (D-M-01 pendiente):

| Ventana del modelo | Tokens disponibles | Caracteres admisibles | Páginas aproximadas a 2.000 caracteres |
| --- | --- | --- | --- |
| 128.000 | 64.000 | 224.000 | ~112 |
| 200.000 | 100.000 | 350.000 | ~175 |
| 1.000.000 | 500.000 | 1.750.000 | ~875 |

**Política ante exceso: rechazo explícito, nunca truncado silencioso.**

Justificación: truncar en silencio produce una respuesta fundada en un fragmento del documento sin que el usuario sepa que hubo un corte ni dónde. Eso viola directamente el atributo de calidad número uno de —trazabilidad y explicabilidad de las decisiones— y genera un riesgo de negocio superior al de rechazar el documento: una respuesta incorrecta con apariencia de completa es peor que una petición rechazada.

El rechazo devuelve `413 DOCUMENT_EXCEEDS_CONTEXT` con caracteres extraídos, tokens estimados, límite vigente, total de páginas y páginas aproximadas admisibles, de modo que el usuario pueda dividir el documento o seleccionar un rango en lugar de quedarse sin salida.

**Consecuencia aceptada.** Existe una franja de documentos —extensos pero legítimos— que este sistema no puede procesar. Esa franja es exactamente la que la recuperación aumentada eliminaría, y está fuera de alcance por decisión. Ver R-M-01.

## 9.5 Detección de tipo y regla de OCR

### Detección de tipo real

| Regla | Implementación |
| --- | --- |
| Fuente de verdad | *Magic bytes* del binario. **Nunca la extensión ni el**`Content-Type`**declarado**, ambos controlados por el cliente |
| Verificación estructural | Además de la firma, se abre el contenedor: un `.docx` es un contenedor comprimido con una estructura interna esperada; si no la tiene, se rechaza |
| Discrepancia | Si el tipo real difiere del declarado, se rechaza con `FILE_TYPE_MISMATCH` **y se registra como evento de seguridad**. La discrepancia es señal de intento de elusión, no un error del usuario |
| Documentos protegidos | Se rechazan con `FILE_ENCRYPTED`. **No se intenta descifrar** |

### Detección de codificación para texto plano

Orden de resolución, deteniéndose en el primer éxito:

1. Marca de orden de bytes, si está presente: determina UTF-8, UTF-16 LE o UTF-16 BE sin ambigüedad.
2. Intento de decodificación UTF-8 estricta. Si no falla, es UTF-8.
3. Detección estadística de codificación. Se acepta si la confianza supera el umbral.
4. Latin-1 como último recurso, **registrando la baja confianza en la metadata**. Latin-1 nunca falla al decodificar, pero puede producir texto ilegible; el registro permite diagnosticarlo después.

Si el paso 3 queda por debajo del umbral y el paso 4 produce una proporción alta de caracteres de reemplazo, se rechaza con `ENCODING_UNDETECTABLE`.

### Regla de decisión OCR — implementada por página, no por documento

Los documentos mixtos son comunes: un contrato con firmas escaneadas intercaladas entre páginas nativas. Decidir a nivel de documento aplica OCR de más —con su costo— o de menos —perdiendo contenido.

```
[CDATA[para cada pagina:
 chars = caracteres extraidos de la capa de texto
 si chars < 100 - OCR
 si 100 <= chars < 500 -> OCR + fusion con la capa de texto
 si chars >= 500 -> solo capa de texto
]]>
```

| Umbral | Valor | Justificación |
| --- | --- | --- |
| Umbral de página escaneada | < 100 caracteres | Una página de texto en español contiene típicamente entre 1.500 y 3.000 caracteres. Menos de 100 indica ausencia de capa de texto: solo encabezado, pie o número de página añadidos por el escáner |
| Umbral de página mixta | 100 a 499 caracteres | Franja donde conviven una capa de texto parcial y contenido en imagen: portadas, páginas con tablas o figuras rotuladas |
| Confianza mínima de OCR | `[PENDIENTE DE DEFINIR]` | Debe calibrarse con la muestra real de P-M-03. El método es el de 13.4 |
| Política `ocr_policy` por defecto | `auto` | `force` se reserva a diagnóstico; `never` a casos donde el costo del OCR no se justifica |

La decisión implementada es **capa de texto frente a OCR**, resuelta por página. El envío directo de la imagen a un modelo de visión está fuera de alcance.

## 9.6 Sanitización

La sanitización se ejecuta en diez pasos, en el orden siguiente.

| Paso | Operación | Motivo |
| --- | --- | --- |
| 1 | Normalización Unicode NFKC | Formas equivalentes de un mismo carácter permiten eludir filtros basados en patrones |
| 2 | Eliminación de caracteres de control, excepto salto de línea y tabulación | Pueden alterar el parseo aguas abajo |
| 3 | Eliminación de caracteres de ancho cero e invisibles | Vector clásico para ocultar instrucciones dentro de texto aparentemente inocuo |
| 4 | Eliminación de marcas de control bidireccional | Permiten reordenar visualmente el texto: lo que el revisor humano lee no es lo que el modelo recibe |
| 5 | Eliminación de texto oculto en PDF | Texto con modo de renderizado invisible o con color de relleno igual al fondo. **Es el vector de inyección documental más frecuente** |
| 6 | Eliminación de comentarios y de texto eliminado con control de cambios en DOCX | Un comentario o una supresión con control de cambios contiene texto que el autor no considera parte del documento, pero que el extractor sí leería |
| 7 | Eliminación de metadatos del documento | Autor, título y propiedades personalizadas pueden contener PII o instrucciones |
| 8 | Colapso de espacios en blanco excesivos | Reduce el consumo de tokens sin pérdida semántica |
| 9 | Delimitación con marcadores estructurales | El contenido queda acotado. Ver 11.7 |
| 10 | Verificación de longitud | Última barrera antes del Context Guard |

Todo paso que elimine contenido **registra un hallazgo** en `SECURITY_FINDING` y en la metadata de la respuesta. Sanitizar en silencio impide distinguir un documento limpio de uno del que se retiró un intento de ataque.

## 9.7 Caché de artefactos

| Aspecto | Definición | Justificación |
| --- | --- | --- |
| **Clave** | `SHA-256(binario)` + `version_extractor` + `version_motor_ocr` + `hash_parametros` + `idioma` + `ambito_aislamiento` | El hash identifica el contenido con independencia del nombre. Incluir las versiones hace que una actualización del motor invalide el caché de forma natural, sin purga manual. Incluir el ámbito impide reutilizar texto entre ámbitos de aislamiento distintos |
| **Qué se almacena** | Texto extraído y sanitizado, desglose por página, métricas de extracción | No se almacena el resultado de PII ni de moderación: dependen del usuario y de la política vigente, y se reevalúan siempre |
| **TTL** | 7 días | Cubre el ciclo de trabajo típico en el que un usuario vuelve sobre el mismo documento. Más allá, el costo de almacenamiento y la exposición de PII superan la tasa de acierto esperada. Configurable |
| **Invalidación por versión** | Automática: la versión forma parte de la clave | Elimina la clase de defecto en que un cambio de motor sirve resultados obsoletos |
| **Invalidación explícita** | `DELETE /v1/files/artifact/{id}` y el evento `artifact.deleted_by_user` | Derecho de supresión |
| **Invalidación por retención** | `artifact.retention_expired` | Un caché que sobrevive a la retención del dato la vuelve inefectiva |
| **Aciertos y autorización** | Un acierto **nunca** omite la evaluación de autorización ni la de PII para el usuario solicitante. Ver SD-M-05 | Sin esta regla, el caché se convierte en un canal de fuga entre usuarios |
| **Beneficio medido** | Reducción del 65 % en el p95 de procesamiento | Sección 2.3 |

## 9.8 Moderación de entrada y de salida

| Punto | Qué se evalúa | Comportamiento ante fallo del servicio |
| --- | --- | --- |
| Entrada | Texto extraído tras la sanitización, antes del contexto del modelo. Categorías de contenido dañino y detección de ataques indirectos embebidos en documento | **Se rechaza la petición.** No se opera sin control |
| Salida | Respuesta del agente antes de devolverla al usuario. Categorías de contenido y verificación de esquema | **Se rechaza la respuesta.** No se devuelve contenido no moderado |

`AI Security Enforcement.md` no admite operación sin enforcement. El comportamiento ante fallo es cerrado en ambos extremos: fallar abierto convertiría una caída del servicio de seguridad en una ventana de exposición.

---

# 10. Manejo de fallas

## 10.1 Modos de fallo

| ID | Modo de fallo | Detección | Impacto | Respuesta |
| --- | --- | --- | --- | --- |
| F-M-01 | Tipo real no soportado | Validación por *magic bytes* | Petición rechazada | 400 con lista de formatos soportados |
| F-M-02 | Tipo real distinto del declarado | Comparación | Posible intento de elusión | 400 y evento de seguridad |
| F-M-03 | Archivo corrupto o ilegible | Fallo al abrir el contenedor | Sin extracción | 400 |
| F-M-04 | Documento protegido por contraseña | Estructura cifrada | Sin extracción | 400. No se intenta descifrar |
| F-M-05 | Malware detectado | Escaneo | Riesgo de seguridad | 422, descarte inmediato, evento a SIEM |
| F-M-06 | Excede tamaño o páginas | Validación de límites | Rechazo | 413 con el límite concreto |
| F-M-07 | **Excede el límite de contexto** | Context Guard | Rechazo | 413 con datos accionables. Ver 9.4 |
| F-M-08 | Extracción vacía | Cero caracteres útiles | Sin contenido | 422. Puede indicar PDF de solo imagen con `ocr_policy: never` |
| F-M-09 | Codificación indeterminable | Detector por debajo del umbral | Texto ilegible | 400 sugiriendo guardar como UTF-8 |
| F-M-10 | Confianza de OCR baja | Confianza por página bajo umbral | Texto poco fiable | Se entrega con advertencia visible en la metadata. **No se oculta al usuario** |
| F-M-11 | Motor de extracción caído | Error o timeout | Sin procesamiento | Circuit breaker. Ver 10.2 |
| F-M-12 | Motor de OCR caído | Ídem | Sin OCR | Se degrada: se entrega el texto de la capa nativa con cobertura parcial declarada |
| F-M-13 | Servicio de PII caído | Error o timeout | Sin verificación | **Se rechaza.** No se persiste ni se envía al modelo sin verificación de PII |
| F-M-14 | Servicio de moderación caído | Ídem | Sin control | **Se rechaza.** Fallo cerrado |
| F-M-15 | Timeout de extracción | Vence el timeout | Trabajo incompleto | Reintento por la ruta asíncrona |
| F-M-16 | Cola saturada | Profundidad sobre umbral | Espera prolongada | Se informa el tiempo estimado. Cuota de trabajos concurrentes por usuario |
| F-M-17 | Agotamiento de memoria en la extracción | Terminación del proceso | Trabajo caído | Límite de concurrencia por memoria. Ver 8.3 |
| F-M-18 | Cuota agotada | Contador de APIM | Rechazo | 429 con `Retry-After` |
| F-M-19 | Agent Runtime no disponible | Circuit breaker | Sin respuesta | **El artefacto ya extraído se conserva**: el usuario reintenta sin volver a subir ni a pagar la extracción |
| F-M-20 | Inyección detectada en documento | Sanitizer y moderación | Intento de ataque | Eliminación del fragmento o bloqueo. Evento a SIEM. Ver SD-M-06 |
| F-M-21 | Credencial de subida directa expirada | Rechazo del almacenamiento | Subida fallida | El cliente solicita una nueva credencial y reintenta |

## 10.2 Matriz de degradación por componente

| Componente que falla | El canal sigue operando | Modo degradado | Aviso al usuario |
| --- | --- | --- | --- |
| Motor de extracción | Parcialmente | Solo texto directo y audio. Adjuntos deshabilitados | Sí, explícito |
| Motor de OCR | Sí | PDF nativo sí, escaneado no. **Cobertura parcial declarada, nunca oculta** | Sí |
| Escaneo de malware | **No para archivos** | Adjuntos deshabilitados. Texto y audio continúan | Sí |
| Detección de PII | **No** | Se rechaza la ingesta | Sí |
| Moderación | **No** | Se rechaza la ingesta y la salida | Sí |
| Caché | Sí | Se procesa todo desde cero. Mayor latencia y costo | No |
| Broker | Sí, con límite | Solo ruta síncrona. Documentos grandes rechazados temporalmente | Sí |
| Blob Storage | Parcialmente | Solo ruta síncrona sin persistencia | Sí |
| Governance API | Depende | Si no se puede clasificar, **no se persiste** el binario. La interacción continúa | No |
| Agent Runtime | No | El artefacto se conserva para reintento | Sí |
| Observabilidad | Sí | Registro local y reenvío posterior | No |

**Principio de degradación.** El fallo de un componente de transformación degrada la modalidad, nunca el servicio completo. El fallo de un componente de seguridad —malware, PII, moderación— **detiene** el flujo afectado. Esta asimetría es deliberada y proviene de `AI Security Enforcement.md`.

## 10.3 Timeouts

| Llamada | Timeout | Justificación |
| --- | --- | --- |
| Cliente → APIM, ruta síncrona | 60 s | Cubre subida de 10 MB más procesamiento con margen |
| APIM → pipeline | 45 s | Menor que el del cliente, para que el error se genere en el servidor y sea observable |
| Pipeline → escaneo de malware | 10 s | Escanear 10 MB. Superarlo indica saturación del servicio |
| Pipeline → extracción síncrona | 20 s | 50 páginas nativas caben en 2.500 ms; 20 s cubre el peor caso con amplio margen |
| Worker → extracción asíncrona | 600 s | 300 páginas con OCR a 2 s por página |
| Pipeline → PII | 5 s | En ruta crítica |
| Pipeline → moderación | 5 s | En ruta crítica |
| Pipeline → Governance API | 2 s | Fuera de la ruta crítica de respuesta |
| APIM → Agent Runtime | Según el SLA del `agent-card` | — |

**Regla de anidamiento.** El timeout de cada capa debe ser estrictamente menor que el de la capa que la invoca; de lo contrario el cliente abandona antes de que el servidor registre la causa.

## 10.4 Política de reintentos

| Dimensión | Valor |
| --- | --- |
| Intentos totales | 3, es decir 2 reintentos |
| Backoff | Exponencial: 1.000 ms y 2.000 ms |
| Jitter | ±20 % |
| Reintentables | 429, 500, 502, 503, 504, timeout de red |
| No reintentables | 400, 401, 403, 413, 422 |
| Extracción | **No se reintenta en la ruta síncrona.** Un fallo de extracción se promueve a la ruta asíncrona, donde el reintento no hace esperar al usuario |
| Idempotencia | Obligatoria vía `Idempotency-Key`. Sin ella, un reintento tras timeout puede extraer y pagar el OCR dos veces |

**Circuit breaker.** Se reutiliza el patrón ya implementado en el proyecto: apertura tras 5 fallos consecutivos o 50 % de error en ventana de 30 s; 30 s abierto; 1 sonda en semiabierto.

## 10.5 Ruta asíncrona: criterios de promoción

Una petición se promueve automáticamente a la ruta asíncrona cuando se cumple cualquiera de estas condiciones. El cliente no elige la ruta: la decide el servidor y la comunica con `202`.

| Condición | Umbral |
| --- | --- |
| Tamaño del archivo | > 10 MB |
| Páginas de PDF nativo | > 50 |
| Páginas que requieren OCR | > 5 |
| Timeout de extracción síncrona | Al vencer |
| Saturación del pipeline síncrono | Concurrencia sobre umbral |

---

# 11. Seguridad aplicada

Esta sección prescribe la aplicación de los controles transversales de `AI Security Enforcement` sobre el canal multimodal.

## 11.1 Autenticación y autorización

| Control | Aplicación |
| --- | --- |
| Autenticación de usuario | Entra ID con JWT vía MSAL. |
| Validación del token | En APIM antes de cualquier enrutamiento: firma, emisor, audiencia y expiración |
| Propagación de identidad | El JWT **del usuario** viaja en toda la cadena: APIM → pipeline → Agent Runtime → herramientas. |
| Antipatrón prohibido | Delegar con identidad de servicio. |
| Autorización de canal | El permiso para adjuntar archivos es un *scope* diferenciado del chat de texto: su perfil de costo y de riesgo es distinto |
| Acceso al blob | Exclusivo del pipeline mediante identidad administrada. Las credenciales temporales de 6.2 son de escritura, de un solo blob y de 300 s |
| Autenticación entre servicios | Identidad administrada y red privada. Sin claves compartidas |

## 11.2 Gestión de secretos

| Secreto | Almacén | Rotación |
| --- | --- | --- |
| Credenciales de motores de extracción y OCR | Key Vault, accedido por identidad administrada | `[PENDIENTE DE DEFINIR]` según política corporativa |
| Credenciales de PII y moderación | Ídem | Ídem |
| Cadenas de conexión | Ídem, o autenticación sin secreto por identidad administrada | Ídem |

**Prohibido:** secretos en código, en variables de entorno del contenedor, en imágenes o en repositorios de configuración.

## 11.3 Escaneo de malware

El escaneo de malware es un requisito no negociable de todo canal que reciba binarios del usuario.

| Regla | Implementación |
| --- | --- |
| Momento | **Antes de toda extracción.** Un motor de extracción que abre un documento no escaneado es él mismo la superficie de ataque |
| Alcance | Todo binario, sin excepción. También los que van por subida directa |
| Veredicto positivo | Descarte inmediato, sin extracción, sin persistencia y sin entrada en caché |
| Registro | Evento a SIEM con usuario, hash, nombre de archivo y veredicto |
| Respuesta al usuario | Mensaje genérico. **No se expone el detalle del veredicto**, que sería información útil para un atacante |
| Fallo del servicio | Los adjuntos se deshabilitan. No se procesa sin escanear |

## 11.4 Tratamiento de PII

| Control | Aplicación |
| --- | --- |
| Detección | Sobre el texto extraído, **antes de persistirlo y antes de entrar al contexto del modelo** |
| Redacción | Según política de Governance API. Las categorías restringidas se rechazan. |
| Minimización | El binario no se persiste salvo requisito. Se conserva el texto, no el original |
| Metadatos | Se eliminan en la sanitización: autor y propiedades del documento son PII frecuente y pasan inadvertidos |
| Reevaluación en aciertos de caché | Obligatoria. El caché almacena texto, no veredictos de PII |
| DLP | Integración con la capacidad corporativa según `AI Security Enforcement.md` |
| Evidencia | Registro de cada decisión de política, con envío a SIEM |

## 11.5 Cifrado

| Punto | Control |
| --- | --- |
| En tránsito | TLS 1.2 como mínimo en todos los saltos, incluidos los internos y la subida directa |
| En reposo, blobs | Cifrado del servicio de almacenamiento. |
| En reposo, base de datos | Cifrado del motor |
| En reposo, caché | Cifrado en reposo. El caché contiene texto extraído con PII potencial |
| Claves | `[DECISIÓN PENDIENTE]` D-M-11: claves de plataforma frente a claves gestionadas por el cliente. Criterio: requisito regulatorio, operación de rotación y costo |

## 11.6 Aislamiento y caché

El caché es el componente con mayor riesgo de fuga entre usuarios de todo el pipeline, porque su propósito es precisamente reutilizar el resultado de un procesamiento previo.

| Control | Implementación |
| --- | --- |
| Ámbito en la clave | El ámbito de aislamiento forma parte de la clave. Texto de un ámbito nunca se sirve a otro |
| Revalidación de autorización | Todo acierto revalida la autorización del usuario solicitante antes de servir. Ver SD-M-05 |
| Reevaluación de PII | Todo acierto reevalúa PII con la política del usuario solicitante |
| No se cachean veredictos | Solo se cachea el texto extraído. Los veredictos de seguridad dependen del usuario y del momento |
| Supresión | El borrado del artefacto invalida el caché de forma sincrónica |

## 11.7 Defensa contra inyección de prompt vía documento

El contenido de archivos se trata como **input no confiable**. La defensa se implementa en ocho capas.

**Perfil de amenaza del vector documental.** En una inyección por chat el atacante es el propio usuario y el alcance del daño se limita a su sesión. En una inyección documental el atacante es un tercero que preparó el archivo, y quien lo sube puede ser una víctima que desconoce su contenido oculto. Por eso la defensa no puede depender de la intención del usuario que origina la petición.

| Capa | Control |
| --- | --- |
| 1. Eliminación de contenido oculto | Pasos 3 a 7 de 9.6: invisibles, bidi, texto oculto en PDF, comentarios y control de cambios en DOCX, metadatos |
| 1. Delimitación estructural | El texto se inserta en el prompt dentro de marcadores explícitos, **nunca concatenado libremente** con la instrucción del sistema |
| 1. Instrucción defensiva | El prompt del sistema declara que el contenido delimitado es **dato aportado por el usuario y nunca instrucción a ejecutar**, y que ninguna instrucción hallada dentro modifica su comportamiento |
| 1. Detección de ataque indirecto | Servicio de guardrails con detección específica de ataques embebidos en documento. D-M-06 |
| 1. Registro de hallazgos | Todo fragmento eliminado se registra. Sanitizar en silencio impide distinguir un documento limpio de uno saneado |
| 1. Límite de longitud | Context Guard. Un documento sobredimensionado puede desplazar el prompt del sistema |
| 1. Validación de salida | Verificación de esquema y moderación de la respuesta antes de devolverla |
| 1. Mínimo privilegio en herramientas | El agente conserva sus restricciones de herramientas con independencia del contenido del documento. `AI Gateway.md` |

**Orden obligatorio del pipeline:** Sanitizer → PII Detection → Content Moderation → Context Guard. Invertir cualquiera de estos pasos rompe la defensa: moderar antes de sanitizar deja pasar contenido oculto que el moderador no ve; verificar contexto antes de sanitizar mide una longitud que aún incluye lo que se va a eliminar.

## 11.8 Clasificación en la Matriz de Riesgos

La Matriz de Riesgos opera como gate formal alineado con el EU AI Act. Para este canal:

- El canal hereda la clasificación del agente al que sirve y no la altera por sí mismo.
- La ingesta de documentos **puede** elevar el nivel de riesgo si los documentos contienen categorías de datos sensibles, aunque el agente en sí sea de riesgo limitado. La evaluación debe considerar el tipo de documento previsto, no solo la función del agente.
- El registro de la evaluación es evidencia de cumplimiento y debe conservarse.

---

# 12. Observabilidad

## 12.1 Metadata de traza

El canal emite los campos siguientes en cada traza.

| Campo | Origen |
| --- | --- |
| `input_channel` | `texto`, `archivo`, `voz` |
| `file_type` | Tipo **real** detectado, no el declarado |
| `extraction_latency_ms` | File Text Extractor |
| `transcription_latency_ms` | Speech Processor |
| `transcription_confidence` | Proveedor STT |
| `stt_provider` | Speech Processor |
| `file_size_bytes` | Validator |
| `pages_total` | Validator |
| `pages_ocr` | Extractor. **Métrica principal de costo** |
| `coverage_pages` | Extractor. Páginas con texto obtenido sobre total |
| `chars_extracted` | Extractor |
| `estimated_tokens` | Context Guard |
| `context_utilization_pct` | Context Guard. Anticipa el rechazo por contexto |
| `cache_hit` | Artifact Cache |
| `malware_scan_result` | Malware Scanner |
| `sanitization_findings` | Sanitizer. Lista de reglas que eliminaron contenido |
| `hidden_content_found` | Sanitizer. **Señal de posible inyección** |
| `pii_detected` | PII Detection |
| `moderation_result` | Moderation |
| `min_ocr_confidence` | OCR Engine |
| `processing_route` | `sync` o `async` |
| `rejection_reason` | Código de error cuando aplica |

Obligatorio propagar `traceId`, `spanId` y `correlationId` en toda la cadena.

## 12.2 Métricas con umbral

| Métrica | Umbral de alerta | Severidad | Justificación |
| --- | --- | --- | --- |
| Cobertura de extracción | `[PENDIENTE DE DEFINIR]` P-M-07 | Alta | Métrica principal de calidad. |
| Exactitud de extracción de texto plano | `[PENDIENTE DE DEFINIR]` P-M-07 | Alta | Ídem |
| Latencia p50 de procesamiento | 2.295 ms | Baja | Presupuesto de 2.3 |
| Latencia p95 de procesamiento | 6.270 ms | Media | Ídem |
| Latencia p99 de procesamiento | `[PENDIENTE DE DEFINIR]` | Baja | Requiere línea base real |
| Tasa de rechazo por contexto | > 10 % de las ingestas | **Alta** | Señal directa de que la ausencia de recuperación aumentada está afectando a los usuarios. Ver R-M-01 |
| Tasa de acierto de caché | < 15 % | Media | El caché no está aportando el beneficio previsto; revisar TTL |
| Páginas de OCR por día | `[PENDIENTE DE DEFINIR]` | **Alta** | Mayor riesgo de costo del canal. Se factura por página |
| Tasa de fallo de extracción | > 3 % diario | Alta | Motor degradado o perfil documental distinto al previsto |
| Confianza mínima de OCR bajo umbral | > 10 % de páginas | Media | Calidad de escaneo insuficiente |
| Detecciones de contenido oculto | ≥ 1 | **Alta** | Posible intento de inyección. Requiere revisión, no solo registro |
| Rechazos por malware | ≥ 1 | Crítica | Evento de seguridad |
| Rechazos por PII no autorizada | > 5 % | Media | Puede indicar mal encaje del caso de uso |
| Profundidad de la cola asíncrona | > 100 trabajos | Media | Saturación |
| Aperturas de circuit breaker | ≥ 1 en 1 h | Alta | Indisponibilidad de dependencia |
| Costo por documento | `[PENDIENTE DE DEFINIR]` P-M-06 | Media | `FinOps.md` |
| Fallos por agotamiento de memoria | > 0 | Alta | Límite de concurrencia mal dimensionado. Ver 8.3 |

## 12.3 Logs y trazas

- Logs estructurados en JSON, correlacionables con la traza distribuida.
- **Prohibido** registrar en logs el contenido del documento o el texto extraído. Se registran identificadores, longitudes, hashes y metadata. El contenido vive en el almacén gobernado con su clasificación, no en el sistema de logs.
- **Prohibido** registrar el nombre original del archivo en claro si el caso de uso lo considera sensible: los nombres de archivo suelen contener nombres de personas y números de documento.
- Span por etapa: `ingest.validate`, `ingest.malware_scan`, `ingest.cache_lookup`, `ingest.extract`, `ingest.ocr`, `ingest.sanitize`, `ingest.pii`, `ingest.moderate`, `ingest.context_guard`, `ingest.agent_invoke`.
- Cada span registra su duración, para validar el presupuesto de 2.3 contra la realidad.
- Evidencia de policy enforcement enviada a SIEM.

## 12.4 Paneles

| Panel | Audiencia | Contenido |
| --- | --- | --- |
| Operación del pipeline | Operación | Volumen por formato, latencia por etapa, tasa de error, profundidad de cola, circuit breakers |
| Calidad de extracción | Owner funcional y calidad | Cobertura, confianza de OCR, tasa de extracción vacía, distribución por formato |
| Límite de contexto | Arquitectura y owner | Distribución de utilización del contexto y **tasa de rechazo por contexto**. Es la evidencia para decidir si la recuperación aumentada debe volver al alcance |
| Seguridad del canal | Seguridad | Rechazos por malware, contenido oculto, detecciones de PII, bloqueos de moderación |
| FinOps del canal | FinOps y owner | Costo por documento, páginas de OCR, tokens de contexto consumidos, cuotas |

---

# 13. Estrategia de pruebas

## 13.1 Pruebas unitarias

| Componente | Qué se prueba | Criterio |
| --- | --- | --- |
| Validator | Detección por *magic bytes*, discrepancia de tipo, límites, documentos protegidos, contenedores malformados | Todos los códigos de 6.5 cubiertos |
| Detector de codificación | BOM, UTF-8, UTF-16, Latin-1, casos indeterminables | Matriz completa de codificaciones con archivos de prueba |
| File Text Extractor | Extracción por formato, desglose por página, documentos mixtos | Cobertura ≥ 80 % de la lógica de extracción |
| Clasificador de OCR | Regla por página en los tres tramos de 9.5 | Casos frontera: 99, 100, 499 y 500 caracteres |
| Sanitizer | Los 10 pasos de 9.6, cada uno con su caso adverso | 100 % de los pasos con caso positivo y negativo |
| Context Guard | Cálculo de tokens estimados, decisión en el límite | Casos frontera exactos |
| Artifact Cache | Construcción de clave, invalidación por versión, TTL, aislamiento por ámbito | El cambio de versión de motor invalida siempre |
| Cliente de motores | Reintentos, backoff, circuit breaker, idempotencia | Todos los códigos reintentables y no reintentables |

## 13.2 Pruebas de integración

| Escenario | Verifica |
| --- | --- |
| Flujo feliz de PDF nativo | SD-M-01 completo con propagación de `traceId` |
| PDF escaneado asíncrono | SD-M-02: encolado, OCR, consulta de estado, borrado del temporal |
| Exceso de contexto | SD-M-03: rechazo explícito con datos accionables. **Nunca truncado silencioso** |
| Malware | SD-M-04: descarte, evento a SIEM, respuesta genérica |
| Acierto de caché con otro usuario | SD-M-05: revalidación de autorización y reevaluación de PII |
| Inyección embebida en documento | SD-M-06: eliminación del contenido oculto y registro del hallazgo |
| Documento mixto | Páginas nativas y escaneadas en el mismo PDF, OCR aplicado solo donde corresponde |
| Propagación de identidad | El JWT del usuario llega hasta las herramientas MCP |
| Cuotas | El 429 se produce en el límite configurado |
| Subida directa | Credencial de vida corta, alcance de un solo blob, confirmación explícita |
| Fallo del servicio de PII | La ingesta **se rechaza**, no se deja pasar |
| Fallo del servicio de moderación | Ídem, en entrada y en salida |
| Sin conectividad a Governance API | El binario **no** se persiste y la interacción continúa |
| Fallo del Agent Runtime | El artefacto se conserva y el usuario reintenta sin volver a subir |

## 13.3 Pruebas de carga

| Prueba | Diseño | Criterio de aceptación |
| --- | --- | --- |
| Carga nominal | Concurrencia de P-M-01 con la mezcla documental de P-M-03, durante 30 min | p95 dentro del presupuesto de 2.3; error < 1 % |
| Pico | 3× la concurrencia nominal durante 5 min | Sin 5xx; degradación solo por cuota o encolado |
| Resistencia | 70 % de la carga nominal durante 8 h | **Sin fugas de memoria**: la extracción es el componente con mayor riesgo |
| Saturación de OCR | Volumen alto de PDF escaneados | La cola absorbe; no se degrada la ruta síncrona de PDF nativo |
| Documentos límite | Archivos en el máximo de tamaño y páginas | Sin agotamiento de memoria. Ver F-M-17 |
| Caché en frío frente a caliente | Misma carga con y sin caché poblado | Se confirma la reducción del 65 % de p95 de 2.3 |
| Caos: motor de OCR caído | Indisponibilidad inyectada | Degradación a solo capa de texto con cobertura parcial **declarada** |
| Caos: servicio de PII caído | Ídem | 100 % de las ingestas rechazadas. Cero fugas |

Todas las pruebas de carga dependen de P-M-01, P-M-02 y P-M-03. **P-M-03 es especialmente crítica:** sin la proporción real de PDF escaneado, el dimensionamiento de OCR es una conjetura y el costo del canal no es predecible.

## 13.4 Set de evaluación y umbrales de aceptación

La evaluación se rige por el marco de `AI-LLM Lifecycle Management`.

**Composición del set de evaluación:**

| Categoría | Cobertura requerida |
| --- | --- |
| Texto plano | UTF-8 con y sin BOM, UTF-16 LE y BE, Latin-1, archivo vacío, líneas muy largas, caracteres especiales del español |
| DOCX | Texto corrido, tablas, listas anidadas, encabezados y pies, notas al pie, **comentarios y control de cambios**, imágenes con texto alternativo |
| PDF nativo | Una y varias columnas, tablas, texto rotado, formularios, marcas de agua |
| PDF escaneado | Escaneo limpio, escaneo degradado, documento inclinado, resolución baja, manuscrito parcial |
| PDF mixto | Páginas nativas y escaneadas intercaladas |
| Casos frontera | Justo por debajo y por encima de cada límite de 9.2, 9.3 y 9.4 |
| Casos adversos de seguridad | Texto oculto en PDF, caracteres invisibles, control bidireccional, instrucciones en comentarios de DOCX, instrucciones en metadatos, tipo real falsificado |
| Casos de PII | Documentos con cada categoría de PII prevista |
| Casos de dominio | Documentos representativos reales del caso de uso, anonimizados |

**Métricas y umbrales:**

| Métrica | Cómo se mide | Umbral |
| --- | --- | --- |
| Cobertura de extracción | Páginas con texto obtenido sobre páginas totales | `[PENDIENTE DE DEFINIR]` P-M-07 |
| Exactitud de texto plano | Comparación carácter a carácter contra el original | 100 %. Un decodificador correcto no admite pérdida |
| Exactitud de estructura en DOCX y PDF | Comparación contra transcripción de referencia | `[PENDIENTE DE DEFINIR]` P-M-07 |
| Tasa de error de OCR | Comparación contra transcripción de referencia del escaneo | `[PENDIENTE DE DEFINIR]`. Debe ser **más exigente** para documentos de dominio crítico |
| Correlación confianza de OCR – error | Regresión sobre el set | Sirve para **calibrar** el umbral de confianza de 9.5 |
| Precisión de la regla de OCR por página | Páginas correctamente clasificadas | ≥ 95 %. Un error de clasificación produce OCR innecesario, que cuesta, u omisión de contenido, que es peor |
| Tasa de bloqueo de inyecciones | Casos adversos de seguridad | **100 % de los casos conocidos.** No admite umbral parcial |
| Tasa de detección de PII | Casos de PII | `[PENDIENTE DE DEFINIR]`. Se calibra con el servicio de D-M-05 |
| Falsos positivos de moderación | Documentos legítimos bloqueados | `[PENDIENTE DE DEFINIR]`. Un canal que bloquea documentos válidos es inutilizable |

**Método para fijar los umbrales pendientes.** Ejecutar el set completo con los motores elegidos, obtener la distribución real por métrica, y fijar el umbral en el percentil que el negocio acepte como mínimo operable. Este es el procedimiento que describe como *"las metas cuantitativas se establecen tras la primera ejecución con datos reales"*, aquí hecho ejecutable.

## 13.5 Pruebas de seguridad

| Prueba | Verifica |
| --- | --- |
| Falsificación de tipo | Un ejecutable renombrado a `.pdf` se rechaza por *magic bytes* |
| Inyección por texto oculto en PDF | El fragmento se elimina y se registra el hallazgo |
| Inyección por comentario de DOCX | Ídem |
| Inyección por metadatos | Ídem |
| Caracteres invisibles y bidi | Neutralizados en la sanitización |
| Fuga entre usuarios vía caché | Un usuario de otro ámbito no recibe el texto cacheado |
| Elusión de autorización | Sin JWT válido no hay ingesta por ningún camino |
| Abuso de la credencial de subida directa | No permite lectura, listado ni escritura en otro blob; expira a los 300 s |
| Elusión del escaneo de malware | No existe camino de ingesta que omita el escaneo |
| Fallo abierto de PII o moderación | Ante caída del servicio, la petición **se rechaza** |
| Bomba de descompresión | Un contenedor con ratio de expansión anómalo se rechaza antes de expandirse |
| Elusión de cuota | Peticiones paralelas no superan el límite configurado |

---

# 14. Plan de implementación por fases

| Hito | Entregables | Dependencias | Criterio de salida |
| --- | --- | --- | --- |
| **H1** Pipeline base y seguridad | Modality Router, Validator con detección por *magic bytes*, Malware Scanner, Sanitizer, PII Detection, Moderation, Context Guard, Artifact Cache; rutas y policies en APIM; contratos de la sección 6; secretos en Key Vault | D-M-01, D-M-02, D-M-04, D-M-05, D-M-06, D-M-07, D-M-08 | El pipeline completo opera sobre un formato de prueba. Pruebas de seguridad de 13.5 superadas |
| **H2** Texto plano en backend | File Text Extractor con `.txt`, `.csv` y `.md` con detección de codificación; metadata de traza de 12.1 | H1 | SD-M-01 verde para texto plano. La extracción no ocurre en el cliente |
| **H3** Documentos ofimáticos y PDF nativo | Extracción de `.docx` y de `.pdf` con capa de texto; desglose por página; Context Guard operativo con rechazo explícito | H2 | SD-M-01 y SD-M-03 verdes |
| **H4** OCR y ruta asíncrona | Clasificación por página; motor de OCR; broker, Ingest Worker y consulta de estado; subida directa para archivos grandes | H3, D-M-03, **P-M-03** | SD-M-02 verde. Precisión de la regla de OCR ≥ 95 % |
| **H5** Producción | Set de evaluación construido y ejecutado; umbrales de P-M-07 fijados; paneles de 12.4; alertas; cuotas dimensionadas; runbook operativo | H4 y cierre de P-M-01 a P-M-08 | Pruebas de carga superadas y gate de calidad aprobado |

## 14.1 Ruta crítica

1. **D-M-01** determina el límite de contexto, que es el techo funcional del sistema. Sin él, el Context Guard no tiene valor que aplicar y no se puede comunicar al usuario qué documentos son procesables.
2. **D-M-02** bloquea H1 y condiciona el resto del pipeline. Su consecuencia sobre el runtime —Java frente a Python— tiene impacto en la topología.
3. **P-M-03**, la muestra real de documentos, bloquea D-M-03 y con ella todo H4. Es el pendiente más subestimado del plan: sin conocer la proporción de PDF escaneado, ni el motor de OCR ni su costo se pueden decidir con fundamento.
4. **D-M-07 y D-M-08** bloquean el aprovisionamiento.
5. **P-M-01 y P-M-02** condicionan el criterio de aceptación de las pruebas de carga, y sin ellos H5 no se puede cerrar.

## 14.2 Camino único de ingesta

**Existe un solo camino de ingesta y atraviesa el pipeline de backend.** Ninguna extracción de contenido ocurre en el cliente.

La regla es estructural, no de conveniencia: un camino de ingesta que no atraviese el escaneo de malware, la sanitización, la detección de PII y la moderación anula los controles del camino que sí lo hace. Habilitar `.txt` en H2 cierra ese camino alterno de forma definitiva.

---

# 15. Riesgos y decisiones pendientes

## 15.1 Riesgos

| ID | Riesgo | Prob. | Impacto | Mitigación | Riesgo residual |
| --- | --- | --- | --- | --- | --- |
| R-M-01 | **Documentos extensos legítimos no se pueden procesar** por ausencia de recuperación aumentada | **Alta** | Alto | Límite explícito y comunicado; rechazo accionable con páginas admisibles; métrica de tasa de rechazo por contexto en el panel de 12.4 | **Alto y aceptado.** Es la consecuencia directa de la acotación de alcance. La métrica de 12.4 es la evidencia con la que decidir si la recuperación aumentada debe incorporarse al alcance |
| R-M-02 | El agente no puede citar página ni región, lo que dificulta verificar sus afirmaciones sobre el documento | Alta | Medio | El desglose por página del contrato de 6.4 conserva la información necesaria por si la citación se incorporara después | **Medio y aceptado.** La citación está fuera de alcance por decisión |
| R-M-03 | El costo de OCR se dispara si la proporción de PDF escaneado supera lo previsto | **Alta** | Alto | Cuota específica de páginas de OCR por usuario y día; métrica de páginas de OCR con alerta; `ocr_policy` configurable | Medio hasta que se cierre P-M-03 |
| R-M-04 | La precisión de OCR sobre documentos degradados queda por debajo de lo operable | Media | Alto | Casos de escaneo degradado en el set de evaluación; confianza mínima por página; advertencia visible al usuario cuando la confianza es baja | Medio. Depende de la calidad real del origen documental |
| R-M-05 | Inyección de prompt embebida en documento no detectada | Media | **Alto** | Ocho capas de defensa de 11.7; casos adversos con umbral del 100 % en 13.4; alerta ante cualquier detección de contenido oculto | Medio. El vector documental es más peligroso porque el usuario puede ser una víctima, no el atacante |
| R-M-06 | El caché filtra texto entre usuarios | Baja | **Alto** | Ámbito de aislamiento en la clave; revalidación de autorización y de PII en cada acierto; prueba de seguridad específica | Bajo |
| R-M-07 | La extracción agota memoria y tumba instancias | Media | Medio | Límite de concurrencia derivado de memoria, no de CPU; prueba de resistencia de 8 h; métrica de fallos por memoria | Bajo |
| R-M-08 | El motor de extracción elegido obliga a un runtime distinto del resto del backend | Media | Medio | Evaluado explícitamente en D-M-02 como consecuencia, no como detalle | Bajo si se decide con conocimiento del impacto |
| R-M-09 | Los objetivos de negocio nunca se fijan y el canal opera sin criterio de calidad | Media | Alto | P-M-01 a P-M-08 como bloqueantes formales del hito H5 | Bajo si se respeta el gate |
| R-M-10 | Coexisten dos caminos de ingesta con controles distintos si no se completa la migración de H2 | Media | **Alto** | La migración es criterio de salida de H2, no un entregable diferible. Ver 14.2 | Bajo si se respeta el hito |
| R-M-11 | Falsos positivos de moderación bloquean documentos legítimos y el canal se vuelve inutilizable | Media | Medio | Métrica de falsos positivos en 13.4; umbral explícito; ajuste con el set de evaluación | Medio hasta calibrar |
| R-M-12 | Documentos con PII no prevista obligan a rediseñar el gobierno del canal | Media | Medio | Detección antes de persistir; rechazo de categorías restringidas; evaluación en la Matriz de Riesgos según 11.8 | Bajo |

## 15.2 Tabla consolidada de decisiones

| ID | Decisión | Alternativas | Criterio | Consecuencia | Estado |
| --- | --- | --- | --- | --- | --- |
| D-M-01 | Modelo de lenguaje y ventana de contexto | Modelos disponibles en la región elegida | Tamaño de ventana, calidad en español sobre documentos largos, costo por millón de tokens, disponibilidad regional | **Fija el techo de tamaño de documento del sistema.** Ver 9.4 | **Pendiente. Bloqueante** |
| D-M-02 | Motor de extracción documental | Apache Tika · librerías Python especializadas · servicio administrado | Cobertura de formatos, fidelidad de tablas y estructura, huella operativa, costo, compatibilidad con el runtime | Tika implica runtime Java separado. El servicio administrado resuelve también D-M-03 a costa de dependencia externa | **Pendiente. Bloqueante** |
| D-M-03 | Motor de OCR | Servicio administrado · motor autoalojado | Precisión en español sobre muestra real, costo por página, latencia, *private endpoint*, residencia | **No evaluable sin P-M-03** | **Pendiente. Bloqueante de H4** |
| D-M-04 | Servicio de escaneo de malware | Escaneo integrado del almacenamiento · servicio corporativo · terceros | Cobertura de formatos, latencia en T2, integración con SIEM | Sin él no hay ingesta de archivos. Ver 11.3 | Pendiente |
| D-M-05 | Servicio de detección y redacción de PII | Servicio administrado de lenguaje · DLP corporativo · combinación | Precisión en español, categorías, latencia, integración corporativa | Su caída detiene la ingesta. Ver 10.2 | Pendiente |
| D-M-06 | Servicio de moderación y guardrails | Seguridad de contenido administrada · guardrails del proveedor de modelos | Detección de ataques indirectos por documento, latencia, categorías | Su caída detiene la ingesta y la salida | Pendiente |
| D-M-07 | Región de despliegue | Regiones candidatas de Azure | Residencia, disponibilidad de OCR y PII, latencia, consistencia con el resto del despliegue | Bloquea la sección 8 | **Pendiente. Bloqueante** |
| D-M-08 | Runtime de despliegue del pipeline | AKS · Container Apps · App Service | Perfil intensivo en memoria de la extracción, escalado por cola, capacidad operativa | Bloquea la sección 8 | **Pendiente. Bloqueante** |
| D-M-09 | Base de datos del dominio | Motores administrados disponibles en la región | — | Bloquea la materialización de la sección 7 | **Pendiente. Información faltante** |
| D-M-10 | Almacén del caché de artefactos | Caché distribuida · base de datos · almacenamiento de objetos | Tamaño del texto, latencia de lectura, TTL nativo, costo | Afecta el beneficio de latencia de 2.3 | Pendiente |
| D-M-11 | Modelo de cifrado en reposo | Claves de plataforma · claves gestionadas por el cliente | Requisito regulatorio, operación de rotación, costo | Afecta el modelo operativo de claves | Pendiente |
| D-M-12 | Broker de mensajería concreto | Servicios de mensajería administrados de la nube elegida | Garantías de entrega, orden, cola de fallidos | Bloquea la ruta asíncrona | Pendiente |
| **D-M-13** | **Recuperación aumentada para documentos extensos** | Incorporar chunking, indexación y recuperación · mantener el límite de contexto | Tasa de rechazo por contexto medida en producción; volumen de documentos extensos legítimos | **Fuera de alcance por decisión.** Se registra para que la métrica de 12.4 alimente su reconsideración | **Descartada en esta versión** |
