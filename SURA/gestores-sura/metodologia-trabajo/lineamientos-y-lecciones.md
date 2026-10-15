# Lineamientos y lecciones aprendidas · Presentación del equipo para SURA

> Documento interno de Tech and Solve. No se entrega al cliente.
> Construido el 15 de octubre de 2026, al cerrar la primera versión de
> `Tech and Solve - Dinámica de trabajo del equipo.html` y su `.pptx`.
> Propósito: que la próxima iteración acierte a la primera.

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
| `_generador/` | Genera el `.pptx`. Instrucciones en su `README.md`. |
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
  orden de incrementos es «un orden, no un calendario».

### Composición del equipo

| Persona | Rol en la propuesta | Dedicación |
|---|---|---|
| Raúl A. De Villa C. · Co-Founder | Acompaña los hitos clave con mirada crítica de negocio y de solución | Puntual |
| Alexandra Acosta · Gerente de Éxito del Cliente | La experiencia y los estándares de toda la compañía | Puntual |
| Jorge Andrés Gómez Velásquez · Líder del Éxito del Cliente | Punto de contacto con SURA: lo acordado, con calidad y a tiempo | Puntual |
| Didier Fabián Franco Gómez · Líder de Comunidad | Arquitecto: marca el rumbo técnico, lo alinea con la arquitectura de SURA y revisa | Parcial |
| Desarrollador A y Desarrollador B | Construyen los sistemas agénticos | Completa |

- **El arquitecto no implementa historias.** Define con el equipo prácticas, arquetipos,
  componentes y lineamientos; se alinea con el equipo de arquitectura de SURA; revisa.
- **Los desarrolladores no tienen frentes.** Un equipo, un backlog: cada uno toma la siguiente
  prioridad. Nunca asignar «A hace Solicitud, B hace Evaluación».
- **Los desarrolladores participan en refinamiento y estimación, y luego implementan.**

### Forma de trabajo

- Sprints de **diez días hábiles** (el estándar de SuraHis que fija la hoja de seguimiento).
- **SURA define las historias de usuario y recibe la demo.** Las ceremonias son internas.
- **Tres sesiones con SURA por sprint**: alineación de arquitectura, sesión de historias, y
  demo con entrega.
- **Estimación por puntos.** Las épicas tienen talla (S, M, L, XL) y sirven para ordenar el
  backlog. Las historias que se desprenden se estiman en puntos (1, 2, 3, 5, 8, 13; más de 13
  se parte). El sprint se llena con la velocidad del equipo.
- **Arquitectura evolutiva**: la de cada sistema agéntico se define al empezar su
  implementación. Solo lo común se define en el arranque.
- **La trazabilidad para la torre de control es transversal**: se define en el arranque y se
  implementa en todos los incrementos.
- **Qué recibe SURA al cierre de cada sprint**: las historias trabajadas con su estado, la demo
  de lo implementado y las evidencias de cada implementación según la definición de hecho.

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

El hilo conductor es: **quién → el mapa → cómo nace una historia → cómo vive en el sprint →
qué sale → hacia dónde → la IA → por qué nosotros.**

| # | Lámina | Para qué está |
|---|---|---|
| 1 | Portada: MVP de Gestores | Proyecto, dos secciones y el equipo de liderazgo |
| 2 | Equipo Tech and Solve | Quién construye y quién acompaña |
| 3 | Equipo de trabajo propuesto: modelo Tech and Solve y SURA | Roles y dedicación de cada lado |
| 4 | Diez etapas | **El mapa.** Cuándo necesitamos a SURA y cuándo no |
| 5 | Construimos los sistemas agénticos | Alcance |
| 6 | El arquitecto define el cómo | Gobierno técnico |
| 7 | Las historias se escriben con SURA | Con SURA · definir |
| 8 | Épicas con talla, historias con puntos | Con SURA · definir |
| 9 | Cuándo entra una historia y cuándo está hecha | Sprint interno |
| 10 | Un sprint de diez días hábiles | Sprint interno |
| 11 | Qué hace cada quien en cada momento | Sprint interno |
| 12 | Tablero y seis acuerdos | Sprint interno |
| 13 | Qué recibe SURA al cierre de cada sprint | Con SURA · ver y recibir |
| 14 | El orden sugerido | Con SURA · ver y recibir |
| 15 | IA de Tech and Solve | Portada de sección |
| 16 | Lo que la hace nuestra es lo que construimos encima del modelo | Qué es |
| 17 | No es un IDE con IA | En qué se diferencia |
| 18 | Nuestra IA potencia cada etapa | Dónde actúa |
| 19 | Calidad, performance y seguridad que se verifican | Qué garantiza |
| 20 | Por qué el equipo de Tech and Solve es la mejor opción | Cierre |

**Las diez etapas son la columna vertebral.** Al cliente le gustan porque dejan claro en qué
momentos se le necesita y en cuáles no. Las demás láminas siguen sus zonas en orden.

---

## 4. Reglas de redacción

### Tono comercial

- **El enfoque lo da Didier; la redacción es nuestra.** No copiar sus frases literales:
  convertirlas en texto corto, orientado al valor para SURA. Los datos factuales (nombres,
  cargos) sí van exactos.
- **Una idea por lámina.** El título la afirma; el cuerpo la sostiene.
- **Títulos afirmativos**, sin signos de interrogación, coherentes entre sí.

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
- Coma tras frase introductoria («Al cierre de cada sprint, SURA…»).
- Un solo «dos puntos» por oración.
- Artículos y preposiciones que faltaban («Iteración **del** equipo tech»).

---

## 5. Reglas de fuentes

Aplican las dos reglas de oro del `CLAUDE.md` del repositorio.

- **Guía de Scrum 2020** y **Manifiesto Ágil**, con enlace oficial **en la misma lámina** donde
  se usan. Se presentan como práctica de industria, no como norma.
- **Nuestra dinámica es una adaptación**: el Product Owner no asiste a la planning ni a la
  retro. Decirlo; no atribuirle a Scrum lo que es decisión nuestra.
- **El documento de proceso de desarrollo con IA está en borrador.** Sus etapas se usan como
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
   Este equipo es un arquitecto parcial y dos desarrolladores. Preguntar la composición antes.
2. **Meter estimación de tiempos.** El cliente quería la dinámica, no plazos.
3. **Estimar en tallas a nivel historia.** Las tallas son de épicas; las historias van en puntos.
4. **Segmentar a los desarrolladores por frentes.** Son un equipo con un backlog.
5. **Presentar al arquitecto como constructor.** Define, alinea y revisa; no implementa.
6. **Afirmar sobre nuestra IA lo que no está respaldado**: «no es un servicio externo»,
   «derechos de autor», cifras de agentes y reglas, prácticas del borrador de gobierno.
7. **Nombrar los modelos.** Basta con «modelos de primer nivel de Anthropic».
8. **Citar Scrum por algo que no dice.** Separar lo que tomamos de lo que adaptamos.
9. **Llamar «otros equipos» a SURA** y usar jerga coloquial.
10. **Copiar literal lo que dicta Didier.** Hay que redactarlo con tono comercial.
11. **Reemplazar una lámina sin avisar al rediseñarla.** Si se rehace una lámina, la anterior
    no se borra sin confirmar. Si el cliente pide «otra forma», se agrega al lado para comparar.
12. **Ordenar las láminas sin hilo conductor.** Primero el mapa y la gente; después el detalle.
13. **Interpretar instrucciones ambiguas sin decirlo.** Ante «deja esa» o «deja solo el
    título», decir qué se entendió y ofrecer revertir.

---

## 8. Cómo trabajar la próxima iteración

1. Leer este documento y el `context.md` vigente de la cuenta.
2. Hacer cada cambio **primero en el HTML** y revisar que no haya desbordes.
3. Llevar el mismo cambio a `_generador/generar.js` y regenerar con `npm run generar`. Los dos
   archivos deben decir lo mismo.
4. Si el cambio toca personas, usar la tarjeta estándar y las fotos de `personas/`.
5. Antes de entregar, pasar la lista de verificación de la sección 9.
6. Commit en español y en minúscula, cuando Didier lo pida.

---

## 9. Lista de verificación antes de entregar

- [ ] Ningún texto se desborda de su caja ni de la lámina, en HTML y en `.pptx`.
- [ ] El `.pptx` pasa la validación y se abrió en PowerPoint al menos una vez.
- [ ] HTML y `.pptx` tienen las mismas láminas, en el mismo orden y con los mismos textos.
- [ ] Ninguna mención de tiempos del proyecto.
- [ ] Ningún desarrollador con frente asignado.
- [ ] SURA nombrado como protagonista; ningún «otros equipos» ni «no participa».
- [ ] Nada sobre nuestra IA que no esté respaldado; sin cifras internas ni nombres de modelos.
- [ ] Toda cita a Scrum o al Manifiesto con su enlace en la misma lámina.
- [ ] Nombres y cargos del equipo exactos.
- [ ] Sin menciones a otros clientes.

---

## 10. Pendientes abiertos al cierre de esta versión

- **El subtítulo de la lámina 2** no menciona el acompañamiento del liderazgo.
- **La foto de Alexandra** es de 120 px y se ve borrosa en pantalla grande. Falta una de mejor
  resolución.
- **El nombre completo de Alexandra**: hoy dice «Alexandra Acosta», tomado de su correo.
- **El pie de página** sigue diciendo «Dinámica de trabajo del equipo · MVP de gestores ·
  SURA», aunque la sección se llama ahora «Equipo Tech and Solve».
- **Afirmaciones sin documento de respaldo**: «madurez medida» y «uso responsable» vienen de
  Didier. Confirmar que se pueden sostener ante SURA.
- **El `.pptx` no se ha abierto en PowerPoint.** Revisar fotos circulares, celdas combinadas de
  la tabla de roles y la fuente Poppins.
- **Nada está en commit.**
