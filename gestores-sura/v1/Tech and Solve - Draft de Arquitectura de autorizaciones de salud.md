SURA COLOMBIA · TRANSFORMACIÓN PRESTACIÓN Y RECLAMACIONES · MVP AUTORIZACIONES DE SALUD

# Draft de Arquitectura de autorizaciones de salud

Vista de cara a los tres actores principales, asegurado, corredor y prestador, separada de la arquitectura interna de gestores.
Sirve como referencia compartida entre negocio y arquitectura durante las sesiones de definición.

| Asegurado | Corredor | Prestador |
| --- | --- | --- |
| Origina la solicitud, recibe el servicio autorizado y evalúa la experiencia al final del proceso. | Acompaña al asegurado en la radicación y el seguimiento de su caso ante la compañía. | Ejecuta el servicio autorizado y factura contra las condiciones pactadas en el convenio. |

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Objetivos de negocio del MVP

Los cinco objetivos operativos del alcance del MVP, y las dos cifras financieras que sostienen la decisión de invertir. Los cruces de las tres matrices siguientes referencian BG1 a BG5; BG6 y BG7 son resultados agregados, no algo que un solo gestor mueva por sí solo.

- **BG1.** Disminuir la necesidad de preradicados manuales.
- **BG2.** Aumentar el porcentaje de autorizaciones automáticas.
- **BG3.** Mejorar la experiencia de asegurado, corredor y prestador.
- **BG4.** Reducir de forma significativa los contactos entrantes a la línea de atención.
- **BG5.** Garantizar visibilidad en tiempo real del estado de cada solicitud.
- **BG6.** La inversión del MVP se recupera en 1.4 años.
- **BG7.** El retorno proyectado es de 4 veces la inversión en 5 años.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Mapa de calor: gestor frente a momento del asegurado

Filas: los seis gestores de la arquitectura. Columnas: los seis momentos que vive el asegurado. Cada cruce indica qué tan relevante es ese gestor para ese momento puntual, y cómo debería afectarlo positivamente.

Leyenda: **Relación crítica, define el momento** · **Relación relevante, influye en el momento** · **No aplica directamente**

| | 1. Solicitud | 2. Evaluación y coordinación | 3. Decisión comunicada | 4. Prestación | 5. Monitoreo | 6. Finalización |
| --- | --- | --- | --- | --- | --- | --- |
| **Lo que vive el asegurado** | "Sube la orden médica y espera que baste con eso" | "Silencio total. Ansiedad si el caso es urgente" | "Recibe la respuesta. Si es negación, casi nunca sabe por qué" | "Espera que el servicio coincida con lo autorizado" | "Tiene que llamar él mismo, porque nadie le avisa" | "Decide si vuelve a confiar en SURA la próxima vez" |
| **Gestor de Solicitud**<br>Recibe solicitudes desde todos los canales<br>Identifica asegurado y solicitante<br>Valida derechos: póliza, cobertura, afiliación<br>Recopila y normaliza documentos | **CRÍTICO** Especificación 1 BG1<br>Simplificar el cargue a un solo paso guiado y validar de inmediato que estén los documentos correctos, sin depender de la transcripción manual posterior. | NO APLICA | NO APLICA | NO APLICA | **RELEVANTE** BG5<br>La calidad del dato capturado aquí es la que hace confiable, o no, el estado que se muestre después. | NO APLICA |
| **Gestor de Evaluación**<br>Evalúa causalidad y pertinencia médica<br>Interpreta documentos clínicos y técnicos<br>Homologa CUPS y diagnósticos CIE10<br>Evalúa carencias, exclusiones y topes de póliza | NO APLICA | **CRÍTICO** Especificación 2 BG2<br>Resolver automáticamente el mayor número de casos posible, para que el silencio que percibe el cliente dure lo menos posible. | **CRÍTICO** Especificación 3 BG3<br>Producir, junto con la decisión, el motivo en lenguaje claro que hoy no se genera. | **RELEVANTE** BG3<br>La pertinencia médica evaluada aquí es la que determina si el servicio recibido coincidirá con lo esperado. | NO APLICA | **RELEVANTE** BG3<br>Evaluar pertinencia desde el inicio evita que las inconsistencias se descubran tarde, en cuentas médicas. |
| **Gestor de Coordinación**<br>Aplica reglas de distribución y criticidad<br>Asigna el caso al perfil idóneo, interno o externo<br>Gestiona flujos de aprobación o rechazo | NO APLICA | **CRÍTICO** Especificación 10 BG3<br>Asignar el caso al evaluador o prestador más idóneo según criticidad, sin sumar tiempo de espera innecesario. | NO APLICA | **RELEVANTE** BG3<br>Elegir bien el prestador aquí reduce el riesgo de una prestación que no coincide con lo que el cliente espera. | NO APLICA | NO APLICA |
| **Gestor de Prestación**<br>Garantiza la reserva del prestador<br>Alinea la prestación con convenios autorizados<br>Registra la ejecución del servicio | NO APLICA | NO APLICA | NO APLICA | **CRÍTICO** Especificación 7 BG4<br>Confirmar de forma proactiva fecha, lugar y alcance exacto del servicio autorizado, antes de que el cliente pregunte. | **RELEVANTE** BG5<br>Reportar en tiempo real el estado de la reserva, para que el gestor de monitoreo tenga algo real que mostrar. | **RELEVANTE** BG3<br>Registrar con precisión lo efectivamente prestado, para que el cierre no genere sorpresas al cliente. |
| **Gestor de Monitoreo**<br>Trazabilidad end to end de cada solicitud<br>Visibilidad diferenciada por actor<br>Activa escalamientos por alertas de tiempo o criticidad<br>Entrega información en el lenguaje de cada actor<br>Consume el datalake de forma bidireccional como base para los agentes | **RELEVANTE** BG5<br>Confirmar de inmediato que la solicitud fue recibida, aunque la evaluación aún no haya comenzado. | **CRÍTICO** Especificación 3 BG4<br>Notificar proactivamente que el caso está en evaluación y dar un tiempo estimado, en lugar de dejar el silencio total. | **CRÍTICO** Especificación 3 BG4<br>Entregar la decisión y su motivo por el canal de preferencia del cliente, sin que tenga que llamar a preguntar. | **RELEVANTE** BG4<br>Confirmar que el servicio programado sigue vigente y recordar la cita al cliente. | **CRÍTICO** Especificación 3 BG4<br>Eliminar la necesidad de llamar, cruzando la línea de visibilidad con notificaciones automáticas por cada cambio de estado. | **RELEVANTE** BG4<br>Avisar cuándo el caso quedó formalmente cerrado, sin que el cliente tenga que indagar por su cuenta. |
| **Gestor de Finalización**<br>Concilia prestación y obligación de pago<br>Determina el cierre formal y financiero<br>Gestiona la valoración de la experiencia | NO APLICA | NO APLICA | **RELEVANTE** Especificación 4 BG3<br>Si hay negación con integralidad EPS SURA, activar ese flujo de forma transparente, sin que se perciba como un trámite aparte. | NO APLICA | NO APLICA | **CRÍTICO** Especificación 8 BG3<br>Cerrar el caso con evidencia clara y activar la encuesta de experiencia en el momento justo, mientras el recuerdo del servicio está fresco. |

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Mapa de calor: gestor frente a momento del corredor

Mismos seis momentos y mismos seis gestores, ahora desde la experiencia del corredor que acompaña al asegurado en la radicación y el seguimiento.

Leyenda: **Relación crítica, define el momento** · **Relación relevante, influye en el momento** · **No aplica directamente**

| | 1. Solicitud | 2. Evaluación y coordinación | 3. Decisión comunicada | 4. Prestación | 5. Monitoreo | 6. Finalización |
| --- | --- | --- | --- | --- | --- | --- |
| **Lo que vive el corredor** | "Ayudo a mi cliente a radicar todo bien desde el principio, para que no se devuelva" | "No tengo manera de saber en qué va, tengo que confiar en que se está moviendo" | "Me entero de la decisión casi al mismo tiempo que mi cliente, sin poder explicarle el motivo" | "Espero que el servicio se dé como quedó autorizado, para no mediar un problema después" | "Termino llamando a la línea en nombre del cliente, tiempo que no dedico a nuevas pólizas" | "El cliente me pregunta si todo quedó bien, y yo tampoco lo sé con certeza" |
| **Gestor de Solicitud**<br>Recibe solicitudes desde todos los canales<br>Identifica asegurado y solicitante<br>Valida derechos: póliza, cobertura, afiliación<br>Recopila y normaliza documentos | **CRÍTICO** Especificación 1 BG1<br>Confirmar de inmediato al corredor si la radicación quedó completa, para que no tenga que reconfirmarla después. | NO APLICA | NO APLICA | NO APLICA | **RELEVANTE** BG4<br>La calidad del dato capturado aquí evita que el corredor tenga que llamar después a aclarar algo mal registrado. | NO APLICA |
| **Gestor de Evaluación**<br>Evalúa causalidad y pertinencia médica<br>Interpreta documentos clínicos y técnicos<br>Homologa CUPS y diagnósticos CIE10<br>Evalúa carencias, exclusiones y topes de póliza | NO APLICA | **CRÍTICO** Especificación 2 BG2<br>Resolver automáticamente el mayor número de casos evita que el corredor tenga que hacer seguimiento manual de cada solicitud de su cliente. | **CRÍTICO** Especificación 3 BG3<br>Generar el motivo de la decisión en lenguaje claro, para que el corredor pueda explicárselo a su cliente sin inventar una respuesta. | **RELEVANTE** BG3<br>La pertinencia evaluada aquí reduce el riesgo de que el corredor tenga que mediar una inconformidad con el prestador. | NO APLICA | **RELEVANTE** BG3<br>Evaluar pertinencia desde el inicio evita que el corredor reciba reclamos tardíos por glosas o ajustes. |
| **Gestor de Coordinación**<br>Aplica reglas de distribución y criticidad<br>Asigna el caso al perfil idóneo, interno o externo<br>Gestiona flujos de aprobación o rechazo | NO APLICA | **RELEVANTE** BG3<br>Asignar bien el caso reduce el tiempo que el corredor pasa dando seguimiento a casos estancados. | NO APLICA | **RELEVANTE** BG3<br>Elegir el prestador idóneo reduce la probabilidad de que el corredor tenga que intervenir por una mala asignación. | NO APLICA | NO APLICA |
| **Gestor de Prestación**<br>Garantiza la reserva del prestador<br>Alinea la prestación con convenios autorizados<br>Registra la ejecución del servicio | NO APLICA | NO APLICA | NO APLICA | **CRÍTICO** Especificación 7 BG4<br>Confirmar proactivamente la cita evita que el corredor sea el canal informal de confirmación entre el cliente y el prestador. | **RELEVANTE** BG5<br>Reportar el estado de la reserva en tiempo real le da al corredor algo concreto que responder si el cliente pregunta. | NO APLICA |
| **Gestor de Monitoreo**<br>Trazabilidad end to end de cada solicitud<br>Visibilidad diferenciada por actor<br>Activa escalamientos por alertas de tiempo o criticidad<br>Entrega información en el lenguaje de cada actor<br>Consume el datalake de forma bidireccional como base para los agentes | **RELEVANTE** BG4<br>Confirmar de inmediato la recepción reduce la primera llamada típica del corredor para verificar que todo llegó bien. | **CRÍTICO** Especificación 3 BG4<br>Notificar el avance evita que el corredor se convierta en el canal de consulta de estado de su cliente. | **CRÍTICO** Especificación 3 BG4<br>Entregar la decisión y su motivo directamente al corredor y al cliente evita que el corredor llame para poder explicarle algo. | **RELEVANTE** BG4<br>Confirmar la vigencia de la cita reduce las llamadas de verificación previas a la prestación. | **CRÍTICO** Especificación 3 BG4<br>Eliminar la necesidad de llamar en nombre del cliente libera tiempo que hoy se resta a la gestión comercial del corredor. | **RELEVANTE** BG4<br>Avisar el cierre formal le da al corredor una respuesta clara cuando el cliente le pregunte si todo quedó bien. |
| **Gestor de Finalización**<br>Concilia prestación y obligación de pago<br>Determina el cierre formal y financiero<br>Gestiona la valoración de la experiencia | NO APLICA | NO APLICA | **RELEVANTE** Especificación 4 BG3<br>Activar la integralidad EPS de forma visible evita que el corredor tenga que explicar un trámite que él mismo no entiende. | NO APLICA | NO APLICA | **CRÍTICO** Especificación 8 BG3<br>Cerrar el caso con evidencia clara le da al corredor un respaldo objetivo frente a cualquier reclamo posterior del cliente. |

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Mapa de calor: gestor frente a momento del prestador

Mismos seis momentos y mismos seis gestores, ahora desde la experiencia del prestador que ejecuta el servicio y factura contra lo autorizado.

Leyenda: **Relación crítica, define el momento** · **Relación relevante, influye en el momento** · **No aplica directamente**

Las celdas críticas sin enlace a una especificación ya quedan cubiertas por la responsabilidad general del gestor, sin necesidad de una regla adicional. El enlace a BG se mantiene en todas para mostrar a qué objetivo de negocio aporta cada una.

| | 1. Solicitud | 2. Evaluación y coordinación | 3. Decisión comunicada | 4. Prestación | 5. Monitoreo | 6. Finalización |
| --- | --- | --- | --- | --- | --- | --- |
| **Lo que vive el prestador** | "Radico o recibo la solicitud, esperando que la información que me llega esté completa" | "No sé bajo qué tarifa ni condición me van a aprobar el servicio hasta que ya es tarde" | "Me llega la autorización, pero a veces no coincide con lo que negocié en el convenio" | "Presto el servicio confiando en que va a coincidir con lo autorizado y lo pactado" | "No tengo visibilidad de mi cuenta médica hasta que me llega la glosa" | "Me notifican una glosa o ajuste sobre algo que ya presté, sin poder corregirlo a tiempo" |
| **Gestor de Solicitud**<br>Recibe solicitudes desde todos los canales<br>Identifica asegurado y solicitante<br>Valida derechos: póliza, cobertura, afiliación<br>Recopila y normaliza documentos | **CRÍTICO** Especificación 5 BG3<br>Validar en el momento el derecho y la cobertura, para no generar expectativas sobre un servicio que no aplica. | NO APLICA | NO APLICA | NO APLICA | **RELEVANTE** BG3<br>La calidad del dato capturado aquí reduce las disputas de facturación que aparecen después. | NO APLICA |
| **Gestor de Evaluación**<br>Evalúa causalidad y pertinencia médica<br>Interpreta documentos clínicos y técnicos<br>Homologa CUPS y diagnósticos CIE10<br>Evalúa carencias, exclusiones y topes de póliza | NO APLICA | **CRÍTICO** Especificación 6 BG3<br>Aplicar la tarifa y condición del convenio desde la evaluación, no después en cuentas médicas. | **CRÍTICO** Especificación 6 BG3<br>Comunicar junto con la autorización la tarifa y condición exacta aplicada, para que no haya sorpresas al facturar. | **CRÍTICO** BG3<br>La pertinencia evaluada aquí determina si lo prestado será reconocido sin ajustes posteriores. | NO APLICA | **CRÍTICO** BG3<br>Evaluar pertinencia desde el inicio evita que la glosa aparezca después de que el servicio ya fue prestado y facturado. |
| **Gestor de Coordinación**<br>Aplica reglas de distribución y criticidad<br>Asigna el caso al perfil idóneo, interno o externo<br>Gestiona flujos de aprobación o rechazo | NO APLICA | **RELEVANTE** BG3<br>Asignar bien la carga evita que el prestador reciba más casos de los que puede atender a tiempo. | NO APLICA | **RELEVANTE** BG3<br>Una asignación correcta reduce el riesgo de cuellos de botella en la agenda del prestador. | NO APLICA | NO APLICA |
| **Gestor de Prestación**<br>Garantiza la reserva del prestador<br>Alinea la prestación con convenios autorizados<br>Registra la ejecución del servicio | NO APLICA | NO APLICA | NO APLICA | **CRÍTICO** BG3<br>Alinear la reserva con las condiciones exactas del convenio antes de ejecutar, para que lo prestado sea reconocible sin ajustes. | **RELEVANTE** BG5<br>Registrar la ejecución en tiempo real es la base de cualquier conciliación posterior sin disputas. | **RELEVANTE** BG3<br>Un registro preciso de lo ejecutado reduce el margen de ajuste en la facturación. |
| **Gestor de Monitoreo**<br>Trazabilidad end to end de cada solicitud<br>Visibilidad diferenciada por actor<br>Activa escalamientos por alertas de tiempo o criticidad<br>Entrega información en el lenguaje de cada actor<br>Consume el datalake de forma bidireccional como base para los agentes | NO APLICA | **RELEVANTE** BG5<br>Visibilidad temprana del estado evita que el prestador agende sobre una autorización que aún no está confirmada. | **CRÍTICO** Especificación 6 BG4<br>Entregar la autorización y sus condiciones tarifarias al prestador de forma clara, sin que tenga que llamar a confirmar. | **RELEVANTE** BG3<br>Confirmar la vigencia de la reserva reduce reprogramaciones de última hora. | **CRÍTICO** Especificación 9 BG5<br>Dar visibilidad del estado de la cuenta médica antes de que llegue la glosa, para poder corregir a tiempo. | **RELEVANTE** BG3<br>Avisar el cierre formal le da al prestador certeza sobre cuándo un caso ya no admite ajustes. |
| **Gestor de Finalización**<br>Concilia prestación y obligación de pago<br>Determina el cierre formal y financiero<br>Gestiona la valoración de la experiencia | NO APLICA | NO APLICA | **RELEVANTE** BG3<br>Anticipar condiciones de conciliación reduce sorpresas cuando el caso llega a cierre. | NO APLICA | NO APLICA | **CRÍTICO** Especificación 8 BG3<br>Conciliar exactamente lo prestado contra lo autorizado y notificar cualquier desviación con anticipación, no como una glosa sin explicación. |

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Especificaciones de comportamiento

Las celdas marcadas con un número de referencia en las tres matrices dependen de una decisión de diseño que la responsabilidad general del gestor no fija por sí sola. Varias celdas de distintos actores comparten la misma especificación, porque describen un mismo comportamiento visto desde ángulos distintos; en esos casos se extendió el alcance de la especificación en lugar de duplicarla. La especificación 11 es la única excepción: no nace de una celda de journey, nace directamente de un riesgo del caso de negocio identificado en el driver de interoperabilidad. Cada una está en formato dado, cuando, entonces.

### Especificación 1 · Transcripción automática en la Solicitud

*Gestor de Solicitud*

**Dado que** el cliente, asesor o prestador carga uno o más documentos como parte de una solicitud de autorización,
**cuando** el documento es recibido por cualquier canal, APP, WhatsApp, Portal de Proveedores, AVA o SVP,
**entonces** el sistema extrae y estructura automáticamente la información relevante, orden médica, diagnóstico y procedimiento, sin que Konecta transcriba manualmente.

Regla de excepción: si el documento es ilegible o no corresponde al tipo esperado, el sistema le pide al cliente reintentar antes de escalar a revisión manual.

**MÉTRICA DE ÉXITO**

Reducción de los casos que hoy requieren transcripción manual, contra la línea base de 2.370 casos mensuales.

**VÍNCULO CON EL CASO DE NEGOCIO**

Sostiene el ahorro proyectado de entre 5,2 y 11,1 millones de pesos mensuales según el año.

### Especificación 2 · Calibración del motor de autorización automática

*Gestor de Evaluación*

**Dado que** una solicitud completa y validada llega al Gestor de Evaluación,
**cuando** se evalúan las reglas de póliza, la pertinencia médica y la homologación CUPS y CIE10,
**entonces** el caso se autoriza automáticamente si supera el umbral mínimo de confianza definido, y se escala a evaluación humana con el contexto ya estructurado si no lo supera.

Regla de calibración: el umbral de confianza no es único para todo el motor. El caso de negocio distingue al menos tres agentes con madurez distinta, uno replicado de EPS con efectividad base conocida, uno de pertinencia médica construido desde cero, y uno de integralidad sin referencia previa, así que cada uno se calibra y se revisa por separado, con respaldo humano más prolongado para los dos últimos mientras acumulan desempeño.

**MÉTRICA DE ÉXITO**

Tasa de autorización automática igual o superior al 70 por ciento actual, con tendencia ascendente.

**VÍNCULO CON EL CASO DE NEGOCIO**

Sostiene la reducción del volumen de 130.000 casos mensuales que hoy requieren evaluación manual. Beneficia directamente al asegurado, que espera menos, al corredor, que hace menos seguimiento manual, y al prestador, que agenda sobre una decisión más rápida.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### Especificación 3 · Notificación proactiva de estado y de decisión

*Gestor de Monitoreo, con la salida del Gestor de Evaluación*

**Dado que** el estado de una solicitud cambia, recibida, en evaluación, autorizada, negada, con prestación confirmada o cerrada,
**cuando** ese cambio ocurre en cualquiera de los gestores,
**entonces** el sistema notifica automáticamente al cliente, y al asesor cuando aplica, por su canal de preferencia, dentro de un tiempo máximo definido, sin que el cliente tenga que preguntar.

Regla especial para negación: si la decisión es una negación, el mensaje incluye el motivo en lenguaje claro para el cliente, no un código o nota interna del gestor.

**MÉTRICA DE ÉXITO**

Reducción de llamadas entrantes por consulta de estado, contra la línea base de 8.319 casos mensuales de clientes y prestadores, y 2.798 de asesores.

**VÍNCULO CON EL CASO DE NEGOCIO**

Sostiene el ahorro más grande del caso de negocio, entre 204 y 1.014 millones de pesos al año, combinando los tres actores. Libera además tiempo comercial del corredor, que hoy usa parte de su jornada llamando en nombre del cliente.

Dato pendiente de acordar con negocio y arquitectura: el tiempo máximo de notificación no está fijado en ningún lugar del caso de negocio. Sin ese número, la especificación no es verificable todavía.

### Especificación 4 · Integralidad EPS SURA transparente para el cliente

*Gestor de Finalización, con la activación del Gestor de Evaluación*

**Dado que** una solicitud es negada y el asegurado pertenece a EPS SURA,
**cuando** se activa el flujo de evaluación de integralidad bajo condiciones EPS,
**entonces** el sistema informa al cliente, por el mismo canal y de forma continua, que su caso está en evaluación de integralidad, sin que perciba que salió del proceso original ni que deba iniciar un trámite aparte.

Regla de excepción: si el flujo de integralidad no se resuelve dentro del tiempo estándar definido, se escala como alerta al Gestor de Monitoreo.

**MÉTRICA DE ÉXITO**

Ausencia de contactos adicionales del cliente pidiendo explicación sobre el estado de la integralidad.

**VÍNCULO CON EL CASO DE NEGOCIO**

Mitiga el riesgo de fragmentación de la experiencia del asegurado descrito en el numeral 3.3.

Dato pendiente de acordar con negocio y arquitectura: el tiempo estándar de resolución de la integralidad no está fijado en ningún lugar del caso de negocio.

### Especificación 5 · Validación de derechos y elegibilidad al recibir la solicitud

*Gestor de Solicitud*

**Dado que** llega una solicitud de autorización desde cualquier canal, incluido el Portal de Proveedores,
**cuando** el Gestor de Solicitud identifica al asegurado y al solicitante,
**entonces** el sistema valida de inmediato póliza activa, cobertura, morosidad y afiliación, y responde antes de aceptar la solicitud como válida.

Regla de excepción: si el derecho no está vigente, el sistema informa el motivo específico al solicitante, en lugar de dejar la solicitud en un estado ambiguo.

**MÉTRICA DE ÉXITO**

Cero solicitudes aceptadas que avancen a evaluación sin derecho vigente confirmado.

**VÍNCULO CON EL CASO DE NEGOCIO**

Evita que el prestador programe o ejecute un servicio sobre una expectativa de cobertura que no existe, descrito como fuente de fricción en el numeral 3.3.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### Especificación 6 · Condiciones tarifarias del convenio comunicadas junto con la autorización

*Gestor de Evaluación, entregado por el Gestor de Monitoreo*

**Dado que** una solicitud dirigida a un prestador específico entra en evaluación,
**cuando** el sistema aplica las reglas de póliza y determina la autorización,
**entonces** el sistema aplica también la tarifa y la condición vigente del convenio con ese prestador, y entrega esa condición junto con la autorización, no como un dato separado que aparece después en cuentas médicas.

Regla de excepción: si el convenio no tiene una tarifa vigente para el servicio solicitado, el caso se escala a coordinación humana antes de autorizar, en lugar de autorizar con una condición ambigua. Si la fuente de convenios no responde o entrega un dato desactualizado, la autorización se marca como condicional y no se comunica una tarifa al prestador hasta que el dato se confirme.

**MÉTRICA DE ÉXITO**

Reducción de glosas y ajustes por desviación tarifaria, contra la línea base actual de reprocesos en cuentas médicas.

**VÍNCULO CON EL CASO DE NEGOCIO**

Ataca directamente la causa raíz descrita en el numeral 3.3: la ausencia de integración entre autorizaciones y convenios impide asegurar desde el origen que el servicio se preste bajo condiciones tarifarias negociadas.

### Especificación 7 · Confirmación proactiva de la prestación programada

*Gestor de Prestación*

**Dado que** una prestación queda autorizada y con un prestador asignado,
**cuando** el Gestor de Prestación garantiza la reserva y la alinea con las condiciones del convenio,
**entonces** el sistema confirma proactivamente al cliente y al corredor la fecha, el lugar y el alcance exacto del servicio, sin que ninguno de los dos tenga que preguntar o mediar esa confirmación.

Regla de excepción: si la reserva no se puede confirmar dentro del tiempo estándar, se escala como alerta al Gestor de Monitoreo antes de que el cliente llegue a la cita.

**MÉTRICA DE ÉXITO**

Reducción de las llamadas del corredor y del cliente para confirmar fecha, lugar o alcance del servicio antes de la cita.

**VÍNCULO CON EL CASO DE NEGOCIO**

Cierra la brecha que dejaba abierta la responsabilidad general del gestor, descrita en el numeral 6.1, entre alinear la reserva y comunicarla a quien la espera.

Dato pendiente de acordar con negocio y arquitectura: el tiempo estándar para confirmar la reserva no está fijado en ningún lugar del caso de negocio.

### Especificación 8 · Cierre formal con evidencia y notificación diferenciada por actor

*Gestor de Finalización*

**Dado que** una prestación queda conciliada entre lo ejecutado, lo registrado y lo liquidado,
**cuando** el Gestor de Finalización determina que el caso está formal y financieramente cerrado,
**entonces** el sistema notifica el cierre a cada actor con el contenido que le corresponde: al cliente, con la confirmación y la encuesta de experiencia; al corredor, con la confirmación que respalda su gestión frente al cliente; y al prestador, con el detalle de la conciliación y el valor liquidado.

Regla de excepción: si existe una desviación entre lo prestado y lo autorizado, la notificación al prestador incluye el motivo específico del ajuste, no solo el valor final.

**MÉTRICA DE ÉXITO**

Encuestas de experiencia activadas dentro de una ventana corta después del cierre, y ausencia de reclamos por cierres percibidos como sorpresivos.

**VÍNCULO CON EL CASO DE NEGOCIO**

Cierra la brecha entre las dos responsabilidades ya documentadas del gestor en el numeral 6.1, determinar el cierre y gestionar la valoración de la experiencia, que hoy no están conectadas con una notificación activa hacia cada actor.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### Especificación 9 · Alerta temprana de desviaciones antes del cierre financiero

*Gestor de Monitoreo, con el Gestor de Finalización*

**Dado que** una prestación ya ejecutada avanza hacia la conciliación,
**cuando** el sistema detecta una desviación entre lo prestado, lo autorizado o la tarifa aplicada,
**entonces** el sistema notifica al prestador esa desviación antes del cierre formal, con tiempo suficiente para aportar evidencia o solicitar una corrección, en lugar de que la desviación se le comunique como una glosa ya decidida.

Regla de excepción: si el prestador no responde dentro del tiempo estándar de réplica, el caso avanza a cierre con la desviación documentada.

**MÉTRICA DE ÉXITO**

Reducción de glosas que llegan al prestador sin oportunidad previa de réplica, contra la línea base actual del proceso de cuentas médicas.

**VÍNCULO CON EL CASO DE NEGOCIO**

Ataca el patrón descrito en el numeral 3.3: la validación técnica y médica ocurre hoy después de la prestación del servicio, generando reprocesos, glosas y disputas por errores de facturación.

Dato pendiente de acordar con negocio y arquitectura: el tiempo estándar de réplica del prestador no está fijado en ningún lugar del caso de negocio.

### Especificación 10 · Asignación del caso al perfil idóneo según criticidad

*Gestor de Coordinación, con casos entregados por el Gestor de Evaluación*

**Dado que** el Gestor de Evaluación entrega un caso que no pudo resolverse de forma automática,
**cuando** el Gestor de Coordinación aplica las reglas de distribución, priorización y criticidad,
**entonces** el sistema asigna el caso al evaluador humano o al prestador más idóneo según nivel de complejidad, tipo de servicio y capacidad disponible, sin dejarlo en una cola genérica por orden de llegada.

Regla de excepción: si ningún perfil interno o externo tiene capacidad disponible dentro del tiempo esperado según el tipo de servicio, el caso se marca como en riesgo y se notifica al Gestor de Monitoreo para escalamiento.

**MÉTRICA DE ÉXITO**

Reducción del tiempo de espera de los casos escalados a evaluación humana, frente a una asignación por orden de llegada sin priorización por criticidad.

**VÍNCULO CON EL CASO DE NEGOCIO**

Es la única responsabilidad de las seis definidas en el numeral 6.1 que no tenía todavía una regla de comportamiento asociada, a pesar de que el caso de negocio le da autoridad explícita sobre quién recibe cada caso y en qué orden.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### Especificación 11 · Contexto del datalake disponible para el agente, o ausencia declarada

*Gestor de Monitoreo, consumido por el agente del gestor que evalúa*

**Dado que** un agente de IA necesita contexto histórico, frecuencias, patrones o dominios de información de seguros, para tomar una decisión,
**cuando** el agente invoca su herramienta de evaluación,
**entonces** esa herramienta consulta directamente el datalake que el Gestor de Monitoreo mantiene actualizado de forma bidireccional, sin depender de que Monitoreo esté disponible en el momento exacto de la consulta, y enriquece la decisión con ese contexto en lugar de que el agente razone únicamente con los datos del caso individual.

Regla de excepción: si el dominio de información requerido no está mapeado o el datalake no responde, la herramienta lo declara explícitamente en el registro de auditoría y reduce el nivel de confianza de la decisión, en lugar de decidir con un contexto incompleto sin que nadie lo note.

**MÉTRICA DE ÉXITO**

Proporción de decisiones de agentes que se toman con contexto de datalake confirmado, frente a las que se toman con ausencia declarada.

**VÍNCULO CON EL CASO DE NEGOCIO**

Mitigación explícita del Riesgo 3, alto: "priorizar el acceso al datalake como habilitador crítico del MVP. Establecer ingesta bidireccional desde el Gestor de Monitoreo."

Dato pendiente de acordar con negocio y arquitectura: el levantamiento completo de los dominios de información, previsto para el Sprint 1 según el Riesgo 3, todavía no está hecho, así que hoy no se sabe con certeza qué contexto va a estar disponible para cada agente al momento de calibrarlo.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Drivers de arquitectura

Orden de prioridad propuesto para el MVP de autorizaciones de salud, con el fragmento del caso de negocio o del análisis de riesgos que sustenta cada uno. El orden importa: cuando dos drivers entren en tensión durante una decisión de diseño, gana el que aparece primero en esta lista.

### 1 · Seguridad

Un agente de IA autoriza gasto médico y maneja historia clínica del asegurado en nombre de la compañía. Cualquier falla de seguridad expone al mismo tiempo información de salud sensible y decisiones financieras reales.

**VÍNCULO CON EL CASO DE NEGOCIO**

La Superintendencia Financiera avanza hacia un modelo de Supervisión Basada en Riesgos, descrito en el numeral 3.1, que exige mayor trazabilidad y monitoreo continuo sobre este tipo de datos y decisiones.

**DECISIONES DE ARQUITECTURA CLAVE**

Acceso mínimo por rol de gestor. Los gestores que leen historia clínica y los que autorizan pagos operan con permisos separados, para que ningún componente tenga más acceso del que su función exige.

Agentes con capacidades acotadas, no con acceso total. Cada agente de IA invoca solo las herramientas y datos que su tarea requiere, el patrón de menor privilegio propio de un sistema agéntico moderno, no el de un usuario con acceso irrestricto.

Ningún agente mueve dinero directamente. El agente de IA no tiene acceso de escritura sobre pago o póliza; solo puede invocar una herramienta (tool) que expone las reglas deterministas del Gestor de Finalización, la cual valida y ejecuta la operación. La decisión del agente nunca es la ejecución misma, es apenas el argumento con el que llama a la herramienta.

**MISMO MECANISMO EN OTROS DRIVERS**

Exponer reglas deterministas como herramientas invocables, no como acceso libre a los datos, es el mecanismo que también sostiene la auditabilidad, la modificabilidad, la usabilidad de la configuración y la interoperabilidad. En cada uno de esos drivers verás la misma idea aplicada a un problema distinto.

### 2 · Auditabilidad y trazabilidad

No es un atributo deseable, es un principio de diseño que el propio caso de negocio declara explícito: determinismo financiero en un entorno de sistemas no determinísticos. Cada valor autorizado o pagado por un agente de IA tiene que poder reconstruirse ante un auditor.

**VÍNCULO CON EL CASO DE NEGOCIO**

Numeral 6.1: "cualquier impacto económico es completamente trazable, auditable y controlado. Cada valor autorizado o pagado se deriva de reglas explícitas, topes, validaciones y evidencia operativa."

**DECISIONES DE ARQUITECTURA CLAVE**

Registro completo de cada decisión de IA. Se guarda la versión del modelo, los datos de entrada y el nivel de confianza obtenido, no solo el resultado. Como cada acción del agente pasa por una herramienta con esquema definido, ese registro es automático y estructurado, no una nota redactada aparte, así una glosa reclamada por el prestador se puede reconstruir con evidencia.

Monitoreo como bus de eventos central. Todos los gestores publican al Gestor de Monitoreo en lugar de llevar cada uno su propio registro aislado, la columna vertebral típica de un sistema multiagente observable.

Una sola fuente de verdad para explicar y para auditar. El motivo que recibe el asegurado es el mismo registro que usaría un regulador, para que "lo que le decimos al cliente" nunca sea un sistema distinto de "lo que podemos probar".

**TENSIÓN CON DISPONIBILIDAD, RESUELTA POR DISEÑO**

Centralizar el registro en Monitoreo crea una dependencia: si todos los gestores necesitaran su confirmación para poder continuar, Monitoreo se convertiría en el punto único de falla que el driver de disponibilidad busca evitar. Por eso cada gestor publica su evento de forma asíncrona hacia una cola durable, sin esperar respuesta de Monitoreo para seguir su propio flujo. Ver la decisión de degradación independiente en el driver de disponibilidad.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### 3 · Disponibilidad

Alrededor de 560.000 autorizaciones se procesan al mes, el 70 por ciento de forma automática. Una caída del sistema no es un incidente técnico aislado, paraliza en tiempo real el acceso de un paciente a un servicio de salud.

**VÍNCULO CON EL CASO DE NEGOCIO**

Volumen y automatización actual descritos en el numeral 3.3.

**DECISIONES DE ARQUITECTURA CLAVE**

Degradación independiente por gestor. Si el agente de pertinencia médica falla, el Gestor de Evaluación escala a un humano en vez de detener todo el flujo, aplicando el principio de conectar y desconectar del propio caso de negocio.

Confirmación inmediata, validación asíncrona. El Gestor de Solicitud nunca hace esperar al asegurado o al corredor la respuesta de un core legado; confirma de una vez y valida de fondo después.

Modo degradado documentado por gestor, incluido Monitoreo. Cada gestor define qué hace cuando su vecino no responde, en vez de asumir que los seis estarán siempre disponibles al mismo tiempo. Concretamente, si el Gestor de Monitoreo no responde, los demás gestores acumulan sus eventos en una cola local durable y siguen operando con normalidad; el registro de auditoría se retrasa, nunca se pierde, y ningún gestor se bloquea esperando su confirmación.

### 4 · Escalabilidad

Las primas emitidas en Colombia crecieron 9,5 por ciento anual, y la adopción de IA agéntica en seguros crece 26 por ciento anual a nivel global. El sistema se diseña para un volumen que va a seguir creciendo, no para el volumen de hoy.

**VÍNCULO CON EL CASO DE NEGOCIO**

Contexto de crecimiento de la industria descrito en el numeral 3.1.

**DECISIONES DE ARQUITECTURA CLAVE**

Gestores que escalan por separado. Evaluación y Finalización no crecen al mismo ritmo; cada gestor es un servicio independiente que se dimensiona según su propia demanda, no según un monolito compartido.

Agentes de IA en paralelo cuando el caso lo permite. Pertinencia médica y homologación CUPS pueden evaluarse al mismo tiempo, no en fila, un patrón de orquestación de agentes que reduce la espera del asegurado sin pedir más cómputo.

Más instancias sin cambiar el contrato. Sumar capacidad de un agente es una decisión de infraestructura, no un rediseño, para que un pico de demanda no se sienta como una degradación de servicio para corredor y prestador.

### 5 · Modificabilidad

Distinto de escalabilidad: no es si el sistema aguanta más volumen, es qué tan caro es cambiar una regla de póliza, una tarifa de convenio o un umbral de confianza de un agente de IA sin tocar código ni redesplegar.

**VÍNCULO CON EL CASO DE NEGOCIO**

Riesgo 9, Parametrización inicial rígida de reglas de negocio: "si las reglas de negocio se configuran de forma demasiado restrictiva en la fase inicial, la tasa de autorización automática puede no alcanzar los niveles proyectados."

**DECISIONES DE ARQUITECTURA CLAVE**

Reglas y umbrales fuera del código. Tarifas, reglas de póliza y umbrales de confianza de cada agente viven en configuración externa que alimenta directamente la herramienta que el agente invoca, para que el equipo de negocio ajuste un umbral sin esperar un despliegue ni tocar el agente mismo.

Agentes versionados de forma independiente. Cada agente de IA se recalibra o se reemplaza sin tocar a los demás, porque en un sistema agéntico moderno los modelos evolucionan a ritmos distintos entre sí.

Contratos entre gestores por evento versionado. Evaluación y Coordinación se comunican con un esquema de evento explícito, no con llamadas acopladas al código interno, para que cambiar uno no obligue a tocar el otro.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### 6 · Usabilidad de la configuración

No es la interfaz que ve el asegurado, el corredor o el prestador, es la de quien configura las reglas, tarifas y umbrales por dentro. Si esa configuración solo la puede operar un desarrollador, la modificabilidad del driver anterior queda en el papel: cada cambio seguirá dependiendo de TI, que es justo lo que se quería evitar.

**VÍNCULO CON EL CASO DE NEGOCIO**

No tiene un numeral propio en el caso de negocio; se deriva directamente de la condición para que la modificabilidad del driver 5 sea real y no solo teórica.

**DECISIONES DE ARQUITECTURA CLAVE**

Configuración en lenguaje natural asistida por un agente. Un analista describe la regla en español, un agente de IA la traduce a la configuración estructurada de la herramienta que el agente de negocio invoca, y el analista revisa una vista previa antes de publicarla, el mismo patrón de asistir sin ejecutar que ya aparece en otros drivers.

Vista previa y reversión antes que edición directa. Ningún cambio se aplica en caliente sin simularse primero contra casos históricos, y todo cambio queda versionado y reversible en un clic, para no depender de la confianza ciega en la traducción del agente.

El cambio de configuración se audita igual que una decisión de negocio. Ese registro alimenta el mismo bus de auditoría del driver 2, para que una regla mal configurada sea tan trazable como una autorización mal decidida.

### 7 · Interoperabilidad

El sistema convive con ADR, Global Web, SURA HIS, la red de prestadores y Konecta, cada uno con su propia calidad y disponibilidad de datos. La arquitectura completa depende de aislar la lógica de negocio de estos sistemas, no de integrarse rígidamente con ellos.

**VÍNCULO CON EL CASO DE NEGOCIO**

Riesgo 1, Dependencia crítica del Core SURA HIS, y Riesgo 2, Integración compleja con sistemas legados ADR y Global Web, ambos clasificados como riesgo alto en el numeral 11.

**DECISIONES DE ARQUITECTURA CLAVE**

Capa adaptadora frente a los sistemas legados. ADR, Global Web y SURA HIS quedan aislados detrás de un adaptador que se expone a los agentes de IA como una herramienta más, con el mismo contrato limpio que cualquier otra, tal como el propio caso de negocio propone para mitigar su riesgo más alto.

Contratos estándar, no formatos propietarios. Los gestores exponen eventos y APIs propias; sumar un canal o un core nuevo el día de mañana es una integración adicional, no una reescritura de la lógica de negocio.

Una sola fuente de datos compartida, sin intermediario síncrono. El Gestor de Monitoreo gobierna el datalake y lo mantiene actualizado de forma bidireccional, pero cada agente lo consulta de forma directa, sin esperar a que Monitoreo esté disponible en el momento exacto de decidir, el mismo principio de no bloquear un gestor por otro que ya aplicamos a la disponibilidad.

**RIESGO HEREDADO, NO RESUELTO POR ESTA ARQUITECTURA**

Riesgo 3, alto: los dominios de información que alimentan al datalake no están completamente mapeados todavía, lo que puede retrasar el entrenamiento y calibración de los agentes. Riesgo 8, alto: la calidad de los datos en los sistemas core es un problema transversal que el proyecto no resuelve pero que condiciona la precisión de cualquier agente.

La decisión de arquitectura no elimina estos riesgos, los hace visibles: si el datalake no tiene el dominio que un agente necesita, la especificación 11 obliga a que esa ausencia se declare, en lugar de que el agente decida con un contexto incompleto sin que nadie lo note.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

### 8 · Desempeño

Los tiempos de respuesta están definidos según el tipo de servicio, ambulatorio, hospitalario o quirúrgico. Un agente de IA que evalúa más lento que el proceso manual actual no es una mejora, así sea más preciso.

**VÍNCULO CON EL CASO DE NEGOCIO**

Tiempos de respuesta por tipo de servicio, descritos en el numeral 3.3.

**DECISIONES DE ARQUITECTURA CLAVE**

Presupuesto de tiempo distinto por agente. El agente replicado de EPS, con mayor certeza, resuelve más rápido; los de mayor incertidumbre reciben más tiempo de validación, en vez de tratar a todos igual.

Notificación por evento, no por consulta periódica. Los cambios de estado se empujan hacia el asegurado, el corredor y el prestador en el momento en que ocurren, el patrón reactivo de un sistema agéntico moderno, sin aumentar la carga del sistema.

Prioridad por criticidad clínica, no por orden de llegada. El Gestor de Coordinación ordena los casos según urgencia real, para que el desempeño se mida por el caso más crítico, no por un promedio que lo esconde.

### 9 · No exclusión de extensibilidad futura

Deliberadamente no se llama extensibilidad. El criterio de éxito no es diseñar hoy para generalizar a otros ramos, es no incrustar lógica específica de salud, CUPS, CIE10, EPS SURA, dentro de los contratos compartidos entre gestores, para que extender después sea configuración y no reescritura.

**VÍNCULO CON EL CASO DE NEGOCIO**

Numeral 6.2: el MVP de autorizaciones de salud se prioriza para levantar aprendizajes que luego se aplican al resto de capacidades, no al revés.

**DECISIONES DE ARQUITECTURA CLAVE**

Momentos como contrato genérico. Solicitud, Evaluación, Coordinación, Prestación, Monitoreo y Finalización se modelan sin lógica de salud incrustada, para que otro ramo reutilice el esqueleto sin heredar el contenido clínico.

Agentes de salud detrás de una interfaz genérica. Ningún contrato compartido entre gestores referencia directamente CUPS, CIE10 o pertinencia médica; otro ramo conecta su propio agente sin tocar la orquestación central.

Aprendizajes documentados como activo del ecosistema. Tasa de automatización, tiempos de respuesta y patrones de escalamiento quedan registrados como conocimiento reusable, no como resultado exclusivo del proyecto de salud.

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Ejemplo de arquitectura de un agente

Vista interna de cómo opera un agente dentro de un gestor, usando como ejemplo al Gestor de Evaluación. El agente razona, pero solo actúa a través de herramientas que exponen la capa determinista de negocio, el mismo mecanismo de tools que sostiene varias de las decisiones de los drivers anteriores.

**Caso de autorización**
datos clínicos, póliza, convenio

↓

**Agente de IA**
razona y decide qué herramienta invocar

↓

| `consultar_poliza()` | `evaluar_pertinencia()` | `aplicar_convenio()` |
| --- | --- | --- |
| valida cobertura y derechos | CUPS, CIE10, reglas clínicas | tarifa y condición vigente |

↓

**Capa determinista de negocio**
reglas de póliza, topes, tarifas, validaciones

**Datalake**
dominios de información y patrones históricos

↓

| Confianza igual o mayor al umbral | Confianza menor al umbral |
| --- | --- |
| autorización automática | escala al equipo de Konecta |

↓

**Registro de auditoría, Gestor de Monitoreo**
cada llamada a herramienta se registra con entrada, salida y nivel de confianza

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Propuesta de arquitectura de la solución

Vista estructural de alto nivel. Los tres actores entran por los canales existentes, los seis gestores orquestan el proceso, el Gestor de Monitoreo recibe eventos de los otros cinco sin bloquearlos, y una capa adaptadora aísla la lógica de negocio de los sistemas fuente.

| Asegurado | Corredor | Prestador |
| --- | --- | --- |
| origina y recibe el servicio | acompaña y hace seguimiento | ejecuta y factura |

↓

**Canales: APP · WhatsApp · Portal de Proveedores · AVA**

↓

| Solicitud | Evaluación | Coordinación | Prestación | Finalización |
| --- | --- | --- | --- | --- |
| recepción | decisión | asignación | ejecución | cierre |

↓

**Gestor de Monitoreo — bus de eventos asíncrono y durable**
recibe de los cinco gestores sin bloquearlos si alguno falla

**Datalake**
dominios de información

↓

**Capa adaptadora**
aísla la lógica de negocio de los sistemas fuente, conectar y desconectar

↓

| ADR | Global Web | SURA HIS | Red de prestadores |
| --- | --- | --- | --- |

**Konecta, BPO, no es un sistema a integrar**
equipo humano al que Evaluación escala casos, y cuyas llamadas Monitoreo busca reducir

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*

---

## Vista dinámica: recorrido de un caso en el tiempo

La vista estructural muestra dónde vive cada pieza. Esta vista muestra cómo se mueve un caso a través de ellas en el tiempo, y en qué momento cada paso publica su evento hacia el Gestor de Monitoreo sin esperar su confirmación para continuar.

**Gestor de Monitoreo**
recibe cada evento de forma asíncrona, sin bloquear a los gestores de origen

1. El asegurado envía la solicitud por su canal preferido
2. Gestor de Solicitud valida derechos y documentos
3. Gestor de Evaluación invoca al agente de IA y sus herramientas
   homologación, pertinencia, aplicación de convenio
4. Si la confianza supera el umbral, autoriza de inmediato
   si no, escala al equipo de Konecta con el contexto ya listo
5. Gestor de Coordinación asigna el prestador idóneo
6. Gestor de Prestación confirma la reserva
   notifica de una vez al asegurado y al corredor
7. Gestor de Finalización concilia y cierra el caso
   notifica a los tres actores con el contenido que le corresponde a cada uno

*Elaborado con base en el Caso de Negocio, Transformación prestación y Reclamaciones personas y empresas, SURA Colombia, abril de 2026. Niveles de criticidad son una lectura de trabajo para validar en sesión con el equipo de arquitectura. Documento elaborado por Tech and Solve para SURA.*
