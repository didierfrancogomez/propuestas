---
titulo: "Arquitectura de Referencia Multimodal V1.0"
id: 6094422066
espacio: AFGLYP
version: 4
actualizado: 2026-08-06T13:38:27.559Z
actualizado_por: "Junior Millan Perez"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Referencia [Multimodal - Voz - Multiagente]"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6094422066
---

# Arquitectura de Referencia Multimodal V1.0

## Índice

1. Alcance del diseño
2. Principio arquitectónico
3. Capas arquitectónicas
4. Arquitectura de referencia
5. Componentes del diseño
6. Flujos por modalidad
7. Stack tecnológico habilitado
8. Criterios de adopción
9. Persistencia, información sensible y ciclo de vida
10. Observabilidad multimodal
11. Calidad de la conversión a texto
12. Adaptación al PoC actual

---

## Resumen ejecutivo

Esta arquitectura de referencia habilita al agente para procesar entradas en múltiples modalidades: texto directo, archivos y documentos, y audio. Todos los canales convergen en un único endpoint del agente entregando texto, aplicando el principio de normalización del input antes de llegar al núcleo del agente.

El agente no requiere lógica específica por canal. La conversión de cada modalidad a texto ocurre en componentes especializados que encapsulan a los proveedores tecnológicos, garantizando que el gateway sea el punto único de entrada y aplicación de gobierno.

El diseño es adaptable al PoC existente sin reescritura: los componentes que hoy están construidos (frontend con captura, agente con LLM real, gateway APIM, observabilidad y gobierno) se preservan y se extienden con transformadores por modalidad detrás del gateway. La sección 12 describe cómo se materializa esta evolución.

---

## 1. Alcance del diseño

**Modalidades cubiertas:**

- Texto directo (chat).
- Archivos y documentos (`.txt` en primera fase; `.pdf`, `.docx` y otros formatos como extensión posterior).
- Audio (voz del usuario transcrita a texto).

**Alcance funcional:**

- Definición de componentes por modalidad.
- Flujos end-to-end incluyendo la respuesta al usuario.
- Stack tecnológico habilitado.
- Criterios de adopción por caso de uso.
- Consideraciones de persistencia, información sensible y ciclo de vida.

**Fuera de alcance:**

- Respuesta del agente en modalidades distintas al texto.
- Streaming de audio en tiempo real.
- Procesamiento de video.
- Procesamiento de imágenes.
- Múltiples idiomas simultáneos en una misma sesión.

---

## 2. Principio arquitectónico

**Normalización del input antes del agente. Gateway como punto único de entrada.**

Todo canal de entrada se transforma a texto antes de llegar al agente, y toda comunicación desde y hacia el frontend atraviesa el gateway. Consecuencias del principio:

- El agente no requiere lógica específica por modalidad.
- La trazabilidad es uniforme independientemente del origen del input.
- La aplicación de autenticación, cuotas y gobierno se centraliza en el gateway.
- La superficie de exposición del núcleo del agente no crece con cada modalidad.
- La incorporación de modalidades adicionales se resuelve agregando un transformador detrás del gateway, sin rediseñar el agente.

---

## 3. Capas arquitectónicas

La solución multimodal se organiza en cinco capas.

| Capa | Responsabilidad |
| --- | --- |
| Capa de Experiencia | Captura del input en su modalidad original (texto, archivo, audio) en el frontend. |
| Capa de Gateway | Autenticación, enrutamiento y control de cuotas por canal. Punto único de entrada. |
| Capa de Transformación de Canal | Conversión de cada modalidad a texto normalizado. Componentes backend detrás del gateway. |
| Capa de Agent Runtime | Procesamiento del texto por parte del agente. No conoce la modalidad de origen. |
| Capa Transversal | Observabilidad, gobierno del dato, seguridad y evaluación de calidad. |

---

## 4. Arquitectura de referencia

<!-- [macro: mermaid (size=medium, isEditable=true, diagramCode=flowchart TB
    subgraph EXP["Capa de Experiencia"]
        USER([Usuario])
        UI[Frontend<br/>Captura: texto, archivo, audio]
    end

    subgraph GW["Capa de Gateway"]
        APIM[API Gateway<br/>Autenticación · Enrutamiento · Cuotas]
    end

    subgraph TRANSFORM["Capa de Transformación de Canal"]
        TXT_EXTRACT[File Text Extractor<br/>Extracción de contenido de archivos]
        SPEECH[Speech Processor<br/>Audio a Texto]
    end

    subgraph RT["Capa de Agent Runtime"]
        O[Orquestador]
        A[Agente Experto]
    end

    subgraph CROSS["Capa Transversal"]
        OTEL[Observabilidad<br/>OpenTelemetry]
        GOB[Gobierno del Dato<br/>Governance API]
        SEC[Seguridad<br/>Entra ID · TLS]
        EVAL[Gobierno de Evals<br/>Golden set · WER · Calidad]
    end

    USER <--> UI

    UI -->|texto directo| APIM
    UI -->|archivo binario| APIM
    UI -->|audio binario| APIM

    APIM --> TXT_EXTRACT
    APIM --> SPEECH
    TXT_EXTRACT -->|texto extraído| APIM
    SPEECH -->|texto transcrito| APIM

    APIM --> O
    O --> A
    A -->|respuesta texto| APIM
    APIM -->|respuesta texto| UI

    APIM -.-> SEC
    APIM -.-> GOB
    O -.-> OTEL
    SPEECH -.-> OTEL
    TXT_EXTRACT -.-> OTEL
    SPEECH -.-> EVAL, caption=default2026-07-09T13:22:25.879Zmermaid)] -->

En esta arquitectura, el frontend envía siempre al gateway. El gateway aplica autenticación y cuotas, enruta al componente de transformación cuando aplica (archivo o audio), recibe el texto normalizado, y lo entrega al Agent Runtime. La respuesta del agente sale al usuario también a través del gateway.

---

## 5. Componentes del diseño

### 5.1 Frontend

Componente existente que incorpora tres capacidades de entrada: chat directo, adjunto de archivos y captura de audio. Todas se apoyan en APIs nativas del navegador (`FileReader`, `MediaRecorder`). El frontend no ejecuta transformación ni extracción; delega la conversión al backend a través del gateway. Esto centraliza el gobierno y evita procesamiento sensible en el navegador.

### 5.2 File Text Extractor

Componente backend detrás del gateway responsable de leer archivos adjuntos y extraer su contenido como texto plano.

Responsabilidades:

- Recibir el binario del archivo desde el gateway.
- Validación de tipo real, tamaño y codificación.
- Extracción del contenido según el formato.
- Sanitización básica previa al envío al agente.
- Retornar el texto extraído junto con metadata (tipo de archivo, tamaño, latencia de extracción).

En la primera fase soporta archivos `.txt` con detección de codificación (UTF-8, UTF-16, Latin-1). Formatos adicionales (`.pdf`, `.docx`) se incorporan mediante estrategias de extracción especializadas (Apache Tika u OCR) sin modificar el contrato del componente.

### 5.3 Speech Processor

Componente backend independiente detrás del gateway responsable de convertir audio a texto.

Responsabilidades:

- Recibir el binario de audio desde el gateway.
- Validar formato de audio y aplicar conversión si es necesario (ver sección 7.2).
- Invocar el servicio de transcripción seleccionado.
- Retornar el texto resultante con metadata de confianza, latencia y proveedor.
- Encapsular el detalle del proveedor de transcripción.

Su ubicación aísla la capacidad del ciclo de vida del agente y permite su reutilización por otros clientes (móvil, integración corporativa).

### 5.4 Gateway

Componente existente que actúa como punto único de entrada al backend. Sus responsabilidades para el flujo multimodal son:

- Validación del token JWT emitido por Entra ID.
- Aplicación de cuotas por canal (audio consume más tokens que texto directo).
- Enrutamiento del flujo de archivo hacia el File Text Extractor.
- Enrutamiento del flujo de audio hacia el Speech Processor.
- Enrutamiento del texto normalizado hacia el Agent Runtime.
- Enrutamiento de la respuesta del agente de vuelta al frontend.
- Propagación de la identidad del usuario en cada request hacia los componentes de transformación y el agente.

### 5.5 Agent Runtime

Componente existente. No cambia. Recibe siempre texto y no conoce la modalidad de origen. La modalidad se registra únicamente en la metadata de la traza para observabilidad.

### 5.6 Componentes transversales

- **Observabilidad:** trazabilidad end-to-end con metadata de canal de origen.
- **Gobierno del dato:** clasificación, retención y ACL heredada por canal.
- **Seguridad:** autenticación, autorización, cifrado en tránsito y en reposo.
- **Gobierno de evals:** medición de calidad de la conversión a texto en cada modalidad.

---

## 6. Flujos por modalidad

Todos los flujos parten del frontend, atraviesan el gateway, aplican transformación cuando corresponde y terminan con la respuesta del agente entregada al usuario a través del mismo gateway.

### 6.1 Flujo de texto directo

<!-- [macro: mermaid (size=medium, isEditable=true, diagramCode=sequenceDiagram
    autonumber
    participant U as Usuario
    participant FE as Frontend
    participant GW as Gateway
    participant O as Orquestador
    participant A as Agente

    U->>FE: Escribe mensaje
    FE->>GW: envía texto (input_channel = texto)
    GW->>GW: valida token · aplica cuota
    GW->>O: enruta
    O->>A: procesa
    A-->>O: respuesta texto
    O-->>GW: respuesta texto
    GW-->>FE: respuesta texto
    FE-->>U: muestra respuesta, caption=default2026-07-09T13:24:13.315Zmermaid)] -->

### 6.2 Flujo de archivo adjunto

<!-- [macro: mermaid (size=medium, isEditable=true, diagramCode=sequenceDiagram
    autonumber
    participant U as Usuario
    participant FE as Frontend
    participant GW as Gateway
    participant EX as File Text Extractor
    participant O as Orquestador
    participant A as Agente

    U->>FE: Adjunta archivo
    FE->>GW: envía binario del archivo (input_channel = archivo)
    GW->>GW: valida token · aplica cuota
    GW->>EX: enruta al File Text Extractor
    EX->>EX: valida tipo, tamaño, codificación
    EX->>EX: extrae contenido
    EX-->>GW: texto extraído + metadata
    GW->>O: enruta texto al Orquestador
    O->>A: procesa (idéntico al canal texto)
    A-->>O: respuesta texto
    O-->>GW: respuesta texto
    GW-->>FE: respuesta texto
    FE-->>U: muestra respuesta, caption=default2026-07-09T13:24:54.915Zmermaid)] -->

### 6.3 Flujo de audio

<!-- [macro: mermaid (size=medium, isEditable=true, diagramCode=sequenceDiagram
    autonumber
    participant U as Usuario
    participant FE as Frontend
    participant GW as Gateway
    participant SP as Speech Processor
    participant STT as Servicio de Transcripción
    participant O as Orquestador
    participant A as Agente

    U->>FE: Graba audio
    FE->>FE: captura audio (MediaRecorder)
    FE->>GW: envía binario de audio (input_channel = voz)
    GW->>GW: valida token · aplica cuota
    GW->>SP: enruta al Speech Processor
    SP->>SP: valida formato y convierte si aplica
    SP->>STT: solicita transcripción
    STT-->>SP: texto transcrito + confianza + latencia
    SP-->>GW: texto transcrito + metadata
    GW->>O: enruta texto al Orquestador
    O->>A: procesa (idéntico al canal texto)
    A-->>O: respuesta texto
    O-->>GW: respuesta texto
    GW-->>FE: respuesta texto
    FE-->>U: muestra respuesta, caption=default2026-07-09T13:25:45.831Zmermaid)] -->

---

## 7. Stack tecnológico habilitado

Stack aprobado para la construcción del canal multimodal.

| Capa | Componente | Tecnología habilitada |
| --- | --- | --- |
| Frontend | SPA de captura | Angular con APIs nativas del navegador (`FileReader`, `MediaRecorder`) |
| File Text Extractor | Extracción de contenido | Componente backend con motor de extracción según formato (extractor plano para `.txt`, Apache Tika o equivalente para `.pdf` y `.docx`) |
| Speech Processor | Servicio de transcripción | Componente backend en el runtime del proyecto. Encapsula el proveedor de transcripción |
| Gateway | API Management | Azure APIM (existente en el proyecto) |
| Agent Runtime | Runtime del agente | Python + LangGraph (existente en el proyecto) |
| LLM | Modelos de lenguaje | LLM Gateway existente en el proyecto |
| Observabilidad | Trazas y métricas | OpenTelemetry con exportación a Dynatrace (existente) |
| Gobierno del dato | Políticas y clasificación | Governance API existente. Modelo de gobierno de archivos aplicable al binario de audio |
| Seguridad | Autenticación e identidad | Microsoft Entra ID con JWT (existente) |
| Almacenamiento | Archivos y binarios | Azure Blob Storage cuando aplique persistencia |

### 7.1 Alternativas para el servicio de transcripción

| Opción | Descripción | Consideraciones |
| --- | --- | --- |
| A. STT dedicado | Servicio administrado como Azure Speech Service. Soporte nativo para español latinoamericano. Custom Speech para vocabulario del dominio. | Requiere provisionamiento. Facturación separada. Máxima madurez para producción escalada. |
| B. Whisper vía LLM Gateway | Reutiliza el gateway de modelos ya establecido. Facturación consolidada con el resto de invocaciones al LLM. | Latencia mayor que STT dedicado. Sin Custom Speech. |
| C. Modelo multimodal nativo | Procesa audio y texto en el mismo request. Elimina el paso separado de transcripción. | Disponibilidad regional variable. Sin transcripción intermedia auditable. |

La selección se determina con criterios objetivos: latencia end-to-end, costo por minuto, precisión sobre términos del dominio validada con golden set, cumplimiento con gobierno del dato y ciberseguridad, consistencia con el stack de la plataforma.

La arquitectura absorbe cualquiera de las tres opciones sin cambios estructurales, dado que el Speech Processor encapsula al proveedor.

### 7.2 Formato de audio soportado

El navegador con `MediaRecorder` produce por defecto formatos que pueden variar entre navegadores (WebM/Opus en Chrome, MP4/AAC en Safari). El Speech Processor debe cumplir una de las dos condiciones:

- Soportar directamente los formatos generados por los navegadores objetivo.
- Realizar conversión previa al formato requerido por el servicio de transcripción (WAV a 16 kHz es el formato más ampliamente compatible).

El diseño delega esta responsabilidad al Speech Processor y no la expone al frontend ni al agente.

---

## 8. Criterios de adopción

### 8.1 Casos de uso donde aplica

- Interfaces conversacionales donde el usuario necesita adjuntar contexto adicional en forma de documentos.
- Escenarios de accesibilidad donde la escritura no es la modalidad preferente.
- Flujos de evaluación que requieren aportar evidencia documental como parte del análisis.
- Escenarios donde la voz reduce fricción del usuario en tareas repetitivas o de campo.
- Iniciativas que requieren registrar y analizar el contenido de reuniones o entrevistas.

### 8.2 Casos de uso donde no aplica

- Procesos batch sin intervención humana en el punto de entrada.
- Interfaces embebidas en sistemas legacy sin acceso a APIs de navegador.
- Casos que exigen respuesta del agente en voz sintetizada — fuera del alcance del diseño actual.
- Escenarios con volumen extremadamente alto de audio que exijan streaming en tiempo real — no cubierto por el diseño de procesamiento por lote.
- Procesamiento de contenido en modalidades no textualizables (video, imagen sin OCR, señales biométricas).

### 8.3 Restricciones técnicas

- La transcripción se ejecuta por lote al finalizar la grabación. No hay streaming en tiempo real.
- El diseño contempla un idioma por sesión.
- La calidad de la transcripción depende del entorno del usuario, incluyendo el micrófono y el ruido ambiente.
- El tamaño máximo del archivo adjunto queda definido por la configuración del gateway.
- El agente responde únicamente en texto.

### 8.4 Restricciones de gobierno

- El texto transcrito y el contenido de archivos adjuntos se tratan como input no confiable y pasan por sanitización antes de entrar al contexto del modelo.
- El contenido adjunto hereda la clasificación de la evaluación a la que pertenece.
- La retención del binario de audio se define según requisitos regulatorios y de negocio.
- Los canales que consumen más tokens tienen cuotas específicas por usuario y por sesión.

---

## 9. Persistencia, información sensible y ciclo de vida

### 9.1 Persistencia por modalidad

| Elemento | Persistencia | Ubicación |
| --- | --- | --- |
| Texto directo | En la traza de la evaluación | Base de datos del proyecto |
| Contenido de archivo adjunto | Como referencia en la traza. Binario según política de retención | Base de datos + Azure Blob Storage cuando aplique |
| Binario del archivo | Según requisito de auditoría | Azure Blob Storage con clasificación heredada |
| Audio original | Por defecto no se persiste | En memoria durante procesamiento |
| Transcripción del audio | Como parte de la traza | Base de datos del proyecto |

### 9.2 Manejo de información sensible

- **Cifrado en tránsito:** TLS obligatorio para todas las modalidades.
- **Cifrado en reposo:** los binarios almacenados en Azure Blob Storage se cifran en reposo.
- **Sanitización:** el texto extraído de archivos y la transcripción de audio pasan por sanitización previa al contexto del modelo para protección contra prompt injection.
- **Detección de PII:** el pipeline de ingesta valida el contenido antes de indexarlo. Los archivos con PII no autorizada se rechazan o se redactan según política.
- **Autenticación:** cada request se autentica con JWT emitido por Entra ID. La modalidad no debilita el modelo de autenticación.
- **Autorización:** el rol del usuario aplica igual a los tres canales.

### 9.3 Ciclo de vida del audio

| Fase | Duración | Estado del binario |
| --- | --- | --- |
| Captura | Durante la grabación | En memoria del navegador |
| Transmisión | Durante el envío al gateway y al Speech Processor | En tránsito por TLS |
| Procesamiento | Durante la transcripción | En memoria del Speech Processor |
| Post-procesamiento | Hasta completar la traza | Retención mínima operativa para auditoría en caso de disputa |
| Eliminación | Al cerrar la sesión o cumplir la retención | Descartado. Solo permanece la transcripción textual |

Si se requiere persistencia auditable del audio original por requisito regulatorio, se activa el modelo de gobierno de archivos existente en el proyecto con clasificación, ACL heredada y política de retención.

### 9.4 Ciclo de vida del archivo adjunto

| Fase | Duración | Estado del archivo |
| --- | --- | --- |
| Adjunto | Al momento del upload | Validado en el frontend por tamaño y extensión |
| Envío al backend | Durante la transmisión | En tránsito por TLS |
| Extracción de contenido | Al procesarse el mensaje | En memoria del File Text Extractor |
| Persistencia opcional | Según política del proyecto | Azure Blob Storage con clasificación |
| Eliminación | Según retención definida | Descartado |

---

## 10. Observabilidad multimodal

El canal de origen del input queda registrado en la traza de cada evaluación.

| Campo | Valores |
| --- | --- |
| input_channel | texto, archivo, voz |
| file_type | Solo cuando el canal es archivo — tipo del archivo adjunto |
| extraction_latency_ms | Solo cuando el canal es archivo |
| transcription_latency_ms | Solo cuando el canal es voz |
| transcription_confidence | Solo cuando el canal es voz |
| stt_provider | Solo cuando el canal es voz — identifica el proveedor usado |

El modelo de observabilidad estructurada existente en el proyecto se conserva. Se incorpora únicamente la metadata anterior.

---

## 11. Calidad de la conversión a texto

La calidad de cada modalidad se evalúa siguiendo la metodología de gobierno de evals del proyecto.

| Modalidad | Métrica principal | Métrica operativa |
| --- | --- | --- |
| Archivo `.txt` | Exactitud de la extracción respecto al contenido original | Latencia de extracción |
| Archivo `.pdf` / `.docx` | Cobertura del texto extraído respecto al documento original | Latencia y precisión de estructura |
| Audio | Word Error Rate sobre golden set | Latencia end-to-end y precisión sobre términos del dominio |

Las metas cuantitativas se establecen tras la primera ejecución con datos reales, siguiendo el mismo esquema de gobierno usado para los evals del agente.

---

## 12. Adaptación al PoC actual

Esta sección describe cómo esta arquitectura de referencia se materializa sobre lo que ya está construido en el PoC, sin exigir reescritura de los componentes existentes.

### 12.1 Componentes ya construidos que soportan el diseño

| Componente del diseño | Estado en el PoC | Rol en la arquitectura multimodal |
| --- | --- | --- |
| Frontend con captura | Angular funcional con captura de archivos `.txt` operativa | Punto de captura para las tres modalidades. Se amplía con captura de audio (MediaRecorder) manteniendo el mismo patrón |
| Gateway API | Azure APIM en operación con dos herramientas verificadas end-to-end | Punto único de entrada. Absorbe las rutas de archivo y audio con nuevas policies |
| Agent Runtime | Orquestador y Agente Experto en operación con LLM real | No cambia. Sigue recibiendo texto |
| Observabilidad | OpenTelemetry cableado con contexto estructurado por request | Se extiende con los campos por canal descritos en la sección 10 |
| Gobierno del dato | Governance API construida (Opción A, standalone) | Se conecta al flujo multimodal para clasificación y retención por canal |
| Seguridad | Entra ID con JWT implementado en frontend y backend | Aplica igual a los tres canales sin modificaciones |

### 12.2 Componentes a evolucionar

| Componente | Evolución requerida | Grado de cambio |
| --- | --- | --- |
| File Text Extractor | Actualmente en frontend soportando `.txt`. Migra a backend detrás del gateway. La primera fase mantiene `.txt`; formatos adicionales se incorporan bajo el mismo contrato | Reubicación con conservación del contrato existente |
| Speech Processor | Componente nuevo. Se construye como backend independiente detrás del gateway | Componente nuevo |
| APIM | Nuevas rutas para archivo y audio, con cuotas específicas por canal | Configuración incremental |
| Angular | Se agrega captura de audio con MediaRecorder | Extensión, no rediseño |
