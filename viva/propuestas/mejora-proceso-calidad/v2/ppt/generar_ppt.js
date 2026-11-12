// Genera la versión editable (PPTX) de la propuesta, con texto y formas nativas.
//   node generar_ppt.js            -> ../propuesta-mejora-proceso-calidad-para-cliente-editable-v2.pptx (cliente)
//                                     ../propuesta-mejora-proceso-calidad-uso-interno-no-enviar-editable-v2.pptx (con la slide interna)
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
  const c3 = [72, 456, 840], cw = 368;
  const c4 = [72, 360, 648, 936], cw4 = 272;
  const content = (sectionTitle) => pres.addSlide({ masterName: "Contenido", sectionTitle });

  // ---------- 1 · Portada ----------
  pres.addSection({ title: "Situación" });
  let s = pres.addSlide({ masterName: "Portada", sectionTitle: "Situación" });
  s.addText("VIVA AEROBUS · GENERIC API · PROPUESTA", { x: px(72), y: px(300), w: px(900), h: px(24), fontFace: FONT, fontSize: 11, bold: true, color: BLUE, charSpacing: 1, margin: 0, isTextBox: true, objectName: "Kicker" });
  s.addText("Control de calidad automático\ny propio para el código de Viva", { x: px(72), y: px(334), w: px(1000), h: px(150), fontFace: FONT, fontSize: 42, bold: true, color: WHITE, margin: 0, valign: "top", isTextBox: true, objectName: "Titulo portada" });
  s.addText("Tech and Solve para Viva Aerobus · Noviembre de 2026 · Documento confidencial", { x: px(72), y: px(672), w: px(900), h: px(20), fontFace: FONT, fontSize: 9, color: LV, margin: 0, isTextBox: true, objectName: "Pie" });

  // ---------- 2 · Qué es SonarQube ----------
  s = content("Situación");
  kicker(s, "PARA EMPEZAR · QUÉ ES SONARQUBE");
  title(s, "Un revisor automático para cada cambio de código");
  s.addText("SonarQube analiza el código fuente con reglas por lenguaje y señala los problemas antes de que un cambio se integre a la rama principal. Existe como servicio en la nube (SonarQube Cloud) o instalado en servidores propios (SonarQube Server).", { x: px(72), y: px(196), w: px(1136), h: px(44), fontFace: FONT, fontSize: 13, color: WHITE, margin: 0, valign: "top", isTextBox: true, objectName: "Subtitulo" });
  const lbl = (t, y) => s.addText(t, { x: px(72), y: px(y), w: px(600), h: px(18), fontFace: FONT, fontSize: 9.5, bold: true, color: LV, charSpacing: 1, margin: 0, isTextBox: true, objectName: "Etiqueta" });
  const lk = (t, k, size = 11) => r(t, { fontSize: size, bold: true, color: BLUE, hyperlink: { url: {'metrics': 'https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/metric-definitions', 'hotspots': 'https://docs.sonarsource.com/sonarqube-cloud/standards/managing-rules/security-hotspots', 'coverage': 'https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/overview', 'profiles': 'https://docs.sonarsource.com/sonarqube-cloud/standards/managing-quality-profiles/understanding-quality-profiles', 'gates': 'https://docs.sonarsource.com/sonarqube-cloud/standards/managing-quality-gates/introduction-to-quality-gates', 'newcode': 'https://docs.sonarsource.com/sonarqube-cloud/standards/about-new-code', 'pr': 'https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/pull-request-analysis', 'home': 'https://docs.sonarsource.com/sonarqube-cloud/'}[k] } });
  lbl("QUÉ REVISA", 250);
  card(s, c4[0], 270, cw4, 100, [h3("Confiabilidad", 13), p("Defectos que pueden hacer fallar el sistema en ejecución.", 11, true)]);
  card(s, c4[1], 270, cw4, 100, [h3("Seguridad", 13), r("Vulnerabilidades, y código sensible (", { fontSize: 11 }), lk("security hotspots", "hotspots"), r(") que Sonar marca para que el equipo lo revise.", { fontSize: 11 })]);
  card(s, c4[2], 270, cw4, 100, [h3("Mantenibilidad", 13), p("Código difícil de entender o de cambiar, y código duplicado.", 11, true)]);
  card(s, c4[3], 270, cw4, 100, [h3("Cobertura", 13), r("Qué parte del código recorren las pruebas unitarias, ", { fontSize: 11 }), lk("medida cuando el pipeline las ejecuta", "coverage"), r(".", { fontSize: 11 })]);
  lbl("CÓMO APORTA A LA CALIDAD", 384);
  card(s, c3[0], 406, cw, 104, [r("Perfil de reglas · ", { fontSize: 13, bold: true }), lk("Quality Profile", "profiles", 13), r("", { breakLine: true }), p("Qué reglas se aplican en cada lenguaje. Se define una vez y queda por defecto para todos los proyectos.", 11, true)], { fill: BLACK });
  card(s, c3[1], 406, cw, 104, [r("Filtro de calidad · ", { fontSize: 13, bold: true }), lk("Quality Gate", "gates", 13), r("", { breakLine: true }), p("Los umbrales que un cambio debe cumplir. El resultado es uno solo: aprobado o fallido.", 11, true)], { fill: BLACK });
  card(s, c3[2], 406, cw, 104, [r("Foco en el ", { fontSize: 13, bold: true }), lk("código nuevo", "newcode", 13), r("", { breakLine: true }), p("Se exige a lo nuevo o modificado: la calidad mejora con cada cambio, sin frenar por lo existente.", 11, true)], { fill: BLACK });
  card(s, 72, 526, 1136, 84, [r("En el día a día:", { fontSize: 11.5, bold: true, color: BLUE }), r(" el resultado ", { fontSize: 11.5 }), lk("aparece en el propio cambio de código en GitHub", "pr", 11.5), r(", con el detalle de cada problema. ", { fontSize: 11.5 }), r("Lo que no hace:", { fontSize: 11.5, bold: true, color: BLUE }), r(" no reemplaza la revisión de una persona ni las pruebas funcionales; no sabe si el código hace lo que el negocio necesita. Documentación oficial: ", { fontSize: 11.5 }), lk("docs.sonarsource.com/sonarqube-cloud", "home", 11.5)], { fill: BLACK, border: BLUE, valign: "middle", name: "Franja" });

  // ---------- 3 · Lo que Sonar puede medir ----------
  s = content("Situación");
  kicker(s, "PARA EMPEZAR · EL POTENCIAL DE SONAR");
  title(s, "Lo que Sonar puede medir, del plan base al completo");
  {
    const U3 = {'sast': 'https://docs.sonarsource.com/sonarqube-cloud/advanced-security/introduction#advanced-sast', 'owasp': 'https://docs.sonarsource.com/sonarqube-cloud/standards/managing-rules/security-related-rules', 'secrets': 'https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/secrets', 'iac': 'https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/terraform', 'coverage': 'https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/dotnet-test-coverage', 'sca': 'https://docs.sonarsource.com/sonarqube-cloud/advanced-security/introduction#sca', 'compliance': 'https://docs.sonarsource.com/sonarqube-cloud/getting-started-with-enterprise/viewing-enterprise-reports/project-compliance-reports', 'plans': 'https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/managing-subscription/subscription-plans', 'owaspO': 'https://owasp.org/Top10/', 'cwe': 'https://cwe.mitre.org/top25/', 'pci': 'https://www.pcisecuritystandards.org/standards/pci-dss/'};
    const lk3 = (t, k, size = 10.5) => r(t, { fontSize: size, bold: true, color: BLUE, hyperlink: { url: U3[k] } });
    const li = (parts, last) => parts.map((x, i) => { const o = Object.assign({}, x.options, { paraSpaceAfter: 6 }); if (i === 0) o.bullet = { code: "2013" }; if (i === parts.length - 1 && !last) o.breakLine = true; return r(x.text, o); });
    const t10 = (t, b) => r(t, { fontSize: 10.5, bold: !!b, color: WHITE });
    card(s, 72, 196, 412, 280, [tag("VIENE CON SONARQUBE CLOUD", BLUE), h3("Calidad y seguridad del código propio", 13),
      ...li([lk3("SAST", "sast"), t10(": revisa el código fuente sin ejecutarlo. Detecta inyección SQL, cross-site scripting, deserialización insegura y más, con reglas "), lk3("mapeadas", "owasp"), t10(" a "), lk3("OWASP Top 10", "owaspO"), t10(" para C#.")]),
      ...li([lk3("Secretos", "secrets"), t10(": credenciales, llaves y tokens escritos en el código.")]),
      ...li([lk3("Infraestructura como código", "iac"), t10(": Terraform, Docker, Kubernetes, CloudFormation, Ansible y workflows de GitHub Actions.")]),
      ...li([t10("Confiabilidad, mantenibilidad y duplicación.", true)]),
      ...li([lk3("Cobertura de pruebas", "coverage"), t10(": de líneas y de condiciones, a partir de las pruebas que ejecuta el pipeline.")], true)], { border: BLUE });
    card(s, 494, 196, 412, 280, [tag("CON ADVANCED SECURITY"), h3("Seguridad de las dependencias", 13),
      ...li([lk3("SCA", "sca"), t10(": vulnerabilidades conocidas (CVE) en las librerías de terceros, priorizando las que el código realmente usa.")]),
      ...li([t10("Paquetes maliciosos", true), t10(" entre las dependencias.")]),
      ...li([t10("Licencias:", true), t10(" políticas de licencias permitidas.")]),
      ...li([t10("SBOM:", true), t10(" inventario exportable de todas las dependencias.")]),
      ...li([t10("SAST avanzado:", true), t10(" vulnerabilidades que nacen de la interacción entre el código y las librerías open source; disponible para C#/.NET.")], true)]);
    card(s, 916, 196, 292, 280, [tag("CON PLAN ENTERPRISE"), h3("Reportes frente a estándares de seguridad", 13),
      ...li([lk3("Reportes de cumplimiento", "compliance"), t10(": qué hallazgos de cada proyecto incumplen estándares como "), lk3("OWASP Top 10", "owaspO"), t10(", "), lk3("CWE Top 25", "cwe"), t10(" o "), lk3("PCI DSS", "pci"), t10(", el estándar de seguridad para pagos con tarjeta. Listos para el área de seguridad.")]),
      ...li([t10("Una sola vista:", true), t10(" todos los proyectos de Viva juntos, aunque estén en distintas organizaciones de GitHub.")], true)]);
    card(s, 72, 492, 1136, 90, [r("Lo que no hace:", { fontSize: 11, bold: true, color: BLUE }), r(" no ejecuta la aplicación, así que no es DAST, IAST ni prueba de penetración; esas pruebas se hacen con otras herramientas. ", { fontSize: 11 }),
      r("En este servicio", { fontSize: 11, bold: true, color: BLUE }), r(" configuramos las reglas .NET y el filtro de calidad; secretos e infraestructura como código ya vienen con SonarQube Cloud, y Advanced Security y el plan Enterprise se suman cuando Viva lo decida. Planes en la ", { fontSize: 11 }), lk3("documentación oficial", "plans", 11), r(".", { fontSize: 11 })], { fill: BLACK, valign: "middle", name: "Franja" });
  }

  // ---------- 4 · Estado actual ----------
  s = content("Situación");
  kicker(s, "ESTADO ACTUAL");
  title(s, "El equipo de desarrollo de Generic API no tiene acceso a la herramienta de calidad");
  card(s, c3[0], 222, cw, 250, [tag("DÓNDE ESTÁ"), h3("En la infraestructura de un tercero"),
    r("La herramienta de calidad, SonarQube, vive en ", { fontSize: 11.5 }), r("sonarqube.ezyflight.se", { fontSize: 11.5, bold: true }),
    r(": un dominio de Ezy, administrado por Ezy. Cada cambio de código enlaza ahí (por ejemplo, ", { fontSize: 11.5 }),
    r("#2511", { fontSize: 11.5, color: BLUE, hyperlink: { url: GH + "2511" } }), r(").", { fontSize: 11.5 })]);
  card(s, c3[1], 222, cw, 250, [tag("QUÉ VE EL EQUIPO"), h3("Solo un semáforo y un número"),
    p("El equipo de desarrollo de Generic API no tiene acceso: ve si el cambio pasó el filtro de calidad y cuántos problemas tiene, pero no cuáles ni dónde están.", 11.5, true)]);
  card(s, c3[2], 222, cw, 250, [tag("QUÉ IMPLICA", BLUE), h3("Se desaprovecha la herramienta"),
    p("Lo que no se ve, no se corrige. Y cualquier cambio de reglas o de accesos depende de pedírselo a un tercero.", 11.5, true)], { border: BLUE });
  band(s, 494, 70, "Además,", "la revisión automática actual de Generic API **no ejecuta las pruebas unitarias** ni **bloquea**: un cambio con problemas detectados puede llegar igual a la rama principal.");

  // ---------- 5 · Lo que cuesta hoy ----------
  s = content("Situación");
  kicker(s, "LO QUE ESTO CUESTA HOY · SEPTIEMBRE 2026");
  title(s, "Problemas que llegan a la rama principal y retrabajo en cada revisión");
  card(s, c3[0], 222, cw, 240, [...num("9", "de 20"), h3("cambios llegaron a la rama principal con el filtro de calidad en rojo", 13), p("20 problemas nuevos detectados por la herramienta, sin que se mencionaran en las revisiones.", 11.5, true)]);
  card(s, c3[1], 222, cw, 240, [...num("0", "%"), h3("del código nuevo con pruebas unitarias medidas", 13), p("La revisión automática no ejecuta las pruebas unitarias, así que no se mide qué parte del código nuevo está probada.", 11.5, true)]);
  card(s, c3[2], 222, cw, 240, [...num("46", "%"), h3("de los cambios comentados, por estilo o convenciones", 13), p("12 de 26. Son revisiones que una regla automática hace sola, sin ocupar a un revisor.", 11.5, true)]);
  card(s, 72, 482, 1136, 96, [h3("Revisión manual de lo que una máquina ya detecta"), p("Cuatro tipos de comentario de los revisores los detectan reglas automáticas. Cada uno es tiempo de revisión y un ciclo más de corrección.", 11.5, true)]);
  source(s, "Fuente: cambios de código (PRs) de Generic API de septiembre de 2026 y sus revisiones en GitHub, consulta del 8 oct 2026. Enlaces a cada uno en el anexo (slide 16).");

  // ---------- 6 · El objetivo ----------
  pres.addSection({ title: "Propuesta" });
  s = content("Propuesta");
  kicker(s, "EL OBJETIVO");
  title(s, "Qué queda funcionando en 10 días hábiles");
  card(s, 72, 200, 1136, 120, [r("Objetivo:", { fontSize: 14, bold: true, color: BLUE }), ...rich(" que Viva tenga **su propio SonarQube**, con **reglas comunes para todos sus proyectos .NET** y un **filtro de calidad por defecto acordado con Viva**; que **Generic API ya lo aplique**, bloqueando los cambios que no cumplen; y que **cualquier proyecto nuevo se sume siguiendo una guía**, sin redefinir reglas ni filtro.", 14)], { fill: BLACK, border: BLUE, valign: "middle", name: "Objetivo" });
  [["Un cambio que no cumple, no se integra", "En Generic API, un cambio de prueba que no pasa el filtro de calidad queda en rojo y GitHub no permite integrarlo. Uno que cumple, pasa."],
   ["Las reglas y el filtro son los acordados", "El perfil de reglas .NET y el filtro de calidad por defecto del Sonar de Viva coinciden con lo que Viva aprobó por escrito."],
   ["Un proyecto nuevo se suma con la guía", "Siguiendo solo la guía, un equipo conecta su proyecto .NET al Sonar de Viva desde GitHub Actions y hereda las reglas y el filtro por defecto."]]
    .forEach(([t, x], i) => card(s, c3[i], 338, cw, 150, [tag("SE COMPRUEBA", BLUE), h3(t), p(x, 11.5, true)]));

  // ---------- 7 · Paso 1 ----------
  s = content("Propuesta");
  kicker(s, "LA PROPUESTA · PASO 1");
  title(s, "Una herramienta de calidad de Viva, para todos sus proyectos");
  s.addText("Las reglas de calidad dependen del lenguaje, no del proyecto. Viva las define una vez, las aplica a todos sus proyectos y decide quién tiene acceso, sin depender de un tercero.", { x: px(72), y: px(196), w: px(1136), h: px(44), fontFace: FONT, fontSize: 13, color: WHITE, margin: 0, valign: "top", isTextBox: true, objectName: "Subtitulo" });
  card(s, 72, 256, 360, 160, [tag("DEFINE VIVA", BLUE), h3("Las reglas de calidad de Viva", 15), p("Un conjunto de reglas por lenguaje y un mismo filtro de calidad, aprobados por Viva.", 11, true)], { fill: BLACK, border: BLUE });
  arrow(s, 440, 316);
  card(s, 478, 256, 236, 160, [tag("PRIMERO"), h3("Generic API"), p("Donde se configura y se prueba en este servicio.", 11, true)], { border: LV });
  card(s, 726, 256, 236, 160, [h3("Otros proyectos .NET de Viva"), p("Usan las mismas reglas, sin redefinirlas.", 11, true)]);
  card(s, 974, 256, 234, 160, [h3("Proyectos en otros lenguajes"), p("Se suman con las reglas de su lenguaje, bajo el mismo criterio.", 11, true)]);
  card(s, 72, 432, 560, 120, [tag("BASE DE ESTA PROPUESTA", BLUE), h3("En la nube: SonarQube Cloud"), p("Servicio administrado por SonarSource, bajo una organización de Viva. Sin servidores que mantener. 10 días hábiles.", 11, true)], { fill: BLACK });
  card(s, 648, 432, 560, 120, [tag("ALTERNATIVA · UNA SEMANA MÁS"), h3("En infraestructura propia"), p("En servidores y dominio de Viva, con edición Developer o superior. Si la configuramos nosotros, suma 5 días hábiles (slide 13).", 11, true)], { fill: BLACK });

  // ---------- 8 · Paso 2 ----------
  s = content("Propuesta");
  kicker(s, "LA PROPUESTA · PASO 2");
  title(s, "Cada cambio pasa por el filtro antes de que lo vea una persona");
  {
  const sx = [72, 362, 652, 942], sw = 266;
  [["1", "Compilar", "¿El código compila?", "Si no, el cambio se detiene.", "BLOQUEA", BLUE],
   ["2", "Pruebas unitarias", "¿Pasan todas las pruebas unitarias?", "Una prueba unitaria rota detiene el cambio.", "BLOQUEA", BLUE],
   ["3", "Análisis", "¿Qué problemas nuevos hay?", "El detalle queda en el cambio, con el enlace a cada problema.", "INFORMA", LV],
   ["4", "Filtro de calidad", "¿Cumple el estándar de Viva?", "Si cumple, pasa a la revisión de una persona; si no, no se puede integrar.", "BLOQUEA", BLUE]]
    .forEach(([n, t, q, x, tg, tc], i) => card(s, sx[i], 206, sw, 200,
      [r(n, { fontSize: 20, bold: true, color: BLUE, breakLine: true, paraSpaceAfter: 6 }), h3(t, 15), r(q + " ", { fontSize: 11.5, bold: true }), r(x, { fontSize: 11.5, breakLine: true, paraSpaceAfter: 10 }), r(tg, { fontSize: 9, bold: true, color: tc, charSpacing: 1 })]));
  card(s, 72, 424, 1136, 120, [
    r("Propuesta inicial del filtro: ", { fontSize: 12.5, bold: true, color: BLUE }),
    r("Pruebas unitarias que recorran al menos el 80 % del código nuevo", { fontSize: 12.5, bold: true }),
    r(" · ningún defecto ni vulnerabilidad nueva · problemas de mantenimiento dentro del límite acordado · poco código duplicado (≤ 3 %).", { fontSize: 12.5, breakLine: true, paraSpaceAfter: 4 }),
    r("Solo se exige al código nuevo de cada cambio: el código existente no frena el trabajo. Es el punto de partida: Viva aprueba los umbrales. Como hoy la cobertura no se mide, recomendamos que solo informe las primeras semanas y que Viva decida cuándo pasa a bloquear. Quedan como filtro por defecto para todos sus proyectos.", { fontSize: 11, color: LV })], { fill: BLACK, valign: "middle", name: "Franja" });
  }

  // ---------- 9 · Beneficios ----------
  pres.addSection({ title: "Valor" });
  s = content("Valor");
  kicker(s, "BENEFICIOS");
  title(s, "Menos retrabajo, menos riesgo, más control");
  card(s, c3[0], 196, cw, 250, [h3("Viva Aerobus"), ...bullets(["Ningún cambio llega a la rama principal sin pasar el filtro, salvo un salto de emergencia autorizado por Viva.", "Los problemas dejan de acumularse: se controla lo nuevo sin frenar por lo existente.", "Cambia reglas y da accesos sin pedírselo a un tercero.", "Si cambia un proveedor, el control de calidad y el historial que se genere desde ahora se quedan en Viva."], 11)]);
  card(s, c3[1], 196, cw, 250, [h3("Revisores"), ...bullets(["Dejan de corregir a mano lo que una máquina detecta.", "Dedican su tiempo a diseño y negocio.", "Un solo criterio de calidad, igual para todos los cambios."], 11)]);
  card(s, c3[2], 196, cw, 250, [h3("Equipo de desarrollo"), ...bullets(["Ve cada problema y dónde está, desde el propio cambio.", "Sabe si su cambio cumple antes de que lo revise una persona.", "Menos devoluciones y menos idas y vueltas por cambio."], 11)]);
  card(s, 72, 462, 560, 120, [tag("HOY"), ...num("9", "de 20", WHITE), p("cambios de septiembre llegaron a la rama principal con el filtro de calidad en rojo, sin pruebas unitarias medidas.", 11, true)], { fill: BLACK });
  card(s, 648, 462, 560, 120, [tag("CON EL CONTROL", BLUE), ...num("0"), p("cambios llegan a la rama principal sin pasar las pruebas y el filtro, salvo saltos de emergencia autorizados por Viva y registrados.", 11, true)], { fill: BLACK });

  // ---------- 10 · Plan de trabajo ----------
  pres.addSection({ title: "Plan y cierre" });
  s = content("Plan y cierre");
  kicker(s, "PLAN DE TRABAJO");
  title(s, "Dos semanas, con tres hitos verificables");
  {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px(72), y: px(160), w: px(1136), h: px(268), rectRadius: 0.12, fill: { color: BLACK }, line: { type: "none" }, objectName: "Cronograma fondo" });
    const x0 = 330, dw = (1188 - 330) / 10;
    const txt = (t, x, y, w, o) => s.addText(t, Object.assign({ x: px(x), y: px(y), w: px(w), h: px(20), fontFace: FONT, fontSize: 9.5, color: WHITE, margin: 0, valign: "middle", isTextBox: true }, o));
    txt("SEMANA 1", x0, 170, dw * 5, { bold: true, color: BLUE, align: "center", charSpacing: 1 });
    txt("SEMANA 2", x0 + dw * 5, 170, dw * 5, { bold: true, color: BLUE, align: "center", charSpacing: 1 });
    for (let d = 1; d <= 10; d++) txt(`Día ${d}`, x0 + dw * (d - 1), 194, dw, { color: LV, align: "center" });
    const bar = (a, b, t, y, fill) => s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: px(x0 + dw * (a - 1) + 2), y: px(y), w: px(dw * (b - a + 1) - 4), h: px(26), fill: { color: fill || BLUE }, line: { type: "none" }, fontFace: FONT, fontSize: 9.5, bold: true, color: DV, align: (a === b ? "center" : "left"), valign: "middle", margin: [0, 6, 0, 6], objectName: "Barra" });
    [["Sonar de Viva con reglas .NET", 1, 3, "Organización, accesos y reglas"],
     ["Reglas y filtro, aprobados por Viva", 1, 5, "Propuesta, sesión y aprobación de Viva"],
     ["Generic API integrado y bloqueando", 4, 8, "Pipeline, pruebas, análisis y bloqueo"],
     ["Guía de integración", 8, 10, "Guía, plantilla y validación"]].forEach(([l, a, b, t], i) => {
      const y = 222 + i * 38; txt(l, 92, y + 3, 230, { bold: true, fontSize: 10.5 }); bar(a, b, t, y);
    });
    const yh = 222 + 4 * 38; txt("Hitos", 92, yh + 3, 230, { bold: true, fontSize: 10.5 });
    bar(5, 5, "Aprobación", yh, LV); bar(8, 8, "Bloqueo", yh, LV); bar(10, 10, "Entrega", yh, LV);
  }
  card(s, c3[0], 444, cw, 130, [tag("DÍA 5", BLUE), h3("Viva aprueba reglas y filtro", 13), p("Nuestro plan prevé la aprobación por escrito ese día. Si aún no llega, queda configurada la propuesta inicial y Viva la ajusta después.", 11, true)]);
  card(s, c3[1], 444, cw, 130, [tag("DÍA 8", BLUE), h3("Generic API bloqueando", 13), p("El pipeline falla si un cambio no pasa el filtro, y GitHub no deja integrarlo.", 11, true)]);
  card(s, c3[2], 444, cw, 130, [tag("DÍA 10", BLUE), h3("Entrega", 13), p("Demostración con un cambio en rojo bloqueado y uno en verde, guía validada y sesión de entrega.", 11, true)], { border: BLUE });

  // ---------- 11 · Precondiciones ----------
  s = content("Plan y cierre");
  kicker(s, "PRECONDICIONES PARA PRESTAR EL SERVICIO");
  title(s, "Lo que Viva decide y habilita");
  const pc = (i, tg, t, items) => card(s, c4[i], 168, cw4, 304, [tag(tg), h3(t, 13), ...bullets(items, 10)]);
  pc(0, "SONAR", "En SonarQube Cloud", [
    "Aprobación de seguridad para analizar su código en la nube.",
    "La organización de Viva, con plan Team o superior (lo contrata Viva) y un administrador para Tech and Solve.",
    "Lectura del Sonar de Ezy para exportar las reglas y el filtro actuales; sin ella, partimos del perfil recomendado por Sonar (Sonar way).",
    "La lista de equipos y personas con acceso, y su rol."]);
  pc(1, "GITHUB", "En GitHub", [
    "Administración del repositorio de Generic API: workflows, secretos y reglas de protección de ramas.",
    "La app de SonarQube Cloud instalada en la organización de GitHub de Generic API, hoy de Ezy.",
    "Permiso para integrar el cambio del pipeline en Generic API.",
    "Un repositorio de prueba para la guía y el bloqueo."]);
  pc(2, "DECISIONES", "Lo que Viva decide", [
    "Un responsable con disponibilidad para aprobar reglas y filtro en la primera semana.",
    "Qué ramas se protegen: master y las que indique.",
    "Quién puede saltarse el bloqueo en una emergencia.",
    "Que Generic API se analice solo en el Sonar de Viva.",
    "Que corregir hallazgos y escribir pruebas sea parte de cada tarea."]);
  pc(3, "SI ELIGE SONAR PROPIO", "En su infraestructura", [
    "El servidor o la cuenta de nube, con acceso de administración.",
    "El dominio, el certificado y la licencia Developer o superior, ya comprada.",
    "Sonar alcanzable desde GitHub Actions: publicado en internet o con runners propios en la red de Viva.",
    "Permiso para crear la GitHub App de Sonar en la organización de Generic API.",
    "Viva opera el servidor después de la entrega."]);
  band(s, 488, 84, "Supuestos:", "todos los accesos y permisos, incluidos los que dependen de Ezy, se entregan antes de arrancar; los días hábiles cuentan desde ese momento. El pipeline se integra solo en Generic API; otros proyectos se suman con la guía o se cotizan aparte. Si una prueba unitaria no corre en el pipeline, se documenta y el bloqueo se activa con las que sí corren. No incluye corregir hallazgos existentes ni escribir pruebas unitarias.", 11);

  // ---------- 12 · Inversión ----------
  s = content("Plan y cierre");
  kicker(s, "LA INVERSIÓN · SERVICIO LLAVE EN MANO");
  title(s, "10 días hábiles, llave en mano");
  card(s, 72, 160, 560, 136, [tag("TIEMPO APROXIMADO DE IMPLEMENTACIÓN", BLUE), ...num("10", "días hábiles", WHITE), p("Dos semanas con SonarQube Cloud, desde que se cumplen las precondiciones (slide 11). Con Sonar propio, 15 (slide 13).", 11, true)], { fill: BLACK });
  card(s, 648, 160, 560, 136, [tag("COSTO", BLUE), ...num("xxx", "", WHITE), p("Incluye los cuatro entregables. Acompañamiento opcional en la slide 14.", 11, true)], { fill: BLACK });
  const dx = [72, 360, 648, 936], dw = 272;
  [["Sonar de Viva con reglas .NET comunes", "Organización de Viva en SonarQube Cloud, con un perfil de reglas .NET por defecto para todos los proyectos y los accesos de los equipos que Viva indique."],
   ["Reglas y filtro por defecto, aprobados por Viva", "El perfil de reglas .NET y los umbrales del filtro que apruebe Viva o, sin aprobación, la propuesta inicial; configurados por defecto para todos los proyectos."],
   ["Generic API integrado y bloqueando", "Su pipeline de GitHub Actions compila, prueba y analiza cada cambio, y falla si no pasa el filtro. Solo el grupo que Viva defina puede saltarse el bloqueo en una emergencia."],
   ["Guía de integración de proyectos nuevos", "Paso a paso y una plantilla de workflow de GitHub Actions para conectar un proyecto .NET al Sonar de Viva. Con sesión de entrega."]]
    .forEach(([t, x], i) => card(s, dx[i], 312, dw, 250, [r(String(i + 1), { fontSize: 22, bold: true, color: BLUE, breakLine: true, paraSpaceAfter: 4 }), h3(t, 13), p(x, 11, true)], { name: `Entregable ${i + 1}` }));

  // ---------- 13 · Alternativa: Sonar propio ----------
  s = content("Plan y cierre");
  kicker(s, "ALTERNATIVA · SONAR EN INFRAESTRUCTURA PROPIA");
  title(s, "Sonar propio: una semana más si lo configuramos nosotros");
  card(s, 72, 196, 560, 130, [tag("TIEMPO APROXIMADO DE IMPLEMENTACIÓN", BLUE), ...num("15", "días hábiles", WHITE), p("Tres semanas: una para montar el Sonar de Viva y las dos del servicio base.", 11, true)], { fill: BLACK });
  card(s, 648, 196, 560, 130, [tag("COSTO", BLUE), ...num("yyy", "", WHITE), p("Los mismos cuatro entregables, más el Sonar de Viva instalado y documentado.", 11, true)], { fill: BLACK });
  card(s, 72, 342, 640, 210, [tag("LO QUE HACEMOS EN LA SEMANA ADICIONAL", BLUE), ...bullets([
    "Instalar SonarQube, edición Developer o superior, en contenedores, con su base de datos PostgreSQL.",
    "Publicarlo en el dominio de Viva con HTTPS, detrás de un proxy inverso con el certificado de Viva.",
    "Activar la licencia y configurar el inicio de sesión y los grupos de los equipos.",
    "Conectarlo con GitHub para que el resultado aparezca en cada cambio.",
    "Respaldo programado de la base de datos y manual de operación: arranque, actualización y restauración."], 10.5)], { border: BLUE });
  card(s, 728, 342, 480, 210, [tag("QUÉ GANA VIVA"), ...bullets([
    "Los resultados del análisis y su historial quedan en la infraestructura de Viva.",
    "Control total del servidor, las versiones y los respaldos.",
    "Las mismas reglas, filtro y guía que con SonarQube Cloud."], 10.5)]);

  // ---------- 14 · Opcional: acompañamiento ----------
  s = content("Plan y cierre");
  kicker(s, "OPCIONAL · ACOMPAÑAMIENTO");
  title(s, "Una o dos semanas de acompañamiento con el bloqueo ya activo");
  card(s, 72, 196, 560, 130, [tag("DURACIÓN", BLUE), ...num("1 o 2", "semanas", WHITE), p("Justo después de la entrega, a demanda de Viva. Viva elige la duración.", 11, true)], { fill: BLACK });
  card(s, 648, 196, 560, 130, [tag("COSTO", BLUE), ...num("zzz", "por semana", WHITE), p("Aparte del servicio base. Aplica igual con SonarQube Cloud o con Sonar propio.", 11, true)], { fill: BLACK });
  card(s, 72, 342, 640, 210, [tag("QUÉ INCLUYE", BLUE), ...bullets([
    "Resolver dudas de los equipos sobre hallazgos, cobertura y por qué un cambio quedó bloqueado.",
    "Revisar falsos positivos y proponer a Viva ajustes de reglas o umbrales; se aplican solo con su aprobación.",
    "Atender fallas del pipeline que no vengan del código: configuración, secretos o tiempos de ejecución.",
    "Acompañar a un primer proyecto nuevo mientras se integra con la guía.",
    "Un resumen semanal para Viva: cambios bloqueados, saltos de emergencia usados y cobertura del código nuevo."], 10.5)], { border: BLUE });
  card(s, 728, 342, 480, 210, [tag("POR QUÉ CONVIENE"), ...bullets([
    "Los primeros días con el bloqueo activo concentran las dudas y los ajustes.",
    "Los equipos adoptan el filtro con respuesta rápida, en lugar de buscar cómo saltarlo.",
    "Viva decide los ajustes con datos de las primeras semanas de uso real."], 10.5)]);

  // ---------- 15 · Siguiente paso ----------
  s = content("Plan y cierre");
  kicker(s, "DESPUÉS DE GENERIC API");
  title(s, "Una ruta para crecer sobre la misma base");
  {
    const rx = [72, 470, 868], rw = 340;
    card(s, rx[0], 176, rw, 200, [...num("1"), h3("Sumar proyectos .NET", 15), p("Cada equipo conecta su proyecto con la guía y hereda las reglas y el filtro de Viva, sin redefinir reglas ni filtro.", 11.5, true)]);
    arrow(s, 422, 256);
    card(s, rx[1], 176, rw, 200, [...num("2"), h3("Sumar otros lenguajes", 15), p("Un perfil de reglas por lenguaje, bajo el mismo criterio y el mismo filtro de calidad.", 11.5, true)]);
    arrow(s, 820, 256);
    card(s, rx[2], 176, rw, 200, [...num("3"), h3("Ampliar la seguridad", 15), r("Advanced Security para las dependencias y, con el plan Enterprise, reportes frente a estándares como ", { fontSize: 11.5 }), r("PCI DSS", { fontSize: 11.5, bold: true, color: BLUE, hyperlink: { url: "https://www.pcisecuritystandards.org/standards/pci-dss/" } }), r(" (slide 3).", { fontSize: 11.5 })], { border: BLUE });
    band(s, 396, 58, "Cada paso lo decide Viva,", "cuando lo necesite, sobre la base que deja este servicio. Tech and Solve puede acompañar cualquiera de ellos.");
  }

  // ---------- 16 · Anexo ----------
  pres.addSection({ title: "Anexo" });
  s = content("Anexo");
  kicker(s, "ANEXO · DETALLE DE LOS CAMBIOS REVISADOS");
  title(s, "Los cambios de código que respaldan estas cifras");
  const links = (nums) => nums.flatMap((n, i) => [r(`#${n}`, { fontSize: 12, bold: true, color: BLUE, hyperlink: { url: GH + n } }), r(i < nums.length - 1 ? "   " : "", { fontSize: 12 })]);
  card(s, 72, 214, 560, 170, [h3("9 de 20 · Llegaron a la rama principal con el filtro en rojo"), ...links(["2421", "2467", "2484", "2487", "2488", "2493", "2506", "2509", "2516"])]);
  card(s, 648, 214, 560, 170, [h3("12 de 26 · Comentarios de estilo o convenciones"), ...links(["2421", "2467", "2478", "2484", "2487", "2488", "2494", "2499", "2504", "2508", "2511", "2516"])]);
  const rule = (n, t, last) => [r(`#${n}`, { fontSize: 11, bold: true, color: BLUE, hyperlink: { url: GH + n } }), r(` · ${t}`, { fontSize: 11, breakLine: !last, paraSpaceAfter: 4 })];
  card(s, 72, 400, 1136, 170, [h3("Comentarios que detecta una regla automática"),
    ...rule("2516", "parámetro sin uso · Sonar S1172"),
    ...rule("2467", "métodos idénticos · Sonar S4144; nombre de campo · .editorconfig"), ...rule("2494", "Array.Empty · analizador .NET CA1825", true)]);
  source(s, "PRs de Generic API de septiembre de 2026 en GitHub (EzyWebwerkstaden/VivaAerobus.Generic.Api), consulta del 8 oct 2026. Ningún revisor menciona Sonar en las revisiones ni en los comentarios de los 28 PRs del periodo. Un PR puede estar en varios grupos.");

  // ---------- Interna ----------
  if (withInternal) {
    pres.addSection({ title: "Uso interno" });
    s = content("Uso interno");
    s.addText("USO INTERNO DE TECH AND SOLVE · NO MOSTRAR AL CLIENTE", { x: px(72), y: px(20), w: px(560), h: px(28), fontFace: FONT, fontSize: 10, bold: true, color: WHITE, fill: { color: BLACK }, line: { color: WHITE, width: 1 }, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Marca interna" });
    kicker(s, "EQUIPO DE TRABAJO");
    title(s, "Un ingeniero DevOps al 100 % durante dos semanas");
    card(s, 72, 220, 360, 300, [tag("EQUIPO", BLUE), ...num("1", "ingeniero DevOps", WHITE), p("Dedicación: tiempo completo."), p("Duración: 10 días hábiles con SonarQube Cloud, desde que se cumplen las precondiciones."), p("Con Sonar propio: 15 días hábiles. La primera semana se monta el servidor y luego sigue el plan base.", 11.5, true)], { fill: BLACK });
    card(s, 452, 220, 756, 300, [tag("RESPONSABLE DE LOS CUATRO ENTREGABLES"), ...bullets([
      "Sonar de Viva (días 1-3): configurar la organización en SonarQube Cloud y los accesos, migrar el perfil de reglas .NET desde el Sonar de Ezy y dejarlo como perfil por defecto.",
      "Reglas y filtro (días 1-5): proponer perfil y umbrales, sesión con el responsable de Viva, aprobación por escrito y configuración por defecto.",
      "Generic API (días 4-8): GitHub Actions con compilación, pruebas unitarias, cobertura y análisis; checks obligatorios en el ruleset de master; bypass de emergencia para el grupo de Viva.",
      "Guía (días 8-10): paso a paso y plantilla de workflow para proyectos nuevos, validada contra un repositorio de prueba; demostración final con un PR en rojo bloqueado y uno en verde, y sesión de entrega."], 11.5)]);
  }

  return pres.writeFile({ fileName: path.join(OUT, fileName) }).then(async (f) => { await applyTheme(f, THEME); return f; });
}

(async () => {
  console.log(await build(false, "propuesta-mejora-proceso-calidad-para-cliente-editable-v2.pptx"));
  console.log(await build(true, "propuesta-mejora-proceso-calidad-uso-interno-no-enviar-editable-v2.pptx"));
})();
