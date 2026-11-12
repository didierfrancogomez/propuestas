// Genera la versión editable (PPTX) de la propuesta, con texto y formas nativas.
//   node generar_ppt.js            -> ../propuesta-mejora-proceso-calidad-editable.pptx (cliente)
//                                     ../propuesta-mejora-proceso-calidad-interno-editable.pptx (con la slide interna)
// El contenido replica draft.html; si cambia el HTML, actualizar también este archivo.
// Coordenadas en px del lienzo HTML (1280 x 720) -> pulgadas con px / 96.
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const ASSETS = process.env.BRAND_ASSETS;
const OUT = path.resolve(__dirname, "..");
const GH = "https://github.com/EzyWebwerkstaden/VivaAerobus.Generic.Api/pull/";
const FONT = "Arial";

const THEME = {
  name: "Tech and Solve",
  headFontFace: FONT,
  bodyFontFace: FONT,
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "280265", lt2: "EBEBFF",
    accent1: "22D0FF", accent2: "5300DF", accent3: "282E3F", accent4: "EBEBFF",
    accent5: "280265", accent6: "000000", hlink: "22D0FF", folHlink: "EBEBFF",
  },
};

const px = (v) => v / 96;

function build(withInternal, fileName) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 1280 x 720 px
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  pres.title = "Control de calidad · Generic API";
  pres.company = "Tech and Solve";
  const C = pres.SchemeColor;
  const WHITE = C.background1, LV = C.background2, DV = C.text2, BLACK = C.text1;
  const BLUE = C.accent1, GRAY = C.accent3;

  pres.defineSlideMaster({
    title: "Portada",
    background: { color: DV },
    objects: [
      { image: { path: `${ASSETS}/Isotipo_Lighter_Violet.png`, x: px(860), y: px(145), w: px(420), h: px(575), transparency: 92 } },
      { image: { path: `${ASSETS}/logo_white.png`, x: px(72), y: px(56), w: px(170), h: px(170 / 1.843) } },
    ],
  });
  pres.defineSlideMaster({
    title: "Contenido",
    background: { color: DV },
    margin: [px(56), px(72), px(48), px(72)],
    objects: [
      { image: { path: `${ASSETS}/logo_white.png`, x: px(1058), y: px(44), w: px(150), h: px(150 / 1.843) } },
      { placeholder: { options: { name: "title", type: "title", x: px(72), y: px(82), w: px(960), h: px(110), fontFace: FONT, fontSize: 30, bold: true, color: WHITE, align: "left", valign: "top", margin: 0 }, text: "" } },
    ],
    slideNumber: { x: px(1130), y: px(686), w: px(80), h: px(20), fontFace: FONT, fontSize: 9, color: LV, align: "right" },
  });

  // ---------- helpers ----------
  const kicker = (s, t) => s.addText(t, { x: px(72), y: px(56), w: px(900), h: px(22), fontFace: FONT, fontSize: 10.5, bold: true, color: BLUE, charSpacing: 1, margin: 0, isTextBox: true, objectName: "Kicker" });
  const title = (s, t) => s.addText(t, { placeholder: "title", align: "left" });
  const sub = (s, t, y, h = 58) => s.addText(t, { x: px(72), y: px(y), w: px(1000), h: px(h), fontFace: FONT, fontSize: 14, color: WHITE, margin: 0, valign: "top", isTextBox: true, objectName: "Subtitulo" });
  const source = (s, t) => s.addText(t, { x: px(72), y: px(672), w: px(1000), h: px(36), fontFace: FONT, fontSize: 9, color: LV, margin: 0, valign: "top", isTextBox: true, objectName: "Fuente" });

  // A card is one rounded rectangle with one text box on top, so its text stays editable as a block.
  function card(s, x, y, w, h, parts, o = {}) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: px(x), y: px(y), w: px(w), h: px(h), rectRadius: 0.12,
      fill: { color: o.fill || GRAY },
      line: o.border ? { color: o.border, width: 1.75 } : { type: "none" },
      objectName: o.name ? `${o.name} fondo` : "Tarjeta fondo",
    });
    s.addText(parts, {
      x: px(x + 20), y: px(y + 16), w: px(w - 40), h: px(h - 30),
      fontFace: FONT, color: WHITE, valign: o.valign || "top", margin: 0, isTextBox: true,
      objectName: o.name || "Tarjeta",
    });
  }
  const r = (text, opt = {}) => ({ text, options: opt });
  const tag = (t, color) => r(t, { fontSize: 8.5, bold: true, color: color || LV, charSpacing: 1, breakLine: true, paraSpaceAfter: 6 });
  const num = (n, small, color) => [r(n, { fontSize: 30, bold: true, color: color || BLUE }), r(small ? ` ${small}` : "", { fontSize: 14, bold: true, color: color || BLUE, breakLine: true, paraSpaceAfter: 4 })];
  const h3 = (t, size = 14) => r(t, { fontSize: size, bold: true, color: WHITE, breakLine: true, paraSpaceAfter: 4 });
  const p = (t, size = 11.5, last = false) => r(t, { fontSize: size, color: WHITE, breakLine: !last, paraSpaceAfter: 2 });
  const bullets = (items, size = 11.5) => items.map((t, i) => r(t, { fontSize: size, color: WHITE, bullet: { code: "2013" }, indentLevel: 0, breakLine: i < items.length - 1, paraSpaceAfter: 5 }));
  // Body text with **bold** segments.
  const rich = (t, size = 11.5, color, last = true) => {
    const out = t.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map((seg) =>
      seg.startsWith("**") ? r(seg.slice(2, -2), { fontSize: size, bold: true, color: color || WHITE }) : r(seg, { fontSize: size, color: color || WHITE }));
    if (!last) out[out.length - 1].options.breakLine = true;
    return out;
  };
  const band = (s, y, h, lead, text, size = 12) => card(s, 72, y, 1136, h, [r(lead, { fontSize: size, bold: true, color: BLUE }), ...rich(" " + text, size)], { fill: BLACK, valign: "middle", name: "Franja" });
  const arrow = (s, x, y) => s.addText("→", { x: px(x), y: px(y), w: px(30), h: px(40), fontFace: FONT, fontSize: 22, color: LV, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Flecha" });
  const content = (sectionTitle) => pres.addSlide({ masterName: "Contenido", sectionTitle });

  // ---------- 1 · Portada ----------
  pres.addSection({ title: "Situación" });
  let s = pres.addSlide({ masterName: "Portada", sectionTitle: "Situación" });
  s.addText("VIVA AEROBUS · GENERIC API · PROPUESTA", { x: px(72), y: px(300), w: px(900), h: px(24), fontFace: FONT, fontSize: 11, bold: true, color: BLUE, charSpacing: 1, margin: 0, isTextBox: true, objectName: "Kicker" });
  s.addText("Control de calidad automático\ny propio para el código de Viva", { x: px(72), y: px(334), w: px(1000), h: px(150), fontFace: FONT, fontSize: 42, bold: true, color: WHITE, margin: 0, valign: "top", isTextBox: true, objectName: "Titulo portada" });
  s.addText("Tech and Solve para Viva Aerobus · Octubre de 2026 · Documento confidencial", { x: px(72), y: px(672), w: px(900), h: px(20), fontFace: FONT, fontSize: 9, color: LV, margin: 0, isTextBox: true, objectName: "Pie" });

  // ---------- 2 · Estado actual ----------
  s = content("Situación");
  kicker(s, "ESTADO ACTUAL");
  title(s, "El equipo de desarrollo de Generic API no tiene acceso a la herramienta de calidad");
  const c3 = [72, 456, 840], cw = 368;
  card(s, c3[0], 222, cw, 250, [tag("DÓNDE ESTÁ"), h3("En la infraestructura de un tercero"),
    r("La herramienta de calidad, SonarQube, vive en ", { fontSize: 11.5 }), r("sonarqube.ezyflight.se", { fontSize: 11.5, bold: true }),
    r(": un dominio de Ezy, administrado por Ezy. Cada cambio de código enlaza ahí (por ejemplo, ", { fontSize: 11.5 }),
    r("#2511", { fontSize: 11.5, color: BLUE, hyperlink: { url: GH + "2511" } }), r(").", { fontSize: 11.5 })]);
  card(s, c3[1], 222, cw, 250, [tag("QUÉ VE EL EQUIPO"), h3("Solo un semáforo y un número"),
    p("El equipo de desarrollo de Generic API no tiene acceso: ve si el cambio pasó el filtro de calidad y cuántos problemas tiene, pero no cuáles ni dónde están.", 11.5, true)]);
  card(s, c3[2], 222, cw, 250, [tag("QUÉ IMPLICA", BLUE), h3("Se desaprovecha la herramienta"),
    p("Lo que no se ve, no se corrige. Y cualquier cambio de reglas o de accesos depende de pedírselo a un tercero.", 11.5, true)], { border: BLUE });
  band(s, 494, 70, "Además,", "la revisión automática actual de Generic API **no ejecuta las pruebas unitarias** ni **bloquea**: un cambio con problemas detectados puede llegar igual a la rama principal.");

  // ---------- 3 · Lo que cuesta hoy ----------
  s = content("Situación");
  kicker(s, "LO QUE ESTO CUESTA HOY · SEPTIEMBRE 2026");
  title(s, "Problemas que llegan a la rama principal y retrabajo en cada revisión");
  card(s, c3[0], 222, cw, 240, [...num("9", "de 20"), h3("cambios llegaron a la rama principal con problemas señalados", 13), p("20 problemas nuevos detectados por la herramienta, y en sus revisiones no se mencionó.", 11.5, true)]);
  card(s, c3[1], 222, cw, 240, [...num("0", "%"), h3("del código nuevo con pruebas unitarias medidas", 13), p("La revisión automática no ejecuta las pruebas unitarias, así que no se mide qué parte del código nuevo está probada.", 11.5, true)]);
  card(s, c3[2], 222, cw, 240, [...num("46", "%"), h3("de los cambios comentados, por estilo o convenciones", 13), p("12 de 26. Y 7 de 26 (27 %), por errores funcionales que una prueba unitaria detecta antes.", 11.5, true)]);
  card(s, 72, 482, 1136, 96, [h3("Revisión manual de lo que una máquina ya detecta"), p("Cinco tipos de comentario de los revisores los detecta una regla automática. Cada uno es tiempo de revisión y un ciclo más de corrección.", 11.5, true)]);
  source(s, "Fuente: cambios de código (PRs) de Generic API de septiembre de 2026 y sus revisiones en GitHub, consulta del 8 oct 2026. Enlaces a cada uno en el anexo (slide 10).");

  // ---------- 4 · El propósito ----------
  pres.addSection({ title: "Propuesta" });
  s = content("Propuesta");
  kicker(s, "EL PROPÓSITO");
  title(s, "Viva, dueña de cómo se mide la calidad de todos sus proyectos");
  sub(s, "Las reglas de calidad dependen del lenguaje de programación, no del proyecto. Viva las define una vez y se aplican a todos sus proyectos.", 200);
  card(s, 72, 270, 360, 200, [tag("DEFINE VIVA", BLUE), h3("Las reglas de calidad de Viva", 16), p("Un conjunto de reglas por lenguaje y un mismo filtro de calidad, aprobados por Viva.", 11.5, true)], { fill: BLACK, border: BLUE });
  arrow(s, 440, 350);
  card(s, 478, 270, 236, 200, [tag("PRIMERO"), h3("Generic API"), p("Donde se configura y se prueba en este servicio.", 11.5, true)], { border: LV });
  card(s, 726, 270, 236, 200, [h3("Otros proyectos .NET de Viva"), p("Usan las mismas reglas, sin redefinirlas.", 11.5, true)]);
  card(s, 974, 270, 234, 200, [h3("Proyectos en otros lenguajes"), p("Se suman con las reglas de su lenguaje, bajo el mismo criterio.", 11.5, true)]);
  card(s, 72, 492, 1136, 62, [r("Hoy", { fontSize: 12, bold: true, color: BLUE }), r(" las reglas las define y administra un tercero. ", { fontSize: 12 }), r("Con la propuesta", { fontSize: 12, bold: true, color: BLUE }), r(", Viva es la dueña del criterio de calidad de toda su organización.", { fontSize: 12 })], { fill: BLACK, valign: "middle", name: "Franja" });

  // ---------- 5 · Paso 1 ----------
  s = content("Propuesta");
  kicker(s, "LA PROPUESTA · PASO 1");
  title(s, "Una herramienta de calidad de Viva, sin depender de un tercero");
  sub(s, "Viva tiene su propio SonarQube, con acceso para los equipos que Viva decida.", 196, 26);
  const c4 = [72, 360, 648, 936], cw4 = 272;
  [["Propiedad", "El historial de calidad del código de Viva queda en manos de Viva."],
   ["Accesos", "Viva da y quita accesos cuando lo necesita. Los equipos con acceso ven cada problema y dónde está."],
   ["Reglas", "Viva define y ajusta las reglas y el filtro de calidad para todos sus proyectos, sin pedir permiso a nadie."],
   ["Continuidad", "Si cambia un proveedor, el control de calidad y su historial se quedan."]]
    .forEach(([t, x], i) => card(s, c4[i], 240, cw4, 170, [h3(t), p(x, 11.5, true)]));
  card(s, 72, 428, 560, 130, [tag("OPCIÓN A", BLUE), h3("En la nube: SonarQube Cloud"), p("Servicio administrado por SonarSource, bajo una organización de Viva. Sin servidores que mantener.", 11.5, true)], { fill: BLACK });
  card(s, 648, 428, 560, 130, [tag("OPCIÓN B", BLUE), h3("En infraestructura propia"), p("En servidores y dominio de Viva, con una edición que revise cambios de código (Developer o superior). Viva la opera.", 11.5, true)], { fill: BLACK });
  s.addText([r("En ambas partimos de las reglas con las que trabaja hoy el equipo de Generic API. La configuración está ", { fontSize: 11 }), r("incluida en el servicio", { fontSize: 11, bold: true }), r(" (slide 12).", { fontSize: 11 })],
    { x: px(72), y: px(574), w: px(1136), h: px(30), fontFace: FONT, color: WHITE, margin: 0, valign: "top", isTextBox: true, objectName: "Nota" });

  // ---------- 6 · Paso 2 ----------
  s = content("Propuesta");
  kicker(s, "LA PROPUESTA · PASO 2");
  title(s, "Cada cambio se revisa solo antes de que lo vea una persona");
  const fx = [72, 470, 868], fw = 340;
  card(s, fx[0], 226, fw, 236, [...num("1"), h3("El desarrollador sube su cambio", 15), p("Propone su cambio de código para integrarlo a la rama principal.", 12, true)]);
  arrow(s, 422, 316);
  card(s, fx[1], 226, fw, 236, [...num("2"), h3("La revisión automática lo analiza", 15), p("Compila el código, ejecuta las pruebas unitarias, mide qué parte del código nuevo recorren y lo analiza con la herramienta de calidad de Viva.", 12, true)]);
  arrow(s, 820, 316);
  card(s, fx[2], 226, fw, 236, [...num("3"), h3("El resultado queda en el cambio", 15), ...rich("**Si cumple**, pasa a la revisión de una persona. **Si no cumple**, queda bloqueado con el detalle de qué corregir.", 12)], { border: BLUE });
  band(s, 486, 66, "El resultado:", "la máquina revisa lo repetitivo y las personas dedican su tiempo a diseño y negocio.");

  // ---------- 7 · El filtro ----------
  s = content("Propuesta");
  kicker(s, "LA PROPUESTA · EL FILTRO DE CALIDAD");
  title(s, "Un filtro automático que bloquea lo que no cumple");
  const sx = [72, 362, 652, 942], sw = 266;
  [["1", "Compilar", "¿El código compila?", "Si no, el cambio se detiene.", "BLOQUEA", BLUE],
   ["2", "Pruebas unitarias", "¿Pasan todas las pruebas unitarias?", "Una prueba unitaria rota detiene el cambio.", "BLOQUEA", BLUE],
   ["3", "Análisis", "¿Qué problemas nuevos hay?", "El detalle queda en el cambio, con el enlace a cada problema.", "INFORMA", LV],
   ["4", "Filtro de calidad", "¿Cumple el estándar de Viva?", "Si no, el cambio no se puede integrar.", "BLOQUEA", BLUE]]
    .forEach(([n, t, q, x, tg, tc], i) => card(s, sx[i], 226, sw, 210,
      [r(n, { fontSize: 20, bold: true, color: BLUE, breakLine: true, paraSpaceAfter: 6 }), h3(t, 15), r(q + " ", { fontSize: 11.5, bold: true }), r(x, { fontSize: 11.5, breakLine: true, paraSpaceAfter: 10 }), r(tg, { fontSize: 9, bold: true, color: tc, charSpacing: 1 })]));
  card(s, 72, 456, 1136, 104, [
    r("Qué exige el filtro: ", { fontSize: 12.5, bold: true, color: BLUE }),
    r("Pruebas unitarias que recorran al menos el 80 % del código nuevo", { fontSize: 12.5, bold: true }),
    r(" · ningún defecto ni vulnerabilidad nueva · problemas de mantenimiento dentro del límite acordado · poco código duplicado (≤ 3 %).", { fontSize: 12.5, breakLine: true, paraSpaceAfter: 4 }),
    r("Solo se exige al código nuevo de cada cambio: el código existente no frena el trabajo.", { fontSize: 11.5, color: LV })], { fill: BLACK, valign: "middle", name: "Franja" });

  // ---------- 8 · Beneficios ----------
  pres.addSection({ title: "Valor" });
  s = content("Valor");
  kicker(s, "BENEFICIOS");
  title(s, "Menos retrabajo, menos riesgo, más control");
  card(s, c3[0], 190, cw, 250, [h3("Viva Aerobus"), ...bullets(["Ningún cambio llega a la rama principal sin pasar el filtro de calidad.", "Cada cambio nuevo llega con pruebas unitarias que se ejecutan siempre.", "Los problemas dejan de acumularse: se controla lo nuevo sin frenar por lo existente."])]);
  card(s, c3[1], 190, cw, 250, [h3("Revisores"), ...bullets(["Dejan de corregir a mano lo que una máquina detecta.", "Dedican su tiempo a diseño y negocio.", "Un solo criterio de calidad, igual para todos los cambios."])]);
  card(s, c3[2], 190, cw, 250, [h3("Equipo de desarrollo"), ...bullets(["Ve cada problema y dónde está, desde el propio cambio.", "Sabe si su cambio cumple antes de que lo revise una persona.", "Menos devoluciones y menos idas y vueltas por cambio."])]);
  card(s, 72, 458, 1136, 142, [tag("SIN DEPENDENCIA DE TERCEROS", BLUE), h3("De una herramienta de un tercero a una propia", 19),
    ...rich("Viva deja de depender de Ezy para **cambiar reglas o dar accesos**, y sus reglas de calidad, definidas por lenguaje, se aplican a **todos los proyectos de Viva**, no solo a Generic API.", 12.5)], { fill: BLACK, border: BLUE });

  // ---------- 9 · Por qué ahora ----------
  s = content("Valor");
  kicker(s, "POR QUÉ AHORA");
  title(s, "La herramienta ya existe: falta que sea de Viva y que se use");
  sub(s, "SonarQube ya revisa cada cambio de Generic API, pero hoy no es obligatorio atender su resultado. Hacerlo propio y obligatorio convierte ese dato en un control.", 196);
  [["Se apoya en lo que ya existe", "La herramienta de calidad, las pruebas unitarias del proyecto y la revisión automática de GitHub. Se suma al flujo de trabajo actual."],
   ["Un criterio objetivo", "El mismo estándar para todos los cambios y todos los revisores, verificado por una máquina."],
   ["Inversión acotada", "1 mes, llave en mano, y la herramienta queda lista para otros proyectos de Viva."]]
    .forEach(([t, x], i) => card(s, c3[i], 268, cw, 140, [h3(t), p(x, 11.5, true)]));
  card(s, 72, 428, 560, 150, [tag("HOY"), ...num("9", "de 20", WHITE), p("cambios de septiembre llegaron a la rama principal con problemas señalados, sin pruebas unitarias medidas.", 11.5, true)], { fill: BLACK });
  card(s, 648, 428, 560, 150, [tag("CON EL CONTROL", BLUE), ...num("0"), p("cambios llegan a la rama principal sin pasar las pruebas unitarias y el filtro de calidad.", 11.5, true)], { fill: BLACK });

  // ---------- 10 · Anexo ----------
  pres.addSection({ title: "Anexo y cierre" });
  s = content("Anexo y cierre");
  kicker(s, "ANEXO · EVIDENCIA");
  title(s, "Los cambios de código que respaldan estas cifras");
  const links = (nums) => nums.flatMap((n, i) => [r(`#${n}`, { fontSize: 12, bold: true, color: BLUE, hyperlink: { url: GH + n } }), r(i < nums.length - 1 ? "   " : "", { fontSize: 12 })]);
  card(s, 72, 214, 560, 170, [h3("9 de 20 · Llegaron a la rama principal con el filtro en rojo"), ...links(["2421", "2467", "2484", "2487", "2488", "2493", "2506", "2509", "2516"])]);
  card(s, 648, 214, 560, 170, [h3("12 de 26 · Comentarios de estilo o convenciones"), ...links(["2421", "2467", "2478", "2484", "2487", "2488", "2494", "2499", "2504", "2508", "2511", "2516"])]);
  card(s, 72, 400, 560, 170, [h3("7 de 26 · Error funcional o escenario no cubierto"), ...links(["2421", "2491", "2493", "2502", "2504", "2505", "2511"])]);
  const rule = (n, t, last) => [r(`#${n}`, { fontSize: 11, bold: true, color: BLUE, hyperlink: { url: GH + n } }), r(` · ${t}`, { fontSize: 11, breakLine: !last, paraSpaceAfter: 4 })];
  card(s, 648, 400, 560, 170, [h3("Comentarios que detecta una regla automática"),
    ...rule("2387", "capturar Exception (revisión del 6 may) · Sonar S2221"), ...rule("2516", "parámetro sin uso · Sonar S1172"),
    ...rule("2467", "métodos idénticos · Sonar S4144; nombre de campo · .editorconfig"), ...rule("2494", "Array.Empty · analizador .NET CA1825", true)]);
  source(s, "PRs de Generic API de septiembre de 2026 en GitHub (EzyWebwerkstaden/VivaAerobus.Generic.Api), consulta del 8 oct 2026. Ningún revisor menciona Sonar en las revisiones ni en los comentarios de los 28 PRs del periodo. Un PR puede estar en varios grupos.");

  // ---------- 11 · Precondiciones ----------
  s = content("Anexo y cierre");
  kicker(s, "PRECONDICIONES");
  title(s, "Lo que necesitamos para empezar");
  card(s, 72, 160, 1136, 56, [r("Decisión de Viva:", { fontSize: 12.5, bold: true, color: BLUE }), r(" dónde vive su herramienta de calidad, ", { fontSize: 12.5 }), r("en la nube (SonarQube Cloud)", { fontSize: 12.5, bold: true }), r(" o ", { fontSize: 12.5 }), r("en infraestructura propia", { fontSize: 12.5, bold: true }), r(" (slide 5).", { fontSize: 12.5 })], { fill: BLACK, valign: "middle", name: "Franja" });
  card(s, c3[0], 232, cw, 356, [tag("SONAR"), h3("Punto de partida y destino"), ...bullets([
    "Acceso al SonarQube de Ezy (sonarqube.ezyflight.se) para descargar el perfil de reglas y el Quality Gate con los que trabaja hoy el equipo de Generic API: son el punto de partida.",
    "Según la decisión: la organización de Viva en SonarQube Cloud, o el servidor, el dominio y la licencia (Developer o superior) del Sonar propio.",
    "Un usuario administrador en el Sonar de Viva para configurar reglas, Quality Gate y el token del pipeline."], 11)]);
  card(s, c3[1], 232, cw, 356, [tag("REPOSITORIO Y PIPELINE"), h3("GitHub"), ...bullets([
    "Permisos de administración en el repositorio para crear workflows de GitHub Actions y sus secretos.",
    "Permiso para hacer obligatorios los checks del ruleset de master.",
    "Runner ubuntu-latest para el job de calidad (hoy usa windows-latest, que no ejecuta contenedores Linux)."], 11)]);
  card(s, c3[2], 232, cw, 356, [tag("EQUIPO Y PROCESO"), h3("Acuerdos"), ...bullets([
    "Permiso para corregir los hallazgos de Sonar y escribir pruebas unitarias dentro de cada task.",
    "Acuerdo de Viva y Ezy: un cambio que no pasa el filtro de calidad no se integra, y quién puede autorizar una excepción.",
    "Un responsable de Viva, dueño de las reglas de calidad y del filtro para todos sus proyectos."], 11)]);

  // ---------- 12 · Inversión ----------
  s = content("Anexo y cierre");
  kicker(s, "LA INVERSIÓN · SERVICIO LLAVE EN MANO");
  title(s, "1 mes, llave en mano");
  card(s, 72, 160, 560, 136, [tag("TIEMPO APROXIMADO DE IMPLEMENTACIÓN", BLUE), ...num("1", "mes", WHITE), p("Desde que se cumplen las precondiciones de la slide 11.", 11.5, true)], { fill: BLACK });
  card(s, 648, 160, 560, 136, [tag("COSTO", BLUE), ...num("xxx", "", WHITE), p("Incluye los cinco entregables, aplicados a Generic API.", 11.5, true)], { fill: BLACK });
  const dx = [72, 302, 532, 762, 992], dw = 216;
  [["Herramienta de calidad de Viva", "SonarQube de Viva, en la nube o propio, con las reglas y el filtro de calidad (cobertura ≥ 80 % del código nuevo) configurados."],
   ["Imagen Docker de calidad", "El paquete con las herramientas que usa la revisión automática."],
   ["Revisión automática de cada cambio", "Compila, ejecuta las pruebas unitarias y analiza cada cambio de Generic API con la herramienta de Viva."],
   ["Bloqueo automático", "En Generic API, un cambio que no pasa las pruebas unitarias o el filtro de calidad no se puede integrar."],
   ["Lineamiento de pruebas unitarias", "Cómo escribir pruebas unitarias que comprueben resultados."]]
    .forEach(([t, x], i) => card(s, dx[i], 312, dw, 250, [r(String(i + 1), { fontSize: 22, bold: true, color: BLUE, breakLine: true, paraSpaceAfter: 4 }), h3(t, 13), p(x, 11, true)], { name: `Entregable ${i + 1}` }));
  s.addText([r("Alcance:", { fontSize: 11.5, bold: true }), r(" el servicio se aplica a ", { fontSize: 11.5 }), r("Generic API", { fontSize: 11.5, bold: true }), r(". Sumar otros proyectos de Viva a las mismas reglas se cotiza aparte.", { fontSize: 11.5 })],
    { x: px(72), y: px(578), w: px(1136), h: px(26), fontFace: FONT, color: WHITE, margin: 0, isTextBox: true, objectName: "Alcance" });

  // ---------- Interna ----------
  if (withInternal) {
    pres.addSection({ title: "Uso interno" });
    s = content("Uso interno");
    s.addText("USO INTERNO DE TECH AND SOLVE · NO MOSTRAR AL CLIENTE", { x: px(72), y: px(20), w: px(560), h: px(28), fontFace: FONT, fontSize: 10, bold: true, color: WHITE, fill: { color: BLACK }, line: { color: WHITE, width: 1 }, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Marca interna" });
    kicker(s, "EQUIPO DE TRABAJO");
    title(s, "Un ingeniero DevOps a tiempo completo durante 1 mes");
    card(s, 72, 220, 360, 300, [tag("EQUIPO", BLUE), ...num("1", "ingeniero DevOps", WHITE), p("Dedicación: tiempo completo."), p("Duración: 1 mes, desde que se cumplen las precondiciones.", 11.5, true)], { fill: BLACK });
    card(s, 452, 220, 756, 300, [tag("RESPONSABLE DE LOS CINCO ENTREGABLES"), ...bullets([
      "Sonar de Viva: instalar o configurar la instancia, migrar el perfil de reglas desde el Sonar de Ezy y crear el Quality Gate con cobertura ≥ 80 % del código nuevo.",
      "Imagen Docker: construirla, versionarla y publicarla en el registro del repositorio.",
      "Pipeline: configurar GitHub Actions con compilación, pruebas unitarias, cobertura y análisis apuntando al Sonar de Viva.",
      "Bloqueo automático: hacer obligatorios los checks en el ruleset de master y verificar que un PR en rojo no se pueda mergear.",
      "Lineamiento de pruebas unitarias: redactarlo con ejemplos sobre Generic API y la checklist del revisor."], 11.5)]);
  }

  return pres.writeFile({ fileName: path.join(OUT, fileName) }).then(async (f) => { await applyTheme(f, THEME); return f; });
}

(async () => {
  console.log(await build(false, "propuesta-mejora-proceso-calidad-editable.pptx"));
  console.log(await build(true, "propuesta-mejora-proceso-calidad-interno-editable.pptx"));
})();
