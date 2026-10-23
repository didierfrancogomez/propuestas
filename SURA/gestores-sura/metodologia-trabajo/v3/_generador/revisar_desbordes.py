"""Approximate renderer for QA: draws shapes, tables and wrapped text, flags overflow.
Body text measured with Arial (wider than Calibri: conservative). Heading (Poppins) with Arial Bold x1.12."""
import sys, zipfile, re
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
EMU = 914400
DPI = 100
THEME = {"dk1": "1A1E27", "lt1": "FFFFFF", "dk2": "280265", "lt2": "EBEBFF", "accent1": "5300DF", "accent2": "B9720A",
         "accent3": "1B6B4F", "accent4": "FAF9FE", "accent5": "DCD8EC", "accent6": "5B5A66", "tx1": "1A1E27", "tx2": "280265",
         "bg1": "FFFFFF", "bg2": "EBEBFF", "hlink": "5300DF"}
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_fc = {}
def font(pt, bold):
    k = (round(pt * 4) / 4, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FB if bold else FR, max(1, int(round(pt / 72 * DPI))))
    return _fc[k]

def color(el):
    if el is None: return None
    s = el.find("a:srgbClr", NS)
    if s is not None: return "#" + s.get("val")
    s = el.find("a:schemeClr", NS)
    if s is not None: return "#" + THEME.get(s.get("val"), "FF00FF")
    return None

def px(v): return int(v) / EMU * DPI

warnings = []

def draw_text(d, txBody, x, y, w, h, label, default_sz=14, default_col="#1A1E27", heading=False):
    bp = txBody.find("a:bodyPr", NS)
    ins = lambda k, dflt: px(bp.get(k)) if bp is not None and bp.get(k) is not None else dflt
    l, t, r, b = ins("lIns", 9.6), ins("tIns", 4.8), ins("rIns", 9.6), ins("bIns", 4.8)
    anchor = bp.get("anchor", "t") if bp is not None else "t"
    W = w - l - r
    lines = []  # (height, [(word, font, col, width)], align, indent)
    for p in txBody.findall("a:p", NS):
        ppr = p.find("a:pPr", NS)
        algn = ppr.get("algn", "l") if ppr is not None else "l"
        bullet = ppr is not None and ppr.find("a:buChar", NS) is not None
        indent = 0.25 * DPI if bullet else 0
        spcAft = 0
        if ppr is not None and ppr.find("a:spcAft/a:spcPts", NS) is not None:
            spcAft = int(ppr.find("a:spcAft/a:spcPts", NS).get("val")) / 100 / 72 * DPI
        toks = []
        maxsz = 0
        for rr in p.findall("a:r", NS):
            rp = rr.find("a:rPr", NS)
            sz = int(rp.get("sz")) / 100 if rp is not None and rp.get("sz") else default_sz
            bold = rp is not None and rp.get("b") == "1"
            col = color(rp.find("a:solidFill", NS)) if rp is not None else None
            col = col or default_col
            scale = 1.12 if heading else 1.0
            f = font(sz * scale, bold or heading)
            maxsz = max(maxsz, sz)
            txt = rr.findtext("a:t", default="", namespaces=NS)
            for part in re.split(r"(\s+)", txt):
                if part: toks.append((part, f, col, d.textlength(part, font=f), sz))
        if not toks:
            sz = default_sz
            ep = p.find("a:endParaRPr", NS)
            if ep is not None and ep.get("sz"): sz = int(ep.get("sz")) / 100
            lines.append((sz * 1.2 / 72 * DPI, [], algn, indent, spcAft)); continue
        cur, cw, avail = [], 0, W - indent
        out = []
        for tk in toks:
            if tk[0].isspace():
                if cur: cur.append(tk); cw += tk[3]
                continue
            if cw + tk[3] > avail and cur:
                while cur and cur[-1][0].isspace(): cw -= cur.pop()[3]
                out.append(cur); cur, cw = [], 0
            if tk[3] > avail:
                warnings.append(f"{label}: word too long '{tk[0]}'")
            cur.append(tk); cw += tk[3]
        if cur: out.append(cur)
        for i, ln in enumerate(out):
            lh = max(t_[4] for t_ in ln) * 1.2 / 72 * DPI
            lines.append((lh, ln, algn, indent if True else 0, spcAft if i == len(out) - 1 else 0, bullet and i == 0))
    total = sum(L[0] + L[4] for L in lines)
    if total > h - t - b + 1.5:
        warnings.append(f"{label}: text overflow {total:.0f}px > {h - t - b:.0f}px :: " + "".join(tk[0] for L in lines for tk in L[1])[:70])
    cy = y + t
    if anchor == "ctr": cy = y + t + (h - t - b - total) / 2
    elif anchor == "b": cy = y + h - b - total
    for L in lines:
        lh, ln, algn, indent = L[0], L[1], L[2], L[3]
        lw = sum(tk[3] for tk in ln)
        cx = x + l + indent
        if algn == "ctr": cx = x + l + (W - lw) / 2
        elif algn == "r": cx = x + l + W - lw
        if len(L) > 5 and L[5]:
            d.ellipse([x + l + 4, cy + lh / 2 - 3, x + l + 10, cy + lh / 2 + 3], fill="#1A1E27")
        for tk in ln:
            d.text((cx, cy + lh * 0.1), tk[0], font=tk[1], fill=tk[2]); cx += tk[3]
        cy += lh + L[4]

def draw_shape(d, sp, label, img_rels, z, im, heading_ph=False):
    off = sp.find(".//a:xfrm/a:off", NS); ext = sp.find(".//a:xfrm/a:ext", NS)
    if off is None: return
    x, y, w, h = px(off.get("x")), px(off.get("y")), px(ext.get("cx")), px(ext.get("cy"))
    if x + w > 13.34 * DPI + 1 or y + h > 7.5 * DPI + 1 or x < -1 or y < -1:
        warnings.append(f"{label}: off-slide {x:.0f},{y:.0f},{w:.0f},{h:.0f}")
    spPr = sp.find("p:spPr", NS)
    if spPr is not None:
        geom = spPr.find("a:prstGeom", NS)
        g = geom.get("prst") if geom is not None else "rect"
        fill = color(spPr.find("a:solidFill", NS))
        ln = spPr.find("a:ln", NS)
        lc = color(ln.find("a:solidFill", NS)) if ln is not None else None
        box = [x, y, x + w, y + h]
        if fill or lc:
            if g == "ellipse": d.ellipse(box, fill=fill, outline=lc)
            elif g == "roundRect": d.rounded_rectangle(box, radius=min(w, h) * 0.12, fill=fill, outline=lc)
            elif g == "chevron":
                k = h * 0.5
                d.polygon([(x, y), (x + w - k, y), (x + w, y + h / 2), (x + w - k, y + h), (x, y + h), (x + k, y + h / 2)], fill=fill)
            elif g == "leftArrow":
                k = h
                d.polygon([(x, y + h / 2), (x + k, y), (x + k, y + h * .2), (x + w, y + h * .2), (x + w, y + h * .8), (x + k, y + h * .8), (x + k, y + h)], fill=fill)
            else: d.rectangle(box, fill=fill, outline=lc)
    tb = sp.find("p:txBody", NS)
    if tb is not None:
        draw_text(d, tb, x, y, w, h, label, default_sz=28 if heading_ph else 14, default_col="#280265" if heading_ph else "#1A1E27", heading=heading_ph)

def draw_pic(d, pic, im, rels, z, label):
    off = pic.find(".//a:xfrm/a:off", NS); ext = pic.find(".//a:xfrm/a:ext", NS)
    x, y, w, h = px(off.get("x")), px(off.get("y")), px(ext.get("cx")), px(ext.get("cy"))
    rid = pic.find(".//a:blip", NS).get("{%s}embed" % NS["r"])
    tgt = rels.get(rid)
    if tgt:
        from io import BytesIO
        try:
            pi = Image.open(BytesIO(z.read(tgt))).convert("RGBA").resize((int(w), int(h)))
            im.paste(pi, (int(x), int(y)), pi)
        except Exception as e:
            warnings.append(f"{label}: pic {e}")

def draw_table(d, gf, label):
    off = gf.find("p:xfrm/a:off", NS)
    x0, y0 = px(off.get("x")), px(off.get("y"))
    tbl = gf.find(".//a:tbl", NS)
    cols = [px(g.get("w")) for g in tbl.findall("a:tblGrid/a:gridCol", NS)]
    y = y0
    for ri, tr in enumerate(tbl.findall("a:tr", NS)):
        h = px(tr.get("h")); x = x0
        # compute needed height
        for ci, tc in enumerate(tr.findall("a:tc", NS)):
            tcPr = tc.find("a:tcPr", NS)
            fill = color(tcPr.find("a:solidFill", NS)) if tcPr is not None else None
            d.rectangle([x, y, x + sum(cols[ci:ci+int(tc.get("gridSpan","1"))]), y + h], fill=fill, outline="#DCD8EC")
            mar = lambda k, dv: px(tcPr.get(k)) if tcPr is not None and tcPr.get(k) else dv
            # fake bodyPr from tcPr margins
            tb = tc.find("a:txBody", NS)
            span = int(tc.get("gridSpan", "1"))
            cw_ = sum(cols[ci:ci+span])
            if tc.get("hMerge") or tc.get("vMerge") or tb is None:
                x += cols[ci]; continue
            bp = tb.find("a:bodyPr", NS)
            if bp is None:
                bp = etree.SubElement(tb, "{%s}bodyPr" % NS["a"]); tb.insert(0, bp)
            for k, dv in (("lIns", "marL"), ("rIns", "marR"), ("tIns", "marT"), ("bIns", "marB")):
                if tcPr is not None and tcPr.get(dv): bp.set(k, tcPr.get(dv))
            if tcPr is not None and tcPr.get("anchor"): bp.set("anchor", tcPr.get("anchor"))
            draw_text(d, tb, x, y, cw_, h, f"{label} r{ri}c{ci}")
            x += cols[ci]
        y += h
    if y > 6.9 * DPI: warnings.append(f"{label}: table bottom at {y/DPI:.2f}in")

def rels_of(z, part):
    rp = part.rsplit("/", 1); rp = rp[0] + "/_rels/" + rp[1] + ".rels"
    out = {}
    if rp in z.namelist():
        for r in etree.fromstring(z.read(rp)):
            tgt = r.get("Target")
            base = part.rsplit("/", 1)[0]
            parts = (base + "/" + tgt).split("/")
            st = []
            for p_ in parts:
                if p_ == "..": st.pop()
                else: st.append(p_)
            out[r.get("Id")] = "/".join(st)
    return out

def render(path, outdir):
    z = zipfile.ZipFile(path)
    pres = etree.fromstring(z.read("ppt/presentation.xml"))
    prels = rels_of(z, "ppt/presentation.xml")
    slides = [prels[s.get("{%s}id" % NS["r"])] for s in pres.findall("p:sldIdLst/p:sldId", NS)]
    for n, sp_path in enumerate(slides, 1):
        im = Image.new("RGB", (int(13.333 * DPI), int(7.5 * DPI)), "white")
        d = ImageDraw.Draw(im)
        srels = rels_of(z, sp_path)
        layout = [v for v in srels.values() if "slideLayout" in v][0]
        lrels = rels_of(z, layout)
        lx = etree.fromstring(z.read(layout))
        for el in lx.find(".//p:spTree", NS):
            tag = etree.QName(el).localname
            if tag == "pic": draw_pic(d, el, im, lrels, z, f"s{n} layout pic")
            elif tag == "sp" and el.find(".//p:ph", NS) is None: draw_shape(d, el, f"s{n} layout", lrels, z, im)
        sx = etree.fromstring(z.read(sp_path))
        for i, el in enumerate(sx.find(".//p:spTree", NS)):
            tag = etree.QName(el).localname
            lab = f"s{n} #{i}"
            if tag == "sp":
                ph = el.find(".//p:ph", NS)
                if ph is not None and el.find(".//a:xfrm", NS) is None:
                    # inherit from layout title placeholder
                    for lsp in lx.findall(".//p:sp", NS):
                        lph = lsp.find(".//p:ph", NS)
                        if lph is not None and lph.get("type") == ph.get("type"):
                            spPr = el.find("p:spPr", NS)
                            spPr.append(etree.fromstring(etree.tostring(lsp.find(".//a:xfrm", NS))))
                            lbp = lsp.find(".//a:bodyPr", NS)
                            bp = el.find(".//a:bodyPr", NS)
                            for k, v in lbp.attrib.items(): bp.set(k, v)
                    draw_shape(d, el, lab + " title", srels, z, im, heading_ph=True)
                else:
                    draw_shape(d, el, lab, srels, z, im)
            elif tag == "pic": draw_pic(d, el, im, srels, z, lab)
            elif tag == "graphicFrame": draw_table(d, el, lab)
        d.text((12.5 * DPI, 7.05 * DPI), str(n), font=font(11, False), fill="#5B5A66")
        im.save(f"{outdir}/r{n:02d}.png")
    for w in warnings: print("WARN", w)
    print("slides", len(slides))

render(sys.argv[1], sys.argv[2])
