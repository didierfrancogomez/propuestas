#!/usr/bin/env python3
"""Reescribe en la presentación SURA las láminas que dependen del modelo de tallas y ajusta las internas.

Láminas que regenera (se buscan por su título, no por número): capacidad por talla (4), mezclas (5) y reparto por persona
(interna, siempre la última). Ajusta las internas de septiembre y del plan Inicial (aviso de datos de referencia, leyendas).

Lee datos.json (lo genera generar_modelo.py, ya verificado contra el Excel). Idempotente: puede correrse varias veces.
Solo toca el HTML de SURA; nunca archivos de Viva.
"""
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(AQUI, "..", "tech-and-solve-propuesta-paquetes-de-actividades.html")
m = json.load(open(os.path.join(AQUI, "datos.json")))
ORDEN = ["XL", "L", "M", "S", "XS"]
PUNTOS = {"XL": 8, "L": 5, "M": 3, "S": 2, "XS": 1}
COL = {"XL": "#280265", "L": "#5300DF", "M": "#8A5CF0", "S": "#B9A6F5", "XS": "#DCD8EC"}
PLANES = [(p["nombre"], p["personas"], p["capacidad"]) for p in m["planes"]]
FOOT = '<div class="foot">Propuesta de cambio de dinámica de trabajo · SURA</div>'
INTERNO = ('<div style="background:#B9720A;color:#fff;border-radius:0.625cqw;padding:0.625cqw 1.250cqw;margin-bottom:0.781cqw;'
           'font-size:1.172cqw;font-weight:700;letter-spacing:.02em">USO INTERNO · Esta lámina no se debe mostrar al cliente.</div>')
REF = "Proyecto de referencia: Generic API, Viva Aerobus. "


def txt(mix):
    return " + ".join(f"{mix[t]} {t}" for t in ORDEN if mix.get(t))


def slide_capacidad():
    td = "padding:0.625cqw 1.406cqw;font-size:1.250cqw;background:transparent;border-bottom:0.078cqw solid #DCD8EC;border-radius:0"
    chip = lambda x: ('<span style="display:inline-flex;align-items:center;justify-content:center;width:3.125cqw;height:3.125cqw;'
                      f'border-radius:50%;background-color:var(--blue-accent);color:var(--black);font-weight:700;font-size:1.250cqw">{x}</span>')
    desc = {"XS": "Ajuste puntual: un cambio menor o una corrección acotada", "S": "Cambio acotado sobre un componente existente",
            "M": "Funcionalidad estándar con sus pruebas", "L": "Funcionalidad con varias reglas o integraciones",
            "XL": "La mayor permitida; lo que la supere se divide"}
    filas = ""
    for t in ["XS", "S", "M", "L", "XL"]:
        celdas = "".join(f'<td style="{td};text-align:center;font-size:1.719cqw;font-weight:700;color:var(--blue-accent)">{p["max_por_talla"][t]}</td>' for p in m["planes"])
        filas += f'<tr><td style="{td}">{chip(t)}</td><td style="{td}">{desc[t]}</td>{celdas}</tr>'
    base = m["sept_por_talla"]
    lbl = 'font-size:0.938cqw;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--lighter-violet)'
    return ('<section class="slide"><div class="in"><h2>Cuántas características de cada talla <span style="color:var(--blue-accent)">soporta cada plan</span> al mes</h2><div class="content">'
            '<table><colgroup><col style="width:9%"><col style="width:46%"><col style="width:15%"><col style="width:15%"><col style="width:15%"></colgroup>'
            '<thead><tr><th>Talla</th><th>Qué tipo de característica</th>' + "".join(f'<th style="text-align:center">{n}</th>' for n, _, _ in PLANES) + '</tr></thead>'
            f'<tbody>{filas}</tbody></table>'
            '<div class="row" style="margin-top:1.094cqw">'
            f'<div class="card" style="flex:1;padding:0.938cqw 1.406cqw"><div style="{lbl}">Máximo por talla</div><div class="t16" style="margin-top:0.312cqw">'
            'Cada columna muestra el máximo si todas las características del mes fueran de una sola talla (número entero). En la práctica las tallas se mezclan, y Tech and Solve lleva el saldo del plan y lo comparte en cada priorización.</div></div>'
            f'<div class="card" style="flex:1;padding:0.938cqw 1.406cqw;border:0.156cqw solid var(--blue-accent)"><div style="{lbl}">Perfil real de septiembre en el plan Inicial</div>'
            f'<div style="font-size:1.406cqw;font-weight:700;margin-top:0.156cqw">{txt(base)}</div>'
            '<div class="t16" style="margin-top:0.312cqw">Las horas que el equipo de referencia dedicó en septiembre a sus tareas terminadas, expresadas en tallas: llenan el plan Inicial.</div></div></div>'
            '</div><p class="src" style="margin-top:.8cqw">Propuesta de Tech and Solve. Capacidad medida con el tiempo real invertido por el equipo de referencia (septiembre de 2026).</p>'
            f'{FOOT}</div></section>\n')


def slide_mezclas():
    td = "padding:0.625cqw 1.094cqw;background:transparent;border-bottom:0.078cqw solid #DCD8EC;border-radius:0;vertical-align:middle"

    def celda(mix, cap):
        assert sum(PUNTOS[t] * c for t, c in mix.items()) == cap
        orden = [t for t in ORDEN if mix.get(t)]
        barra = "".join(f'<span style="display:block;width:{PUNTOS[t] * mix[t] / cap * 100:.2f}%;background:{COL[t]}"></span>' for t in orden)
        return (f'<td style="{td}"><div style="font-size:1.250cqw;font-weight:700;line-height:1.2">{txt(mix)}</div>'
                f'<div style="display:flex;height:0.938cqw;border-radius:0.469cqw;overflow:hidden;margin:0.391cqw 0">{barra}</div>'
                f'<div style="font-size:1.016cqw;color:var(--lighter-violet)">{sum(mix.values())} características en el mes</div></td>')

    cuerpo = "".join(
        f'<tr><td style="{td}"><div style="font-size:1.406cqw;font-weight:700;color:var(--blue-accent)">{mz["nombre"]}</div>'
        f'<div style="font-size:1.016cqw;line-height:1.3;color:var(--lighter-violet)">{mz["desc"]}</div></td>'
        + "".join(celda(p["mezcla"], cap) for p, (_, _, cap) in zip(mz["planes"], PLANES)) + '</tr>' for mz in m["mezclas"])
    leyenda = "".join(f'<span style="display:inline-flex;align-items:center;gap:0.391cqw;margin-right:1.250cqw"><span style="width:1.094cqw;height:1.094cqw;border-radius:0.234cqw;background:{COL[t]};border:0.078cqw solid #DCD8EC"></span>{t}</span>' for t in ORDEN)
    return ('<section class="slide"><div class="in"><h2>Cada plan se puede llenar con <span style="color:var(--blue-accent)">distintas mezclas de tallas</span></h2><div class="content">'
            '<table><colgroup><col style="width:22%"><col style="width:26%"><col style="width:26%"><col style="width:26%"></colgroup>'
            '<thead><tr><th>Mezcla</th>' + "".join(f'<th>{n}</th>' for n, _, _ in PLANES) + '</tr></thead>'
            f'<tbody>{cuerpo}</tbody></table>'
            f'<div style="margin-top:0.938cqw;font-size:1.016cqw;color:var(--lighter-violet)">La barra muestra cuánto del plan ocupa cada talla: {leyenda}</div>'
            '<div style="margin-top:0.781cqw;background-color:var(--darker-gray);border-radius:0.938cqw;padding:0.938cqw 1.406cqw;font-size:1.211cqw;line-height:1.4">'
            '<b>Son ejemplos:</b> cada mes SURA puede mezclar las tallas como necesite, mientras quepan en su plan. Tech and Solve lleva el saldo y lo comparte en cada priorización.</div>'
            '</div><p class="src" style="margin-top:.8cqw">Propuesta de Tech and Solve. Cada mezcla ocupa el 100 % de la capacidad de su plan y pide un esfuerzo parecido del equipo; la primera es el perfil de septiembre escalado a cada plan.</p>'
            f'{FOOT}</div></section>\n')


def slide_equipo():
    td = "padding:0.469cqw 0.938cqw;background:transparent;border-bottom:0.078cqw solid #DCD8EC;border-radius:0;vertical-align:top"

    def celda(equipo):
        grupos = []
        for per in equipo:
            clave = tuple(per[t] for t in ORDEN)
            for g in grupos:
                if g[0] == clave:
                    g[1] += 1
                    break
            else:
                grupos.append([clave, 1])
        grupos.sort(key=lambda g: -g[1])
        lineas = "".join(
            f'<div style="display:flex;gap:0.625cqw;align-items:baseline;margin-top:0.234cqw"><span style="flex:0 0 5.469cqw;font-size:0.938cqw;color:var(--lighter-violet)">{c} {"persona" if c == 1 else "personas"}</span>'
            f'<span style="font-size:1.094cqw;font-weight:700">{" + ".join(f"{x} {t}" for t, x in zip(ORDEN, v) if x)}</span></div>' for v, c in grupos)
        return f'<td style="{td}">{lineas}</td>'

    cuerpo = "".join(
        f'<tr><td style="{td}"><div style="font-size:1.328cqw;font-weight:700;color:var(--blue-accent)">{mz["nombre"]}</div></td>'
        + "".join(celda(p["equipo"]) for p in mz["planes"]) + '</tr>' for mz in m["mezclas"])
    ppp = m["pts_por_persona"]
    pi = m["por_integrante"]
    real_t = " · ".join(str(pi[str(i)]["terminadas"]) for i in (1, 2, 3))
    real_a = " · ".join(str(pi[str(i)]["terminadas"] + pi[str(i)]["otras"]) for i in (1, 2, 3))
    hp = [h for mz in m["mezclas"] for p in mz["planes"] for h in p["horas"]["por_persona_medio"]]
    h_min, h_max = round(min(hp)), round(max(hp))
    return ('<section class="slide"><div class="in"><h2>Cómo se reparte cada mezcla en el equipo: <span style="color:var(--blue-accent)">' + f'{ppp} puntos por persona</span></h2><div class="content">'
            + INTERNO +
            '<table style="border-spacing:0 0.234cqw"><colgroup><col style="width:16%"><col style="width:28%"><col style="width:28%"><col style="width:28%"></colgroup>'
            '<thead><tr><th style="padding:0.156cqw 0.938cqw">Mezcla</th>' + "".join(f'<th style="padding:0.156cqw 0.938cqw">{n} · {k} personas</th>' for n, k, _ in PLANES) + '</tr></thead>'
            f'<tbody>{cuerpo}</tbody></table>'
            '<div style="margin-top:0.781cqw;background-color:var(--darker-gray);border-radius:0.938cqw;padding:0.781cqw 1.406cqw;font-size:1.133cqw;line-height:1.4">'
            f'<b>Cada persona toma exactamente {ppp} puntos al mes</b> (XS = 1 · S = 2 · M = 3 · L = 5 · XL = 8): {ppp} = 117 de septiembre / 3 personas. '
            f'Es un reparto objetivo y parejo: en septiembre fue desigual ({real_t} puntos en tareas terminadas) y quedó parejo con todo el esfuerzo del mes ({real_a}). Con el esfuerzo típico de cada talla, cada persona queda entre {h_min} y {h_max} h de trabajo al mes (unas 3 semanas de 42 h). Subir o bajar de plan es sumar o quitar una persona.</div>'
            f'</div><p class="src" style="margin-top:.8cqw">{REF}F1 informe de septiembre de 2026. Mezclas de la lámina 5. Cálculo en modelo-calculo-tallas.xlsx (hojas Mezclas y Equipo).</p>'
            f'{FOOT}</div></section>\n')


def main():
    t = open(HTML).read()
    slides = list(re.finditer(r'<section class="slide">.*?</section>\n?', t, flags=re.S))

    def idx(h2):
        r = [i for i, s in enumerate(slides) if h2 in s.group(0)]
        assert len(r) == 1, (h2, r)
        return r[0]

    for clave, nuevo in (("Cuántas características de cada talla", slide_capacidad()), ("Cada plan se puede llenar con", slide_mezclas()),
                         ("Cómo se reparte cada mezcla en el equipo", slide_equipo())):
        s = slides[idx(clave)]
        t = t.replace(s.group(0), nuevo)
        slides = list(re.finditer(r'<section class="slide">.*?</section>\n?', t, flags=re.S))

    # Lámina 10 (tareas de septiembre): leyenda de la escala sin ambigüedad y fuente del cálculo
    a = re.search(r"Tallas: XS = 1 pt \(hasta 6 h\).*?con su talla\.", t, flags=re.S)
    if a:
        t = t.replace(a.group(0), "Tallas por horas reales + 30 %: XS = 1 pt (hasta 6 h) · S = 2 (11 h) · M = 3 (17 h) · L = 5 (28 h) · XL = 8 (39 h). "
                  "Una característica de más de 39 h (30 h de trabajo) se divide: bloques XL de 39 h más el resto con su talla.")
    if "Cálculo tarea por tarea" not in t:
        t = t.replace("No incluye API-1860, implementada por un revisor.</p>", "No incluye API-1860, implementada por un revisor. Cálculo tarea por tarea en modelo-calculo-tallas.xlsx.</p>")
    # Lámina 11 (plan Inicial): equivalencias exactas en vez de máximos por talla
    hpp = m["horas_por_punto"]
    for p in m["planes"]:
        cap = p["capacidad"]
        viejo = re.search(r"= \d+ S · %d M · \d+ L · \d+ XL" % (cap // 3), t)
        if not viejo:
            continue
        t = t.replace(viejo.group(0), f"= {cap // 3} características M (exacto) · ≈ {round(cap * hpp)} h de trabajo")
    # Láminas 10 y 11: aviso de que son datos de referencia de otro equipo y proyecto
    aviso = ('<div style="background:#B9720A;color:#fff;border-radius:0.625cqw;padding:0.45cqw 1.250cqw;margin-bottom:0.7cqw;letter-spacing:.02em">'
             '<div style="font-size:1.172cqw;font-weight:700">USO INTERNO · Esta lámina no se debe mostrar al cliente.</div>'
             '<div style="font-size:1.0cqw;font-weight:500;margin-top:0.1cqw">Datos de referencia del equipo de Generic API de Viva Aerobus. '
             'En SURA pueden variar según el tipo de proyecto.</div></div>')
    banner = re.compile(r'<div style="background:#B9720A;color:#fff;border-radius:0\.625cqw;padding:0\.625cqw 1\.250cqw;margin-bottom:0\.938cqw;'
                        r'font-size:1\.172cqw;font-weight:700;letter-spacing:\.02em">USO INTERNO · Esta lámina no se debe mostrar al cliente\.</div>')
    for clave in ("Tallas de referencia", "El plan Inicial es de"):
        s = [x.group(0) for x in re.finditer(r'<section class="slide">.*?</section>\n?', t, flags=re.S) if clave in x.group(0)]
        assert len(s) == 1, clave
        if "pueden variar según el tipo de proyecto" in s[0]:
            continue
        nuevo, n = banner.subn(aviso, s[0])
        assert n == 1, clave
        t = t.replace(s[0], nuevo)
    # La lámina de reparto por persona es interna: va siempre al final, después de las del cliente y de las otras internas
    eq = [x.group(0) for x in re.finditer(r'<section class="slide">.*?</section>\n?', t, flags=re.S) if "Cómo se reparte cada mezcla" in x.group(0)]
    assert len(eq) == 1
    t = t.replace(eq[0], "")
    t = t.replace('<div class="hint">', eq[0] + '<div class="hint">', 1)
    t = t.replace(">XS · 1 pts<", ">XS · 1 pt<")
    open(HTML, "w").write(t)
    print("láminas:", t.count('class="slide"'))


if __name__ == "__main__":
    main()
