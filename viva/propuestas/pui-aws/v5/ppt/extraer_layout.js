// Lee la geometría de las láminas de cliente del HTML y la guarda en layout.json (+ imágenes en img/).
//   node extraer_layout.js
// Abre el HTML en Chrome sin interfaz, con la lámina a 1280 x 720 px, y recorre el DOM:
//   - cajas con fondo o borde        -> formas (rectángulo redondeado, círculo o líneas)
//   - bloques de texto               -> párrafos con sus corridas (color, negrita, tamaño, mayúsculas...)
//   - <img> y <svg>                  -> imágenes PNG a 3x
// generar_ppt.js convierte layout.json en el PPTX editable.
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer-core");

const HTML = path.resolve(__dirname, "..", "propuesta-viva-pui-aws-v5-fuente-con-internas.html");
const CLIENT_SLIDES = 19; // las láminas 20 a 30 son de uso interno
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const IMG = path.join(__dirname, "img");

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--disable-gpu"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900, deviceScaleFactor: 3 });
  await page.goto("file://" + HTML, { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);
  const hint = await page.$(".hint");
  if (hint) await page.evaluate((h) => h.remove(), hint);

  const slides = await page.evaluate((N) => {
    const hex = (c) => {
      const m = c.match(/rgba?\(([^)]+)\)/);
      if (!m) return null;
      const [r, g, b, a = 1] = m[1].split(",").map((v) => parseFloat(v));
      if (a === 0) return null;
      return { hex: [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("").toUpperCase(), a };
    };
    const isInline = (cs) => cs.display === "inline" || cs.display === "contents";
    const visible = (el, cs) => cs.display !== "none" && cs.visibility !== "hidden";

    function hasInlineText(el) {
      for (const n of el.childNodes) {
        if (n.nodeType === 3 && n.textContent.trim()) return true;
        if (n.nodeType === 1) {
          const cs = getComputedStyle(n);
          if (!visible(n, cs)) continue;
          if (isInline(cs) && (n.textContent.trim() || n.tagName === "BR")) return true;
        }
      }
      return false;
    }
    function hasBlockChildren(el) {
      for (const c of el.children) {
        const cs = getComputedStyle(c);
        if (visible(c, cs) && !isInline(cs)) return true;
      }
      return false;
    }
    function runStyle(el) {
      const cs = getComputedStyle(el);
      const bg = isInline(cs) ? hex(cs.backgroundColor) : null;
      return {
        color: hex(cs.color)?.hex || "000000",
        bold: parseInt(cs.fontWeight, 10) >= 600,
        italic: cs.fontStyle === "italic",
        size: parseFloat(cs.fontSize),
        mono: /mono|menlo|courier/i.test(cs.fontFamily),
        upper: cs.textTransform === "uppercase",
        ls: cs.letterSpacing === "normal" ? 0 : parseFloat(cs.letterSpacing),
        hl: bg ? bg.hex : null,
      };
    }
    // Paragraphs of an element's inline content. A <br> or a newline in white-space:pre starts a new one.
    function paragraphs(el) {
      const pre = getComputedStyle(el).whiteSpace.startsWith("pre");
      const paras = [[]];
      const nodes = [];
      const walk = (node, style) => {
        for (const n of node.childNodes) {
          if (n.nodeType === 3) {
            nodes.push(n);
            let t = n.textContent;
            if (pre) {
              t.split("\n").forEach((part, i) => { if (i) paras.push([]); if (part) paras[paras.length - 1].push({ text: part, ...style }); });
            } else {
              t = t.replace(/\s+/g, " ");
              if (t) paras[paras.length - 1].push({ text: style.upper ? t.toUpperCase() : t, ...style });
            }
          } else if (n.nodeType === 1) {
            const cs = getComputedStyle(n);
            if (!visible(n, cs) || !isInline(cs)) continue;
            if (n.tagName === "BR") { paras.push([]); continue; }
            nodes.push(n);
            walk(n, runStyle(n));
          }
        }
      };
      walk(el, runStyle(el));
      const out = paras.map((runs) => {
        if (!pre && runs.length) {
          runs[0].text = runs[0].text.replace(/^ +/, "");
          runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/ +$/, "");
        }
        return runs.filter((r) => r.text);
      }).filter((p) => p.length);
      return { paras: out, nodes };
    }
    function unionRect(nodes) {
      let l = 1e9, t = 1e9, r = -1e9, b = -1e9;
      for (const n of nodes) {
        const range = document.createRange();
        range.selectNodeContents(n);
        for (const q of range.getClientRects()) {
          if (!q.width && !q.height) continue;
          l = Math.min(l, q.left); t = Math.min(t, q.top); r = Math.max(r, q.right); b = Math.max(b, q.bottom);
        }
      }
      return l < r ? { left: l, top: t, right: r, bottom: b } : null;
    }

    const sections = [...document.querySelectorAll("section.slide")].slice(0, N);
    let imgId = 0;
    return sections.map((sec, si) => {
      const S = sec.getBoundingClientRect();
      const R = (l, t, w, h) => ({ x: +(l - S.left).toFixed(1), y: +(t - S.top).toFixed(1), w: +w.toFixed(1), h: +h.toFixed(1) });
      const items = [];
      const lh = (cs) => (cs.lineHeight === "normal" ? parseFloat(cs.fontSize) * 1.2 : parseFloat(cs.lineHeight));

      function walk(el, depth) {
        const cs = getComputedStyle(el);
        if (!visible(el, cs)) return;
        const r = el.getBoundingClientRect();
        if (el.tagName === "IMG" || el.tagName.toLowerCase() === "svg") {
          const id = `s${si + 1}-${++imgId}`;
          el.setAttribute("data-xid", id);
          items.push({ t: "img", id, ...R(r.left, r.top, r.width, r.height) });
          return;
        }
        const bg = el === sec ? null : hex(cs.backgroundColor);
        const sides = ["Top", "Right", "Bottom", "Left"].map((s) => ({
          w: parseFloat(cs[`border${s}Width`]), style: cs[`border${s}Style`], c: hex(cs[`border${s}Color`]),
        })).map((b) => (b.w > 0 && b.style !== "none" && b.c ? b : null));
        const allSides = sides.every((b) => b && b.w === sides[0].w && b.c.hex === sides[0].c.hex);
        const radius = parseFloat(cs.borderTopLeftRadius) || 0;
        const isBox = !!bg || sides.some(Boolean);
        const textHere = hasInlineText(el);
        const pad = ["Top", "Right", "Bottom", "Left"].map((s) => parseFloat(cs[`padding${s}`]) + parseFloat(cs[`border${s}Width`] || 0));

        if (isBox) {
          const shape = {
            t: "shape", ...R(r.left, r.top, r.width, r.height),
            fill: bg, radius: Math.min(radius, r.width / 2, r.height / 2),
            ellipse: radius >= Math.min(r.width, r.height) / 2 - 0.5 && Math.abs(r.width - r.height) < 2,
            line: allSides ? { w: sides[0].w, color: sides[0].c.hex, dash: sides[0].style === "dashed" } : null,
            name: (el.className && typeof el.className === "string" ? el.className.split(" ")[0] : el.tagName.toLowerCase()),
          };
          // A box whose content is only inline text (badge, circle, banner) carries its own text.
          if (textHere && !hasBlockChildren(el)) {
            const { paras } = paragraphs(el);
            const centered = cs.justifyContent === "center" || cs.textAlign === "center";
            Object.assign(shape, { paras, pad, align: centered ? "center" : "left", lh: lh(cs), valign: "middle" });
            items.push(shape);
            return;
          }
          items.push(shape);
          if (!allSides) sides.forEach((b, i) => {
            if (!b) return;
            const L = [[r.left, r.top, r.width, 0], [r.right, r.top, 0, r.height], [r.left, r.bottom, r.width, 0], [r.left, r.top, 0, r.height]][i];
            items.push({ t: "line", ...R(...L), color: b.c.hex, w: b.w, dash: b.style === "dashed" });
          });
        }

        if (textHere) {
          const { paras, nodes } = paragraphs(el);
          const u = unionRect(nodes);
          if (u && paras.length) {
            const contentRight = r.right - pad[1];
            const li = el.tagName === "LI" && cs.listStyleType !== "none";
            let left = u.left;
            let indent = 0;
            if (li) { indent = r.left - el.parentElement.getBoundingClientRect().left; left = r.left - indent; }
            const item = {
              t: "text", ...R(left, u.top, Math.max(contentRight, u.right) - left, u.bottom - u.top),
              paras, align: cs.textAlign === "center" ? "center" : cs.textAlign === "right" ? "right" : "left",
              lh: lh(cs), bullet: li ? { indent, color: hex(cs.color).hex } : null,
              box: el.closest("[data-boxid]")?.getAttribute("data-boxid") || "slide",
            };
            items.push(item);
          }
          // Slide number from .foot::after { content: counter(slide) }
          if (el.matches(".foot")) {
            const after = getComputedStyle(el, "::after");
            items.push({ t: "text", ...R(r.right - 60, u ? u.top : r.top, 60, u ? u.bottom - u.top : r.height),
              paras: [[{ text: String(si + 1), ...runStyle(el), bold: parseInt(after.fontWeight, 10) >= 600 }]],
              align: "right", lh: lh(cs), bullet: null, box: "foot-num" });
          }
        }
        if (isBox) el.setAttribute("data-boxid", `b${items.length}`);
        for (const c of el.children) {
          const ccs = getComputedStyle(c);
          if (!isInline(ccs) || c.tagName === "IMG" || c.tagName.toLowerCase() === "svg") walk(c, depth + 1);
        }
      }
      walk(sec, 0);
      const title = (sec.querySelector("h1, h2")?.textContent || "").replace(/\s+/g, " ").trim();
      return { n: si + 1, title, bg: hex(getComputedStyle(sec).backgroundColor)?.hex || "FFFFFF", items };
    });
  }, CLIENT_SLIDES);

  // Logos and diagram with transparent background, so they sit cleanly on the slide's own background.
  await page.addStyleTag({ content: "html, body, section.slide, section.slide * { background-color: transparent !important; }" });
  fs.rmSync(IMG, { recursive: true, force: true });
  fs.mkdirSync(IMG, { recursive: true });
  for (const s of slides) for (const it of s.items) if (it.t === "img") {
    const el = await page.$(`[data-xid="${it.id}"]`);
    await el.screenshot({ path: path.join(IMG, `${it.id}.png`), omitBackground: true });
  }
  fs.writeFileSync(path.join(__dirname, "layout.json"), JSON.stringify(slides, null, 1));
  console.log(`layout.json: ${slides.length} láminas, ${slides.reduce((a, s) => a + s.items.length, 0)} elementos`);
  await browser.close();
})();
