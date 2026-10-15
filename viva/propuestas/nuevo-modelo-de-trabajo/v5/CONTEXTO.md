# Contexto de la propuesta v5 · Presentación comercial (6 slides)

> Archivo vivo. Se actualiza con cada cambio que pida Didier. Última actualización: 2026-10-14.
> Los datos, fuentes F1–F6, definiciones y reglas de medición están en `../v4/CONTEXTO.md` (v4 queda congelada: no se edita).

## 1. Qué es
- **Entregable activo:** `v5/tech-and-solve-propuesta-paquetes-de-actividades.html` (+ PDF, 5 páginas 16:9). Presentación para Viva Aerobus, marca Tech and Solve (skill `tech-and-solve-deck`: Dark Violet, Poppins, un solo acento = Blue, chequeo de marca limpio).
- **Pedido (14 oct 2026):** v4 pasada a slides de propuesta comercial ganadora, con el proceso muy visible (cómo trabajamos y cómo evolucionamos). Primera versión salió con 24 slides; Didier pidió **máximo 5, pensando como vendedor**.
- **Navegación:** flechas, espacio, Inicio/Fin, `F` pantalla completa; el hash `#3` abre la diapositiva 3. Al imprimir sale una por página.

## 2. Estructura (6 slides: 5 pedidas + 1 ejemplo agregado a pedido)
1. **Promesa:** «Pago por actividades terminadas, no por horas» + 3 ideas (paquete mensual de puntos, tamaño por actividad, se paga la tarea finalizada).
2. **Ejemplo real de septiembre (agregado el 14 oct; ajustado el mismo día):** las **9 tareas del equipo marcadas «Finalizada»/«Finalizado» en el informe de septiembre** (API-1834, 1427, 1738, 1877, 1867, 1839, 1851, 1871, 1872) suman **93 puntos** (2×21, 2×13, 2×8, 1×5, 2×2). Cubren todos los paquetes; el más chico, **Inicial 114 (sobran 21)**. Se excluye API-1860 (figura de Gabriel pero la implementó un revisor). Solo estas (Daniel, Gabriel y Luis, estado Finalizada/Finalizado; Didier lo confirmó): el slide ya no menciona Ready for prod. Las 10 tareas que cerraron el mes en Ready for prod (+91 puntos, total 184) quedan fuera del ejemplo. El script verifica 93. Primera versión del slide usaba las 19 tareas con pase a Ready for prod en septiembre (184); Didier pidió basarse en las marcadas Finalizada del Excel de Daniel, Gabriel y Luis.
3. **Cómo trabajamos hoy (dolor):** flujo de Jira To Do → Done con devoluciones (44 desde In review, 2 desde UAT), lo que se mide (659 h estimadas, 819 h ejecutadas, 41 devoluciones), la espera de revisión que no se mide, y 3 cifras: +169 h en 4 esperas, 12 de 19 con devoluciones cumplieron, 8 de 19 PRs con Sonar en rojo y 7 PRs sin estándar. Chip «Con la propuesta: aquí se paga» bajo Ready for prod.
4. **Cómo trabajaremos (solución):** 6 pasos (Diseño conjunto, Tamaño en puntos, Desarrollo, PR abierto, PR aprobado = entrega, Defectos y Ready for prod) con «Se observa» en cada uno; qué se paga; reglas de corrección y cambios.
5. **Cómo se calcula (oferta):** 104 actividades → 3.220,5 h → +30 % = 4.186,65 h → 983 puntos; escala 1–21 y «Dividir»; paquetes Inicial 114 / Ampliado 190 / Avanzado 350 puntos al mes; valor del punto pendiente.
6. **Cómo evolucionamos + cierre:** ciclo mensual Medir → Detectar → Ajustar → Verificar, ruta (antes de empezar, mes 1, cada mes), siguiente paso y «Por definir juntos».

## 3. Decisiones de Didier en v5
- **Se paga la tarea finalizada = Ready for prod** (no el PR aprobado a secas). Resuelve el pendiente 15 de v4. Done (despliegue a producción) no es el disparador.
- **Regla de entrega y corrección (14 oct 2026):** la tarea se **entrega con el PR aprobado**; luego el equipo **corrige todos los defectos** reportados en las etapas posteriores (UAT), **máximo 5 días desde abierto el PR**. **Si el cliente no da feedback, se cobra.** Si pide cambios adicionales después de esos 5 días, se cobra como **control de cambios**. **Solo se ajusta lo que es error de la implementación; los cambios de alcance son controles de cambio** (tarea nueva con su propio tamaño, como en v4). Interpretación de Claude, por confirmar: se cobra al quedar en Ready for prod o al vencer la ventana sin feedback; «5 días» se escribió tal cual (v4 mide esperas en días hábiles).
- **Máximo 5 slides.** Lo que no cabe (94 actividades, 20 PRs, tablas de devoluciones, compromisos detallados, preguntas frecuentes, 7 mejoras con su dato) sigue en `v4/` como evidencia; no se lleva a la presentación.
- **Proceso visible:** cómo trabajamos (slide 2), cómo cambia (3), cómo se calcula (4) y cómo evolucionamos (5). La cadencia mensual del ciclo es propuesta de Tech and Solve; solo el «al cierre del primer mes se comparan los tamaños» viene de v4.

- **El cliente no necesita saber con cuántas personas trabajamos (14 oct 2026):** los paquetes se muestran solo en puntos (114 / 190 / 350 al mes). Se quitaron de la presentación: número de personas por paquete, «equipo actual», 38 puntos por persona, horas reales y % de la capacidad de 504 h, «3 personas · 524 h» del flujo y la fuente F6. Internamente la base sigue siendo personas × 38 (ver `../v4/CONTEXTO.md`).

- **Paquetes (14 oct 2026, decisión de Didier):** tres escalones **Inicial 114 · Ampliado 190 (intermedio) · Avanzado 350**. Inicial = para meses de menos carga (es el 114 de v4, 3×38 internos); Ampliado = el 190 de v4 (5×38), ahora en el medio y resaltado; Avanzado = 350, **definido por Didier, no sale de la regla personas × 38** (350/38 = 9,2) y no tiene histórico. Se quitó el «Estándar» de 152. «Avanzado» es nombre propuesto por Claude (por confirmar); el 114 como piso lo dedujo Claude de «uno por si tiene menos carga» (por confirmar). Con la serie de 13 meses: 114 cubre 12 de 13 meses, 190 los 13; el promedio es 73 y la mediana 68 puntos.

## 4. Reglas que se mantienen
Las de `../CLAUDE.md` y v4: tallaje = tiempo real + 30 %, solo actividades finalizadas del equipo (incluye Ready for prod); toda cifra es citable (pie de cada slide con F1–F6); sin nombres de personas ni IA ante el cliente; sin mencionar versiones previas; lo pendiente se muestra marcado (valor del punto, puntos no usados, días de aviso, actividades en curso: 6 de 26 abiertas al 9 oct).

## 5. Verificado y no verificado
- Cifras copiadas de v4 (recalculadas el 9 oct 2026); no se recalcularon en v5. «373 h reales · 74 %» etc. vienen de la tabla de paquetes de v4.
- Pendientes de ajuste por la decisión del pago: v4 (congelada) todavía dice «PR aprobado»; las horas de los paquetes y la serie mensual se calcularon con la fecha de pase a Ready for prod (para septiembre) o «Fecha fin»: coherente con el nuevo disparador.
- El PDF se exporta con Chrome headless; el chequeo de marca (`check_brand_compliance.py`) pasa sin violaciones. El texto «→» se evitó (Poppins no lo tiene); las flechas son SVG.

## 6. Archivos
- `calculos/build_v5.py` genera el borrador (`deck-borrador.html`, con tokens de logo); `calculos/rebuild.sh [dir_png]` embebe los logos, corre el chequeo de marca y renderiza PNGs; `calculos/render.sh` hace las capturas con Chrome. Las cifras están escritas en el script con la referencia a v4.
- PDF: `google-chrome --headless=new --no-pdf-header-footer --print-to-pdf=… archivo.html`.

## 7. Historial de pedidos sobre v5
1. «Hacer mucho más visible el proceso, como slides de una propuesta comercial ganadora; llévate todo el proceso de cómo hacemos y evolucionamos.»
2. «Son demasiadas, piensa como vendedor y resume en máximo 5.»
3. «La propuesta es que solo se pague por tarea finalizada, que es cuando queda Ready for prod.»
4. «Como regla, la tarea se entrega en PR aprobado; el equipo corrige defectos de etapas posteriores, máx. 5 días desde abierto el PR; sin feedback se cobra; cambios después de 5 días o de alcance son control de cambios; solo se ajustan errores de implementación.» → paso 5 «PR aprobado = entrega», paso 6 «Ready for prod» (con la corrección de defectos), tarjeta «Reglas de corrección y cambios» en el slide 3 (se quitó «Qué cambia en lo que mira Viva», que sigue en el slide 2 y en la fila «Se observa»).
5. «La idea de este enfoque es que el cliente no necesita saber con cuántas personas internamente trabajamos para cerrar los puntos que compró.» → se quitó todo número de personas, capacidad y horas por paquete de la presentación (ver sección 3).
6. «Adiciona un ejemplo de tareas liberadas en septiembre, cuántos puntos equivale y qué paquete lo habría completado igualmente… como una página nueva.» → nuevo slide 2 (queda en 6 slides, por pedido explícito, por encima del máximo de 5).
7. «Pensemos en otros paquetes» → comparación de topes contra los 13 meses (60, 75, 90, 114, 152, 190…).
8. «Uno por si tiene menos carga, el que ahora tenemos de 190 puntos y otro superior de 350.» → Inicial 114 / Ampliado 190 / Avanzado 350 en los slides 1, 2 y 5.
9. «Fíjate en las que en septiembre se marcaron como finalizad@ en el Excel de seguimiento, las que pertenecen a Daniel, Gabriel y Luis.» → slide 2 pasa a 9 tareas / 93 puntos, solo esas, sin la extensión a Ready for prod. Pendiente de confirmar: API-1860 (Finalizada a nombre de Gabriel en el informe) sigue excluida por la regla de v4.
