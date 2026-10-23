// Generador del .pptx de la presentación del equipo para SURA.
// El HTML de la carpeta de arriba es la fuente de verdad: todo cambio se hace allá primero
// y luego se refleja aquí. Uso: ver README.md.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
// Imágenes de marca y fotos del equipo, ya recortadas (ver README.md).
const ASSETS = path.join(__dirname, "assets");
// El .pptx se escribe junto al HTML, en la carpeta de arriba.
const OUT = path.join(__dirname, "..", "Tech and Solve - Dinámica de trabajo del equipo-v3.pptx");
const LOGO = "image/jpeg;base64," + fs.readFileSync(path.join(ASSETS, "logo.jpeg")).toString("base64");

const THEME = {
  name: "Tech and Solve",
  headFontFace: "Poppins",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1A1E27", lt1: "FFFFFF", dk2: "280265", lt2: "EBEBFF",
    accent1: "5300DF", accent2: "B9720A", accent3: "1B6B4F", accent4: "FAF9FE",
    accent5: "DCD8EC", accent6: "5B5A66", hlink: "5300DF", folHlink: "280265",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Dinámica de trabajo del equipo";
pres.author = "Tech and Solve";
pres.company = "Tech and Solve";
const C = pres.SchemeColor;
const BORDER = "DCD8EC";
const M = 0.6;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITULO",
  background: { color: "FFFFFF" },
  objects: [],
  slideNumber: undefined,
});
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: "FFFFFF" },
  objects: [
    { image: { data: LOGO, x: M, y: 6.98, w: 0.66, h: 0.346 } },
    { text: { text: "Dinámica de trabajo del equipo · MVP de gestores · SURA", options: { x: 1.4, y: 6.98, w: 8, h: 0.35, fontSize: 11, color: C.accent6, valign: "middle", margin: 0 } } },
    {
      placeholder: {
        options: { name: "title", type: "title", x: M, y: 0.45, w: 12.1, h: 1.05, fontSize: 28, bold: true, color: C.text2, valign: "top", align: "left", margin: 0 },
        text: "",
      },
    },
  ],
  slideNumber: { x: 12.1, y: 6.98, w: 0.63, h: 0.35, fontSize: 11, color: C.accent6, align: "right" },
});

// ---------- helpers ----------
function T(slide, text, x, y, w, h, o = {}) {
  slide.addText(text, Object.assign({ x, y, w, h, isTextBox: true, margin: 0, valign: "top", fontSize: 14, color: C.text1 }, o));
}
function card(slide, x, y, w, h, o = {}) {
  slide.addShape(pres.ShapeType.roundRect, Object.assign({ x, y, w, h, rectRadius: 0.08, fill: { color: C.accent4 }, line: { color: BORDER, width: 1 } }, o));
}
function dot(slide, x, y, d, label, o = {}) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: o.fill || C.accent1 }, line: { color: o.fill || C.accent1, width: 0 } });
  T(slide, label, x, y, d, d, { align: "center", valign: "middle", bold: true, color: C.background1, fontSize: o.fontSize || 14 });
}
const tagPill = (s, x, y, w, text, col) => {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.22, rectRadius: 0.11, fill: { color: col }, line: { color: col, width: 0 } });
  s.addText(text, { x, y, w, h: 0.22, align: "center", valign: "middle", fontSize: 8.5, bold: true, color: C.background1, margin: 0, isTextBox: true });
};
const link = (text, url) => ({ text, options: { hyperlink: { url }, color: C.accent1, underline: { style: "sng" } } });
const H = (slide, text) => slide.addText(text, { placeholder: "title" });
function newSlide(section, title, notes) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: section });
  H(s, title);
  if (notes) s.addNotes(notes);
  return s;
}

const IMG = (n) => "image/jpeg;base64," + fs.readFileSync(path.join(ASSETS, "p_" + n + ".jpg")).toString("base64");
// ===== Generador alineado con el HTML vigente de v3 (20 láminas, Tech and Solve Spec Flow) =====
const SEC1 = "Equipo", SECSF = "Tech and Solve Spec Flow", SEC4 = "Cierre";
const tblBase = (o) => Object.assign({ border: { type: "solid", pt: 1, color: BORDER }, fill: { color: C.accent4 }, valign: "middle" }, o);
const th = (t, fill, o = {}) => ({ text: t, options: Object.assign({ bold: true, color: C.background1, fill: { color: fill || C.text2 }, valign: "middle" }, o) });
const violetSlide = (section) => {
  const s = pres.addSlide({ masterName: "TITULO", sectionTitle: section });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  return s;
};
const logoBox = (s, x, y) => {
  s.addShape(pres.ShapeType.roundRect, { x, y, w: 1.9, h: 1.0, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: C.background1, width: 0 } });
  s.addImage({ data: LOGO, x: x + 0.12, y: y + 0.08, w: 1.66, h: 0.87 });
};
// Banda violeta clara con un inicio en negrita
const band = (s, x, y, w, h, lead, rest, fs = 12) => {
  card(s, x, y, w, h, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: lead, options: { bold: true, color: C.text2 } }, { text: rest }], x + 0.22, y, w - 0.44, h, { fontSize: fs, valign: "middle" });
};
const bullets = (items, gap = 5) => items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1, paraSpaceAfter: gap } }));
const boldBullets = (items, gap = 5) => {
  const out = [];
  items.forEach(([a, b], k) => {
    out.push({ text: a, options: { bold: true, bullet: true } });
    out.push({ text: b, options: { breakLine: k < items.length - 1, paraSpaceAfter: gap } });
  });
  return out;
};

// Tarjeta de persona: mismo diseño en todas las láminas (foto o inicial en círculo con aro blanco, nombre y cargo)
const personCard = (s, x, y, w, h, o) => {
  if (!o.light) s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.12, fill: { color: "3A1878" }, line: { color: "5B3D96", width: 0.75 } });
  const d = o.d || 0.9, px = x + (o.light ? 0 : 0.18), py = y + (h - d) / 2;
  s.addShape(pres.ShapeType.ellipse, { x: px, y: py, w: d, h: d, fill: { color: C.background1 }, line: { color: o.light ? BORDER : C.background1, width: o.light ? 1 : 0 } });
  if (o.img) s.addImage({ data: o.img, x: px + 0.03, y: py + 0.03, w: d - 0.06, h: d - 0.06, rounding: true, altText: o.name });
  else T(s, o.initial, px, py, d, d, { align: "center", valign: "middle", bold: true, fontSize: 16, color: C.text2 });
  if (o.name) T(s, [{ text: o.name, options: { bold: true, fontSize: o.nfs || 13, breakLine: true } }, { text: o.role, options: { fontSize: o.rfs || 10.5, color: C.background2 } }], px + d + 0.15, y + 0.06, w - (px - x) - d - 0.27, h - 0.12, { valign: "middle", color: C.background1 });
};

// ================= 1 · portada de la propuesta =================
pres.addSection({ title: "Portada" });
{
  const s = violetSlide("Portada");
  logoBox(s, 0.8, 0.7);
  T(s, "MÉTODO DE TRABAJO DE TECH AND SOLVE PARA SURA", 0.8, 2.45, 8, 0.35, { fontSize: 13, bold: true, color: C.background2, charSpacing: 3 });
  s.addText("MVP de Gestores:\ninnovación para SURA", { x: 0.8, y: 2.85, w: 11.5, h: 1.75, fontSize: 44, bold: true, color: C.background1, fontFace: "+mj-lt", valign: "top", margin: 0, isTextBox: true });
  T(s, "Un equipo multidisciplinario dedicado al éxito de SURA,\ncon IA generativa propia que acelera resultados medibles", 0.8, 4.85, 11.5, 0.9, { fontSize: 20, bold: true, color: C.background1 });
  s.addShape(pres.ShapeType.line, { x: 0.8, y: 6.2, w: 11.73, h: 0, line: { color: C.background2, width: 0.75, transparency: 60 } });
  T(s, "SURA Colombia · Transformación prestación y reclamaciones\nMVP de autorizaciones de salud", 0.8, 6.32, 6.5, 0.6, { fontSize: 11, color: C.background2 });
  T(s, "Tech and Solve · Octubre de 2026\nDocumento confidencial", 7.3, 6.32, 5.23, 0.6, { fontSize: 11, color: C.background2, align: "right" });
  s.addNotes("Portada de la propuesta: qué equipo proponemos, cómo trabajaría con SURA y qué lo diferencia. Trabajamos con Tech and Solve Spec Flow, nuestro método de entrega continua guiada por especificaciones con IA: un equipo pequeño dirige a los agentes de IA, SURA define y certifica cada capacidad, y después del primer release las capacidades se liberan de forma continua.");
}

// ================= 2 · equipo Tech and Solve (oculta) =================
pres.addSection({ title: SEC1 });
{
  const s = pres.addSlide({ masterName: "TITULO", sectionTitle: SEC1 });
  s.hidden = true; // oculta en la presentación, como la dejó el equipo tech
  s.addShape(pres.ShapeType.rect, { x: 8.6, y: 0, w: 4.733, h: 7.5, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  s.addImage({ data: LOGO, x: 0.8, y: 0.7, w: 1.9, h: 0.995 });
  s.addText("Equipo Tech and Solve", { x: 0.8, y: 2.1, w: 7.4, h: 1.2, fontSize: 40, bold: true, color: C.text2, fontFace: "+mj-lt", valign: "top", margin: 0, isTextBox: true });
  T(s, "Un equipo ágil y experto que garantiza resultados medibles en el MVP:", 0.8, 3.3, 7.4, 0.85, { fontSize: 17, bold: true, color: C.text2 });
  T(s, "Dos desarrolladores construyen los sistemas agénticos del MVP de gestores, con un arquitecto que define el cómo y lo revisa, en flujo continuo, y con el respaldo de un equipo directivo que apoya de forma transversal el éxito de la implementación.", 0.8, 4.2, 7.4, 1.95, { fontSize: 16, color: C.accent6 });
  T(s, "Tech and Solve · SURA, MVP de gestores de autorizaciones de salud\nOctubre de 2026 · Sugerencia de trabajo, debatible y ajustable", 0.8, 6.3, 7.4, 0.7, { fontSize: 13, color: C.accent6 });
  const team = [
    { img: IMG("raul"), name: "Raúl A. De Villa C.", role: "Co-Founder · Acompaña los hitos clave con una mirada crítica de negocio y de solución.", h: 0.86 },
    { img: IMG("alexandra"), name: "Alexandra Acosta", role: "Gerente de Éxito del Cliente · Pone al servicio de SURA la experiencia y los estándares de toda la compañía.", h: 0.86 },
    { img: IMG("jorge"), name: "Jorge Andrés Gómez Velásquez", role: "Líder del Éxito del Cliente · Punto de contacto con SURA: lo acordado, con calidad y a tiempo.", h: 0.86 },
    { img: IMG("didier"), name: "Didier Fabián Franco Gómez", role: "Arquitecto Líder. Marca el rumbo técnico con el equipo, lo alinea con la arquitectura de SURA y asegura que cada capacidad lo cumpla.", h: 1.0 },
    { img: IMG("juan"), name: "Juan Gabriel Colorado", role: "Desarrollador IA · Construye los sistemas agénticos desde un backlog compartido", h: 0.76 },
    { img: IMG("gian"), name: "Gian Valdiris", role: "Desarrollador IA · Construye los sistemas agénticos desde un backlog compartido", h: 0.76 },
    { initial: "S", name: "Soporte", role: "Media jornada · Opera el pipeline y el monitoreo, y atiende lo que ya opera", h: 0.76 },
  ];
  let ty = 0.55;
  team.forEach((o) => { personCard(s, 8.95, ty, 3.95, o.h, Object.assign({ d: 0.62, nfs: 11.5, rfs: 9.5 }, o)); ty += o.h + 0.1; });
  s.addNotes("El equipo construye los sistemas agénticos; el front y la integración los lideran los equipos de SURA. Trabaja con Tech and Solve Spec Flow: SURA define y certifica cada capacidad, y las capacidades certificadas se liberan de forma continua. Todo lo que sigue es una sugerencia de trabajo.");
}

// ================= 3 · roles =================
{
  const s = newSlide(SEC1, "Equipo de trabajo propuesto: modelo Tech and Solve y SURA",
    "El liderazgo de Tech and Solve acompaña de forma puntual: Raúl en los hitos clave, con una mirada crítica de negocio y de solución; Alexandra, con la experiencia y los estándares de toda la compañía; y Jorge, como punto de contacto con SURA para que cada entrega cumpla lo acordado. El arquitecto define el cómo, se alinea con el equipo de arquitectura de SURA y revisa. Los builders, que son los desarrolladores IA, refinan, dimensionan y luego implementan dirigiendo a la IA. Trabajan sobre el mismo backlog y cada uno toma la siguiente capacidad priorizada; no hay frentes repartidos. Tech and Solve Spec Flow pide que la verificación y la liberación sean responsabilidades explícitas: la verificación la asumen los builders con apoyo de la IA, y la liberación la opera el soporte de media jornada, que además atiende lo que ya opera para que el flujo de nuevas capacidades no se interrumpa. Del lado de SURA están los dos roles de Tech and Solve Spec Flow, el líder funcional y el arquitecto técnico de negocio, con el apoyo de usuarios clave, negocio y equipo médico. Además dependemos de los equipos de front, integración, core y plataformas, cuyas piezas reemplazamos por simuladores mientras llegan.");
  const lw = 7.9;
  card(s, M, 1.6, lw, 1.42, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "LIDERAZGO QUE ACOMPAÑA", M + 0.25, 1.68, lw - 0.5, 0.25, { fontSize: 9.5, bold: true, color: C.text2, charSpacing: 1 });
  const mw = (lw - 0.5 - 0.3) / 3;
  [["raul", "Raúl A. De Villa C.", "Co-Founder", "Acompaña los hitos clave con una mirada crítica de negocio y de solución."], ["alexandra", "Alexandra Acosta", "Gerente de Éxito del Cliente", "Pone al servicio de SURA la experiencia y los estándares de toda la compañía."], ["jorge", "Jorge Andrés Gómez Velásquez", "Líder del Éxito del Cliente", "Punto de contacto con SURA: lo acordado, con calidad y a tiempo."]].forEach(([k, n, r, d], i) => {
    const x = M + 0.25 + i * (mw + 0.15), y = 1.97;
    personCard(s, x, y, 0.5, 0.5, { light: true, img: IMG(k), name: "", d: 0.48 });
    T(s, [{ text: n, options: { bold: true, color: C.text2, fontSize: 10, breakLine: true } }, { text: r, options: { bold: true, color: C.accent2, fontSize: 8.5 } }], x + 0.58, y - 0.02, mw - 0.58, 0.54, { valign: "middle" });
    T(s, d, x, y + 0.55, mw, 0.45, { fontSize: 9.5 });
  });
  card(s, M, 3.1, lw, 0.9);
  personCard(s, M + 0.2, 3.18, 0.72, 0.72, { light: true, img: IMG("didier"), name: "", d: 0.72 });
  T(s, [{ text: "Didier Fabián Franco Gómez", options: { bold: true, color: C.text2, fontSize: 13 } }, { text: "  · Arquitecto Líder", options: { bold: true, color: C.accent2, fontSize: 11 } }], M + 1.08, 3.15, lw - 1.25, 0.3, {});
  T(s, "Marca el rumbo técnico: define con el equipo prácticas, arquetipos y componentes, los alinea con la arquitectura de SURA, cuida el harness que guía a la IA y asegura que cada capacidad los cumpla.", M + 1.08, 3.45, lw - 1.25, 0.5, { fontSize: 10.5 });
  card(s, M, 4.08, lw, 2.05);
  T(s, [{ text: "Builders", options: { bold: true, color: C.text2, fontSize: 15, breakLine: true } }, { text: "Dedicación completa", options: { bold: true, color: C.accent2, fontSize: 9 } }], M + 0.22, 4.14, 1.7, 0.55, { valign: "middle" });
  [["juan", "Juan Gabriel Colorado"], ["gian", "Gian Valdiris"]].forEach(([k, n], i) => {
    const x = M + 2.1 + i * 2.75, y = 4.15;
    personCard(s, x, y, 0.5, 0.5, { light: true, img: IMG(k), name: "", d: 0.48 });
    T(s, [{ text: n, options: { bold: true, color: C.text2, fontSize: 10, breakLine: true } }, { text: "Desarrollador IA", options: { bold: true, color: C.accent2, fontSize: 8.5 } }], x + 0.56, y - 0.02, 2.1, 0.54, { valign: "middle" });
  });
  const sw = (lw - 0.44 - 0.24) / 3;
  [["1 · Refinan", "Bajan cada capacidad a especificación y diseño técnico con el arquetipo, junto al arquitecto."], ["2 · Dimensionan", "Definen si cada capacidad es acotada o amplia, y parten la amplia."], ["3 · Implementan", "Dirigen a la IA con las prácticas del equipo, revisan, integran y la entregan a certificación."]].forEach(([t, b], i) => {
    const x = M + 0.22 + i * (sw + 0.12);
    card(s, x, 4.75, sw, 0.82, { fill: { color: C.background1 } });
    T(s, [{ text: t, options: { bold: true, color: C.accent1, breakLine: true } }, { text: b }], x + 0.1, 4.78, sw - 0.2, 0.77, { fontSize: 9.5 });
  });
  T(s, [{ text: "Un equipo, un backlog: ", options: { bold: true, color: C.text2 } }, { text: "siempre se trabaja en la prioridad más alta de SURA, y el conocimiento queda en el equipo. Los builders también verifican: con IA convierten los ejemplos de SURA en pruebas y evalúan a los agentes." }], M + 0.22, 5.6, lw - 0.44, 0.5, { fontSize: 9.5, color: C.accent6, valign: "middle" });
  card(s, M, 6.2, lw, 0.62);
  dot(s, M + 0.2, 6.31, 0.4, "S", { fontSize: 12, fill: C.accent2 });
  T(s, [{ text: "Soporte", options: { bold: true, color: C.text2, fontSize: 12 } }, { text: "  · media jornada · operador de liberación", options: { bold: true, color: C.accent2, fontSize: 10, breakLine: true } }, { text: "Opera pipeline, banderas, monitoreo e incidentes, y atiende lo que ya opera sin frenar el flujo.", options: { fontSize: 10 } }], M + 0.75, 6.2, lw - 0.95, 0.62, { valign: "middle" });
  const x0 = 8.9, wr = 3.83;
  T(s, "Equipo SURA", x0, 1.55, wr, 0.38, { fontSize: 17, bold: true, color: C.text2 });
  const lab = (t, y, col) => T(s, t, x0, y, wr, 0.22, { fontSize: 8.5, bold: true, color: col, charSpacing: 1 });
  const sc = (t, r, d, y, h, tint) => {
    card(s, x0, y, wr, h, tint ? { fill: { color: "E8F1ED" }, line: { color: C.accent3, width: 1 } } : { fill: { color: C.background1 } });
    T(s, [{ text: t, options: { bold: true, color: C.text2 } }].concat(r ? [{ text: "  · " + r, options: { bold: true, color: C.accent3, fontSize: 8.5 } }] : []).concat([{ text: "", options: { breakLine: true } }, { text: d, options: { color: C.accent6 } }]), x0 + 0.15, y, wr - 0.3, h, { fontSize: 10, valign: "middle" });
  };
  lab("ROLES EN TECH AND SOLVE SPEC FLOW", 1.98, C.accent3);
  sc("Líder funcional", "Product Owner", "Prioriza el backlog, aporta ejemplos con datos en la mesa de definición y certifica cada capacidad.", 2.24, 0.86, true);
  sc("Arquitecto técnico de negocio", "arquitectura de SURA", "Acuerda lineamientos con nuestro arquitecto líder; aporta reglas, integraciones, seguridad y cumplimiento, y acceso a ambientes y datos.", 3.17, 1.0, true);
  sc("Usuarios clave, negocio y equipo médico", "", "Apoyan la certificación, definen el error tolerable y validan la muestra clínica.", 4.24, 0.78, false);
  lab("EQUIPOS DE LOS QUE DEPENDEMOS", 5.12, C.accent6);
  sc("Front, integración y core SuraHis", "", "Construyen la base donde se integran los agentes; mientras llega, trabajamos contra simuladores.", 5.38, 0.72, false);
  sc("Plataformas habilitadora y agéntica", "", "Exponen gateways, modelos y herramientas autorizadas por SURA.", 6.17, 0.65, false);
}

// ================= 4 · alcance =================
{
  const s = newSlide(SEC1, "Construimos los sistemas agénticos; el front y la integración los lideran los equipos de SURA",
    "El equipo construye los agentes, lo que los gobierna y la base de la torre de control. Además, construye y mantiene los simuladores de cada gestor, para que el ritmo del equipo no dependa de que el front, la API orquestadora o SuraHis lleguen a tiempo. Los simuladores respetan el contrato acordado en el arranque y se reemplazan por las piezas reales cuando SURA las libera.");
  const w = 5.95;
  card(s, M, 1.65, w, 4.95, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Lo construye y mantiene este equipo", M + 0.3, 1.8, w - 1.5, 0.4, { fontSize: 16, bold: true, color: C.text2 });
  tagPill(s, M + w - 1.15, 1.89, 0.8, "Tech", C.accent1);
  const blocks = [["Los agentes", "Clasificador, enrutador, extractores, request builder, LLM-as-a-judge, pertinencia médica, duplicidad, concepto al escalar y auditor."], ["Lo que los gobierna", "Golden set, compuerta, traza de la decisión, umbrales, calibración del juez y techos de autonomía."], ["La base de la torre de control", "Contrato de eventos y torre de control, capas 1 y 2."], ["Los simuladores de cada gestor", "Del front, de la API orquestadora y de SuraHis, sobre el contrato acordado, para construir y verificar sin esperar a que lleguen."]];
  const runs = [];
  blocks.forEach(([a, b], k) => {
    runs.push({ text: a, options: { bold: true, color: C.accent1, breakLine: true } });
    runs.push({ text: b, options: { breakLine: k < blocks.length - 1, paraSpaceAfter: 8 } });
  });
  T(s, runs, M + 0.3, 2.3, w - 0.6, 4.2, { fontSize: 12.5 });
  const x2 = M + w + 0.2;
  card(s, x2, 1.65, w, 4.95);
  T(s, "Lo lideran los equipos de SURA", x2 + 0.3, 1.8, w - 1.5, 0.4, { fontSize: 16, bold: true, color: C.accent6 });
  tagPill(s, x2 + w - 1.15, 1.89, 0.8, "SURA", C.accent3);
  T(s, bullets(["Front Angular y canales", "API orquestadora de cada gestor e integración con el core SuraHis", "Plataforma habilitadora y plataforma agéntica"], 8), x2 + 0.3, 2.35, w - 0.6, 1.7, { fontSize: 14 });
  band(s, x2 + 0.3, 4.2, w - 0.6, 2.2, "El contrato manda. ", "El contrato entre cada agente y su gestor se acuerda en el arranque. Los simuladores lo respetan; cuando llega la pieza real de SURA, se cambia el simulador por ella y el golden set confirma que nada se rompe.", 13);
}

// ================= 5 · sección Tech and Solve Spec Flow =================
pres.addSection({ title: SECSF });
{
  const s = violetSlide(SECSF);
  logoBox(s, 0.9, 1.95);
  s.addText("Tech and Solve Spec Flow", { x: 0.9, y: 3.25, w: 11.5, h: 1.0, fontSize: 46, bold: true, color: C.background1, fontFace: "+mj-lt", valign: "top", margin: 0, isTextBox: true });
  s.addNotes("Tech and Solve Spec Flow es nuestro método de entrega continua guiada por especificaciones con IA. Organiza la implementación con generación de código por IA sobre una arquitectura ya definida y aprobada: un equipo pequeño dirige a los agentes de IA, SURA define y certifica cada capacidad, y después del primer release las capacidades se liberan de forma continua. Ya opera en proyectos de clientes. Usa la IA propia de Tech and Solve, exclusiva de su equipo, sobre modelos de primer nivel de Anthropic y siempre con autorización de SURA.");
}

// Tabla con encabezado violeta y primera columna en negrita
const sfTable = (s, headers, rows, o) => {
  const c = (t, extra = {}) => ({ text: t, options: Object.assign({ fontSize: o.fs }, extra) });
  const body = rows.map((r) => r.map((t, k) => (typeof t === "object" ? t : c(t, k === 0 ? { bold: true, color: C.text2 } : {}))));
  s.addTable([headers.map((h) => th(h, C.text2, { fontSize: o.fs }))].concat(body), tblBase({ x: o.x ?? M, y: o.y, w: o.w ?? 12.1, colW: o.colW, rowH: o.rowH, fontSize: o.fs }));
};
// ================= 6 · principios =================
{
  const s = newSlide(SECSF, "Principios: seis reglas que guían cada capacidad",
    "Los seis principios de Tech and Solve Spec Flow. La IA está en el centro del método: escribe el código, y el trabajo de las personas es especificar, revisar y certificar. El sexto principio deja claro que no partimos de cero: la arquitectura de gestores ya definida con SURA es el marco.");
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 1.6, w: 3.45, h: 5.15, rectRadius: 0.1, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, "Las personas definen y revisan.\nLa IA escribe el código.", M + 0.3, 2.2, 2.85, 1.6, { fontSize: 20, bold: true, color: C.background1, fontFace: "+mj-lt" });
  T(s, "Un equipo pequeño dirige a los agentes de IA, SURA define y certifica cada capacidad, y después del primer release las capacidades se liberan de forma continua.", M + 0.3, 4.0, 2.85, 2.2, { fontSize: 13, color: C.background2 });
  const items = [
    ["La especificación es el producto principal del equipo humano", "La IA escribe código. Las personas definen qué debe hacer, con qué datos y cómo se comprueba, y la especificación resultante es la fuente de verdad del sistema."],
    ["Primero los ejemplos, después el código", "Los datos de prueba y los criterios de certificación de SURA se convierten en pruebas automatizadas antes de generar código."],
    ["Revisión humana obligatoria", "Ningún código generado llega a producción sin revisión de un builder y, cuando afecta a la arquitectura, del arquitecto líder."],
    ["Flujo continuo", "Cada capacidad avanza a su ritmo y se libera cuando está certificada."],
    ["SURA forma parte del equipo", "Su tiempo de respuesta es parte del flujo y se mide igual que el del equipo."],
    ["La arquitectura definida es el marco", "Partimos de la arquitectura de gestores ya trabajada con SURA y la hacemos evolucionar. Cualquier desviación es una decisión explícita del arquitecto líder con el arquitecto de negocio de SURA."],
  ];
  const gx = M + 3.65, cw = (12.1 - 3.65 - 0.18) / 2, ch = (5.15 - 2 * 0.15) / 3;
  items.forEach(([t, b], i) => {
    const x = gx + (i % 2) * (cw + 0.18), y = 1.6 + Math.floor(i / 2) * (ch + 0.15);
    card(s, x, y, cw, ch);
    s.addShape(pres.ShapeType.rect, { x: x, y: y + 0.12, w: 0.06, h: ch - 0.24, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 } });
    T(s, "0" + (i + 1), x + 0.2, y, 0.75, ch, { fontSize: 28, bold: true, color: "C9BEF5", valign: "middle" });
    T(s, [{ text: t, options: { bold: true, color: C.text2, fontSize: 12.5, breakLine: true } }, { text: b, options: { fontSize: 10.5 } }], x + 0.95, y + 0.08, cw - 1.1, ch - 0.16, { valign: "middle" });
  });
}

// ================= 7 · conceptos =================
{
  const s = newSlide(SECSF, "Conceptos: el vocabulario común del método",
    "El vocabulario de Tech and Solve Spec Flow, con los términos propios del MVP de gestores. La capacidad es la unidad de trabajo y se agrupa en metas funcionales con su talla. La ficha es lo que SURA define; la especificación es lo que el agente genera y el equipo revisa. El harness es lo que rodea al modelo para que el código salga bien. El golden set y la compuerta protegen a cada agente, y los simuladores evitan esperar a las piezas de SURA. En el ejemplo, la homologación de códigos se diseña para convivir con CIE-10 y CIE-11, porque Colombia está en transición.");
  sfTable(s, ["Concepto", "Definición"], [
    ["Capacidad", "Unidad de valor que se puede construir, certificar y liberar por sí sola"],
    ["Meta funcional", "Agrupa capacidades y conserva su talla S, M, L o XL para ordenar el backlog. Ejemplo: pertinencia médica (XL) se parte en capacidades como la homologación de CUPS y CIE-10, lista para CIE-11"],
    ["Backlog", "Lista de capacidades priorizada por el líder funcional de SURA"],
    ["Ficha de capacidad", "Ficha de una sola pantalla que acompaña a cada capacidad: para qué, ejemplos con datos, reglas no obvias y cómo se certifica"],
    ["Especificación", "Traducción técnica de la ficha en requisitos verificables, generada por el agente y revisada por el equipo. Vive en el repositorio y es la fuente de verdad del comportamiento"],
    ["Talla", "Acotada (cabe en una ficha y se construye en no más de tres días) o amplia (se parte antes de construirse). No se estima esfuerzo; se mide el tiempo de ciclo real"],
    ["Contexto del agente", "Archivos que guían a la IA: arquitectura, convenciones de código, estructura del repositorio, patrones aprobados y registros de decisiones técnicas"],
    ["Harness", "Lo que rodea al modelo para que el código salga bien: contexto del agente, plantillas, reglas desde revisiones reales, puntos de aprobación, pruebas primero y agentes auditores"],
    ["Golden set y compuerta", "Casos con respuesta conocida que prueban cada agente. Ningún agente se promueve si su golden set muestra regresión"],
    ["Simulador", "Réplica del front, la API orquestadora o SuraHis sobre el contrato acordado. La construye y mantiene Tech and Solve para no esperar a que lleguen las piezas reales"],
    ["Liberada y estable", "Una capacidad está terminada cuando está en producción y superó el periodo de observación sin incidentes"],
  ], { y: 1.45, colW: [2.3, 9.8], rowH: [0.3].concat(Array(11).fill(0.42)), fs: 9.5 });
  T(s, [
    { text: "CIE-10 y CIE-11: ", options: { bold: true } }, { text: "clasificación internacional de enfermedades. Colombia adoptó la CIE-11 con la " },
    link("Resolución 1442 de 2024", "https://normograma.supersalud.gov.co/compilacion/docs/resolucion_minsaludps_1442_2024.htm"), { text: "; la " },
    link("Resolución 1657 de 2025", "https://normograma.supersalud.gov.co/compilacion/docs/resolucion_minsaludps_1657_2025.htm"),
    { text: " da hasta 36 meses de transición, con la CIE-10 vigente y codificación dual para quien migra. " },
    { text: "CUPS: ", options: { bold: true } }, { text: "clasificación colombiana de procedimientos en salud, hoy la de la " },
    link("Resolución 2706 de 2025", "https://minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/VP/DOA/OAS/socializacion-res-2706-de-2025-cups.pdf"), { text: "." },
  ], M, 6.35, 12.1, 0.55, { fontSize: 9.5, color: C.accent6, valign: "bottom" });
}

// ================= 8 · roles =================
{
  const s = newSlide(SECSF, "Roles: dos de SURA y cuatro de Tech and Solve",
    "Tech and Solve Spec Flow combina dos roles de SURA con cuatro de Tech and Solve. Los roles se cubren con el equipo de la lámina 3: el arquitecto líder y los dos desarrolladores IA, que son los builders. La verificación la asumen los builders, apoyados en la IA, y el operador de liberación es el soporte de media jornada.");
  const part = (t, col) => ({ text: t, options: { bold: true, color: col, fontSize: 10.5, align: "center" } });
  const rol = (a, b) => ({ text: [{ text: a, options: { bold: true, color: C.text2, breakLine: !!b } }].concat(b ? [{ text: b, options: { color: C.accent6, fontSize: 8.5 } }] : []), options: { fontSize: 10 } });
  sfTable(s, ["Rol", "Parte", "Responsabilidad"], [
    [rol("Líder funcional", "Product Owner de SURA"), part("SURA", C.accent3), "Decide qué capacidades importan y en qué orden. Describe cómo deben funcionar con ejemplos concretos, entrega datos de prueba realistas y certifica cada capacidad, apoyándose en usuarios clave si lo necesita."],
    [rol("Arquitecto técnico de negocio", "Arquitectura de SURA"), part("SURA", C.accent3), "Aporta reglas de negocio complejas, integraciones con sus sistemas, restricciones de seguridad y cumplimiento, y acceso a ambientes y datos. Valida cualquier decisión técnica que afecte a sus sistemas y aprueba con el arquitecto líder cada paso a producción."],
    [rol("Arquitecto líder"), part("Tech", C.accent1), "Garantiza que la implementación respete la arquitectura de gestores definida con SURA, sus lineamientos AI First y los techos de autonomía: ningún agente niega. Mantiene el contexto del agente y las plantillas, revisa el código crítico y es el interlocutor del arquitecto de SURA, con quien aprueba cada paso a producción. Responde del tablero y del ajuste continuo del método."],
    [rol("Builders (2)"), part("Tech", C.accent1), "Generan con el agente la especificación, el diseño técnico y las tareas de cada capacidad a partir de la ficha, dirigen la generación de código, revisan, integran y corrigen lo que la IA no resuelve bien. Máximo dos capacidades a la vez cada uno. Con IA asumen también la verificación."],
    [rol("Verificador", "Lo asumen los builders, con IA"), part("Tech", C.accent1), "Traduce los ejemplos y datos de SURA en pruebas automatizadas de aceptación, mantiene la suite de regresión y los controles de calidad del pipeline, e incorpora la evaluación de los agentes: golden set sin regresión, LLM-as-a-judge calibrado, y latencia y costo por caso."],
    [rol("Operador de liberación", "El soporte de media jornada"), part("Tech", C.accent1), "Mantiene el pipeline de integración y despliegue continuo, que lleva cada capacidad a certificación de forma automática y a producción una vez aprobada, con su rollback. Atiende la operación: banderas, monitoreo e incidentes, con una prueba nueva por cada incidente, y se alinea con el arquitecto líder o un builder si tiene dudas."],
  ], { y: 1.45, colW: [2.6, 0.9, 8.6], rowH: [0.32, 0.6, 0.6, 0.72, 0.6, 0.6, 0.6], fs: 10 });
  T(s, [{ text: "En el equipo propuesto, el arquitecto líder es Didier Fabián Franco Gómez; los builders son Juan Gabriel Colorado y Gian Valdiris, que con IA asumen también la verificación, y el operador de liberación es el soporte de media jornada." }], M, 5.55, 12.1, 0.4, { fontSize: 9.5, color: C.accent6 });
}

// ================= 9 · fases del proyecto (hoja de ruta) =================
{
  const s = newSlide(SECSF, "Fases del proyecto: arranque, primer release y flujo continuo",
    "Tres fases. El arranque dura como máximo una semana, deja todo listo para construir y define lo común: arquetipo, contrato de eventos y trazabilidad. El primer release es el único alcance que se agrupa. En el flujo continuo proponemos un orden de tres bloques con dos hitos de activación; es un orden, no un calendario, y SURA lo confirma o lo cambia. Los hitos dependen también del front y la integración que lideran los equipos de SURA; los simuladores evitan que esa dependencia detenga la construcción.");
  const g = 0.08, w1 = 2.95, w2 = 2.45, w3 = 12.1 - w1 - w2 - 2 * g;
  const x1 = M, x2 = x1 + w1 + g, x3 = x2 + w2 + g, hy = 1.55, hh = 0.42, by = 2.05, bh = 3.85;
  s.addShape(pres.ShapeType.homePlate, { x: x1, y: hy, w: w1, h: hh, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  s.addShape(pres.ShapeType.chevron, { x: x2, y: hy, w: w2, h: hh, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 } });
  s.addShape(pres.ShapeType.chevron, { x: x3, y: hy, w: w3, h: hh, fill: { color: C.accent3 }, line: { color: C.accent3, width: 0 } });
  [["1 · Arranque", x1, w1], ["2 · Primer release", x2, w2], ["3 · Flujo continuo", x3, w3]].forEach(([t, x, w]) => T(s, t, x, hy, w, hh, { align: "center", valign: "middle", fontSize: 12.5, bold: true, color: C.background1 }));
  card(s, x1, by, w1, bh);
  T(s, [{ text: "Máximo una semana", options: { bold: true, color: C.text2, fontSize: 12.5, breakLine: true, paraSpaceAfter: 6 } }, { text: "Repositorio base, contexto del agente, pipeline, simuladores, ambientes de desarrollo y certificación, acceso a datos y sistemas de SURA, y primeras fichas listas.", options: { breakLine: true, paraSpaceAfter: 6 } }, { text: "Se define lo común: ", options: { bold: true, color: C.text2 } }, { text: "arquetipo, contrato de eventos y trazabilidad." }], x1 + 0.18, by + 0.12, w1 - 0.36, bh - 0.24, { fontSize: 11.5 });
  card(s, x2, by, w2, bh);
  T(s, [{ text: "Conjunto mínimo de capacidades acordado con el líder funcional.", options: { breakLine: true, paraSpaceAfter: 6 } }, { text: "Es la única vez que se agrupa un alcance.", options: { bold: true, color: C.text2 } }], x2 + 0.18, by + 0.12, w2 - 0.36, bh - 0.24, { fontSize: 11.5 });
  card(s, x3, by, w3, bh);
  T(s, "Cada capacidad certificada se libera de forma independiente y automatizada, normalmente detrás de una bandera de activación que SURA decide encender.", x3 + 0.18, by + 0.1, w3 - 0.36, 0.6, { fontSize: 11.5 });
  T(s, "Orden sugerido, no un calendario: SURA lo confirma o lo cambia al priorizar el backlog", x3 + 0.18, by + 0.72, w3 - 0.36, 0.28, { fontSize: 10, bold: true, color: C.accent3 });
  const bw = (w3 - 0.36 - 2 * 0.12) / 3, bt = by + 1.08;
  [["Bloque 1", "Agentes de Solicitud", "Clasificador, enrutador, extractores, request builder y LLM-as-a-judge; escala a preradicado con su motivo.", "Hito 1 · agentes de Solicitud listos para activar"], ["Bloque 2", "Agentes de Evaluación", "Coberturas, pertinencia médica, duplicidad y concepto al escalar. Ningún agente niega.", "Hito 2 · autorización automática de nivel 1 lista para activar"], ["Bloque 3", "Auditor y cierre", "Auditor dentro de cada gestor, que propone sin promover, y pruebas de punta a punta.", ""]].forEach(([b, t, d, h], i) => {
    const x = x3 + 0.18 + i * (bw + 0.12);
    card(s, x, bt, bw, 1.45, { fill: { color: C.background1 } });
    s.addShape(pres.ShapeType.rect, { x: x + 0.08, y: bt, w: bw - 0.16, h: 0.05, fill: { color: C.accent3 }, line: { color: C.accent3, width: 0 } });
    T(s, [{ text: b, options: { bold: true, color: C.accent2, fontSize: 8.5, breakLine: true } }, { text: t, options: { bold: true, color: C.text2, fontSize: 11, breakLine: true } }, { text: d, options: { fontSize: 9.5 } }], x + 0.1, bt + 0.08, bw - 0.2, 1.32, { valign: "top" });
    if (h) {
      s.addShape(pres.ShapeType.roundRect, { x, y: bt + 1.58, w: bw, h: 0.55, rectRadius: 0.08, fill: { color: C.background1 }, line: { color: C.accent3, width: 1.5 } });
      T(s, h, x + 0.06, bt + 1.58, bw - 0.12, 0.55, { align: "center", valign: "middle", fontSize: 9, bold: true, color: C.accent3 });
    }
  });
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 6.05, w: 12.1, h: 0.72, rectRadius: 0.08, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, [{ text: "Transversal · trazabilidad para la torre de control. ", options: { bold: true } }, { text: "Se define en el arranque y se implementa en todos los bloques. Traza, golden set, compuerta, umbral y calibración entran con Solicitud; corrección estructurada y muestreo, con Evaluación." }], M + 0.25, 6.05, 11.6, 0.72, { fontSize: 11, color: C.background1, valign: "middle" });
}

// ================= 10 · etapas de una capacidad (zonas, como la lámina 4 de v2) =================
{
  const s = newSlide(SECSF, "Etapas de una capacidad: SURA define y certifica, Tech and Solve construye, y liberamos y observamos en conjunto",
    "Las ocho etapas de una capacidad, con el diagrama de Tech and Solve Spec Flow. SURA lidera la propuesta, la definición y la certificación; Tech and Solve lidera la preparación, la construcción y la verificación. La liberación a producción y la observación de lo liberado se hacen en conjunto: el arquitecto líder y el arquitecto técnico de negocio de SURA aprueban el paso, el pipeline despliega de forma automática, SURA decide cuándo activar y ambos observan hasta que la capacidad está estable. Una capacidad que falla en verificación o es rechazada en certificación vuelve a construcción; en el segundo caso, primero se actualiza la especificación.");
  const zone = (x, w, label, fill, txtCol) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.62, w, h: 4.0, rectRadius: 0.08, fill: { color: fill }, line: { color: BORDER, width: 1 } });
    T(s, label, x + 0.18, 1.7, w - 0.36, 0.32, { fontSize: 11.5, bold: true, color: txtCol });
  };
  const stage = (x, y, w, h, n, t, sub, col) => {
    card(s, x, y, w, h, { fill: { color: C.background1 } });
    dot(s, x + 0.12, y + (h - 0.44) / 2, 0.44, n, { fontSize: 12, fill: col });
    T(s, [{ text: t, options: { bold: true, color: C.text2, fontSize: 12, breakLine: true } }, { text: sub, options: { color: C.accent6, fontSize: 9.5 } }], x + 0.65, y + 0.04, w - 0.75, h - 0.08, { valign: "middle" });
  };
  const SU = C.accent3, TE = C.accent1, DO = C.accent2;
  zone(M, 3.25, "Definir", C.background2, C.text2);
  stage(M + 0.15, 2.1, 2.95, 1.1, "1", "Propuesta", "El líder funcional la registra con su valor de negocio", SU);
  stage(M + 0.15, 3.28, 2.95, 1.1, "2", "Definición", "Ficha en la mesa de definición y se asigna talla", SU);
  stage(M + 0.15, 4.46, 2.95, 1.1, "3", "Lista para construir", "Ficha completa y al menos tres ejemplos con datos", TE);
  const mx = M + 3.25 + 0.2, mw = 5.4, cw = (mw - 0.45) / 2;
  zone(mx, mw, "Construir con IA · el equipo, con el negocio cerca", C.accent4, C.accent1);
  stage(mx + 0.15, 2.1, cw, 1.1, "4", "Construcción", "Especificación, diseño y tareas; primero pruebas, luego código", TE);
  stage(mx + 0.3 + cw, 2.1, cw, 1.1, "5", "Verificación", "Pruebas, regresión y revisión de seguridad en el pipeline", TE);
  s.addShape(pres.ShapeType.roundRect, { x: mx + 0.15, y: 3.32, w: mw - 0.3, h: 2.2, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Dentro de Construcción: desarrollo guiado por especificaciones", mx + 0.3, 3.4, mw - 0.6, 0.3, { fontSize: 10.5, bold: true, color: C.text2 });
  const chips = [["Ficha", true], ["Especificación", false], ["Diseño técnico", false], ["Tareas", false], ["Pruebas y código", false]];
  const gap = 0.14, chw = (mw - 0.6 - 4 * gap) / 5;
  chips.forEach(([t, cl], i) => {
    const x = mx + 0.3 + i * (chw + gap), y = 3.95;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: chw, h: 0.6, rectRadius: 0.06, fill: { color: C.background1 }, line: { color: cl ? SU : TE, width: 1 } });
    T(s, t, x + 0.01, y, chw - 0.02, 0.6, { align: "center", valign: "middle", fontSize: 8, bold: true, color: C.text2 });
    if (i < 4) s.addShape(pres.ShapeType.line, { x: x + chw + 0.01, y: y + 0.3, w: gap - 0.02, h: 0, line: { color: C.accent6, width: 1, endArrowType: "triangle" } });
  });
  T(s, "Revisión humana antes de cada paso; la ficha la aprueba SURA.", mx + 0.3, 4.75, mw - 0.6, 0.45, { fontSize: 9.5, color: C.accent6, valign: "middle" });
  const rx = mx + mw + 0.2, rw = 12.1 - (rx - M);
  zone(rx, rw, "Certificar, liberar y observar", C.background2, C.text2);
  stage(rx + 0.15, 2.1, rw - 0.3, 1.1, "6", "Certificación", "SURA prueba en QA y aprueba o rechaza con observaciones", SU);
  stage(rx + 0.15, 3.28, rw - 0.3, 1.1, "7", "Liberada", "Los dos arquitectos aprueban, el pipeline despliega y SURA activa", DO);
  stage(rx + 0.15, 4.46, rw - 0.3, 1.1, "8", "Estable", "Observación conjunta sin incidentes, p. ej. 5 días hábiles", DO);
  s.addShape(pres.ShapeType.leftArrow, { x: M, y: 5.78, w: 12.1, h: 0.7, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Vuelve a construcción si falla la verificación o si SURA la rechaza en certificación; en el segundo caso, primero se actualiza la especificación", M + 0.8, 5.78, 11.0, 0.7, { fontSize: 11.5, bold: true, color: C.text2, valign: "middle", align: "center" });
  const y = 6.98;
  s.addText("Quién lidera:", { x: 6.6, y, w: 1.3, h: 0.35, fontSize: 10, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true });
  [["SURA", SU, 7.95, 0.6], ["Tech and Solve", TE, 8.95, 1.2], ["En conjunto", DO, 10.55, 1.0]].forEach(([lab, col, x, w]) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: y + 0.1, w: 0.3, h: 0.15, rectRadius: 0.04, fill: { color: col }, line: { color: col, width: 0 } });
    s.addText(lab, { x: x + 0.38, y, w: w + 0.3, h: 0.35, fontSize: 10, color: C.accent6, valign: "middle", margin: 0, isTextBox: true });
  });
}

// ================= 11 · definición liviana =================
{
  const s = newSlide(SECSF, "Definición liviana: una conversación corta y una ficha de una sola pantalla",
    "La definición es una conversación corta que deja un artefacto mínimo: una ficha de cuatro campos que cabe en una pantalla. Los ejemplos con datos son la base de las pruebas. Con los datos clínicos distinguimos tres momentos: para construir y verificar usamos casos reales de SURA con los datos sensibles anonimizados, porque así la afinación de los agentes es óptima; la pertinencia médica y la calibración del juez se evalúan dentro de la infraestructura de SURA, con muestra anonimizada que revisan sus expertos; y la activación pasa por modo shadow. El marco es la Ley 1581 de 2012, la Resolución 1995 de 1999 y la Ley 2015 de 2020, además de las políticas de SURA. El protocolo se acuerda en el arranque con el arquitecto técnico de negocio y el área de protección de datos de SURA.");
  const lw = 5.2;
  T(s, [{ text: "Con IA, " }, { text: "construir es barato y lo caro es la ambigüedad", options: { bold: true, color: C.text2 } }, { text: ". Si una capacidad no cabe en una pantalla o en tres días, se parte." }], M, 1.45, lw, 0.5, { fontSize: 10.5 });
  sfTable(s, ["Campo", "Contenido"], [["Para qué", "Una frase con el resultado de negocio que se busca"], ["Ejemplos", "Entre 3 y 5 casos concretos en tabla: datos de entrada y resultado esperado"], ["Reglas no obvias", "Solo lo que un builder no deduciría por sí mismo"], ["Cómo se certifica", "Quién prueba y qué tiene que ver para aprobar"]], { x: M, y: 2.0, w: lw, colW: [1.5, 3.7], rowH: [0.3, 0.42, 0.48, 0.42, 0.42], fs: 10 });
  const rx = M + lw + 0.25, rw = 12.1 - lw - 0.25;
  card(s, rx, 1.45, rw, 2.6);
  T(s, "Prácticas de la mesa de definición", rx + 0.2, 1.52, rw - 0.4, 0.32, { fontSize: 12, bold: true, color: C.text2 });
  T(s, boldBullets([["Ejemplos en lugar de redacción: ", "los builders, con IA, los convierten en pruebas de aceptación."], ["La ficha se escribe en la conversación, ", "de 20 a 30 minutos; con la sesión grabada, la IA genera el borrador y SURA solo corrige."], ["Prototipo generado por IA, ", "desechable, para que SURA reaccione a algo visible."], ["Justo a tiempo: ", "solo lo que entra a construcción en las próximas dos semanas."], ["Las dudas menores no bloquean: ", "SURA responde en menos de 24 horas."]], 3), rx + 0.2, 1.88, rw - 0.4, 2.1, { fontSize: 10 });
  card(s, M, 4.2, 12.1, 2.65, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Los datos clínicos: con qué datos se trabaja en cada momento", M + 0.25, 4.28, 11.6, 0.34, { fontSize: 12.5, bold: true, color: C.text2 });
  const dw = (12.1 - 0.5 - 2 * 0.3) / 3;
  [[C.accent1, "Construir y verificar. ", "Casos reales de SURA con los datos sensibles anonimizados, para que la afinación de los agentes sea óptima. Nada que identifique a un paciente sale de SURA."], [C.accent2, "Evaluar con la muestra clínica. ", "Dentro de la infraestructura de SURA, con muestra anonimizada que revisan sus expertos. Ahí se valida la pertinencia médica y se calibra el LLM-as-a-judge; los datos no salen de SURA."], [C.accent3, "Activar con control. ", "En modo shadow, el agente opina sin decidir y se compara con las personas. SURA decide la activación."]].forEach(([col, t, b], i) => {
    const x = M + 0.25 + i * (dw + 0.3);
    s.addShape(pres.ShapeType.rect, { x, y: 4.7, w: dw, h: 0.05, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, [{ text: t, options: { bold: true, color: C.text2 } }, { text: b }], x, 4.8, dw, 1.15, { fontSize: 10 });
  });
  T(s, [
    { text: "Los datos de salud son sensibles según la " }, link("Ley 1581 de 2012", "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981"),
    { text: "; la historia clínica es reservada según la " }, link("Resolución 1995 de 1999", "https://normograma.supersalud.gov.co/compilacion/docs/resolucion_minsalud_r1995_99.htm"),
    { text: ", y su intercambio electrónico lo regula la " }, link("Ley 2015 de 2020", "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=105472"),
    { text: ". Aplican las políticas de SURA, y sus datos solo van a herramientas que SURA autorice." },
  ], M + 0.25, 6.0, 11.6, 0.75, { fontSize: 9.5, color: C.accent6, valign: "middle" });
}

// ================= 12 · desarrollo guiado por especificaciones =================
{
  const s = newSlide(SECSF, "Desarrollo guiado por especificaciones: la especificación define el qué antes del cómo",
    "La construcción sigue el enfoque de desarrollo guiado por especificaciones (spec driven development). La ficha la escribe SURA con el arquitecto líder; la especificación, el diseño técnico, las tareas, las pruebas y el código los genera el agente y los aprueba el equipo, con puntos de aprobación entre cada paso. Lo que lo hace posible es el harness, que se explica en la lámina siguiente.");
  T(s, "La especificación vive en el repositorio junto al código y es la fuente de verdad del comportamiento. La IA genera a partir de ella el diseño, las tareas y el código; las personas la revisan y aprueban en cada paso. La ficha sigue siendo liviana: SURA no carga con más documentación.", M, 1.5, 12.1, 0.55, { fontSize: 11 });
  sfTable(s, ["Artefacto", "Quién lo produce", "Quién lo aprueba", "Contenido"], [
    ["Ficha de capacidad", "Líder funcional con el arquitecto líder", "Líder funcional", "Para qué, ejemplos con datos, reglas no obvias, cómo se certifica"],
    ["Especificación", "Agente, dirigido por un builder", "Builder", "Requisitos verificables derivados de la ficha, en formato estructurado (por ejemplo, «cuando ocurra X, el sistema hará Y»)"],
    ["Diseño técnico", "Agente, dirigido por un builder", "Builder; arquitecto líder si toca la arquitectura", "Cómo se implementa dentro de la arquitectura definida: componentes, datos, integraciones"],
    ["Tareas", "Agente", "Builder", "Pasos pequeños y verificables que el agente ejecuta uno a uno"],
    ["Pruebas y código", "Agente", "Builders, que verifican con IA", "Primero las pruebas de aceptación, después el código"],
  ], { y: 2.05, colW: [1.85, 2.55, 2.55, 5.15], rowH: [0.32].concat(Array(5).fill(0.5)), fs: 10.5 });
  T(s, "Reglas", M, 4.92, 12.1, 0.32, { fontSize: 13, bold: true, color: C.text2 });
  const rw = (12.1 - 0.2) / 2;
  [["Puntos de aprobación.", "No se pasa de especificación a diseño, ni de diseño a tareas, sin revisión humana: es el lugar más barato para corregir a la IA."], ["Primero la especificación.", "Todo cambio, incluidas observaciones de certificación e incidentes, va primero a la especificación y después se regenera."], ["El contexto del agente es la base común,", "y el arquitecto líder lo mantiene junto con las plantillas."], ["Trazabilidad.", "Cada prueba se vincula a un requisito, y cada requisito a un ejemplo de la ficha."]].forEach(([a, t], i) => {
    const x = M + (i % 2) * (rw + 0.2), y = 5.3 + Math.floor(i / 2) * 0.78;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: rw, h: 0.68, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
    T(s, [{ text: a + " ", options: { bold: true, color: C.text2 } }, { text: t }], x + 0.18, y, rw - 0.36, 0.68, { fontSize: 10.5, valign: "middle" });
  });
}
// ================= 13 · harness =================
{
  const s = newSlide(SECSF, "Las personas no escriben el código línea a línea: cuidan el harness que lo produce",
    "El trabajo del equipo no es escribir el código línea a línea, sino construir y cuidar el harness que lo produce: el contexto del agente, las plantillas, las reglas desde revisiones reales, los puntos de aprobación, las pruebas primero y los auditores. El arquitecto líder cuida que ese harness refleje la arquitectura acordada con SURA. Cuando algo sale mal, no se arregla solo el código: se corrige la pieza del harness que lo produjo, con las palancas del ajuste continuo del método, para que el error no vuelva. A diferencia de un IDE con IA, no depende de la disciplina de cada quien.");
  const lw = 7.85, rx = M + lw + 0.25, rw = 12.1 - lw - 0.25;
  T(s, "El harness es todo lo que rodea al modelo para que el código salga bien y encaje con la arquitectura definida.", M, 1.5, lw, 0.4, { fontSize: 11 });
  sfTable(s, ["Pieza", "Qué hace", "Quién la cuida"], [["Contexto del agente", "Arquitectura, convenciones y decisiones técnicas, y una base de conocimiento sincronizada con el código antes de cada sesión", "Arquitecto líder"], ["Plantillas de ficha y de especificación", "Dan la misma forma a cada capacidad, de la conversación con SURA a los requisitos verificables", "Arquitecto líder"], ["Reglas desde revisiones reales", "Lo que un revisor corrigió una vez, el agente lo aplica siempre", "Arquitecto líder"], ["Puntos de aprobación y compuertas", "El agente no avanza sin revisión humana; publicar exige la firma de una persona", "Builders; arquitecto líder si toca la arquitectura"], ["Pruebas primero y golden set", "Los ejemplos de SURA se vuelven pruebas antes de que exista el código", "Builders, que verifican con IA"], ["Auditores, traza y continuidad", "Agentes auditores revisan requisitos y evidencia; cada tarea queda versionada y se retoma en cualquier momento", "Builders y arquitecto líder"]], { x: M, y: 1.95, w: lw, colW: [2.0, 3.65, 2.2], rowH: [0.32, 0.62].concat(Array(5).fill(0.54)), fs: 9.5 });
  s.addShape(pres.ShapeType.roundRect, { x: rx, y: 1.5, w: rw, h: 2.95, rectRadius: 0.1, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, "Qué cuida el arquitecto líder", rx + 0.22, 1.6, rw - 0.44, 0.38, { fontSize: 13, bold: true, color: C.background1 });
  T(s, ["Que el contexto del agente refleje la arquitectura acordada con SURA.", "Las plantillas de especificación y el arquetipo de agente.", "Los diseños que tocan la arquitectura y el código crítico.", "La bitácora del método: cada ajuste al harness queda a la vista del equipo y de SURA."].map((t, k, a) => ({ text: t, options: { bullet: true, breakLine: k < a.length - 1, paraSpaceAfter: 5 } })), rx + 0.22, 2.02, rw - 0.44, 2.35, { fontSize: 10.5, color: C.background1 });
  card(s, rx, 4.58, rw, 1.42, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "No es un IDE con IA. ", options: { bold: true, color: C.text2 } }, { text: "El conocimiento, las reglas y el control no dependen de la disciplina de cada quien. Es independiente de la herramienta: Claude Code y plantillas propias, GitHub Spec Kit o los specs de Kiro." }], rx + 0.2, 4.58, rw - 0.4, 1.42, { fontSize: 9.5, valign: "middle" });
  band(s, M, 6.12, 12.1, 0.72, "Si algo sale mal, se corrige el harness, no solo el código: ", "así el error no vuelve y la solución encaja con las definiciones de arquitectura. La responsabilidad sigue siendo de las personas: todo lo revisa alguien antes de llegar a certificación.", 11);
}

// ================= 14 · matriz de roles por momento =================
{
  const s = newSlide(SECSF, "Matriz de roles por momento",
    "Qué hace cada rol en cada momento, del arranque a la operación. SURA está presente en todas las etapas, con más peso en la propuesta, la definición, la certificación y la decisión de activar. Los tiempos de respuesta de SURA son los compromisos de la lámina 19. La liberación a producción es un modelo compartido: el arquitecto líder de Tech and Solve y el arquitecto técnico de negocio de SURA aprueban juntos cada paso, el pipeline despliega de forma continua y automatizada, SURA decide cuándo activar y los dos observan lo liberado. La operación la atiende el soporte, que se alinea con el arquitecto líder o un builder cuando tiene dudas. Los builders construyen y verifican con IA, así que no hay una columna aparte de verificador; el soporte es el operador de liberación y atiende la operación.");
  const c = (t) => ({ text: t, options: { fontSize: 8.5, valign: "middle" } });
  const KIND = { "Arranque": "D", "Propuesta": "S", "Definición": "S", "Lista para construir": "T", "Construcción": "T", "Verificación": "T", "Certificación": "S", "Liberación": "D", "Operación": "D" };
  const LAB = { S: ["Lidera SURA", C.accent3], T: ["Lidera Tech", C.accent1], D: ["En conjunto", C.accent2] };
  const SHARED = new Set(["Liberación", "Operación"]);
  const mom = (t) => ({ text: t, options: { fontSize: 9, bold: true, color: C.text2, fill: { color: C.background2 } } });
  const rows = [
    ["Arranque", "Prioriza el backlog y define el alcance del primer release", "Da acceso a sistemas, datos y ambientes", "Traslada la arquitectura al contexto del agente", "Montan la base del código y el marco de pruebas", "Monta pipeline, ambientes y monitoreo"],
    ["Propuesta", "Registra y prioriza capacidades", "Señala impactos en sus sistemas", "Detecta dependencias técnicas", "Informados", "Informado"],
    ["Definición", "Aporta ejemplos con datos y reacciona al prototipo", "Aporta reglas e integraciones", "Facilita la sesión, llena la ficha en vivo y asigna talla", "Hacen preguntas técnicas, generan prototipos desechables y validan que los criterios sean verificables", "Señala impactos operativos"],
    ["Lista para construir", "Confirma la ficha", "Confirma reglas e integraciones", "Aprueba la entrada a construcción", "Toman la capacidad y generan con IA las pruebas de aceptación", "Informado"],
    ["Construcción", "Responde dudas en menos de 24 h", "Resuelve dudas de integración", "Aprueba los diseños que tocan la arquitectura y revisa código crítico", "Revisan especificación, diseño y tareas; dirigen la generación, revisan, integran y ajustan las pruebas", "Prepara la bandera de activación"],
    ["Verificación", "Informado", "Informado", "Revisa hallazgos graves", "Ejecutan las pruebas con IA, reportan resultados y corrigen fallos", "Vigila el pipeline"],
    ["Certificación", "Prueba y certifica en menos de 48 h", "Certifica aspectos de integración", "Atiende observaciones técnicas", "Actualizan la especificación, corrigen observaciones y suman los rechazos a la regresión", "El pipeline despliega en certificación de forma automática"],
    ["Liberación", "Decide cuándo activar", "Coordina ventanas y aprueba la liberación con el arquitecto líder", "Aprueba la liberación con el arquitecto de negocio", "De guardia ante incidencias", "Una vez aprobada, el pipeline despliega; activa la bandera y ejecuta pruebas en producción"],
    ["Operación", "Reporta comportamientos anómalos", "Reporta incidencias de integración", "Analiza causas raíz", "Actualizan la especificación y corrigen incidentes", "Monitorea y atiende incidentes; añade pruebas para cada incidente"],
  ].map(([m, ...r]) => [mom(m)].concat(r.map(c)));
  const head = [
    [th("Momento", C.text2, { rowspan: 2, valign: "bottom", fontSize: 9.5 }), th("SURA", C.accent3, { colspan: 2, align: "center", fontSize: 9.5 }), th("Tech and Solve", C.accent1, { colspan: 3, align: "center", fontSize: 9.5 })],
    [th("Líder funcional", C.accent3, { fontSize: 9.5 }), th("Arquitecto de negocio", C.accent3, { fontSize: 9.5 }), th("Arquitecto líder", C.text2, { fontSize: 9.5 }), th("Builders (construyen y verifican con IA)", C.text2, { fontSize: 9.5 }), th("Soporte (operador de liberación)", C.text2, { fontSize: 9.5 })],
  ];
  s.addTable(head.concat(rows), tblBase({ x: M, y: 1.45, w: 12.1, colW: [1.4, 1.85, 1.7, 1.95, 2.75, 2.45], rowH: [0.27, 0.44].concat(Array(9).fill(0.52)), fontSize: 8.5 }));
}

// ================= 15 · encuentros de trabajo =================
{
  const s = newSlide(SECSF, "Encuentros de trabajo: tres espacios con SURA",
    "Tres encuentros de trabajo con SURA: la mesa de definición dos veces por semana, la revisión de flujo semanal con todos y la certificación según llegan capacidades. En cada certificación SURA recibe el estado de cada capacidad, la entrega en QA y las evidencias trazables, y decide cuándo activar en producción.");
  sfTable(s, ["Encuentro", "Frecuencia", "Participantes", "Propósito"], [
    ["Mesa de definición", "Dos veces por semana", "Líder funcional, arquitecto de negocio, arquitecto líder", "Llevar capacidades a «lista para construir», de 20 a 30 minutos por capacidad"],
    ["Revisión de flujo", "Semanal, 45 minutos", "Todos, incluido SURA", "Prioridades, bloqueos y métricas"],
    ["Certificación", "Según llegan capacidades", "Líder funcional, usuarios clave y builders", "Probar y aprobar"],
  ], { y: 1.5, colW: [2.4, 2.4, 3.6, 3.7], rowH: [0.36, 0.6, 0.45, 0.45], fs: 12 });
  T(s, "Qué recibe SURA en cada certificación", M, 3.55, 12.1, 0.34, { fontSize: 13, bold: true, color: C.text2 });
  const w = (12.1 - 2 * 0.22) / 3;
  [["Capacidades con su estado", "En el tablero: lista para certificar, certificada o de vuelta a construcción, y el porqué."], ["Entrega en QA", "Funcionando con su traza sobre casos reales anonimizados, con su bandera de activación lista."], ["Evidencias trazables", "Ficha, especificación aprobada, pruebas vinculadas a cada requisito, golden set sin regresión y revisión humana."]].forEach(([t, b], i) => {
    const x = M + i * (w + 0.22);
    card(s, x, 4.0, w, 1.75);
    dot(s, x + 0.2, 4.15, 0.42, String(i + 1), { fontSize: 12, fill: C.accent3 });
    T(s, t, x + 0.75, 4.12, w - 0.9, 0.46, { fontSize: 12, bold: true, color: C.text2, valign: "middle" });
    T(s, b, x + 0.2, 4.7, w - 0.4, 1.0, { fontSize: 11 });
  });
  band(s, M, 5.95, 12.1, 0.6, "A producción, cuando SURA lo decide. ", "El paso a producción lo aprueban el arquitecto líder y el arquitecto técnico de negocio de SURA, y el pipeline lo despliega de forma continua y automatizada; cada capacidad se activa por separado con su bandera, y la activación siempre la aprueba una persona.", 11.5);
}

// ================= 16 · ajuste continuo del método (ciclo y señales) =================
{
  const s = newSlide(SECSF, "Ajuste continuo del método: se mejora en cuanto se detecta un problema",
    "El método se ajusta de forma continua, no en una sesión dedicada. El arquitecto líder mira el tablero y la calidad del código generado, y corrige el contexto del agente, las plantillas, los límites de trabajo en curso o los acuerdos con SURA. Cada cambio queda en una bitácora visible.");
  // Izquierda: ciclo observa, detecta, ajusta y registra alrededor del arquitecto líder
  const lw = 3.85;
  card(s, M, 1.6, lw, 4.4);
  const ccx = M + lw / 2, ccy = 3.2, R = 1.2;
  s.addShape(pres.ShapeType.ellipse, { x: ccx - R, y: ccy - R, w: 2 * R, h: 2 * R, fill: { type: "none" }, line: { color: C.accent1, width: 2 } });
  s.addShape(pres.ShapeType.ellipse, { x: ccx - 0.62, y: ccy - 0.62, w: 1.24, h: 1.24, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, "Arquitecto\nlíder", ccx - 0.62, ccy - 0.62, 1.24, 1.24, { align: "center", valign: "middle", fontSize: 12, bold: true, color: C.background1 });
  [["1 · Observa", "tablero y código", 0, -1], ["2 · Detecta", "un problema", 1, 0], ["3 · Ajusta", "una palanca", 0, 1], ["4 · Registra", "en la bitácora", -1, 0]].forEach(([t, d, dx, dy]) => {
    const nw = 1.3, nh = 0.56, x = ccx + dx * R - nw / 2, y = ccy + dy * R - nh / 2;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: nw, h: nh, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: C.accent1, width: 1.5 } });
    T(s, [{ text: t, options: { bold: true, color: C.text2, fontSize: 11, breakLine: true } }, { text: d, options: { fontSize: 8.5, color: C.accent6 } }], x, y, nw, nh, { align: "center", valign: "middle" });
  });
  T(s, "De forma permanente, con las métricas del tablero y la calidad del código generado, sin esperar a una sesión dedicada.", M + 0.2, 4.95, lw - 0.4, 0.9, { fontSize: 10, color: C.accent6, align: "center", valign: "middle" });
  // Derecha: señal y palanca
  const rx = M + lw + 0.25, rw = 12.1 - lw - 0.25, sw = rw * 0.41, aw = 0.4, pw = rw - sw - aw, rh = 1.0, g = 0.13;
  [["La IA repite un error o se desvía de un patrón", "Contexto del agente", "se corrige para que no vuelva a ocurrir."], ["Sube el rechazo en certificación o el código se aparta de lo esperado", "Plantillas de la ficha y de especificación", "se ajustan para cerrar los huecos."], ["Se forma cola en una etapa", "Límites de trabajo en curso", "se suben o bajan según dónde esté la cola."], ["Crecen los bloqueos de SURA", "Acuerdos con SURA", "se tratan en la revisión de flujo semanal."]].forEach(([sig, lev, act], i) => {
    const y = 1.6 + i * (rh + g);
    s.addShape(pres.ShapeType.roundRect, { x: rx, y, w: sw, h: rh, rectRadius: 0.08, fill: { color: "F7EEDF" }, line: { color: "F7EEDF", width: 0 } });
    T(s, [{ text: "SEÑAL", options: { bold: true, fontSize: 8, color: C.accent2, breakLine: true } }, { text: sig }], rx + 0.15, y, sw - 0.3, rh, { fontSize: 11.5, valign: "middle" });
    s.addShape(pres.ShapeType.line, { x: rx + sw + 0.07, y: y + rh / 2, w: aw - 0.14, h: 0, line: { color: C.accent1, width: 1.75, endArrowType: "triangle" } });
    s.addShape(pres.ShapeType.roundRect, { x: rx + sw + aw, y, w: pw, h: rh, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
    T(s, [{ text: "PALANCA " + (i + 1), options: { bold: true, fontSize: 8, color: C.accent1, breakLine: true } }, { text: lev + ": ", options: { bold: true, color: C.text2 } }, { text: act }], rx + sw + aw + 0.15, y, pw - 0.3, rh, { fontSize: 11.5, valign: "middle" });
  });
  band(s, M, 6.15, 12.1, 0.62, "Bitácora del método. ", "Cada cambio queda registrado en una bitácora visible para todo el equipo y se comenta brevemente en la revisión de flujo.", 12);
}

// ================= 17 · tablero de gestión =================
{
  const s = newSlide(SECSF, "Tablero de gestión: una columna por etapa y límites de trabajo en curso",
    "El tablero tiene una columna por etapa. Las etapas activas se dividen en en curso y terminado esperando la siguiente etapa, para ver dónde se forma cola. Los límites de trabajo en curso son 6 en definición, 6 en lista para construir como reserva, 4 en construcción (dos por builder), 3 en verificación y 4 en certificación. Cada bloqueo lleva origen, fecha y responsable.");
  const KC = { S: C.accent3, T: C.accent1, D: C.accent2 };
  const cols = [["Propuesta", "S", "", ""], ["Definición", "S", "6", ""], ["Lista para construir", "T", "6", "reserva"], ["Construcción", "T", "4", "2 por builder"], ["Verificación", "T", "3", ""], ["Certificación", "S", "4", ""], ["Liberada", "D", "", ""], ["Estable", "D", "", ""]];
  const g = 0.08, bw = (12.1 - 7 * g) / 8, by = 1.55, bh = 1.95;
  cols.forEach(([n, k, w, note], i) => {
    const x = M + i * (bw + g), col = KC[k];
    s.addShape(pres.ShapeType.roundRect, { x, y: by, w: bw, h: bh, rectRadius: 0.06, fill: { color: C.accent4 }, line: { color: BORDER, width: 1 } });
    s.addShape(pres.ShapeType.rect, { x: x + 0.05, y: by, w: bw - 0.1, h: 0.06, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, n, x + 0.04, by + 0.1, bw - 0.08, 0.36, { align: "center", valign: "middle", fontSize: 10, bold: true, color: C.text2 });
    if (w) {
      T(s, [{ text: w, options: { fontSize: 22, bold: true, color: col } }, { text: " límite", options: { fontSize: 8.5, color: C.accent6 } }], x, by + 0.48, bw, 0.4, { align: "center", valign: "middle" });
      T(s, note || " ", x, by + 0.88, bw, 0.18, { align: "center", fontSize: 7.5, color: C.accent6 });
      const lw = (bw - 0.24) / 2;
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.08, y: by + 1.1, w: lw, h: 0.75, rectRadius: 0.04, fill: { color: C.background1 }, line: { color: BORDER, width: 0.75 } });
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.16 + lw, y: by + 1.1, w: lw, h: 0.75, rectRadius: 0.04, fill: { color: C.background1 }, line: { color: BORDER, width: 0.75, dashType: "dash" } });
      T(s, "en curso", x + 0.08, by + 1.12, lw, 0.18, { align: "center", fontSize: 6.5, color: C.accent6 });
      T(s, "terminado", x + 0.16 + lw, by + 1.12, lw, 0.18, { align: "center", fontSize: 6.5, color: C.accent6 });
    } else {
      T(s, "sin límite", x, by + 0.48, bw, 0.4, { align: "center", valign: "middle", fontSize: 8.5, color: C.accent6 });
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.08, y: by + 1.1, w: bw - 0.16, h: 0.75, rectRadius: 0.04, fill: { color: C.background1 }, line: { color: BORDER, width: 0.75 } });
    }
  });
  T(s, [{ text: "Las etapas activas tienen dos carriles, " }, { text: "en curso", options: { italic: true } }, { text: " y " }, { text: "terminado, esperando siguiente etapa", options: { italic: true } }, { text: ", para ver dónde se forma cola." }], M, 3.55, 7.4, 0.28, { fontSize: 9, color: C.accent6, valign: "middle" });
  [["Lidera SURA", C.accent3, 8.1], ["Lidera Tech and Solve", C.accent1, 9.35], ["En conjunto", C.accent2, 11.15]].forEach(([lab, col, x]) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 3.62, w: 0.26, h: 0.13, rectRadius: 0.03, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, lab, x + 0.32, 3.55, 1.6, 0.28, { fontSize: 9, color: C.accent6, valign: "middle" });
  });
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 3.95, w: 12.1, h: 0.5, rectRadius: 0.08, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, [{ text: "Si una etapa llega a su límite, ", options: { bold: true } }, { text: "el equipo ayuda a despejarla antes de tomar trabajo nuevo." }], M + 0.25, 3.95, 11.6, 0.5, { fontSize: 13, color: C.background1, valign: "middle" });
  const lw2 = 5.25, rx = M + lw2 + 0.2, rw = 12.1 - lw2 - 0.2, cy = 4.6, ch = 2.2;
  card(s, M, cy, lw2, ch);
  T(s, "Bloqueos", M + 0.22, cy + 0.08, lw2 - 0.44, 0.34, { fontSize: 13.5, bold: true, color: C.text2 });
  T(s, [{ text: "Cada tarjeta bloqueada se marca con su " }, { text: "origen", options: { bold: true } }, { text: " (SURA, equipo o tercero), la " }, { text: "fecha", options: { bold: true } }, { text: " de inicio y el " }, { text: "responsable", options: { bold: true } }, { text: " de resolverlo. Los de SURA se muestran aparte y se tratan en la revisión de flujo." }], M + 0.22, cy + 0.45, lw2 - 0.44, 0.95, { fontSize: 10.5 });
  s.addShape(pres.ShapeType.roundRect, { x: M + 0.22, y: cy + 1.45, w: lw2 - 0.44, h: 0.6, rectRadius: 0.06, fill: { color: "F7EEDF" }, line: { color: C.accent2, width: 1.25 } });
  T(s, [{ text: "C-09 · LLM-as-a-judge", options: { bold: true, color: C.text2, breakLine: true } }, { text: "Origen: SURA", options: { bold: true, color: C.accent2 } }, { text: " · lleva 3 días · responsable: líder funcional" }], M + 0.35, cy + 1.45, lw2 - 0.7, 0.6, { fontSize: 9.5, valign: "middle" });
  card(s, rx, cy, rw, ch);
  T(s, "Indicadores", rx + 0.22, cy + 0.08, rw - 0.44, 0.34, { fontSize: 13.5, bold: true, color: C.text2 });
  const tw = (rw - 0.44 - 0.12) / 2, th2 = 0.5;
  ["Trabajo en curso por etapa y su antigüedad en días", "Capacidades liberadas por semana", "Tiempo de ciclo, de «lista para construir» a «liberada»", "Tiempo bloqueado por origen", "Tasa de rechazo en certificación"].forEach((t, i) => {
    const x = rx + 0.22 + (i % 2) * (tw + 0.12), y = cy + 0.5 + Math.floor(i / 2) * (th2 + 0.08);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: tw, h: th2, rectRadius: 0.06, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
    dot(s, x + 0.08, y + 0.11, 0.28, String(i + 1), { fontSize: 9 });
    T(s, t, x + 0.42, y, tw - 0.5, th2, { fontSize: 9.5, valign: "middle" });
  });
}

// ================= 18 · tablero de gestión: ejemplo =================
{
  const s = newSlide(SECSF, "Tablero de gestión, un ejemplo: qué lidera SURA, qué lidera Tech and Solve y qué hacemos en conjunto",
    "Ejemplo de tablero con capacidades ilustrativas del MVP de gestores. En verde, lo que lidera SURA: propuesta, definición y certificación. En violeta, lo que lidera Tech and Solve: lista para construir, construcción y verificación. En ámbar, lo que se hace en conjunto: la liberación a producción, que aprueban el arquitecto líder y el arquitecto técnico de negocio de SURA y que el pipeline despliega de forma automática, y la observación de lo liberado. En el ejemplo, Construcción está en su límite y hay dos bloqueos: uno de un tercero en construcción y uno de SURA en certificación, que ya supera las 48 horas. Ambos se tratan en la revisión de flujo.");
  const k = 12.1 / 1180, X = (u) => M + u * k, Y = (u) => 1.5 + u * k, L = (u) => u * k;
  const colFill = (who) => who === "S" ? { fill: { color: "E8F1ED" }, line: { color: C.accent3, width: 1.25 } } : who === "D" ? { fill: { color: "F7EEDF" }, line: { color: C.accent2, width: 1.25 } } : { fill: { color: C.accent4 }, line: { color: C.accent1, width: 1 } };
  const legendBox = (x, t, kind) => {
    const st = kind === "S" || kind === "T" || kind === "D" ? colFill(kind) : { fill: kind === "block" ? { color: "F7EEDF" } : { color: C.background1 }, line: { color: kind === "block" ? C.accent2 : C.accent6, width: 1, dashType: kind === "wait" ? "dash" : "solid" } };
    s.addShape(pres.ShapeType.roundRect, Object.assign({ x: X(x), y: Y(4), w: L(22), h: L(15), rectRadius: 0.02 }, st));
    T(s, t, X(x + 30), Y(1), L(300), L(21), { fontSize: 9.5, color: C.accent6, valign: "middle" });
  };
  legendBox(2, "Lidera SURA", "S"); legendBox(132, "Lidera Tech and Solve", "T"); legendBox(318, "En conjunto", "D"); legendBox(468, "En curso", "run"); legendBox(580, "Terminado, esperando siguiente etapa", "wait"); legendBox(892, "Bloqueada", "block");
  const ex = [
    ["Propuesta", "S", "2 capacidades", false, [["Alerta de tutela", "C-21", "run"], ["Integralidad del caso", "C-22", "run"]]],
    ["Definición", "S", "3 de 6", false, [["Homologación CUPS y CIE", "C-17, 2 días", "run"], ["Score de complejidad", "C-18, 1 día", "run"], ["Coberturas", "C-19, 3 días", "wait"]]],
    ["Lista para construir", "T", "2 de 6", false, [["Duplicidad", "C-15, 1 día", "run"], ["Concepto al escalar", "C-16, 3 días", "run"]]],
    ["Construcción", "T", "4 de 4, al límite", true, [["Extractor de la orden", "C-11 · Builder 1 · 3 días", "run"], ["Request builder", "C-12 · Builder 1 · 2 días", "run"], ["Enrutador", "C-13 · Builder 2 · 4 días", "block:tercero"], ["Traza de la decisión", "C-14 · Builder 2 · 1 día", "wait"]]],
    ["Verificación", "T", "1 de 3", false, [["Clasificador", "C-10, 1 día", "run"]]],
    ["Certificación", "S", "2 de 4", false, [["Escalar a preradicado", "C-08, 1 día", "run"], ["LLM-as-a-judge", "C-09, 3 días", "block:SURA"]]],
    ["Liberada", "D", "2 esta semana", false, [["Lectura de adjuntos", "C-06, activa", "run"], ["Contrato de eventos", "C-07, sin activar", "run"]]],
    ["Estable", "D", "5 en total", false, [["Golden set de Solicitud", "C-05", "run"], ["Arquetipo de agente", "C-04", "run"], ["y 3 más", "", "more"]]],
  ];
  const cw = 144, top = 54;
  ex.forEach(([name, who, cnt, limit, cards], i) => {
    const x = 2 + i * (cw + 4);
    s.addShape(pres.ShapeType.roundRect, Object.assign({ x: X(x), y: Y(top - 20), w: L(cw), h: L(350), rectRadius: 0.06 }, colFill(who)));
    T(s, [{ text: who === "S" ? "Lidera SURA" : who === "D" ? "En conjunto" : "Lidera Tech", options: { bold: true, fontSize: 8, color: who === "S" ? C.accent3 : who === "D" ? C.accent2 : C.accent1, breakLine: true } }, { text: name, options: { bold: true, color: C.text2, breakLine: true } }, { text: cnt, options: { fontSize: 8.5, bold: limit, color: limit ? C.accent2 : C.accent6 } }], X(x + 8), Y(top - 16), L(cw - 12), L(54), { fontSize: 9.5, valign: "middle" });
    let y = top + 50;
    cards.forEach(([t, d, kind]) => {
      if (kind === "more") { T(s, t, X(x + 12), Y(y), L(cw - 20), L(20), { fontSize: 8.5, color: C.accent6 }); return; }
      const blocked = kind.startsWith("block"), two = t.length > 15, h = (blocked ? 66 : 50) + (two ? 15 : 0);
      s.addShape(pres.ShapeType.roundRect, { x: X(x + 6), y: Y(y), w: L(cw - 12), h: L(h), rectRadius: 0.04, fill: blocked ? { color: "F7EEDF" } : { color: C.background1 }, line: { color: blocked ? C.accent2 : C.accent6, width: blocked ? 1.25 : 0.75, dashType: kind === "wait" ? "dash" : "solid" } });
      const runs = [{ text: t, options: { bold: true, color: C.text2, breakLine: true } }, { text: d, options: { fontSize: 7.5, color: C.accent6, breakLine: blocked } }];
      if (blocked) runs.push({ text: "Bloqueo: " + kind.split(":")[1], options: { fontSize: 7.5, bold: true, color: C.accent2 } });
      T(s, runs, X(x + 12), Y(y + 3), L(cw - 22), L(h - 6), { fontSize: 9, valign: "middle" });
      y += h + 8;
    });
  });
  const w = (12.1 - 2 * 0.25) / 3;
  [[C.accent3, "SURA: ", "el líder funcional registra y prioriza (C-21, C-22), define las fichas con el arquitecto líder (C-17 a C-19) y certifica (C-08). C-09 supera el compromiso de 48 horas: es un bloqueo de SURA."],
   [C.accent1, "Tech and Solve: ", "los builders construyen (C-11 a C-14) y Construcción está en su límite, así que nadie toma C-15 hasta que salga una. C-13 lleva 4 días bloqueada por un tercero. Los builders verifican C-10 con IA."],
   [C.accent2, "En conjunto: ", "el arquitecto líder y el arquitecto de negocio de SURA aprobaron el paso de C-06 y C-07, y el pipeline las desplegó; SURA decide cuándo activarlas. Las capacidades estables (C-04, C-05) las observan los dos."]].forEach(([col, t, d], i) => {
    const x = M + i * (w + 0.25);
    s.addShape(pres.ShapeType.rect, { x, y: 5.6, w: 0.05, h: 1.2, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, [{ text: t, options: { bold: true, color: col } }, { text: d }], x + 0.15, 5.6, w - 0.15, 1.2, { fontSize: 9, valign: "middle" });
  });
}

// ================= 19 · compromisos de SURA =================
{
  const s = newSlide(SECSF, "Compromisos de SURA y dependencias, cada una con su dueño",
    "Los compromisos de SURA que conviene dejar por escrito: dedicación del líder funcional, respuesta a dudas en menos de 24 horas, certificación en menos de 48 horas y al menos tres ejemplos con datos. Junto a ellos, las dependencias del MVP, cada una con su dueño y con cómo evitamos que bloquee el flujo. La más importante es el ritmo de certificación; la segunda, que front, API orquestadora y SuraHis lleguen a tiempo, que cubrimos con simuladores que construye y mantiene Tech and Solve. Cada bloqueo nuevo entra al tablero con origen, fecha y responsable.");
  T(s, "Conviene dejar los compromisos por escrito en el acuerdo de trabajo. Se pactan en el arranque y se revisan en la revisión de flujo: el tiempo de SURA se mide igual que el del equipo.", M, 1.45, 12.1, 0.45, { fontSize: 11 });
  const w = (12.1 - 3 * 0.2) / 4;
  [["Dedicación del líder funcional", "Entre el 30 y el 40 % de su tiempo"], ["Respuesta a dudas", "En menos de 24 horas"], ["Certificación", "En menos de 48 horas"], ["Ejemplos para construir", "Al menos tres con datos; el resto llega en la construcción"]].forEach(([t, b], i) => {
    const x = M + i * (w + 0.2);
    card(s, x, 1.98, w, 0.82);
    dot(s, x + 0.15, 2.17, 0.42, String(i + 1), { fontSize: 12, fill: C.accent3 });
    T(s, [{ text: t, options: { bold: true, color: C.text2, breakLine: true } }, { text: b }], x + 0.65, 2.0, w - 0.75, 0.78, { fontSize: 10, valign: "middle" });
  });
  T(s, "Dependencias y cómo evitamos que nos bloqueen", M, 2.95, 12.1, 0.32, { fontSize: 12.5, bold: true, color: C.text2 });
  sfTable(s, ["Dependencia", "Dueño", "Riesgo si se demora", "Cómo la cuidamos"], [
    ["Certificación al ritmo de las entregas", "Líder funcional de SURA", "Capacidades represadas en QA", "Acuerdo de 48 h, límite de 4 en certificación y bloqueos de SURA a la vista"],
    ["Front Angular y canales", "Equipos de front de SURA", "Lo construido no se ve de punta a punta", "Contrato del arranque; construimos y verificamos contra el simulador"],
    ["API orquestadora de cada gestor", "Equipos de integración de SURA", "El agente no recibe ni entrega en el gestor real", "Simulador que mantiene Tech; se cambia por la API real sin tocar el agente"],
    ["Core SuraHis: reglas, histórico y gateways", "Equipo del core de SURA", "Reglas o datos distintos a los supuestos", "Simulador con casos reales anonimizados; el golden set detecta diferencias al integrar"],
    ["Accesos, ambientes y plataforma agéntica", "Arquitecto técnico de negocio de SURA", "El arranque no cierra", "Condición de salida del arranque; solo herramientas que SURA autorice"],
    ["Muestra clínica anonimizada y expertos", "Negocio y equipo médico de SURA", "Juez sin calibrar y pertinencia sin validar", "Evaluación dentro de la infraestructura de SURA (lámina 11)"],
  ], { y: 3.35, colW: [2.9, 2.5, 2.5, 4.2], rowH: [0.32].concat(Array(6).fill(0.5)), fs: 9.5 });
}

// ================= 20 · por qué Tech and Solve =================
pres.addSection({ title: SEC4 });
{
  const s = newSlide(SEC4, "Tech and Solve: más que tecnología, resultados sostenibles para SURA",
    "Cierre de la propuesta. Resume la propuesta: Tech and Solve Spec Flow con SURA, con la IA de Tech and Solve integrada en todo el flujo. El argumento más fuerte es que ya conocemos la arquitectura de gestores por el trabajo previo con SURA.");
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 1.75, w: 3.7, h: 4.7, rectRadius: 0.1, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, "Un equipo que combina visión de negocio, excelencia técnica e IA generativa propia para acelerar resultados medibles y sostenibles.", M + 0.3, 2.0, 3.1, 2.3, { fontSize: 17, bold: true, color: C.background1, fontFace: "+mj-lt" });
  T(s, "Conocemos la arquitectura de gestores, trabajamos en flujo continuo con SURA y construimos con una IA propia que acelera sin perder control.", M + 0.3, 4.35, 3.1, 1.95, { fontSize: 13, color: C.background2 });
  const why = [["Capacidades distintivas", "Expertos en sistemas agénticos y arquitectura de gestores."], ["IA: procesos medibles", "IA propia que acelera cada liberación con validación humana."], ["Equipo: estructura flexible", "Equipo ágil con arquitecto y desarrolladores dedicados."], ["Talento consultivo", "Experiencia previa con SURA, mirada crítica de negocio y acompañamiento cercano."], ["Medición integral", "Garantías verificables en calidad, performance y seguridad."]];
  const gx = M + 3.9, cw = (12.1 - 3.9 - 0.2) / 2, ch = 1.45;
  why.forEach(([t, d], i) => {
    const wide = i === 4;
    const x = gx + (wide ? 0 : (i % 2) * (cw + 0.2)), y = 1.75 + Math.floor(i / 2) * (ch + 0.175), w = wide ? 2 * cw + 0.2 : cw;
    card(s, x, y, w, ch);
    dot(s, x + 0.2, y + 0.18, 0.42, String(i + 1), { fontSize: 12 });
    T(s, t, x + 0.75, y + 0.15, w - 0.9, 0.48, { fontSize: 14, bold: true, color: C.text2, valign: "middle" });
    T(s, d, x + 0.2, y + 0.7, w - 0.4, ch - 0.75, { fontSize: 12 });
  });
}

// ---------- tema ----------
// pptxgenjs escribe la paleta de Office en el tema; aquí se reemplaza por la de Tech and Solve
// para que los colores de esquema (C.text2, C.accent1, ...) resuelvan a la marca.
async function aplicarTema(file, theme) {
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const partes = Object.keys(zip.files).filter((p) => /^ppt\/theme\/theme\d+\.xml$/.test(p));
  for (const p of partes) {
    let xml = await zip.file(p).async("string");
    for (const [k, v] of Object.entries(theme.colors)) {
      if (!/^[0-9A-F]{6}$/i.test(v)) throw new Error(`Color inválido para ${k}: ${v}`);
      xml = xml.replace(new RegExp(`<a:${k}>[\\s\\S]*?</a:${k}>`), `<a:${k}><a:srgbClr val="${v}"/></a:${k}>`);
    }
    xml = xml.replace(/<a:clrScheme name="[^"]*"/, `<a:clrScheme name="${theme.name}"`);
    zip.file(p, xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await aplicarTema(OUT, THEME);
  console.log("Generado:", OUT);
})();
