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
# Diseño de la presentación de referencia «Tech and Solve - Dinámica de trabajo del equipo» (SURA):
# láminas 16:9 apiladas, todo medido en cqw (1cqw = 12,8 px a 1280 px de ancho), fondo blanco,
# títulos violeta, tarjetas violeta claro, pie con logo y número. Las piezas propias de esta
# propuesta (.row, .num, .tag, .pend, .t16…) se escribieron en px a 1280 px y se pasan a cqw.
CSS = """
:root {
  --violet: #280265; --violet-light: #EBEBFF; --accent: #5300DF; --amber: #B9720A;
  --green: #1B6B4F; --card: #FAF9FE; --text: #1A1E27; --text-2: #5B5A66; --border: #DCD8EC;
  --logo: url("{{LOGO_DARK_VIOLET}}");
  /* nombres usados por el contenido de esta propuesta */
  --dark-violet: #FFFFFF; --white: var(--text); --lighter-violet: var(--text-2); --darker-gray: var(--violet-light);
  --blue-accent: var(--accent); --black: #FFFFFF;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: #E6E4EE; font-family: "Poppins", Arial, sans-serif; color: var(--text); }
body { counter-reset: slide; padding: 24px 0 60px; }
.slide {
  container-type: inline-size; position: relative; width: min(1280px, 96vw); aspect-ratio: 16 / 9;
  margin: 0 auto 24px; background: #fff; overflow: hidden; counter-increment: slide;
  box-shadow: 0 4px 24px rgba(40, 2, 101, .12); scroll-snap-align: center;
}
.in { position: absolute; inset: 0; padding: 3.4cqw 4.5cqw 5.2cqw; display: flex; flex-direction: column; font-size: 1.32cqw; line-height: 1.38; }
h2 { font-size: 2.6cqw; line-height: 1.2; color: var(--violet); margin: 0 0 1.8cqw; font-weight: 700; max-width: 95%; }
h3 { font-size: 1.45cqw; color: var(--violet); margin: 0 0 .8cqw; font-weight: 700; line-height: 1.25; }
p { margin: 0 0 .7cqw; }
ul { margin: 0; padding-left: 1.4cqw; } li { margin-bottom: .6cqw; }
b, strong { font-weight: 600; }
.foot { position: absolute; left: 4.5cqw; right: 4.5cqw; bottom: 1.6cqw; display: flex; align-items: center; gap: 1.2cqw; font-size: .95cqw; color: var(--text-2); }
.foot::before { content: ""; width: 5cqw; height: 2.6cqw; background: var(--logo) left center / contain no-repeat; }
.foot::after { content: counter(slide); margin-left: auto; }
.src { margin-top: auto; font-size: .92cqw; color: var(--text-2); }
.src a, a { color: var(--accent); }
.content { position: relative; flex: 1; }

/* piezas propias (px a 1280 px → cqw) */
.lead { font-size: 1.72cqw; line-height: 1.4; color: var(--text-2); }
.sub { color: var(--text-2); }
.card { background: var(--violet-light); border-radius: 1.1cqw; padding: 1.56cqw 1.72cqw; }
.row { display: flex; gap: 1.25cqw; }
.col { display: flex; flex-direction: column; gap: 1.1cqw; }
.t20 { font-size: 1.56cqw; font-weight: 600; line-height: 1.25; }
.t16 { font-size: 1.25cqw; line-height: 1.4; }
.t18 { font-size: 1.4cqw; line-height: 1.4; }
.num { font-size: 5cqw; font-weight: 700; line-height: 1; }
.tag { display: inline-block; font-size: .94cqw; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; padding: .31cqw .78cqw; border-radius: 999px; }
.pend { border: 2px dashed var(--text); border-radius: 1.1cqw; padding: 1.25cqw 1.56cqw; }
table { border-collapse: separate; border-spacing: 0 .47cqw; width: 100%; }
th { font-size: 1.02cqw; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; text-align: left; padding: .31cqw 1.4cqw; color: var(--text-2); }
td { background: var(--violet-light); padding: .86cqw 1.4cqw; font-size: 1.33cqw; line-height: 1.3; }
td:first-child { border-radius: .94cqw 0 0 .94cqw; } td:last-child { border-radius: 0 .94cqw .94cqw 0; }
svg text { font-family: "Poppins", sans-serif; }
.pend li { margin-bottom: .2cqw; }

/* Impresión: una lámina por página */
@page { size: 13.333in 7.5in; margin: 0; }
@media print {
  body { background: #fff; padding: 0; }
  .slide { width: 13.333in; margin: 0; box-shadow: none; break-after: page; }
  .hint { display: none; }
}
.hint { position: fixed; right: 16px; bottom: 12px; font-size: 12px; color: var(--text-2); background: #fff; padding: 6px 10px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
"""

# ---------------------------------------------------------------- JS (el de la presentación de referencia)
JS = """
  const slides = [...document.querySelectorAll('.slide')];
  const current = () => slides.findIndex(s => s.getBoundingClientRect().bottom > innerHeight / 2);
  addEventListener('keydown', e => {
    const i = current();
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); slides[Math.min(i + 1, slides.length - 1)].scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); slides[Math.max(i - 1, 0)].scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  });
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


# Paquetes (decisión de Didier, 15 oct 2026): promedio de 51 puntos por persona → base 51 × 3, luego 51 × 4 y 51 × 5.
PP_PROM = 51
# Regla (19 oct 2026): para los puntos del paquete solo cuentan 3 de las 4 semanas del mes; la última se va en revisión
# y certificación en UAT, y lo que se empiece ahí no alcanza a certificarse en el mes. 51 × 3/4 = 38,25 → 38 (hacia abajo).
SEM_DEV, SEM_MES = 3, 4
# Decisión de Didier (19 oct 2026): el Inicial es lo que se completó en septiembre (117 puntos trabajados en el mes
# en las tareas terminadas) = 39 por persona; los demás suman una persona. Concuerda con 3 de 4 semanas (153 × 3/4 ≈ 115).
PP_PAQ = 39
PK_MIN = 3 * PP_PAQ

# =============================================================== 1 PROMESA
three = [("1", "Se compra un paquete de puntos al mes", "Tres paquetes: 117, 156 o 195 puntos al mes."),
         ("2", "Cada actividad cuesta los puntos de su tamaño", "1, 2, 3, 5 u 8 (Fibonacci), acordados antes de empezar. Máximo 8 puntos por actividad; lo mayor se divide."),
         ("3", "Se paga solo la tarea finalizada", "Entregada con PR aprobado y sin defectos pendientes. No se paga por horas, personas ni intentos de revisión.")]
def persona(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{22*s:.0f}" fill="#EBEBFF"/>'
            f'<path d="M{x-40*s:.0f},{y+88*s:.0f} a{40*s:.0f},{44*s:.0f} 0 0 1 {80*s:.0f},0 z" fill="#EBEBFF"/>')


cover_svg = (
    '<svg viewBox="0 0 1152 250" width="1152" height="250" role="img" aria-label="Del modelo staff, con personas, a una aplicación entregada llave en mano">'
    # izquierda: tres personas
    '<rect x="0" y="0" width="430" height="250" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.25"/>'
    + persona(125, 70) + persona(215, 56, 1.15) + persona(305, 70) +
    '<text x="215" y="205" text-anchor="middle" font-family="Poppins" font-size="22" font-weight="700" fill="#FFFFFF">Hoy: modelo staff</text>'
    '<text x="215" y="232" text-anchor="middle" font-family="Poppins" font-size="16" fill="#EBEBFF">se paga el tiempo de las personas</text>'
    # flecha
    '<path d="M470,125 H660" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>'
    '<path d="M650,105 L684,125 L650,145 Z" fill="#FFFFFF"/>'
    # derecha: aplicación terminada
    '<rect x="722" y="0" width="430" height="250" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.25"/>'
    '<rect x="827" y="26" width="220" height="140" rx="12" fill="none" stroke="#EBEBFF" stroke-width="4"/>'
    '<path d="M827,52 H1047" stroke="#EBEBFF" stroke-width="4"/>'
    '<circle cx="845" cy="39" r="5" fill="#EBEBFF"/><circle cx="862" cy="39" r="5" fill="#EBEBFF"/><circle cx="879" cy="39" r="5" fill="#EBEBFF"/>'
    '<circle cx="937" cy="110" r="36" fill="#FFFFFF"/>'
    '<path d="M919,110 l12,12 l24,-26" fill="none" stroke="#280265" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    '<text x="937" y="205" text-anchor="middle" font-family="Poppins" font-size="22" font-weight="700" fill="#FFFFFF">Propuesta: llave en mano</text>'
    '<text x="937" y="232" text-anchor="middle" font-family="Poppins" font-size="16" fill="#EBEBFF">se paga la actividad terminada</text>'
    '</svg>')

add("Propuesta comercial · Generic API",
    f"Propuesta de cambio de dinámica de trabajo: del modelo staff a {hl('llave en mano')} por actividades",
    cover_svg,
    "Documento confidencial. Elaborado por Tech and Solve para Viva Aerobus.", "cover", top=380)

# =============================================================== 2 QUIÉN SE ENCARGA DE QUÉ (modelo staff vs llave en mano)
V, T = "Viva Aerobus", "Tech and Solve"


def chip(q):
    if q == T:
        return ('<span style="display:inline-block;background-color:var(--blue-accent);color:var(--black);border-radius:999px;'
                'padding:4px 14px;font-size:14px;font-weight:700">Tech and Solve</span>')
    return ('<span style="display:inline-block;border:2px solid var(--white);color:var(--white);border-radius:999px;'
            'padding:2px 12px;font-size:14px;font-weight:600">Viva Aerobus</span>')


resp = [("Definir las actividades a desarrollar", V, V),
        ("Gestionar el proceso hasta lograr los resultados", V, T),
        ("Gestionar la capacidad del equipo", V, T),
        ("Elegir personas aptas, cambiarlas y cubrir la rotación", V, T),
        ("Transferir el conocimiento entre integrantes", V, T),
        ("Seguir el rendimiento de cada integrante y ajustar la dinámica", V, T),
        ("Calidad del trabajo entregado", T, T)]
td = 'style="padding:6px 18px;font-size:16px;background:transparent;border-bottom:1px solid #DCD8EC;border-radius:0"'
rows = "".join(f'<tr><td {td}>{r}</td><td {td}>{chip(h)}</td><td {td}>{chip(c)}</td></tr>' for r, h, c in resp)
rows += (f'<tr><td {td}><strong>Qué se paga</strong></td><td {td}>El tiempo de las personas</td>'
         f'<td {td}><strong style="color:var(--blue-accent)">Solo las actividades certificadas en UAT (Ready for prod)</strong></td></tr>')
add("El cambio · quién se encarga de qué",
    f"Viva deja de gestionar el equipo y {hl('solo pide desarrollos')}",
    '<table><colgroup><col style="width:46%"><col style="width:20%"><col style="width:34%"></colgroup>'
    '<thead><tr><th>Responsabilidad</th><th>Hoy · modelo staff</th><th>Con el cambio · llave en mano</th></tr></thead>'
    f'<tbody>{rows}</tbody></table>'
    '<div class="t16 sub" style="margin-top:10px">Hoy, todo lo que está a cargo de Viva Aerobus le demanda tiempo de gestión del equipo. '
    'Con el cambio, Tech and Solve entrega las actividades con las pruebas de UAT aceptadas y solo cobra las certificadas.</div>',
    "Propuesta de Tech and Solve.", top=176)

# =============================================================== 2 CÓMO FUNCIONA (contenido que estaba en la portada)
# Rediseño visual (19 oct 2026): tres pasos a la izquierda y los paquetes como escalera a la derecha.
fib = ''.join(f'<span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;'
              f'border:2px solid var(--blue-accent);color:var(--blue-accent);font-weight:700;font-size:15px;margin-right:6px">{n}</span>' for n in (1, 2, 3, 5, 8))
pasos3 = [("Se compra un paquete de puntos al mes", "Viva Aerobus elige cuántos puntos necesita; no contrata personas ni horas.", ""),
          ("Cada actividad cuesta los puntos de su tamaño", "Escala Fibonacci, acordada antes de empezar; máximo 8 puntos por actividad.", f'<div style="margin-top:8px">{fib}</div>'),
          ("Se paga la actividad finalizada", "Certificada en UAT (Ready for prod), sin defectos pendientes. No se paga por intentos de revisión.", "")]
col_pasos = ''.join(
    f'<div style="display:flex;gap:16px;align-items:flex-start;padding:14px 0;{"border-bottom:1px solid #DCD8EC" if i < 2 else ""}">'
    f'<span style="flex:0 0 44px;height:44px;border-radius:50%;background-color:var(--blue-accent);color:var(--black);font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center">{i + 1}</span>'
    f'<div><div style="font-size:20px;font-weight:700;line-height:1.2">{t}</div><div style="font-size:15px;line-height:1.4;margin-top:4px;color:var(--lighter-violet)">{d}</div>{x}</div></div>'
    for i, (t, d, x) in enumerate(pasos3))
escalones = [("Inicial", "paquete base", PK_MIN, 230, True), ("Ampliado", "para meses de más carga", 4 * PP_PAQ, 300, False),
             ("Avanzado", "para la mayor carga", 5 * PP_PAQ, 370, False)]
escalera = ''.join(
    f'<div style="flex:1;height:{h}px;border-radius:16px 16px 6px 6px;padding:16px 18px;display:flex;flex-direction:column;justify-content:flex-end;'
    f'{"background-color:var(--blue-accent);color:var(--black)" if dest else "background-color:var(--darker-gray)"}">'
    + (f'<span style="align-self:flex-start;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:999px;background:#fff;color:#5300DF;margin-bottom:auto">Para empezar</span>' if dest else '')
    + f'<div style="font-size:21px;font-weight:700">{nom}</div><div style="font-size:13px;{"" if dest else "color:var(--lighter-violet)"}">{uso}</div>'
    f'<div style="font-size:54px;font-weight:700;line-height:1;margin-top:6px;{"" if dest else "color:var(--blue-accent)"}">{pts}</div>'
    f'<div style="font-size:14px">puntos al mes</div></div>'
    for nom, uso, pts, h, dest in escalones)
add("Cómo funciona",
    f"Pago por actividades {hl('terminadas')}, no por FTE",
    '<div style="display:flex;gap:40px;align-items:stretch">'
    f'<div style="flex:0 0 500px;padding-top:24px">{col_pasos}</div>'
    '<div style="flex:1;display:flex;flex-direction:column">'
    '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--lighter-violet);margin-bottom:8px">Los tres paquetes que ofrecemos</div>'
    f'<div style="display:flex;gap:14px;align-items:flex-end">{escalera}</div>'
    '<div style="margin-top:14px;background-color:var(--darker-gray);border-radius:12px;padding:12px 16px;font-size:14.5px;line-height:1.4">'
    '<b>El paquete Inicial cubre el trabajo entregado en septiembre:</b> las actividades que quedaron en Ready for prod y Finalizado.</div>'
    '</div></div>',
    "Propuesta de Tech and Solve. Septiembre de 2026: F1 informe de seguimiento (actividades en Ready for prod y Finalizado).")

# =============================================================== MODELO DE TRABAJO (pedido de Didier, 15 oct 2026)
# Actores Viva Aerobus y Tech and Solve; seis pasos alternados por carril y la regla del feedback.
LBL, CW, GX, X0 = 120, 150, 24, 144          # ancho de etiqueta, de tarjeta, separación, x de la primera tarjeta
RH, RG = 134, 22                              # alto de carril y separación entre carriles
pasos = [("V", "Entrega la actividad", "Describe lo que necesita desarrollar."),
         ("T", "Valida y estima", "Revisa el alcance y si es implementable; entrega los puntos."),
         ("V", "Prioriza", "Ordena las actividades y elige cuáles entran en su paquete."),
         ("T", "Implementa y entrega", "Desarrolla, prueba y entrega en el ambiente de UAT."),
         ("V", "Certifica", "La prueba en UAT: la aprueba o pide una corrección o un cambio de alcance."),
         ("T", "Valida el feedback", "Revisa si es una corrección o un cambio de alcance.")]


def xcol(i):
    return X0 + i * (CW + GX)


def ycar(a):
    return 0 if a == "V" else RH + RG


carriles = ''.join(
    f'<div style="position:absolute;left:0;top:{ycar(a)}px;width:1164px;height:{RH}px;border-radius:14px;'
    f'{"background-color:var(--darker-gray)" if a == "V" else "border:2px solid var(--blue-accent)"}"></div>'
    f'<div style="position:absolute;left:16px;top:{ycar(a) + RH / 2 - 22}px;width:{LBL - 20}px;font-size:17px;font-weight:700;line-height:1.2">{n}</div>'
    for a, n in (("V", "Viva Aerobus"), ("T", "Tech and Solve")))
tarjetas = ''.join(
    f'<div style="position:absolute;left:{xcol(i)}px;top:{ycar(a) + 10}px;width:{CW}px;height:{RH - 20}px;border-radius:10px;padding:8px 10px;'
    f'{"background-color:#fff;border:1px solid #DCD8EC" if a == "V" else "background-color:var(--blue-accent);color:var(--black)"}">'
    f'<div style="display:flex;gap:6px;align-items:center"><span style="flex:0 0 22px;height:22px;border-radius:50%;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;'
    f'{"background-color:var(--blue-accent);color:var(--black)" if a == "V" else "background-color:#fff;color:#5300DF"}">{i + 1}</span>'
    f'<span style="font-size:15px;font-weight:700;line-height:1.15">{t}</span></div>'
    f'<div style="font-size:12.5px;line-height:1.3;margin-top:5px">{d}</div></div>'
    for i, (a, t, d) in enumerate(pasos))
flechas = []
for i in range(5):
    a, b = pasos[i][0], pasos[i + 1][0]
    x1, x2 = xcol(i) + CW, xcol(i + 1)
    y1, y2 = ycar(a) + RH / 2, ycar(b) + RH / 2
    xm = x1 + GX / 2
    flechas.append(f'<path d="M{x1},{y1} H{xm} V{y2} H{x2 - 7}" fill="none" stroke="#22D0FF" stroke-width="2.5"/>'
                   f'<path d="M{x2 - 8},{y2 - 6} L{x2},{y2} L{x2 - 8},{y2 + 6}z" fill="#22D0FF"/>')
H2 = 2 * RH + RG
svg_fl = f'<svg width="1164" height="{H2}" viewBox="0 0 1164 {H2}" style="position:absolute;left:0;top:0;pointer-events:none">{"".join(flechas)}</svg>'
rama = [("Si es un cambio de alcance", "No entra en la actividad: se registra como una actividad nueva, con su propia estimación en puntos, y Tech and Solve la cobra."),
        ("Si es una corrección (dentro del alcance)", "Tech and Solve la ajusta, sin cambiar sus puntos, hasta que pase las pruebas de UAT.")]
ramas = ''.join(
    f'<div class="card" style="flex:1;padding:10px 18px"><div style="font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--lighter-violet)">Después del paso 6</div>'
    f'<div style="font-size:18px;font-weight:700;margin-top:2px">{t}</div><div class="t16" style="margin-top:4px">{d}</div></div>'
    for t, d in rama)
add("Modelo de trabajo",
    f"Modelo de trabajo: Viva Aerobus prioriza y certifica; Tech and Solve {hl('estima, construye y ajusta')}",
    f'<div style="position:relative;height:{H2}px">{carriles}{svg_fl}{tarjetas}</div>'
    f'<div class="row" style="margin-top:10px">{ramas}</div>'
    '<div style="margin-top:10px;background-color:var(--blue-accent);color:var(--black);border-radius:12px;padding:12px 18px;font-size:15.5px;line-height:1.4">'
    '<b>Tech and Solve entrega cada actividad en UAT</b> y corrige ahí todo el feedback, hasta dejarla lista para que Viva Aerobus la certifique.</div>',
    "Propuesta de Tech and Solve. Se paga la actividad certificada en UAT (Ready for prod).")

# =============================================================== 2 EJEMPLO SEPTIEMBRE
# Tareas del equipo (Daniel, Gabriel y Luis) con estado Finalizada/Finalizado en el informe de septiembre de 2026 (F1).
# Puntos calculados con v4/calculos/build_v4.py (horas reales H+I + 30 %). Se excluye API-1860 (implementada por un revisor).
# Regla (15 oct 2026): ninguna actividad pasa de 30 h de trabajo (39 h con el 30 %); la que pasa se divide en partes iguales.
# (tarea, partes) por tamaño de cada parte. Recalculado con la lógica de v4 y la escala 1-2-3-5-8 (tope 39 h con margen).
# Solo horas de Daniel, Gabriel y Luis (15 oct 2026): API-1427 queda en 43 h (sin las 21 h de otra persona) y se divide en 2.
# Base (15 oct 2026): tareas del equipo en «Finalizado»/«Finalizada» o «Ready for prod» en el informe de septiembre (F1),
# con horas o fecha de entrega en septiembre. Horas reales (H + I) solo de Daniel, Gabriel y Luis. Ver v5/CONTEXTO.md pedidos 20-22.
HORAS9 = [("API-1663", 60, "R"), ("API-1834", 57, "F"), ("API-1738", 53, "F"), ("API-1693", 45, "R"), ("API-1427", 43, "F"),
          ("API-1832", 40, "R"), ("API-1877", 36, "F"), ("API-1839", 32, "F"), ("API-1867", 31, "F"), ("API-1901", 25, "R"),
          ("API-1764", 24, "R"), ("API-1822", 24, "R"), ("API-1908", 22, "R"), ("API-1859", 20, "R"), ("API-1858", 16, "R"),
          ("API-1851", 16, "F"), ("API-1872", 8, "F"), ("API-1871", 7, "F"), ("API-1682", 5, "R")]
# Escala Fibonacci (regla de Didier): 1, 2, 3, 5, 8; topes en horas con 30 %: 6 / 11 / 17 / 28 / 39 (39 h = 30 h de trabajo).
# Más de 30 h de trabajo: se sacan bloques completos de 30 h (8 puntos cada uno) y el resto toma su tamaño
# (evita que 45 h y 60 h valgan lo mismo, como pasaba al partir en mitades iguales).
LIM5, PTS5 = [6, 11, 17, 28, 39], [1, 2, 3, 5, 8]


def talla(a):
    return next(p for l, p in zip(LIM5, PTS5) if a <= l + 1e-9)


def puntos(h):
    a = h * 1.3
    bloques = int((a + 1e-9) // LIM5[-1])
    resto = a - bloques * LIM5[-1]
    partes = [8] * bloques + ([talla(resto)] if resto > 1e-9 else [])
    return partes


fila9, PARTES = [], {}
for k, h, e in HORAS9:
    partes = puntos(h)
    PARTES[k] = partes
    fila9.append((k, e, h, h * 1.3, 1, sum(partes)))
SEPT_PTS = sum(n * pt for *_, n, pt in fila9)
SEPT_H = sum(r[2] for r in fila9)
assert SEPT_PTS == 164 and SEPT_H == 564 and len(fila9) == 19
# Puntos de septiembre por persona (dueño de las horas de cada tarea en el informe; uso interno, sin nombres en la lámina).
DUENO = {"Daniel": ["API-1663", "API-1834", "API-1738", "API-1832", "API-1764", "API-1858"],
         "Gabriel": ["API-1693", "API-1427", "API-1867", "API-1901", "API-1822", "API-1859", "API-1851", "API-1872", "API-1871", "API-1682"],
         "Luis": ["API-1877", "API-1839", "API-1908"]}
PP_SEPT = {d: sum(n * pt for k, e, h, a, n, pt in fila9 if k in ks) for d, ks in DUENO.items()}
# Capacidad (15 oct 2026): solo las horas reportadas en septiembre (columna I) de cada tarea, no las de meses anteriores.
# Las horas de septiembre de cada tarea se pasan por la misma escala Fibonacci (sin decimales: cada parte sube a la talla que la cubre).
HSEP = {"API-1663": 20, "API-1834": 33, "API-1738": 27, "API-1693": 6, "API-1427": 2}   # el resto: todas sus horas son de septiembre
H_SEP = {k: HSEP.get(k, h) for k, e, h, a, n, pt in fila9}
P_SEP = {k: puntos(H_SEP[k]) for k in H_SEP}
CAPAC = sum(sum(v) for v in P_SEP.values())
CAP_PP = {d: sum(sum(P_SEP[k]) for k in ks) for d, ks in DUENO.items()}
assert CAP_PP == {"Daniel": 46, "Gabriel": 44, "Luis": 27}
assert sum(H_SEP.values()) == 394 and round(CAPAC) == 117
# Capacidad real (15 oct 2026): todas las horas que el equipo reportó en septiembre (524 h), también las de tareas
# que no terminaron en el mes (y API-1860). Solo se usa para la capacidad; no cambia los puntos de ninguna tarea.
OTRAS = [("API-724", "Luis", 15, "Feedback"), ("API-1529", "Luis", 30, "En curso"), ("API-1854", "Luis", 37, "Feedback"),
         ("API-1696", "Gabriel", 12, "Pausado"), ("API-1925", "Gabriel", 12, "En curso"), ("API-1860", "Gabriel", 8, "Finalizada, la implementó un revisor"),
         ("API-1920", "Daniel", 16, "En curso")]
P_OTRAS = {k: sum(puntos(h)) for k, d, h, e in OTRAS}
H_OTRAS = sum(h for _, _, h, _ in OTRAS)
CAPAC_REAL = CAPAC + sum(P_OTRAS.values())
CAPR_PP = {d: CAP_PP[d] + sum(P_OTRAS[k] for k, dd, h, e in OTRAS if dd == d) for d in CAP_PP}
assert H_OTRAS == 130 and sum(H_SEP.values()) + H_OTRAS == 524 and CAPAC_REAL == 153 and CAPR_PP == {"Daniel": 51, "Gabriel": 52, "Luis": 50}
assert sum(PP_SEPT.values()) == SEPT_PTS and PP_SEPT == {"Daniel": 72, "Gabriel": 65, "Luis": 27}
tdx = 'style="padding:3px 7px;font-size:12.5px;white-space:nowrap"'
EST = {"F": "Finalizada", "R": "Ready for prod"}


def tabla_tareas(filas, total=False):
    # Horas totales de la tarea con sus puntos debajo; horas de septiembre con los puntos que representan (capacidad).
    th = 'style="white-space:nowrap;padding:2px 7px;text-align:right"'
    cab = ('<table style="border-spacing:0 3px"><thead><tr><th style="white-space:nowrap;padding:2px 7px">Tarea</th><th style="white-space:nowrap;padding:2px 7px">Estado</th>'
           f'<th {th}>Completa</th><th {th}>Septiembre</th></tr></thead><tbody>')
    td2 = 'style="padding:2px 7px;font-size:12.5px;line-height:1.2;white-space:nowrap" align="right"'

    def celda(horas, pts_txt):
        return f'<td {td2}>{horas}<br><b style="color:var(--blue-accent);font-size:12px">{pts_txt}</b></td>'

    def p1(x):
        return str(round(x, 1)).replace(".", ",")
    cuerpo = ''.join(
        f'<tr><td {tdx}><b>{k}</b></td><td {tdx}>{EST[e]}</td>'
        + celda(f'{h} h', f'{n * pt} pts' + (' (' + '+'.join(map(str, PARTES[k])) + ')' if len(PARTES[k]) > 1 else ''))
        + celda(f'{H_SEP[k]} h', f'{sum(P_SEP[k])} pts' + (' (' + '+'.join(map(str, P_SEP[k])) + ')' if len(P_SEP[k]) > 1 else '')) + '</tr>'
        for k, e, h, a, n, pt in filas)
    if total:
        cuerpo += (f'<tr><td {tdx}><b>Total</b></td><td {tdx}>19 tareas</td>'
                   + celda(f'<b>{SEPT_H} h</b>', f'{SEPT_PTS} pts') + celda(f'<b>{sum(H_SEP.values())} h</b>', f'{round(CAPAC)} pts') + '</tr>')
    return cab + cuerpo + '</tbody></table>'


# Regla (15 oct 2026): cada paquete = personas enteras × capacidad real por persona, para que subir o bajar de paquete
# sea solo sumar o quitar una persona. Capacidad real por persona = capacidad del equipo en septiembre / 3.
PPP = round(CAPAC_REAL / 3)
PPP_PAQ = CAPAC // 3   # puntos por persona del paquete: lo completado en septiembre (117) entre 3
PK3 = [("Inicial", 3 * PPP_PAQ), ("Ampliado", 4 * PPP_PAQ), ("Avanzado", 5 * PPP_PAQ)]   # personas solo internas
assert PPP == PP_PROM == 51 and PPP_PAQ == PP_PAQ == 39 and CAPAC == 117 and [v for _, v in PK3] == [117, 156, 195]
K7 = 1.1
bars7 = []
for i, (n, v) in enumerate(PK3):
    y = 30 + i * 74
    full = v >= CAPAC_REAL
    fill = "#22D0FF" if n == "Inicial" else "#EBEBFF"
    bars7.append(f'<rect x="0" y="{y}" width="300" height="64" rx="10" fill="#282E3F"/>')
    bars7.append(f'<rect x="8" y="{y+8}" width="{v*K7:.0f}" height="28" rx="6" fill="{fill}"/>')
    bars7.append(f'<text x="18" y="{y+28}" font-size="15" font-weight="700" fill="#000000">{n} · {v}</text>')
    cap = {3 * PPP_PAQ: "39 × 3 · el equipo de hoy", 4 * PPP_PAQ: "39 × 4 · una persona más", 5 * PPP_PAQ: "39 × 5 · dos personas más"}[v]
    bars7.append(f'<text x="10" y="{y+54}" font-size="13" font-weight="{700 if v == CAPAC_REAL else 400}" fill="#FFFFFF">{cap}</text>')
svg7b = ('<svg width="250" height="210" viewBox="0 0 300 252">'
         + ''.join(bars7) +
         f'<text x="2" y="16" font-size="13" font-weight="600" fill="#FFFFFF">Paquetes con 3 semanas de desarrollo</text></svg>')
# =============================================================== CONDICIONES DEL SERVICIO (pedido de Didier, 15 oct 2026)
# Última lámina para el cliente; las internas van después. Fuentes: pedido del 15 oct (3 días hasta UAT, pruebas unitarias
# sin límite, accesos) y condiciones de `instrucciones.md` (v1) y `REGLAS.md` §4.
cond = [("Tiempos de Viva Aerobus", [
            "<b>Revisión del PR y paso a UAT:</b> máximo 3 días hábiles desde que se abre el PR.",
            "<b>Feedback de UAT:</b> dentro de los 5 días desde abierto el PR; sin feedback, la actividad se da por entregada y se cobra.",
            "<b>Datos para certificar:</b> cuando haya que provisionar datos, Viva Aerobus los entrega en máximo 2 horas desde la solicitud.",
            "<b>Priorización del mes</b> definida antes de empezar."]),
        ("Calidad y pruebas", [
            "<b>Pruebas unitarias automatizadas sin límite:</b> el equipo implementa todas las que considere necesarias.",
            "<b>Sonar</b> como estándar común de buenas prácticas en la revisión.",
            "Un PR por actividad, con sus pruebas y la evidencia de resultados."]),
        ("Accesos y ambientes", [
            "<b>Accesos efectivos desde el inicio</b> a repositorios, ambientes de prueba, logs y monitoreo, bases de datos, VPN y Sonar.",
            "Un ambiente de UAT disponible para certificar cada entrega.",
            "Las demoras por accesos no cuentan en los tiempos del equipo."]),
        ("Alcance de cada actividad", [
            "<b>Criterios de aceptación claros</b>, sin ambigüedad y sin dependencias externas por resolver; si no, la actividad no se acepta todavía.",
            "<b>Máximo 8 puntos</b> por actividad; lo mayor se divide.",
            "<b>Cambios de alcance</b> o ajustes por cambios en la rama base después de aprobado el PR: actividad nueva, con su propia estimación."])]
cond_html = ''.join(
    f'<div class="card" style="padding:16px 20px"><div style="display:flex;gap:10px;align-items:center;margin-bottom:8px">'
    f'<span style="flex:0 0 28px;height:28px;border-radius:50%;background-color:var(--blue-accent);color:var(--black);font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center">{i + 1}</span>'
    f'<span style="font-size:19px;font-weight:700">{t}</span></div>'
    f'<ul style="margin:0 0 0 20px;font-size:14.5px;line-height:1.38">{"".join(f"<li style=\"margin-bottom:4px\">{x}</li>" for x in xs)}</ul></div>'
    for i, (t, xs) in enumerate(cond))
add("Condiciones del servicio",
    f"Condiciones del servicio: lo que se necesita para {hl('cumplir en cada entrega')}",
    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">{cond_html}</div>',
    "Propuesta de Tech and Solve. Días hábiles: lunes a viernes.")

# =============================================================== TÉRMINOS Y CONDICIONES (pedido de Didier, 15 oct 2026)
tyc = [("Cambio de paquete", "Viva Aerobus avisa con <b>mínimo 3 meses de anticipación</b> si va a subir o bajar de paquete, para planear la capacidad del equipo.", False),
       ("Facturación mensual", "Se factura el <b>100 % del paquete</b> cada mes. Solo se descuentan los puntos de las actividades que Tech and Solve no cumplió en la entrega.", False),
       ("Escala de puntos", "1, 2, 3, 5 u 8 (Fibonacci). Tech and Solve estima cada actividad en puntos antes de empezar; máximo 8 puntos por actividad, lo mayor se divide.", False),
       ("Puntos no usados", "Viva Aerobus es responsable de usar los puntos de su paquete: los que no use en el mes, por no tener actividades priorizadas, no se descuentan.", False),
       ("Actividades en curso al empezar", "Cómo se tratan las actividades que estén abiertas el día que empieza el nuevo modelo.", True)]
tyc_html = ''.join(
    f'<div class="{"pend" if pend else "card"}" style="padding:10px 20px;display:flex;gap:16px;align-items:center">'
    f'<div style="flex:0 0 300px;font-size:18px;font-weight:700">{t}'
    + ('<div><span class="tag" style="background-color:var(--white);color:var(--black);margin-top:6px">Por definir juntos</span></div>' if pend else '')
    + f'</div><div class="t16">{d}</div></div>'
    for t, d, pend in tyc)
add("Términos y condiciones", f"Términos y condiciones: {hl('cambios de paquete con 3 meses de aviso')}",
    f'<div style="display:flex;flex-direction:column;gap:8px">{tyc_html}</div>',
    "Propuesta de Tech and Solve.")

# Lámina interna 1: las tareas terminadas en septiembre y sus puntos.
add("Ejemplo real · septiembre de 2026", f"En septiembre se trabajaron {hl(str(CAPAC) + ' puntos')} en las tareas terminadas",
    # Alerta pedida por Didier (15 oct 2026): lámina de uso interno, no se muestra al cliente.
    '<div style="background:#B9720A;color:#fff;border-radius:8px;padding:8px 16px;margin-bottom:12px;font-size:15px;font-weight:700;letter-spacing:.02em">'
    'USO INTERNO · Esta lámina no se debe mostrar al cliente.</div>'
    '<div class="row" style="gap:12px;align-items:flex-start">'
    f'<div style="flex:1">{tabla_tareas(fila9[:10])}</div>'
    f'<div style="flex:1">{tabla_tareas(fila9[10:], total=True)}'
    '<div style="font-size:12px;margin-top:2px;color:var(--lighter-violet)">(8+…): más de 30 h de trabajo: bloques de 30 h (8 puntos) más el resto con su tamaño. Septiembre: las horas del mes con la misma escala.</div></div>'
    '<div style="flex:0 0 250px">'
    f'<div class="card" style="padding:14px 16px;border:2px solid var(--blue-accent)"><div style="font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--lighter-violet)">Trabajado en septiembre</div>'
    f'<div style="font-size:34px;font-weight:700;color:var(--blue-accent);line-height:1.1">{CAPAC} pts</div>'
    f'<div style="font-size:13px;line-height:1.35">Las {sum(H_SEP.values())} h que el equipo reportó en septiembre en estas {len(fila9)} tareas (columna «Septiembre»).</div></div>'
    f'<div class="card" style="margin-top:10px;padding:14px 16px"><div style="font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--lighter-violet)">Valor completo de estas tareas</div>'
    f'<div style="font-size:26px;font-weight:700;line-height:1.1">{SEPT_PTS} pts</div>'
    f'<div style="font-size:13px;line-height:1.35">{SEPT_H} h en total: {SEPT_H - sum(H_SEP.values())} h se trabajaron en meses anteriores. No es lo producido en septiembre.</div></div>'
    '</div></div>',
    "Septiembre de 2026 · F1 informe de septiembre: tareas del equipo en «Finalizada» o «Ready for prod» y sus horas reales. Puntos = horas reales del equipo + 30 %, máx. 30 h de trabajo por parte. No incluye API-1860, implementada por un revisor.", top=172)

# Lámina interna 2 (pedido de Didier, 15 oct 2026): la medición de la capacidad del equipo.
arrow_svg = ('<svg width="30" height="24" viewBox="0 0 30 24" style="flex:0 0 30px;align-self:center"><path d="M2,12 H22 M14,4 L24,12 L14,20" fill="none" stroke="#22D0FF" stroke-width="3"/></svg>')
flujo_cap = [(f"{sum(H_SEP.values()) + H_OTRAS} h", "reportadas en septiembre; nada de meses anteriores"),
             (f"{CAPAC} + {sum(P_OTRAS.values())} pts", f"{sum(H_SEP.values())} h en 19 tareas terminadas + {H_OTRAS} h en otras 7"),
             (f"{CAPAC_REAL} pts", "de esfuerzo dedicado en septiembre: la capacidad del equipo"),
             (f"{PPP} pts", "por persona en promedio")]
row_cap = arrow_svg.join(
    f'<div class="card" style="flex:1;padding:12px 16px"><div class="num" style="font-size:30px;color:var(--blue-accent)">{b_}</div>'
    f'<div style="font-size:14px;margin-top:4px;color:var(--lighter-violet)">{d_}</div></div>' for b_, d_ in flujo_cap)
tdc = 'style="padding:4px 8px;font-size:13.5px;white-space:nowrap"'
tab_otras = ('<table style="border-spacing:0 3px"><thead><tr><th style="padding:2px 8px">Tarea</th><th style="padding:2px 8px">Estado</th><th style="padding:2px 8px;text-align:right">Sept.</th><th style="padding:2px 8px;text-align:right">Puntos</th></tr></thead><tbody>'
             + ''.join(f'<tr><td {tdc}><b>{k}</b></td><td {tdc}>{e.split(",")[0]}</td><td {tdc} align="right">{h} h</td>'
                       f'<td {tdc} align="right"><b style="color:var(--blue-accent)">{P_OTRAS[k]}</b></td></tr>' for k, d, h, e in OTRAS)
             + f'<tr><td {tdc}><b>Total</b></td><td {tdc}>7 tareas</td><td {tdc} align="right"><b>{H_OTRAS} h</b></td><td {tdc} align="right"><b style="color:var(--blue-accent)">{sum(P_OTRAS.values())}</b></td></tr></tbody></table>')
HPERS = {"Daniel": 176, "Gabriel": 176, "Luis": 172}      # horas de septiembre por persona (columna I), F1
assert sum(HPERS.values()) == sum(H_SEP.values()) + H_OTRAS
tab_pers = ('<table style="border-spacing:0 3px"><thead><tr><th style="padding:2px 8px">Integrante</th><th style="padding:2px 8px;text-align:right">Horas</th><th style="padding:2px 8px;text-align:right">Terminadas</th><th style="padding:2px 8px;text-align:right">Otras</th><th style="padding:2px 8px;text-align:right">Total</th></tr></thead><tbody>'
            + ''.join(f'<tr><td {tdc}><b>Integrante {i + 1}</b></td><td {tdc} align="right">{HPERS[d]} h</td><td {tdc} align="right">{CAP_PP[d]}</td>'
                      f'<td {tdc} align="right">{CAPR_PP[d] - CAP_PP[d]}</td><td {tdc} align="right"><b style="color:var(--blue-accent)">{CAPR_PP[d]}</b></td></tr>'
                      for i, d in enumerate(("Daniel", "Gabriel", "Luis")))
            + f'<tr><td {tdc}><b>Equipo</b></td><td {tdc} align="right"><b>{sum(HPERS.values())} h</b></td><td {tdc} align="right">{CAPAC}</td><td {tdc} align="right">{sum(P_OTRAS.values())}</td><td {tdc} align="right"><b style="color:var(--blue-accent)">{CAPAC_REAL}</b></td></tr></tbody></table>')
# Lámina «La capacidad del equipo en septiembre fue de 153 puntos…» retirada por pedido de Didier (19 oct 2026); sus cálculos siguen arriba y los usa la lámina del paquete.
# add("Capacidad del equipo · septiembre de 2026", f"La capacidad del equipo en septiembre fue de {hl(str(CAPAC_REAL) + ' puntos')} de esfuerzo dedicado",
#     '<div style="background:#B9720A;color:#fff;border-radius:8px;padding:8px 16px;margin-bottom:12px;font-size:15px;font-weight:700;letter-spacing:.02em">'
#     'USO INTERNO · Esta lámina no se debe mostrar al cliente.</div>'
#     f'<div style="display:flex;gap:10px">{row_cap}</div>'
#     '<div class="row" style="gap:18px;align-items:flex-start;margin-top:14px">'
#     '<div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2px;color:var(--lighter-violet)">Horas de sept. en otras tareas</div>'
#     f'{tab_otras}</div>'
#     '<div style="flex:1.2;min-width:0"><div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2px;color:var(--lighter-violet)">Capacidad por integrante (puntos)</div>'
#     f'{tab_pers}</div>'
#     '</div>',
#     "Septiembre de 2026 · F1 informe de septiembre, columna «Registrado Septiembre26» (horas del mes). Cada tarea pasa sus horas del mes por la escala Fibonacci (+30 %, bloques de 30 h). No cuentan las horas de meses anteriores. API-1860 entra con sus 8 h (la implementó un revisor, pero las horas son del equipo).", top=172)

# Lámina interna 3 (pedido de Didier, 19 oct 2026): de la capacidad al paquete, con 3 semanas de desarrollo.
sem = ''.join(
    f'<div style="flex:1;border-radius:12px;padding:14px 16px;{"background-color:var(--blue-accent);color:var(--black)" if i < SEM_DEV else "border:2px dashed #5B5A66"}">'
    f'<div style="font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase">Semana {i + 1}</div>'
    + (f'<div style="font-size:20px;font-weight:700;margin-top:4px">Desarrollo</div><div style="font-size:14px;margin-top:4px">Cuenta para los puntos del paquete.</div>' if i < SEM_DEV else
       f'<div style="font-size:20px;font-weight:700;margin-top:4px">Revisión y certificación</div><div style="font-size:13px;line-height:1.3;margin-top:4px">Lo que se entrega esta semana no alcanza a pasar la revisión del PR (máx. 3 días hábiles) ni la certificación en UAT: no se cobra en el mes.</div>')
    + '</div>' for i in range(SEM_MES))
calc = [(f"{CAPAC_REAL} pts", "esfuerzo del mes (4 semanas, 524 h)"),
        (f"≈ {round(CAPAC_REAL * SEM_DEV / SEM_MES)} pts", "si solo cuentan 3 semanas de desarrollo"),
        (f"{CAPAC} pts", "completados en septiembre (Finalizada o Ready for prod)"),
        (f"{3 * PPP_PAQ} pts", f"paquete base: {PPP_PAQ} × 3 personas")]
row_calc = arrow_svg.join(
    f'<div class="card" style="flex:1;padding:12px 16px"><div class="num" style="font-size:28px;color:var(--blue-accent)">{b_}</div>'
    f'<div style="font-size:14px;margin-top:4px;color:var(--lighter-violet)">{d_}</div></div>' for b_, d_ in calc)
paq_tab = ''.join(
    f'<div class="card" style="flex:1;padding:14px 18px;{"border:2px solid var(--blue-accent)" if i == 0 else ""}">'
    f'<div style="font-size:20px;font-weight:700">{n}</div><div style="font-size:14px;color:var(--lighter-violet)">{k} personas × {PPP_PAQ} puntos</div>'
    f'<div style="display:flex;align-items:baseline;gap:8px;margin-top:4px"><span style="font-size:38px;font-weight:700;line-height:1;color:var(--blue-accent)">{v}</span><span style="font-size:15px">puntos a entregar en el mes</span></div></div>'
    for i, ((n, v), k) in enumerate(zip(PK3, (3, 4, 5))))
add("Del esfuerzo al paquete", f"El paquete base es de {hl(str(3 * PPP_PAQ) + ' puntos')}: lo que se completó en septiembre",
    '<div style="background:#B9720A;color:#fff;border-radius:8px;padding:8px 16px;margin-bottom:12px;font-size:15px;font-weight:700;letter-spacing:.02em">'
    'USO INTERNO · Esta lámina no se debe mostrar al cliente.</div>'
    f'<div style="display:flex;gap:12px">{sem}</div>'
    f'<div style="display:flex;gap:10px;margin-top:10px">{row_calc}</div>'
    '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin:10px 0 6px;color:var(--lighter-violet)">Puntos a proporcionar en el mes</div>'
    f'<div class="row" style="gap:14px">{paq_tab}</div>',
    f"Septiembre de 2026 (F1): {sum(H_SEP.values()) + H_OTRAS} h reportadas = {CAPAC_REAL} pts de esfuerzo; {sum(H_SEP.values())} h en las 19 tareas terminadas = {CAPAC} pts completados.", top=172)

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
# Lámina «Hoy se mide el esfuerzo…» retirada por pedido de Didier (15 oct 2026); su código de apoyo queda arriba sin uso.
# add("1 · Cómo trabajamos hoy", f"Hoy se mide el esfuerzo; lo que frena la entrega es {hl('la espera de revisión')}",
#     f'<div style="display:flex;gap:{gap}px">{cards}</div>' + arrows + chips +
#     '<div class="row" style="margin-top:12px">' +
#     ''.join(f'<div class="card" style="flex:1;padding:14px 20px"><div class="num" style="font-size:44px;color:var(--blue-accent)">{b}</div>'
#             f'<div class="t16" style="margin-top:6px;color:var(--lighter-violet)">{d}</div></div>' for b, d in stats) + '</div>',
#     "Septiembre de 2026, 26 actividades · F1 informe de septiembre · F3 Jira · F4 GitHub (lecturas del 9 de octubre de 2026).", top=172)

# =============================================================== 3 NUEVO RECORRIDO
w6 = 178
steps = [("1", "Diseño conjunto", "Se define la actividad con criterios de aceptación claros.", "Criterios de aceptación"),
         ("2", "Tamaño en puntos", "1, 2, 3, 5 u 8, en vez de horas. Máx. 30 h de trabajo.", "Tamaño acordado"),
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
# Lámina «El nuevo recorrido: seis pasos…» retirada por pedido de Didier (15 oct 2026).
# add("2 · Cómo trabajaremos", f"El nuevo recorrido: seis pasos y {hl('algo que se observa en cada uno')}",
#     f'<div style="display:flex;gap:14px">{hero}</div>'
#     '<div class="row" style="margin-top:16px">'
#     '<div class="card" style="flex:0 0 380px;border:2px solid var(--blue-accent)"><div style="font-size:20px;font-weight:700">Qué se paga</div>'
#     '<div class="t16" style="margin-top:6px;color:var(--lighter-violet)">Los puntos de cada tarea finalizada (Ready for prod), dentro de su paquete mensual de puntos. '
#     'Si Viva Aerobus no da feedback en los 5 días, se cobra.</div></div>'
#     '<div class="card" style="flex:1"><div style="font-size:20px;font-weight:700">Reglas de corrección y cambios</div>'
#     '<ul style="margin:8px 0 0 18px;font-size:15px;line-height:1.45;color:var(--lighter-violet)">'
#     '<li><b style="color:var(--white)">Defectos:</b> solo se ajusta lo que es un error de la implementación; el equipo corrige todos los que se reporten en las etapas posteriores.</li>'
#     '<li><b style="color:var(--white)">Después de los 5 días</b> o ante cambios de alcance: control de cambios, que se cobra como tarea nueva con su propio tamaño.</li></ul></div></div>',
#     "Propuesta de Tech and Solve. Referencias de los PRs de septiembre de 2026 (F4 GitHub): 2 días hábiles de revisión, Sonar y estándar de PR.", top=172)

# =============================================================== 4 OFERTA
# Base (15 oct 2026): las 19 tareas de septiembre en Finalizado/Finalizada o Ready for prod en el informe, solo horas del equipo de Generic API.
flow4 = [("19", "tareas terminadas en septiembre"), ("564 h", "realmente invertidas por el equipo"),
         ("733,2 h", "con +30 % de desviación"), ("164 puntos", "por rango de tamaño")]
arrow_svg = ('<svg width="30" height="24" viewBox="0 0 30 24" style="flex:0 0 30px;align-self:center"><path d="M2,12 H22 M14,4 L24,12 L14,20" fill="none" stroke="#22D0FF" stroke-width="3"/></svg>')
row_a = arrow_svg.join(
    f'<div class="card" style="flex:1;padding:12px 16px"><div class="num" style="font-size:30px;color:var(--blue-accent)">{b}</div>'
    f'<div style="font-size:14px;margin-top:4px;color:var(--lighter-violet)">{d}</div></div>' for b, d in flow4)
sz = [("1", "hasta 6 h"), ("2", "hasta 11 h"), ("3", "hasta 17 h"), ("5", "hasta 28 h"), ("8", "hasta 39 h")]
row_b = ''.join(
    f'<div class="card" style="flex:1;padding:10px 12px;text-align:center"><div style="font-size:28px;font-weight:700;color:var(--blue-accent);line-height:1">{p}</div>'
    f'<div style="font-size:13px;margin-top:4px">{h}</div></div>' for p, h in sz) + \
    '<div class="card" style="flex:1.3;padding:10px 12px;text-align:center"><div style="font-size:20px;font-weight:700;line-height:1.3">Dividir</div><div style="font-size:13px;margin-top:4px">más de 39 h (30 h de trabajo)</div></div>'
pk = [("Inicial", "para meses de menos carga", "78", "Una persona menos que hoy.", ""),
      ("Ampliado", "la capacidad de hoy", "117", "Capacidad de septiembre de 2026.", ""),
      ("Avanzado", "para meses de más carga", "156", "Una persona más que hoy.", "")]
row_c = ''.join(
    f'<div class="card" style="flex:1;padding:14px 18px{";border:3px solid var(--blue-accent)" if i == 1 else ""}">'
    f'<div><div style="font-size:24px;font-weight:700;line-height:1.2">{n}</div><div style="font-size:14px;color:var(--lighter-violet)">{p}</div></div>'
    f'<div style="display:flex;align-items:baseline;gap:10px"><div class="num" style="font-size:56px;color:var(--blue-accent)">{pts}</div><div class="t16">puntos al mes</div></div>'
    f'<div class="t16" style="margin-top:4px">Máx.: {pts} × valor del punto</div>'
    f'<div style="font-size:14px;margin-top:6px;color:var(--lighter-violet)">{h}<br>{e}</div></div>'
    for i, (n, p, pts, h, e) in enumerate(pk)) + \
    '<div class="pend" style="flex:0 0 190px;padding:14px"><span class="tag" style="background-color:var(--white);color:var(--black)">Pendiente</span>' \
    '<div class="t16" style="margin-top:8px"><b>Valor del punto</b><br>se acuerda antes de empezar.</div></div>'
# Lámina «Tamaños y paquetes construidos con lo que ya entregamos» retirada por pedido de Didier (15 oct 2026).
# add("3 · Cómo se calcula", f"Tamaños y paquetes construidos con {hl('lo que ya entregamos')}",
#     f'<div style="display:flex;gap:10px">{row_a}</div>'
#     '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin:14px 0 6px;color:var(--lighter-violet)">Tamaño en puntos según horas reales + 30 %</div>'
#     f'<div style="display:flex;gap:8px">{row_b}</div>'
#     '<div style="font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin:14px 0 6px;color:var(--lighter-violet)">Paquetes mensuales de puntos</div>'
#     f'<div class="row" style="gap:24px">{row_c}</div>',
#     "Septiembre de 2026 · F1 informe de septiembre: tareas en «Finalizado», «Finalizada» o «Ready for prod», solo horas del equipo de Generic API · F5 escala Fibonacci (práctica de industria).", top=172)

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
# Lámina «Cada mes medimos y mejoramos; empezamos con tareas reales» retirada por pedido de Didier (15 oct 2026).
# add("4 · Cómo evolucionamos", f"Cada mes medimos y mejoramos; {hl('empezamos con tareas reales')}",
#     f'<div style="display:flex;gap:16px">{ccards}</div>{loop}'
#     f'<div class="row" style="gap:12px">{rc}</div>'
#     '<div class="row" style="margin-top:12px;gap:14px">'
#     '<div class="card" style="flex:1.15;background-color:var(--blue-accent);color:var(--black)"><div style="font-size:14px;font-weight:600;letter-spacing:.1em;text-transform:uppercase">Siguiente paso</div>'
#     '<div style="font-size:20px;font-weight:700;line-height:1.25;margin-top:4px">Elegir un paquete y entregar una muestra de tareas reales del backlog.</div></div>'
#     '<div class="pend" style="flex:1.5;padding:12px 18px"><span class="tag" style="background-color:var(--white);color:var(--black)">Por definir juntos</span>'
#     '<ul style="margin:8px 0 0 18px;font-size:14px;line-height:1.4">' + ''.join(f'<li>{p}</li>' for p in pend) + '</ul></div></div>',
#     "Propuesta de Tech and Solve · Línea base: septiembre de 2026 (F1 informe, F3 Jira, F4 GitHub). Actividades abiertas al 9 de octubre de 2026.", top=172)

# ---------------------------------------------------------------- ENSAMBLE
import re as _re
LIGHT = {"#22D0FF": "#5300DF", "#282E3F": "#EBEBFF", "#EBEBFF": "#5B5A66", "#FFFFFF": "#1A1E27", "#280265": "#FFFFFF", "#000000": "#FFFFFF"}


def a_claro(h):      # colores fijos del contenido (pensado en oscuro) al claro, en una sola pasada
    return _re.sub(r"#[0-9A-Fa-f]{6}", lambda m: LIGHT.get(m.group(0).upper(), m.group(0)), h)


def a_cqw(h):        # px a 1280 px de ancho → cqw, en estilos en línea y en el tamaño de los SVG
    h = _re.sub(r"(<svg\b[^>]*?)\swidth=\"(\d+(?:\.\d+)?)\"\s+height=\"(\d+(?:\.\d+)?)\"",
                lambda m: f'{m.group(1)} style="width:{float(m.group(2)) / 12.8:.3f}cqw;height:{float(m.group(3)) / 12.8:.3f}cqw;max-width:100%"', h)
    h = _re.sub(r"<svg\b([^>]*)\sstyle=\"([^\"]*)\"([^>]*)\sstyle=\"([^\"]*)\"", lambda m: f'<svg{m.group(1)} style="{m.group(2)};{m.group(4)}"{m.group(3)}', h)
    return _re.sub(r"(-?\d+(?:\.\d+)?)px", lambda m: f"{float(m.group(1)) / 12.8:.3f}cqw", h)


FOOT = "Propuesta de cambio de dinámica de trabajo · Generic API · Viva Aerobus"
total = len(slides)
out = []
for n, (kick, title, body, src_, kind, top) in enumerate(slides, 1):
    if kind == "cover":
        out.append(
            '<section class="slide"><div class="in" style="background:var(--violet);color:#fff;padding:5cqw 6cqw;--blue-accent:#EBEBFF">'
            '<div style="width:11cqw;background:#fff;border-radius:.8cqw;padding:.9cqw 1.3cqw"><img src="{{LOGO_DARK_VIOLET}}" alt="Tech and Solve logo" style="width:100%;height:auto;display:block"></div>'
            f'<p style="margin:2cqw 0 1cqw;font-size:1.3cqw;letter-spacing:.15cqw;text-transform:uppercase;opacity:.8;font-weight:600">{kick}</p>'
            f'<h1 style="font-size:3.3cqw;line-height:1.12;margin:0 0 1.8cqw;max-width:80cqw">{title}</h1>'
            f'<div>{a_cqw(body)}</div>'
            '<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:1.1cqw;opacity:.85;'
            'border-top:1px solid rgba(255,255,255,.25);padding-top:1.4cqw">'
            '<span>Viva Aerobus · Generic API<br>Propuesta comercial</span>'
            '<span style="text-align:right">Tech and Solve · Octubre de 2026<br>Documento confidencial</span></div>'
            '</div></section>')
    else:
        out.append(
            f'<section class="slide"><div class="in"><h2>{a_claro(title)}</h2>'
            f'<div class="content">{a_cqw(a_claro(body))}</div>'
            f'<p class="src" style="margin-top:.8cqw">{src_}</p>'
            f'<div class="foot">{FOOT}</div></div></section>')

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tech and Solve - Propuesta de cambio de dinámica de trabajo · Viva Aerobus</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{chr(10).join(out)}
<div class="hint">← → para navegar · Ctrl/Cmd+P para PDF</div>
<script>{JS}</script>
</body>
</html>"""
open(sys.argv[1], "w", encoding="utf-8").write(html)
print("diapositivas:", total)
