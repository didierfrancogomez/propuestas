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
.t.dense { font-size: 1.12cqw; } .t.dense td, .t.dense th { padding: .45cqw .8cqw; }
.est { font-weight: 700; } .est.ok { color: var(--green); } .est.pa { color: var(--amber); } .est.pr { color: var(--accent); }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.4cqw; margin-bottom: 1.5cqw; }
.step { position: relative; background: var(--card); border: 1px solid var(--border); border-radius: 1cqw; padding: 1.2cqw 1.4cqw; }
.step:not(:last-child)::after { content: ""; position: absolute; right: -1.85cqw; top: 50%%; margin-top: -.9cqw; width: 1.3cqw; height: 1.8cqw; background: var(--violet); clip-path: polygon(0 0, 100%% 50%%, 0 100%%); }
.step.dev { background: #FFF6E8; border-color: var(--amber); }
.step .who { font-size: .95cqw; font-weight: 700; letter-spacing: .06cqw; text-transform: uppercase; color: var(--accent); margin-bottom: .3cqw; }
.step.dev .who { color: var(--amber); }
.step h3 { margin: 0 0 .5cqw; font-size: 1.5cqw; }
.step p { font-size: 1.12cqw; margin: 0; line-height: 1.4; }
.dolor { display: flex; justify-content: space-between; align-items: center; gap: 1.8cqw; flex: 1 1 0; max-height: 15cqw; background: var(--card); border: 1px solid var(--border); border-radius: 1cqw; padding: 1.2cqw 1.6cqw; }
.dolor .dl { flex: 1; }
.dolor h3 { margin: 0 0 .5cqw; font-size: 1.7cqw; }
.dolor p { margin: 0; font-size: 1.3cqw; color: var(--text-2); line-height: 1.38; }
.dolor .dr { flex: none; text-align: right; min-width: 15cqw; }
.dolor .num { font-size: 2.1cqw; font-weight: 700; color: var(--accent); line-height: 1.15; }
.dolor .tr { font-size: 1.05cqw; font-weight: 600; color: var(--text-2); margin-top: .3cqw; }
.dolor .tr.up { color: var(--amber); } .dolor .tr.dn { color: var(--green); }
.chipag { display: inline-block; background: var(--violet-light); color: var(--violet); border: 1px solid #CFC8F5; font-weight: 600; font-size: 1.1cqw; border-radius: 99px; padding: .25cqw 1.1cqw; margin: .1cqw .6cqw .1cqw 0; }
.t.plain th { background: var(--violet-light); color: var(--violet); }
.t.plain td { background: #fff; }
.t.plain td:first-child { font-weight: 400; color: var(--text); }
.c4 .dolor { padding: .6cqw 1.4cqw; } .c4 .dolor h3 { font-size: 1.35cqw; margin-bottom: .15cqw; } .c4 .dolor p { font-size: 1.08cqw; line-height: 1.3; } .c4 .dolor .num { font-size: 1.6cqw; } .c4 .dolor .tr { font-size: .95cqw; margin-top: .1cqw; } .c4 { gap: .8cqw !important; }
.pre { display: flex; gap: 1cqw; align-items: flex-start; margin-bottom: 1.5cqw; }
.pre p { margin: 0; font-size: 1.38cqw; line-height: 1.4; }
.pre p b { color: var(--violet); }
.notes { display: none; }
body.show-notes .notes { display: block; width: min(1280px, 96vw); margin: -14px auto 28px; background: #FFFBEF; border: 1px dashed var(--amber); padding: 10px 14px; font-size: 14px; color: var(--text-2); border-radius: 6px; }

/* Mapa: agentes por fase del flujo de Jira de Viva */
.gr { display: grid; grid-template-columns: 24.5cqw repeat(7, 1fr); border-bottom: 1px solid var(--border); height: 3.3cqw; }
.gr.h { height: auto; border-bottom: 0; margin-bottom: .5cqw; }
.gr .n { grid-column: 1; grid-row: 1; align-self: center; font-weight: 600; color: var(--violet); font-size: 1.3cqw; padding-right: .6cqw; line-height: 1.2; }
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


def fases(*nombres):
    return ('<div class="chips">Fase del flujo de Viva Aerobus en Jira: '
            + "".join(f'<span class="pill violet">{n}</span>' for n in nombres) + "</div>")


def gana(txt):
    return f'<div class="band" style="margin-top:auto">{txt}</div>'


# =============================================================== Portada
SECCIONES.append(f"""<section class="slide"><div class="in" style="background:var(--violet);color:#fff;padding:5cqw 6cqw">
  <div style="width:13cqw;height:6.8cqw;background:#fff var(--logo) center / 85% no-repeat;border-radius:.8cqw"></div>
  <h1 style="font-size:5.4cqw;line-height:1.12;margin:auto 0 0;max-width:80cqw">Desarrollo de Generic API con sistemas agénticos</h1>
  <div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:1.1cqw;opacity:.85;border-top:1px solid rgba(255,255,255,.25);padding-top:1.4cqw">
    <span>Viva Aerobus · Generic API</span>
    <span style="text-align:right">Tech and Solve · Octubre de 2026<br>Documento confidencial</span>
  </div>
</div></section>
<aside class="notes">Propuesta para los líderes de tecnología de Viva Aerobus: seis agentes, uno por fase del ciclo de desarrollo que Viva ya tiene (Jira, GitHub, revisión de PR, UAT). En cada fase el desarrollador pide el trabajo y certifica el resultado. Construidos sobre Claude, de Anthropic.</aside>""")

# Lámina retirada a pedido de Didier (19 oct 2026): «Cuatro fases del ciclo de desarrollo, un agente en cada una». Se conserva comentada.
# # =============================================================== 2 Cuatro fases (mapa)
# FASES = ["To Do análisis", "To Do", "In Progress", "In review", "UAT", "Ready for prod", "Done"]
# AGENTES = [  # (nombre, descriptor, [(col_inicio, ancho)])
#     ("Análisis", "Cuando se recibe una actividad: entiende el alcance antes de escribir código.", [(1, 2)]),
#     ("Implementador de código", "Construye lo que piden los criterios de aceptación y automatiza sus pruebas unitarias.", [(3, 1)]),
#     ("Validador de calidad", "Comprueba Sonar, estilos y convenciones del código.", [(3, 1)]),
#     ("Publicador", "Prepara el PR con toda la evidencia y los pasos del pipeline.", [(3, 2)]),
# ]
#
#
# def fila_mapa(nombre, barras):
#     celdas = "".join(f'<div class="s{" hl" if c == 3 else ""}" style="grid-column:{c + 1}"></div>' for c in range(1, 8))
#     bs = "".join(f'<div class="bar" style="grid-column:{ini + 1} / span {ancho}"></div>' for ini, ancho in barras)
#     return f'<div class="gr"><div class="n">{nombre}</div>{celdas}{bs}</div>'
#
#
# cab = '<div class="gr h"><div class="n"></div>' + "".join(
#     f'<div class="ph" style="grid-column:{i + 2}">{f}</div>' for i, f in enumerate(FASES)) + "</div>"
# tarjetas = "".join(
#     f'<div class="card tint" style="padding:1.4cqw 1.3cqw"><div style="display:flex;gap:.7cqw;align-items:center;margin-bottom:.5cqw"><div class="dot sm">{i + 1}</div>'
#     f'<h3 style="margin:0;font-size:1.5cqw;line-height:1.2">{n}</h3></div><p style="margin:0;font-size:1.4cqw">{d}</p></div>'
#     for i, (n, d, _) in enumerate(AGENTES))
# lamina(
#     "Cuatro fases del ciclo de desarrollo, un agente en cada una",
#     f"""<div>{cab}{"".join(fila_mapa(n, b) for n, _, b in AGENTES)}</div>
#     <div class="legend" style="margin-bottom:1.6cqw"><span><i style="background:var(--accent)"></i>Actúa en la fase</span>
#       <span><i style="background:var(--violet-light);border:1px solid var(--border)"></i>Trabajo previo a que el equipo de revisión vea el PR</span></div>
#     <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:1.4cqw">{tarjetas}</div>""",
#     src="Propuesta de Tech and Solve construida sobre el flujo de Jira y GitHub que Viva Aerobus ya usa.",
#     notas="El flujo es el de Viva (To Do análisis, To Do, In Progress, In review, UAT, Ready for prod, Done). Los cuatro agentes trabajan antes de que el equipo de revisión vea el PR; el Publicador lo deja listo al cierre de In Progress.",
# )

# =============================================================== 3 Diagrama de flujo (tres franjas)
NW, NH = 124, 78
NWV = 132


def nodo(cx, cy, nombre, rol, tipo="ag", w=None):
    fill = {"ag": "var(--accent)", "viva": "var(--green)"}[tipo]
    w = w or (NWV if tipo == "viva" else NW)
    x = cx - w / 2
    lineas = nombre.split("|")
    y0 = cy - 3 - (len(lineas) - 1) * 8
    nom = "".join(f'<text x="{cx}" y="{y0 + i * 16}" text-anchor="middle" class="fn">{t}</text>' for i, t in enumerate(lineas))
    return (f'<rect x="{x}" y="{cy - NH / 2}" width="{w}" height="{NH}" rx="10" style="fill:{fill}"/>' + nom
            + f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" class="fr">{rol}</text>')


def flecha(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="fl" marker-end="url(#ah)"/>'


def pastilla(cx, cy, txt, w=92):
    return (f'<rect x="{cx - w / 2}" y="{cy - 14}" width="{w}" height="28" rx="14" style="fill:var(--amber)"/>'
            f'<text x="{cx}" y="{cy + 4.5}" text-anchor="middle" class="fp">{txt}</text>')


def franja(x, w, titulo, tipo):
    est = ("fill:var(--green);fill-opacity:.09;stroke:var(--green)" if tipo == "viva"
           else "fill:var(--violet-light);stroke:var(--accent)")
    col = "var(--green)" if tipo == "viva" else "var(--accent)"
    return (f'<rect x="{x}" y="2" width="{w}" height="432" rx="14" style="{est};stroke-width:2"/>'
            f'<text x="{x + w / 2}" y="33" text-anchor="middle" class="fh" style="fill:{col}">{titulo}</text>')


# franjas: Viva (entrega) · Tech and Solve (agentes) · Viva (revisión, UAT, producción)
B1, B2, B3 = (0, 148), (162, 716), (894, 266)
AX = [240, 380, 520, 660, 800]    # centros de los cinco agentes, en orden de invocación
V1, V3 = 74, 1027                 # centros de los nodos de las franjas de Viva
RO = 104                          # fila del Orquestador: por ahí entra y sale la característica
RA = 306                          # fila de los agentes
svg = ['<div style="flex:1;display:flex;align-items:center;margin-bottom:1cqw"><svg viewBox="0 0 1160 480" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block">',
       '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:var(--violet)"/></marker></defs>',
       '<style>.fn{font:700 13.5px Poppins,Arial,sans-serif;fill:#fff}.fr{font:400 11px Poppins,Arial,sans-serif;fill:#fff}.fl{stroke:var(--violet);stroke-width:2.2;fill:none}.ft{font:400 12px Poppins,Arial,sans-serif;fill:var(--text-2)}.fp{font:700 12px Poppins,Arial,sans-serif;fill:#fff}.fh{font:700 16px Poppins,Arial,sans-serif}.fb{font:700 12px Poppins,Arial,sans-serif;fill:var(--accent)}</style>']
svg += [franja(*B1, "Viva Aerobus", "viva"), franja(*B2, "Tech and Solve", "ag"), franja(*B3, "Viva Aerobus", "viva")]
# el Orquestador (también es un agente) orquesta todo el flujo: toma la característica, invoca a los demás agentes y la lleva a revisión
OX, OW = AX[0] - NW / 2, AX[-1] + NW / 2 - (AX[0] - NW / 2)
svg.append(f'<rect x="{OX}" y="{RO - 33}" width="{OW}" height="66" rx="10" style="fill:var(--accent)"/>'
           f'<text x="{OX + OW / 2}" y="{RO - 4}" text-anchor="middle" class="fn" style="font-size:16px">Orquestador</text>'
           f'<text x="{OX + OW / 2}" y="{RO + 17}" text-anchor="middle" class="fr" style="font-size:12px">Orquesta todo el flujo: toma la característica, invoca a los agentes y la lleva a revisión</text>')
# franja 1: Viva entrega la característica al Orquestador
svg.append(nodo(V1, RO, "Característica", "Viva la entrega en Jira", "viva"))
svg.append(flecha(V1 + NWV / 2, RO, OX, RO))
# franja 2: los cinco agentes, invocados por el Orquestador (flecha punteada: invoca y recibe el resultado)
AGENTES = [("Analista", "Entiende el alcance", "Valida"), ("Implementador", "Código y sus pruebas", "Certifica"),
           ("Pruebas|funcionales", "Evidencia en Jira", "Certifica"), ("Validador", "Calidad y cobertura", "Certifica"),
           ("Publicador", "Prepara el PR", "Certifica")]
for i, (cx, (nom, rol, gate)) in enumerate(zip(AX, AGENTES)):
    svg.append(f'<line x1="{cx}" y1="{RO + 33}" x2="{cx}" y2="{RA - NH / 2}" class="fl" stroke-dasharray="6 4" marker-start="url(#ah)" marker-end="url(#ah)"/>')
    svg.append(nodo(cx, RA, nom, rol))
    svg.append(f'<circle cx="{cx - NW / 2 + 6}" cy="{RA - NH / 2 + 6}" r="13" style="fill:#fff;stroke:var(--accent);stroke-width:2"/>'
               f'<text x="{cx - NW / 2 + 6}" y="{RA - NH / 2 + 11}" text-anchor="middle" class="fb">{i + 1}</text>')
    svg.append(pastilla(cx, RA + NH / 2 + 26, gate, w=96))
# del Orquestador a la revisión del PR de Viva
svg.append(flecha(OX + OW, RO, V3 - NWV / 2, RO))
svg.append(pastilla((OX + OW + V3 - NWV / 2) / 2, RO, "Aprueba PR", w=88))
# franja 3: revisión, UAT y producción, a igual distancia
RUAT, RPRO = RO + 114, RO + 228
svg += [nodo(V3, RO, "Revisión del PR", "Equipo de revisión", "viva"),
        nodo(V3, RUAT, "UAT", "Viva certifica", "viva"),
        nodo(V3, RPRO, "Producción", "Ready for prod · Done", "viva")]
svg.append(flecha(V3, RO + NH / 2, V3, RUAT - NH / 2))
svg.append(flecha(V3, RUAT + NH / 2, V3, RPRO - NH / 2))
# leyenda
ly = 466
svg.append(f'<rect x="0" y="{ly - 11}" width="22" height="12" rx="3" style="fill:var(--accent)"/><text x="30" y="{ly}" class="ft">Agente</text>'
           f'<rect x="120" y="{ly - 11}" width="22" height="12" rx="3" style="fill:var(--green)"/><text x="150" y="{ly}" class="ft">Viva Aerobus</text>'
           f'<rect x="290" y="{ly - 11}" width="22" height="12" rx="7" style="fill:var(--amber)"/><text x="320" y="{ly}" class="ft">Decide el desarrollador</text>'
           f'<text x="560" y="{ly}" class="ft">La flecha punteada es una invocación, y el número, su orden</text>')
svg.append("</svg></div>")
lamina(
    "La característica va a Tech and Solve y vuelve a Viva",
    "".join(svg) + gana("Cada agente se detiene al terminar, y el desarrollador certifica antes de que la característica avance."),
    notas="Se lee de izquierda a derecha en tres franjas: Viva Aerobus entrega una característica; el orquestador de Tech and Solve la toma, invoca internamente a los agentes analista, implementador, pruebas funcionales, validador y Publicador, y la lleva a revisión, y el desarrollador certifica cada salida; Viva Aerobus hace la revisión del PR, la UAT y el paso a producción. Los ajustes tras la revisión son una propuesta: los atiende el desarrollador, con el Implementador si lo pide.",
)


# =============================================================== 4 Cómo se usa un agente
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
    "<li><b>Aprobar</b> el plan y la publicación del PR.</li>"
    "<li><b>Responder por el cambio</b> ante el equipo de revisión y ante Viva Aerobus.</li></ul></div>"
    '<div class="card"><h3>El agente no hace</h3><ul style="font-size:1.2cqw">'
    "<li>Publicar un PR ni mover un ticket sin aprobación del desarrollador.</li>"
    "<li>Dar por hecho un paso que le toca al desarrollador.</li>"
    "<li>Completar con supuestos: lo que no puede verificar, lo dice («no consta»).</li></ul></div></div>",
    src=f"Práctica de Tech and Solve. Como referencia, Claude Code, en su modo manual, pide aprobación antes de modificar archivos o ejecutar la mayoría de los comandos: {a(U_PERM, 'documentación oficial de permisos')} (Anthropic).",
    notas="Es la idea central: el agente trabaja a petición del desarrollador y entrega; el desarrollador comprueba que es lo que esperaba y solo entonces se avanza. La responsabilidad por el cambio nunca pasa al agente.",
)


# =============================================================== 5 a 9 Un agente por lámina
def lamina_agente(titulo, chips, hace, recibe, decide, gana_txt, apoyo="", depende="", notas=""):
    pasos = "".join(
        f'<div style="display:flex;gap:1cqw;align-items:flex-start;margin-bottom:1.5cqw"><div class="dot sm" style="margin-top:.1cqw">{i + 1}</div>'
        f'<div style="font-size:1.55cqw;line-height:1.4">{t}</div></div>' for i, t in enumerate(hace))
    izq = (f'<div class="card" style="flex:1"><div class="k" style="margin-top:0">Qué hace</div><div style="margin-top:.7cqw">{pasos}</div>'
           + (f'<p class="muted" style="font-size:1.2cqw;margin:.6cqw 0 0">{apoyo}</p>' if apoyo else "") + "</div>")
    der = (f'<div class="card tint"><div class="k" style="margin-top:0">Qué recibe Viva Aerobus</div><p style="font-size:1.45cqw;margin:0">{recibe}</p></div>'
           f'<div class="card tint"><div class="k" style="margin-top:0">Quién decide</div><p style="font-size:1.45cqw;margin:0">{decide}</p></div>'
           + (f'<div class="card" style="border-color:var(--amber)"><div class="k" style="margin-top:0">Depende de Viva Aerobus</div><p style="font-size:1.45cqw;margin:0">{depende}</p></div>' if depende else ""))
    lamina(titulo, fases(*chips)
           + f'<div style="display:grid;grid-template-columns:58fr 38fr;gap:1.6cqw;flex:1;min-height:0;margin-bottom:1.2cqw"><div style="display:flex;flex-direction:column">{izq}</div>'
           f'<div style="display:flex;flex-direction:column;gap:1cqw">{der}</div></div>' + gana(gana_txt), notas=notas)


# Láminas retiradas a pedido de Didier (19 oct 2026): la definición de cada agente (Orquestador, Analista, Implementador, Validador y Publicador). Se conservan comentadas.
# lamina_agente(
#     "Orquestador: coordina a los agentes y las compuertas",
#     ["To Do análisis", "To Do", "In Progress", "In review"],
#     ["Toma la característica que entrega Viva Aerobus y se la asigna al Analista para que empiece.",
#      "Invoca a cada agente en orden y le pasa lo que necesita del anterior: el análisis al Implementador, el cambio al Validador y todo el recorrido al Publicador.",
#      "Comprueba cada compuerta antes de avanzar, y ante un bloqueo o un hallazgo detiene la cadena y devuelve el trabajo al agente que corresponde.",
#      "Lleva el estado de la característica y, cuando el Publicador termina, la lleva a la revisión del PR de Viva Aerobus."],
#     "Un resumen del estado de la característica y de lo que entregó cada agente, siempre al día, y el PR listo para la revisión.",
#     "El desarrollador pide el avance, certifica cada compuerta y decide si la característica sigue.",
#     "Lo que gana Viva Aerobus: la característica avanza por las compuertas en orden y se sabe en qué fase está y qué entregó cada agente.",
#     notas="El orquestador lo pidió Didier sin definirlo (19 oct 2026): la definición es nuestra, por confirmar. En LLMCoder el proceso interno ya orquesta las fases con compuertas y lleva un tablero de estado por actividad.",
# )
# lamina_agente(
#     "Analista: al recibir una actividad, entiende el alcance antes de escribir código",
#     ["To Do análisis", "To Do"],
#     ["Lee la actividad en Jira: su descripción, los criterios de aceptación y los comentarios.",
#      "La contrasta con el código real: qué módulos toca y qué otros puntos pueden verse afectados.",
#      "Verifica que los criterios cubran ese impacto y que la actividad sea viable.",
#      "Si quedan dudas, se detiene y las devuelve como preguntas priorizadas, sin escribir código."],
#     "Un veredicto (lista, con preguntas o bloqueada), con el impacto identificado y la evidencia que lo respalda.",
#     "El desarrollador decide si la actividad continúa; Viva Aerobus responde las preguntas.",
#     "Lo que gana Viva Aerobus: las dudas sobre una actividad llegan antes de escribir código, no durante la revisión del PR.",
#     apoyo="Se apoya en un mapa del sistema derivado del código, donde cada afirmación cita la ruta que la respalda; lo que no consta se marca como «no consta».",
#     notas="El análisis termina en una compuerta: sin bloqueos se avanza; con bloqueos se devuelven preguntas. Es lo primero que ocurre cuando se recibe una actividad para desarrollar.",
# )
# lamina_agente(
#     "Implementador de código: construye y prueba sobre los criterios",
#     ["In Progress"],
#     ["Solo arranca si el análisis fue favorable, y toma los criterios de aceptación como contrato de lo que hay que construir.",
#      "Propone un plan por pasos y lo somete al desarrollador antes de escribir código.",
#      "Implementa con las guías de código de Generic API, tomadas de sus revisiones de PR, y reutiliza lo que ya existe.",
#      "Escribe pruebas unitarias automatizadas para cada criterio y para los casos límite, las ejecuta y deja el resultado completo, también cuando una prueba falla."],
#     "Un cambio en su rama, con commits trazables a la actividad, el plan en el que se basó y sus pruebas unitarias automatizadas con el resultado de su ejecución.",
#     "El desarrollador valida el plan y certifica que el código y sus pruebas son lo que esperaba recibir.",
#     "Lo que gana Viva Aerobus: un cambio que responde a los criterios de aceptación, sigue las guías del proyecto y llega con sus pruebas unitarias automatizadas.",
#     notas="El Implementador no inventa un estándar propio: aplica las guías de código del proyecto. Las pruebas unitarias van dentro de este mismo agente. Validar con Didier que ligar cada paso del plan a su criterio de aceptación es práctica que se puede prometer.",
# )
# lamina_agente(
#     "Validador de calidad: comprueba Sonar, estilos y convenciones",
#     ["In Progress"],
#     ["Aplica el perfil de estilo del equipo de revisión a los archivos del cambio y comprueba que no queden diferencias en las líneas que el cambio tocó.",
#      "Revisa el cambio contra las convenciones de código de Generic API: estilo, arquitectura y robustez.",
#      "Lee el resultado de Sonar sobre el código nuevo: sin issues nuevos, sin security hotspots y sin duplicación.",
#      "Devuelve al desarrollador lo que esté en rojo, con la regla que no se cumple."],
#     "Un veredicto con el estado de estilo, convenciones y Sonar, y la lista de lo que hay que corregir.",
#     "El desarrollador corrige o justifica cada hallazgo, y certifica que el cambio queda limpio.",
#     "Lo que gana Viva Aerobus: un cambio que llega al PR con estilo, convenciones y Sonar ya verificados.",
#     notas="El estilo y las convenciones ya se verifican en nuestro proceso. Leer el resultado de Sonar es propuesta: hoy el equipo de revisión no lo usa como criterio, así que hay que acordarlo con Viva.",
# )
# lamina_agente(
#     "Publicador: prepara el PR con toda la evidencia y los pasos del pipeline",
#     ["In Progress", "In review"],
#     ["Arma la descripción del PR con la plantilla del repositorio: contexto, solución, alternativas, impacto, cómo probarlo y riesgos.",
#      "Adjunta la evidencia de la actividad: pruebas unitarias y su resultado.",
#      "Reúne el estado de cada paso del pipeline de GitHub, incluido Sonar, y avisa si alguno está en rojo.",
#      "Deja el PR listo; no lo publica por su cuenta."],
#     "Un PR con descripción completa, evidencia y el estado del pipeline a la vista.",
#     "El desarrollador revisa el PR y aprueba su publicación.",
#     "Lo que gana Viva Aerobus: el equipo de revisión recibe un PR con contexto, evidencia y pipeline a la vista.",
#     notas="Los pasos del pipeline son los que ya corren en GitHub (Sonar incluido). El PR no se publica sin aprobación del desarrollador.",
# )


# =============================================================== 4 a 9 Dolores en las devoluciones del PR y agente que los ataca
SRC_DOLORES = 'Fuente: informe «Seguimiento de equipo Viva Aerobus Generic Api» (septiembre de 2026) y análisis de septiembre, sección 2.1: PRs de septiembre con comentarios del equipo de revisión (26) frente a agosto (17), GitHub (F5). Un PR puede tener varios motivos; la clasificación de los motivos es lectura de Tech and Solve de los comentarios. No prometemos una cifra de mejora.'


def lamina_dolores(titulo, dolores, como, depende="", notas=""):
    izq = "".join(
        f'<div class="dolor"><div class="dl"><h3>{m}</h3><p>{d}</p></div><div class="dr"><div class="num">{n}</div>'
        + (f'<div class="tr {"up" if "Subió" in t else "dn" if "Bajó" in t else ""}">{t}</div>' if t else "")
        + "</div></div>" for m, n, t, d in dolores)
    lis = "".join(f"<li>{c}</li>" for c in como)
    der = (f'<div class="card tint" style="flex:1"><div class="k" style="margin-top:0">Cómo lo ataca</div><ul style="font-size:1.45cqw;margin-top:1cqw">{lis}</ul></div>'
           + (f'<div class="card" style="border-color:var(--amber)"><div class="k" style="margin-top:0">Depende de Viva Aerobus</div><p style="font-size:1.35cqw;margin:0">{depende}</p></div>' if depende else ""))
    lamina(titulo,
           f'<div style="display:grid;grid-template-columns:57fr 40fr;gap:1.6cqw;flex:1;min-height:0;margin-bottom:1.4cqw"><div class="{"c4" if len(dolores) >= 4 else ""}" style="display:flex;flex-direction:column;gap:1cqw">{izq}</div>'
           f'<div style="display:flex;flex-direction:column;gap:1cqw">{der}</div></div>',
           src=SRC_DOLORES, notas=notas)


# ---- resumen: motivos de devolución y agente que ataca cada uno
# Los 9 motivos de la tabla «Por qué se devuelven los PRs» del análisis de septiembre (sección 2.1), con los agentes que los atacan (propuesta nuestra)
FILAS_MOT = [
    ("Diseño, ubicación de la lógica, reutilización, código de más", ["Implementador de código", "Validador de calidad"]),
    ("Nombres, estilo y convenciones", ["Validador de calidad"]),
    ("Error funcional o escenario no cubierto", ["Analista", "Implementador de código", "Validador de calidad"]),
    ("Descripción del PR y release notes", ["Publicador"]),
    ("Preguntas de negocio y alcance para Viva", ["Analista"]),
    ("Evidencias y casos de prueba", ["Pruebas funcionales"]),
    ("Estructura de pruebas unitarias (BDD) o pruebas rotas", ["Implementador de código"]),
    ("Higiene de Git (rebase, rama, commits, conflictos)", ["Publicador"]),
    ("Cambios no revisados antes del push", ["Validador de calidad"]),
]
chip_ag = lambda n: f'<span class="chipag">{n}</span>'
tabla = ('<table class="t dense plain" style="font-size:1.25cqw"><tr><th style="width:52%">Motivo de devolución del PR</th><th>Agentes que lo atacan</th></tr>'
         + "".join(f'<tr><td>{m}</td><td>{"".join(chip_ag(a) for a in ags)}</td></tr>' for m, ags in FILAS_MOT)
         + "</table>")
lamina(
    "Qué motivos de devolución del PR ataca cada agente",
    tabla + '<p style="margin:1.1cqw 0 0;font-size:1.2cqw">El <span class="chipag">Orquestador</span> orquesta todo el flujo: invoca a estos agentes en el orden en que cada motivo los necesita.</p>',
    src="Fuente: informe «Seguimiento de equipo Viva Aerobus Generic Api» y análisis de septiembre de 2026, sección 2.1 (GitHub, F5). Un PR puede tener varios motivos; la clasificación es lectura de Tech and Solve y los agentes asignados, una propuesta.",
    notas="Es la tabla consolidada de los nueve motivos de devolución del análisis de septiembre, con los agentes que los atacan como chips. Un motivo puede atacarlo más de un agente. La asignación es nuestra propuesta; el informe dice qué se trabaja ya y qué se sugiere.",
)

lamina_dolores(
    "Orquestador: orquesta todo el flujo, de la característica al PR",
    [("Feedback que se repite entre rondas", "1 señal", "", "#2493 retoma lo que ya se había dicho en #2467: la misma observación vuelve en otra ronda.")],
    ["Orquesta todo el flujo: toma la característica, invoca a cada agente en el orden en que se necesita y la lleva a la revisión del PR.",
     "No pasa a la siguiente fase hasta que el desarrollador certifica la anterior.",
     "Ante un hallazgo, devuelve el trabajo al agente que corresponde, en vez de seguir.",
     "Conserva lo ya comentado en la revisión, para aplicarlo antes del siguiente envío."],
    notas="El Orquestador ataca el feedback repetido entre rondas: conservar lo comentado es propuesta; en LLMCoder, /continue lee primero los hilos del PR. El motivo «cambios no revisados antes del push» se quitó de la lámina por tono (decisión de Didier).",
)
lamina_dolores(
    "Analista: las preguntas de alcance llegan antes de escribir código",
    [("Preguntas de negocio y alcance para Viva", "6 de 26 PRs · 23 %", "Subió (0 en agosto)", "Preguntas que aparecen en el PR y que podían resolverse con Viva antes de codificar."),
     ("Error funcional o escenario no cubierto", "7 de 26 PRs · 27 %", "Igual", "El Analista sabe lo que la task pide; lo ataca junto con el Implementador y el Validador."),
     ("Alcance que se reabre en la revisión", "2 PRs", "", "#2484 y #2494: la revisión reabre alcance que ya había definido el negocio; además, 3 PRs piden casos fuera de la matriz.")],
    ["Sabe lo que la task pide: lee la actividad y sus criterios de aceptación, y los deja claros para los demás agentes.",
     "Los contrasta con el código real.",
     "Devuelve a Viva las preguntas priorizadas antes de empezar.",
     "Si hay bloqueos, no se escribe código."],
    depende="Que Viva Aerobus responda las preguntas, y que las actividades lleguen con criterios de aceptación.",
    notas="El informe dice que este motivo depende de cómo llegan definidas las tasks: el Analista no lo elimina, adelanta las preguntas.",
)
lamina_dolores(
    "Implementador de código: diseño, escenarios y pruebas unitarias",
    [("Diseño, ubicación de la lógica y reutilización", "16 de 26 PRs · 62 %", "Igual (59 % en agosto)", "El motivo más frecuente: dónde va la lógica y qué ya existe para reutilizar."),
     ("Error funcional o escenario no cubierto", "7 de 26 PRs · 27 %", "Igual", "El Implementador le da implementación real a lo que fijó el Analista, escenario por escenario."),
     ("Pruebas unitarias (BDD)", "3 de 26 PRs · 12 %", "Subió (0 en agosto)", "Cada revisor exige algo distinto de las pruebas unitarias.")],
    ["Toma los criterios de aceptación como contrato de lo que hay que construir.",
     "Aplica las guías de reutilización y de dónde va la lógica, tomadas de las revisiones de PR.",
     "Escribe pruebas unitarias por criterio y por caso límite, en el mismo cambio."],
    notas="Las guías de reutilización y ubicación de la lógica ya se trabajan desde el 6 de octubre según el informe, sin efecto medible aún. El informe de septiembre decía que Viva no permitía pruebas automatizadas; Didier confirmó el 19 de octubre que ya las permite.",
)
lamina_dolores(
    "Pruebas funcionales: la evidencia del consumo de servicios reales en Jira",
    [("Evidencias y casos de prueba", "4 de 26 PRs · 15 %", "Igual (12 % en agosto)", "Son las evidencias manuales de consumo de servicios reales que Viva Aerobus exige en cada actividad de Jira."),
     ("Formato de evidencia cuestionado después", "6 tickets", "", "Un formato de evidencia que pasó la validación se cuestionó más tarde, sin aviso de cambio.")],
    ["Toma la matriz de casos de prueba de la task, que define Viva Aerobus.",
     "Ejecuta los casos consumiendo los servicios reales y deja la evidencia de cada caso lista para Jira.",
     "Mantiene un solo formato de evidencia, el que se acuerde con Viva y el equipo de revisión."],
    depende="Un ambiente con el que el agente pueda comunicarse para las pruebas funcionales, y acordar por escrito el formato de evidencia con Viva Aerobus y el equipo de revisión.",
    notas="Didier (19 oct 2026): la evidencia manual de consumo de servicios reales en Jira se marca como otro agente, de pruebas funcionales; el Implementador automatiza solo las unitarias. La definición es nuestra, por confirmar. En LLMCoder el proceso arma ese paquete de evidencia (fase 7).",
)
lamina_dolores(
    "Validador de calidad: cobertura, estilo y Sonar antes del PR",
    [("Error funcional o escenario no cubierto", "7 de 26 PRs · 27 %", "Igual", "El Validador garantiza que todo lo que la task pide quedó cubierto, criterio por criterio."),
     ("Nombres, estilo y convenciones", "12 de 26 PRs · 46 %", "Subió (29 % en agosto)", "El segundo motivo más frecuente; el estilo se revisa a mano en cada PR."),
     ("Lo que una regla automática podía detectar", "5 tipos · 5 PRs", "", "Excepciones genéricas, parámetros sin uso, métodos idénticos, Array.Empty y nombres."),
     ("Sonar en rojo al mergear", "9 de 20 PRs", "", "Sonar corre en el pipeline de cada PR; su resultado queda para leerse antes de pedir la revisión.")],
    ["Garantiza que todo se cubre: compara cada criterio de la task con el código y las pruebas que lo cubren, y señala lo que falte.",
     "Aplica el perfil de estilo y las convenciones del equipo de revisión antes de abrir el PR.",
     "Lee el resultado de Sonar sobre el código nuevo y devuelve lo que esté en rojo.",
     "Corrige antes de la revisión lo que una regla puede detectar."],
    depende="Acceso de lectura a Sonar para el equipo (hoy no lo tiene) y acordar si su resultado pasa a ser criterio de la revisión.",
    notas="El estilo con el perfil del equipo ya se verifica en nuestro proceso; leer Sonar es propuesta y requiere acceso. La clasificación de motivos es lectura nuestra de los comentarios.",
)
lamina_dolores(
    "Publicador: descripción, evidencias y rama del PR en orden",
    [("Descripción del PR y release notes", "7 de 26 PRs · 27 %", "Igual", "Pedidos sobre la plantilla del PR; ningún control automático la valida."),
     ("Higiene de Git", "2 de 26 PRs · 8 %", "Bajó (24 % en agosto)", "Rama, commits y rama al día con master antes del merge.")],
    ["Arma la descripción con la plantilla del repositorio y la deja fiel a los cambios.",
     "Adjunta la evidencia que entregan los agentes de pruebas: unitarias y funcionales.",
     "Verifica la rama, los commits, que esté al día con master y el estado del pipeline; no publica sin el desarrollador."],
    notas="La evidencia de consumo de servicios reales en Jira la produce el agente de Pruebas funcionales; el Publicador la adjunta al PR. La verificación de la rama es propuesta.",
)

# Lámina retirada a pedido de Didier (19 oct 2026): «Cada agente responde a un problema concreto del flujo actual». Se conserva comentada.
# # =============================================================== 10 Problemas
# def problema(num, titulo, hoy, agentes, cambia, mide):
#     return (f'<div class="card" style="padding:1.3cqw 1.5cqw"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.6cqw"><div class="dot sm">{num}</div><h3 style="margin:0">{titulo}</h3></div>'
#             f'<div class="k" style="margin-top:.4cqw">Hoy</div><p style="font-size:1.2cqw;margin:0">{hoy}</p>'
#             f'<div class="k">Agentes</div><p style="font-size:1.2cqw;margin:0">{agentes}</p>'
#             f'<div class="k">Qué cambia</div><p style="font-size:1.2cqw;margin:0">{cambia}</p>'
#             f'<div class="k">Cómo lo veremos</div><p style="font-size:1.2cqw;margin:0">{mide}</p></div>')
#
#
# lamina(
#     "Cada agente responde a un problema concreto del flujo actual",
#     '<div class="grid g3" style="gap:1.3cqw">'
#     + problema("1", "Devoluciones en la revisión del PR",
#                "Cada ronda de comentarios del equipo de revisión cuenta como una devolución.",
#                "Analista, Implementador de código y Validador de calidad.",
#                "Las dudas de alcance se resuelven antes de codificar, el estilo y las convenciones se verifican antes del PR.",
#                "Devoluciones por actividad, con la fuente que ya existe en los PR.")
#     + problema("2", "Pruebas y evidencias",
#                "Viva Aerobus exige pruebas manuales y su evidencia cargada en cada actividad de Jira.",
#                "Implementador de código y Publicador.",
#                "Cada actividad llega con pruebas unitarias automatizadas y el PR trae la evidencia reunida.",
#                "Actividades con pruebas unitarias automatizadas que pasan, sobre el total.")
#     + problema("3", "Calidad y trazabilidad",
#                "El pipeline de GitHub ya incluye Sonar para medir la calidad de cada PR.",
#                "Validador de calidad, Publicador y Orquestador.",
#                "El PR llega con estilo, convenciones y Sonar verificados y el pipeline a la vista, y el estado de la característica y de cada agente queda visible.",
#                "PR con Sonar en verde y sin diferencias de estilo en las líneas del cambio.")
#     + "</div>"
#     + '<p class="muted" style="margin-top:auto;font-size:1.05cqw">No prometemos una cifra de mejora: proponemos medirla con el informe de seguimiento desde el primer mes (lámina 11).</p>',
#     notas="Los tres problemas se tomaron del modelo de trabajo actual de Viva. «Hoy» describe ese modelo, no una comparación con cifras.",
# )
#
# # Lámina retirada a pedido de Didier (19 oct 2026): «Construidos sobre las capacidades documentadas de Claude». Se conserva comentada.
# # # =============================================================== 11 Cómo se construye
# # lamina(
# #     "Construidos sobre las capacidades documentadas de Claude",
# #     '<p class="lead" style="margin-bottom:1.4cqw">Esta es la documentación oficial de Anthropic sobre los bloques con que se construye un agente en Claude Code. Lo que construimos encima, con las guías y los controles de Generic API, es de Tech and Solve.</p>'
# #     '<div class="grid g2" style="gap:1.4cqw">'
# #     f'<div class="card"><h3>Subagentes</h3><p style="margin:0">Cada agente corre con su propio contexto, sus instrucciones, las herramientas que se le permiten y sus propios permisos, y devuelve solo un resumen. Se definen en archivos de texto. {a(U_SUB, "Documentación oficial")}.</p></div>'
# #     f'<div class="card"><h3>Skills</h3><p style="margin:0">Paquetes de instrucciones reutilizables, definidos en un archivo, que se cargan solo cuando hacen falta; por ejemplo, el procedimiento de revisión de un PR. {a(U_SKILLS, "Documentación oficial")}.</p></div>'
# #     f'<div class="card"><h3>Hooks</h3><p style="margin:0">Comandos que se ejecutan siempre en puntos definidos del ciclo, para que ciertas acciones ocurran sin depender de que el modelo decida hacerlas. {a(U_HOOKS, "Documentación oficial")}.</p></div>'
# #     f'<div class="card"><h3>MCP (Model Context Protocol)</h3><p style="margin:0">Estándar abierto para conectar al agente con herramientas como el gestor de tareas o el repositorio. La documentación recomienda conectar solo servidores de confianza. {a(U_MCP, "Documentación oficial")}.</p></div>'
# #     "</div>",
# #     src="Fuente: documentación oficial de Claude Code, Anthropic (code.claude.com). Es documentación del fabricante sobre su propio producto: describe prácticas y capacidades, no una norma. Sin versiones: las capacidades se verifican en la documentación vigente.",
# #     notas="Cada bloque tiene su enlace oficial en la misma lámina. La documentación del fabricante es práctica documentada, no estándar. No se citan modelos ni versiones.",
# # )
#
# # Lámina retirada a pedido de Didier (19 oct 2026): «El agente se detiene, pide aprobación y cita su evidencia». Se conserva comentada.
# # # =============================================================== 12 Control humano
# # lamina(
# #     "El agente se detiene, pide aprobación y cita su evidencia",
# #     '<div class="grid g3" style="gap:1.4cqw;margin-bottom:1.4cqw">'
# #     '<div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">1</div><h3 style="margin:0">Se detiene ante un bloqueo</h3></div><p style="margin:0">El análisis termina en una compuerta. Si hay dudas sin resolver, el agente devuelve preguntas y no escribe código.</p></div>'
# #     '<div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">2</div><h3 style="margin:0">Lee primero, actúa con permiso</h3></div><p style="margin:0">El agente lee Jira y GitHub. Publicar un PR requiere la aprobación del desarrollador, y antes se muestra lo que se va a publicar.</p></div>'
# #     '<div class="card tint"><div style="display:flex;gap:.9cqw;align-items:center;margin-bottom:.7cqw"><div class="dot sm">3</div><h3 style="margin:0">Cada afirmación lleva su evidencia</h3></div><p style="margin:0">Cita el ticket, el comentario o la ruta del código que la respalda. Lo que no se puede verificar se dice: «no consta».</p></div>'
# #     "</div>"
# #     f'<p class="muted" style="margin-bottom:.6cqw">Estas prácticas son de Tech and Solve. Se apoyan en controles que la documentación oficial de Claude Code describe: reglas de permisos que definen qué puede hacer el agente ({a(U_PERM, "documentación de permisos")}) y hooks que ejecutan comandos en puntos del ciclo con control determinista ({a(U_HOOKS, "documentación de hooks")}).</p>'
# #     + gana("Los agentes aceleran el trabajo previo; la responsabilidad de cada entrega sigue siendo del desarrollador."),
# #     src="Fuente: documentación oficial de Claude Code, Anthropic (code.claude.com): permisos y hooks. Práctica documentada del fabricante, no una norma.",
# #     notas="Aquí se responde a la pregunta de un líder de tecnología: ¿qué pasa si el agente se equivoca? Se detiene ante bloqueos, no publica sin aprobación y deja evidencia. La práctica es nuestra; los controles de permisos y hooks son los que documenta Anthropic.",
# # )

# Láminas retiradas a pedido de Didier (19 oct 2026): medición y las dos internas (estado de cada agente y lo que no se dice al cliente). Se conservan comentadas.
# # =============================================================== 13 Medición
# lamina(
#     "Medimos el efecto con el informe de seguimiento de Viva",
#     '<p class="lead" style="margin-bottom:1.3cqw">Antes de activar cada agente se toma una línea base con los meses ya registrados; después se compara con las mismas definiciones.</p>'
#     '<table class="t"><tr><th style="width:26%">Indicador</th><th style="width:44%">Cómo se mide</th><th>Fuente</th></tr>'
#     "<tr><td>Devoluciones por actividad</td><td>Rondas de comentarios del equipo de revisión en el PR de cada actividad.</td><td>GitHub y informe de seguimiento</td></tr>"
#     "<tr><td>Pruebas unitarias automatizadas</td><td>Actividades con pruebas unitarias automatizadas que pasan, sobre el total de actividades.</td><td>GitHub y pipeline</td></tr>"
#     "<tr><td>Sonar en verde</td><td>PR cuyo resultado de calidad en Sonar queda aprobado al entrar a revisión.</td><td>GitHub</td></tr>"
#     "<tr><td>Estilo del equipo</td><td>Actividades sin diferencias de estilo en las líneas que el cambio tocó, sobre el total.</td><td>Pipeline y repositorio</td></tr>"
# "</table>"
#     '<p class="muted" style="margin:1.2cqw 0 0">Propuesta de medición, a acordar con Viva Aerobus. Si alguna fuente no permite calcular un indicador, se dice y no se estima.</p>',
#     notas="No hay hoy una medición del efecto de los agentes; se propone construirla. Los indicadores salen del modelo de trabajo del cliente (devoluciones, Sonar en el pipeline, criterios de aceptación en Jira).",
# )
#
# # Lámina retirada a pedido de Didier (19 oct 2026): «Cómo entra a Generic API y qué decidimos juntos». Se conserva comentada.
# # # =============================================================== 14 Entrada y decisiones
# # lamina(
# #     "Cómo entra a Generic API y qué decidimos juntos",
# #     '<div class="grid g2" style="gap:1.8cqw;flex:1">'
# #     '<div><h3>Un orden sugerido, no un calendario</h3><div class="grid" style="gap:.9cqw">'
# #     '<div class="card" style="display:flex;gap:1cqw;align-items:flex-start"><div class="dot sm">1</div><div><b style="color:var(--violet)">Primero, lo que no cambia el flujo</b><br><span class="muted">Orquestador, Analista, Implementador de código (con sus pruebas unitarias) y Validador de calidad trabajan antes del PR, dentro del flujo que Viva Aerobus ya tiene.</span></div></div>'
# #     '<div class="card" style="display:flex;gap:1cqw;align-items:flex-start"><div class="dot sm">2</div><div><b style="color:var(--violet)">Después, lo que depende de acuerdos</b><br><span class="muted">Publicador, con la plantilla de PR y los pasos del pipeline que Viva Aerobus defina.</span></div></div>'
# #     '<div class="card" style="display:flex;gap:1cqw;align-items:flex-start"><div class="dot sm">3</div><div><b style="color:var(--violet)">Al final, el ajuste con lo medido</b><br><span class="muted">Se revisan los indicadores y se decide qué agente seguir, cambiar o dejar.</span></div></div>'
# #     "</div></div>"
# #     '<div><h3>Lo que necesitamos de Viva Aerobus</h3><div class="grid" style="gap:.9cqw">'
# #     '<div class="card tint"><b style="color:var(--violet)">Acceso de lectura</b><br><span>A Jira y GitHub de Generic API, para que los agentes lean el contexto de cada actividad.</span></div>'
# #     '<div class="card tint"><b style="color:var(--violet)">La guía de revisión del equipo</b><br><span>La que aplica el equipo de revisión, para tomarla como base del Implementador y del Validador.</span></div>'
# #     '<div class="card tint"><b style="color:var(--violet)">Decisiones por tomar</b><br><span>Si el resultado de Sonar pasa a ser criterio de la revisión y qué indicadores se miden.</span></div>'
# #     "</div></div></div>",
# #     notas="No se dan plazos: el orden es una sugerencia. Las dependencias de Viva son accesos, la guía de revisión y dos decisiones. El plazo de cada una lo declara su dueño.",
# # )
#
# # =============================================================== 15 Interna: estado y evidencia
# fila = lambda ag, est, cls, ev: f'<tr><td>{ag}</td><td class="est {cls}">{est}</td><td>{ev}</td></tr>'
# lamina(
#     "Estado de cada agente y la evidencia que lo respalda",
#     '<table class="t dense" style="font-size:.98cqw"><tr><th style="width:22%">Agente de la propuesta</th><th style="width:15%">Estado</th><th>Evidencia en LLMCoder (solo lectura)</th></tr>'
#     + fila("Orquestador", "Opera", "ok", "CLAUDE.md («este archivo orquesta»: el pipeline de fases con compuertas); .claude/commands/implement.md y continue.md (recorren las fases); .claude/hooks/pipeline-state.sh (estado de las compuertas); work/&lt;KEY&gt;/delivery-state.md (tablero de estado por actividad). Definición como agente aparte: nuestra, por confirmar")
#     + fila("Analista", "Opera", "ok", "process/phase-00 a 04; process/ANALYZE-TASK.md (criterios de aceptación en términos comprobables); .claude/agents/requirement-analyst.md; mapa del sistema: .claude/agents/doc-sync.md y documents/")
#     + fila("Implementador de código", "Opera", "ok", "process/phase-05-planning.md y phase-06-implementation.md; CLAUDE.md (compuerta y reglas); guidelines/ (guías de código desde revisiones de PR). Pruebas unitarias: process/phase-07-testing.md §7.0 a 7.2 (xUnit primero; una fila [Automated] exige prueba xUnit en el PR), dentro del mismo proceso. Plan ligado a criterio: no consta")
#     + fila("Pruebas funcionales", "Opera, definición nuestra", "pa", "process/phase-07-testing.md §7.0 (humo, runner PS1, Postman + newman) y §7.4 (paquete de evidencia en tres formatos); tools/evidence/EVIDENCE-FORMAT.md; .claude/agents/tc-evidence-auditor.md. Como agente aparte: nuestra definición, por confirmar")
#     + fila("Validador de calidad", "Parcial", "pa", "Cobertura: process/REVIEW-CODE.md («mapear cada criterio de aceptación al código», tabla criterio · implementado por · estado). Estilo: process/phase-09-pre-review.md §9.5 (perfil Ezy con tools/code-style.sh, cero diferencias en líneas del cambio) y guidelines/csharp-style.md (STY); REVIEW-CODE.md fases de diseño y estilo. Sonar: solo guía PRC-38 (gate de CI), el proceso no lo lee")
#     + fila("Publicador", "Parcial", "pa", "process/phase-10-pr-review.md §10.1: plantilla de PR, evidencia, «CI en verde antes de pedir revisión», aprobación de publicación. Pasos del pipeline dentro de la descripción: no consta")
#     + "</table>",
#     src="Ruta base: /Users/didierfranco/Documents/GitHubViva/VivaAerobus.Generic.ApiLLMCoder. Actividades con carpeta de trabajo: API-1711, API-1738, API-1834, API-1858. «Opera» significa que existe en el proceso; no consta que cada paso haya corrido en cada PR.",
#     notas="Lámina interna. Separa lo que ya existe en nuestro proceso de lo que se propone. No se muestra al cliente ni se nombra el repositorio ante él.",
#     interna=True,
# )
#
# # =============================================================== 16 Interna: límites
# lamina(
#     "Lo que no se dice al cliente y lo que falta verificar",
#     '<div class="grid g3" style="gap:1.3cqw">'
#     '<div class="card tint ag"><h3>No se dice al cliente</h3><ul style="font-size:1.15cqw"><li>El repositorio LLMCoder ni su nombre.</li><li>Cuántas reglas, fases o agentes tiene nuestro proceso interno.</li><li>Nombres de personas ni cuántas trabajan en el equipo.</li><li>Que algo «ya opera»: se presenta como propuesta.</li><li>Modelos ni versiones de Claude.</li></ul></div>'
#     '<div class="card ag"><h3>No consta o falta verificar</h3><ul style="font-size:1.15cqw"><li>Ninguna medición del efecto en devoluciones, tiempos o defectos: no se afirma reducción.</li><li>Que cada paso haya corrido en cada PR de Viva: solo hay cuatro carpetas de trabajo.</li><li>Pruebas automatizadas: el contexto de Generic API decía que el cliente no las permite; Didier confirmó el 19 oct que ya permite pruebas unitarias automatizadas; el informe de septiembre aún decía que no. Sin evidencia escrita en el repositorio.</li><li>Pasos del pipeline en el PR y plan ligado a cada criterio: propuesta, no consta.</li><li>Sonar en el Validador: el proceso interno no lo lee; es propuesta, y hoy el equipo de revisión no lo usa como criterio.</li></ul></div>'
#     '<div class="card ag"><h3>Decisiones y fuentes</h3><ul style="font-size:1.15cqw"><li>Confirmado por Didier (19 oct): se nombra «Claude Code» y se dice que las guías se toman de las revisiones de PR de Generic API.</li><li>No se cita «Building Effective AI Agents»: trae una nota de que el panorama cambió.</li><li>No se cita Managed Agents: está en beta.</li><li>Orquestador: lo pidió Didier sin definirlo; la definición es nuestra, por confirmar.</li></ul></div>'
#     "</div>",
#     notas="Lámina interna. Resume los límites de lo que se dice y los pendientes antes de presentar.",
#     interna=True,
# )


# =============================================================== Precondiciones para el éxito (se coloca después de la tabla de motivos)
def pre(n, t):
    return f'<div class="pre"><div class="dot sm" style="flex:none">{n}</div><p>{t}</p></div>'


def col_pre(titulo, items, tint=False):
    return (f'<div class="card{" tint" if tint else ""}" style="padding:1.5cqw 1.6cqw"><h3 style="margin-bottom:1.1cqw">{titulo}</h3>'
            + "".join(pre(n, t) for n, t in items) + "</div>")


lamina(
    "Precondiciones para el éxito",
    '<div class="grid g3" style="gap:1.4cqw;flex:1;min-height:0;margin-bottom:1.2cqw;align-items:stretch">'
    + col_pre("Herramientas y accesos", [
        (1, "<b>Licencia de Claude</b> obligatoria para cada persona que use los agentes."),
        (2, "<b>Acceso de lectura</b> a Jira y GitHub de Generic API, para que los agentes lean el contexto de cada característica."),
        (3, "<b>Un ambiente con el que los agentes puedan comunicarse</b> para hacer las pruebas funcionales.<br><span style=\"font-size:1.1cqw\">Solo afecta al agente </span><span class=\"chipag\" style=\"font-size:1.05cqw\">Pruebas funcionales</span>"),
    ])
    + col_pre("Sonar como fuente de verdad", [
        (4, "<b>Sonar habilitado para todo el equipo.</b>"),
        (5, "<b>Estilo, nombres y convenciones definidos en Sonar</b>, para que se validen de forma automática."),
        (6, "<b>Sonar manda en estilo:</b> si el revisor quiere cambiar un lineamiento, lo define en Sonar y la validación queda automática."),
        (7, "<b>El revisor del PR valida solo que la métrica de Sonar pase en verde</b> en el pipeline."),
    ], tint=True)
    + col_pre("Alcance y criterios", [
        (8, "<b>Las pruebas automatizadas no las acota ni las bloquea una revisión manual:</b> se automatizan con los criterios de aceptación de la característica en Jira."),
        (9, "<b>Cada característica llega con criterios de aceptación claros</b> y comprobables."),
        (10, "<b>Un formato de evidencia y una plantilla de PR acordados por escrito</b> con Viva Aerobus y el equipo de revisión."),
    ])
    + "</div>",
    src="Son sugerencias para conversar. Varias recogen las recomendaciones del informe «Seguimiento de equipo Viva Aerobus Generic Api» (septiembre de 2026): Quality Gate de Sonar obligatorio para mergear con acceso de lectura para el equipo, estilo y plantilla del PR validados por checks automáticos, un formato de evidencia escrito con Viva y el equipo de revisión, y pruebas automatizadas con la matriz como único criterio.",
    notas="Las precondiciones 1, 4, 5, 6, 7 y 8 las dictó Didier (19 oct 2026); la redacción es nuestra. Las precondiciones 2, 3, 9 y 10 las agregamos nosotros: 2 sale de lo que los agentes necesitan leer; 3 la ajustó Didier (un ambiente con el que los agentes se comuniquen para pruebas funcionales; solo afecta a ese agente); 9 del motivo «preguntas de negocio y alcance»; 10 de las recomendaciones del informe sobre evidencia y plantilla del PR. Quién provee la licencia de Claude no está definido.",
)

# Orden pedido por Didier (19 oct 2026): la tabla de motivos de devolución (lámina 3) va antes de «Cómo se usa un agente» (lámina 4)
SECCIONES[2], SECCIONES[3] = SECCIONES[3], SECCIONES[2]
# Precondiciones: lámina 4, justo después de la tabla de motivos
SECCIONES.insert(3, SECCIONES.pop())

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
