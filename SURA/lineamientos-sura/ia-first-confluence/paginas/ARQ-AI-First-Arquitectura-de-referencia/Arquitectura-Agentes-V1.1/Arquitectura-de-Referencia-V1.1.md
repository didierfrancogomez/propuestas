---
titulo: "Arquitectura de Referencia V1.1."
id: 5666766913
espacio: AFGLYP
version: 7
actualizado: 2026-04-01T20:47:55.588Z
actualizado_por: "Nataly Leal"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > [ARQ] AI First: Arquitectura de referencia > Arquitectura Agentes V1.1."
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5666766913
---

# Arquitectura de Referencia V1.1.

<!-- [macro: tabla de contenido] -->

# 1. Antecedentes y fundamentos

Esta sección presenta los conceptos fundamentales y los análisis previos a la definición propiamente dicha de la arquitectura de referencia.

## IA-FIRST Cómo aproximación

### **Definición estratégica**

“AI First define una ruta de evolución donde la inteligencia artificial se convierte en el principio de diseño para tecnologías, prácticas y procesos”

Es decir:

· La IA no es un complemento.

· No es un feature adicional.

· Es el punto de partida de las decisiones técnicas.

### **¿Qué implica realmente?**

Una aproximación AI-First se caracteriza por:

· **Diseño centrado en IA**: la inteligencia artificial se incorpora desde la concepción de cada solución

· **Transformación profunda y sostenible**: se prioriza la IA antes que métodos tradicionales

· **Aplicación transversal**: impacta IT for IT y IT for Business

Esto cambia completamente la forma de pensar la arquitectura.

No estamos hablando de hacernos la siguiente pregunta:

“Tengo un sistema, ¿le pongo IA?”

Es más bien:

“¿Cómo diseño este sistema para que la IA sea parte estructural de su comportamiento?”

### **Relación con Agentes (según el marco teórico)**

En el documento “Agentes de IA – Fundamentación teórica y mapa tecnológico en SURA” se establece que:

· Los agentes pueden tener distintos niveles de agencia.

· La IA agéntica corresponde a niveles altos de autonomía y capacidad operativa.

· La hiperautomatización combina automatización tradicional con IA avanzada.

Por tanto, IA-First en SURA implica:

· Diseñar soluciones donde los **agentes de IA sean componentes estructurales del ecosistema**.

· Pensar en memoria, razonamiento, herramientas y orquestación desde el principio en la arquitectura.

· Integrar seguridad, observabilidad y gobierno desde el inicio.

### **En términos arquitectónicos IA-First Significa**

1. Evaluar siempre primero si el problema debe resolverse con:

a. Agente

b. Hiperautomatización

c. LLM + herramientas

d. Multi-agentes

1. Diseñar la arquitectura pensando en:

a. Desacoplamiento

b. Orquestación inteligente

c. Persistencia de memoria

d. Evaluación continua

e. Seguridad e identidad propagada

1. Construir una **línea base técnica común** para agentes (frameworks, patrones, gobernanza, infraestructura).

### **Lo que NO es IA-First**

· No es usar Copilot.

· No es hacer un chatbot.

· No es un piloto aislado.

· No es innovación experimental.

Es un **cambio estructural en cómo se diseña tecnología empresarial**.

### **En una frase**

IA-First es adoptar la inteligencia artificial —especialmente arquitecturas basadas en agentes— como principio de diseño obligatorio en el ecosistema tecnológico de SURA, tanto para IT for IT como para IT for Business.

## Retos de Negocio Identificados

1. **Eficiencia operativa y sostenibilidad del modelo de operación.** Existen procesos administrativos, (Por ejemplo, los de suscripción, reclamaciones y soporte) que siguen siendo intensivos en intervención humana, con alta carga repetitiva y dispersión de información.

1. **Gestión del conocimiento y soporte experto distribuido.** La organización tiene importantes bases documentales y conocimiento experto disperso entre áreas de negocio.

1. **Inteligencia en decisiones de negocio y diseño de productos.** Multiples procesos requieren análisis de múltiples variables y colaboración entre dominios. ( En aseguramiento, por ejemplo, diferentes modelos de tarificación, mutualidad, segmentación y oferta)

1. **IT for IT — Productividad y calidad en ingeniería de software.** Alta demanda de desarrollo y mantenimiento de software con recursos limitados.

1. **Transformación del modelo de atención y experiencia del cliente.** Interacción fragmentada con clientes y asesores; procesos lentos en movilidad, salud y PQRs.

## Retos Técnicos Identificados

Ahora, por cada reto de negocio se presentan a continuación los retos técnicos que han sido identificados a la hora de pensar en cómo una arquitectura IA-First de agentes pueda ser efectiva para abordar esos retos.

### Retos técnicos asociados al Reto de negocio 1: Eficiencia operativa y sostenibilidad del modelo de operación

· **Agentes de automatización inteligente (RPA + LLM)** para ejecutar tareas repetitivas dentro de flujos transaccionales, reduciendo intervención humana.

· **Agentes multi‑rol que orquesten tareas entre sistemas** como ERP, OIPA, CRM y portales, permitiendo flujos de punta a punta sin fricción.

· **Agentes colaborativos entre humanos y bots**, orientados a disminuir tiempos de ciclo, reprocesos y errores operativos.

· **Interoperabilidad efectiva con sistemas backend**, garantizando que los agentes puedan interactuar de forma uniforme con APIs y sistemas core.

· **Desempeño y escalabilidad de sistemas de agentes a nivel empresarial**, asegurando que la eficiencia lograda se mantenga cuando los volúmenes crecen.

### Retos técnicos asociados al reto de negocio 2: Gestión del conocimiento y soporte experto distribuido

· **Agentes RAG (Retrieval‑Augmented Generation)** para búsqueda semántica y respuesta contextual sobre políticas, manuales, productos y normativas.

· **Sistemas multiagente con sub‑agentes especializados por dominio** (legal, médico, comercial), que permitan razonamiento experto distribuido.

· **Memoria semántica y episódica**, orientada a retener contexto entre interacciones y habilitar aprendizaje continuo de los agentes.

· **Arquitectura de Datos adecuada para agentes**, que garantice disponibilidad, calidad y consistencia de la información consumida.

· **Cumplimiento de MAGI en la información operativa y dominios de conocimiento**, asegurando que los agentes usen información gobernada y apta para producción.

· **Acceso seguro y controlado a datos con cumplimiento normativo**, reforzando trazabilidad y confianza en el uso del conocimiento.

### Retos técnicos asociados al Reto de negocio 3: Inteligencia en decisiones de negocio y diseño de productos

· **Agentes colaborativos y orquestados que integren datos de producto**, incluyendo portafolio, políticas, topes y cláusulas.

· **Integración mediante APIs a lo largo del ciclo de vida del producto**, permitiendo que los agentes participen en análisis, simulación y diseño.

· **Interoperabilidad backend consistente**, que facilite la agregación confiable de información proveniente de múltiples fuentes.

· **Marco unificado de orquestación de agentes**, habilitando coordinación, gobernanza y trazabilidad de decisiones automatizadas.

### Retos técnicos asociados al Reto de negocio 4: IT for IT — Productividad y calidad en ingeniería de software

· **Modelo de Madurez de Calidad (Excelencia TID)** enfocado en pruebas, mantenibilidad, clean code y adecuación a casos de uso de IA.

· **Redefinición de prácticas y escenarios de prueba** que ya no aplican o deben evolucionar en aplicaciones AI Native.

· **Evaluación de calidad en agentes No‑Code**, ya sean de terceros o provenientes de comunidades certificadas.

· **Agentes para creación y adopción de templates**, que guíen a los equipos de dominio en buenas prácticas técnicas.

· **Observabilidad y monitoreo adaptados a agentes autónomos**, permitiendo entender cadenas de decisión y dependencias técnicas.

· **Marco unificado para orquestación y gobernanza técnica**, reduciendo complejidad y deuda arquitectónica.

### Retos técnicos asociados al reto de negocio 5: Transformación del modelo de atención y experiencia del cliente

· **Agentes conversacionales multimodales (voz, texto, imágenes)** integrados con CRM para atención más natural y contextual.

· **Multi‑agentes transaccionales que conecten canales digitales y backend**, incluyendo WhatsApp, portales, apps y sistemas core.

· **Uso de memoria episódica para personalización y seguimiento contextual**, mejorando continuidad de la experiencia.

· **Interoperabilidad backend y escalabilidad de agentes**, garantizando consistencia de la experiencia incluso en picos de demanda.

· **Acceso seguro a datos y cumplimiento normativo**, clave para mantener confianza del cliente.

### Retos técnicos transversales (Aplican a todos los retos de negocio)

Existen retos técnicos que no pertenecen a un único dominio de negocio, sino que **habilitan de manera transversal** toda la estrategia de agentes:

· **IA Responsable y Auditable**, como principio base de confianza, explicabilidad y control.

· **Interoperabilidad consistente con sistemas backend**, reduciendo heterogeneidad técnica.

· **Marco unificado de orquestación de agentes**, enrutamiento de mensajes y automatización.

· **Observabilidad y monitoreo de sistemas de agentes**, adaptados a autonomía y toma de decisiones.

· **Acceso seguro a datos, cumplimiento normativo y trazabilidad**.

· **Desempeño y escalabilidad a nivel empresarial**.

· **Barreras culturales y de adopción**, abordadas mediante comunicación, capacitación y comunidades.

· **Gobernanza de información y cumplimiento MAGI** para operación en producción.

## Prácticas de industria y arquitecturas emergentes

### Arquitecturas emergentes para la construcción de agentes

Tomando como base el documento *“Agentes de IA – Fundamentación teórica y mapa tecnológico en SURA”* construido por el laboratorio de IA y con el enfoque estratégico **AI First** definido para la organización se muestran los **Patrones de desarrollo para Agentes basados en LLMs contenidos en la sección 2.1** donde se estructuran los elementos necesarios para diseñar, implementar y operar agentes dentro del ecosistema tecnológico empresarial.

Los **patrones arquitectónicos principales** definidos en el documento son:

· **Agente Singular:**Implementación monolítica donde un único agente concentra procesamiento, memoria y herramientas. Adecuado para tareas de complejidad baja o moderada.

· **Agente con Roles.**Un mismo agente configurado con distintos comportamientos o personalidades funcionales. Útil cuando se requiere coherencia funcional específica (por ejemplo, asesor experto).

· **Multi-agentes.**Sistema compuesto por múltiples agentes especializados que colaboran o se orquestan. Indicado para problemas complejos, multifacéticos o distribuidos.

![image-20260312-140706.png](../../../recursos/5666766913/image-20260312-140706.png)

¿Pero cómo se estructuran estos tres tipos de arquitectura en el contexto particular de SURA?

Eso es lo que se pretende definir en la siguiente sección, teniendo en cuenta que esta versión del documento se limita solo a la definición de la arquitectura de “Agente singular”

# 2. Arquitectura de Referencia (Linea Base)

Esta sección busca definir la manera en que al día de hoy deben implementarse agentes en SURA. Se convierte entonces en la línea base de la arquitectura de referencia sobre la que se pretende evolucionar de una manera ágil en lo que más adelante se comienza a definir como arquitectura de referencia deseada (To-Be)

La separación se hace básicamente teniendo en cuenta los artefactos y plataformas transversales disponibles al día de hoy y se complementa con la arquitectura de implementación definida en documento aparte.

## Modelo de decisión Base

Lo primero que hay que preguntarse a la hora de diseñar un agente basado en IA es: ¿Realmente necesito un agente para resolver el problema de negocio?, luego de haber respondido eso, aterrizar el diseño estructural requiere plantear qué patrón general de agentes es adecuado usar: “¿Agente singular? ¿Agente singular con roles? ¿Multi-Agentes?” El módelo presentado a continuación busca entregar una guía para responder a esas preguntas:

### ¿Agente, IA Generativa simple o aplicación tradicional?

El siguiente es un modelo de decisión simple, que en esta primera versión de la arquitectura resume las conversaciones tenidas en la comunidad de IA respecto a la pertinencia de usar o no agentes.

Partiendo de la base de que es necesario construir una solución para un proceso de negocio, se debe responder a las siguientes preguntas para saber si es necesario implementar un sistema de agentes:

**P1.** ¿El proceso se puede describir como reglas claras y estables (Con entradas, reglas y salidas deterministas) y cambia poco?

· **Sí** → Utilice una **Aplicación tradicional** (App transaccional, workflow, formularios, motor BPM/BRMS).

· **No** → sigue.

**P2.** ¿La dificultad principal (en la implementación de la solución) es entender lenguaje natural, documentos, conversaciones, o contextos ambiguos?

· **No** → **Aplicación tradicional** (quizá con analítica/ML puntual si aplica).

· **Sí** → sigue.

**P3.** ¿La solución debe **tomar acciones** en un orden que puede variar (consultar sistemas, decidir próximos pasos[[NR1]](#) [[DG2]](#) , coordinar tareas) y no solo “responder” o “resumir”?

· **No** → normalmente **NO necesitas agente**: usa **IA Generativa**dentro de una app (chat/RAG/extracción) con un flujo controlado.

· **Sí** → sigue.

**P4.** ¿Un error del proceso puede causar impacto alto (dinero, legal, salud, reputación, pérdida de datos)?

· **Sí** → **Agente IA con humano en el loop** (aprobación antes de ejecutar acciones).

· **No / Bajo** → sigue.

**P5.** ¿Tienes capacidad de operación y control? (logs/auditoría, límites, monitoreo de calidad, rollback, seguridad/permisos mínimos)

· **No** → mejor **Aplicación tradicional** o **IA asistida** acotada.

· **Sí** → **Agente IA** es buena opción.

En términos generales:

· Se debe utilizar una**Aplicación tradicional** si la solución implica reglas claras y deterministas, hay alto riesgo, se requieren SLAs estrictos y mucha estabilidad.

· **Agente IA** si se necesite interpretar el lenguaje natural, hay ambigüedad, se necesita actuar en varios pasos, hay riesgo bajo/medio (o con aprobaciones) y por último, si se puede operar bien.

Ejemplos:

· **Tradicional:** cálculo de primas, validaciones normativas, conciliaciones contables, reglas de elegibilidad, flujos con pasos fijos.

· **Agente IA:** triage de casos, coordinación de tareas entre sistemas, soporte operativo con diagnóstico/acciones guiadas, atención interna donde cambian preguntas y rutas.

La siguiente imagen resume el flujo:

![Decisión 1.png](../../../recursos/5666766913/Decisión 1.png)

### ¿Patrónes Multi-Agente, Agente singular o Agente Singular con Rol?

Una vez definida la necesidad de usar agentes para un problema determinado es necesario identificar el patrón arquitectónico adecuado.

Opciones de patrones:

A. **Agente Singular.**

B. **Agente con Roles.**

C. **Multi-Agentes.**

**Paso 0 — Define el objetivo y el “trabajo” del agente**

Antes de elegir patrón, escribe en 3 líneas:

· Qué tarea resuelve (resultado esperado).

· Qué entradas usa (texto, documentos, imágenes, señales, eventos).

· Qué herramientas debe ejecutar (APIs, BD, colas, flujos, etc.).

El objetivo aquí es evitar elegir el patrón más complejo de multi-agentes “por moda” y concretar el alcance.

**Paso 1 — Evalúa complejidad, multifaceticidad y escalabilidad requerida**

¿El proyecto aborda tareas de alta complejidad o entornos multifacéticos que requieren segmentación de responsabilidades y alta escalabilidad?

La respuesta puede ser positiva si:

· Tarea alta y multifacética (varias habilidades o dominios a la vez).

· Necesitas concurrencia real (varias cosas en paralelo).

· Crece por módulos (nuevas capacidades frecuentes) y quieres flexibilidad.

· Hay muchas herramientas o integraciones heterogéneas.

Si la respuesta es **Sí** la opción adecuada es **C: Multi-Agentes**

Justificación: permite especialización, distribución de carga y handoff dinámico.

Trade Off: Se asume mayor complejidad de coordinación y observabilidad

Si la respuesta es **No,** pasa al **Paso 2.**

**Paso 2 — Decide si necesitas rol/persona para alinear el comportamiento**

¿La solución requiere que el agente adopte una personalidad o rol concreto para alinear su comportamiento?

La respuesta puede ser positiva si:

· Debe comportarse como asesor experto, agente de soporte, gestor, auditor, etc.

· Necesitas coherencia conversacional (tono, estilo, políticas, criterios de decisión) como parte del producto.

· La “forma” de responder es tan importante como el “qué” responde.

Si la respuesta es **Sí**, la opción adecuada es **B: Agente con Roles**

Justificación: el rol condiciona el comportamiento y mejora coherencia/alineamiento para funciones específicas.

Si la respuesta es **No,**pasa al **Paso 3**.

**Paso 3 — Elige simplicidad y trazabilidad como criterio dominante**

Si llegaste aquí, estás en tareas baja a moderada, objetivos bien definidos y sin necesidad de “humanización” fuerte.

La opción adecuada es **A: Agente Singular**

Justificación: implementación única con herramientas integradas; ideal para tareas acotadas y alta trazabilidad/monitoreo (más simple de operar y auditar).

**Paso final: validar la decisión con algunos tips:**

Si la prioridad de trazabilidad/monitoreo es MUY alta (auditoría estricta, compliance, post-mortems frecuentes): Prefiere Agente Singular o Agente con Roles.

Solo ve a Multi-Agentes si la complejidad lo hace inevitable y estás dispuesto a invertir en observabilidad.

Si necesitas mucha flexibilidad y evolución, pero hoy el caso es simple, empieza con Agente Singular (o Roles si aplica) con diseño modular; deja preparada la ruta para escalar a multi-agentes cuando la complejidad lo exija.

Si el rol puede volverse rígido o ambiguo (Es decir, ves muchas funciones contradictorias bajo “un solo rol”). Entonces tienes dos opciones: O aclaras y acotas el rol, o debes considerar usar el patrón multi-agentes (Para separar responsabilidades).

Al final, tu decisión debe quedar en una frase, por ejemplo:

· A. Agente Singular: “Tiene una tarea acotada, sin rol fuerte y requiere máxima trazabilidad”.

· B. Agente con Roles: “Tiene una cantidad de tareas moderada, debe tener coherencia por rol/persona”.

· C. Multi-Agentes: “Tiene alta complejidad, es multifacético, requiere segmentación y escalabilidad/flexibilidad”.

![image-20260312-140817.png](../../../recursos/5666766913/image-20260312-140817.png)

## Atributos de calidad perseguidos

Durante las conversaciones de comunidad de IA que dieron origen a esta arquitectura se definieron en términos simples los aspectos que deberían ser priorizados a la hora de construir agentes y teniendo en cuenta la realidad de Sura:

- **Trazabilidad de decisiones y acciones.** Dados los dominios de solución sobre los cuales se mueve Sura, las soluciones de agentes deben poder ser trazables en todo su flujo de trabajo. Cualquier acción que tomen debe poder ser auditable.

- **Mantenibilidad y facilidad de evolución.** Una realidad histórica en Sura es que debido a la heterogeneidad de sus sistemas y la rápida evolución de los equipos y los negocios, la mantenibilidad cada vez es más importante.

- **Eficiencia operativa y de recursos.** Para alinearse incluso con la estrategia de la compañía en términos de incrementar la eficiencia operativa es necesario construir sistemas que sean faciles de evolucionar y que hagan un uso adecuado y con el mínimo desperdicio de los recursos disponibles.

- **Cumplimiento normativo y Seguridad**. Sura es una empresa altamente regulada y esto exige tener un especial cuidado en el cumplimiento de la normatividad y en la seguridad de las aplicaciones.

- **Adaptabilidad creciente (futuro).**Uno de los aspectos que se mencionaron bastante en las reuniones de comunidad fue la necesidad de que pudieramos iterar rápido con las soluciones y adaptarnos a la vertiginosa velocidad que tiene el mundo de IA. Lo que se busca es tener una capacidad de resiliencia al cambio en las soluciones de agentes.

Los términos anteriores están en función de las necesidades expresadas desde el análisis, pero con el objetivo de trasladarlas a un marco estandar realizamos una homologación de conceptos con las normas existentes para Productos de software, Sistemas de IA, y Datos.

De esta manera obtenemos el listado final de atributos de calidad priorizados que se ve en la siguiente tabla.

Se espera que todo diseño estructural de sistemas de agentes en SURA priorice los siguientes atributos.

| **Atributo de Calidad Prioritario** | **Sinónimos / Relacionados** | **ISO/IEC 25010 (Producto Software)** | **ISO/IEC 25059 (Sistemas IA)** | **ISO/IEC 25012 (Datos)** |
| --- | --- | --- | --- | --- |
| **Trazabilidad de decisiones y acciones** | Auditabilidad; Rastreabilidad; Rendición de cuentas (*accountability*); No repudio; Transparencia (explicabilidad) | **Seguridad - Responsabilidad y No repudio:** subcaracterísticas que garantizan que las acciones pueden atribuirse al actor y no negarse. Soporta auditoría de agentes. **Mantenibilidad - Analizabilidad:** un sistema bien instrumentado con trazas facilita diagnosticar causas y entender el comportamiento. | **Transparencia & Explicabilidad:** el modelo de calidad IA evalúa la *trazabilidad de las decisiones* como parte de la explicabilidad, exigiendo poder seguir el razonamiento del agente. **Regulaciones IA:** la trazabilidad contribuye al cumplimiento de requisitos como el EU AI Act que piden transparencia. | **Trazabilidad de datos:** característica que define la capacidad de auditar el ciclo de vida completo de los datos. Asegura que los datos (ej. registros de eventos de agentes) conserven su historia, apoyando auditorías. |
| **Mantenibilidad y facilidad de evolución** | Facilidad de mantenimiento; Evolutividad; Modificabilidad; Extensibilidad; Reusabilidad; Testeabilidad | **Mantenibilidad:** característica principal que abarca modularidad, analizabilidad, modificabilidad, reusabilidad y comprobabilidad (test). Garantiza poder corregir y adaptar el sistema con facilidad. | *(No introduce nuevas categorías; aplica mantenibilidad general).* *(Posible énfasis en mantenibilidad de componentes IA, pero cubierto en el marco general.)* | *N/A directa.* (La calidad de datos no incluye mantenibilidad de software). |
| **Eficiencia operativa y de recursos** | Rendimiento; Performance; Escalabilidad (de rendimiento); Optimización; Capacidad; Utilización de recursos | **Eficiencia de desempeño:** característica principal con subcaracterísticas *Comportamiento temporal*, *Utilización de recursos* y *Capacidad*. Mide tiempos de respuesta, throughput y uso óptimo de CPU, memoria, etc. | **Rendimiento de IA:** mantiene foco en eficiencia (ej. tiempo de inferencia, manejo de datos incompletos sin degradar rendimiento). **Recursos limitados:** incorpora consideraciones de eficiencia en contextos como Edge AI. | **Eficiencia de datos:** datos que permiten procesamiento con niveles de rendimiento esperados. Implica que la estructura/calidad de datos no entorpece el desempeño (ej. datos consistentes y accesibles favorecen consultas más rápidas). |
| **Cumplimiento normativo y Seguridad** | Compliance; Conformidad; Regulaciones; Gobernanza; Seguridad de la información; Confidencialidad; Integridad; Autenticidad; Disponibilidad; Privacidad | **Seguridad:** característica principal abarcando *Confidencialidad, Integridad, Autenticidad, No repudio, Responsabilidad*. Cubre protección de información y accountability. **(Cumplimiento normativo):** no es subcaracterística explícita; se aborda como requisito externo que el software debe satisfacer (ej. funciones o restricciones adicionales según leyes). | **Ética y cumplimiento en IA:** calidad IA enfatiza *alineación con consideraciones éticas y regulatorias*. Incluye transparencia, equidad (no sesgos), y mecanismos de control para cumplir futuras leyes de IA. **Seguridad IA:** mantiene los requisitos de seguridad tradicionales, más controles adicionales para mitigar riesgos únicos de IA (p.ej. evitar outputs indebidos). | **Conformidad de datos:** datos con atributos que cumplen estándares/normas vigentes (ej. formatos legales, campos obligatorios por ley). **Confidencialidad de datos:** protección de datos según su naturaleza, acceso solo a roles autorizados. *(Además, integridad, disponibilidad y trazabilidad de datos son relevantes para compliance, aunque ya cubiertos en otros atributos.)* |
| **Adaptabilidad creciente (futuro)** | Flexibilidad; Extensibilidad; Escalabilidad evolutiva; Portabilidad; Configurabilidad; Resiliencia al cambio | **Portabilidad - Adaptabilidad:** subcaracterística que indica capacidad de un sistema de adaptarse a entornos de hardware/soft distintos o en evolución. Permite migraciones tecnológicas fáciles. **Mantenibilidad - Modificabilidad:** facilidad para adaptar el sistema a nuevos requisitos o contextos sin introducir defectos (evolutividad del software). | **Aprendizaje y Adaptación:** característica IA que evalúa si el sistema puede ajustarse efectivamente a nuevas situaciones aprendiendo de datos. **Controlabilidad/Configurabilidad:** posibilidad de intervención y ajuste por usuarios, permitiendo reconfigurar comportamiento sin recodificar (no explícito como característica, pero alineado con prácticas de IA responsable). | **Portabilidad de datos:** capacidad de instalar, reemplazar o migrar datos a otro sistema conservando calidad. Esto apoya la adaptabilidad tecnológica (cambiar de sistema sin perder datos). **Accesibilidad de datos:** datos disponibles para nuevos usos o sistemas futuros (evitar silos inaccesibles que limiten expansión). |

## Modelo Arquitectónico Agnóstico para Agente Singular

En conformidad con el mecanismo estandar de diagramación definido en el método de arquitectura de SURA se presenta a continuación la visión arquitectónica utilizando el modelo C4, desde un punto de vista estructural para la construcción de agentes en SURA.

En esta arquitectura de Referencia se abordan los niveles 1 y 2 de C4 desde un punto de vista agnóstico (Sin tecnologías especificas).

### Nivel 1. Vista de contexto.

![image-20260312-141844.png](../../../recursos/5666766913/image-20260312-141844.png)

El diagrama representa la **vista de contexto del sistema (C4 – Nivel 1)** para la habilitación de agentes de IA en la organización.

En esta vista, el agente no se modela como un componente interno, sino como un **Software System completo**, que interactúa con:

· Actores externos (usuarios, sistemas, eventos).

· Sistemas empresariales.

· Recursos tecnológicos y de información.

El objetivo de esta arquitectura es establecer la base para la construcción de **Agentes Singulares Empresariales**, bajo principios de desacoplamiento, gobernanza y seguridad, alineados con la estrategia AI First y se articula con los lineamientos conceptuales definidos para agentes de IA en SURA (Documento producido por el laboratorio de IA SURA)

#### Actores y Sistemas Externos

En el extremo izquierdo del diagrama se ubican los actores y sistemas que interactúan con el agente:

· Usuario interno o externo.

· Canales digitales.

· Eventos del negocio.

· Servicios corporativos.

· Otros agentes externos.

Estos elementos representan el **entorno del agente**.
 Desde la perspectiva C4, son sistemas o personas externas que consumen o activan el Software System “Sistema de Agente Singular”.

Aquí se materializa la función de **percepción** del agente, pero la lógica no reside en esta capa.

#### Sistema de Agente Singular (Software System)

El bloque central del diagrama corresponde al **Software System principal**:
 **Sistema de Agente Singular en SURA**.

En esta vista C4 Nivel 1 no se detallan componentes internos (eso correspondería a C4 Nivel 2 o 3), pero sí se identifican sus capacidades fundamentales como parte de su responsabilidad sistémica:

El Sistema de Agente Singular es responsable de:

1. Recibir interacciones.

1. Orquestar razonamiento y planeación.

1. Administrar memoria.

1. Invocar herramientas.

1. Ejecutar acciones en sistemas empresariales.

1. Retornar respuestas estructuradas.

1. Garantizar cumplimiento, identidad y trazabilidad.

Es importante enfatizar que en esta fase inicial la arquitectura está orientada a **agentes singulares**, es decir:

· Un único centro de control.

· Un único flujo de orquestación.

· No existe coordinación entre múltiples subagentes.

· No hay handoff dinámico entre agentes.

Esto reduce complejidad operativa y permite consolidar prácticas antes de evolucionar hacia arquitecturas multi-agente.

Es importante tener en cuenta que aquí se presentan capacidades Internas (Representadas a Nivel Conceptual) Es decir, que aunque esta es una vista de sistema (no de contenedores), el diagrama evidencia que el Software System integra conceptualmente:

· Elementos de identidad y políticas.

· Núcleo de orquestación.

· Capacidades LLM.

· Acceso controlado a herramientas y recursos.

Estas capacidades no deben interpretarse como sistemas independientes, sino como **responsabilidades del Sistema de Agente Singular**.

Desde C4 Nivel 1, lo relevante no es cómo están implementadas, sino que el sistema:

· Centraliza la orquestación.

· Gobierna el uso de modelos.

· Controla el acceso a recursos.

· Aplica políticas corporativas.

#### Sistemas Empresariales y Recursos (Lado Derecho del Diagrama)

En el extremo derecho se encuentran los sistemas externos que el agente consume o acciona:

· APIs corporativas.

· Sistemas transaccionales.

· Dominios de conocimiento.

· Servicios MCP.

· RAG.

· Ejecución de código.

· Infraestructura.

Desde la perspectiva C4, estos son **Software Systems externos** con los cuales el Sistema de Agente Singular se integra.

La arquitectura establece un principio fundamental:

El agente no contiene la lógica de negocio transaccional. La orquesta.

Esto protege el core empresarial y evita acoplamientos indebidos.

### Nivel 2. Vista de contenedores.

![image-20260312-141754.png](../../../recursos/5666766913/image-20260312-141754.png)

El presente diagrama describe la estructura interna de un **Sistema de Agente Singular**, entendiendo este como un sistema autónomo que concentra en una única unidad lógica de orquestación las capacidades de:

· Planeación

· Razonamiento

· Gestión de memoria

· Uso de herramientas

· Integración con sistemas empresariales

El diseño está alineado con el enfoque **AI First**, donde la inteligencia artificial se convierte en principio de diseño transversal y se articula con los lineamientos conceptuales definidos para agentes de IA en SURA (Documento producido por el laboratorio de IA SURA)

#### Alcance arquitectónico

El diagrama representa:

· Un **Software System**: *Sistema de Agente Singular*.

· Sus **contenedores internos** (C4 Nivel 2).

· Las integraciones con sistemas externos empresariales.

· Los mecanismos de memoria, observabilidad, seguridad y acceso a conocimiento.

No modela múltiples agentes ni coordinación distribuida; se enfoca en un único agente con responsabilidad unificada.

#### Vista general del Sistema

El sistema está compuesto por tres grandes bloques:

1. Canales de entrada

1. Núcleo del agente (Agent Core)

1. Sistemas Externos

a. Servicios cognitivos (LLM y MCP)

b. Acceso a conocimiento empresarial

c. Capacidades transversales (observabilidad, seguridad e identidad)

#### Contenedores del Sistema

Interfaz de Usuario (Container)

**Responsabilidad:**
 Canal conversacional o de interacción estructurada con el usuario.

Puede materializarse como:

· Aplicación web

· Chat en Teams / WhatsApp

· Portal interno

· API expuesta a otros sistemas

**Función arquitectónica:**

· Recibe instrucciones.

· Envía respuestas.

· Mantiene el contexto de sesión (memoria de corto plazo).

##### Gateway / API Layer (Container)

**Responsabilidad:**
 Capa de exposición y gobierno de APIs para el sistema de agentes.

**Funciones:**

· Autenticación y autorización.

· Propagación de identidad.

· Control de acceso.

· Versionamiento.

· Trazabilidad.

Este contenedor desacopla el canal de entrada del núcleo del agente.

##### Broker / Mensajería (Container)

**Responsabilidad:**
 Permitir integración desacoplada y asincrónica con sistemas empresariales.

**Funciones:**

· Publicación y consumo de eventos por parte del nucleo del agente.

· Manejo de reintentos.

· Resiliencia.

· Integración con flujos empresariales.

Este patrón es coherente con entornos transaccionales distribuidos. Tiene en cuenta las definiciones de integración en SURA que priorizan los mecanismos de integración asincrona y define como dueño del broker la aplicación que requiere proveer servicios para que sean consumidos por actores externos.

##### Agent Core (Software Subsystem)

El **Agent Core** es el subsistema central del sistema y concentra la lógica agéntica.

![image-20260312-142339.png](../../../recursos/5666766913/image-20260312-142339.png)

Contiene los siguientes contenedores internos:

###### Orquestador del Agente Singular (Container)

**Es el cerebro operativo del agente.**

Responsabilidades:

· Interpretar la intención del usuario.

· Diseñar el plan de acción.

· Invocar herramientas.

· Gestionar memoria.

· Controlar iteraciones y límites.

· Consolidar la respuesta final.

· Instrumentación de la observabilidad (Trazas, logs y métricas)

Este contenedor puede implementar patrones como:

· ReAct

· Chain of Thought

· Generación dinámica de planes

· Límites de reintentos

· Respuesta estructurada

###### LLM Gateway (Container)

**Responsabilidad:**
 Abstraer el acceso a modelos de lenguaje.

Funciones:

· Encapsular integración con Azure OpenAI u otros modelos.

· Manejar políticas de uso.

· Controlar costos y tokens.

· Permitir intercambiabilidad de modelo (evitar lock-in).

Este contenedor desacopla el Orquestador del proveedor de LLM.

###### Servicio LLM (Container externo cognitivo)

Representa el proveedor de modelo (ej. Azure OpenAI).

No pertenece al sistema, pero es una dependencia crítica.

###### Persistencia / Memoria (Container)

**Responsabilidad:**
 Gestión de memoria de largo plazo.

Incluye:

· Memoria episódica.

· Memoria de procedimiento.

· Historial conversacional persistente.

Puede implementarse con:

· Base relacional

· Base vectorial

· Base documental

· Grafo

El Orquestador consulta este contenedor antes y durante la planificación.

###### MCP Privado (Container)

**Responsabilidad:**
 Repositorio de herramientas privadas del dominio de la solución del agente.

Permite:

· Function calling controlado.

· Ejecución de capacidades empresariales.

· Acceso a APIs internas.

· Validaciones determinísticas.

Actúa como puente seguro y desacoplado entre el agente y sistemas internos. El objetivo principal de este componente es desacoplar herramientas que son instanciadas por el orquestador, de ningún modo se trata de herramientas que puedan ser compartidas con otros agentes, para esto se definen los MCPs públicos.

##### Sistemas Empresariales Externos

Los sistemas empresariales externos pueden interactura con el agente y este a su vez puede interactuar con otros sistemas empresariales externos.

Con el agente puede ser posible interactuar desde sistemas como:

- Teams

- Whatsapp

Y a su vez el agente puede interactuar con:

· APIs corporativas

· Sistemas transaccionales

· Motores de reglas

· Sistemas legacy

La interacción de salida ocurre a través de:

· MCP Privado

· APIs gobernadas

· Mensajería

###### Sistema Interfaz Externa (Software System)

La interacción con el agente puede originarse desde distintos canales externos tales como portales web, aplicaciones móviles, asistentes conversacionales o plataformas de mensajería empresarial (por ejemplo Teams o WhatsApp). Estos sistemas constituyen **interfaces externas al sistema del agente** y consumen sus capacidades mediante APIs.

![image-20260312-142426.png](../../../recursos/5666766913/image-20260312-142426.png)

###### Sistema Catálogo MCP Público (Software System)

En un sistema como este, el objetivo principal es disponibilizar un conjunto de **Herramientas** que representan funcionalidades, servicios o capacidades específicas que pueden ser consumidas por otros sistemas o agentes dentro del ecosistema organizacional. Estas herramientas pueden abarcar desde validaciones, procesamiento de datos, consultas a bases de datos, hasta integraciones con servicios externos.

La disponibilización se realiza a través del **protocolo MCP**, que actúa como un estándar para la publicación, descubrimiento y consumo seguro de dichas herramientas. Así, mediante el uso de MCP Gateway y servidores MCP públicos, se garantiza que las herramientas estén centralizadas, sean fácilmente accesibles y reutilizables por los diferentes actores, manteniendo control y gobernanza sobre su uso.

**En SURA, todo sistema que requiera exponer capacidades para agentes debe hacerlo en el marco de la estrategia API-LED**, lo cual implica que toda capacidad debe ser expuesta primero por una API de Sistema o de Proceso. Posteriormente, el servidor MCP consume esas APIs, permitiendo que las herramientas y servicios estén disponibles de manera estandarizada, segura y gobernada a través de un MCP Gateway y de un futuro catálogo MCP. Este enfoque facilita la integración modular y la reutilización de capacidades dentro del ecosistema, optimizando la interoperabilidad y la escalabilidad.

Aunque para esta línea base no existe un catalogo completo implementado el ecosistema de la organización busca disponibilizar un catálogo centralizado de herramientas accesibles mediante el protocolo MCP en posteriores iteraciones de esta arquitectura.

Para esta línea base de arquitectuta de referencia, sin embargo, si se define el uso de dos componentes: El MCP Gateway y los MCP Servers.

![image-20260312-142523.png](../../../recursos/5666766913/image-20260312-142523.png)

Incluye:

· MCP Gateway: El MCP Gateway actúa como punto de acceso a estas herramientas, permitiendo que los agentes descubran y utilicen capacidades disponibles dentro de la organización.

· Servidores MCP públicos: Los servidores MCP públicos alojan herramientas reutilizables que pueden ser utilizadas por múltiples agentes.

Función clave del sistema MCP:

· Acceso gobernado a herramientas reutilizables que exponen capacidades de los sistemas de la organización.

###### Acceso al Conocimiento (Software System)

La arquitectura contempla la comunicación del agente, a través de servidores MCP, de los sistemas especializados en la gestión de conocimiento empresarial. Este sistema habilita patrones de Retrieval Augmented Generation (RAG).

![image-20260312-142658.png](../../../recursos/5666766913/image-20260312-142658.png)

Incluye:

· Índices (vectoriales o híbridos).

· Gestor de Ingesta.

· Conexión con el sistema de Dominios de Información del negocio

Este bloque garantiza:

· Gobernanza de fuentes.

· Actualización controlada.

· Separación entre modelo de información (Productos de datos) y conocimiento.

###### Sistema Dominios de Información de Negocio (Sistema externo)

Los sistemas de dominio representan las fuentes oficiales de información empresarial utilizadas por el agente.

Entre ellos se encuentran:

- Catálogo de información corporativa

- Repositorios documentales del dominio

- Repositorios específicos del caso de uso

Estos sistemas son gestionados por los equipos responsables de cada dominio de negocio y constituyen la base de conocimiento utilizada por el agente.

###### Sistema de Observabilidad (Sistema externo)

![image-20260312-143042.png](../../../recursos/5666766913/image-20260312-143042.png)

Sistema externo que centraliza:

· Logs

· Métricas

· Trazas

· Telemetría

Además de métricas y trazas, los sistemas de agentes en SURA deben emitir **logs estructurados** correlacionables con la traza distribuida. Es obligatorio propagar y registrar **traceId/spanId/correlationId** a través de Gateway, Orquestador, llamadas a herramientas (MCP), Broker y dependencias externas, de forma que la auditoría pueda reconstruir una ejecución extremo a extremo.

Es obligatorio para:

· Auditoría

· Cumplimiento regulatorio

· Evaluación de agencia

· Optimización continua

###### Usuario Owner (Actor)

Representa:

· Responsable funcional del agente.

· Configuración de parámetros.

· Supervisión.

· Activación de casos de uso.

Este rol es clave en el marco AI First para asegurar gobernanza técnica y funcional

### Principios Arquitectónicos Implícitos

Este diseño refleja los siguientes principios:

1. **Separación de responsabilidades**

Orquestación ≠ Modelo ≠ Memoria ≠ Herramientas ≠ Conocimiento.

1. **Desacoplamiento**

Integración mediante APIs y mensajería.

1. **Gobernanza y seguridad**

Propagación de identidad.
Guardrails.
Observabilidad obligatoria.

1. **Escalabilidad progresiva**

Aunque es un agente singular, su diseño permite evolucionar hacia:

Agente con roles

Multi-agente

Agent Mesh

1. **Alineación con niveles de agencia (Presentados en los lineamientos conceptuales de agentes)**

El agente puede escalar en autonomía según: Planeación, Uso de memoria, Interacción con entorno, Adaptabilidad.

# 3. Arquitectura de referencia deseada (To-Be)

## Momento 1 (Transición)

El diagrama presentado describe una arquitectura de transición dentro del proceso de evolución de la arquitectura de agentes de IA de la organización. Su propósito es reflejar un cambio estructural importante en la forma en que los agentes consumen modelos de lenguaje, preparando la plataforma para una arquitectura futura más desacoplada, gobernada y reutilizable.

En la arquitectura inicial base, el LLM Gateway se encuentra embebido dentro del Sistema de Agente Singular, lo que implicaba que cada agente gestiona de forma local aspectos como el acceso a modelos de lenguaje, el control de consumo, la aplicación de políticas y la integración con proveedores de LLM. Aunque este enfoque simplifica el desarrollo inicial, y es el enfoque disponible actualmente en SURA, genra riesgos de duplicación de capacidades, falta de gobierno centralizado y dificultades para estandarizar el uso de modelos en la organización principalmente cuando el ecosistema de agentes escale.

La arquitectura presentada aquí introduce un cambio fundamental (Ver en el diagrama en gris claro): la transversalización del LLM Gateway como un sistema externo compartido, convirtiéndolo en una capacidad de plataforma accesible para todos los agentes.

![image-20260312-143323.png](../../../recursos/5666766913/image-20260312-143323.png)

El LLM Gateway deja de formar parte del Sistema de Agente Singular y pasa a convertirse en un sistema independiente dentro del ecosistema de la plataforma de IA.

Esto implica que los agentes ya no gestionan directamente la conexión con los modelos de lenguaje, sino que consumen estos servicios a través de una capa intermedia centralizada.

Esta capa actúa como punto único de acceso a los modelos de lenguaje de la organización, proporcionando capacidades de control, gobierno y estandarización.

De esta manera, el LLM Gateway se posiciona como un servicio transversal dentro del ecosistema tecnológico, permitiendo que múltiples agentes utilicen la misma infraestructura de acceso a modelos de IA.

La arquitectura de transición se organiza en dos dominios principales:

- Sistema de Agente Singular – Contiene el runtime del agente.

- Plataforma de Capacidades de IA y Servicios Empresariales – Conjunto de sistemas externos que proveen capacidades al agente.

Esta separación refuerza el principio de arquitectura empresarial de desacoplamiento entre el runtime de los agentes y las plataformas tecnológicas que proveen capacidades compartidas.

## Momento 2 (Deseada)

El siguiente diagrama representa la arquitectura objetivo (To-Be) de la plataforma de agentes de IA. Esta arquitectura evoluciona a partir de la arquitectura de transición previamente definida, incorporando nuevas capacidades de plataforma que permiten operar agentes de forma más gobernada, reutilizable y escalable.

En esta sección se describen únicamente los cambios introducidos respecto a la arquitectura de transición, los cuales aparecen representados en el diagrama con un tono de color más claro. Estos elementos corresponden a nuevas capacidades que amplían la plataforma de IA y fortalecen la gobernanza del uso de modelos, prompts y herramientas.

![image-20260312-143922.png](../../../recursos/5666766913/image-20260312-143922.png)

### Introducción de un Sistema de Gestión de Prompts

Uno de los cambios más relevantes es la incorporación de un **Sistema de gestión de Prompts** como componente transversal de la plataforma.

En la arquitectura de transición los prompts eran gestionados directamente dentro del runtime del agente o como artefactos embebidos en el código. En la arquitectura objetivo se introduce una plataforma dedicada para gestionar el ciclo de vida de los prompts de forma centralizada.

Este sistema está compuesto por dos contenedores principales:

#### Prompt Server

El Prompt Server actúa como repositorio y servicio de acceso para los prompts utilizados por los agentes. Sus responsabilidades incluyen:

· Almacenamiento de prompts

· Versionamiento de prompts

· Gestión de estado de despliegue

· Distribución de prompts a los agentes

Los agentes solicitan al Prompt Server las plantillas de prompts que necesitan para ejecutar sus flujos de razonamiento.

#### Prompt Compiler

El Prompt Compiler es responsable de compilar o preparar los prompts antes de ser utilizados por los agentes. Este componente permite transformar definiciones declarativas de prompts en artefactos listos para ser consumidos por el runtime del agente.

Este patrón permite tratar los prompts como artefactos gestionados dentro de la plataforma, habilitando prácticas similares a **"prompts as code"**.

### Sistema CI/CD para Prompts

Para soportar el ciclo de vida de los prompts se incorpora un **Sistema CI/CD para prompts**.

Este sistema introduce prácticas de ingeniería similares a las utilizadas para el desarrollo de software, permitiendo gestionar prompts mediante pipelines automatizados.

Este subsistema incluye:

#### Prompt‑as‑Code Pipeline

Pipeline encargado de:

· Validar cambios en prompts

· Ejecutar pruebas

· Construir artefactos de prompts

· Desplegar versiones hacia el Prompt Server

Esto permite que los prompts evolucionen de forma controlada dentro del ciclo de desarrollo.

#### Eval Service + Golden Sets

Se incorpora un servicio de evaluación automática que permite validar el comportamiento de los prompts antes de su despliegue.

Este componente utiliza **conjuntos de evaluación (golden sets)** para verificar que los cambios introducidos no degradan el comportamiento esperado del agente.

Este mecanismo permite establecer controles de calidad sobre los prompts antes de que sean utilizados en producción.

### Evolución del AI Gateway

La arquitectura objetivo introduce nuevas capacidades dentro del **Sistema AI Gateway**.

En la arquitectura de transición este sistema centralizaba el acceso a modelos LLM y herramientas MCP. En la arquitectura objetivo se amplía su rol incorporando mecanismos adicionales de gobernanza.

#### Guardrails Service

Se introduce un servicio de **Guardrails** encargado de aplicar controles sobre las interacciones con modelos de lenguaje.

Entre sus responsabilidades se encuentran:

· Validación de entradas

· Validación de salidas

· Prevención de ataques de prompt injection

· Aplicación de esquemas de entrada y salida

Este servicio permite reforzar la seguridad y confiabilidad del uso de modelos de lenguaje.

#### Policy Engine

El Policy Engine introduce una capa de políticas que gobierna el comportamiento de los agentes y el acceso a herramientas o modelos.

Este motor permite implementar reglas como:

· Restricciones de uso de herramientas

· Políticas de acceso a modelos

· Controles basados en roles

· Validaciones de cumplimiento

Esta capacidad fortalece la gobernanza del ecosistema de agentes.

### Consolidación de la Plataforma de IA

Con la incorporación de estos nuevos componentes, la arquitectura objetivo consolida una **plataforma de IA más completa**, donde múltiples capacidades transversales soportan la operación de agentes.

La plataforma pasa a incluir:

· Sistema de acceso a LLM

· Catálogo de herramientas MCP

· Sistema de gestión de prompts

· CI/CD de prompts

· Guardrails y políticas

· Observabilidad de IA

· Plataforma de conocimiento empresarial

Este conjunto de servicios constituye una **plataforma compartida de capacidades de IA** utilizada por múltiples agentes dentro de la organización.

### Impacto en el Runtime del Agente

Es importante destacar que el **Sistema de Agente Singular mantiene su estructura principal sin cambios significativos** respecto a la arquitectura de transición.

El runtime del agente continúa compuesto por:

· Interfaz de usuario

· Gateway

· Broker

· Orquestador del agente

· Persistencia

· MCP privado

La principal diferencia es que el agente ahora consume capacidades adicionales de la plataforma, particularmente relacionadas con la gestión de prompts y los mecanismos de gobernanza del uso de LLM.

### Conclusión

La arquitectura objetivo introduce nuevas capacidades de plataforma que permiten gestionar de manera más madura el ciclo de vida de prompts, el gobierno del uso de modelos de lenguaje y la seguridad del ecosistema de agentes.

Estos cambios consolidan una **plataforma de IA empresarial**, donde los agentes funcionan como runtimes cognitivos que consumen servicios especializados provistos por la plataforma tecnológica de la organización.

# 4. Lineamientos y artefactos de Gobierno.

## Matriz de Riesgo

Para esta primera versión de la arquitectura de referencia se libera el artefacto de “Matriz de Riesgos V1”

### ¿Qué es y para qué sirve la Matriz de Riesgos?

La **Matriz de Riesgos de IA** es una herramienta diseñada para **evaluar, clasificar, mitigar y monitorear los riesgos asociados a iniciativas de Inteligencia Artificial**, en alineación con:

· **EU AI Act**

· **Política corporativa de AI Risk Management**

· Requisitos legales, éticos, técnicos y operativos

Su objetivo principal es **permitir la toma de decisiones informadas** sobre si una iniciativa de IA puede:

· continuar,

· requerir controles adicionales,

· o no debe ejecutarse (en caso de sistemas prohibidos).

### Capacidades principales de la Matriz

#### 1. Clasificar una iniciativa de IA según su nivel de riesgo

La matriz permite **clasificar cualquier iniciativa de IA** (PoC, presales, iniciativas internas o de clientes) en una de las siguientes categorías:

· **Sistema Prohibido**

· **Sistema de Alto Riesgo**

· **Sistema de Riesgo Limitado**

· **Sistema de Riesgo Mínimo**

Esta clasificación se realiza mediante un **cuestionario estructurado** alineado con el **EU AI Act**, evaluando aspectos como:

· manipulación subliminal,

· explotación de vulnerabilidades,

· biometría,

· scoring social,

· decisiones automatizadas sobre personas,

· uso en sectores regulados (salud, seguros, empleo, justicia, etc.).

#### 2. Determinar si una iniciativa puede o no continuar

En función del resultado de la clasificación:

· **Sistema Prohibido** → la iniciativa **no debe continuar**.

· **Sistema de Alto Riesgo** → debe completarse la matriz completa de riesgos y cumplir requisitos adicionales.

· **Riesgo Limitado o Mínimo** → se puede continuar, conservando el registro como evidencia de cumplimiento.

Esto convierte la matriz en un **gate formal de gobierno de IA**.

#### 3. Identificar y estructurar riesgos por dimensiones estandarizadas

Para sistemas de **Alto Riesgo**, la matriz permite **identificar riesgos específicos** organizados en dimensiones predefinidas, entre ellas:

· Derechos y libertades humanas

· Daño a la vida y la propiedad

· Injusticia y discriminación

· Desinformación

· Privacidad y protección de datos

· Propiedad intelectual

· Seguridad informática

· Uso indebido o malintencionado

· Impacto ambiental

· Intereses económicos y reputacionales

· Cumplimiento normativo

Estas dimensiones **no son modificables**, ya que provienen de la política corporativa y regulación vigente.

#### 4. Evaluar impacto y probabilidad del riesgo

Para cada riesgo identificado, la matriz permite:

· Evaluar el **impacto** (desde “Sin riesgo” hasta “Máximo”).

· Evaluar la **probabilidad** de ocurrencia.

· Calcular un **riesgo inicial** mediante scoring.

Esto genera una **priorización objetiva de riesgos**, facilitando la toma de decisiones.

#### 5. Definir y documentar medidas de mitigación

La herramienta permite:

· Asociar **medidas técnicas y organizativas** a cada riesgo.

· Evaluar la **eficacia de las medidas** para reducir impacto y probabilidad.

· Documentar **cómo se implementan** las medidas (no solo que existen).

Incluye además un **Catálogo de Medidas de Seguridad** reutilizable, que cubre:

· human‑in‑the‑loop,

· control de sesgos,

· trazabilidad,

· seguridad,

· privacidad,

· gobernanza,

· resiliencia y continuidad operativa.

#### 6. Calcular y aceptar el riesgo residual

Una vez aplicadas las mitigaciones, la matriz permite:

· Calcular el **riesgo residual**.

· Compararlo con el riesgo inicial.

· Verificar si el riesgo residual es **aceptable** según el apetito de riesgo corporativo.

Esto habilita una **decisión formal de continuar, ajustar o detener** la iniciativa de IA.

#### 7. Habilitar monitoreo y revisión periódica

La matriz establece que:

· El riesgo **no es estático**.

· Debe revisarse al menos **una vez al año** o ante cambios relevantes (modelo, datos, contexto legal).

· Sirve como base para **seguimiento continuo**, auditoría interna y control.

#### 8. Soportar cumplimiento regulatorio y auditorías

La matriz permite:

· Trazar cada riesgo y mitigación a artículos específicos del **EU AI Act**.

· Demostrar cumplimiento frente a auditorías internas.

· Documentar roles (proveedor, usuario, implementador, distribuidor, etc.).

· Proveer evidencia de gobernanza responsable de IA.

No está diseñada para ser compartida externamente (clientes o reguladores), pero sí como **artefacto interno de compliance**.

# 5. Prácticas de excelencia en la construcción de sistemas de agentes en SURA

## DevOps como fundamento en la construcción de agentes.

Las prácticas de devops nacen pensadas para la construcción de software que podriamos llamar “Deterministico”. Sin embargo, las nuevas capacidades que aportan los sistemas de IA requieren repensar la práctica y redefinir el alcance de la misma.

![image-20260312-144143.png](../../../recursos/5666766913/image-20260312-144143.png)

La nueva propuesta gira alrededor de un **modelo de madurez y prácticas para desarrollo y operación de agentes con IA**, organizado en **pilares**, algunos heredados del mundo tradicional y otros evolucionados para el nuevo paradigma de IA.

### Pilar Metodológico

Este pilar aborda **cómo se conciben, planifican y gestionan los desarrollos con IA desde su origen**.

· Incorpora **nuevos elementos que no existían en el modelo tradicional**, especialmente la **definición explícita del contexto de negocio**.

· El contexto se vuelve un **factor crítico de calidad**, porque condiciona:

o La forma en que se diseñan los agentes.

o Los criterios de aceptación.

o Las evaluaciones funcionales posteriores.

· Se conecta con prácticas ágiles existentes, pero ahora:

o Se apoya en capacidades de IA para **acelerar la creación de planes de pruebas**.

o Se apoya en observabilidad para evidenciar el avance real de los equipos.

La idea central es que **la calidad y la evaluación de la IA empiezan desde la concepción del caso de uso**, no al final.

### Pilar de CI/CD (Integración y Despliegue Continuo)

Este pilar se enfoca en **cómo se construyen, versionan, validan y despliegan los artefactos**, incluyendo agentes y componentes con IA.

· Sigue aplicando **CI/CD tradicional**, porque los agentes **siguen siendo código**.

· Se apoya en:

o **Infrastructure as Code (IaC)**.

o Templates corporativos de despliegue.

o Pipelines estandarizados.

· Introduce **nuevos artefactos a versionar**, como:

o Prompts.

o Configuraciones de contexto.

· Refuerza los **quality gates**, combinando:

o Calidad de código.

o Evaluaciones específicas de IA (cuando aplique).

El mensaje clave es: **LLMOps no reemplaza CI/CD; lo extiende**.

### Pilar de Operación (antes Observabilidad)

Este pilar **trasciende la observabilidad clásica** y se convierte en un pilar de **operación integral**.

Incluye explícitamente:

· **Métricas operativas y de negocio**.

· **FinOps**, por el costo asociado al uso de modelos.

· **Gestión de incidentes**.

· **Alertas y monitoreo en tiempo real**.

· **Auditoría de decisiones de los agentes**.

· **Mantenibilidad y reentrenamiento**, identificados como riesgos operativos clave.

Además:

· Los agentes y modelos **cambian su comportamiento en el tiempo**, por lo que la operación debe detectar:

o Variaciones.

o Degradaciones.

o Riesgos de calidad o seguridad.

Este pilar asegura que el sistema **siga siendo confiable después del despliegue**.

### Pilar de Estrategia de Pruebas (Incluye Evals)

Es uno de los pilares más discutidos y considerados **críticos**.

· Evoluciona el concepto clásico de pruebas hacia **evaluaciones (evals)**.

· Debe cubrir **dos mundos claramente diferenciados**:

o **Pruebas tradicionales (shift-left)**:

§ Pruebas unitarias.

§ Análisis estático.

§ SCA.

§ Seguridad del código.

o **Evals específicos de IA**:

§ Task success rate.

§ Tool-use success.

§ Hallucination rate.

§ Guardrails y pruebas de seguridad IA (prompt injection, fuga de datos, etc.).

Las definiciones que vendrán en versiones posteriores de esta arquitectura de referencia se trabajarán con **niveles de madurez**, empezando por evaluaciones básicas, incluso manuales o determinísticas.

Este pilar busca **medir si la IA hace bien lo que promete hacer**.

### Observabilidad como habilitador transversal

Aunque inicialmente era un pilar independiente, después de diferentes revisiones se encontró que la **observabilidad debe ser un habilitador transversal** para que:

· Apoye el pilar metodológico.

· Alimente operación.

· Permita medir evals y calidad.

· Sirva como feedback continuo para los equipos.

Incluye:

· Logging.

· Tracing.

· Métricas.

· Dashboards de calidad y comportamiento.

No es solo monitorear, sino **aprender y ajustar continuamente**.

### Gobierno (pilar transversal)

· Gobierno de:

o Identidad de agentes.

o Niveles de madurez.

o Riesgos.

o Roles y responsabilidades.

· Se evidencia la necesidad de alinear estas definiciones con otros frentes corporativos (PM, seguridad, plataforma) en versiones posteriores de esta arquitectura de referencia.

## LLMOps como práctica emergente.

LLMOps (Large Language Model Operations) constituye el marco central para la gestión integral del ciclo de vida de agentes y modelos de lenguaje en la organización. Bajo este enfoque, se establecen procesos, herramientas y controles que aseguran la trazabilidad, mantenibilidad, calidad y gobernanza de los sistemas de IA, desde su diseño hasta su operación y evolución continua.

Entre otros aspectos LLMOps articula y conecta las definiciones y prácticas en torno a la evaluación de agentes (evals) y la gestión de prompts, garantizando que ambos procesos sean sistemáticos, auditables y alineados con los objetivos de negocio, la seguridad y el cumplimiento normativo.

Toda la definición de LLMOps para la compañía se encuentra documentada en el sitio de confluence: [Framework de LLMOps](https://segurosti.atlassian.net/wiki/x/LIBOCgE)

Es importante aclarar que en la construcción de agentes LLMOps se centra en todas las prácticas necesarias para definir adecuadamente el contexto de un agente, pero, por su misma naturaleza, los sistemas o soluciones integrales de agentes deben seguir contemplando el manejo de prácticas adicionales como devops y dataops.

### **Evaluación de agentes (Evals)**

La evaluación de agentes es un proceso estructurado y recurrente, definido y gestionado bajo el marco de LLMOps, que busca asegurar que cada agente desplegado cumpla con los más altos estándares de calidad, robustez y alineamiento estratégico. Los principales lineamientos acordados son:

· **Criterios de evaluación:** Todo agente debe ser evaluado en dimensiones como agencia (capacidad de actuar autónomamente), robustez ante escenarios adversos, explicabilidad de sus decisiones y alineamiento con los objetivos de negocio y las políticas de la organización.

· **Pruebas integrales:** Se establece la obligatoriedad de realizar pruebas de caja negra (evaluación funcional y de resultados) y caja blanca (análisis interno del comportamiento y lógica del agente), así como pruebas de estrés, seguridad y resiliencia.

· **Trazabilidad y documentación:** Los resultados de las evaluaciones deben ser documentados, versionados y auditables, permitiendo el seguimiento de la evolución del agente y la justificación de decisiones tomadas.

· **Métricas y revisión periódica:** Se promueve la adopción de métricas estándar (precisión, cobertura, robustez, explicabilidad, etc.) y la revisión periódica del desempeño de los agentes, habilitando la mejora continua y la detección temprana de desviaciones o riesgos.

· **Integración con LLMOps:** Todas las evaluaciones y sus resultados se gestionan y almacenan centralizadamente, integrados en los pipelines de LLMOps, facilitando la automatización, el monitoreo y la trazabilidad de cambios.

### **Gestión de Prompts**

La gestión de prompts es reconocida como un componente crítico en la operación y evolución de agentes basados en LLMs. Bajo el marco de LLMOps, se han definido las siguientes prácticas clave:

· **Centralización y versionado:** Todos los prompts utilizados por los agentes deben ser gestionados de manera centralizada, con control de versiones, historial de cambios y trazabilidad de responsables.

· **Auditoría y reutilización:** Los prompts deben ser auditables, es decir, se debe poder rastrear su origen, propósito y modificaciones a lo largo del tiempo. Además, se fomenta la reutilización de prompts efectivos y la creación de librerías compartidas.

· **Alineamiento con políticas y compliance:** El diseño y uso de prompts debe cumplir con las políticas de seguridad, privacidad y compliance de la organización, evitando la generación de contenido no autorizado, sesgado o riesgoso.

· **Pruebas de efectividad:** Se deben implementar mecanismos automáticos y manuales para evaluar la efectividad de los prompts (evals de prompts), midiendo su impacto en el desempeño del agente y su alineamiento con los objetivos definidos.

· **Documentación de buenas prácticas:** Se deben documentar y difundir las buenas prácticas para el diseño, mantenimiento y actualización de prompts, asegurando la calidad y consistencia en su uso.

· **Integración con LLMOps:** La gestión de prompts debe estar integrada en los flujos de LLMOps, permitiendo la automatización de pruebas, despliegues y auditorías, así como la rápida adaptación ante cambios regulatorios o de negocio.

En una versión posterior de este documento se espera contar con una definición de las prácticas concretas para la gestión de prompts y la manera en que estás modifican la estructura arquitectónica de las soluciones de agentes.
