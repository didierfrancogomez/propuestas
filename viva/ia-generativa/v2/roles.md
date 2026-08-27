# Ingeniero de Desarrollo Asistido por IA
*(AI Development Systems Engineer)*

Definición de rol para reclutamiento. Se cubre en pareja: **dos personas con el mismo perfil**, que
se auditan mutuamente. Perfil senior: más de 6 años en desarrollo, al menos 1 usando agentes de IA
sobre código real. Inglés técnico de lectura y escritura.

---

## Enfoque

Construye el sistema con el que un equipo entero programa: la base de conocimiento del código del
cliente, el estándar técnico convertido en reglas, el proceso por fases y los guardrails que impiden
avanzar cuando falta algo.

**No escribe ese sistema a mano: lo concibe, lo dirige y lo audita.** Los documentos, las reglas y
los guardrails los redacta el agente de IA. El valor del rol está en entender la solución y el
proceso, diseñar cómo se estructuran, orientar al agente y verificar lo que produce.

Dos criterios gobiernan el diseño:

- **Lo que debe estar garantizado se implementa fuera del modelo** — en un guardrail, no en una
  instrucción que se le pide al modelo cumplir.
- **Nada se afirma sin evidencia citada.** Un resultado que suena razonable pero es incorrecto hace
  más daño que uno ausente.

---

## 1. Responsabilidades del rol

- **Diseñar el proceso de la IA:** las fases del ciclo, el criterio de salida de cada una, y **qué
  artefacto la cierra** — su contenido, su estructura y qué lo hace verificable.
- **Diseñar e implementar los guardrails:** impedir que se escriba código sin análisis aprobado;
  impedir la publicación sin pruebas verdes, revisión aprobada, aprobación anclada al commit
  validado y firma humana. Con pruebas propias del mecanismo.
- **Levantar la base de conocimiento** del sistema del cliente: definir el corte y la granularidad,
  dirigir el mapeo y revisar que cada afirmación esté citada y lo desconocido marcado como tal.
- **Obtener lo que no está escrito:** llevar las dudas al equipo técnico y funcional, y convertir
  las respuestas en documentación, reglas o guardrails, dejando constancia de quién definió qué.
- **Extraer el estándar** del histórico de revisiones del equipo y decidir qué es regla y qué es
  preferencia personal.
- **Integrar con el flujo real de trabajo:** conexión con el gestor de tickets, arranque con un solo
  comando, avance versionado y retomable desde cualquier máquina, y escritura hacia el ticket
  siempre detrás de aprobación humana.
- **Cerrar diseño, pruebas y entrega:** decisiones registradas antes de codificar; pruebas trazadas
  una a una con la matriz de escenarios y cobertura sobre lo modificado; PR autosuficiente con la
  evidencia y el match uno a uno contra el ticket.
- **Sostener la adopción:** eval set para detectar degradación, acompañamiento sobre trabajo real y
  traspaso al dueño del proceso del cliente.

---

## 2. Conocimientos requeridos

Excluyentes, en orden de lo que más discrimina.

### 2.1 Diseño de procesos y de sus artefactos
Descomponer un ciclo de trabajo real en fases con criterio de salida verificable. Definir qué
contiene el artefacto que cierra cada fase y qué lo hace auditable. Distinguir qué se le pide al
modelo y qué se implementa por fuera. Convertir una regla en un mecanismo que la sostiene. Convertir
la ambigüedad en pregunta bloqueante en vez de resolverla.

### 2.2 Dirección y revisión de agentes de codificación
- Arquitectura de instrucciones y de contexto: archivo orquestador, progressive disclosure — las
  reglas siempre en contexto, los procedimientos solo cuando se necesitan — y el context window
  entendido como una restricción real de ingeniería.
- **Hooks:** al iniciar sesión, al enviar un prompt y antes de usar una herramienta; cómo se deniega
  una operación; cómo se inyecta estado en el contexto; y la regla de **fail-closed**.
- Subagentes: no heredan nada; definiciones versionadas en el repositorio; ejecución en paralelo con
  consolidación posterior.
- Comandos propios como punto de entrada único; permisos; trabajo sobre varios repositorios;
  ejecución headless en CI.
- **Revisar lo producido:** detectar afirmaciones sin evidencia, ambigüedades resueltas por cuenta
  propia, artefactos que no corresponden al trabajo hecho, y guardrails que en la práctica no
  impiden nada.

> Referencia directa: **Claude Code**. Se admite experiencia equivalente con otro agente. No se
> admite haberlo usado como autocompletado, ni sin revisar lo que produce.

### 2.3 Levantamiento de información y comunicación asertiva
Conversar con perfiles técnicos y funcionales, llegar con las preguntas preparadas y con una
recomendación, reconocer un vacío y formularlo como pregunta concreta, contradecir con evidencia
cuando dos personas afirman cosas incompatibles, y conducir una reunión de decisión con las opciones
por escrito.

### 2.4 Amplitud técnica senior
Recorrido real en los cuatro frentes, porque es lo que hace posible revisar el trabajo del agente:
- **Arquitectura:** APIs REST, capas o CQRS, inyección de dependencias, acceso a datos,
  integraciones con terceros.
- **Desarrollo:** un stack de backend empresarial (.NET/C#, Java, Node o equivalente), y capacidad
  de entrar a un código grande y ajeno y explicarlo con evidencia en días.
- **DevOps:** CI/CD, contenedores, y capacidad de leer, depurar y corregir scripts de automatización
  (Bash sobre todo; Python y PowerShell según el cliente). No se exige escribirlos de memoria.
- **Calidad:** qué demuestra cada nivel de prueba, cobertura sobre el cambio, y por qué un test
  flaky inutiliza un guardrail.

### 2.5 Git y plataforma de código, a nivel de mecanismo
Anclar una aprobación a un commit y saber qué la invalida; fast-forward; squash a un solo commit;
ramas por ticket; varios repositorios independientes; CLI y API de GitHub o equivalente; CI.

### 2.6 Integración con el gestor de tickets
API REST de Jira o equivalente: lectura completa del ticket, transiciones, comentarios y adjuntos.
Escritura siempre detrás de aprobación humana explícita.

### 2.7 Manejo de información sensible
Credenciales y secretos fuera del control de versiones; los dumps de tickets tratados como datos
sensibles. Los tickets de los clientes suelen traer credenciales de prueba pegadas en comentarios.

### 2.8 Rasgos exigibles
- **Disciplina de evidencia:** escribir *desconocido* y sostenerlo bajo presión de fecha. Es el
  requisito que más candidatos técnicamente sólidos no cumplen.
- **Criterio editorial:** aunque el agente redacte, la persona responde por el texto — debe ver qué
  sobra, qué falta y qué se afirma sin respaldo.
- **Autonomía con criterio para detenerse** cuando la ambigüedad es real.

---

## 3. Conocimientos deseados

- **Evaluación de sistemas con LLM:** eval sets y detección de regresiones al cambiar de modelo o de
  prompt. El de mayor valor de esta lista.
- MCP (Model Context Protocol) y construcción de herramientas propias para el agente.
- Costo y latencia: prompt caching, tamaño del context window, elección de modelo por tipo de tarea.
- **Developer platform / developer experience:** tooling interno, plantillas, linters, calidad
  automatizada. La experiencia más transferible a este rol.
- Análisis estático y reglas propias (analizadores del compilador, SonarQube).
- Consultoría o fábrica de software: comodidad entrando a organizaciones ajenas.
- Dominio de negocio del cliente de destino.
- Observabilidad, ambientes reproducibles y métricas de ingeniería.

---

## Guía rápida para el reclutador

**Dónde buscar:** ingenieros de developer platform / developer experience · backend senior que
construyó su propia automatización sobre un agente de IA · perfiles DevOps con base fuerte de
desarrollo · tech leads que definieron estándares y los implementaron.

**Palabras clave de búsqueda:** `Claude Code` · `AI agent` · `agentic coding` · `hooks` · `MCP` ·
`context engineering` · `Agent SDK` · `Copilot` · `Cursor` · `developer experience` · `internal
tooling` · `CI/CD` · `Bash` · `.NET` / `Java` / `Node` · `Jira API` · `technical writing`

**Motivos de descarte:**
- Usa el agente como autocompletado, o acepta lo que produce sin revisarlo.
- Perfil de machine learning o data science: aquí no se entrena ni se ajusta un modelo.
- No puede juzgar un texto técnico: en este rol la documentación es el entregable.
- Llena los vacíos con respuestas que suenan razonables en vez de decir que no sabe.
- Nunca entró a un código ajeno y grande.

**Tres preguntas de filtro:**

| Pregunta | Qué se busca en la respuesta |
|---|---|
| Si necesitas garantizar que algo nunca ocurra, ¿se lo pides al modelo o lo implementas por fuera? | **Por fuera, siempre.** Es la que mejor discrimina. |
| Descompón este proceso de desarrollo en fases: ¿qué artefacto cierra cada una y cuál impediría avanzar? | Criterio de salida y control real, no una lista de pasos. |
| ¿Qué construiste alrededor de un agente de IA, más allá de conversar con él? | Hooks, comandos, instrucciones versionadas, ejecución headless en CI. Mecanismo, no resultado. |

**Se define por proyecto antes de abrir la búsqueda:** stack del cliente · dominio de negocio ·
herramientas del ciclo (tickets, código, CI) · sistema operativo del equipo.
