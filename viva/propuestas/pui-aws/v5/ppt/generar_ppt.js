// Genera la versión editable (PPTX) de la propuesta para el cliente, con texto y formas nativas.
//   node generar_ppt.js  -> ../propuesta-viva-pui-aws-v5-cliente-editable.pptx
// Lee layout.json (lo produce extraer_layout.js desde el HTML); si cambia el HTML, correr ./generar.sh.
// Coordenadas en px del lienzo HTML (1280 x 720) -> pulgadas con px / 96; tamaños de letra px -> pt con * 0.75.
// Cada tarjeta es un rectángulo redondeado; los párrafos apilados de una tarjeta van en una sola caja de texto.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const OUT = path.resolve(__dirname, "..", "propuesta-viva-pui-aws-v5-cliente-editable.pptx");
const FONT = "Arial";
const MONO = "Courier New";
const THEME = {
  name: "Tech and Solve",
  headFontFace: FONT,
  bodyFontFace: FONT,
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "280265", lt2: "EBEBFF",
    accent1: "5300DF", accent2: "22D0FF", accent3: "282E3F", accent4: "EBEBFF",
    accent5: "280265", accent6: "000000", hlink: "5300DF", folHlink: "280265",
  },
};

const px = (v) => v / 96;
const pt = (v) => +(v * 0.75).toFixed(2);
const slides = JSON.parse(fs.readFileSync(path.join(__dirname, "layout.json"), "utf8"));

// Runs of one or more paragraphs -> pptxgenjs text array.
function textRuns(paras, o) {
  const out = [];
  paras.forEach((runs, pi) => {
    runs.forEach((r, ri) => {
      const opt = {
        fontFace: r.mono ? MONO : FONT, fontSize: pt(r.size), color: r.color,
        bold: r.bold, italic: r.italic, align: o.align, lineSpacing: pt(o.lh),
      };
      if (r.ls) opt.charSpacing = pt(r.ls);
      if (r.hl) opt.highlight = r.hl;
      if (o.bullet) opt.bullet = { indent: pt(o.bullet.indent) };
      if (pi === 0 && o.spaceBefore) opt.paraSpaceBefore = o.spaceBefore;
      if (ri === runs.length - 1 && !(o.last && pi === paras.length - 1)) opt.breakLine = true;
      out.push({ text: r.text, options: opt });
    });
  });
  return out;
}

// Consecutive text blocks stacked in the same column of the same card become one text box.
function groupTexts(items) {
  const out = [];
  for (const it of items) {
    const prev = out[out.length - 1];
    if (it.t === "text" && prev && prev.t === "textgroup" && prev.box === it.box && it.box !== "foot-num"
      && Math.abs(prev.x - it.x) < 1.5 && Math.abs(prev.x + prev.w - (it.x + it.w)) < 3
      && it.y >= prev.y + prev.h - 1 && it.y - (prev.y + prev.h) < 34) {
      prev.blocks.push({ ...it, gap: it.y - (prev.y + prev.h) });
      prev.h = it.y + it.h - prev.y;
      continue;
    }
    out.push(it.t === "text" ? { ...it, t: "textgroup", blocks: [{ ...it, gap: 0 }] } : it);
  }
  return out;
}

async function build() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 1280 x 720 px
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  pres.title = "Integración con la PUI en AWS · Viva Aerobus";
  pres.company = "Tech and Solve";
  pres.author = "Tech and Solve";

  for (const sl of slides) {
    const s = pres.addSlide();
    s.background = { color: sl.bg };
    let titled = false;
    for (const it of groupTexts(sl.items)) {
      if (it.t === "img") {
        s.addImage({ path: path.join(__dirname, "img", `${it.id}.png`), x: px(it.x), y: px(it.y), w: px(it.w), h: px(it.h),
          altText: sl.n === 2 && it.w > 400 ? "Diagrama de interacción entre la PUI, la solución y la API interna de Viva" : "Logo",
          objectName: it.w > 400 ? "Diagrama" : "Logo" });
      } else if (it.t === "line") {
        s.addShape(pres.shapes.LINE, { x: px(it.x), y: px(it.y), w: px(it.w), h: px(it.h),
          line: { color: it.color, width: pt(it.w), dashType: it.dash ? "dash" : "solid" }, objectName: "Línea" });
      } else if (it.t === "shape") {
        const o = {
          x: px(it.x), y: px(it.y), w: px(it.w), h: px(it.h),
          fill: it.fill ? { color: it.fill.hex, transparency: Math.round((1 - it.fill.a) * 100) } : { type: "none" },
          line: it.line ? { color: it.line.color, width: pt(it.line.w), dashType: it.line.dash ? "dash" : "solid" } : { type: "none" },
          objectName: `Forma ${it.name}`,
        };
        let shape = pres.shapes.RECTANGLE;
        if (it.ellipse) shape = pres.shapes.OVAL;
        else if (it.radius > 0.5) { shape = pres.shapes.ROUNDED_RECTANGLE; o.rectRadius = px(it.radius); }
        if (it.paras) {
          const [t, r, b, l] = it.pad.map(pt);
          // Badges and circles hold one line: never wrap them.
          const oneLine = it.paras.length === 1 && it.h - it.pad[0] - it.pad[2] < it.lh * 1.5;
          s.addText(textRuns(it.paras, { align: it.align, lh: it.lh, last: true }), {
            ...o, shape, margin: [l, r, b, t] /* pptxgenjs: izquierda, derecha, abajo, arriba */,
            valign: it.valign, align: oneLine ? "center" : it.align, fit: "none", wrap: !oneLine });
        } else {
          s.addShape(shape, o);
        }
      } else if (it.t === "textgroup") {
        const runs = [];
        it.blocks.forEach((b, i) => runs.push(...textRuns(b.paras, {
          align: b.align, lh: b.lh, bullet: b.bullet, spaceBefore: i ? pt(b.gap) : 0, last: i === it.blocks.length - 1 })));
        const isTitle = !titled && it.y < 140 && Math.max(...it.blocks[0].paras.flat().map((r) => r.size)) >= 30;
        if (isTitle) titled = true;
        const slack = it.align === "right" ? 0 : 6;
        s.addText(runs, {
          x: px(it.x), y: px(it.y), w: px(Math.min(it.w + slack, 1280 - it.x)), h: px(it.h + 4),
          margin: 0, valign: "top", wrap: true, fit: "none", isTextBox: true,
          objectName: isTitle ? "Título" : it.box === "foot-num" ? "Número de lámina" : "Texto",
        });
      }
    }
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  return OUT;
}

build().then((f) => console.log(f));
