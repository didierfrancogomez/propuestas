#!/usr/bin/env python3
"""Genera el borrador HTML de la presentación v5 (slides 16:9, marca Tech and Solve).

Las cifras vienen de la propuesta v4 (calculos/build_v4.py y evidencia.json, lecturas del
9 oct 2026); aquí solo se presentan. Uso:
    python3 build_v5.py salida-borrador.html
Luego: embed_assets.py (logos) y check_brand_compliance.py del skill tech-and-solve-deck.
"""
import sys

JIRA = "https://vivaaerobus.atlassian.net/browse/"


def hl(t):
    return f'<span style="color:var(--blue-accent)">{t}</span>'


# ---------------------------------------------------------------- CSS
CSS = """
:root{
  --dark-violet:#280265; --lighter-violet:#EBEBFF; --black:#000000; --white:#FFFFFF;
  --violet-accent:#5300DF; --blue-accent:#22D0FF; --darker-gray:#282E3F;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#280265;font-family:'Poppins',sans-serif;overflow:hidden}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.stage{position:fixed;left:0;top:0;width:1280px;height:720px;transform-origin:top left}
.slide{position:absolute;left:0;top:0;width:1280px;height:720px;display:none;overflow:hidden;
  padding:0 64px}
.slide.on{display:block}
.kick{position:absolute;left:64px;top:36px;font-size:13px;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;color:var(--lighter-violet)}
.logo{position:absolute;right:56px;top:14px;width:150px;height:auto}
h1{position:absolute;left:64px;top:64px;width:930px;font-size:42px;line-height:1.14;font-weight:700}
.body{position:absolute;left:64px;right:64px;top:190px;bottom:56px}
.foot{position:absolute;left:64px;right:120px;bottom:22px;display:flex;justify-content:space-between;
  font-size:12px;color:var(--lighter-violet)}
.foot .src{max-width:960px}
.sub{color:var(--lighter-violet)}
.lead{font-size:22px;line-height:1.4;color:var(--lighter-violet)}
.card{background:var(--darker-gray);border-radius:14px;padding:20px 22px}
.row{display:flex;gap:16px}
.col{display:flex;flex-direction:column;gap:14px}
.t20{font-size:20px;font-weight:600;line-height:1.25}
.t16{font-size:16px;line-height:1.4}
.t18{font-size:18px;line-height:1.4}
.num{font-size:64px;font-weight:700;line-height:1}
.tag{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
  padding:4px 10px;border-radius:999px}
.pend{border:2px dashed var(--white);border-radius:14px;padding:16px 20px}
table{border-collapse:separate;border-spacing:0 6px;width:100%}
th{font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;text-align:left;
  padding:4px 18px;color:var(--lighter-violet)}
td{background:var(--darker-gray);padding:11px 18px;font-size:17px;line-height:1.3}
td:first-child{border-radius:12px 0 0 12px}td:last-child{border-radius:0 12px 12px 0}
a{color:inherit;text-decoration:underline;text-underline-offset:3px}
svg text{font-family:'Poppins',sans-serif}
.ui{position:fixed;right:18px;bottom:14px;display:flex;gap:8px;z-index:10}
.ui button{font-family:'Poppins',sans-serif;font-size:14px;font-weight:600;border:2px solid #EBEBFF;
  background:#280265;color:#EBEBFF;border-radius:999px;width:38px;height:38px;cursor:pointer}
.ui button:hover,.ui button:focus-visible{background:#EBEBFF;color:#280265;outline:none}
.watermark{position:absolute;right:-40px;bottom:-120px;width:460px;opacity:.08}
@media print{
  @page{size:1280px 720px;margin:0}
  html,body{overflow:visible;height:auto}
  .stage{position:static;width:auto;height:auto;transform:none!important}
  .slide{display:block!important;position:relative;break-after:page;page-break-after:always}
  .ui{display:none}
}
"""

# ---------------------------------------------------------------- JS
JS = """
(function(){
  var stage=document.getElementById('stage');
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var i=0;
  function fit(){
    var s=Math.min(innerWidth/1280,innerHeight/720);
    var x=(innerWidth-1280*s)/2,y=(innerHeight-720*s)/2;
    stage.style.transform='translate('+x+'px,'+y+'px) scale('+s+')';
  }
  function show(n){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach(function(s,k){s.classList.toggle('on',k===i)});
    try{history.replaceState(null,'','#'+(i+1))}catch(e){}
  }
  function go(d){show(i+d)}
  addEventListener('resize',fit);
  addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();go(1)}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(-1)}
    else if(e.key==='Home'){show(0)} else if(e.key==='End'){show(slides.length-1)}
    else if(e.key==='f'||e.key==='F'){
      if(!document.fullscreenElement){document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}
      else{document.exitFullscreen()}
    }
  });
  document.getElementById('prev').onclick=function(){go(-1)};
  document.getElementById('next').onclick=function(){go(1)};
  var h=parseInt((location.hash||'').slice(1),10);
  fit();show(isNaN(h)?0:h-1);
})();
"""

slides = []  # (kicker, title_html, body_html, source, kind)


def add(kick, title, body, src="", kind="content", top=None):
    slides.append((kick, title, body, src, kind, top))


def stepcard(w, num, title, desc, fill=False):
    st = ('background-color:var(--blue-accent);color:var(--black)' if fill
          else 'background-color:var(--darker-gray);color:var(--white)')
    return (f'<div style="{st};width:{w}px;border-radius:14px;padding:16px 16px;height:212px">'
            f'<div style="font-size:14px;font-weight:600;letter-spacing:.08em">{num}</div>'
            f'<div style="font-size:19px;font-weight:700;line-height:1.2;margin:4px 0 8px">{title}</div>'
            f'<div style="font-size:15px;line-height:1.35">{desc}</div></div>')


# =============================================================== 1 PROMESA
three = [("1", "Se compra un paquete de puntos al mes", "Tres paquetes: 114, 190 o 350 puntos al mes."),
         ("2", "Cada actividad cuesta los puntos de su tamaño", "1, 2, 3, 5, 8, 13 o 21, acordados antes de empezar."),
         ("3", "Se paga solo la tarea finalizada", "Entregada con PR aprobado y sin defectos pendientes. No se paga por horas, personas ni intentos de revisión.")]
add("Propuesta comercial · Generic API",
    f"Pago por actividades {hl('terminadas')}, no por horas",
    '<div class="lead" style="width:920px">Viva Aerobus compra puntos cada mes. Cada actividad cuesta los puntos de su tamaño '
    'y se paga cuando la tarea queda finalizada, en Ready for prod.</div>'
    '<div class="row" style="margin-top:26px">' +
    ''.join(
        f'<div class="card" style="flex:1;display:flex;flex-direction:column;gap:8px;min-height:190px">'
        f'<div class="num" style="font-size:44px;color:var(--blue-accent)">{n}</div>'
        f'<div style="font-size:21px;font-weight:700;line-height:1.2">{t}</div>'
        f'<div class="t16 sub">{d}</div></div>' for n, t, d in three) + '</div>',
    "Documento confidencial. Elaborado por Tech and Solve para Viva Aerobus.", "cover", top=340)

# =============================================================== 2 EJEMPLO SEPTIEMBRE
# Tareas del equipo (Daniel, Gabriel y Luis) con estado Finalizada/Finalizado en el informe de septiembre de 2026 (F1).
# Puntos calculados con v4/calculos/build_v4.py (horas reales H+I + 30 %). Se excluye API-1860 (implementada por un revisor).
SEPT = {21: ["API-1834", "API-1427"],
        13: ["API-1738", "API-1877"],
        8: ["API-1867", "API-1839"],
        5: ["API-1851"],
        2: ["API-1871", "API-1872"]}
SEPT_PTS = sum(p * len(v) for p, v in SEPT.items())
assert SEPT_PTS == 93 and sum(len(v) for v in SEPT.values()) == 9
tile_rows = ''.join(
    f'<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px">'
    f'<div style="flex:0 0 150px"><span style="font-size:26px;font-weight:700;color:var(--blue-accent)">{p}</span>'
    f'<span style="font-size:14px"> pts × {len(ids)} = {p*len(ids)}</span></div>'
    + ''.join(f'<div style="background-color:var(--darker-gray);color:var(--white);border-radius:8px;padding:8px 0;width:80px;text-align:center;font-size:13px;font-weight:600">{i}</div>' for i in ids)
    + '</div>' for p, ids in SEPT.items())
PK3 = [("Inicial", 114), ("Ampliado", 190), ("Avanzado", 350)]
K7 = 1.1
bars7 = []
for i, (n, v) in enumerate(PK3):
    y = 30 + i * 80
    full = v >= SEPT_PTS
    fill = "#22D0FF" if n == "Inicial" else "#EBEBFF"
    bars7.append(f'<rect x="0" y="{y}" width="400" height="70" rx="10" fill="#282E3F"/>')
    bars7.append(f'<rect x="8" y="{y+8}" width="{v*K7:.0f}" height="30" rx="6" fill="{fill}"/>')
    bars7.append(f'<text x="18" y="{y+29}" font-size="16" font-weight="700" fill="#000000">{n} · {v}</text>')
    cap = f"Cubre todo (sobran {v - SEPT_PTS})" if full else f"Cubre {v} de {SEPT_PTS} (faltan {SEPT_PTS - v})"
    bars7.append(f'<text x="10" y="{y+58}" font-size="14" font-weight="{700 if full else 400}" fill="#FFFFFF">{cap}</text>')
svg7b = ('<svg width="400" height="270" viewBox="0 0 400 270">'
         + ''.join(bars7) +
         f'<text x="8" y="16" font-size="14" font-weight="600" fill="#FFFFFF">Tareas finalizadas en septiembre: 93 puntos</text></svg>')
add("Ejemplo real · septiembre de 2026", f"Las tareas finalizadas en septiembre suman {hl('93 puntos')}",
    '<div class="row" style="gap:36px;align-items:flex-start">'
    '<div style="flex:0 0 600px">'
    '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px;color:var(--lighter-violet)">9 tareas marcadas «Finalizada» en el informe</div>'
    f'{tile_rows}</div>'
    '<div style="flex:1"><div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:6px;color:var(--lighter-violet)">Qué paquete la habría cubierto</div>'
    f'{svg7b}</div></div>'
        '<div class="card" style="margin-top:18px;border:2px solid var(--blue-accent);display:flex;gap:24px;align-items:center">'
    '<div style="font-size:20px;font-weight:700;flex:0 0 300px;line-height:1.25">Con el paquete Inicial, lo finalizado en septiembre se habría pagado completo</div>'
    '<div class="t16" style="color:var(--lighter-violet)">Las 9 tareas están marcadas «Finalizada» en el informe de seguimiento de septiembre. Suman 93 de los 114 puntos del paquete Inicial; '
    'sus puntos salen de las horas reales de cada tarea + 30&nbsp;%.</div></div>',
    "Septiembre de 2026 · F1 informe de septiembre (estado y horas reales). Puntos = horas reales + 30 %. No incluye API-1860, implementada por un revisor.", top=172)

# =============================================================== 2 HOY
cw, gap = 178, 14
cx = [cw / 2 + i * (cw + gap) for i in range(6)]
states = [("To Do", "otro equipo<br>estima en horas"), ("In Progress", "desarrollo y pruebas<br>del equipo"),
          ("In review", "revisión del PR<br>20 PRs en sept.<br><b>espera: no se mide</b>"), ("UAT", "prueba tras el<br>despliegue a prueba"),
          ("Ready for prod", "listo para producción:<br>el equipo terminó"), ("Done", "desplegado en<br>producción")]
cards = ''.join(
    f'<div class="card" style="width:{cw}px;padding:12px 14px;min-height:104px'
    f'{";border:2px solid var(--blue-accent)" if n == "In review" else ""}">'
    f'<div style="font-size:19px;font-weight:700;line-height:1.2">{n}</div>'
    f'<div style="font-size:14px;line-height:1.35;margin-top:4px;color:var(--lighter-violet)">{d}</div></div>'
    for n, d in states)
arrows = (
    f'<svg width="1152" height="70" viewBox="0 0 1152 70" style="display:block">'
    f'<g fill="none" stroke="#22D0FF" stroke-width="3">'
    f'<path d="M{cx[2]:.0f},0 V32 H{cx[1]+12:.0f} V8"/>'
    f'<path d="M{cx[3]:.0f},0 V58 H{cx[1]-12:.0f} V8"/></g>'
    f'<g fill="#22D0FF"><path d="M{cx[1]+12:.0f},0 l-7,12 h14z"/><path d="M{cx[1]-12:.0f},0 l-7,12 h14z"/></g>'
    f'<text x="{cx[2]+14:.0f}" y="30" font-size="15" font-weight="600" fill="#FFFFFF">44 desde In review</text>'
    f'<text x="{cx[3]+14:.0f}" y="56" font-size="15" font-weight="600" fill="#FFFFFF">2 desde UAT</text>'
    f'</svg>')


def chip(left, w, label):
    return (f'<div style="position:absolute;left:{left:.0f}px;width:{w:.0f}px;background-color:var(--darker-gray);color:var(--white);'
            f'border-radius:10px;padding:6px 10px;font-size:14px;font-weight:600;text-align:center;line-height:1.25">{label}</div>')


chips = ('<div style="position:relative;height:48px">'
         + chip(cx[0] - cw / 2, cw, "Se mide: horas estimadas · 659 h")
         + chip(cx[1] - cw / 2, cw, "Se mide: horas ejecutadas · 819 h")
         + chip(cx[2] - cw / 2, 2 * cw + gap, "Se mide: número de devoluciones · 41 en septiembre")
         + chip(cx[4] - cw / 2, cw, "Con la propuesta: se paga aquí").replace("background-color:var(--darker-gray);color:var(--white)", "background-color:var(--blue-accent);color:var(--black)")
         + '</div>')
stats = [("+169 h", "4 actividades con espera de revisión de más de 30 días hábiles (hasta 227) explican la desviación; las otras 21 suman −9 h."),
         ("12 de 19", "actividades con devoluciones cumplieron lo estimado: el número de devoluciones no separa cumplir de no cumplir."),
         ("8 de 19", "PRs mergeados con el Quality Gate de Sonar en rojo, y 7 PRs con pedidos distintos sobre evidencia: sin estándar de revisión.")]
add("1 · Cómo trabajamos hoy", f"Hoy se mide el esfuerzo; lo que frena la entrega es {hl('la espera de revisión')}",
    f'<div style="display:flex;gap:{gap}px">{cards}</div>' + arrows + chips +
    '<div class="row" style="margin-top:12px">' +
    ''.join(f'<div class="card" style="flex:1;padding:14px 20px"><div class="num" style="font-size:44px;color:var(--blue-accent)">{b}</div>'
            f'<div class="t16" style="margin-top:6px;color:var(--lighter-violet)">{d}</div></div>' for b, d in stats) + '</div>',
    "Septiembre de 2026, 26 actividades · F1 informe de septiembre · F3 Jira · F4 GitHub (lecturas del 9 de octubre de 2026).", top=172)

# =============================================================== 3 NUEVO RECORRIDO
w6 = 178
steps = [("1", "Diseño conjunto", "Se define la actividad con criterios de aceptación claros.", "Criterios de aceptación"),
         ("2", "Tamaño en puntos", "1, 2, 3, 5, 8, 13 o 21, en vez de horas.", "Tamaño acordado"),
         ("3", "Desarrollo", "Un PR por tarea con pruebas unitarias y Sonar. Sin pruebas no pasa a revisión.", "Quality Gate de Sonar"),
         ("4", "PR abierto", "Con descripción y evidencia estándar. Desde aquí corren los 5 días.", "Estándar de PR"),
         ("5", "PR aprobado", "Es la entrega. Viva responde en máx. 2 días hábiles; si no, se cuenta entregada.", "Espera de revisión"),
         ("6", "Ready for prod", "Se corrigen los defectos, máx. 5 días desde abierto el PR. Finalizada: se paga.", "Cumplimiento en la entrega")]
hero = ''.join(
    f'<div style="width:{w6}px">' + stepcard(w6, f"PASO {n}", t, d, fill=(n == "6")).replace("height:212px", "height:196px") +
    f'<div style="margin-top:8px;border-top:3px solid var(--blue-accent);padding-top:6px;font-size:12px;font-weight:600;'
    f'letter-spacing:.1em;text-transform:uppercase;color:var(--lighter-violet)">Se observa</div>'
    f'<div style="font-size:16px;font-weight:600;line-height:1.3;margin-top:2px">{o}</div></div>'
    for n, t, d, o in steps)
add("2 · Cómo trabajaremos", f"El nuevo recorrido: seis pasos y {hl('algo que se observa en cada uno')}",
    f'<div style="display:flex;gap:14px">{hero}</div>'
    '<div class="row" style="margin-top:16px">'
    '<div class="card" style="flex:0 0 380px;border:2px solid var(--blue-accent)"><div style="font-size:20px;font-weight:700">Qué se paga</div>'
    '<div class="t16" style="margin-top:6px;color:var(--lighter-violet)">Los puntos de cada tarea finalizada (Ready for prod), dentro de su paquete mensual de puntos. '
    'Si Viva Aerobus no da feedback en los 5 días, se cobra.</div></div>'
    '<div class="card" style="flex:1"><div style="font-size:20px;font-weight:700">Reglas de corrección y cambios</div>'
    '<ul style="margin:8px 0 0 18px;font-size:15px;line-height:1.45;color:var(--lighter-violet)">'
    '<li><b style="color:var(--white)">Defectos:</b> solo se ajusta lo que es un error de la implementación; el equipo corrige todos los que se reporten en las etapas posteriores.</li>'
    '<li><b style="color:var(--white)">Después de los 5 días</b> o ante cambios de alcance: control de cambios, que se cobra como tarea nueva con su propio tamaño.</li></ul></div></div>',
    "Propuesta de Tech and Solve. Referencias de los PRs de septiembre de 2026 (F4 GitHub): 2 días hábiles de revisión, Sonar y estándar de PR.", top=172)

# =============================================================== 4 OFERTA
flow4 = [("104", "actividades terminadas por el equipo"), ("3.220,5 h", "realmente invertidas"),
         ("4.186,65 h", "con +30 % de desviación"), ("983 puntos", "por rango de tamaño")]
arrow_svg = ('<svg width="30" height="24" viewBox="0 0 30 24" style="flex:0 0 30px;align-self:center"><path d="M2,12 H22 M14,4 L24,12 L14,20" fill="none" stroke="#22D0FF" stroke-width="3"/></svg>')
row_a = arrow_svg.join(
    f'<div class="card" style="flex:1;padding:12px 16px"><div class="num" style="font-size:30px;color:var(--blue-accent)">{b}</div>'
    f'<div style="font-size:14px;margin-top:4px;color:var(--lighter-violet)">{d}</div></div>' for b, d in flow4)
sz = [("1", "hasta 6 h"), ("2", "hasta 11 h"), ("3", "hasta 17 h"), ("5", "hasta 28 h"), ("8", "hasta 46 h"), ("13", "hasta 74 h"), ("21", "hasta 90 h")]
row_b = ''.join(
    f'<div class="card" style="flex:1;padding:10px 12px;text-align:center"><div style="font-size:28px;font-weight:700;color:var(--blue-accent);line-height:1">{p}</div>'
    f'<div style="font-size:13px;margin-top:4px">{h}</div></div>' for p, h in sz) + \
    '<div class="card" style="flex:1.3;padding:10px 12px;text-align:center"><div style="font-size:20px;font-weight:700;line-height:1.3">Dividir</div><div style="font-size:13px;margin-top:4px">más de 90 h</div></div>'
pk = [("Inicial", "para meses de menos carga", "114", "Jul.–sept. 2026: 1 de 3 meses lo alcanzó (97, 68 y 184).", ""),
      ("Ampliado", "cubre un mes como septiembre", "190", "Septiembre de 2026 (184 puntos) cabe completo.", ""),
      ("Avanzado", "máxima capacidad", "350", "Sin histórico: supera lo operado hasta hoy.", "")]
row_c = ''.join(
    f'<div class="card" style="flex:1;padding:14px 18px{";border:3px solid var(--blue-accent)" if i == 1 else ""}">'
    f'<div><div style="font-size:24px;font-weight:700;line-height:1.2">{n}</div><div style="font-size:14px;color:var(--lighter-violet)">{p}</div></div>'
    f'<div style="display:flex;align-items:baseline;gap:10px"><div class="num" style="font-size:56px;color:var(--blue-accent)">{pts}</div><div class="t16">puntos al mes</div></div>'
    f'<div class="t16" style="margin-top:4px">Máx.: {pts} × valor del punto</div>'
    f'<div style="font-size:14px;margin-top:6px;color:var(--lighter-violet)">{h}<br>{e}</div></div>'
    for i, (n, p, pts, h, e) in enumerate(pk)) + \
    '<div class="pend" style="flex:0 0 190px;padding:14px"><span class="tag" style="background-color:var(--white);color:var(--black)">Pendiente</span>' \
    '<div class="t16" style="margin-top:8px"><b>Valor del punto</b><br>se acuerda antes de empezar.</div></div>'
add("3 · Cómo se calcula", f"Tamaños y paquetes construidos con {hl('lo que ya entregamos')}",
    f'<div style="display:flex;gap:10px">{row_a}</div>'
    '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin:14px 0 6px;color:var(--lighter-violet)">Tamaño en puntos según horas reales + 30 %</div>'
    f'<div style="display:flex;gap:8px">{row_b}</div>'
    '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin:14px 0 6px;color:var(--lighter-violet)">Paquetes mensuales de puntos</div>'
    f'<div class="row" style="gap:24px">{row_c}</div>',
    "Sept. 2025 a sept. 2026 · F1 informe de septiembre, F3 Jira, F5 escala de puntos (práctica de industria).", top=172)

# =============================================================== 5 EVOLUCION Y CIERRE
cyc = [("1", "Medir", "Tareas finalizadas, cumplimiento, espera de revisión y Quality Gate."),
       ("2", "Detectar", "En qué paso se frenó cada actividad: revisión, rama base, ambigüedad o pruebas."),
       ("3", "Ajustar", "Tamaños, estándar de PR, reglas que automatiza Sonar y compromisos."),
       ("4", "Verificar", "El mes siguiente se comparan los mismos indicadores.")]
cw4 = 270
ccards = ''.join(stepcard(cw4, f"PASO {n}", t, d, fill=(n == "1")).replace("height:212px", "height:150px") for n, t, d in cyc)
loop = ('<svg width="1152" height="56" viewBox="0 0 1152 56" style="display:block;margin-top:4px">'
        '<path d="M1017,0 V28 H135 V8" fill="none" stroke="#22D0FF" stroke-width="3"/>'
        '<path d="M128,12 l7,-12 l7,12z" fill="#22D0FF"/>'
        '<text x="576" y="48" text-anchor="middle" font-size="15" font-weight="600" fill="#FFFFFF">Un ciclo por mes: lo que se verifica alimenta la siguiente medición</text></svg>')
route = [("Antes de empezar", "Viva Aerobus elige un paquete y entrega una muestra de tareas reales del backlog. Primera sesión de tamaños."),
         ("Mes 1", "Se opera con el paquete. Al cierre se comparan los tamaños con lo entregado y se ajustan si hace falta."),
         ("Cada mes", "Se repite el ciclo contra la línea base de septiembre. Si se necesitan más puntos, se elige un paquete mayor.")]
rc = ''.join(
    f'<div class="card" style="flex:1;padding:12px 18px;display:flex;gap:14px"><div style="flex:0 0 30px;width:30px;height:30px;border-radius:50%;background-color:var(--blue-accent);color:var(--black);'
    f'font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center">{i+1}</div>'
    f'<div><div style="font-size:18px;font-weight:700">{t}</div><div style="font-size:14px;line-height:1.35;margin-top:2px;color:var(--lighter-violet)">{d}</div></div></div>'
    for i, (t, d) in enumerate(route))
pend = ["Valor del punto", "Puntos del paquete que Viva Aerobus no use por no tener tareas definidas",
        "Días de aviso para cambiar de paquete", "Actividades en curso: 6 de las 26 de septiembre siguen abiertas"]
add("4 · Cómo evolucionamos", f"Cada mes medimos y mejoramos; {hl('empezamos con tareas reales')}",
    f'<div style="display:flex;gap:16px">{ccards}</div>{loop}'
    f'<div class="row" style="gap:12px">{rc}</div>'
    '<div class="row" style="margin-top:12px;gap:14px">'
    '<div class="card" style="flex:1.15;background-color:var(--blue-accent);color:var(--black)"><div style="font-size:14px;font-weight:600;letter-spacing:.1em;text-transform:uppercase">Siguiente paso</div>'
    '<div style="font-size:20px;font-weight:700;line-height:1.25;margin-top:4px">Elegir un paquete y entregar una muestra de tareas reales del backlog.</div></div>'
    '<div class="pend" style="flex:1.5;padding:12px 18px"><span class="tag" style="background-color:var(--white);color:var(--black)">Por definir juntos</span>'
    '<ul style="margin:8px 0 0 18px;font-size:14px;line-height:1.4">' + ''.join(f'<li>{p}</li>' for p in pend) + '</ul></div></div>',
    "Propuesta de Tech and Solve · Línea base: septiembre de 2026 (F1 informe, F3 Jira, F4 GitHub). Actividades abiertas al 9 de octubre de 2026.", top=172)

# ---------------------------------------------------------------- ENSAMBLE
total = len(slides)
out = []
for n, (kick, title, body, src_, kind, top) in enumerate(slides, 1):
    wm = '<img class="watermark" src="{{ISOTIPO_LIGHTER_VIOLET}}" alt="" aria-hidden="true">' if kind == "cover" else ""
    if kind == "cover":
        logo = '<img class="logo" style="left:64px;right:auto;top:44px;width:200px" src="{{LOGO_WHITE}}" alt="Tech and Solve logo">'
        head = (f'<div class="kick" style="top:160px">{kick}</div>'
                f'<h1 style="top:190px;width:900px;font-size:56px">{title}</h1>'
                f'<div class="body" style="top:{top or 390}px">{body}</div>')
    else:
        logo = '<img class="logo" src="{{LOGO_WHITE}}" alt="Tech and Solve logo">'
        head = f'<div class="kick">{kick}</div><h1>{title}</h1><div class="body" style="top:{top or 190}px">{body}</div>'
    out.append(
        f'<section class="slide" id="s{n}" style="background-color:var(--dark-violet);color:var(--white)" aria-label="Diapositiva {n} de {total}">'
        f'{wm}{logo}{head}'
        f'<div class="foot"><span class="src">{src_}</span><span>{n:02d} / {total:02d}</span></div></section>')

html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tech and Solve · Propuesta de paquetes de puntos para Generic API</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body style="background-color:var(--dark-violet);color:var(--white)">
<div class="stage" id="stage">
{''.join(out)}
</div>
<div class="ui"><button id="prev" aria-label="Anterior" type="button">&#8249;</button><button id="next" aria-label="Siguiente" type="button">&#8250;</button></div>
<script>{JS}</script>
</body></html>"""
open(sys.argv[1], "w", encoding="utf-8").write(html)
print("diapositivas:", total)
