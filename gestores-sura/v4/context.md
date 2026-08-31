# Contexto de trabajo — Propuesta de arquitectura agéntica y torre de control

> Documento interno de Tech and Solve. No se entrega al cliente.
> Última actualización: 31 de agosto de 2026.
> Propósito: dejar por escrito el enfoque, las decisiones tomadas, las fuentes y los
> pendientes, para que ningún cambio futuro nos haga perder el radar.

---

## 1. El enfoque, en una frase

**Indicar, según estándar, cómo se debe tener una torre de control de sistemas agénticos,
orientada a las necesidades de este cliente, sin perder de vista las buenas prácticas.**

Todo lo que escribamos tiene que poder responder a esa frase. Si un contenido no ayuda a
gobernar el sistema agéntico, no va en el cuerpo del documento.

### Qué es nuestra propuesta

- Cómo se **mide la acertividad** de un agente y con qué evidencia.
- Cómo se **entrega y retira autonomía** con respaldo verificable.
- Cómo se **sostiene la trazabilidad** de cada decisión, de forma reconstruible.
- Cómo se **detecta deriva** y cómo se refina un agente sin perder control.
- Cómo se **audita** todo lo anterior frente a un tercero.

### Qué NO es

- No es una especificación de monitoreo operativo. El cliente ya tiene su catálogo de
  indicadores de operación, con 9 ejes y 88 variables. **No lo reemplazamos.**
- No es un rediseño de la arquitectura de gestores. Nos apoyamos en lo que ya construyeron.
- No es una auditoría del equipo cliente. Ver reglas de tono en la sección 6.
- No es un catálogo de teoría. El marco conceptual va en anexos, nunca en el cuerpo.

### Error a no repetir

En la sesión del 31 de agosto propuse *reemplazar* nuestra sección de indicadores por el
catálogo operativo del cliente. Eso disuelve la propuesta en un documento de monitoreo.
Lo correcto: nuestros indicadores agénticos son una **capa que se enchufa** en sus ejes,
y su catálogo se mantiene tal como está.

---

## 2. Entregables vigentes

| Ruta | Qué es | Estado |
|---|---|---|
| `gestores-sura/v3/Tech and Solve - Notas de arquitectura.html` | Propuesta principal: catálogo de 6 propuestas (P1–P6) con anatomía fija, 2 acuerdos aparte, secuencia, y 4 anexos | Entregable, versionado y con PDF |
| `gestores-sura/v4/Tech and Solve - Torre de control.html` | Propuesta de torre de control: 5 capas, 3 relojes de la verdad, eventos mínimos, indicadores, tableros por actor, alertas, autonomía, anomalías, secuencia, 2 anexos | Entregable, versionado. **Pendiente de actualizar** con los hallazgos de la sección 5 |
| `gestores-sura/v4/Gestores_Seguimiento_Requerimientos_2026.xlsx` | Insumo del cliente, 5 hojas | Insumo, ya analizado |
| `gestores-sura/v3/currentDesigns/*.drawio` | Diseños vigentes del cliente, 2 archivos, 9 vistas | Insumo, ya analizado |
| `gestores-sura/v3/_borradores/` | Notas locales de la iteración previa | No se entregan |

### Estructura de la propuesta principal (v3)

Portada → Introducción → 9 partes → anexos.

1. Dónde está hoy la solución · 2. Hallazgos principales (7) · 3. Qué se decide ahora ·
4. Arquitectura agéntica de referencia · 5. Acertividad: cómo medirla y refinarla ·
6. Madurez, autonomía y gobierno · 7. Decisiones a cerrar (12 fichas D1–D12) ·
8. Preguntas del equipo respondidas · 9. Riesgos y secuencia. Anexos A–D.

Las 6 propuestas: **P1** traza y evento comunes · **P2** verdad de referencia desde
preradicado · **P3** compuerta antes de producción · **P4** escala de madurez conectada a
la API de autonomía · **P5** auditor pasivo con compuerta · **P6** umbral derivado del
costo del error.

### Estructura de la torre de control (v4)

Objetivo → Punto de partida → Qué es y qué no es → 5 capas → 3 relojes → Eventos mínimos →
Indicadores → Tableros por actor → Alertas → Autonomía → Anomalías → Secuencia → Riesgos →
Anexo A estándares → Anexo B coherencia con v3.

**Las 5 capas**: 1 ingesta y consolidación · 2 correlación y contexto · 3 medición y
evaluación · 4 decisión y actuación · 5 exposición.

**Los 3 relojes de la verdad** (pieza central y diferenciadora):
inmediato en segundos, la compuerta; medio en horas o días, la corrección humana;
tardío en semanas, glosas, casos revocados, reclamaciones y tutelas. Solo el tardío
revela el error caro.

---

## 3. Decisiones de forma y estilo

- **Sistema de diseño**: hoja de estilos compartida entre v3 y v4. Poppins, violeta
  `#280265`, acento `#5300DF`, ámbar `#B9720A`. Logos embebidos en base64, sin
  dependencias externas salvo Google Fonts.
- **Escala tipográfica en `em`** relativa al cuerpo, con valores fijos en `@media print`
  para no alterar el PDF. Los títulos nunca más pequeños que el párrafo que titulan.
- **Navegación lateral** en pantalla, oculta en impresión. Salto de página por parte.
- **Cuerpo liviano, anexos cargados**. El cuerpo de v3 quedó en ~25 mil caracteres y los
  anexos en ~14 mil.
- **Las figuras hacen trabajo**, no decoran. 11 figuras en v3, 6 en v4.
- **Anatomía fija por propuesta**: qué habilita, qué problema ataca, cómo se ve, qué
  cuesta, cómo se verifica, qué acuerdos requiere. El campo de valor siempre dice **lo que
  se podrá afirmar después y hoy no**.
- **Fichas de decisión** con contexto, recomendación, dueño y fitness function.
- **Verificación técnica antes de entregar**: anclas de índice, balance de etiquetas, ids
  únicos, y que ningún texto de las figuras se desborde de su lienzo ni de su caja.

---

## 4. Terminología acordada

Regla: **usar el término correcto, aunque esté en inglés**, y preferir la etiqueta que el
cliente ya usa en sus diagramas.

| Usar | No usar |
|---|---|
| core, SuraHis | núcleo, núcleo de registro |
| AI Control Plane | plano de control de IA |
| LLM Gateway | puerta de modelos |
| Prompt Management | gestión de prompts |
| runtime agéntico | tiempo de ejecución agéntico |
| golden set | conjunto de oro |
| modo shadow, canary | sombra, canario |
| LLM-as-a-judge | modelo como juez |
| control plane (concepto genérico) | plano de control |
| análisis actuarial | actuaría |
| lago de datos | "al lago" a secas |
| agregar sin reprocesar lo registrado | retrofitear |

Se conservan por ser vocabulario del cliente o del negocio: **acertividad**, bandeja,
preradicado, glosa, meta-estados, rescate digital, siniestro padre, ANS, tutela, PQRS,
integralidad, reestudio, toque cero.

Se conserva **compuerta de regresión** en español; si se decide, pasa a *gate*.

---

## 5. Hallazgos del archivo de seguimiento del cliente (31-ago-2026)

Veredicto: **complementarios, no excluyentes**. Nada invalida la propuesta.

### Lo que el archivo valida

- Riesgo 10: *"no se verifica que el servicio facturado se haya prestado realmente"*,
  declarado fraude estructural no mitigado → es exactamente lo que mide el reloj tardío.
- Riesgo 9: presión regulatoria sobre explicabilidad citando **EU AI Act, NAIC y Colombia**
  → justifica el anexo de estándares.
- Requisito técnico 12: reutilizan el agente de pre-radicación de EPS con **~93% de
  precisión** → línea base contra la cual medir el golden set.
- Requisito técnico 44: **~600.000 autorizaciones/mes** frente a 20.000 de reembolsos →
  el costo por caso pesa, y multiplica por seis la carga de Siniestro Integral.
- Requisitos técnicos 31, 32, 54 y 55: EDA, bus compartido, suscripción a la **totalidad**
  de los eventos, y un evento por cada cambio de estado → es nuestra capa 1 y P1.

### Pendientes del cliente que nuestra propuesta cierra

- **Requisito técnico 52**: *"El nivel de autonomía de ejecución de cada agente (recomendar
  vs. ejecutar) determina con qué sistemas debe conectarse y qué capacidades de escritura
  requiere; pendiente de definir antes de dimensionar el desarrollo."* → P4 y el semáforo.
- **Requisito funcional 90**: concepto de "gestor auditor" con autoaprendizaje sobre las
  decisiones del Gestor de Evaluación, **parqueado el 26-ago** → P5 con compuerta.
- **Requisito técnico 33**: si se expone una API única con filtrado por perfil o varias por
  actor → nuestra capa 5 recomienda filtrar por perfil antes de construir la vista.

### Las tres colisiones a corregir

1. **"La torre no ejecuta" es falso.** Requisitos 49, 50, 51 y 92 piden intervenir otros
   gestores, rescate digital automático, bloqueo de duplicados y reasignación automática
   por vencimiento. Consecuencia en el idioma del estándar: la torre necesita identidad
   propia, alcance de escritura mínimo, registro por acción y **su propio nivel de
   autonomía**. Se mantiene la frontera: no decide el negocio, autorizar, negar o coordinar.
2. **La palabra "nivel" ya significa tres cosas.** Escalamiento humano 1–4 (funcional 23:
   automático, administrativo, enfermeras, médicos) · madurez agéntica 1–3 de Coordinación
   (técnico 25: determinístico, explicativo, autónomo) · nuestra madurez 1–4. Hay que
   renombrar la nuestra y mapearla contra las otras dos.
3. **Custodia de reglas.** Nuestro acuerdo decía core como custodio único. El técnico 3 dice
   que el core es fuente de verdad transaccional **y no motor de reglas**, y el riesgo 3
   advierte romper la filosofía coreless si el core absorbe lógica. El técnico 51 aclara que
   Gestores tiene estados propios, como preradicado, que SuraHis no tiene.

### Techos de autonomía ya decididos por el negocio

- **La negación nunca es 100% automática** y siempre exige evaluador humano (funcional 21);
  además **debe ser determinística y trazable, nunca probabilística** (técnico 20).
- **Autorización automática solo para servicios nivel 1**; niveles 3 y 4, alto costo o
  riesgo, siempre a evaluación manual (funcional 15).
- Nuestro semáforo de autonomía debe respetar esos techos. Hoy la figura muestra autonomía
  en alto costo, lo cual contradice la decisión del cliente.

### Realidad de fuentes que corrige nuestra Figura 1

- **Principio de responsabilidad única** (funcional 66): si Gestores necesita un dato de
  interoperabilidad, lo pide vía SuraHis; conexión directa solo si el core no lo tiene.
- **No existe interoperabilidad de agenda** (técnico 41). Agenda sale como fuente.
- **OTP y clave dinámica quedaron fuera de alcance** de esta fase (funcionales 43, 44, 60).
- Interoperabilidad clínica limitada hoy a consulta externa, ~30% de prestadores
  (funcional 77, riesgo 11).

### Dependencias de secuencia

- Riesgo 2: el proyecto solo funciona si los cores exponen información vía API a tiempo;
  **SuraHis estima 6 o 7 meses**.
- Técnico 35: **Datalake de autorizaciones en el Release 3, feb–abr 2027**.
- Consecuencia: la acertividad se puede medir desde el día uno con eventos propios de
  Gestores; el reloj tardío llega con el Datalake.

### Frente paralelo a resolver

**Requisito técnico 50**: existe otra propuesta de torre de control sobre la mesa, una
arquitectura de **9 agentes** especializados, radar, riesgo operacional, capacidad,
predictor, director del tráfico, marcos de actuación, anomalías, explicador y recomendación,
más un "comandante de operaciones" a futuro con ejecución directa. Está *por validar*, con
el pendiente de revisarla agente por agente contra casos de uso reales.

No compite con la nuestra: esa propuesta define **quién hace el trabajo**; la nuestra,
**qué debe producir la torre y con qué gobierno**. Nuestro criterio de admisión, qué
decisión cambia cada capacidad, más los 9 ejes de su catálogo, resuelven ese pendiente.

### El catálogo de monitoreo del cliente

Hoja "Variables de monitoreo": 9 ejes, 88 variables. Demanda · Inventario · Oportunidad
(ANS) · Capacidad operativa · Calidad · Experiencia cliente · Riesgos operativos · Impacto
financiero · Automatización y transformación. Incluye **Toque cero**, **Casos revocados**,
**Reprocesos**, **Reaperturas**, **Fuera de ANS**, **Casos sin movimiento**, **Tutelas
activas**, **Cliente PEP**.

**Se mantiene tal cual.** Nuestros indicadores agénticos se enchufan ahí: acertividad por
campo y respaldo verificable en Calidad; deriva y consistencia en Riesgos operativos; costo
por caso correcto en Impacto financiero; nivel de autonomía en Automatización.

---

## 6. Reglas de tono y de relación con el cliente

- Son **sugerencias debatibles y descartables**, construidas sobre su diseño, no una
  alternativa a él. Cada una se puede tomar, ajustar o dejar sin que caigan las demás.
- **No juzgar.** Nada de "hallazgos" como vocabulario de auditoría en el cuerpo, ni de
  secciones que "responden" sus preguntas como si fueran tarea corregida. Sus anotaciones
  se citan textualmente **dentro** de la propuesta que motivan.
- **Recomendación firme con secuencia**, no un menú de opciones sin criterio.
- Declarar **qué no proponemos**, temprano y explícito.
- **Nunca mencionar** las iteraciones internas ni versiones previas del documento. Para el
  cliente esto es una sola propuesta.
- Ninguna norma citada obliga a SURA en Colombia: se presentan como **referencia de
  mercado y defensa razonable**, no como cumplimiento exigible.
- **Sin jerga inventada** y sin traducciones literales que obliguen a traducir de vuelta.

---

## 6b. Regla de oro sobre las fuentes

Está escrita como política del repositorio en `CLAUDE.md`. En resumen: **solo fuentes
oficiales del emisor y solo versiones liberadas.** Nunca sitios de terceros, nunca
borradores ni especificaciones en desarrollo, y verificar la URL antes de citar. La práctica
de fabricante se cita desde su sitio oficial y se etiqueta como práctica, no como norma. Y
no citamos plazos de trabajo de otros equipos como si fueran nuestros.

Y una segunda regla que la complementa: **todo estándar debe ser citable con enlace
oficial, en el mismo bloque donde se afirma.** No basta con tener las fuentes en una lista
de referencias al final: quien lee una afirmación debe poder verificarla ahí mismo. Si no
hay enlace oficial, la afirmación se reformula como opinión propia o se elimina.

Correcciones ya aplicadas por estas reglas, para no repetirlas:

- El Reglamento europeo de IA se citaba desde `artificialintelligenceact.eu`, un sitio de
  seguimiento de terceros cuyas páginas advierten que la traducción es generada por
  máquina. Ahora se cita desde **EUR-Lex**, texto del Diario Oficial en español, con
  anclas por artículo del tipo `#art_14` y `#anx_III` sobre
  `legal-content/ES/TXT/HTML/?uri=CELEX:32024R1689`.
- Las convenciones semánticas de OpenTelemetry para IA generativa se citaban como
  estándar, pero esas páginas están marcadas como trasladadas y sin mantenimiento, y las
  convenciones viven en un repositorio aparte todavía en desarrollo. Ahora se cita la
  **versión liberada 1.44.0** de las convenciones semánticas, y se declara explícitamente
  que la parte de IA generativa está en desarrollo, recomendando fijar esquema propio.


- Las afirmaciones que invocaban "la práctica documentada" sin enlace ahora lo llevan
  inline: gestión del ciclo de vida, ciclo de vida de desarrollo, pruebas de agentes,
  arquitectura agéntica y agentes jerárquicos.
- El contexto colombiano citaba el régimen de datos y de historia clínica sin fuente. Ahora
  enlaza la Ley 1581 de 2012 en el Gestor Normativo de Función Pública y la Resolución 1995
  de 1999 en el sitio del Ministerio de Salud.

## 7. Fuentes del sustento

### Del cliente
- `Arquitectura-Gestores.drawio`, 8 vistas: Arq gestores V2, Gestor de monitoreo, Detalle,
  Gestor de finalización, Arq gestores base, Descartado, Resumen, Página-7.
- `Arquitectura-Gestores-General Transversal.drawio`, vista multi-línea de negocio.
- `Gestores_Seguimiento_Requerimientos_2026.xlsx`, 5 hojas: Requisitos Funcionales (99),
  Variables de monitoreo (88), Requisitos Técnicos (55), Riesgos (21), NEXO (3).

### Práctica documentada, IBM Think
Arquitectura agéntica · componentes de agentes · agentes jerárquicos · sistemas multiagente ·
flujos agénticos · orquestación · **plano de control de agentes** · evaluación de agentes ·
pruebas de agentes · AgentOps · ADLC · gestión del ciclo de vida · gobierno de agentes ·
seguridad · proliferación · tool calling · memoria · agentes en sanidad · y los tutoriales de
evaluación, observabilidad con trazas, telemetría, human-in-the-loop y agente listo para
producción. En total 27 páginas leídas.

### Estándares verificados
- **OpenTelemetry**, convenciones semánticas para IA generativa, incluidos *agent spans*,
  spans, métricas y eventos.
- **ISO/IEC 42001:2023**, sistema de gestión de IA. **ISO/IEC 23894:2023**, gestión de riesgos.
- **NIST AI RMF 1.0** y su Playbook, funciones gobernar, mapear, medir, gestionar.
- **EU AI Act**: art. 12 registro de eventos · art. 14 supervisión humana proporcional al
  nivel de autonomía · art. 15 exactitud y robustez · art. 19 logs automáticos · art. 72
  monitoreo posterior · **Anexo III 5(a) y 5(c)**, elegibilidad a servicios de salud y
  evaluación de riesgos y tarificación en seguros de vida y salud.
- **NAIC**, boletín modelo sobre uso de IA por aseguradoras, dic-2023, exige un programa
  escrito proporcional al riesgo.
- **EIOPA**, opinión sobre gobernanza y gestión de riesgos de IA, ago-2025.
- **SFC Colombia**: no hay norma específica de IA agéntica; aplica el régimen de datos
  sensibles y de historia clínica. La SFC ha comunicado su enfoque con humano en el bucle.
- Literatura: *Building Evolutionary Architectures* (fitness functions), *Team Topologies*,
  proceso de asesoría de arquitectura de Thoughtworks, último momento responsable, puertas
  de una vía y de dos vías, Cynefin.

---

## 8. Cambios aprobados y pendientes de aplicar en v4

Aprobados en enfoque el 31-ago-2026, **sin aplicar todavía**:

**Por fidelidad, obligatorios**
1. La torre sí ejecuta acciones operativas → reformular la delimitación, y darle identidad,
   alcance de escritura, registro y nivel de autonomía propio.
2. Corregir el acuerdo de custodia de reglas y matizar el de estados.
3. Renombrar nuestra escala de madurez y mapearla contra las otras dos escalas de "nivel".
4. Respetar los techos de autonomía: negación siempre determinística con humano, alto costo
   siempre manual. Corregir la figura del semáforo.
5. Corregir fuentes en la Figura 1: señales tardías vía SuraHis, sin agenda, sin OTP.

**Adiciones que refuerzan el enfoque**
6. Tabla que enchufa nuestros indicadores agénticos en sus 9 ejes, dejando su catálogo intacto.
7. Mapeo contra la propuesta de 9 agentes, con nuestro criterio de admisión.
8. Sección corta de dependencias y qué se puede medir antes de que el core exponga sus API.

**Dado de baja**: ampliar el documento con capacidad y carga de trabajo. Es monitoreo
operativo, ya está en su catálogo, y la torre solo lo consume como insumo de alertas.

---

## 9. Operación del repositorio

- Repositorio: `didierfrancogomez/propuestas`, rama `main`, remoto https.
- Perfil de gh correcto: **didierfrancogomez**. El otro perfil de la máquina,
  `franco52428`, no es dueño de ese remoto.
- `.gitignore` con `.DS_Store`, `._*` y `Thumbs.db`. Los `.DS_Store` ya no se versionan.
- La carpeta externa `~/Documents/GitHub/techandsolve` es **otro repositorio sin remoto**,
  con cambios pendientes de la reorganización que movió todo a `propuestas/`.
- Convención: commits directos a `main`, mensajes en español, en minúscula.
- `propuestas/CLAUDE.md` es el punto de entrada automático de cada sesión de Claude Code:
  se carga al inicio en cualquier subcarpeta del repositorio y remite a este archivo. Si se
  mueve o renombra `context.md`, hay que actualizar ese puntero.

---

## 10. Decisiones abiertas del lado nuestro

- Si `compuerta de regresión` pasa a `gate`.
- Cómo se renombra la escala de madurez para evitar la colisión de "nivel".
- Si el mapeo contra los 9 agentes va en el cuerpo o en un anexo.
- Si se archiva o se elimina la carpeta `_borradores` de v3 antes de la entrega final.
