// Generador del .pptx de la presentación del equipo para SURA.
// El HTML de la carpeta de arriba es la fuente de verdad: todo cambio se hace allá primero
// y luego se refleja aquí. Uso: ver README.md.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
// Imágenes de marca y fotos del equipo, ya recortadas (ver README.md).
const ASSETS = path.join(__dirname, "assets");
// El .pptx se escribe junto al HTML, en la carpeta de arriba.
const OUT = path.join(__dirname, "..", "Tech and Solve - Dinámica de trabajo del equipo.pptx");
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
function source(slide, runs) {
  T(slide, runs, M, 6.5, 12.1, 0.4, { fontSize: 11, color: C.accent6, valign: "bottom" });
}
const link = (text, url) => ({ text, options: { hyperlink: { url }, color: C.accent1, underline: { style: "sng" } } });
const H = (slide, text) => slide.addText(text, { placeholder: "title" });
function newSlide(section, title, notes) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: section });
  H(s, title);
  if (notes) s.addNotes(notes);
  return s;
}

const IMG = (n) => "image/jpeg;base64," + fs.readFileSync(path.join(ASSETS, "p_" + n + ".jpg")).toString("base64");
const PHOTO = "image/jpeg;base64," + fs.readFileSync(path.join(ASSETS, "p_didier.jpg")).toString("base64");
// ===== Generador alineado con el HTML vigente (21 láminas) =====
const SEC1 = "Dinámica de trabajo", SEC2 = "IA de Tech and Solve";
const tblBase = (o) => Object.assign({ border: { type: "solid", pt: 1, color: BORDER }, fill: { color: C.accent4 }, valign: "middle" }, o);
const th = (t, fill, o = {}) => ({ text: t, options: Object.assign({ bold: true, color: C.background1, fill: { color: fill || C.text2 }, valign: "middle" }, o) });
const chipRow = (s, items, x, y, maxW, o) => {
  let cx = x, cy = y;
  items.forEach((t) => {
    const w = t.length * o.cw + 0.45;
    if (cx + w > x + maxW) { cx = x; cy += o.h + 0.12; }
    s.addShape(pres.ShapeType.roundRect, { x: cx, y: cy, w, h: o.h, rectRadius: o.h / 2, fill: { color: o.fill }, line: { color: o.fill, width: 0 } });
    T(s, t, cx, cy, w, o.h, { align: "center", valign: "middle", fontSize: o.fs, bold: true, color: o.color });
    cx += w + 0.12;
  });
};
const violetSlide = (section) => {
  const s = pres.addSlide({ masterName: "TITULO", sectionTitle: section });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  return s;
};
const logoBox = (s, x, y) => {
  s.addShape(pres.ShapeType.roundRect, { x, y, w: 1.9, h: 1.0, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: C.background1, width: 0 } });
  s.addImage({ data: LOGO, x: x + 0.12, y: y + 0.08, w: 1.66, h: 0.87 });
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
  T(s, "PROPUESTA PARA SURA", 0.8, 2.45, 8, 0.35, { fontSize: 13, bold: true, color: C.background2, charSpacing: 3 });
  s.addText("MVP de Gestores", { x: 0.8, y: 2.85, w: 11, h: 1.05, fontSize: 50, bold: true, color: C.background1, fontFace: "+mj-lt", valign: "top", margin: 0, isTextBox: true });
  [["1", "Equipo Tech and Solve"], ["2", "IA de Tech and Solve"]].forEach(([n, t], i) => {
    const y = 4.2 + i * 0.65;
    s.addShape(pres.ShapeType.ellipse, { x: 0.8, y, w: 0.46, h: 0.46, fill: { color: C.background1 }, line: { color: C.background1, width: 0 } });
    T(s, n, 0.8, y, 0.46, 0.46, { align: "center", valign: "middle", bold: true, fontSize: 14, color: C.text2 });
    T(s, t, 1.45, y - 0.04, 9, 0.54, { valign: "middle", bold: true, fontSize: 20, color: C.background1 });
  });
  [["raul", "Raúl A. De Villa C.", "Co-Founder · Director de soluciones digitales para seguros"], ["alexandra", "Alexandra Acosta", "Gerente de Éxito del Cliente"], ["jorge", "Jorge Andrés Gómez Velásquez", "Líder del Éxito del Cliente"], ["didier", "Didier Fabián Franco Gómez", "Líder de Comunidad · Arquitecto de la propuesta"]].forEach(([k, n, r], i) => {
    personCard(s, 8.05, 0.55 + i * 1.36, 4.48, 1.22, { img: IMG(k), name: n, role: r });
  });
  s.addShape(pres.ShapeType.line, { x: 0.8, y: 6.2, w: 11.73, h: 0, line: { color: C.background2, width: 0.75, transparency: 60 } });
  T(s, "SURA Colombia · Transformación prestación y reclamaciones\nMVP de autorizaciones de salud", 0.8, 6.32, 6.5, 0.6, { fontSize: 11, color: C.background2 });
  T(s, "Tech and Solve · Octubre de 2026\nDocumento confidencial", 7.3, 6.32, 5.23, 0.6, { fontSize: 11, color: C.background2, align: "right" });
  s.addNotes("Portada de la propuesta: qué equipo proponemos, cómo trabajaría con SURA y qué lo diferencia.");
}

// ================= 2 · portada de la dinámica =================
pres.addSection({ title: SEC1 });
{
  const s = pres.addSlide({ masterName: "TITULO", sectionTitle: SEC1 });
  s.addShape(pres.ShapeType.rect, { x: 8.6, y: 0, w: 4.733, h: 7.5, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  s.addImage({ data: LOGO, x: 0.8, y: 0.7, w: 1.9, h: 0.995 });
  s.addText("Equipo Tech and Solve", { x: 0.8, y: 2.35, w: 7.4, h: 1.7, fontSize: 40, bold: true, color: C.text2, fontFace: "+mj-lt", valign: "top", margin: 0, isTextBox: true });
  T(s, "Dos desarrolladores construyen los sistemas agénticos del MVP de gestores, con un arquitecto que define el cómo y lo revisa, por sprints y potenciados por la IA generativa propia de Tech and Solve.", 0.8, 4.2, 7.2, 1.5, { fontSize: 19, color: C.accent6 });
  T(s, "Tech and Solve · SURA, MVP de gestores de autorizaciones de salud\nOctubre de 2026 · Sugerencia de trabajo, debatible y ajustable", 0.8, 6.3, 7.4, 0.7, { fontSize: 13, color: C.accent6 });
  const team = [
    { img: IMG("raul"), name: "Raúl A. De Villa C.", role: "Co-Founder · Acompaña los hitos clave con una mirada crítica de negocio y de solución.", h: 0.86 },
    { img: IMG("alexandra"), name: "Alexandra Acosta", role: "Gerente de Éxito del Cliente · Pone al servicio de SURA la experiencia y los estándares de toda la compañía.", h: 0.86 },
    { img: IMG("jorge"), name: "Jorge Andrés Gómez Velásquez", role: "Líder del Éxito del Cliente · Punto de contacto con SURA: lo acordado, con calidad y a tiempo.", h: 0.86 },
    { img: IMG("didier"), name: "Didier Fabián Franco Gómez", role: "Arquitecto · parcial. Marca el rumbo técnico con el equipo, lo alinea con la arquitectura de SURA y asegura que cada historia lo cumpla.", h: 1.42 },
    { initial: "A", name: "Desarrollador A", role: "Construye los sistemas agénticos desde un backlog compartido", h: 0.78 },
    { initial: "B", name: "Desarrollador B", role: "Construye los sistemas agénticos desde un backlog compartido", h: 0.78 },
  ];
  let ty = 0.55;
  team.forEach((o) => { personCard(s, 8.95, ty, 3.95, o.h, Object.assign({ d: 0.62, nfs: 11.5, rfs: 9.5 }, o)); ty += o.h + 0.1; });
  s.addNotes("El equipo construye los sistemas agénticos; el front y la integración los lideran los equipos de SURA. Trabaja por sprints: SURA define las historias y recibe cada demo. Todo lo que sigue es una sugerencia de trabajo.");
}

// ================= 6 · roles =================
{
  const s = newSlide(SEC1, "Equipo de trabajo propuesto: modelo Tech and Solve y SURA",
    "El liderazgo de Tech and Solve acompaña de forma puntual: Raúl en los hitos clave, con una mirada crítica de negocio y de solución; Alexandra, con la experiencia y los estándares de toda la compañía; y Jorge, como punto de contacto con SURA para que cada sprint cumpla lo acordado. El arquitecto define el cómo, se alinea con el equipo de arquitectura de SURA y revisa. Los desarrolladores participan en el refinamiento y la estimación, y luego implementan la solución. Trabajan sobre el mismo backlog y cada uno toma la siguiente historia priorizada; no hay frentes repartidos.");
  const lw = 7.9;
  // Acompañamiento puntual
  card(s, M, 1.62, lw, 1.5, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "LIDERAZGO QUE ACOMPAÑA · DEDICACIÓN PUNTUAL", M + 0.25, 1.7, lw - 0.5, 0.25, { fontSize: 9.5, bold: true, color: C.text2, charSpacing: 1 });
  const mw = (lw - 0.5 - 0.3) / 3;
  [["raul", "Raúl A. De Villa C.", "Co-Founder", "Acompaña los hitos clave con una mirada crítica de negocio y de solución."], ["alexandra", "Alexandra Acosta", "Gerente de Éxito del Cliente", "Pone al servicio de SURA la experiencia y los estándares de toda la compañía."], ["jorge", "Jorge A. Gómez Velásquez", "Líder del Éxito del Cliente", "Punto de contacto con SURA: lo acordado, con calidad y a tiempo."]].forEach(([k, n, r, d], i) => {
    const x = M + 0.25 + i * (mw + 0.15), y = 2.0;
    personCard(s, x, y, 0.55, 0.55, { light: true, img: IMG(k), name: "", d: 0.52 });
    T(s, [{ text: n, options: { bold: true, color: C.text2, fontSize: 10, breakLine: true } }, { text: r, options: { bold: true, color: C.accent2, fontSize: 8.5 } }], x + 0.62, y - 0.02, mw - 0.62, 0.58, { valign: "middle" });
    T(s, d, x, y + 0.6, mw, 0.45, { fontSize: 9.5 });
  });
  // Arquitecto
  card(s, M, 3.22, lw, 1.0);
  personCard(s, M + 0.2, 3.36, 0.72, 0.72, { light: true, img: IMG("didier"), name: "", d: 0.72 });
  T(s, [{ text: "Didier Fabián Franco Gómez", options: { bold: true, color: C.text2, fontSize: 13 } }, { text: "  · Arquitecto, parcial", options: { bold: true, color: C.accent2, fontSize: 11 } }], M + 1.08, 3.28, lw - 1.25, 0.32, {});
  T(s, "Marca el rumbo técnico: define con el equipo prácticas, arquetipos y componentes, los alinea con la arquitectura de SURA y asegura que cada historia los cumpla.", M + 1.08, 3.6, lw - 1.25, 0.58, { fontSize: 11 });
  // Desarrolladores
  card(s, M, 4.32, lw, 2.13);
  dot(s, M + 0.22, 4.44, 0.42, "A", { fontSize: 12 });
  dot(s, M + 0.72, 4.44, 0.42, "B", { fontSize: 12 });
  T(s, "Desarrolladores · dedicación completa", M + 1.3, 4.44, 5, 0.42, { fontSize: 15, bold: true, color: C.text2, valign: "middle" });
  const sw = (lw - 0.44 - 0.24) / 3;
  [["1 · Refinan", "Bajan cada historia a diseño técnico con el arquetipo, junto al arquitecto."], ["2 · Estiman", "Ponen los puntos de cada historia y la parten si pasa de 13."], ["3 · Implementan", "Construyen la solución con las prácticas del equipo y la dejan lista para revisión."]].forEach(([t, b], i) => {
    const x = M + 0.22 + i * (sw + 0.12);
    card(s, x, 4.97, sw, 0.98, { fill: { color: C.background1 } });
    T(s, [{ text: t, options: { bold: true, color: C.accent1, breakLine: true } }, { text: b }], x + 0.12, 5.02, sw - 0.24, 0.9, { fontSize: 10.5 });
  });
  T(s, [{ text: "Un equipo, un backlog: ", options: { bold: true, color: C.text2 } }, { text: "siempre se trabaja en la prioridad más alta de SURA, y el conocimiento queda en el equipo, no en una persona." }], M + 0.22, 6.0, lw - 0.44, 0.4, { fontSize: 10.5, color: C.accent6, valign: "middle" });
  const x0 = 8.9, wr = 3.83;
  T(s, "Equipo SURA", x0, 1.75, wr, 0.4, { fontSize: 17, bold: true, color: C.text2 });
  [["Product Owner de SURA", "define y prioriza las historias, y recibe cada demo"], ["Arquitectura de SURA", "acuerda lineamientos y decisiones con nuestro arquitecto"], ["Equipos de front e integración", "construyen la base donde se integran los agentes"], ["Core SuraHis y plataforma agéntica", "exponen reglas, histórico, gateways y modelos"], ["Negocio y equipo médico", "definen el error tolerable y validan la muestra clínica"]].forEach(([a, b], i) => {
    const y = 2.25 + i * 0.84;
    card(s, x0, y, wr, 0.74, { fill: { color: C.background1 } });
    T(s, [{ text: a, options: { bold: true, color: C.text2, breakLine: true } }, { text: b, options: { color: C.accent6 } }], x0 + 0.15, y, wr - 0.3, 0.74, { fontSize: 12, valign: "middle" });
  });
}

// ================= 3 · diez etapas =================
{
  const s = newSlide(SEC1, "Diez etapas: SURA define al inicio y recibe al cierre de cada sprint",
    "Las diez etapas de nuestro proceso de desarrollo ágil. Las etapas 1 y 2 preparan el trabajo con SURA; de la 3 a la 8 es el sprint, que se repite; 9 y 10 llevan el resultado a producción. Dentro del sprint todo es interno salvo la demo.");
  const zone = (x, w, label, fill, txtCol) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.75, w, h: 3.95, rectRadius: 0.08, fill: { color: fill }, line: { color: BORDER, width: 1 } });
    T(s, label, x + 0.2, 1.88, w - 0.4, 0.35, { fontSize: 14, bold: true, color: txtCol });
  };
  const stage = (x, y, w, n, t, sub, col) => {
    card(s, x, y, w, 0.95, { fill: { color: C.background1 } });
    dot(s, x + 0.15, y + 0.22, 0.5, n, { fontSize: 13, fill: col });
    T(s, t, x + 0.78, y + 0.1, w - 0.9, 0.35, { fontSize: 14, bold: true, color: C.text2 });
    T(s, sub, x + 0.78, y + 0.46, w - 0.9, 0.42, { fontSize: 12, color: C.accent6 });
  };
  zone(M, 3.0, "Con SURA · definir", C.background2, C.text2);
  stage(M + 0.2, 2.35, 2.6, "1", "Descubrimiento", "Objetivo, alcance y reglas", C.accent2);
  stage(M + 0.2, 3.45, 2.6, "2", "Backlog", "Épicas e historias priorizadas", C.accent2);
  const mx = 3.8, mw = 5.55, cw = 2.6;
  zone(mx, mw, "El sprint · interno del equipo, se repite cada 10 días", C.accent4, C.accent1);
  stage(mx + 0.15, 2.35, cw, "3", "Refinamiento", "Diseño técnico y puntos", C.accent1);
  stage(mx + 0.3 + cw, 2.35, cw, "4", "Planificación", "Objetivo del sprint", C.accent1);
  stage(mx + 0.15, 3.45, cw, "5", "Desarrollo", "Código, pruebas y revisión", C.accent1);
  stage(mx + 0.3 + cw, 3.45, cw, "6", "Integración", "Continua: cada cambio se verifica", C.accent1);
  stage(mx + 0.15, 4.55, cw, "8", "Retrospectiva", "Un acuerdo de mejora", C.accent1);
  T(s, "La daily acompaña todo el sprint.", mx + 0.45 + cw, 4.6, cw - 0.2, 0.85, { fontSize: 13, color: C.accent6, valign: "middle" });
  const rx = 9.6, rw = 3.13;
  zone(rx, rw, "Con SURA · ver y recibir", C.background2, C.text2);
  stage(rx + 0.2, 2.35, rw - 0.4, "7", "Revisión y demo", "Al cierre de cada sprint", C.accent3);
  stage(rx + 0.2, 3.45, rw - 0.4, "9", "Despliegue", "Entrega del incremento", C.accent3);
  stage(rx + 0.2, 4.55, rw - 0.4, "10", "Operación", "Uso real y soporte", C.accent3);
  s.addShape(pres.ShapeType.leftArrow, { x: M, y: 5.88, w: 12.1, h: 0.6, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Lo que se aprende en la demo y en la operación vuelve al backlog, y se prioriza con SURA", M + 0.8, 5.88, 11.0, 0.6, { fontSize: 14, bold: true, color: C.text2, valign: "middle", align: "center" });
  source(s, [
    { text: "Práctica de industria, no norma ni requisito: los cuatro valores del " },
    link("Manifiesto por el Desarrollo Ágil de Software", "https://agilemanifesto.org/iso/es/manifesto.html"),
    { text: " (agilemanifesto.org), que son individuos e interacciones, software funcionando, colaboración con el cliente y respuesta ante el cambio." },
  ]);
}

// ================= 5 · alcance =================
{
  const s = newSlide(SEC1, "Construimos los sistemas agénticos; el front y la integración los lideran los equipos de SURA",
    "El equipo construye los agentes y lo que los gobierna.");
  const w = 5.95;
  card(s, M, 1.75, w, 4.6, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Lo construye este equipo", M + 0.3, 1.95, w - 0.6, 0.4, { fontSize: 17, bold: true, color: C.text2 });
  T(s, [
    { text: "Los agentes", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Clasificador, enrutador, extractores, request builder, LLM-as-a-judge, pertinencia médica, duplicidad, concepto al escalar y auditor.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true, fontSize: 7 } },
    { text: "Lo que los gobierna", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Golden set, compuerta, traza de la decisión, umbrales, calibración del juez y techos de autonomía.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true, fontSize: 7 } },
    { text: "La base de la torre de control", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Contrato de eventos y torre de control, capas 1 y 2." },
  ], M + 0.3, 2.5, w - 0.6, 3.7, { fontSize: 14 });
  const x2 = M + w + 0.2;
  card(s, x2, 1.75, w, 4.6);
  T(s, "Lo lideran los equipos de SURA", x2 + 0.3, 1.95, w - 0.6, 0.4, { fontSize: 17, bold: true, color: C.accent6 });
  const others = ["Front Angular y canales", "API orquestadora de cada gestor e integración con el core", "Plataforma habilitadora y plataforma agéntica"];
  T(s, others.map((o, k) => ({ text: o, options: { bullet: true, breakLine: k < others.length - 1, paraSpaceAfter: 10 } })), x2 + 0.3, 2.55, w - 0.6, 3.6, { fontSize: 15 });
  source(s, [{ text: "Los agentes se integran sobre lo que construyen los equipos de SURA; el contrato entre ambos se acuerda en el arranque." }]);
}

// ================= 7 · arquitecto =================
{
  const s = newSlide(SEC1, "El arquitecto define el cómo, se alinea con SURA y revisa que se cumpla",
    "El arquitecto no implementa historias: define con el equipo cómo se construye, lo alinea con el equipo de arquitectura de SURA y revisa que el equipo lo cumpla.");
  const cols = [
    ["1", "Define con el equipo", C.accent1, ["Arquitectura evolutiva: la de cada sistema agéntico se define al empezar su implementación.", "Buenas prácticas de construcción y de prompts.", "Arquetipo de agente: grafo, golden set, compuerta y traza.", "Componentes reutilizables entre gestores.", "Lineamientos y un estándar técnico verificable."]],
    ["2", "Se alinea con el equipo de arquitectura de SURA", C.accent3, ["Lineamientos AI First de la organización.", "Contrato del agente con cada gestor.", "Autonomía y techos de cada agente: ninguno niega.", "Criterio de acierto y umbral del error caro."]],
    ["3", "Revisa que se cumpla", C.accent2, ["Diseño de cada historia, en el refinamiento.", "Código que toca contratos, traza y medición.", "Lo que no falla de forma ruidosa: acierto y deriva.", "Ajusta los lineamientos en la retro."]],
  ];
  const w = 3.85, g = 0.275;
  cols.forEach(([n, t, col, items], i) => {
    const x = M + i * (w + g);
    card(s, x, 1.7, w, 4.05);
    dot(s, x + 0.3, 1.9, 0.5, n, { fontSize: 14, fill: col });
    T(s, t, x + 0.95, 1.85, w - 1.15, 0.65, { fontSize: 14, bold: true, color: C.text2, valign: "middle" });
    T(s, items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1, paraSpaceAfter: 6 } })), x + 0.3, 2.65, w - 0.6, 3.0, { fontSize: 13 });
  });
  card(s, M, 5.9, 12.1, 0.62, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "El equipo implementa las historias con esas prácticas ", options: { bold: true, color: C.text2 } }, { text: "y decide en el sprint lo fácil de cambiar: la estructura interna del grafo, la redacción del prompt y el orden de las tareas." }], M + 0.3, 5.9, 11.5, 0.62, { fontSize: 13, valign: "middle" });
}

// ================= 9 · historias =================
{
  const s = newSlide(SEC1, "Las historias de usuario se escriben con SURA",
    "La sesión de historias es el espacio de SURA dentro de la iteración. De ahí sale la historia con su criterio de aceptación; el equipo la estima en puntos y resuelve el detalle técnico en el refinamiento interno.");
  card(s, M, 1.75, 5.2, 4.7, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "Qué trae cada historia", M + 0.3, 1.95, 4.6, 0.4, { fontSize: 17, bold: true, color: C.text2 });
  [["Quién", "el rol que usa lo que el agente produce"], ["Qué y para qué", "lo que necesita y el valor que gana, en palabras del negocio"], ["Criterios de aceptación", "cómo se sabe en la demo que está bien"], ["Casos del golden set", "los ejemplos con respuesta conocida que la prueban"], ["Puntos", "los pone el equipo; más de 13 se parte"]].forEach(([a, b], i) => {
    T(s, [{ text: a, options: { bold: true, color: C.accent1, breakLine: true } }, { text: b }], M + 0.3, 2.5 + i * 0.75, 4.6, 0.7, { fontSize: 14 });
  });
  const ex = 6.1, ew = 6.63;
  card(s, ex, 1.75, ew, 4.7);
  s.addShape(pres.ShapeType.roundRect, { x: ex + 0.3, y: 1.98, w: 3.6, h: 0.42, rectRadius: 0.21, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 } });
  T(s, "Ejemplo · Gestor de Evaluación", ex + 0.3, 1.98, 3.6, 0.42, { align: "center", valign: "middle", fontSize: 13, bold: true, color: C.background1 });
  T(s, [
    { text: "Como ", options: { color: C.accent6 } }, { text: "evaluador de la bandeja", options: { bold: true, color: C.text2 } },
    { text: ", quiero ", options: { color: C.accent6 } }, { text: "que la solicitud escalada llegue con el concepto del agente", options: { bold: true, color: C.text2 } },
    { text: ", para ", options: { color: C.accent6 } }, { text: "no empezar la revisión de cero.", options: { bold: true, color: C.text2 } },
  ], ex + 0.3, 2.6, ew - 0.6, 1.1, { fontSize: 17 });
  T(s, "Criterios de aceptación", ex + 0.3, 3.8, ew - 0.6, 0.35, { fontSize: 14, bold: true, color: C.accent2 });
  const crit = ["El concepto dice qué se evaluó, contra qué regla y con qué confianza.", "Dice por qué escala; ningún caso se niega de forma automática.", "La decisión queda en la traza con agente, versión y umbral.", "Los casos de escalamiento del golden set pasan sin regresión."];
  T(s, crit.map((c, k) => ({ text: c, options: { bullet: true, breakLine: k < crit.length - 1, paraSpaceAfter: 4 } })), ex + 0.3, 4.2, ew - 0.6, 2.1, { fontSize: 14 });
}

// ================= 8 · épicas e historias =================
{
  const s = newSlide(SEC1, "Las épicas tienen talla; las historias, puntos",
    "Las tallas que existen hoy son de épicas y sirven para ordenar el backlog. De cada épica se desprenden historias de usuario, que el equipo estima en puntos, y el sprint se llena según la velocidad del equipo.");
  const steps = [
    ["Épica", "talla", "La talla S, M, L o XL que ya tiene cada épica. Sirve para ordenar el backlog, no para planear el sprint.", C.text2],
    ["Historias de usuario", "puntos", "Se desprenden de la épica con SURA, y el equipo las estima en puntos: 1, 2, 3, 5, 8 o 13. Una de más de 13 se parte.", C.accent1],
    ["Sprint", "velocidad", "Entra lo que cabe en la velocidad del equipo: los puntos que de verdad termina por sprint.", C.accent3],
  ];
  const w = 3.7, g = 0.5;
  steps.forEach(([t, sub, b, col], i) => {
    const x = M + i * (w + g);
    card(s, x, 1.75, w, 2.45);
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.25, y: 1.95, w: w - 0.5, h: 0.5, rectRadius: 0.06, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, [{ text: t, options: { bold: true } }, { text: "  ·  " + sub }], x + 0.25, 1.95, w - 0.5, 0.5, { align: "center", valign: "middle", fontSize: 15, color: C.background1 });
    T(s, b, x + 0.25, 2.6, w - 0.5, 1.5, { fontSize: 14 });
    if (i < 2) s.addShape(pres.ShapeType.rightArrow, { x: x + w + 0.08, y: 2.75, w: 0.34, h: 0.45, fill: { color: C.accent5 }, line: { color: C.accent5, width: 0 } });
  });
  card(s, M, 4.45, 12.1, 2.0, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "Ejemplo · ", options: { bold: true, color: C.accent1 } }, { text: "épica de pertinencia médica, talla XL, en el Gestor de Evaluación", options: { bold: true, color: C.text2 } }], M + 0.3, 4.6, 11.5, 0.4, { fontSize: 15 });
  const hs = [["Coherencia entre orden e historia clínica", "8"], ["Validación de CIE-10 y CUPS", "5"], ["Score de complejidad del caso", "5"], ["Concepto del agente al escalar", "3"]];
  const hw = 2.8, hg = 0.17;
  hs.forEach(([t, p], i) => {
    const x = M + 0.3 + i * (hw + hg);
    card(s, x, 5.1, hw, 1.15, { fill: { color: C.background1 } });
    T(s, t, x + 0.15, 5.18, hw - 0.95, 1.0, { fontSize: 13, valign: "middle" });
    dot(s, x + hw - 0.75, 5.37, 0.6, p, { fontSize: 16 });
  });
  T(s, "Puntos ilustrativos: los asigna el equipo en el refinamiento técnico.", M, 6.5, 12.1, 0.35, { fontSize: 11, color: C.accent6, valign: "bottom" });
}

// ================= 14 · lista y hecha =================
{
  const s = newSlide(SEC1, "Cuándo entra una historia al sprint y cuándo se da por hecha",
    "Incluye lo propio de los agentes, golden set y traza, y lo que exige nuestro proceso de desarrollo con IA: especificación mínima antes de generar código.");
  const cols = [["Lista para entrar al sprint", C.accent1, ["Se definió con SURA y tiene su criterio de aceptación.", "El contrato del agente con el gestor está acordado: qué recibe, qué entrega y cómo escala.", "Hay una especificación mínima versionada antes de generar código.", "El golden set tiene casos que la prueban.", "Tiene puntos del equipo; una de más de 13 se parte."]], ["Hecha", C.accent3, ["Sigue el arquetipo y los lineamientos del equipo.", "Funciona integrada al gestor o contra su simulador.", "Deja la traza: agente, versión, prompt, umbral y confianza.", "Su golden set corre en la compuerta sin regresión.", "La revisó el arquitecto o una persona distinta del autor."]]];
  cols.forEach(([t, col, items], i) => {
    const x = M + i * 6.15, w = 5.95;
    card(s, x, 1.75, w, 4.7);
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.3, y: 1.97, w: 3.4, h: 0.48, rectRadius: 0.24, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, t, x + 0.3, 1.97, 3.4, 0.48, { align: "center", valign: "middle", fontSize: 15, bold: true, color: C.background1 });
    T(s, items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1, paraSpaceAfter: 8 } })), x + 0.3, 2.65, w - 0.6, 3.7, { fontSize: 15 });
  });
}

// ================= 10 · sprint =================
{
  const s = newSlide(SEC1, "Un sprint de diez días hábiles: tres sesiones con SURA; el resto, implementación interna del equipo tech",
    "Diez días hábiles es el sprint estándar de SuraHis y es lo que fija la hoja de seguimiento. SURA participa en tres sesiones: la alineación del arquitecto con el equipo de arquitectura de SURA, la sesión de historias y la demo con entrega. Las duraciones son sugeridas.");
  const dw = 1.12, dg = 0.1, y0 = 1.95;
  for (let i = 0; i < 10; i++) {
    const x = M + i * (dw + dg);
    s.addShape(pres.ShapeType.roundRect, { x, y: y0, w: dw, h: 0.45, rectRadius: 0.06, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
    T(s, "Día " + (i + 1), x, y0, dw, 0.45, { align: "center", valign: "middle", fontSize: 12, bold: true, color: C.text2 });
  }
  const bar = (label, d0, d1, y, fill) => {
    const x = M + d0 * (dw + dg), w = (d1 - d0 + 1) * dw + (d1 - d0) * dg;
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.42, rectRadius: 0.06, fill: { color: fill }, line: { color: fill, width: 0 } });
    T(s, label, x + 0.06, y, w - 0.12, 0.42, { align: "center", valign: "middle", fontSize: 11, bold: true, color: C.background1 });
  };
  bar("Daily · 15 min, todos los días", 0, 9, 2.55, C.accent1);
  bar("Planning · 2 h", 0, 1, 3.05, C.accent1);
  bar("Arquitectura SURA · 1 h", 2, 3, 3.05, C.accent3);
  bar("Historias con SURA · 1,5 h", 4, 5, 3.05, C.accent3);
  bar("Refinamiento técnico · 1 h", 6, 7, 3.05, C.accent1);
  bar("Demo y entrega · 1 h", 8, 9, 3.05, C.accent3);
  bar("Retro interna · 45 min", 8, 9, 3.55, C.accent1);
  [[M, C.accent1, "Interna del equipo"], [M + 3.0, C.accent3, "Con SURA"]].forEach(([x, col, t]) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 4.17, w: 0.3, h: 0.22, rectRadius: 0.04, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, t, x + 0.4, 4.1, 2.5, 0.36, { fontSize: 12, color: C.accent6, valign: "middle" });
  });
  const cards = [["Arquitectura SURA", "El arquitecto lleva lineamientos y decisiones, y trae lo que SURA define.", C.accent3], ["Historias con SURA", "Las historias del siguiente sprint se desprenden de las épicas y se priorizan.", C.accent3], ["Refinamiento técnico", "El equipo aplica el arquetipo, estima en puntos y parte en tareas de un día o menos.", C.accent1], ["Demo y entrega", "SURA ve la demo y recibe las historias con su estado y sus evidencias. Después, la retro interna.", C.accent3]];
  const cw = 2.9, cg = 0.167;
  cards.forEach(([t, b, col], i) => {
    const x = M + i * (cw + cg);
    card(s, x, 4.6, cw, 1.75);
    T(s, t, x + 0.2, 4.72, cw - 0.4, 0.4, { fontSize: 14, bold: true, color: col });
    T(s, b, x + 0.2, 5.12, cw - 0.4, 1.2, { fontSize: 13 });
  });
  source(s, [{ text: "Adaptación propia de la " }, link("Guía de Scrum 2020", "https://scrumguides.org/scrum-guide.html"), { text: " (scrumguides.org), práctica de industria y no norma: de ella tomamos el sprint de duración fija y sus eventos. A diferencia de la guía, el Product Owner no asiste a la planning ni a la retro." }]);
}

// ================= 11 · quién hace qué =================
{
  const s = newSlide(SEC1, "Qué hace cada quien en cada momento");
  const c = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 11, valign: "middle" }, o) });
  const off = (t = "No requiere tiempo de SURA") => c(t, { italic: true, color: C.accent6 });
  const mom = (t, sura) => ({ text: [{ text: t, options: { bold: true, color: C.text2, breakLine: true } }, { text: sura ? "Con SURA" : "Interna tech", options: { fontSize: 9, bold: true, color: sura ? C.accent3 : C.accent6 } }], options: { fill: { color: C.background2 }, valign: "middle", fontSize: 11 } });
  const rows = [
    [mom("Arquitectura SURA", true), c("Lleva lineamientos y decisiones; trae lo que SURA define."), off("Reciben los acuerdos en el refinamiento."), c("Arquitectura de SURA: valida lineamientos y decisiones.")],
    [mom("Historias con SURA", true), c("Cuida que cada historia se pueda partir, probar y medir."), c("Preguntan hasta entender el criterio de aceptación."), c("Product Owner: define y prioriza las historias del siguiente sprint.")],
    [mom("Refinamiento técnico"), c("Lidera: aplica el arquetipo y los lineamientos a cada historia."), c("Bajan las historias a diseño técnico."), off()],
    [mom("Estimación"), c("Cuida que los puntos reflejen el arquetipo y sus riesgos."), c("Ponen los puntos y parten lo que pasa de 13."), off()],
    [mom("Planning"), c("Señala qué lineamientos y contratos entran en juego."), c("Eligen las historias según su velocidad y se comprometen."), off()],
    [mom("Daily e implementación"), c("Revisa el código contra los lineamientos."), c("Implementan la solución y reportan avance y bloqueos, cada uno con su dueño."), off()],
    [mom("Demo y entrega", true), c("Dice qué se puede afirmar hoy y qué no."), c("Muestran la demo y entregan las historias con su estado y sus evidencias."), c("Product Owner: acepta o ajusta; lo aprendido vuelve al backlog.")],
    [mom("Retro"), c("Ajusta los lineamientos con lo que vio en las revisiones."), c("Eligen un acuerdo de mejora."), off()],
  ];
  const head = [
    [th("Momento", C.text2, { rowspan: 2, valign: "bottom", fontSize: 12 }), th("Equipo tech · Tech and Solve", C.accent1, { colspan: 2, align: "center", fontSize: 12 }), th("Equipo SURA", C.accent3, { align: "center", fontSize: 12 })],
    [th("Arquitecto", C.text2, { fontSize: 12 }), th("Desarrolladores", C.text2, { fontSize: 12 }), th("Product Owner y arquitectura", C.accent3, { fontSize: 12 })],
  ];
  s.addTable(head.concat(rows), tblBase({ x: M, y: 1.6, w: 12.1, colW: [2.0, 3.5, 3.5, 3.1], rowH: [0.34, 0.34].concat(Array(8).fill(0.57)), fontSize: 11 }));
}

// ================= 15 · tablero =================
{
  const s = newSlide(SEC1, "Tablero corto y seis acuerdos para cuidar el flujo",
    "Dos personas implican como máximo dos cosas en curso. Si aparece una tercera, se termina una antes. Los acuerdos son revisables en cada retro.");
  const bw = 1.4, bg = 0.1, bx = M, by = 1.85;
  ["Por hacer", "En curso", "Revisión", "Hecho"].forEach((n, i) => {
    const x = bx + i * (bw + bg);
    s.addShape(pres.ShapeType.roundRect, { x, y: by, w: bw, h: 4.4, rectRadius: 0.06, fill: { color: i === 1 ? C.background2 : C.accent4 }, line: { color: BORDER, width: 1 } });
    T(s, n, x, by + 0.1, bw, 0.3, { align: "center", fontSize: 13, bold: true, color: C.text2 });
  });
  T(s, "máx. 2", bx + bw + bg, by + 0.4, bw, 0.3, { align: "center", fontSize: 12, bold: true, color: C.accent2 });
  const chip = (col, row, fill) => s.addShape(pres.ShapeType.roundRect, { x: bx + col * (bw + bg) + 0.15, y: by + 0.8 + row * 0.62, w: bw - 0.3, h: 0.46, rectRadius: 0.05, fill: { color: fill }, line: { color: fill, width: 0 } });
  [0, 1, 2, 3, 4].forEach((r) => chip(0, r, C.accent5)); [0, 1].forEach((r) => chip(1, r, C.accent1)); chip(2, 0, C.accent2); [0, 1, 2].forEach((r) => chip(3, r, C.accent3));
  const ax = 6.9, aw = 5.8;
  [["Un solo backlog.", " Cada quien toma la siguiente prioridad, con máximo dos cosas en curso."], ["Lo riesgoso, en pareja:", " contratos, traza y agentes que influyen en una decisión."], ["Cambios pequeños, a diario.", " Nada vive en una rama más de un día."], ["Revisa quien no escribió.", " El arquitecto revisa contra los lineamientos."], ["Un bloqueo se dice el mismo día", " y se nombra su dueño."], ["La retro termina con un acuerdo,", " no con una lista de quejas."]].forEach(([a, b], i) => {
    const y = 1.85 + i * 0.73;
    dot(s, ax, y + 0.03, 0.5, String(i + 1), { fontSize: 14 });
    T(s, [{ text: a, options: { bold: true, color: C.text2 } }, { text: b }], ax + 0.7, y, aw - 0.7, 0.62, { fontSize: 14, valign: "middle" });
  });
}

// ================= 12 · entregas =================
{
  const s = newSlide(SEC1, "Qué recibe SURA al cierre de cada sprint",
    "Al cierre de cada sprint SURA recibe tres cosas: las historias trabajadas con su estado, la demo de lo implementado y las evidencias de cada implementación según la definición de hecho (Definition of Done). La demo se hace con datos sintéticos, nunca con datos reales de pacientes.");
  const items = [["Historias trabajadas, con su estado", "Cada historia del sprint con su estado: hecha, en curso o de vuelta al backlog, y el porqué."], ["Demo de lo implementado", "Lo terminado, funcionando con su traza, sobre datos sintéticos y nunca con datos reales de pacientes."], ["Evidencias de cada implementación", "Según la definición de hecho de cada historia: pruebas, traza de la decisión, golden set sin regresión y revisión aprobada."]];
  const w = 3.85, g = 0.275;
  items.forEach(([t, b], i) => {
    const x = M + i * (w + g);
    card(s, x, 1.8, w, 3.35);
    dot(s, x + 0.3, 2.05, 0.6, String(i + 1), { fontSize: 16, fill: C.accent3 });
    T(s, t, x + 0.3, 2.8, w - 0.6, 0.75, { fontSize: 18, bold: true, color: C.text2, valign: "bottom" });
    T(s, b, x + 0.3, 3.65, w - 0.6, 1.45, { fontSize: 14 });
  });
  card(s, M, 5.35, 12.1, 1.1, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "A producción, en los cortes limpios. ", options: { bold: true, color: C.text2 } }, { text: "No todo incremento va a producción: se despliega cuando hay algo usable de punta a punta, como los agentes de Solicitud o la autorización automática de nivel 1. Ese despliegue siempre lo aprueba una persona." }], M + 0.3, 5.35, 11.5, 1.1, { fontSize: 15, valign: "middle" });
}

// ================= 13 · orden de incrementos =================
{
  const s = newSlide(SEC1, "El orden sugerido: tres incrementos y dos cortes limpios",
    "Es un orden sugerido; el orden real lo decide SURA en el backlog, sesión a sesión. Los cortes a producción dependen también del front y la integración, que lideran los equipos de SURA. La trazabilidad para la torre de control es transversal.");
  card(s, M, 1.62, 12.1, 0.62, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "Un orden, no un calendario.  ", options: { bold: true, color: C.accent1, fontSize: 15 } }, { text: "SURA lo confirma o lo cambia en cada sesión de historias. " }, { text: "La arquitectura es evolutiva: ", options: { bold: true, color: C.text2 } }, { text: "la de cada sistema agéntico se define al empezar su implementación." }], M + 0.25, 1.62, 11.6, 0.62, { fontSize: 12, valign: "middle" });
  const cols = [["Arranque", "Primero", "Solo lo común: arquetipo, lineamientos, contrato de eventos y trazabilidad, y primer golden set.", C.text2], ["Agentes de Solicitud", "Incremento 1", "Clasificador, enrutador, extractores, request builder y LLM-as-a-judge; escala a preradicado con su motivo.", C.accent1], ["Agentes de Evaluación", "Incremento 2", "Coberturas, pertinencia médica, duplicidad y concepto al escalar. Ningún agente niega.", C.accent1], ["Auditor y cierre", "Incremento 3", "Auditor dentro de cada gestor, que propone sin promover, y pruebas de punta a punta.", C.accent1]];
  const w = 2.85, g = 0.23;
  cols.forEach(([t, sub, b, col], i) => {
    const x = M + i * (w + g);
    card(s, x, 2.38, w, 2.0);
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.2, y: 2.52, w: w - 0.4, h: 0.38, rectRadius: 0.06, fill: { color: col }, line: { color: col, width: 0 } });
    T(s, t, x + 0.2, 2.52, w - 0.4, 0.38, { align: "center", valign: "middle", fontSize: 13, bold: true, color: C.background1 });
    T(s, sub, x + 0.2, 2.98, w - 0.4, 0.28, { fontSize: 12, bold: true, color: C.accent2 });
    T(s, b, x + 0.2, 3.28, w - 0.4, 1.05, { fontSize: 12 });
  });
  [["Al cerrar · Corte 1: agentes de Solicitud en producción", 1], ["Al cerrar · Corte 2: autorización automática de nivel 1", 2]].forEach(([t, i]) => {
    const x = M + i * (w + g);
    s.addShape(pres.ShapeType.roundRect, { x, y: 4.48, w, h: 0.52, rectRadius: 0.15, fill: { color: C.background1 }, line: { color: C.accent3, width: 1.5 } });
    T(s, t, x + 0.1, 4.48, w - 0.2, 0.52, { align: "center", valign: "middle", fontSize: 11, bold: true, color: C.accent3 });
  });
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 5.12, w: 12.1, h: 0.72, rectRadius: 0.08, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, [{ text: "Transversal · trazabilidad para la torre de control. ", options: { bold: true } }, { text: "Se define en el arranque y se implementa en todos los incrementos: cada agente deja su traza y emite sus eventos con el contrato acordado." }], M + 0.25, 5.12, 11.6, 0.72, { fontSize: 13, color: C.background1, valign: "middle" });
  card(s, M, 5.95, 12.1, 0.62, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "El ciclo de mejora va dentro. ", options: { bold: true, color: C.text2 } }, { text: "Traza, golden set, compuerta, umbral y calibración entran con Solicitud; corrección estructurada y muestreo, con Evaluación." }], M + 0.25, 5.95, 11.6, 0.62, { fontSize: 13, valign: "middle" });
}

// ================= 16 · sección IA =================
pres.addSection({ title: SEC2 });
{
  const s = violetSlide(SEC2);
  logoBox(s, 0.9, 2.1);
  s.addText("IA de Tech and Solve", { x: 0.9, y: 3.35, w: 11, h: 1.0, fontSize: 48, bold: true, color: C.background1, fontFace: "+mj-lt", valign: "top", margin: 0, isTextBox: true });
  T(s, "Nuestra IA generativa propia, cómo potencia el proceso y por qué marca la diferencia.", 0.9, 4.45, 8.5, 0.9, { fontSize: 20, color: C.background2 });
}

// ================= 17 · IA en capas =================
{
  const s = newSlide(SEC2, "La IA de Tech and Solve: lo que la hace nuestra es lo que construimos encima del modelo",
    "Versión en capas. Abajo, los modelos de primer nivel de Anthropic, elegidos según la complejidad, siempre con autorización de SURA. En el medio, lo que construimos y nos hace distintos: base de conocimiento, proceso por fases, reglas desde revisiones reales, agentes especializados y controles con firma humana. Arriba, quién la usa: solo nuestro equipo tech; no se comercializa ni se abre a terceros.");
  const lw = 7.9;
  const lab = (t, x, y, col) => T(s, t, x, y, lw - 0.6, 0.25, { fontSize: 10, bold: true, color: col, charSpacing: 1.5 });
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 1.75, w: lw, h: 0.9, rectRadius: 0.08, fill: { color: C.background1 }, line: { color: C.text2, width: 2 } });
  lab("QUIÉN LA USA", M + 0.3, 1.85, C.text2);
  T(s, [{ text: "Solo el equipo tech de Tech and Solve. ", options: { bold: true, color: C.text2 } }, { text: "No se comercializa ni se abre a terceros." }], M + 0.3, 2.13, lw - 0.6, 0.42, { fontSize: 14, valign: "middle" });
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 2.78, w: lw, h: 2.45, rectRadius: 0.08, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  lab("LO QUE CONSTRUIMOS · LA IA DE TECH AND SOLVE", M + 0.3, 2.95, C.background2);
  T(s, "Conocimiento, proceso y controles propios", M + 0.3, 3.25, lw - 0.6, 0.5, { fontSize: 20, bold: true, color: C.background1 });
  chipRow(s, ["Base de conocimiento", "Proceso por fases", "Reglas desde revisiones reales", "Agentes especializados", "Controles y firma humana"], M + 0.3, 3.85, lw - 0.6, { cw: 0.078, h: 0.4, fs: 11.5, fill: C.background1, color: C.text2 });
  card(s, M, 5.36, lw, 1.1);
  lab("SOBRE MODELOS DE PRIMER NIVEL", M + 0.3, 5.48, C.accent6);
  chipRow(s, ["Anthropic"], M + 0.3, 5.8, 2, { cw: 0.09, h: 0.4, fs: 12, fill: C.accent6, color: C.background1 });
  T(s, "Según la complejidad de cada tarea · siempre con autorización de SURA", M + 1.75, 5.8, lw - 2.1, 0.4, { fontSize: 12, color: C.accent6, valign: "middle" });
  const rx = 8.8, rw = 3.93;
  card(s, rx, 1.75, rw, 1.2, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, "El modelo lo pone el proveedor. Lo que hace que funcione bien es nuestro.", rx + 0.25, 1.75, rw - 0.5, 1.2, { fontSize: 15, bold: true, color: C.text2, valign: "middle" });
  [["Ya opera en proyectos de clientes", "No es un piloto: es como trabajamos hoy."], ["Madurez medida", "Medimos su madurez con métricas de equipo y la mejoramos con evidencia."], ["Uso responsable", "Cada desarrollador se forma en buenos principios y en proteger los datos del cliente."]].forEach(([t, d], i) => {
    const y = 3.1 + i * 1.13;
    card(s, rx, y, rw, 1.0);
    T(s, [{ text: t, options: { bold: true, color: C.text2, breakLine: true } }, { text: d, options: { color: C.accent6 } }], rx + 0.2, y + 0.05, rw - 0.4, 0.9, { fontSize: 12, valign: "middle" });
  });
}

// ================= 18 · no es un IDE =================
{
  const s = newSlide(SEC2, "Así trabaja la IA de Tech and Solve: no es un IDE con IA",
    "Un IDE con IA depende de lo que el desarrollador le dé y de su disciplina. La IA de Tech and Solve trabaja con una base de conocimiento sincronizada con el código, reglas escritas desde revisiones reales, un proceso por fases que se detiene ante bloqueos, compuertas que no puede saltar y firma humana para publicar. Ya opera así en proyectos de clientes.");
  const r = (a, b, c) => [{ text: a, options: { bold: true, color: C.text2, fontSize: 13 } }, { text: b, options: { color: C.accent6, fontSize: 13 } }, { text: c, options: { fill: { color: C.background2 }, fontSize: 13 } }];
  const rows = [
    r("Contexto", "Lo que el desarrollador pegue en el chat.", "Una base de conocimiento del sistema, citada con evidencia y sincronizada con el código antes de cada sesión."),
    r("Reglas", "Las que el desarrollador recuerde.", "Reglas escritas a partir de revisiones de código reales, que el agente aplica siempre."),
    r("Proceso", "Libre: se pide y se genera.", "Un proceso por fases: primero analiza, se detiene si hay bloqueos y solo entonces implementa."),
    r("Control", "Depende de la disciplina de cada quien.", "Compuertas que el agente no puede saltar: no escribe sin pasar la de análisis ni publica sin la firma de una persona."),
    r("Revisión y evidencia", "Al final, en el pull request.", "Agentes auditores revisan requisitos y evidencia de pruebas; cada cambio llega con su porqué."),
    r("Continuidad", "Se pierde al cerrar la sesión.", "Cada tarea deja sus artefactos versionados y se retoma en cualquier momento."),
  ];
  s.addTable([[th(""), th("Un IDE con IA", C.accent6), th("La IA de Tech and Solve")]].concat(rows), tblBase({ x: M, y: 1.7, w: 12.1, colW: [2.0, 3.6, 6.5], rowH: [0.42].concat(Array(6).fill(0.64)), fontSize: 13 }));
  T(s, "Un IDE con IA acelera a quien escribe. La nuestra acelera al equipo, con conocimiento, reglas y control incorporados.", M, 6.2, 12.1, 0.55, { fontSize: 15, bold: true, color: C.text2, valign: "middle" });
}

// ================= 19 · IA en cada etapa =================
{
  const s = newSlide(SEC2, "Nuestra IA potencia cada etapa, y una persona valida cada paso",
    "Cada etapa del proceso usa la IA propia de Tech and Solve donde más rinde, y cada paso tiene una persona que valida. Esa combinación es la que acelera sin perder control.");
  const st = [
    ["1", "Descubrimiento", "mantiene una base de conocimiento del sistema, citada con evidencia y sincronizada con el código.", "el arquitecto valida alcance y reglas.", C.accent2],
    ["2", "Backlog", "lee el tablero, aplica la definición de listo y recomienda qué historia tomar.", "SURA prioriza; el equipo toma la siguiente prioridad.", C.accent2],
    ["3", "Refinamiento", "contrasta la historia con el código real y mide su radio de impacto.", "responde lo que la IA no puede decidir.", C.accent1],
    ["4", "Planificación", "si hay bloqueos, se detiene y pregunta; si no, arma un plan numerado de pasos y pruebas.", "firma antes de seguir en cambios riesgosos.", C.accent1],
    ["5", "Desarrollo", "implementa según el plan y las reglas escritas desde revisiones reales.", "revisa, y lo que queda fuera de alcance va a una historia nueva.", C.accent1],
    ["6", "Integración continua", "corre las pruebas por escenario y arma la evidencia de cada caso.", "un agente auditor y una persona revisan la evidencia.", C.accent1],
    ["7", "Revisión y demo", "se autorrevisa con el estándar de los revisores y defiende cada cambio: quién lo pidió y qué afecta.", "aprueba el pull request.", C.accent3],
    ["8", "Retrospectiva", "deja cada tarea versionada y retomable, con su rastro por fase.", "el proceso solo cambia por decisión del equipo.", C.accent1],
    ["9", "Despliegue", "prepara el despliegue y un rollback que se ejecuta en minutos.", "publicar exige su firma; la IA no la crea.", C.accent3],
    ["10", "Operación", "verifica en producción y vuelve a sincronizar la base de conocimiento.", "cierra la tarea con el resultado verificado.", C.accent3],
  ];
  const w = (12.1 - 4 * 0.13) / 5, h = 2.12;
  st.forEach(([n, t, ia, p, col], i) => {
    const x = M + (i % 5) * (w + 0.13), y = 1.65 + Math.floor(i / 5) * (h + 0.13);
    card(s, x, y, w, h);
    dot(s, x + 0.12, y + 0.12, 0.38, n, { fontSize: 10, fill: col });
    T(s, t, x + 0.58, y + 0.08, w - 0.68, 0.46, { fontSize: 11.5, bold: true, color: C.text2, valign: "middle" });
    T(s, [{ text: "IA: ", options: { bold: true, color: C.accent1 } }, { text: ia, options: { breakLine: true } }, { text: "Persona: ", options: { bold: true, color: C.accent3 } }, { text: p, options: { color: C.accent6 } }], x + 0.12, y + 0.6, w - 0.24, h - 0.68, { fontSize: 10.5, paraSpaceAfter: 4 });
  });
  card(s, M, 6.15, 12.1, 0.62, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "En los sistemas agénticos de SURA, el mismo método se extiende ", options: { bold: true, color: C.text2 } }, { text: "al golden set, a las versiones de prompt y a los casos adversariales que se prueban antes de la compuerta." }], M + 0.25, 6.15, 11.6, 0.62, { fontSize: 12, valign: "middle" });
}

// ================= 20 · calidad =================
{
  const s = newSlide(SEC2, "Velocidad con IA, con calidad, performance y seguridad que se verifican",
    "La columna de hoy describe lo que nuestra IA ya hace en cada cambio. La de SURA es cómo se aplican esas garantías a los agentes: golden set, juez calibrado, latencia y costo observados, y techos de autonomía.");
  const r = (a, b, c) => [{ text: a, options: { bold: true, color: C.text2, fontSize: 15 } }, { text: b, options: { fontSize: 14 } }, { text: c, options: { fill: { color: C.background2 }, fontSize: 14 } }];
  const rows = [
    r("Calidad", "Se autorrevisa con el estándar de los revisores humanos y aprueba una persona distinta del autor. El estilo de código se verifica antes de pedir revisión.", "Ningún agente se promueve si su golden set muestra regresión. El LLM-as-a-judge se calibra contra una muestra revisada por personas expertas."),
    r("Performance", "Antes de planear, analiza la concurrencia, la idempotencia y el radio de impacto. Cada despliegue trae su rollback, ejecutable en minutos.", "Latencia y costo por caso de cada agente, observados. El umbral de confianza es configuración, y la compuerta frena una versión que empeora."),
    r("Seguridad", "No publica sin firma humana. Las credenciales se enmascaran en la evidencia y los datos del cliente no se versionan.", "Los datos de SURA solo van a herramientas que SURA autorice. Techos de autonomía: ningún agente niega una solicitud."),
  ];
  s.addTable([[th(""), th("Hoy, con nuestra IA"), th("En los agentes de SURA", C.accent3)]].concat(rows), tblBase({ x: M, y: 1.75, w: 12.1, colW: [1.8, 5.0, 5.3], rowH: [0.45, 1.25, 1.25, 1.25], fontSize: 14 }));
  card(s, M, 6.05, 12.1, 0.62, { fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
  T(s, [{ text: "Lo de la izquierda ya opera; ", options: { bold: true, color: C.text2 } }, { text: "lo de la derecha es cómo esas mismas garantías se llevan a los sistemas agénticos de SURA." }], M + 0.25, 6.05, 11.6, 0.62, { fontSize: 14, valign: "middle" });
}

// ================= 21 · por qué Tech and Solve =================
{
  const s = newSlide(SEC2, "Por qué el equipo de Tech and Solve es la mejor opción",
    "Cierre de la propuesta. Resume las dos secciones: la dinámica de trabajo con SURA y la IA de Tech and Solve. El argumento más fuerte es que ya conocemos la arquitectura de gestores por el trabajo previo con SURA.");
  s.addShape(pres.ShapeType.roundRect, { x: M, y: 1.75, w: 3.7, h: 4.7, rectRadius: 0.1, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
  T(s, "Expertos en construir sistemas agénticos, y en construirlos con IA.", M + 0.3, 2.2, 3.1, 2.0, { fontSize: 22, bold: true, color: C.background1, fontFace: "+mj-lt" });
  T(s, "Conocemos la arquitectura de gestores, trabajamos por sprints con SURA y construimos con una IA propia que acelera sin perder control.", M + 0.3, 4.3, 3.1, 1.9, { fontSize: 14, color: C.background2 });
  const why = [["Expertos en sistemas agénticos", "Ya trabajamos con SURA en la arquitectura de gestores, la torre de control y la acertividad de los agentes."], ["IA propia de Tech and Solve", "Conocimiento, proceso y controles propios, de uso exclusivo de nuestro equipo tech."], ["Más rápido, sin perder control", "Nuestra IA potencia cada etapa del proceso y una persona valida cada paso."], ["Garantías que se verifican", "Calidad, performance y seguridad que ya operan, llevadas a los agentes de SURA."], ["Equipo enfocado y con dirección", "Un arquitecto que define, se alinea con el equipo de arquitectura de SURA y revisa, y dos desarrolladores que implementan."], ["Sobre el diseño de SURA", "SURA define las historias, prioriza y ve funcionando lo construido en cada demo."]];
  const gx = M + 3.9, cw = (12.1 - 3.9 - 0.2) / 2, ch = 1.45;
  why.forEach(([t, d], i) => {
    const x = gx + (i % 2) * (cw + 0.2), y = 1.75 + Math.floor(i / 2) * (ch + 0.175);
    card(s, x, y, cw, ch);
    dot(s, x + 0.2, y + 0.18, 0.42, String(i + 1), { fontSize: 12 });
    T(s, t, x + 0.75, y + 0.15, cw - 0.9, 0.48, { fontSize: 14, bold: true, color: C.text2, valign: "middle" });
    T(s, d, x + 0.2, y + 0.7, cw - 0.4, ch - 0.75, { fontSize: 12 });
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
