# Contexto de la propuesta v4 · Paquetes de puntos para Generic API

> Archivo vivo. Se actualiza con cada cambio que pida Didier en esta propuesta, para retomar sin el hilo de la conversación.
> Última actualización: 2026-10-09 (v4 con la sección gráfica «La dinámica de trabajo: hoy y después»).

## 1. Qué es y para quién

- **Entregable activo:** `propuestas/viva/propuestas/nuevo-modelo-de-trabajo/v4/tech-and-solve-propuesta-paquetes-de-actividades.html` (y su PDF, 21 páginas).
- **Destinatario:** Viva Aerobus (**documento para el cliente**). Autor: Didier Franco, líder de Tech and Solve en Generic API.
- **Qué propone:** cambiar de equipo fijo de tres personas pagado por persona y hora a **paquetes mensuales de puntos**; cada actividad cuesta los puntos de su tamaño y se paga cuando su PR está aprobado.
- **Equipo:** Daniel Llano, Gabriel Herrera y Luis Galindo (`viva/generic-api/CLAUDE.md`). El documento no los nombra.
- **Origen:** v4 parte de `v3` (que mezclaba los tickets API y STI del informe). `v1`, `v2` y `v3` quedan congeladas.

## 2. Reglas que no se rompen

1. **Versiones:** solo se edita `v4/`. No se toca `v1`–`v3`, `resources/` ni `viva/` (análisis de septiembre). Didier lo pidió así el 9 oct 2026 («sin cambiar nada de otros lugares»). No se crea `v5` hasta que lo indique.
2. **Reglas del folder** (`nuevo-modelo-de-trabajo/CLAUDE.md`, 9 oct 2026):
   - Respaldar los datos propuestos con los datos reales más recientes de `techandsolve/viva`.
   - **Todo dato previo debe ser citable a su evidencia.**
   - **El tallaje considera solo el tiempo realmente invertido para completar una actividad + 30 % de desviación por defecto, y solo actividades finalizadas del equipo.**
3. **Solo lectura** en Jira, GitHub, `GitHubViva/*` y el xlsx. Nada se publica fuera.
4. **Ante el cliente no se menciona IA** ni el repo `VivaAerobus.Generic.ApiLLMCoder` (`viva/generic-api/CLAUDE.md`).
5. **Sin supuestos:** toda cifra sale de un script sobre la fuente; las palabras corresponden a la evidencia («cambió la estimación» ≠ «refutó»). Lo no verificado se declara.
6. **Medición** (`viva/generic-api/CLAUDE.md`): estimación = columna G; tiempo real = H + I; desviación = (H + I) − G; cumple si J ≤ 30 %; todo en horas del informe.
7. **Diseño:** plantilla `tech-and-solve-proposal` (una sola hoja de estilos, Poppins, sin estilos en línea). Texto mínimo, tablas que hablan solas (preferencia de Didier).
8. **Datos sensibles para el cliente:** en el documento no hay nombres de personas (ni del equipo ni de revisores) ni IA. Quedan los números de PR y de tickets, que son del repositorio y del Jira del cliente.

## 3. Fuentes

| Ref | Fuente | Para qué |
|---|---|---|
| F1 | `viva/generic-api/evolucion-generic-api/evidencias/resources/09 Viva Aerobus Seguimiento Tech and Solve - Informe Septiembre2026.xlsx`, hoja «Seguimiento Mes» (copia idéntica por hash en `nuevo-modelo-de-trabajo/resources/`) | Tallaje (H, I), acierto (G, J), horas del mes, devoluciones (K), fechas (E, F). |
| F2 | `…/08 Viva Aerobus … Informe Agosto2026 (1).xlsx` | Acierto y desviación de agosto. |
| F3 | Jira `vivaaerobus.atlassian.net`, proyecto API (cloudId `bb4fb1bb-f13a-40ed-a592-0fe30249927d`), lectura del 9 oct 2026 | Estados, transiciones, historial de «Original Estimate», etiquetas, comentarios, worklogs, adjuntos. |
| F4 | GitHub `EzyWebwerkstaden/VivaAerobus.Generic.Api`, `gh` como `didierfrancogomez`, lectura del 9 oct 2026 | PRs de septiembre: reseñas, comentarios, aprobaciones, merges, Sonar. |
| F6 | `viva/generic-api/CLAUDE.md`, punto 10 (indicación de Didier del 9 oct 2026) | Jornada: 42 h semanales por persona, lunes a viernes; capacidad = 3 × 42 × 4 = **504 h al mes**. El informe registra 524 h en septiembre (22 días hábiles × 8 h): supera la capacidad en 20 h. |
| F5 | https://www.atlassian.com/agile/project-management/fibonacci-story-points (200 al 9 oct 2026) | Escala de puntos. Práctica de industria, no norma. |
| — | `viva/generic-api/acompanamiento/septiembre/v2/analisis.html` y su `CONTEXTO.md` | **Fuente interna** que guió el v4. **No se cita en el documento** (menciona IA y personas). Las cifras que se tomaron de ahí se recalcularon desde F1–F4. |

**Defectos conocidos**
- El informe trae un **autofiltro activo** (508 filas ocultas en septiembre); los scripts leen todas las filas.
- El informe de septiembre es **acumulativo**: «Registrado meses previos» (H) ya incluye agosto (H_sep = H_ago + I_ago en las 511 filas comparables).
- El estado se escribe de dos formas, «Finalizado» y «Finalizada». Es el mismo estado (`evidencias/resources/CLAUDE.md`) y se unifican.
- Algunas filas finalizadas no traen «Fecha fin» (E): quedan «No aplica» o vacías.
- Jira entrega solo los últimos 100 cambios del historial (API-1663, 1738, 1832, 1834 tienen más).

## 4. Universo y definiciones

- **Generic API** = tickets `API-*` del informe. Los `STI-*` son de otros proyectos y no entran.
- **Actividad** = un `Parent ID`. Su tiempo real suma H + I de **todas sus filas**, incluidas las de personas que participaron antes o después.
- **Actividad terminada por el equipo (universo del tallaje, 104; pedido 15):** al menos una fila en «Ready for prod» (listo para producción: el equipo terminó), «Finalizado» o «Finalizada» (Done: desplegada en producción) **y** al menos una fila de Daniel, Gabriel o Luis (nombres exactos; «Luis Galindo Test» no cuenta). Con horas > 0. Flujo de Jira del cliente: To Do → In Progress → In review (revisión del PR) → UAT → Ready for prod → Done; In review y UAT pueden devolver la actividad al equipo (a In Progress o Feedback). Se excluyen:
  - **API-1860:** figura a nombre de Gabriel pero la implementó un revisor (PR #2500, etiqueta Jira «Wieliński»).
  - **API-1621** «Acompañamiento Liderazgo Técnico Abril 2026»: acompañamiento mensual, no una entrega con PR. Regla: resúmenes que empiezan por Acompañamiento, Onboarding, Daily Meetings o Instalación.
  - Otros estados («Cerrado», «Cerrada», «UAT», «En revisión», «En curso»…).
- **Tamaño:** horas reales × 1,3 (margen de 30 %, el de la columna J). Rangos en horas con margen: ≤ 6 → 1; ≤ 11 → 2; ≤ 17 → 3; ≤ 28 → 5; ≤ 46 → 8; ≤ 74 → 13; ≤ 90 → 21; > 90 → «Dividir». Referencia de diseño: 4,5 h por punto; el tope de cada rango la supera como máximo en 33 %. Promedio del equipo: 4,28.
- **Actividad > 90 h:** se divide en partes iguales de hasta 90 h y cada parte cuenta los puntos de su tamaño (en la serie mensual).
- **Mes de cierre:** para las 20 actividades de septiembre con pase a Ready for prod, la fecha de ese pase en Jira (`transiciones_jira.json`, marca †); para las demás, «Fecha fin» (E) del informe o, si falta, «Fecha entrega» (F) (8 actividades, marcadas con *); 2 sin ninguna fecha (API-1686, API-1706) no entran en los meses. Mezcla de dos fuentes de fecha: las anteriores a septiembre no se contrastaron con Jira.
- **Paquetes (regla vigente, pedidos 14 y 15):** personas enteras × puntos por persona al mes (parte entera del promedio con las tres activas jul–sep 2026 = 38 de 38,8). Inicial 3 personas = 114 puntos (equipo actual; solo 1 de los 3 meses lo alcanzó: septiembre 184; jul 97, ago 68), Estándar 4 = 152, Ampliado 5 = 190 (sin histórico). Con la mediana de esos tres meses (97 → 32 por persona) serían 96 / 128 / 160. Decisión abierta.
- **Pago:** valor del punto × puntos de las actividades con PR aprobado, con tope en los puntos del paquete.
- **Días hábiles:** lunes a viernes, fraccionarios, en UTC. Espera hasta la primera revisión = apertura del PR → primera reseña de un tercero que no es del equipo ni un bot.

## 5. Cifras verificadas (recalculadas el 9 oct 2026)

**Tallaje (F1, F3)** — 104 actividades (incluye 10 en Ready for prod), 3.220,5 h reales, 4.186,65 h con 30 %, 983 puntos. Tabla por tamaño: regenerar (`build_v4.py` la imprime en el anexo A del documento).






**Puntos por mes (septiembre 2025 → septiembre 2026):** 28, 74, 36, 52, 98, 68, 35, 90, 71, 47, 97, 68, 184. Septiembre (184) concentra 19 actividades; 10 pasaron a Ready for prod el 28–30 de septiembre y 1427 y 1738 pasan de agosto a septiembre con la fecha de Jira. **Paquetes vigentes 114 / 152 / 190 (3, 4 y 5 personas × 38).**

**Acierto y horas (F1, F2):** septiembre 18 de 25 cumplen (72 %), 819 / 659 h (+160 h, +24 %); agosto 4 de 18 (22 %), 772,5 / 558 h (+214,5 h, +38 %). Coincide al 100 % con «Tipo de Ticket» = «Normal». Horas registradas en septiembre: 524 (176 + 176 + 172); agosto 488. Devoluciones del informe en septiembre: 41 en 26 actividades.

**PRs abiertos en septiembre por el equipo (F4):** 20 abiertos, 19 mergeados; mediana 1,7 días hábiles a la primera revisión (13 de 20 en ≤ 2); 25 solicitudes de cambio (1,25 por PR); 4 aprobados sin ninguna; apertura → primera aprobación: mediana 3,3 (máx 7,7; 19 de 20 aprobados); apertura → merge: mediana 3,7. Sonar: 8 de 19 mergeados con el Quality Gate en rojo (13 issues nuevos); 0 menciones a Sonar en 127 reseñas y comentarios de terceros.

**Jira (F3):** 26 de 26 actividades con etiqueta TestCaseReady/TestCasesReady. Reestimadas durante el trabajo (por el desarrollador asignado): API-1663, 1738, 1764, 1832, 1834, 1867, 1908. Estimación inicial fijada por otra persona: API-1764, 1834, 1867, 1908. Subtarea API-1870 (de API-1738): TC01–TC12 con 24 capturas de Postman. Abiertas al 9 oct: API-724, 1529, 1696, 1854, 1920, 1925 (6 de 26).

**Esperas de más de 30 días hábiles (F3, F4):** API-724 227 (PR #2209 sin reseñas al 8 oct), API-1663 55,9, API-1693 53,8, API-1529 33. **Rama base:** en API-1663 y API-1693 el pedido de actualizar con master fue seguido por 4 devoluciones, 26 h de desarrolladores y 21,5 h de revisores; ejecutadas/estimadas 60/20 y 45/20 (+65 h).

**Devoluciones y desviación (F1, septiembre, 25 actividades con estimación):** 19 tienen devoluciones (columna K) y 12 de ellas cumplieron (J ≤ 30 %); las 6 sin devoluciones cumplieron. Por grupo [cumplen / no]: 0 → 6/0; 1 → 6/1; 2 → 3/2; 3 o más → 3/4. Las 7 que no cumplen suman 19 devoluciones (mediana 3) y las 18 que cumplen 21 (mediana 1). **Desviación:** las 4 actividades con espera de revisión > 30 días hábiles (API-1529 +77 h, API-1663 +40, API-724 +27, API-1693 +25) suman +169 h; las otras 21, −9 h; neto +160 h. **Matiz:** las devoluciones **sí** se asocian algo al incumplimiento (los que no cumplen tienen más), así que el documento no afirma que «no afecten»: afirma que 12 de 19 con devoluciones cumplieron, que el número no separa por sí solo y que la desviación está en las 4 esperas. **Estandarización (F4):** pedidos sobre descripción del PR en #2499, #2506, #2516 y #2508; sobre evidencia de pruebas en #2428, #2509 y #2512 (7 PRs).

**Coinciden con el análisis interno de septiembre** (ver `viva/…/septiembre/v2/CONTEXTO.md`): 4/18 y 18/25, +214,5 y +160 h, 55,9 / 53,8 / 33 / 227, 4 devoluciones y 26 / 21,5 h, 1,7 de mediana y 20 PRs / 19 mergeados. **Difieren en base:** el análisis cuenta Sonar en rojo sobre los PRs mergeados de las 26 tareas (9 de 20, 20 issues); el v4 cuenta los PRs abiertos en septiembre (8 de 19, 13 issues).

## 6. Estructura actual

**Estándar de lectura:** cada afirmación del cuerpo es un dato corto con «ver más →» (panel lateral con el detalle y la evidencia); las figuras SVG y las tablas de compra se mantienen visibles. Paneles: `d-hoy`, `d-acierto`, `d-esperas`, `d-master`, `d-pr`, `d-act`, `d-preg`, `d-estd`, `d-tam`, `d-94`, `d-meses`, `d-pruebas`, `d-abiertas`, `d-terminos` (función `more()` en `build_v4.py`). La sección «Fuentes» (F1–F6) queda visible porque los chips F# enlazan a ella.

Lo que sigue describe el contenido por secciones; el detalle de cada tabla vive en su panel.

Portada · Contenido · **1 Resumen** (cuadro de compra y tabla Hoy / Propuesta con evidencia) · **2 La dinámica de trabajo: hoy y después** (4 figuras SVG: recorrido de una actividad con lo que mira Viva y la espera no medida; devoluciones frente a cumplimiento; dónde está la desviación; lo que mira Viva hoy → después) · **3 Cómo funciona** (tamaños, paquetes, cómo se paga, recorrido) · **4 Mejoras de proceso y su respaldo en datos** (7 filas: propuesta, dato, evidencia; incluye plantilla de PR y evidencia comunes) · **5 Compromisos de cada parte** · **6 Preguntas frecuentes** · **7 Siguiente paso** · **Anexo A** cálculo de tamaños y meses · **Anexo B** las 94 actividades (con enlace a Jira) · **Anexo C** 26 actividades de septiembre con devoluciones y desviación, 20 PRs, esperas, impacto de la rama base, preguntas de negocio y pedidos de estandarización · **Anexo D** fuentes F1–F5 y términos. Las figuras las genera `build_v4.py` (funciones `svg_*`) con la paleta de la plantilla.

Las citas usan chips `F1`–`F5` que enlazan a las filas del anexo D; los tickets y PRs van con enlace (`vivaaerobus.atlassian.net/browse/API-N`, `github.com/EzyWebwerkstaden/VivaAerobus.Generic.Api/pull/N`).

## 7. Datos y scripts (en el repo, `v4/calculos/`)

| Archivo | Qué hace |
|---|---|
| `build_v4.py` | Lee el xlsx de septiembre y agosto (solo lectura) y `evidencia.json`; calcula todo y escribe el HTML del v4. Necesita `openpyxl` y la plantilla del skill `tech-and-solve-proposal`. |
| `evidencia.json` | Datos de Jira y GitHub leídos el 9 oct 2026: tabla de 20 PRs, esperas, rama base, reestimaciones, etiquetas, abiertas, preguntas de negocio, API-1860, subtarea API-1870. |
| `extraer_prs_github.py` | Recalcula con `gh` (solo lectura) la tabla de PRs y su resumen. Reproduce `evidencia.json` exactamente (verificado el 9 oct). |

**Regenerar**
1. `python3 -m venv /tmp/v && /tmp/v/bin/pip install openpyxl`
2. `/tmp/v/bin/python v4/calculos/build_v4.py` (genera el HTML).
3. Con los scripts del skill: `embed_logo.py`, `check_proposal.py`, `export_pdf.py --preview` sobre el HTML.
4. Evidencia de GitHub: `python3 v4/calculos/extraer_prs_github.py salida.json`.
5. Evidencia de Jira (MCP atlassian, solo lectura): JQL `key in (…26 tickets…)` con `fields=[labels,status,timeoriginalestimate]`; `getJiraIssue` con `expand=changelog` en API-724, 1529, 1663, 1693, 1738, 1764, 1832, 1834, 1867, 1908 (guarda a archivo; leer con Python); `fields=[comment,worklog]` en API-1663 y API-1693; `fields=[attachment]` en API-1870.

**Verificación independiente hecha el 9 oct:** el universo, las 94 filas del anexo B, los 13 meses y los paquetes se recalcularon leyendo el xlsx por XML (sin openpyxl): 0 diferencias.

## 8. Historial de pedidos sobre v4

1. «Vamos a trabajar sobre el v4 sin cambiar nada de otros lugares: sustentemos la propuesta con datos reales actualizados; el análisis ya está en `septiembre/v2/analisis.html` y la base en `evolucion-generic-api/evidencias/resources/09…`.» El v4 arrancó como copia del v3.
2. «Recuerda que el tallaje es solo contra los tiempos reales dedicados en las tareas completadas.»
3. «Ten en cuenta `nuevo-modelo-de-trabajo/CLAUDE.md`»: respaldar con datos reales de `viva`, todo dato previo citable, tallaje = tiempo real + 30 % de desviación por defecto, solo actividades finalizadas del equipo.
6. «Me cuesta entender el archivo, es muy verboso y muestra detalle donde no se requiere: sigue el estándar del informe de septiembre, dato corto y «ver más →» para el detalle.» → el cuerpo queda con dato corto + enlace «ver más →» que abre un panel lateral (patrón `input.dr-toggle` + `label.dr-back` + `div.drawer` del informe de septiembre, CSS agregado a la hoja de estilos); el detalle (tablas de 94 actividades, 26 actividades, 20 PRs, esperas, rama base, preguntas, estandarización, cálculo de tamaños, meses y paquetes, términos) vive en 14 paneles. Al imprimir, los paneles salen como «Anexos» al final, así el PDF conserva la evidencia. Se quitaron los pies largos, el ejemplo de mezcla y los textos de método del cuerpo (están en los paneles). Se quitó «Cerrar ✕» por el glifo; «→» queda (Poppins no lo tiene; el verificador lo avisa, igual que en el informe de septiembre).
7. «Reorientar la presentación»: (1) mostrar el modelo de trabajo actual; (2) énfasis en lo que se mide hoy: horas estimadas, horas ejecutadas y devoluciones; (3) en forma de notas lo que no está bien, con «ver más →»: sin estándar de revisión (formato de evidencia que cambió sin aviso), devoluciones por reglas mecánicas que Sonar podría cubrir y alcance de pruebas distinto por PR (debería ser estándar: todo automatizado). Además, la medición debe ser el **cumplimiento en la entrega**, con el detalle de las historias entregadas y sus devoluciones. → sección 2 «El modelo de trabajo actual y lo que se mide» (flujo, tarjetas 659 h / 819 h / 41, gráficos, 3 notas, hoy→después) y paneles `d-entrega` (18 de 25 dentro de lo estimado; 12 con devoluciones), `d-n1`, `d-n2`, `d-n3`. Evidencia nueva en `evidencia.json` (`notas_de_proceso`). **Límite declarado:** «el formato venía funcionando» solo se documenta como: antes del 21 sep solo 3 menciones de revisores a pruebas/evidencia y ninguna al formato; API-1738, 1867 y 1834 pasaron a UAT el 7, 14 y 18 sep; no consta aviso en los PRs (Jira y otros canales no se revisaron). Que Sonar cubra esos pedidos es criterio de Tech and Solve, no un dato; no se citan reglas de Sonar porque no se verificaron en fuente oficial.
5. «El equipo solo puede trabajar 42 horas semanales, 42 × 4 al mes por persona.» → la tabla de paquetes muestra las horas reales que implica cada uno (puntos × 3,3 h reales por punto) y su % de la capacidad de 504 h: 148 h (29 %), 214 h (43 %) y 297 h (59 %). Se agregó la fuente F6.
4. «Quiero ser más gráfico: cómo es la dinámica hoy, dónde están los puntos de dolor, qué mira Viva hoy y cómo cambia el enfoque luego del cambio. El cliente mira horas ejecutadas, devoluciones y fecha de entrega, pero los datos de septiembre muestran que lo que afecta la entrega es la revisión del PR; el enfoque debe ser mejorar el pipeline y la estandarización.» → sección 2 con las 4 figuras, fila de estandarización en la sección 4 y anexo C ampliado. Además pidió crear el CONTEXTO de esta propuesta como el del análisis de septiembre (este archivo; se actualiza con cada pedido).

8. «Mira lo que el cliente mide realmente en el xlsx de septiembre; lo que más nos molesta son los tiempos que se desvían y las devoluciones.» → `Seguimiento Mes` mide por actividad: estimación G, horas H e I, desviación J (30 %), devoluciones K, Tipo de Ticket L (Normal/Desviado/Sin estimación) y observaciones del desvío M. Septiembre, equipo (26 act.): 18 Normal, **7 Desviado** (+196 h sobre lo estimado, 19 devoluciones; observación M diligenciada en 3 de 7: API-1529, 1663, 1693), 1 Sin estimación (API-1764). «Normal» = cumple, verificado con assert en las 25 con estimación. Sección 2: tarjetas ahora «horas estimadas → ejecutadas 659 → 819 h», «7 de 25 desviadas», «41 devoluciones»; panel `d-mide`; la figura «hoy» del enfoque muestra «Tiempos que se desvían». Las otras hojas (Gestión de Riesgos, Histórico*, Bugs, Reporte, BD) se revisaron pero no se citan en el documento: pendiente decidir si alguna entra.

9. «Quita el resumen y la tabla de contenido inicial.» → se quitaron el índice, la sección 1 Resumen (cuadro y tabla hoy/propuesta) y el panel `d-hoy`; el documento arranca tras la portada con «1. El modelo de trabajo actual…»; secciones renumeradas 1–6 (Cómo funciona = 2, Mejoras = 3, Compromisos = 4, Preguntas = 5, Siguiente paso = 6).

10. «Pasar «Lo que cambia en lo que mira Viva Aerobus» a la sección 2, propuesta.» → la figura hoy→después (`svg_enfoque`) abre ahora la sección 2 «Cómo funciona».

11. «Cambia el título de la sección 2 a Propuesta.» → «2. Cómo funciona» pasa a «2. Propuesta».

12. «En la propuesta, primero el gráfico de la dinámica de trabajo, lo que se debe observar y lo que se paga.» → nueva figura `svg_propuesta` al inicio de la sección 2 (diseño conjunto → tamaño en puntos → desarrollo con pruebas unitarias y Sonar → PR → revisión máx. 2 días hábiles → PR aprobado y se paga; recuadro «Qué se paga»). Es la propuesta, no dato previo.

13. «Pensar cuántos puntos al mes hace cada persona para medir los paquetes» y «para soportar x puntos se requieren x personas». → puntos por persona = puntos de cada actividad repartidos por las horas H+I de cada integrante (verificado: suman la serie mensual). Con las tres activas (jul–sep 2026): 28,7 puntos por persona al mes (13 a 50). Personas necesarias = paquete ÷ 28,7: 45 → 1,6 (2), 65 → 2,3 (3), 90 → 3,1 (4). Tabla de paquetes con columna «Personas necesarias», texto bajo la tabla y panel `d-persona` (por mes, sin nombres). Solo 3 meses con las tres personas: base corta; ritmo observado, no compromiso. Decisión abierta: si el Ampliado (90) se mantiene con 3 personas o requiere 4.

14. «No puede haber puntos ni personas parciales, siempre enteras; el primer paquete debe ser lo que ya operamos.» (elegido: 3, 4 y 5 personas) → 28 puntos por persona (entero) → paquetes 84 / 112 / 140; tabla con columna «Equipo» y histórico solo para el Inicial; se eliminó «personas necesarias» con decimales; ejemplo de mezcla ahora con el Inicial (84 puntos). Pendiente: el valor 28 sale de solo 3 meses; 112 y 140 no tienen histórico.

15. «El proceso del cliente: To Do análisis → To Do → In Progress → In review → UAT → Ready for prod → Done. Hay devoluciones en In review y en UAT; Ready for prod es listo para producción y finalizado, Done es cuando se despliega en producción. Hay que ajustar todo el documento.» → (a) `DONE` incluye «Ready for prod»: universo 94 → 104 actividades; (b) historial de estados de las 26 actividades de septiembre leído de Jira (`calculos/transiciones_jira.json`, 9 oct 2026); la fecha de término del equipo es el pase a Ready for prod; (c) figura «Cómo se trabaja hoy» con los estados, devoluciones desde In review (44) y desde UAT (2, en 2 actividades) y la espera; (d) panel `d-etapas` (devoluciones por etapa, UAT → Ready, Ready → Done: pases a Done el 8 y 21 de septiembre y el 1 de octubre, entre 0,5 y 3,8 días hábiles tras Ready for prod); (e) serie mensual y paquetes recalculados (114 / 152 / 190). Pendientes: ¿el pago se dispara con el PR aprobado (salida de In review) o con Ready for prod?; ¿los 38 puntos por persona o la mediana (32)?; el informe cuenta 41 devoluciones, Jira 46 (44 + 2): se explican como conteos distintos en el panel.

**Qué cambió respecto de v3**
- **Alcance:** de todos los tickets del informe (API + STI, 252 actividades, 7 personas) a **Generic API**, 94 actividades del equipo de tres personas. Vuelve «equipo fijo de tres personas» (con evidencia: 524 h) y «Generic API».
- **Margen:** +30 % de desviación por defecto en lugar del +20 % para pruebas y correcciones (regla del CLAUDE.md del folder). El 20 % ya no aparece.
- **Estado:** «Finalizada» = «Finalizado».
- **Paquetes:** de 70 / 115 / 180 a **84 / 112 / 140** (3, 4 y 5 personas × 28 puntos por persona), por regla en lugar de elegirlos a mano.
- **Revisión:** «dos días» pasa a «dos días hábiles», porque todas las esperas se miden en días hábiles.
- **Sonar y pruebas:** el pendiente «confirmar si hay instancia de Sonar» se resolvió con evidencia (el bot publica el resultado en cada PR); queda como pedido de acceso de lectura. Se agregó «Autorizar pruebas unitarias» a los compromisos de Viva Aerobus.
- **Nuevo:** sección 3 con 6 filas de respaldo y anexos C (PRs y esperas) y D (fuentes); fechas de cierre y enlaces a Jira en el anexo B; pregunta «¿qué pasa con las actividades en curso?» con dato.
- **Se quitó:** la fila de reuniones diarias (eran del proyecto STI).
- **Sección 2 (pedido 4):** el documento pasa de 18 a 21 páginas; las secciones 3–7 se renumeran y las referencias internas («sección 4» → 5, «sección 3» → 4) se actualizaron.

## 9. Pendientes y decisiones abiertas

- **Pendientes en el documento (`[PENDIENTE]`):** valor del punto; qué pasa con los puntos del paquete que Viva Aerobus no usa por no tener tareas definidas; días de aviso para cambiar de paquete; si las actividades en curso se cierran con el modelo actual o entran al primer paquete.
- **Decisiones de Didier:**
  1. **Margen:** ¿es solo +30 % (como quedó) o +30 % encima del 20 % de v3?
  2. **Universo:** quedó «actividades con al menos una fila de Daniel, Gabriel o Luis». Con **todos los tickets API** (incluidas las de Eric De la Nuez y Sebastián Miranda): 151 actividades, meses 47 / 91 / 121, paquetes 60 / 90 / 110.
  3. **Estados:** con «Cerrado» y «Cerrada» como finalizados: 101 actividades, meses 28 / 74 / 144, paquetes 45 / 70 / 95.
  4. **Datos delicados para el cliente:** la sección 3 y el anexo C muestran esperas largas (API-724 sin reseña desde noviembre de 2025), devoluciones y preguntas de revisores. Son objetivas y citadas, pero conviene revisarlas antes de enviar.
  5. **Frase del pedido 4:** «prácticamente todas las actividades tienen devoluciones y cumplieron» no se sostiene del todo (19 de 25 tienen devoluciones; 12 de esas cumplieron; 4 de 7 con 3 o más no cumplieron). El documento usa la versión verificada.
  6. **Investigaciones:** 6 actividades del universo son investigaciones o análisis (API-1515, 1516, 1523, 1555, 1606, 1686) y cierran sin PR; hay que definir cómo cuentan en un modelo de «PR aprobado».
- **Límites declarados en el documento:** las horas históricas no incluyen pruebas unitarias nuevas ni correcciones de Sonar; la verificación de quién implementó cada actividad se hizo solo para las 26 de septiembre; entre septiembre de 2025 y marzo de 2026 solo una de las tres personas tuvo actividades cerradas por mes.
- **Posible extensión:** incluir los PRs de octubre (en curso al 9 oct: #2519, #2520, #2522) cuando el mes cierre.
