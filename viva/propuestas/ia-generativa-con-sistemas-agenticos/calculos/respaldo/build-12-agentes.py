#!/usr/bin/env python3
"""Genera la presentación «Sistemas agénticos para el ciclo de desarrollo de Generic API».

Uso: python3 calculos/build.py            (escribe el HTML en la carpeta de la propuesta)

Solo lee el insumo de referencia (línea gráfica y logo de SURA «Dinámica de trabajo del equipo»);
no lo modifica. Todo el contenido está en este archivo; las fuentes de cada afirmación están en
CONTEXTO.md (§5 evidencia interna, §6 fuentes oficiales).
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI.parent / "tech-and-solve-propuesta-sistemas-agenticos.html"
REF = (AQUI.parents[3] / "SURA" / "gestores-sura" / "metodologia-trabajo" / "v2"
       / "Tech and Solve - Dinámica de trabajo del equipo-v2.html")

# Logo oficial: se toma del diseño de referencia (solo lectura).
_ref = REF.read_text(encoding="utf-8")
LOGO = re.search(r'--logo: url\("(data:image/[^"]+)"\)', _ref).group(1)

FOOT = "Sistemas agénticos para el ciclo de desarrollo · Generic API · Viva Aerobus"

# Fuentes oficiales de Anthropic (verificadas el 19 oct 2026; ver CONTEXTO.md §6)
U_SUB = "https://code.claude.com/docs/en/sub-agents"
U_HOOKS = "https://code.claude.com/docs/en/hooks-guide"
U_SKILLS = "https://code.claude.com/docs/en/skills"
U_MCP = "https://code.claude.com/docs/en/mcp"
U_PERM = "https://code.claude.com/docs/en/permissions"


def a(url, txt):
    return f'<a href="{url}">{txt}</a>'


CSS = """
:root {
  --violet: #280265; --violet-light: #EBEBFF; --accent: #5300DF; --amber: #B9720A;
  --green: #1B6B4F; --card: #FAF9FE; --text: #1A1E27; --text-2: #5B5A66; --border: #DCD8EC;
  --logo: url("%(logo)s");
}
* { box-sizing: border-box; }
html, body { margin: 0; background: #E6E4EE; font-family: "Poppins", Arial, sans-serif; color: var(--text); }
body { counter-reset: slide; padding: 24px 0 60px; }
.slide { container-type: inline-size; position: relative; width: min(1280px, 96vw); aspect-ratio: 16 / 9;
  margin: 0 auto 24px; background: #fff; overflow: hidden; counter-increment: slide;
  box-shadow: 0 4px 24px rgba(40, 2, 101, .12); scroll-snap-align: center; }
.in { position: absolute; inset: 0; padding: 3.4cqw 4.5cqw 5.2cqw; display: flex; flex-direction: column; font-size: 1.32cqw; line-height: 1.38; }
.internal .in { padding-top: 5.4cqw; }
.alert { position: absolute; top: 0; left: 0; right: 0; background: #B9720A; color: #fff; text-align: center; font-weight: 700; font-size: 1.15cqw; padding: .6cqw 0; z-index: 3; }
h2 { font-size: 2.6cqw; line-height: 1.2; color: var(--violet); margin: 0 0 1.6cqw; font-weight: 700; max-width: 95%%; }
h3 { font-size: 1.45cqw; color: var(--violet); margin: 0 0 .8cqw; font-weight: 700; line-height: 1.25; }
p { margin: 0 0 .7cqw; }
ul { margin: 0; padding-left: 1.4cqw; } li { margin-bottom: .6cqw; }
b, strong { font-weight: 600; }
.foot { position: absolute; left: 4.5cqw; right: 4.5cqw; bottom: 1.6cqw; display: flex; align-items: center; gap: 1.2cqw; font-size: .95cqw; color: var(--text-2); }
.foot::before { content: ""; width: 5cqw; height: 2.6cqw; background: var(--logo) left center / contain no-repeat; }
.foot::after { content: counter(slide); margin-left: auto; }
.src { margin-top: auto; font-size: .92cqw; color: var(--text-2); }
.src a, a { color: var(--accent); }
.muted { color: var(--text-2); }
.grid { display: grid; gap: 1.6cqw; }
.g2 { grid-template-columns: 1fr 1fr; } .g3 { grid-template-columns: repeat(3, 1fr); } .g4 { grid-template-columns: repeat(4, 1fr); }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 1cqw; padding: 1.4cqw 1.6cqw; }
.card.tint { background: var(--violet-light); border-color: var(--violet-light); }
.card.white { background: #fff; }
.dot { width: 3.2cqw; height: 3.2cqw; border-radius: 50%%; background: var(--accent); color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 1.3cqw; flex: none; }
.dot.sm { width: 2.6cqw; height: 2.6cqw; font-size: 1.05cqw; }
.pill { display: inline-block; border-radius: .5cqw; padding: .3cqw 1cqw; color: #fff; font-weight: 600; background: var(--accent); font-size: 1cqw; }
.pill.violet { background: var(--violet); }
.band { background: var(--violet-light); border-radius: 1cqw; padding: 1.1cqw 1.8cqw; color: var(--violet); font-weight: 600; font-size: 1.25cqw; }
.lead { font-size: 1.55cqw; color: var(--violet); font-weight: 600; line-height: 1.35; }
.k { font-size: .92cqw; font-weight: 700; color: var(--amber); letter-spacing: .06cqw; text-transform: uppercase; margin: .9cqw 0 .25cqw; }
.ag p { font-size: 1.12cqw; line-height: 1.4; margin: 0; }
.g2 .ag p { font-size: 1.32cqw; } .g2 .ag .k { font-size: 1.02cqw; margin-top: 1.2cqw; }
.g3 .ag p { font-size: 1.16cqw; } .g3 .ag .k { font-size: .98cqw; }
.g2 .ag .hd h3 { font-size: 1.7cqw; } .g2 .ag .rol { font-size: 1.1cqw; }
.ag .hd { display: flex; gap: .9cqw; align-items: center; margin-bottom: .2cqw; }
.ag .hd h3 { margin: 0; font-size: 1.4cqw; }
.ag .rol { font-size: 1cqw; color: var(--text-2); line-height: 1.2; }
.gr .n .rol { font-weight: 400; color: var(--text-2); font-size: .9cqw; }
.chips { display: flex; gap: .7cqw; align-items: center; margin: -.6cqw 0 1.3cqw; font-size: 1cqw; color: var(--text-2); }
table.t { width: 100%%; border-collapse: collapse; font-size: 1.28cqw; line-height: 1.3; }
.t th { background: var(--violet); color: #fff; text-align: left; font-weight: 600; padding: .6cqw .9cqw; }
.t td { border: 1px solid var(--border); padding: .8cqw .9cqw; background: var(--card); vertical-align: middle; }
.t td:first-child { font-weight: 600; color: var(--violet); }
.t.dense { font-size: 1.02cqw; } .t.dense td, .t.dense th { padding: .36cqw .8cqw; }
.est { font-weight: 700; } .est.ok { color: var(--green); } .est.pa { color: var(--amber); } .est.pr { color: var(--accent); }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.4cqw; margin-bottom: 1.5cqw; }
.step { position: relative; background: var(--card); border: 1px solid var(--border); border-radius: 1cqw; padding: 1.2cqw 1.4cqw; }
.step:not(:last-child)::after { content: ""; position: absolute; right: -1.85cqw; top: 50%%; margin-top: -.9cqw; width: 1.3cqw; height: 1.8cqw; background: var(--violet); clip-path: polygon(0 0, 100%% 50%%, 0 100%%); }
.step.dev { background: #FFF6E8; border-color: var(--amber); }
.step .who { font-size: .95cqw; font-weight: 700; letter-spacing: .06cqw; text-transform: uppercase; color: var(--accent); margin-bottom: .3cqw; }
.step.dev .who { color: var(--amber); }
.step h3 { margin: 0 0 .5cqw; font-size: 1.5cqw; }
.step p { font-size: 1.12cqw; margin: 0; line-height: 1.4; }
.notes { display: none; }
body.show-notes .notes { display: block; width: min(1280px, 96vw); margin: -14px auto 28px; background: #FFFBEF; border: 1px dashed var(--amber); padding: 10px 14px; font-size: 14px; color: var(--text-2); border-radius: 6px; }

/* Mapa: agentes por fase del flujo de Jira de Viva */
.gr { display: grid; grid-template-columns: 24.5cqw repeat(7, 1fr); border-bottom: 1px solid var(--border); height: 2.62cqw; }
.gr.h { height: auto; border-bottom: 0; margin-bottom: .5cqw; }
.gr .n { grid-column: 1; grid-row: 1; align-self: center; font-weight: 600; color: var(--violet); font-size: 1.02cqw; padding-right: .6cqw; line-height: 1.2; }
.gr .s { grid-row: 1; border-left: 1px solid var(--border); }
.gr .s.hl { background: var(--violet-light); }
.gr .bar { grid-row: 1; align-self: stretch; margin: .42cqw .22cqw; border-radius: .4cqw; background: var(--accent); z-index: 1; }
.gr .bar.tr { background: var(--amber); }
.gr .ph { grid-row: 1; background: var(--violet); color: #fff; text-align: center; font-weight: 600; font-size: .98cqw; padding: .55cqw 0; margin: 0 .15cqw; border-radius: .4cqw; line-height: 1.15; }
.legend { display: flex; gap: 2.6cqw; margin-top: .9cqw; font-size: 1cqw; color: var(--text-2); align-items: center; }
.legend i { display: inline-block; width: 2cqw; height: 1.05cqw; border-radius: .3cqw; margin-right: .6cqw; vertical-align: middle; }

@page { size: 13.333in 7.5in; margin: 0; }
@media print {
  body { background: #fff; padding: 0; }
  .slide { width: 13.333in; margin: 0; box-shadow: none; break-after: page; }
  .notes, .hint { display: none !important; }
}
.hint { position: fixed; right: 16px; bottom: 12px; font-size: 12px; color: var(--text-2); background: #fff; padding: 6px 10px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
""" % {"logo": LOGO}

JS = """
const slides = [...document.querySelectorAll('.slide')];
const current = () => slides.findIndex(s => s.getBoundingClientRect().bottom > innerHeight / 2);
addEventListener('keydown', e => {
  if (e.key === 'n' || e.key === 'N') document.body.classList.toggle('show-notes');
  const i = current();
  if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); slides[Math.min(i + 1, slides.length - 1)].scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); slides[Math.max(i - 1, 0)].scrollIntoView({ behavior: 'smooth', block: 'center' }); }
});
"""

SECCIONES = []


def lamina(titulo, cuerpo, src="", notas="", interna=False):
    alerta = ('<div class="alert">USO INTERNO · Esta lámina no se debe mostrar al cliente.</div>' if interna else "")
    fuente = f'<div class="src">{src}</div>' if src else ""
    SECCIONES.append(
        f'<section class="slide{" internal" if interna else ""}">{alerta}<div class="in">'
        f"<h2>{titulo}</h2>{cuerpo}{fuente}</div>"
        f'<div class="foot">{FOOT}</div></section>'
        f'<aside class="notes">{notas}</aside>'
    )


# Nombre funcional de cada agente (dice lo que hace) y un descriptor corto
APODO = {
    "Analista de actividades": ("Analista", "De la actividad en Jira"),
    "Conocimiento del sistema": ("Documentalista", "Del sistema y su código"),
    "Planificador de solución": ("Planificador", "De la solución"),
    "Implementador": ("Implementador", "Del cambio en código"),
    "Casos de prueba y evidencia": ("Probador", "Pruebas y evidencia"),
    "Verificador de evidencia": ("Verificador", "De la evidencia"),
    "Revisor previo": ("Revisor", "Previo a abrir el PR"),
    "Justificación del cambio": ("Defensor", "Justifica cada cambio"),
    "Retrabajo": ("Corrector", "Comentarios y feedback"),
    "Entrega a Jira": ("Publicador", "Entrega a Jira"),
    "Informe de avance": ("Informador", "Informe de avance"),
    "Trazabilidad": ("Trazador", "Trazabilidad"),
}


def agente(num, nombre, hace, recibe, decide):
    apodo = APODO[nombre][0]
    return (f'<div class="card ag"><div class="hd"><div class="dot sm">{num}</div><div><h3>{apodo}</h3><div class="rol">{APODO[nombre][1]}</div></div></div>'
            f'<div class="k">Qué hace</div><p>{hace}</p>'
            f'<div class="k">Qué recibe Viva Aerobus</div><p>{recibe}</p>'
            f'<div class="k">Quién decide</div><p>{decide}</p></div>')


def fases(*nombres):
    return ('<div class="chips">Fase del flujo de Viva Aerobus en Jira: '
            + "".join(f'<span class="pill violet">{n}</span>' for n in nombres) + "</div>")


def gana(txt):
    return f'<div class="band" style="margin-top:auto">{txt}</div>'


# =============================================================== Portada
SECCIONES.append(f"""<section class="slide"><div class="in" style="background:var(--violet);color:#fff;padding:5cqw 6cqw">
  <div style="width:13cqw;height:6.8cqw;background:#fff var(--logo) center / 85% no-repeat;border-radius:.8cqw"></div>
  <p style="margin:auto 0 1.2cqw;font-size:1.3cqw;letter-spacing:.15cqw;text-transform:uppercase;opacity:.8;font-weight:600">Propuesta de IA aplicada al desarrollo de software</p>
  <h1 style="font-size:4.4cqw;line-height:1.12;margin:0 0 2.4cqw;max-width:84cqw">Un agente de IA en cada fase del ciclo de desarrollo de Generic API</h1>
  <div style="font-size:1.9cqw;font-weight:600;line-height:1.4;max-width:74cqw">
    Qué agentes proponemos, qué hace cada uno y qué gana Viva Aerobus al tenerlos implementados, construidos sobre Claude, de Anthropic.
  </div>
  <div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:1.1cqw;opacity:.85;border-top:1px solid rgba(255,255,255,.25);padding-top:1.4cqw">
    <span>Viva Aerobus · Generic API<br>Propuesta comercial · Sugerencia de trabajo, debatible y ajustable</span>
    <span style="text-align:right">Tech and Solve · Octubre de 2026<br>Documento confidencial</span>
  </div>
</div></section>
<aside class="notes">Propuesta para los líderes de tecnología de Viva Aerobus: qué sistemas agénticos se pueden ofrecer sobre el ciclo de desarrollo que Viva ya tiene (Jira, GitHub, revisión de PR, UAT).</aside>""")

# Lámina retirada a pedido de Didier (19 oct 2026): resumen de tres beneficios. Se conserva comentada.
# # =============================================================== 2 Resumen
# lamina(
#     "Agentes que acompañan cada fase, con el desarrollador decidiendo en cada compuerta",
#     """<p class="lead" style="max-width:88%;margin-bottom:1.8cqw">Proponemos llevar a Generic API un conjunto de agentes de IA, construidos sobre Claude, que acompañan la actividad desde su definición en Jira hasta producción, sobre el flujo de trabajo que Viva Aerobus ya tiene.</p>
#     <div class="grid g3" style="gap:1.4cqw;margin-bottom:1.6cqw">
#       <div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">1</div><h3 style="margin:0">Llegan a revisión con el trabajo previo hecho</h3></div><p style="margin:0;font-size:1.45cqw">Cada actividad se revisa contra las guías de código del proyecto y se justifica antes de abrir el PR. La revisión se concentra en lo que solo una persona puede juzgar.</p></div>
#       <div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">2</div><h3 style="margin:0">Evidencia completa y verificada</h3></div><p style="margin:0;font-size:1.45cqw">Cada caso de la matriz de pruebas llega con su evidencia, y una verificación independiente la comprueba antes de entregar a UAT.</p></div>
#       <div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">3</div><h3 style="margin:0">Trazabilidad de punta a punta</h3></div><p style="margin:0;font-size:1.45cqw">Cada cambio se puede seguir hasta su actividad de Jira, su plan, su PR y su evidencia, desde la clave del ticket.</p></div>
#     </div>
#     <div class="band" style="margin-top:auto">Cada agente trabaja a petición del desarrollador, que certifica el resultado: ningún agente publica un PR ni mueve un ticket sin su aprobación.</div>""",
#     notas="Tres beneficios de tener los agentes implementados. Son propiedades del proceso, no promesas de cifra: la medición se propone en la lámina 13.",
# )

# =============================================================== 3 Mapa
FASES = ["To Do análisis", "To Do", "In Progress", "In review", "UAT", "Ready for prod", "Done"]
# (nombre, [(col_inicio, ancho)], transversal)
FILAS = [
    ("Analista de actividades", [(1, 1)], False),
    ("Conocimiento del sistema", [(1, 1), (6, 2)], False),
    ("Planificador de solución", [(3, 1)], False),
    ("Implementador", [(3, 1)], False),
    ("Casos de prueba y evidencia", [(3, 1)], False),
    ("Verificador de evidencia", [(3, 1)], False),
    ("Revisor previo", [(3, 1)], False),
    ("Justificación del cambio", [(3, 2)], False),
    ("Retrabajo", [(4, 2)], False),
    ("Entrega a Jira", [(4, 1)], False),
    ("Informe de avance", [(3, 3)], True),
    ("Trazabilidad", [(1, 7)], True),
]


def fila_mapa(nombre, barras, transv):
    celdas = "".join(f'<div class="s{" hl" if c == 3 else ""}" style="grid-column:{c + 1}"></div>' for c in range(1, 8))
    bs = "".join(f'<div class="bar{" tr" if transv else ""}" style="grid-column:{ini + 1} / span {ancho}"></div>' for ini, ancho in barras)
    apodo, rol = APODO[nombre]
    return f'<div class="gr"><div class="n">{apodo} <span class="rol">· {rol}</span></div>{celdas}{bs}</div>'


cab = '<div class="gr h"><div class="n"></div>' + "".join(
    f'<div class="ph" style="grid-column:{i + 2}">{f}</div>' for i, f in enumerate(FASES)) + "</div>"
lamina(
    "Dónde entra cada agente en el flujo de trabajo de Viva Aerobus",
    f"""<div>{cab}{"".join(fila_mapa(*f) for f in FILAS)}</div>
    <div class="legend"><span><i style="background:var(--accent)"></i>Actúa en la fase</span>
      <span><i style="background:var(--amber)"></i>Acompaña de forma transversal</span>
      <span><i style="background:var(--violet-light);border:1px solid var(--border)"></i>Trabajo previo a que el equipo de revisión vea el PR</span></div>""",
    src="Propuesta de Tech and Solve construida sobre el flujo de Jira y GitHub que Viva Aerobus ya usa.",
    notas="El flujo es el de Viva (To Do análisis, To Do, In Progress, In review, UAT, Ready for prod, Done). La zona sombreada es donde los agentes hacen el trabajo previo a la revisión. La lámina 3 muestra el recorrido y las láminas 5 a 9 detallan cada agente.",
)


# =============================================================== 4 Diagrama de flujo
SW, GAP = 160, 40


def X(i):
    return i * (SW + GAP)


def nodo(i, cy, apodo, rol, tipo="ag", w=SW, cx=None):
    x = X(i) if cx is None else cx - w / 2
    fill = {"ag": "var(--accent)", "viva": "var(--green)", "per": "var(--amber)"}[tipo]
    return (f'<rect x="{x}" y="{cy - 31}" width="{w}" height="62" rx="9" style="fill:{fill}"/>'
            f'<text x="{x + w / 2}" y="{cy - 4}" text-anchor="middle" class="fn">{apodo}</text>'
            f'<text x="{x + w / 2}" y="{cy + 15}" text-anchor="middle" class="fr">{rol}</text>')


def flecha(x1, y1, x2, y2, dash=False, ambas=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    ini = ' marker-start="url(#ah)"' if ambas else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="fl"{d}{ini} marker-end="url(#ah)"/>'


R1, R2, R3, RV = 52, 192, 332, 452
cxs = lambda i: X(i) + SW / 2
svg = ['<svg viewBox="0 0 1160 545" xmlns="http://www.w3.org/2000/svg" style="width:93%;display:block;margin:0 auto">',
       '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:var(--violet)"/></marker></defs>',
       '<style>.fn{font:700 15px Poppins,Arial,sans-serif;fill:#fff}.fr{font:400 11px Poppins,Arial,sans-serif;fill:#fff}.fl{stroke:var(--violet);stroke-width:2;fill:none}.ft{font:400 11px Poppins,Arial,sans-serif;fill:var(--text-2)}.fb{font:600 11px Poppins,Arial,sans-serif;fill:var(--violet)}.fd{font:700 13px Poppins,Arial,sans-serif;fill:var(--violet)}</style>']
# fila 1: izquierda a derecha
svg += [nodo(0, R1, "Actividad en Jira", "Viva Aerobus la define", "viva"), nodo(1, R1, "Analista", "De la actividad en Jira")]
cd = cxs(2)
svg.append(f'<polygon points="{cd},{R1 - 42} {cd + 80},{R1} {cd},{R1 + 42} {cd - 80},{R1}" style="fill:var(--violet-light);stroke:var(--violet);stroke-width:2"/>'
           f'<text x="{cd}" y="{R1 + 5}" text-anchor="middle" class="fd">¿Hay bloqueos?</text>')
svg += [nodo(3, R1, "Planificador", "De la solución"), nodo(4, R1, "Valida el plan", "El desarrollador", "per"), nodo(5, R1, "Implementador", "Del cambio en código")]
for i in (0, 1):
    svg.append(flecha(X(i) + SW, R1, X(i + 1), R1))
svg.append(flecha(X(1) + SW, R1, cd - 80, R1))
svg.append(flecha(cd + 80, R1, X(3), R1))
svg.append(f'<text x="{cd + 100}" y="{R1 - 7}" text-anchor="middle" class="fb">no</text>')
svg.append(f'<text x="{cd}" y="{R1 + 62}" text-anchor="middle" class="ft">sí: preguntas a Viva Aerobus, vuelve al Analista</text>')
for i in (3, 4):
    svg.append(flecha(X(i) + SW, R1, X(i + 1), R1))
# baja del Implementador al Probador
svg.append(flecha(cxs(5), R1 + 31, cxs(5), R2 - 31))
# fila 2: derecha a izquierda
svg += [nodo(5, R2, "Probador", "Pruebas y evidencia"), nodo(4, R2, "Verificador", "De la evidencia"),
        nodo(3, R2, "Revisor", "Previo a abrir el PR"), nodo(2, R2, "Defensor", "Justifica cada cambio"),
        nodo(1, R2, "Aprueba publicar", "El desarrollador", "per"), nodo(0, R2, "Publicador", "Entrega a Jira")]
for i in (5, 4, 3, 2, 1):
    svg.append(flecha(X(i), R2, X(i - 1) + SW, R2))
svg.append(f'<text x="{cxs(4)}" y="{R2 + 50}" text-anchor="middle" class="ft">sin evidencia, no avanza</text>')
svg.append(f'<text x="{cxs(3)}" y="{R2 + 50}" text-anchor="middle" class="ft">hallazgos vuelven al Implementador</text>')
svg.append(flecha(cxs(0), R2 + 31, cxs(0), R3 - 31))
# fila 3
svg += [nodo(0, R3, "Revisión del PR", "Equipo de revisión de Viva", "viva"), nodo(1, R3, "UAT", "Viva Aerobus certifica", "viva"),
        nodo(2, R3, "Producción", "Ready for prod · Done", "viva"), nodo(3, R3, "Documentalista", "Del sistema y su código")]
for i in (0, 1, 2):
    svg.append(flecha(X(i) + SW, R3, X(i + 1), R3))
# corrector
vcx = (cxs(0) + cxs(1)) / 2
svg.append(nodo(0, RV, "Corrector", "Plan de ajuste, aprobado por el desarrollador", "ag", w=300, cx=vcx))
svg.append(flecha(cxs(0), R3 + 31, cxs(0), RV - 31, dash=True, ambas=True))
svg.append(flecha(cxs(1), R3 + 31, cxs(1), RV - 31, dash=True, ambas=True))
svg.append(f'<text x="{cxs(0) + 8}" y="{(R3 + RV) / 2 + 4}" class="ft">comentarios</text>')
svg.append(f'<text x="{cxs(1) + 8}" y="{(R3 + RV) / 2 + 4}" class="ft">feedback</text>')
# transversales
svg.append(f'<text x="{(cxs(4) + cxs(5)) / 2}" y="{R3 - 46}" text-anchor="middle" class="fb">Acompañan toda la actividad</text>')
for i, (ap, rol) in ((4, ("Informador", "Informe de avance")), (5, ("Trazador", "Trazabilidad"))):
    x = X(i)
    svg.append(f'<rect x="{x}" y="{R3 - 31}" width="{SW}" height="62" rx="9" style="fill:var(--violet-light);stroke:var(--amber);stroke-width:2.5"/>'
               f'<text x="{x + SW / 2}" y="{R3 - 4}" text-anchor="middle" class="fn" style="fill:var(--violet)">{ap}</text>'
               f'<text x="{x + SW / 2}" y="{R3 + 15}" text-anchor="middle" class="fr" style="fill:var(--violet)">{rol}</text>')
# leyenda
ly = 530
svg.append(f'<rect x="{X(2)}" y="{ly - 11}" width="22" height="12" rx="3" style="fill:var(--accent)"/><text x="{X(2) + 30}" y="{ly}" class="ft">Agente</text>'
           f'<rect x="{X(2) + 100}" y="{ly - 11}" width="22" height="12" rx="3" style="fill:var(--green)"/><text x="{X(2) + 130}" y="{ly}" class="ft">Viva Aerobus</text>'
           f'<rect x="{X(2) + 250}" y="{ly - 11}" width="22" height="12" rx="3" style="fill:var(--amber)"/><text x="{X(2) + 280}" y="{ly}" class="ft">Decide el desarrollador</text>'
           f'<rect x="{X(2) + 440}" y="{ly - 11}" width="22" height="12" rx="3" style="fill:var(--violet-light);stroke:var(--amber);stroke-width:2"/><text x="{X(2) + 470}" y="{ly}" class="ft">Transversal</text>')
svg.append("</svg>")
lamina(
    "El recorrido de una actividad por cada agente",
    "".join(svg),
    notas="Se lee de izquierda a derecha en la primera fila, de derecha a izquierda en la segunda y otra vez de izquierda a derecha en la tercera. Las cajas ámbar son las compuertas donde decide el desarrollador; las verdes son lo que hace Viva Aerobus en su flujo.",
)


# =============================================================== 5 Cómo se usa un agente
def paso(num, quien, titulo, texto, dev=False):
    return (f'<div class="step{" dev" if dev else ""}"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw">'
            f'<div class="dot sm" style="background:{"var(--amber)" if dev else "var(--accent)"}">{num}</div>'
            f'<div><div class="who">{quien}</div></div></div><h3>{titulo}</h3><p>{texto}</p></div>')


lamina(
    "El agente trabaja a petición; el desarrollador certifica",
    '<div class="steps">'
    + paso("1", "Desarrollador", "Pide", "Invoca al agente sobre una actividad y define qué espera recibir.", dev=True)
    + paso("2", "Agente", "Trabaja", "Lee el contexto (Jira, GitHub y código) y prepara su resultado dentro de los permisos que se le dieron.")
    + paso("3", "Agente", "Entrega y se detiene", "Presenta lo preparado con su evidencia y con lo que no pudo verificar.")
    + paso("4", "Desarrollador", "Certifica", "Comprueba que es lo que esperaba recibir: lo acepta, pide un ajuste o lo descarta.", dev=True)
    + "</div>"
    '<div class="grid g2" style="gap:1.6cqw;margin-bottom:1cqw">'
    '<div class="card tint"><h3>Sigue siendo del desarrollador</h3><ul style="font-size:1.2cqw">'
    "<li><b>Definir qué espera recibir</b> antes de pedirlo.</li>"
    "<li><b>Certificar</b> que lo entregado es lo esperado: el agente no certifica su propio trabajo.</li>"
    "<li><b>Aprobar</b> el plan y la publicación: el PR, la evidencia en Jira y los cambios de estado.</li>"
    "<li><b>Responder por el cambio</b> ante el equipo de revisión y ante Viva Aerobus.</li></ul></div>"
    '<div class="card"><h3>El agente no hace</h3><ul style="font-size:1.2cqw">'
    "<li>Publicar un PR ni mover un ticket sin aprobación del desarrollador.</li>"
    "<li>Dar por hecho un paso que le toca al desarrollador.</li>"
    "<li>Completar con supuestos: lo que no puede verificar, lo dice («no consta»).</li></ul></div></div>",
    src=f"Práctica de Tech and Solve. Como referencia, Claude Code, en su modo manual, pide aprobación antes de modificar archivos o ejecutar la mayoría de los comandos: {a(U_PERM, 'documentación oficial de permisos')} (Anthropic).",
    notas="Es la idea central: el agente trabaja a petición del desarrollador y entrega; el desarrollador comprueba que es lo que esperaba y solo entonces se publica. La responsabilidad por el cambio nunca pasa al agente.",
)

# =============================================================== 4 Análisis
lamina(
    "Antes de codificar, el análisis valida la actividad",
    fases("To Do análisis", "To Do") + '<div class="grid g2" style="gap:1.6cqw;margin-bottom:1.4cqw">'
    + agente("1", "Analista de actividades",
             "Lee la actividad en Jira y la contrasta con el código real: qué módulos toca, si la actividad cubre ese impacto y si es viable. Si hay bloqueos, se detiene y no escribe código.",
             "Un veredicto (lista, con preguntas o bloqueada) con las preguntas priorizadas y la evidencia que las respalda.",
             "Viva Aerobus responde las preguntas; el desarrollador decide si la actividad continúa.")
    + agente("2", "Conocimiento del sistema",
             "Mantiene un mapa de Generic API derivado del código, donde cada afirmación cita la ruta que la respalda. Se actualiza con cada cambio que llega a la rama principal.",
             "Respuestas sobre cómo funciona el sistema, con la ruta del código como respaldo. Lo que no consta se marca como «no consta».",
             "El desarrollador; el agente no completa con supuestos lo que el código no muestra.")
    + "</div>"
    + gana("Lo que gana Viva Aerobus: las dudas sobre una actividad llegan antes de escribir código, no durante la revisión del PR."),
    notas="El análisis termina en una compuerta: sin bloqueos, se avanza; con bloqueos, se devuelven preguntas. El mapa del sistema es la base que usan los demás agentes.",
)

# =============================================================== 5 Construcción
lamina(
    "En construcción, el plan y el código siguen las guías del proyecto",
    fases("In Progress") + '<div class="grid g2" style="gap:1.6cqw;margin-bottom:1.4cqw">'
    + agente("3", "Planificador de solución",
             "Propone el diseño, las alternativas consideradas, el impacto y un plan por pasos que cita las guías de código que debe cumplir.",
             "Un plan validado antes de codificar, con el radio de impacto y los riesgos identificados.",
             "El desarrollador valida el plan antes de que comience la implementación.")
    + agente("4", "Implementador",
             "Escribe el cambio según el plan y las guías de código de Generic API, tomadas de sus revisiones de PR, y reutiliza lo que ya existe antes de crear algo nuevo. Solo arranca con un veredicto favorable del análisis.",
             "Un cambio en su rama, con commits trazables a la actividad.",
             "El desarrollador revisa el cambio y responde por él.")
    + "</div>"
    + gana("Lo que gana Viva Aerobus: un cambio que sigue el plan aprobado y las guías del proyecto, con cada paso trazable a la actividad."),
    notas="Las guías de código del proyecto son el estándar contra el que se planea, se implementa y se revisa.",
)

# =============================================================== 6 Pruebas
lamina(
    "Cada caso de prueba llega con su evidencia comprobada",
    fases("In Progress", "In review") + '<div class="grid g2" style="gap:1.6cqw;margin-bottom:1.4cqw">'
    + agente("5", "Casos de prueba y evidencia",
             "A partir de la matriz de casos de prueba del ticket, prepara los casos y el paquete de evidencia (ejecuciones, capturas y una tarjeta por caso) en el formato que Viva Aerobus pide en Jira.",
             "Evidencia por cada fila de la matriz, lista para cargarse al ticket. Las pruebas unitarias automatizadas son opcionales, según lo que Viva Aerobus habilite.",
             "Quien implementa ejecuta y valida; Viva Aerobus certifica en UAT.")
    + agente("6", "Verificador de evidencia",
             "Revisa de forma independiente que cada fila de la matriz tenga su evidencia. Una etiqueta de «aprobado» no basta: tiene que haber una prueba que la respalde.",
             "Un veredicto por cada fila, con el archivo que lo respalda.",
             "El desarrollador corrige lo que falte antes de pasar a revisión.")
    + "</div>"
    + gana("Lo que gana Viva Aerobus: llegar a revisión y a UAT con evidencia por cada caso de prueba, verificada antes de entregar."),
    notas="Se parte de la matriz de casos de prueba del ticket, que es lo que Viva ya exige. Las pruebas automatizadas quedan como opción: hay que confirmar con Viva si las habilita.",
)

# =============================================================== 7 Revisión
lamina(
    "Tres agentes acompañan el PR, antes y durante la revisión",
    fases("In Progress (cierre)", "In review", "UAT") + '<div class="grid g3" style="gap:1.3cqw;margin-bottom:1.2cqw">'
    + agente("7", "Revisor previo",
             "Revisa el cambio completo antes de abrir el PR: propósito, corrección, impacto sobre otros módulos, diseño, estilo, pruebas y seguridad. Aplica además el estilo que usa el equipo de revisión. Se propone sumar el resultado de Sonar.",
             "Un veredicto con hallazgos; los bloqueantes se corrigen antes del PR.",
             "El desarrollador corrige o justifica cada hallazgo.")
    + agente("8", "Justificación del cambio",
             "Documenta cada cambio del PR: quién lo pidió, por qué ese enfoque, qué otros puntos toca y si rompe contratos. Un cambio sin origen citable se marca como no justificado.",
             "Una justificación por cambio, con su fuente, para el PR.",
             "El desarrollador responde por cada cambio o lo revierte.")
    + agente("9", "Retrabajo",
             "Cuando llegan comentarios de revisión o feedback de UAT, primero lee sin modificar nada, clasifica los comentarios y propone un plan de ajuste.",
             "El plan de ajuste y respuestas sugeridas a cada comentario.",
             "El desarrollador aprueba el plan antes de que se ejecute.")
    + "</div>"
    + gana("Lo que gana Viva Aerobus: el equipo de revisión recibe un PR ya revisado y justificado, y cada comentario recibe una respuesta planeada."),
    notas="Este es el frente de las devoluciones. No se promete una reducción: se propone medir las devoluciones por actividad en el informe de seguimiento (lámina 13). Sonar es una propuesta; hoy el equipo de revisión no lo usa como criterio.",
)

# =============================================================== 8 Entrega y reporte
lamina(
    "Entrega, informe de avance y trazabilidad salen preparados",
    fases("In review", "UAT", "Ready for prod", "Done") + '<div class="grid g3" style="gap:1.3cqw;margin-bottom:1.2cqw">'
    + agente("10", "Entrega a Jira",
             "Sube la evidencia al ticket, comenta el PR y mueve la actividad. Siempre hace primero un ensayo que muestra lo que va a hacer.",
             "El ticket con su evidencia y el enlace al PR, completos.",
             "El desarrollador aprueba la publicación; el agente no actúa sin ese permiso.")
    + agente("11", "Informe de avance",
             "Prepara el borrador del informe diario con lo que se puede verificar: estado del ticket, devoluciones del PR y evidencias cargadas.",
             "Un borrador en el formato que Viva Aerobus pide hoy.",
             "El desarrollador completa avance y próximo paso, y lo envía.")
    + agente("12", "Trazabilidad",
             "Une en un registro por actividad el ticket, el plan, los commits, el PR, la evidencia y las respuestas de revisión.",
             "Un registro consultable desde la clave de Jira.",
             "El desarrollador; el registro solo recoge lo que ocurrió.")
    + "</div>"
    + gana("Lo que gana Viva Aerobus: el estado, las devoluciones y la evidencia de cada actividad en un mismo lugar, con el borrador del informe ya preparado."),
    notas="El informe de avance y la trazabilidad hacia Viva son propuestas nuevas; la entrega a Jira ya sigue el mismo principio de ensayo previo y aprobación. Ver el estado de cada agente en la lámina interna 15.",
)

# =============================================================== 9 Problemas
def problema(num, titulo, hoy, agentes, cambia, mide):
    return (f'<div class="card" style="padding:1.3cqw 1.5cqw"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.6cqw"><div class="dot sm">{num}</div><h3 style="margin:0">{titulo}</h3></div>'
            f'<div class="k" style="margin-top:.4cqw">Hoy</div><p style="font-size:1.2cqw;margin:0">{hoy}</p>'
            f'<div class="k">Agentes</div><p style="font-size:1.2cqw;margin:0">{agentes}</p>'
            f'<div class="k">Qué cambia</div><p style="font-size:1.2cqw;margin:0">{cambia}</p>'
            f'<div class="k">Cómo lo veremos</div><p style="font-size:1.2cqw;margin:0">{mide}</p></div>')


lamina(
    "Cada agente responde a un problema concreto del flujo actual",
    '<div class="grid g3" style="gap:1.3cqw">'
    + problema("1", "Devoluciones en la revisión del PR",
               "Cada ronda de comentarios del equipo de revisión cuenta como una devolución.",
               "Planificador, Revisor, Defensor y Corrector.",
               "El PR llega revisado contra las guías y justificado; los comentarios que llegan se atienden con un plan.",
               "Devoluciones por actividad, con la fuente que ya existe en los PR.")
    + problema("2", "Pruebas y evidencias",
               "Viva Aerobus exige pruebas manuales y su evidencia cargada en cada actividad de Jira.",
               "Probador, Verificador y Publicador.",
               "Cada fila de la matriz llega con su evidencia, comprobada de forma independiente.",
               "Filas de la matriz con evidencia verificada, sobre el total de filas.")
    + problema("3", "Calidad y trazabilidad",
               "Cada desarrollador envía a diario un informe de avance y evidencias por actividad.",
               "Analista, Documentalista, Informador y Trazador.",
               "Se sabe qué se cambió, por qué y con qué evidencia, y el informe sale preparado.",
               "PR con Sonar en verde y actividades con trazabilidad completa.")
    + "</div>"
    + '<p class="muted" style="margin-top:auto;font-size:1.05cqw">No prometemos una cifra de mejora: proponemos medirla con el informe de seguimiento desde el primer mes (lámina 13).</p>',
    notas="Los tres problemas se tomaron del modelo de trabajo actual de Viva. «Hoy» describe ese modelo, no una comparación con cifras.",
)

# =============================================================== 10 Cómo se construye
lamina(
    "Construidos sobre las capacidades documentadas de Claude",
    '<p class="lead" style="margin-bottom:1.4cqw">Esta es la documentación oficial de Anthropic sobre los bloques con que se construye un agente en Claude Code. Lo que construimos encima, con las guías y los controles de Generic API, es de Tech and Solve.</p>'
    '<div class="grid g2" style="gap:1.4cqw">'
    f'<div class="card"><h3>Subagentes</h3><p style="margin:0">Cada agente corre con su propio contexto, sus instrucciones, las herramientas que se le permiten y sus propios permisos, y devuelve solo un resumen. Se definen en archivos de texto. {a(U_SUB, "Documentación oficial")}.</p></div>'
    f'<div class="card"><h3>Skills</h3><p style="margin:0">Paquetes de instrucciones reutilizables, definidos en un archivo, que se cargan solo cuando hacen falta; por ejemplo, el procedimiento de revisión de un PR. {a(U_SKILLS, "Documentación oficial")}.</p></div>'
    f'<div class="card"><h3>Hooks</h3><p style="margin:0">Comandos que se ejecutan siempre en puntos definidos del ciclo, para que ciertas acciones ocurran sin depender de que el modelo decida hacerlas. {a(U_HOOKS, "Documentación oficial")}.</p></div>'
    f'<div class="card"><h3>MCP (Model Context Protocol)</h3><p style="margin:0">Estándar abierto para conectar al agente con herramientas como el gestor de tareas o el repositorio. La documentación recomienda conectar solo servidores de confianza. {a(U_MCP, "Documentación oficial")}.</p></div>'
    "</div>",
    src="Fuente: documentación oficial de Claude Code, Anthropic (code.claude.com). Es documentación del fabricante sobre su propio producto: describe prácticas y capacidades, no una norma. Sin versiones: las capacidades se verifican en la documentación vigente.",
    notas="Cada bloque tiene su enlace oficial en la misma lámina. La documentación del fabricante es práctica documentada, no estándar. No se citan modelos ni versiones.",
)

# =============================================================== 11 Control humano
lamina(
    "El agente se detiene, pide aprobación y cita su evidencia",
    '<div class="grid g3" style="gap:1.4cqw;margin-bottom:1.4cqw">'
    '<div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">1</div><h3 style="margin:0">Se detiene ante un bloqueo</h3></div><p style="margin:0">El análisis termina en una compuerta. Si hay dudas sin resolver, el agente devuelve preguntas y no escribe código.</p></div>'
    '<div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">2</div><h3 style="margin:0">Lee primero, actúa con permiso</h3></div><p style="margin:0">El agente lee Jira y GitHub. Publicar un PR, subir evidencia o mover un ticket requiere la aprobación del desarrollador, y antes se muestra un ensayo de lo que va a ocurrir.</p></div>'
    '<div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">3</div><h3 style="margin:0">Cada afirmación lleva su evidencia</h3></div><p style="margin:0">Cita el ticket, el comentario o la ruta del código que la respalda. Lo que no se puede verificar se dice: «no consta».</p></div>'
    "</div>"
    f'<p class="muted" style="margin-bottom:.6cqw">Estas prácticas son de Tech and Solve. Se apoyan en controles que la documentación oficial de Claude Code describe: reglas de permisos que definen qué puede hacer el agente ({a(U_PERM, "documentación de permisos")}) y hooks que ejecutan comandos en puntos del ciclo con control determinista ({a(U_HOOKS, "documentación de hooks")}).</p>'
    + gana("Los agentes aceleran el trabajo previo; la responsabilidad de cada entrega sigue siendo del desarrollador."),
    src="Fuente: documentación oficial de Claude Code, Anthropic (code.claude.com): permisos y hooks. Práctica documentada del fabricante, no una norma.",
    notas="Aquí se responde a la pregunta de un líder de tecnología: ¿qué pasa si el agente se equivoca? Se detiene ante bloqueos, no publica sin aprobación y deja evidencia. La práctica es nuestra; los controles de permisos y hooks son los que documenta Anthropic.",
)

# =============================================================== 12 Medición
lamina(
    "Medimos el efecto con el informe de seguimiento de Viva",
    '<p class="lead" style="margin-bottom:1.3cqw">Antes de activar cada agente se toma una línea base con los meses ya registrados; después se compara con las mismas definiciones.</p>'
    '<table class="t"><tr><th style="width:26%">Indicador</th><th style="width:44%">Cómo se mide</th><th>Fuente</th></tr>'
    "<tr><td>Devoluciones por actividad</td><td>Rondas de comentarios del equipo de revisión en el PR de cada actividad.</td><td>GitHub y informe de seguimiento</td></tr>"
    "<tr><td>Evidencia verificada</td><td>Filas de la matriz de casos de prueba con evidencia verificada al entrar a revisión, sobre el total de filas.</td><td>Jira</td></tr>"
    "<tr><td>Sonar en verde</td><td>PR cuyo resultado de calidad en Sonar queda aprobado al entrar a revisión.</td><td>GitHub</td></tr>"
    "<tr><td>Trazabilidad completa</td><td>Actividades con ticket, plan, PR y evidencia enlazados entre sí.</td><td>Jira y GitHub</td></tr></table>"
    '<p class="muted" style="margin:1.2cqw 0 0">Propuesta de medición, a acordar con Viva Aerobus. Si alguna fuente no permite calcular un indicador, se dice y no se estima.</p>',
    notas="No hay hoy una medición del efecto de los agentes; se propone construirla. Los indicadores salen del modelo de trabajo del cliente (devoluciones, evidencias en Jira, Sonar en el pipeline).",
)

# =============================================================== 13 Entrada y decisiones
lamina(
    "Cómo entra a Generic API y qué decidimos juntos",
    '<div class="grid g2" style="gap:1.8cqw;flex:1">'
    '<div><h3>Un orden sugerido, no un calendario</h3><div class="grid" style="gap:.9cqw">'
    '<div class="card" style="display:flex;gap:1cqw;align-items:flex-start"><div class="dot sm">1</div><div><b style="color:var(--violet)">Primero, lo que trabaja antes del PR</b><br><span class="muted">Analista, Planificador, Probador, Verificador y Revisor: no cambian el flujo que Viva Aerobus ya tiene.</span></div></div>'
    '<div class="card" style="display:flex;gap:1cqw;align-items:flex-start"><div class="dot sm">2</div><div><b style="color:var(--violet)">Después, lo que se ve en Jira</b><br><span class="muted">Publicador, Informador y Trazador, con el formato que Viva Aerobus defina.</span></div></div>'
    '<div class="card" style="display:flex;gap:1cqw;align-items:flex-start"><div class="dot sm">3</div><div><b style="color:var(--violet)">Al final, el ajuste con lo medido</b><br><span class="muted">Se revisan los indicadores y se decide qué agente seguir, cambiar o dejar.</span></div></div>'
    "</div></div>"
    '<div><h3>Lo que necesitamos de Viva Aerobus</h3><div class="grid" style="gap:.9cqw">'
    '<div class="card tint"><b style="color:var(--violet)">Acceso de lectura</b><br><span>A Jira y GitHub de Generic API, para que los agentes lean el contexto de cada actividad.</span></div>'
    '<div class="card tint"><b style="color:var(--violet)">La guía de revisión del equipo</b><br><span>La que aplica el equipo de revisión, para tomarla como base del Revisor.</span></div>'
    '<div class="card tint"><b style="color:var(--violet)">Decisiones por tomar</b><br><span>Si se habilitan pruebas automatizadas, si Sonar entra al Revisor y qué indicadores se miden.</span></div>'
    "</div></div></div>",
    notas="No se dan plazos: el orden es una sugerencia. Las dependencias de Viva son accesos, la guía de revisión y tres decisiones. El plazo de cada una lo declara su dueño.",
)

# =============================================================== 14 Interna: estado y evidencia
fila = lambda ag, est, cls, ev: f'<tr><td>{APODO[ag][0]} · {APODO[ag][1]}</td><td class="est {cls}">{est}</td><td>{ev}</td></tr>'
lamina(
    "Estado de cada agente y la evidencia que lo respalda",
    '<table class="t dense"><tr><th style="width:30%">Agente de la propuesta</th><th style="width:14%">Estado</th><th>Evidencia en LLMCoder (solo lectura)</th></tr>'
    + fila("Analista de actividades", "Opera", "ok", "process/phase-00 a 04; process/ANALYZE-TASK.md; .claude/agents/requirement-analyst.md")
    + fila("Conocimiento del sistema", "Opera", "ok", ".claude/agents/doc-sync.md; process/SYNC.md; documents/")
    + fila("Planificador de solución", "Opera", "ok", "process/phase-05-planning.md (fase del proceso, no subagente propio)")
    + fila("Implementador", "Opera", "ok", "process/phase-06-implementation.md; CLAUDE.md (compuerta y reglas)")
    + fila("Casos de prueba y evidencia", "Opera", "ok", "process/phase-07-testing.md; tools/evidence/EVIDENCE-FORMAT.md. Pruebas automatizadas: no consta")
    + fila("Verificador de evidencia", "Opera", "ok", ".claude/agents/tc-evidence-auditor.md")
    + fila("Revisor previo", "Opera, sin Sonar", "pa", "process/REVIEW-CODE.md; phase-09-pre-review.md. Sonar solo en guía PRC-38, no en el validador")
    + fila("Justificación del cambio", "Opera", "ok", ".claude/commands/defend-changes.md; work/API-1738/defend-2026-09-05.md")
    + fila("Retrabajo", "Opera", "ok", ".claude/commands/continue.md; work/API-1738/continue-plan-2026-09-22.md")
    + fila("Entrega a Jira", "Opera", "ok", "process/annex-d-agent-execution.md §D.2; tools/jira-sync/README.md")
    + fila("Informe de avance", "Propuesta", "pr", "No consta en LLMCoder")
    + fila("Trazabilidad", "Parcial", "pa", "work/&lt;KEY&gt;/ y work/README.md indexan por ticket; no hay vista para Viva Aerobus")
    + "</table>",
    src="Ruta base: /Users/didierfranco/Documents/GitHubViva/VivaAerobus.Generic.ApiLLMCoder. Actividades con carpeta de trabajo: API-1711, API-1738, API-1834, API-1858. «Opera» significa que existe en el proceso; no consta que cada paso haya corrido en cada PR.",
    notas="Lámina interna. Separa lo que ya existe en nuestro proceso de lo que se propone. No se muestra al cliente ni se nombra el repositorio ante él.",
    interna=True,
)

# =============================================================== 15 Interna: límites
lamina(
    "Lo que no se dice al cliente y lo que falta verificar",
    '<div class="grid g3" style="gap:1.3cqw">'
    '<div class="card tint ag"><h3>No se dice al cliente</h3><ul style="font-size:1.3cqw"><li>El repositorio LLMCoder ni su nombre.</li><li>Cuántas reglas, fases o agentes tiene nuestro proceso interno.</li><li>Nombres de personas ni cuántas trabajan en el equipo.</li><li>Que algo «ya opera»: se presenta como propuesta.</li><li>Modelos ni versiones de Claude.</li></ul></div>'
    '<div class="card ag"><h3>No consta o falta verificar</h3><ul style="font-size:1.3cqw"><li>Ninguna medición del efecto en devoluciones, tiempos o defectos: no se afirma reducción.</li><li>Que cada paso haya corrido en cada PR de Viva: solo hay cuatro carpetas de trabajo.</li><li>Pruebas automatizadas: el contexto de Generic API dice que el cliente no las permite; la propuesta de paquetes pone pruebas unitarias sin límite.</li><li>Sonar: no forma parte del validador de revisión.</li></ul></div>'
    '<div class="card ag"><h3>Decisiones y fuentes</h3><ul style="font-size:1.3cqw"><li>Confirmado por Didier (19 oct): se nombra «Claude Code» y se dice que las guías se toman de las revisiones de PR de Generic API.</li><li>No se cita «Building Effective AI Agents»: trae una nota de que el panorama cambió.</li><li>No se cita Managed Agents: está en beta.</li></ul></div>'
    "</div>",
    notas="Lámina interna. Resume los límites de lo que se dice y los pendientes antes de presentar.",
    interna=True,
)

HTML = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tech and Solve - Sistemas agénticos para Generic API</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{chr(10).join(SECCIONES)}
<div class="hint">← → para navegar · N notas · Ctrl/Cmd+P para PDF</div>
<script>{JS}</script>
</body>
</html>
"""

SALIDA.write_text(HTML, encoding="utf-8")
print(f"{SALIDA.name}: {HTML.count('<section class=\"slide')} láminas, {len(HTML) // 1024} KB")
