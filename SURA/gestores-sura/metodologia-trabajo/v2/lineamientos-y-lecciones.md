# Lineamientos y lecciones aprendidas · Presentación del equipo para SURA

> Documento interno de Tech and Solve. No se entrega al cliente.
> Construido el 15 de octubre de 2026 al cerrar `v1`; actualizado el 16 de octubre de 2026 para
> `v2`, que incorpora los comentarios recibidos sobre la forma de trabajo. Este documento
> **evoluciona** `../v1/lineamientos-y-lecciones.md`, que queda intacto, igual que el resto de
> `../v1/`. Propósito: que la próxima iteración acierte a la primera.

---

## 1. Qué es este entregable

Una presentación comercial para SURA sobre **cómo trabajaría el equipo de Tech and Solve**
que construye los sistemas agénticos del MVP de Gestores, y **por qué ese equipo, con la IA
de Tech and Solve, es la mejor opción**.

No es un dimensionamiento ni un cronograma. Esos viven en `estimacin mvp/`.

### Archivos

| Archivo | Rol |
|---|---|
| `Tech and Solve - Dinámica de trabajo del equipo.html` | **Fuente de verdad.** Se itera aquí primero. |
| `Tech and Solve - Dinámica de trabajo del equipo.pptx` | Derivado del HTML. Se regenera después de cada cambio. |
| `_generador/` | Genera el `.pptx` de esta versión, junto al HTML. Instrucciones en su `README.md`. |
| `lineamientos-y-lecciones.md` | Este documento. |

Las fotos del equipo salen de `~/Documents/GitHub/techandsolve/personas/<persona>/`.

---

## 2. Decisiones de contenido que ya están tomadas

### Alcance del equipo

- **El equipo construye los sistemas agénticos**: los agentes, lo que los gobierna (golden set,
  compuerta, traza, umbrales, calibración del juez, techos de autonomía) y la base de la torre
  de control (contrato de eventos y capas 1 y 2).
- **El front, la API orquestadora, la integración con el core y las plataformas los lideran los
  equipos de SURA.** Los agentes se integran sobre eso.
- **No se habla de tiempos del proyecto.** Ni días, ni sprints totales, ni calendario. El
  orden de los bloques es «un orden, no un calendario». El equipo tech propuso una nota de «7
  sprints» y se retiró (15-oct-2026). **Excepción decidida (16-oct-2026):** la cadencia de una
  micro-liberación cada dos o tres días (lámina 10) se queda. Es dinámica de trabajo, no un plazo
  del proyecto; no se suman fechas, duraciones ni número de liberaciones.

### Composición del equipo

| Persona | Rol en la propuesta | Dedicación |
|---|---|---|
| Raúl A. De Villa C. · Co-Founder | Acompaña los hitos clave con mirada crítica de negocio y de solución | Puntual |
| Alexandra Acosta · Gerente de Éxito del Cliente | La experiencia y los estándares de toda la compañía | Puntual |
| Jorge Andrés Gómez Velásquez · Líder del Éxito del Cliente | Punto de contacto con SURA: lo acordado, con calidad y a tiempo | Puntual |
| Didier Fabián Franco Gómez · Líder de Comunidad | Arquitecto Líder (en v1, «arquitecto parcial»): marca el rumbo técnico, lo alinea con la arquitectura de SURA y revisa | Parcial |
| Juan Gabriel Colorado y Gian Valdiris · Desarrolladores IA | Construyen los sistemas agénticos | Completa |
| Una persona del equipo tech, sin nombre aún | Soporte: atiende lo que ya opera para no interrumpir el flujo | Media jornada |

- **El arquitecto no implementa características.** Define con el equipo prácticas, arquetipos,
  componentes y lineamientos; se alinea con el equipo de arquitectura de SURA; revisa.
- **Los desarrolladores no tienen frentes.** Un equipo, un backlog: cada uno toma la siguiente
  prioridad. Nunca asignar «A hace Solicitud, B hace Evaluación».
- **Los desarrolladores participan en refinamiento y dimensionamiento, y luego implementan.**

### Forma de trabajo (v2)

- **Flujo continuo, no sprints.** El concepto de sprint quedó obsoleto en SURA por la velocidad
  de entrega que permite la IA. Hay arranque, una primera liberación con un conjunto mínimo
  acordado con SURA, y después micro-liberaciones cada dos o tres días. **No se menciona Scrum**
  (ni sprint, daily, planning, retro ni velocidad); la sincronía diaria se llama así.
- **QA es el ambiente de certificación:** Tech entrega en QA y SURA certifica en QA (precisión de
  Didier, 16-oct-2026).
- **Etapas de la característica (tomadas del documento *Spec Flow* de Raúl):** Propuesta,
  Definición, Lista para construir, Construcción, Verificación, Certificación, Liberada y Estable.
  Se usan sus nombres, con ajustes: sin la frase de que «el agente genera» (es IA y va en su
  sección), sin «5 días hábiles» (es un plazo), con «sesión de definición» y «característica» en
  lugar de «mesa» y «ficha». **Etapa** es lo que recorre una característica (lámina 4) y la lámina 18
  muestra cómo nuestra IA actúa en cada una (16-oct-2026): las afirmaciones son las de antes,
  respaldadas por LLMCoder, reagrupadas sobre las ocho etapas; no se agregó ninguna nueva. «Fases»
  queda solo para el proceso interno de la IA de las láminas 16 y 17.
- **Código de color de quién participa**, el mismo en todo el documento: **verde, SURA**; **violeta,
  Tech**; **ámbar, los dos**. Va en etiquetas y puntos de las láminas 4, 5, 6, 10, 11 y 12, con
  su leyenda («Quién participa»). En las demás láminas el color no significa eso; por eso en la
  lámina 18 la etiqueta «Persona» va en violeta oscuro y no en verde.
- **Como un tablero, sin decir la palabra.** Las características recorren las etapas de la
  lámina 4, una por una y a su ritmo, sin lotes, ni cortes, ni iteraciones. «Corte» y «corte
  limpio» ya no se usan: hay **hitos de activación**, los momentos en que algo es usable de punta
  a punta y SURA decide activarlo. El tablero de la lámina 12 tiene una columna por etapa.
- **Micro-liberación = lo que llega al ambiente de certificación.** El paso a producción es aparte,
  lo decide SURA y se marca con hitos de activación, no con cortes. «Hecha» es certificada.
- **Ambiente de certificación.** Todas las micro-liberaciones llegan allí; **SURA certifica con
  acuerdos de servicio de certificación que define SURA** (no ponemos cifras: el plazo lo declara
  su dueño) y decide cuándo activar en producción.
- **La mejora continua incluye a SURA** (16-oct-2026): el arquitecto la lleva, pero el Product Owner y
  el negocio aportan lo que ven y acuerdan los ajustes. En la matriz y en el tablero cuenta como
  «los dos».
- **Mejora continua, no retrospectiva.** Actividad transversal a cargo del arquitecto, **técnica y
  de alineación con el negocio de SURA** (precisión de Didier, 16-oct-2026).
- **Soporte, un rol más del equipo implementador.** Media jornada de una persona, con su tarjeta de
  rol en las láminas 2 y 3, para que atender lo que ya opera no interrumpa la creación de nuevas
  características. No se cita la duración (el comentario hablaba
  de unos tres meses): es un plazo del proyecto.
- **Negocio hombro a hombro con el equipo**, al estilo de la programación extrema: con
  liberaciones frecuentes, la característica es sobre todo una conversación. El **golden set**
  se conserva para exigir pruebas.
- **Vocabulario nuevo:** «historia de usuario» pasa a **característica**; «épica» pasa a **meta
  funcional**. Los grupos de agentes de la lámina 14 ya no se llaman «incrementos» sino **bloques**, para no chocar con las metas funcionales del backlog. «Historia clínica» sigue siendo historia clínica.
- **Una característica acotada cabe en no más de tres días** (precisión de Didier, 16-oct-2026); si
  no cabe, se parte. Por eso el acuerdo del tablero no habla de ramas de un día: sería contradictorio.
- **Sin puntos.** El comentario dudaba de abrir ahora la discusión de «cuánto es un punto». Se
  sustituye por tamaño: las metas funcionales conservan su talla S, M, L, XL (la del cliente) y las
  características son **acotadas o amplias**; las amplias se parten. Tomado de la idea de talla del
  documento *Spec Flow* de Raúl. Se retiraron estimación, planning y velocidad.
- **Estimación de tiempos:** se mantiene fuera. Se retiró también la nota de «7 sprints».
- **Arquitectura evolutiva**: la de cada sistema agéntico se define al empezar su
  implementación. Solo lo común se define en el arranque.
- **La trazabilidad para la torre de control es transversal**: se define en el arranque y se
  implementa en todos los bloques.
- **Qué recibe SURA con cada micro-liberación**: las características trabajadas con su estado,
  lo liberado en el ambiente de certificación y las evidencias según la definición de hecho.

### La IA de Tech and Solve

- **Lo que la hace nuestra es lo que construimos encima del modelo**: base de conocimiento,
  proceso por fases, reglas desde revisiones reales, agentes especializados, controles y firma
  humana. Esa es la lámina en capas.
- **Exclusiva del equipo tech**: no se comercializa ni se abre a terceros.
- **Sobre modelos de primer nivel de Anthropic.** No nombrar modelos ni versiones.
- **No decir «derechos de autor»**: no hay registro legal. Decir «propia» y «exclusiva».
- **No dar cifras internas**: ni cuántos agentes, ni cuántas reglas, ni cuántas fases.
- **Separar lo que ya opera de lo que aplicaremos en SURA.** Lo que ya opera se respalda con
  LLMCoder; lo que es propósito para SURA se dice como tal.
- **No nombrar a otros clientes** ni el repositorio de donde salen los ejemplos.

---

## 3. Estructura vigente de la presentación

El hilo conductor es: **quién → el mapa → cómo nace una característica → cómo fluye hasta
certificarse → qué sale → hacia dónde → la IA → por qué nosotros.**

| # | Lámina | Para qué está |
|---|---|---|
| 1 | Portada: MVP de Gestores: innovación para SURA | Método de trabajo y propuesta de valor en una línea |
| 2 | Equipo Tech and Solve (**oculta** en el `.pptx`, como la dejó el equipo tech) | Quién construye y quién acompaña |
| 3 | Equipo de trabajo propuesto: modelo Tech and Solve y SURA | Roles y dedicación de cada lado |
| 4 | Cada característica recorre las etapas | **El mapa.** Ocho etapas: SURA define (1 a 3), el equipo construye y verifica (4 y 5), SURA certifica y activa (6 y 7), y la 8 confirma que es estable; la mejora continua es transversal |
| 5 | Construimos los sistemas agénticos | Alcance |
| 6 | El arquitecto define el cómo | Gobierno técnico |
| 7 | Las características se definen con SURA, con el negocio junto al equipo | Con SURA · definir |
| 8 | Las metas funcionales ordenan el backlog; las características se parten si son amplias | Con SURA · definir |
| 9 | Cuándo entra una característica a construcción y cuándo se da por hecha | Flujo |
| 10 | Después de la primera liberación, el flujo es continuo | Flujo y certificación |
| 11 | Qué hace cada quien en cada momento | Quién hace qué, por etapa |
| 12 | Un tablero con las etapas y seis acuerdos (una columna por etapa) | Flujo y participación |
| 13 | Qué recibe SURA con cada micro-liberación | Qué recibe SURA |
| 14 | El orden sugerido: tres bloques y dos hitos de activación | Hacia dónde |
| 15 | IA de Tech and Solve | Portada de sección |
| 16 | Lo que la hace nuestra es lo que construimos encima del modelo | Qué es |
| 17 | No es un IDE con IA | En qué se diferencia |
| 18 | Nuestra IA potencia cada etapa | Dónde actúa, sobre las ocho etapas de la lámina 4 más la mejora continua |
| 19 | Calidad, performance y seguridad que se verifican | Qué garantiza |
| 20 | Tech and Solve: más que tecnología, resultados sostenibles para SURA | Cierre en cinco ejes |

**Las ocho etapas son la columna vertebral.** Al cliente le gustan porque dejan claro en qué
momentos se le necesita y en cuáles no. Las demás láminas siguen sus zonas en orden.

---

## 4. Reglas de redacción

### Tono comercial

- **El enfoque lo da Didier; la redacción es nuestra.** No copiar sus frases literales:
  convertirlas en texto corto, orientado al valor para SURA. Los datos factuales (nombres,
  cargos) sí van exactos.
- **Una idea por lámina.** El título la afirma; el cuerpo la sostiene.
- **Títulos afirmativos**, sin signos de interrogación, coherentes entre sí.

### Dónde va la IA

- **La IA de Tech and Solve vive en su sección (láminas 15 a 19)**, más la portada y el cierre. En
  la sección de dinámica de trabajo (láminas 2 a 14) no se habla de nuestra IA: ni «se genera con
  IA», ni «potenciados por la IA», ni «antes de generar código». «Desarrollador IA» es el cargo de
  las personas y se conserva. «Prompt» y «agente» hablan del producto de SURA, no de nuestra IA.

### Cómo nos referimos a SURA

SURA es protagonista, nunca «los otros».

| No usar | Usar |
|---|---|
| Lo construyen otros equipos | Lo lideran los equipos de SURA |
| Fuera del equipo | Equipo SURA |
| No participa | No requiere tiempo de SURA |
| Citas con SURA | Sesiones con SURA |
| SURA prioriza; el equipo decide | SURA prioriza; el equipo toma la siguiente prioridad |
| Se enchufan | Se integran |
| Error tolerable y muestra revisada | Definen el error tolerable y validan la muestra clínica |

Cada rol de SURA se describe por lo que aporta, con verbo.

### Terminología

- Se mantienen las del `CLAUDE.md` del repositorio: golden set, LLM-as-a-judge, core, SuraHis,
  modo shadow, canary, acertividad (vocabulario del cliente).
- **«Compuerta»**, no «gate». Se unificó en todo el deck.
- **«Definición de hecho»** en el texto visible; «Definition of Done» solo en las notas.
- **«Equipo tech»** para Tech and Solve; **«equipos de SURA»** para el cliente.

### Gramática que ya se corrigió

- Minúscula después de dos puntos, salvo nombres propios.
- Coma tras frase introductoria («Con cada micro-liberación, SURA…»).
- Un solo «dos puntos» por oración.
- Artículos y preposiciones que faltaban («Iteración **del** equipo tech»).

---

## 5. Reglas de fuentes

Aplican las dos reglas de oro del `CLAUDE.md` del repositorio.

- **Manifiesto Ágil**, con enlace oficial **en la misma lámina** donde se usa (lámina 4). Se
  presenta como práctica de industria, no como norma. En v2 **se retiró la cita a la Guía de Scrum
  2020** de la lámina del flujo, porque la dinámica ya no se presenta como adaptación de Scrum.
- **El documento de proceso de desarrollo con IA está en borrador.** Sus fases se usan como
  nuestras, pero no se cita como fuente ni se presentan sus políticas como práctica vigente.
- **Toda afirmación sobre nuestra IA se contrasta contra LLMCoder** antes de entrar al deck.

---

## 6. Reglas de diseño

- Marca: Poppins, violeta `#280265`, acento `#5300DF`, ámbar `#B9720A`, verde `#1B6B4F`.
- **Tarjeta de persona única** (`.pcard` en el HTML, `personCard` en el generador): foto o
  inicial en círculo con aro blanco, nombre en negrita, rol debajo. Se usa igual en todas las
  láminas. Variante `.sm` para paneles con muchas personas y `.light` sobre fondo claro.
- **Fotos**: JPG o PNG de al menos 800 × 800 px, guardadas en `personas/`. No WebP ni capturas.
  Recortar centrado en la cara **y con aire sobre la cabeza**: el círculo corta las esquinas.
- Láminas de sección en violeta completo con título blanco.
- Toda lámina se verifica sin desbordes antes de entregar.

---

## 7. Errores cometidos que no hay que repetir

1. **Asumir el equipo del dimensionamiento.** El dimensionamiento habla de siete integrantes.
   Este equipo es un arquitecto líder, dos desarrolladores y un soporte a media jornada. Preguntar
   la composición antes.
2. **Meter estimación de tiempos.** El cliente quería la dinámica, no plazos.
3. **Estimar en puntos o en tallas a nivel característica.** Sin puntos: las tallas S, M, L y XL
   son de las metas funcionales; las características son acotadas o amplias.
4. **Segmentar a los desarrolladores por frentes.** Son un equipo con un backlog.
5. **Presentar al arquitecto como constructor.** Define, alinea y revisa; no implementa.
6. **Afirmar sobre nuestra IA lo que no está respaldado**: «no es un servicio externo»,
   «derechos de autor», cifras de agentes y reglas, prácticas del borrador de gobierno.
7. **Nombrar los modelos.** Basta con «modelos de primer nivel de Anthropic».
8. **Hablar de Scrum, de sprints o de retrospectivas.** En v2 salieron del cuerpo; no volver a
   introducirlos ni siquiera para decir que no los usamos.
9. **Llamar «otros equipos» a SURA** y usar jerga coloquial.
10. **Copiar literal lo que dicta Didier.** Hay que redactarlo con tono comercial.
11. **Reemplazar una lámina sin avisar al rediseñarla.** Si se rehace una lámina, la anterior
    no se borra sin confirmar. Si el cliente pide «otra forma», se agrega al lado para comparar.
12. **Ordenar las láminas sin hilo conductor.** Primero el mapa y la gente; después el detalle.
13. **Interpretar instrucciones ambiguas sin decirlo.** Ante «deja esa» o «deja solo el
    título», decir qué se entendió y ofrecer revertir.
14. **Meter nuestra IA en la sección de dinámica de trabajo.** Va en las láminas 15 a 19.
15. **Un término con dos sentidos.** «Micro-liberación» es lo que llega a QA, no a producción;
    «meta funcional» es del backlog y los grupos de agentes son «bloques».
16. **Reemplazar una lámina por script sin contar láminas.** Un reemplazo se llevó dos láminas
    vecinas; tras cada cambio, verificar que siguen siendo 20.
17. **Dos nombres para la misma persona.** Usar el nombre completo igual en todas las láminas.

---

## 8. Cómo trabajar la próxima iteración

1. Leer este documento, el de `../v1/` para ver qué cambió, y el `context.md` vigente de la cuenta.
2. Hacer cada cambio **primero en el HTML** y revisar que no haya desbordes.
3. Llevar el mismo cambio a `v2/_generador/generar.js` y regenerar con `npm run generar`. Los dos
   archivos deben decir lo mismo.
4. Si el cambio toca personas, usar la tarjeta estándar y las fotos de `personas/`.
5. Antes de entregar, pasar la lista de verificación de la sección 9.
6. Commit en español y en minúscula, cuando Didier lo pida.

---

## 9. Lista de verificación antes de entregar

- [ ] Ningún texto se desborda de su caja ni de la lámina, en HTML y en `.pptx`.
- [ ] El `.pptx` pasa la validación y se abrió en PowerPoint al menos una vez.
- [ ] HTML y `.pptx` tienen las mismas láminas, en el mismo orden y con los mismos textos.
- [ ] Ninguna mención de tiempos del proyecto; las únicas cifras permitidas son la cadencia de dos o tres
  días entre micro-liberaciones y el tamaño de una característica acotada, de no más de tres días.
- [ ] Ninguna mención de Scrum, sprint, retrospectiva, puntos ni velocidad.
- [ ] La IA de Tech and Solve solo en las láminas 15 a 19, la portada y el cierre.
- [ ] Un término, un sentido: micro-liberación, QA, meta funcional, bloque.
- [ ] Las 20 láminas siguen ahí, en el mismo orden.
- [ ] Ningún desarrollador con frente asignado.
- [ ] SURA nombrado como protagonista; ningún «otros equipos» ni «no participa».
- [ ] Nada sobre nuestra IA que no esté respaldado; sin cifras internas ni nombres de modelos.
- [ ] Toda cita al Manifiesto con su enlace en la misma lámina; ninguna mención de Scrum.
- [ ] Nombres y cargos del equipo exactos, e iguales en todas las láminas.
- [ ] Sin menciones a otros clientes.

---

## 10. Pendientes abiertos al cierre de v2

- **«Sprint» y los demás documentos de la cuenta.** El dimensionamiento de la torre de control
  habla de nueve sprints, y la hoja de seguimiento de SURA define «1 sprint = 10 días hábiles,
  estándar SuraHis». El comentario recibido dice que el sprint quedó obsoleto en SURA. Confirmar
  con SURA antes de presentar v2 junto a esos documentos.
- **Soporte en la matriz (lámina 11):** aparece como «Soporte:» dentro de la columna de
  desarrolladores; si se quiere más claro, darle su propia columna.
- **CIE-10 y CUPS (lámina 8)** se definen en letra pequeña, pero sin enlace a su emisor, y la regla
  de oro pide enlace oficial en el mismo bloque. Conseguir y verificar las dos URL, o cambiar el
  ejemplo por uno sin siglas.
- **Soporte de media jornada:** definir quién es la persona. Hoy aparece sin nombre.
- **Duración del soporte:** el comentario sugería unos tres meses. No se incluyó por ser un plazo
  del proyecto; decidir si se dice.
- **Certificación:** los acuerdos de servicio los define SURA. Confirmar con ellos que están de
  acuerdo con que la propuesta los nombre así.
- **Cadencia de dos o tres días:** decidida para la lámina 10, pero viene del comentario recibido.
  Confirmar que se puede sostener.
- **«Garantizar resultados medibles»** (lámina 2, oculta) viene del equipo tech y promete más de
  lo que podemos sostener. Considerar «lograr».
- **Fotos de Juan Gabriel y Gian:** la de Gian es de 472 × 538 px y puede verse blanda; los
  apellidos salen de la carpeta de personas y del correo.
- **La foto de Alexandra** es de 120 px y se ve borrosa en pantalla grande.
- **Afirmaciones sin documento de respaldo:** «madurez medida» y «uso responsable» vienen de
  Didier. Confirmar que se pueden sostener ante SURA.
- **El `.pptx` no se ha abierto en PowerPoint.** Revisar fotos circulares, celdas combinadas de
  la tabla, la lámina oculta y la fuente Poppins.
- **Nada está en commit.**
