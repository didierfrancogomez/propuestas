# Reglas de la propuesta · Paquetes de puntos para Generic API (Viva Aerobus)

> Reglas dictadas por Didier a lo largo del trabajo. Se cumplen siempre, en esta y en las próximas
> versiones. **Se actualiza en la misma respuesta cada vez que Didier da una regla nueva o cambia una.**
> El detalle de cada pedido y las cifras vigentes están en `CONTEXTO.md`.
> Última actualización: 2026-10-15 (puntos Fibonacci).

## 1. Forma de trabajo

1. **Solo se edita la versión activa (`v5/`).** No se tocan v1–v4 ni se crea una versión nueva sin que Didier lo pida.
2. **Se trabaja solo el HTML.** El PDF se regenera únicamente cuando Didier confirme que está listo.
3. **`CONTEXTO.md` y este archivo se actualizan en cada cambio**, sin que haya que pedirlo.
4. **Interpretar, no copiar.** Didier da los datos y el enfoque; nosotros los interpretamos y buscamos la mejor forma de presentarlos, con tono comercial.
5. **Ante una instrucción ambigua**, decir qué se entendió o preguntar antes de rehacer algo; no reemplazar una lámina sin avisar.
6. **Recursos en solo lectura:** Jira, GitHub, repos de `GitHubViva/`, informes xlsx y propuestas previas. El insumo del cliente (xlsx) no se modifica. Nada se publica en servicios externos.

## 2. Lo que ve el cliente

1. **Sin nombres de personas, sin IA y sin el repositorio LLMCoder.**
2. **El cliente no ve cuántas personas trabajan internamente:** los paquetes se muestran solo en puntos, sin personas, capacidad ni horas por paquete.
3. **Toda cifra mostrada como dato previo es citable** a su evidencia (F1 informe de septiembre, F3 Jira, F4 GitHub). Nunca se completa con supuestos.
4. **La lámina con los datos de septiembre es de uso interno** y lleva la alerta «USO INTERNO · Esta lámina no se debe mostrar al cliente».

## 3. Diseño de la presentación

1. **Línea gráfica de la presentación de referencia** `propuestas/SURA/gestores-sura/metodologia-trabajo/Tech and Solve - Dinámica de trabajo del equipo.html`: láminas 16:9 apiladas, medidas en cqw, fondo blanco, títulos violeta, tarjetas violeta claro, pie con logo y número, portada en violeta con el logo en caja blanca. Se conservan solo las láminas de esta propuesta.
2. **Portada:** «Propuesta de cambio de dinámica de trabajo: del modelo staff a llave en mano por actividades» y la ilustración de tres personas que pasan a una aplicación hecha. Sin contenido adicional.
3. **Lámina 2:** título «Viva deja de gestionar el equipo y solo pide desarrollos»; la dinámica del modelo staff frente a llave en mano (quién se encarga de qué). En modelo staff, Tech and Solve desarrolla y responde por la calidad; Viva Aerobus gestiona el proceso, la capacidad, define qué personas son aptas, hace los cambios de personas, la rotación, la transferencia de conocimiento, el rendimiento y los cambios de dinámica, y eso le demanda tiempo. Con el cambio, Viva Aerobus solo entrega las actividades; Tech and Solve las entrega con UAT aceptado y solo cobra las certificadas.
4. **Lámina 3:** los tres paquetes que ofrecemos.
5. **Condiciones del servicio** como última lámina para el cliente (las internas van después): tiempos de Viva Aerobus (máximo 3 días hábiles de revisión del PR hasta UAT; feedback de UAT dentro de los 5 días desde abierto el PR o se cobra; provisión de datos para certificar en máximo 2 horas desde la solicitud), pruebas unitarias automatizadas sin límite y Sonar, accesos efectivos a los ambientes, y alcance de cada actividad (criterios claros, sin dependencias abiertas, máximo 8 puntos, cambios de alcance o de rama base = actividad nueva).
6. **Términos y condiciones** al final de lo que ve el cliente (después de las condiciones del servicio): cambio de paquete, subir o bajar, con **mínimo 3 meses de aviso**; **facturación mensual del 100 % del paquete**, descontando solo los puntos de lo que Tech and Solve no cumplió en la entrega; **Viva Aerobus es responsable de usar sus puntos** (los no usados no se descuentan); escala de puntos definida (1, 2, 3, 5 u 8; máximo 8 por actividad); actividades en curso al empezar, por definir juntos.
7. Ningún texto se desborda de su caja ni de la lámina.

## 4. El modelo

1. **Flujo del cliente:** To Do análisis → To Do → In Progress → In review → UAT → Ready for prod → Done. In Progress e In review son del equipo; en In review (revisión del PR) y en UAT puede haber devoluciones. Ready for prod = listo para producción, el equipo terminó. Done = desplegado en producción.
2. **Solo se paga la tarea finalizada = Ready for prod** (no el PR aprobado a secas; Done no es el disparador).
3. **Entrega y corrección:** la tarea se entrega con el PR aprobado; el equipo corrige los defectos de las etapas posteriores (UAT), máximo 5 días desde abierto el PR. Si el cliente no da feedback, se cobra. Cambios después de esos 5 días o de alcance = control de cambios, que se cobra como tarea nueva. Solo se ajusta lo que es error de la implementación.
4. **Lo que más molesta hoy son los tiempos que se desvían y las devoluciones;** la medición debe ser el cumplimiento en la entrega.

5. **Modelo de trabajo (actores Viva Aerobus y Tech and Solve):** (1) Viva Aerobus entrega la actividad; (2) Tech and Solve valida el alcance, revisa si es implementable y entrega la estimación en puntos; (3) Viva Aerobus prioriza el orden y elige qué actividades entran en el paquete comprado; (4) Tech and Solve implementa; (5) Viva Aerobus certifica en su proceso (UAT) y aprueba o da feedback; (6) Tech and Solve valida el feedback. **Cambio de alcance:** no se acepta en la actividad; es otra actividad y Tech and Solve la cobra. **Dentro del alcance:** Tech and Solve ajusta hasta que pase las pruebas de UAT.

## 5. Datos y cálculo

1. **Solo actividades de Daniel, Luis y Gabriel, y solo sus horas** (no las de otras personas que aparezcan en la misma tarea).
2. **Base: septiembre de 2026.** Tareas del equipo en «Finalizado»/«Finalizada» o «Ready for prod» en el informe de septiembre (hoy 19). API-1860 queda fuera porque la implementó un revisor.
3. **Tallaje = tiempo realmente invertido (H + I) + 30 % de desviación**, solo con actividades terminadas del equipo. Estimación = columna G; desviación = (H + I) − G; cumple si es de hasta +30 %.
4. **Ninguna actividad pasa de 8 puntos** (internamente, 30 h de trabajo; 39 h con el 30 %). **Ante el cliente el límite se dice en puntos, no en horas.** La que pasa se divide en bloques completos de 30 h (8 puntos cada uno) y el resto toma su tamaño (p. ej. 45 h → 8 + 5 = 13; 60 h → 8 + 8 = 16).
5. **Los puntos son Fibonacci: 1, 2, 3, 5 u 8**, con topes de 6 / 11 / 17 / 28 / 39 h con el 30 %. Evitar saltos grandes entre tareas parecidas (por eso la división en bloques de 30 h y no en mitades iguales).
   **Sin decimales:** los puntos siempre son valores de la escala; si una cantidad no la cubre el valor actual, sube al siguiente de la escala (las horas que pasan de un tope toman la talla mayor).
6. **Personas y puntos siempre enteros.** Nada de personas ni puntos parciales.
7. **Paquetes = promedio por persona × personas enteras:** con 51 puntos por persona (capacidad real del equipo en el mes ÷ 3), **Inicial (base) 51 × 3 = 153 · Ampliado 51 × 4 = 204 · Avanzado 51 × 5 = 255**. Subir o bajar de paquete es solo sumar o quitar una persona. Las personas no se muestran al cliente. (Se descartó el mínimo de 130 del 15 oct.)
8. **Capacidad real del equipo = todas las horas reportadas en el mes** (columna I, también las de tareas que no terminaron en el mes), no las de meses anteriores, pasadas por la misma escala Fibonacci (sin decimales). Aplica solo para medir la capacidad; no cambia los puntos de cada tarea. Los paquetes se comparan con esa capacidad, nunca con los puntos cerrados en el mes, que arrastran trabajo de meses anteriores. Hoy: 524 h → **153 puntos al mes** con tres personas (117 de tareas terminadas + 36 de tareas sin terminar).
9. **Jornada:** 42 h semanales por persona, lunes a viernes (42 × 4 al mes).
