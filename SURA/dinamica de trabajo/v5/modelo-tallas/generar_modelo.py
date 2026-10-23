#!/usr/bin/env python3
"""Genera modelo-calculo-tallas.xlsx (con fórmulas) y datos.json para la propuesta SURA.

Una sola fuente de verdad: las horas del informe de septiembre de 2026 (Viva Aerobus, solo lectura)
-> tallas -> capacidad de los planes -> mezclas -> reparto por persona. El Excel lleva fórmulas vivas;
datos.json lleva los mismos números calculados en Python para la presentación, y el script comprueba
que ambos coinciden (evalúa el Excel con la librería `formulas`).

Uso: python generar_modelo.py   (requiere xlsxwriter y formulas)
"""
import json
import math
import os
import sys

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

AQUI = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(AQUI, "modelo-calculo-tallas.xlsx")

# --------------------------------------------------------------------------- insumos
# Informe de septiembre de 2026, hoja «Seguimiento Mes» (columnas G, H, I): horas del equipo de referencia.
# (tarea, estado, integrante, grupo, horas completas = H + I, horas de septiembre = I)
TAREAS = [
    ("API-1663", "Ready for prod", 1, "Terminada", 60, 20), ("API-1834", "Finalizada", 1, "Terminada", 57, 33),
    ("API-1738", "Finalizado", 1, "Terminada", 53, 27), ("API-1693", "Ready for prod", 2, "Terminada", 45, 6),
    ("API-1427", "Finalizada", 2, "Terminada", 43, 2), ("API-1832", "Ready for prod", 1, "Terminada", 40, 40),
    ("API-1877", "Finalizada", 3, "Terminada", 36, 36), ("API-1839", "Finalizado", 3, "Terminada", 32, 32),
    ("API-1867", "Finalizada", 2, "Terminada", 31, 31), ("API-1901", "Ready for prod", 2, "Terminada", 25, 25),
    ("API-1764", "Ready for prod", 1, "Terminada", 24, 24), ("API-1822", "Ready for prod", 2, "Terminada", 24, 24),
    ("API-1908", "Ready for prod", 3, "Terminada", 22, 22), ("API-1859", "Ready for prod", 2, "Terminada", 20, 20),
    ("API-1858", "Ready for prod", 1, "Terminada", 16, 16), ("API-1851", "Finalizada", 2, "Terminada", 16, 16),
    ("API-1872", "Finalizada", 2, "Terminada", 8, 8), ("API-1871", "Finalizada", 2, "Terminada", 7, 7),
    ("API-1682", "Ready for prod", 2, "Terminada", 5, 5),
    ("API-724", "Feedback", 3, "Otra", 15, 15), ("API-1529", "En curso", 3, "Otra", 30, 30),
    ("API-1854", "Feedback", 3, "Otra", 37, 37), ("API-1696", "Pausado", 2, "Otra", 12, 12),
    ("API-1925", "En curso", 2, "Otra", 12, 12), ("API-1860", "Finalizada (la implementó un revisor)", 2, "Otra", 8, 8),
    ("API-1920", "En curso", 1, "Otra", 16, 16),
]
MARGEN = 0.30
HORAS_XL = 30            # horas de trabajo de una característica XL (39 h con el 30 %)
JORNADA_SEM, SEMANAS = 42, 4
TALLAS = ["XS", "S", "M", "L", "XL"]            # orden de la escala (de menor a mayor)
PUNTOS = {"XS": 1, "S": 2, "M": 3, "L": 5, "XL": 8}
TOPES = {"XS": 6, "S": 11, "M": 17, "L": 28}    # horas con el 30 %; XL = 39 (se calcula)
DESC = {"XS": "Ajuste puntual: un cambio menor o una corrección acotada",
        "S": "Cambio acotado sobre un componente existente",
        "M": "Funcionalidad estándar con sus pruebas",
        "L": "Funcionalidad con varias reglas o integraciones",
        "XL": "La mayor permitida; lo que la supere se divide"}
PERSONAS_REF = 3
PLANES = [("Inicial", 3), ("Profesional", 4), ("Alta velocidad", 5)]
ORDEN = ["XL", "L", "M", "S", "XS"]             # orden de presentación (de mayor a menor)

# Mezclas: unidades por talla que llenan EXACTAMENTE la capacidad de cada plan (117 / 156 / 195 puntos).
MEZCLAS = [
    ("Perfil de septiembre", "Como trabajó el equipo de referencia: pocas características grandes.",
     [{"XL": 10, "L": 4, "M": 1, "S": 5, "XS": 4}, {"XL": 13, "L": 6, "M": 1, "S": 7, "XS": 5},
      {"XL": 16, "L": 7, "M": 2, "S": 9, "XS": 8}]),
    ("Balanceada", "Evolución normal del producto: de todo un poco.",
     [{"XL": 4, "L": 6, "M": 10, "S": 10, "XS": 5}, {"XL": 6, "L": 8, "M": 12, "S": 12, "XS": 8},
      {"XL": 8, "L": 10, "M": 15, "S": 14, "XS": 8}]),
    ("Muchas y pequeñas", "Mantenimiento, ajustes y mejoras puntuales.",
     [{"L": 2, "M": 15, "S": 25, "XS": 12}, {"L": 3, "M": 20, "S": 30, "XS": 21}, {"L": 4, "M": 25, "S": 40, "XS": 20}]),
]


# --------------------------------------------------------------------------- modelo en Python
def partes(horas):
    """Horas reales -> lista de tallas: bloques XL completos + el resto con la talla que lo cubre."""
    a = round(horas * (1 + MARGEN), 6)
    tope_xl = HORAS_XL * (1 + MARGEN)
    bloques = int(a // tope_xl + 1e-9)
    resto = round(a - bloques * tope_xl, 6)
    out = ["XL"] * bloques
    if resto > 0:
        topes = [TOPES[t] for t in TALLAS[:-1]] + [tope_xl]
        out.append(next(t for t, l in zip(TALLAS, topes) if resto <= l))
    return out


def pts(lista):
    return sum(PUNTOS[t] for t in lista)


def conteo(lista):
    return {t: lista.count(t) for t in TALLAS}


def modelo():
    m = {"tareas": []}
    for k, est, per, grupo, hc, hs in TAREAS:
        pc, ps = partes(hc), partes(hs)
        m["tareas"].append({"id": k, "estado": est, "integrante": per, "grupo": grupo, "h_completa": hc, "h_sept": hs,
                            "tallas_completa": pc, "pts_completa": pts(pc), "tallas_sept": ps, "pts_sept": pts(ps)})
    term = [t for t in m["tareas"] if t["grupo"] == "Terminada"]
    otras = [t for t in m["tareas"] if t["grupo"] == "Otra"]
    m["horas"] = {"completa_terminadas": sum(t["h_completa"] for t in term), "sept_terminadas": sum(t["h_sept"] for t in term),
                  "sept_otras": sum(t["h_sept"] for t in otras)}
    m["horas"]["sept_total"] = m["horas"]["sept_terminadas"] + m["horas"]["sept_otras"]
    m["pts_completa_terminadas"] = sum(t["pts_completa"] for t in term)
    m["pts_sept_terminadas"] = sum(t["pts_sept"] for t in term)
    m["pts_sept_otras"] = sum(t["pts_sept"] for t in otras)
    m["capacidad_real"] = m["pts_sept_terminadas"] + m["pts_sept_otras"]
    m["horas_por_punto"] = m["horas"]["sept_terminadas"] / m["pts_sept_terminadas"]
    base = {t: 0 for t in TALLAS}
    for t in term:
        for x in t["tallas_sept"]:
            base[x] += 1
    m["sept_por_talla"] = base
    m["pts_por_persona"] = m["pts_sept_terminadas"] / PERSONAS_REF
    assert m["pts_por_persona"] == int(m["pts_por_persona"])
    m["pts_por_persona"] = int(m["pts_por_persona"])
    m["por_integrante"] = {i: {"terminadas": sum(t["pts_sept"] for t in term if t["integrante"] == i),
                               "otras": sum(t["pts_sept"] for t in otras if t["integrante"] == i),
                               "horas": sum(t["h_sept"] for t in m["tareas"] if t["integrante"] == i)} for i in (1, 2, 3)}
    m["planes"] = []
    for nombre, n in PLANES:
        cap = n * m["pts_por_persona"]
        m["planes"].append({"nombre": nombre, "personas": n, "capacidad": cap,
                            "max_por_talla": {t: cap // PUNTOS[t] for t in TALLAS}})
    return m


def reparto(mezcla, n, por_persona):
    """Reparte una mezcla entre n personas, cada una con exactamente `por_persona` puntos y carga parecida."""
    import itertools
    def candidatos(rem, share):
        rangos = [range(max(0, int(share[t]) - 4), min(rem[t], int(share[t]) + 5) + 1) for t in ORDEN]
        out = []
        for v in itertools.product(*rangos):
            if sum(PUNTOS[t] * x for t, x in zip(ORDEN, v)) == por_persona:
                out.append((sum(abs(x - share[t]) for t, x in zip(ORDEN, v)), v))
        return [v for _, v in sorted(out)]

    def resolver(rem, k):
        if k == 1:
            v = tuple(rem[t] for t in ORDEN)
            return [v] if sum(PUNTOS[t] * x for t, x in zip(ORDEN, v)) == por_persona else None
        share = {t: rem[t] / k for t in ORDEN}
        for v in candidatos(rem, share):
            r = resolver({t: rem[t] - x for t, x in zip(ORDEN, v)}, k - 1)
            if r:
                return [v] + r
        return None

    sol = resolver({t: mezcla.get(t, 0) for t in ORDEN}, n)
    assert sol, (mezcla, n)
    return [dict(zip(ORDEN, v)) for v in sol]


def rangos_horas():
    """Horas de trabajo (sin el margen) que cubre cada talla: desde, punto medio y tope."""
    out, desde = {}, 0.0
    for t in TALLAS:
        tope = (TOPES.get(t, HORAS_XL * (1 + MARGEN))) / (1 + MARGEN)
        out[t] = {"desde": desde, "medio": (desde + tope) / 2, "tope": tope}
        desde = tope
    return out


def completar(m):
    rh = rangos_horas()
    m["rangos_horas"] = rh
    horas = lambda mix, k: sum(mix[t] * rh[t][k] for t in ORDEN)
    disp_persona = JORNADA_SEM * SEMANAS
    m["mezclas"] = []
    for nombre, desc, por_plan in MEZCLAS:
        fila = {"nombre": nombre, "desc": desc, "planes": []}
        for (pn, n), mix, plan in zip(PLANES, por_plan, m["planes"]):
            mix = {t: mix.get(t, 0) for t in ORDEN}
            assert sum(PUNTOS[t] * c for t, c in mix.items()) == plan["capacidad"], (nombre, pn)
            eq = reparto(mix, n, m["pts_por_persona"])
            for t in ORDEN:
                assert sum(p[t] for p in eq) == mix[t]
            assert all(sum(PUNTOS[t] * p[t] for t in ORDEN) == m["pts_por_persona"] for p in eq)
            h = {"medio": horas(mix, "medio"), "tope": horas(mix, "tope"),
                 "equivalentes": plan["capacidad"] * m["horas_por_punto"], "disponibles": n * disp_persona,
                 "por_persona_medio": [horas(p, "medio") for p in eq]}
            # Las mezclas deben pedir un esfuerzo parecido al del plan y caber en el mes
            assert abs(h["medio"] / h["equivalentes"] - 1) <= 0.05 and h["medio"] <= h["disponibles"], (nombre, pn, h)
            assert all(x <= disp_persona for x in h["por_persona_medio"])
            fila["planes"].append({"plan": pn, "mezcla": mix, "equipo": eq, "horas": h})
        m["mezclas"].append(fila)
    return m


# --------------------------------------------------------------------------- Excel
def construir(ruta, m, vals=None):
    """Escribe el libro. `vals` = {(hoja, celda): valor} para dejar el resultado calculado junto a cada fórmula."""
    vals = vals or {}
    wb = xlsxwriter.Workbook(ruta)
    VIO = "#280265"
    f_t = wb.add_format({"bold": True, "font_size": 15, "font_color": VIO})
    f_h = wb.add_format({"bold": True, "bg_color": VIO, "font_color": "#FFFFFF", "border": 1, "text_wrap": True, "valign": "vcenter"})
    f_n = wb.add_format({"border": 1})
    f_i = wb.add_format({"border": 1, "font_color": "#0000FF"})                       # entrada
    f_c = wb.add_format({"border": 1, "bg_color": "#EBEBFF"})                         # fórmula
    f_cb = wb.add_format({"border": 1, "bg_color": "#EBEBFF", "bold": True})
    f_p = wb.add_format({"border": 1, "bg_color": "#EBEBFF", "num_format": "0.0%"})
    f_d = wb.add_format({"border": 1, "bg_color": "#EBEBFF", "num_format": "0.00"})
    f_pi = wb.add_format({"border": 1, "font_color": "#0000FF", "num_format": "0%"})
    f_note = wb.add_format({"italic": True, "font_color": "#5B5A66", "text_wrap": True, "valign": "top"})
    f_ok = wb.add_format({"bold": True, "font_color": "#1B6B4F", "border": 1})
    f_bad = wb.add_format({"bold": True, "font_color": "#FFFFFF", "bg_color": "#C0392B", "border": 1})
    f_b = wb.add_format({"bold": True})
    registro = []

    def hoja(nombre):
        ws = wb.add_worksheet(nombre)
        ws.hide_gridlines(2)
        return ws

    def F(ws, celda, formula, fmt):
        ws.write_formula(celda, formula, fmt, vals.get((ws.get_name(), celda), 0))
        registro.append((ws.get_name(), celda))

    def OK(ws, celda, formula):
        F(ws, celda, formula, f_ok)
        ws.conditional_format(celda, {"type": "cell", "criteria": "==", "value": '"ERROR"', "format": f_bad})

    # ---------------------------------------------------------------- Parametros
    P = hoja("Parametros")
    P.set_column("A:A", 46); P.set_column("B:B", 14); P.set_column("C:C", 22); P.set_column("D:D", 22); P.set_column("E:E", 58)
    P.write("A1", "Parámetros de la escala de tallas", f_t)
    P.write("A2", "Azul = dato de entrada · gris violeta = fórmula. Fuente de las horas: informe de septiembre de 2026 (Viva Aerobus), hoja «Seguimiento Mes».", f_note)
    for c, t in zip("ABC", ("Parámetro", "Valor", "Fundamento")):
        P.write(f"{c}3", t, f_h)
    P.write("A4", "Margen de desviación", f_n); P.write("B4", MARGEN, f_pi); P.write("C4", "Regla: tiempo real + 30 %", f_n)
    P.write("A5", "Horas de trabajo de una característica XL", f_n); P.write("B5", HORAS_XL, f_i); P.write("C5", "Tope por característica", f_n)
    P.write("A6", "Tope de una característica (h con margen)", f_n); F(P, "B6", "=B5*(1+B4)", f_c); P.write("C6", "30 h + 30 % = 39 h", f_n)
    P.write("A7", "Puntos por persona al mes", f_n); F(P, "B7", f"=Septiembre!B10/B8", f_c)
    P.write("C7", "Puntos de septiembre (tareas terminadas) / personas", f_n)
    P.write("A8", "Personas del equipo de referencia", f_n); P.write("B8", PERSONAS_REF, f_i); P.write("C8", "Informe de septiembre", f_n)
    P.write("A9", "Jornada semanal por persona (h)", f_n); P.write("B9", JORNADA_SEM, f_i); P.write("C9", "Lunes a viernes", f_n)
    P.write("A10", "Semanas por mes", f_n); P.write("B10", SEMANAS, f_i); P.write("C10", "42 x 4", f_n)
    P.write("A11", "Horas disponibles por persona al mes", f_n); F(P, "B11", "=B9*B10", f_c)
    P.set_column("F:G", 16)
    for c, t in zip("ABCDEFG", ("Talla", "Puntos", "Tope (h con margen)", "Tope (h de trabajo)", "Qué es",
                                "Desde (h de trabajo)", "Punto medio (h de trabajo)")):
        P.write(f"{c}14", t, f_h)
    P.set_row(13, 30)
    for i, t in enumerate(TALLAS):
        r = 15 + i
        P.write(f"A{r}", t, f_n); P.write(f"B{r}", PUNTOS[t], f_i)
        if t == "XL":
            F(P, f"C{r}", "=B6", f_c)
        else:
            P.write(f"C{r}", TOPES[t], f_i)
        F(P, f"D{r}", f"=C{r}/(1+$B$4)", f_d)
        P.write(f"E{r}", DESC[t], f_n)
        if i == 0:
            P.write(f"F{r}", 0, f_i)
        else:
            F(P, f"F{r}", f"=D{r - 1}", f_d)
        F(P, f"G{r}", f"=(F{r}+D{r})/2", f_d)
    P.write("A22", "Punto medio = esfuerzo típico de una característica de esa talla; sirve para comprobar que las mezclas piden un esfuerzo parecido al del plan.", f_note)
    P.write("A21", "Una característica que pasa de XL se divide: bloques XL completos de 39 h (30 h de trabajo) más el resto con la talla que lo cubre.", f_note)
    CAPS, PTS = "Parametros!$C$15:$C$19", "Parametros!$B$15:$B$19"
    PT = {t: f"Parametros!$B${15 + i}" for i, t in enumerate(TALLAS)}   # puntos de cada talla
    HMED = {t: f"Parametros!$G${15 + i}" for i, t in enumerate(TALLAS)}  # horas de trabajo, punto medio
    HTOP = {t: f"Parametros!$D${15 + i}" for i, t in enumerate(TALLAS)}  # horas de trabajo, tope

    # ---------------------------------------------------------------- Tareas
    T = hoja("Tareas")
    T.set_column("A:A", 11); T.set_column("B:B", 30); T.set_column("C:F", 12); T.set_column("G:AB", 9.5)
    T.write("A1", "Conversión de horas a tallas, tarea por tarea", f_t)
    T.write("A2", "Completa = horas totales de la tarea (H + I del informe), es el tamaño de la característica. Septiembre = solo las horas del mes (columna I), es la capacidad que el equipo dedicó.", f_note)
    enc = ["Tarea", "Estado", "Integrante", "Grupo", "Horas completas (H+I)", "Horas septiembre (I)",
           "Completa: h con margen", "bloques XL", "resto (h)", "talla del resto", "PUNTOS completa",
           "Sept.: h con margen", "bloques XL", "resto (h)", "talla del resto", "PUNTOS sept.",
           "XL", "L", "M", "S", "XS", "Control sept.", "XL", "L", "M", "S", "XS", "Control compl."]
    for j, t in enumerate(enc):
        T.write(3, j, t, f_h)
    T.set_row(3, 42)
    T.write("Q3", "Septiembre: cantidad por talla", f_b); T.write("W3", "Completa: cantidad por talla", f_b)
    R0 = 5
    n = len(m["tareas"])
    R1 = R0 + n - 1
    IDX = {"XS": 1, "S": 2, "M": 3, "L": 4, "XL": 5}
    for i, t in enumerate(m["tareas"]):
        r = R0 + i
        T.write(f"A{r}", t["id"], f_n); T.write(f"B{r}", t["estado"], f_n); T.write(f"C{r}", t["integrante"], f_n)
        T.write(f"D{r}", t["grupo"], f_n); T.write(f"E{r}", t["h_completa"], f_i); T.write(f"F{r}", t["h_sept"], f_i)
        for (a, b, c_, d_, e_, h) in (("G", "H", "I", "J", "K", "E"), ("L", "M", "N", "O", "P", "F")):
            F(T, f"{a}{r}", f"=ROUND({h}{r}*(1+Parametros!$B$4),6)", f_c)
            F(T, f"{b}{r}", f"=INT({a}{r}/Parametros!$B$6)", f_c)
            F(T, f"{c_}{r}", f"=ROUND({a}{r}-{b}{r}*Parametros!$B$6,6)", f_c)
            F(T, f"{d_}{r}", f'=IF({c_}{r}>0,COUNTIF({CAPS},"<"&{c_}{r})+1,0)', f_c)
            F(T, f"{e_}{r}", f"={b}{r}*{PT['XL']}+IF({d_}{r}>0,INDEX({PTS},{d_}{r}),0)", f_cb)
        for cols, b, d_, e_, ctl in ((("Q", "R", "S", "T", "U"), "M", "O", "P", "V"), (("W", "X", "Y", "Z", "AA"), "H", "J", "K", "AB")):
            for col, tt in zip(cols, ("XL", "L", "M", "S", "XS")):
                extra = f"{b}{r}+" if tt == "XL" else ""
                F(T, f"{col}{r}", f"={extra}IF({d_}{r}={IDX[tt]},1,0)", f_c)
            suma = "+".join(f"{col}{r}*{PT[tt]}" for col, tt in zip(cols, ("XL", "L", "M", "S", "XS")))
            OK(T, f"{ctl}{r}", f'=IF({suma}={e_}{r},"OK","ERROR")')
    rng = lambda col: f"Tareas!${col}${R0}:${col}${R1}"
    GR, IN = rng("D"), rng("C")

    # ---------------------------------------------------------------- Septiembre
    S = hoja("Septiembre")
    S.set_column("A:A", 58); S.set_column("B:F", 16)
    S.write("A1", "Septiembre de 2026 en tallas: la base del plan Inicial", f_t)
    S.write("A2", "Equipo de referencia: Generic API (Viva Aerobus). Tareas terminadas = «Finalizada»/«Finalizado» o «Ready for prod» en el informe, solo horas del equipo.", f_note)
    S.write("A3", "Cifra", f_h); S.write("B3", "Valor", f_h)
    filas = [
        ("Tareas terminadas", f'=COUNTIF({GR},"Terminada")'),
        ("Horas completas de las terminadas (H+I)", f'=SUMIFS({rng("E")},{GR},"Terminada")'),
        ("Horas de septiembre de las terminadas (I)", f'=SUMIFS({rng("F")},{GR},"Terminada")'),
        ("Horas de septiembre de otras tareas (en curso, feedback, pausadas)", f'=SUMIFS({rng("F")},{GR},"Otra")'),
        ("Horas totales reportadas en septiembre", "=B6+B7"),
        ("Puntos, valor completo de las terminadas", f'=SUMIFS({rng("K")},{GR},"Terminada")'),
        ("Puntos de septiembre de las terminadas = base del plan Inicial", f'=SUMIFS({rng("P")},{GR},"Terminada")'),
        ("Puntos de septiembre de otras tareas", f'=SUMIFS({rng("P")},{GR},"Otra")'),
        ("Capacidad real del mes (puntos de todas las horas)", "=B10+B11"),
        ("Horas de trabajo por punto (terminadas)", "=B6/B10"),
        ("Control: capacidad real x 3 de 4 semanas", "=B12*3/4"),
        ("Diferencia contra la base del plan (117 - control)", "=B10-B14"),
    ]
    for i, (t, f) in enumerate(filas):
        r = 4 + i
        S.write(f"A{r}", t, f_n)
        F(S, f"B{r}", f, f_d if i in (9, 10, 11) else f_c)
    # B4 tareas, B5 h completas, B6 h sept term, B7 h sept otras, B8 h total, B9 pts completa, B10 pts sept, B11 pts otras, B12 capacidad real, B13 h/pto, B14 control, B15 dif
    S.write("A18", "Talla", f_h); S.write("B18", "Puntos", f_h); S.write("C18", "Cantidad en septiembre", f_h)
    S.write("D18", "Puntos", f_h); S.write("E18", "% de los puntos", f_h)
    for i, t in enumerate(ORDEN):
        r = 19 + i
        S.write(f"A{r}", t, f_n); F(S, f"B{r}", f"={PT[t]}", f_c)
        col = {"XL": "Q", "L": "R", "M": "S", "S": "T", "XS": "U"}[t]
        F(S, f"C{r}", f'=SUMIFS({rng(col)},{GR},"Terminada")', f_c)
        F(S, f"D{r}", f"=B{r}*C{r}", f_c)
        F(S, f"E{r}", f"=D{r}/$D$24", f_p)
    S.write("A24", "Total", f_b); F(S, "C24", "=SUM(C19:C23)", f_cb); F(S, "D24", "=SUM(D19:D23)", f_cb); F(S, "E24", "=SUM(E19:E23)", f_p)
    S.write("A25", "Control: puntos por talla = puntos de septiembre de las terminadas", f_n); OK(S, "B25", '=IF(D24=B10,"OK","ERROR")')
    S.write("A28", "Por integrante (anónimo)", f_h)
    for c, t in zip("BCDE", ("Terminadas", "Otras", "Total puntos", "Horas sept.")):
        S.write(f"{c}28", t, f_h)
    for i in (1, 2, 3):
        r = 28 + i
        S.write(f"A{r}", f"Integrante {i}", f_n)
        F(S, f"B{r}", f'=SUMIFS({rng("P")},{IN},{i},{GR},"Terminada")', f_c)
        F(S, f"C{r}", f'=SUMIFS({rng("P")},{IN},{i},{GR},"Otra")', f_c)
        F(S, f"D{r}", f"=B{r}+C{r}", f_cb)
        F(S, f"E{r}", f'=SUMIFS({rng("F")},{IN},{i})', f_c)
    S.write("A32", "Total", f_b)
    for c in "BCDE":
        F(S, f"{c}32", f"=SUM({c}29:{c}31)", f_cb)
    S.write("A33", "El reparto real fue desigual en las tareas terminadas; con todo el esfuerzo del mes quedó parejo. El plan reparte 39 puntos por persona como objetivo.", f_note)

    # ---------------------------------------------------------------- Planes
    L = hoja("Planes")
    L.set_column("A:A", 30); L.set_column("B:J", 14)
    L.write("A1", "Capacidad de cada plan", f_t)
    L.write("A2", "Plan = personas x puntos por persona. Se sube o baja de plan sumando o quitando una persona.", f_note)
    for c, t in zip("ABCD", ("Plan", "Personas", "Puntos por persona", "Capacidad (pts)")):
        L.write(f"{c}3", t, f_h)
    for i, (nombre, np_) in enumerate(PLANES):
        r = 4 + i
        L.write(f"A{r}", nombre, f_n); L.write(f"B{r}", np_, f_i)
        F(L, f"C{r}", "=Parametros!$B$7", f_c); F(L, f"D{r}", f"=B{r}*C{r}", f_cb)
    L.write("A8", "Máximo de características si todo el mes fuera de una sola talla", f_b)
    for j, t in enumerate(TALLAS):
        L.write(8, 1 + j, t, f_h)
    L.write("A9", "Plan", f_h)
    for i, (nombre, _) in enumerate(PLANES):
        r = 10 + i
        L.write(f"A{r}", nombre, f_n)
        for j, t in enumerate(TALLAS):
            col = xl_col_to_name(1 + j)
            F(L, f"{col}{r}", f"=INT($D{4 + i}/{PT[t]})", f_cb)
    L.write("A14", "Puntos que ocupa ese máximo", f_b); L.write("A15", "Plan", f_h)
    for j, t in enumerate(TALLAS):
        L.write(14, 1 + j, t, f_h)
    for i, (nombre, _) in enumerate(PLANES):
        r = 16 + i
        L.write(f"A{r}", nombre, f_n)
        for j, t in enumerate(TALLAS):
            col = xl_col_to_name(1 + j)
            F(L, f"{col}{r}", f"={col}{10 + i}*{PT[t]}", f_c)
    L.write("A20", "Puntos que sobran (la capacidad no divide exacto)", f_b); L.write("A21", "Plan", f_h)
    for j, t in enumerate(TALLAS):
        L.write(20, 1 + j, t, f_h)
    for i, (nombre, _) in enumerate(PLANES):
        r = 22 + i
        L.write(f"A{r}", nombre, f_n)
        for j, t in enumerate(TALLAS):
            col = xl_col_to_name(1 + j)
            F(L, f"{col}{r}", f"=$D{4 + i}-{col}{16 + i}", f_c)
    L.write("A26", "Se dice «M» como referencia porque divide exacto en los tres planes.", f_note)
    L.write("A28", "Horas de trabajo equivalentes", f_b)
    for c, t in zip("ABCD", ("Plan", "Horas de trabajo del plan", "Horas disponibles", "% de la jornada")):
        L.write(f"{c}29", t, f_h)
    for i, (nombre, _) in enumerate(PLANES):
        r = 30 + i
        L.write(f"A{r}", nombre, f_n)
        F(L, f"B{r}", f"=D{4 + i}*Septiembre!$B$13", f_d)
        F(L, f"C{r}", f"=B{4 + i}*Parametros!$B$11", f_c)
        F(L, f"D{r}", f"=B{r}/C{r}", f_p)
    L.write("A34", "Horas del plan = puntos x horas por punto de septiembre (394 h / 117 pts). Cuadra con que solo cuenten 3 de las 4 semanas.", f_note)

    # ---------------------------------------------------------------- Mezclas
    Z = hoja("Mezclas")
    Z.set_column("A:A", 30); Z.set_column("B:K", 14)
    Z.write("A1", "Mezclas posibles por plan", f_t)
    Z.write("A2", "Cada mezcla (azul = entrada) debe sumar exactamente la capacidad del plan. Los % muestran qué parte de los puntos ocupa cada talla. "
                  "Horas: con el punto medio de cada talla, toda mezcla debe pedir un esfuerzo parecido al del plan (±5 %) y caber en el mes. "
                  "Las horas máximas son el caso extremo (todas en el tope de su talla): solo informativas.", f_note)
    Z.set_row(1, 45)
    base_mezcla = {}
    for v, mz in enumerate(m["mezclas"]):
        r0 = 4 + v * 20
        Z.write(f"A{r0}", f"{v + 1}. {mz['nombre']}: {mz['desc']}", f_b)
        for c, t in zip("ABCDEFGH", ("Talla", "Puntos", PLANES[0][0], PLANES[1][0], PLANES[2][0], "% pts " + PLANES[0][0], "% pts " + PLANES[1][0], "% pts " + PLANES[2][0])):
            Z.write(f"{c}{r0 + 1}", t, f_h)
        if v == 0:
            Z.write(f"I{r0 + 1}", "% pts septiembre", f_h)
        for k, t in enumerate(ORDEN):
            r = r0 + 2 + k
            Z.write(f"A{r}", t, f_n); F(Z, f"B{r}", f"={PT[t]}", f_c)
            for p in range(3):
                col = "CDE"[p]
                Z.write(f"{col}{r}", mz["planes"][p]["mezcla"][t], f_i)
                F(Z, f"{'FGH'[p]}{r}", f"={col}{r}*$B{r}/{col}${r0 + 9}", f_p)
            if v == 0:
                F(Z, f"I{r}", f"=Septiembre!E{19 + k}", f_p)
        a, b = r0 + 2, r0 + 6
        Z.write(f"A{r0 + 7}", "Total características", f_b)
        Z.write(f"A{r0 + 9}", "Total puntos", f_b)
        Z.write(f"A{r0 + 10}", "Capacidad del plan", f_n)
        Z.write(f"A{r0 + 11}", "¿Cuadra?", f_n)
        for p in range(3):
            col = "CDE"[p]
            F(Z, f"{col}{r0 + 7}", f"=SUM({col}{a}:{col}{b})", f_cb)
            F(Z, f"{col}{r0 + 9}", f"=SUMPRODUCT($B{a}:$B{b},{col}{a}:{col}{b})", f_cb)
            F(Z, f"{col}{r0 + 10}", f"=Planes!$D${4 + p}", f_c)
            OK(Z, f"{col}{r0 + 11}", f'=IF({col}{r0 + 9}={col}{r0 + 10},"OK","ERROR")')
            base_mezcla[(v, p)] = {t: f"Mezclas!${col}${r0 + 2 + k}" for k, t in enumerate(ORDEN)}
        base_mezcla[(v, "chk")] = [f"Mezclas!{c}{r0 + 11}" for c in "CDE"]
        for k, txt in enumerate(("Horas de trabajo estimadas (punto medio de cada talla)", "Horas máximas (todas en el tope de su talla)",
                                 "Horas equivalentes del plan (pts x h por punto de septiembre)", "Diferencia: estimadas vs equivalentes",
                                 "Horas disponibles del mes (personas x 168)", "¿Esfuerzo parecido (±5 %) y cabe en el mes?")):
            Z.write(f"A{r0 + 12 + k}", txt, f_n)
        for p in range(3):
            col = "CDE"[p]
            F(Z, f"{col}{r0 + 12}", "=" + "+".join(f"{col}{r0 + 2 + k}*{HMED[t]}" for k, t in enumerate(ORDEN)), f_d)
            F(Z, f"{col}{r0 + 13}", "=" + "+".join(f"{col}{r0 + 2 + k}*{HTOP[t]}" for k, t in enumerate(ORDEN)), f_d)
            F(Z, f"{col}{r0 + 14}", f"=Planes!$B${30 + p}", f_d)
            F(Z, f"{col}{r0 + 15}", f"={col}{r0 + 12}/{col}{r0 + 14}-1", f_p)
            F(Z, f"{col}{r0 + 16}", f"=Planes!$C${30 + p}", f_c)
            OK(Z, f"{col}{r0 + 17}", f'=IF(AND(ABS({col}{r0 + 15})<=0.05,{col}{r0 + 12}<={col}{r0 + 16}),"OK","ERROR")')
        base_mezcla[(v, "horas")] = [f"Mezclas!{c}{r0 + 17}" for c in "CDE"]

    # ---------------------------------------------------------------- Equipo
    E = hoja("Equipo")
    E.set_column("A:A", 34); E.set_column("B:H", 12); E.set_column("I:K", 16)
    E.write("A1", "Cómo toma cada persona su parte de la mezcla", f_t)
    E.write("A2", "Cada persona toma exactamente los puntos por persona (39). La suma del equipo debe ser igual a la mezcla. "
                  "Horas estimadas = punto medio de cada talla; deben caber en el mes de la persona (42 h x 4).", f_note)
    r = 4
    chk_equipo, chk_horas = [], []
    for v, mz in enumerate(m["mezclas"]):
        for p, (pn, np_) in enumerate(PLANES):
            blk = mz["planes"][p]
            E.write(f"A{r}", f"{v + 1}. {mz['nombre']} · {pn} ({np_} personas)", f_b)
            for c, t in zip("ABCDEFGHIJK", ("Integrante", *ORDEN, "Puntos", "¿Cuadra?", "Horas estimadas", "Horas máximas", "¿Cabe en el mes?")):
                E.write(f"{c}{r + 1}", t, f_h)
            a = r + 2
            for i, per in enumerate(blk["equipo"]):
                rr = a + i
                E.write(f"A{rr}", f"Persona {i + 1}", f_n)
                for c, t in zip("BCDEF", ORDEN):
                    E.write(f"{c}{rr}", per[t], f_i)
                F(E, f"G{rr}", "=" + "+".join(f"{c}{rr}*{PT[t]}" for c, t in zip("BCDEF", ORDEN)), f_cb)
                OK(E, f"H{rr}", f'=IF(G{rr}=Parametros!$B$7,"OK","ERROR")')
                chk_equipo.append(f"Equipo!H{rr}")
                F(E, f"I{rr}", "=" + "+".join(f"{c}{rr}*{HMED[t]}" for c, t in zip("BCDEF", ORDEN)), f_d)
                F(E, f"J{rr}", "=" + "+".join(f"{c}{rr}*{HTOP[t]}" for c, t in zip("BCDEF", ORDEN)), f_d)
                OK(E, f"K{rr}", f'=IF(I{rr}<=Parametros!$B$11,"OK","ERROR")')
                chk_horas.append(f"Equipo!K{rr}")
            b = a + np_ - 1
            E.write(f"A{b + 1}", "Suma del equipo", f_b)
            E.write(f"A{b + 2}", "Mezcla (hoja Mezclas)", f_n)
            E.write(f"A{b + 3}", "¿Cuadra?", f_n)
            for c, t in zip("BCDEF", ORDEN):
                F(E, f"{c}{b + 1}", f"=SUM({c}{a}:{c}{b})", f_cb)
                F(E, f"{c}{b + 2}", f"={base_mezcla[(v, p)][t]}", f_c)
                OK(E, f"{c}{b + 3}", f'=IF({c}{b + 1}={c}{b + 2},"OK","ERROR")')
                chk_equipo.append(f"Equipo!{c}{b + 3}")
            F(E, f"G{b + 1}", "=" + "+".join(f"{c}{b + 1}*{PT[t]}" for c, t in zip("BCDEF", ORDEN)), f_cb)
            F(E, f"G{b + 2}", f"=Planes!$D${4 + p}", f_c)
            OK(E, f"G{b + 3}", f'=IF(G{b + 1}=G{b + 2},"OK","ERROR")')
            chk_equipo.append(f"Equipo!G{b + 3}")
            r = b + 5

    # ---------------------------------------------------------------- Verificacion
    V = hoja("Verificacion")
    V.set_column("A:A", 70); V.set_column("B:C", 18); V.set_column("D:D", 12)
    V.write("A1", "Verificación de todos los cálculos", f_t)
    V.write("A2", "Esperado = valor del informe de septiembre de 2026 o de la regla acordada. Todo debe decir OK.", f_note)
    for c, t in zip("ABCD", ("Control", "Calculado", "Esperado", "¿Cuadra?")):
        V.write(f"{c}3", t, f_h)
    ctrl = [
        ("Tareas terminadas del equipo", "=Septiembre!B4", 19),
        ("Horas completas de las terminadas", "=Septiembre!B5", 564),
        ("Horas de septiembre de las terminadas", "=Septiembre!B6", 394),
        ("Horas de septiembre de otras tareas", "=Septiembre!B7", 130),
        ("Horas totales reportadas en septiembre", "=Septiembre!B8", 524),
        ("Puntos, valor completo de las terminadas", "=Septiembre!B9", 164),
        ("Puntos de septiembre de las terminadas", "=Septiembre!B10", 117),
        ("Capacidad real del mes (puntos)", "=Septiembre!B12", 153),
        ("Puntos por persona", "=Parametros!B7", 39),
        ("Capacidad Inicial", "=Planes!D4", 117),
        ("Capacidad Profesional", "=Planes!D5", 156),
        ("Capacidad Alta velocidad", "=Planes!D6", 195),
        ("Características de septiembre por talla: XL", "=Septiembre!C19", 10),
        ("Características de septiembre por talla: L", "=Septiembre!C20", 4),
        ("Características de septiembre por talla: M", "=Septiembre!C21", 1),
        ("Características de septiembre por talla: S", "=Septiembre!C22", 5),
        ("Características de septiembre por talla: XS", "=Septiembre!C23", 4),
    ]
    r = 4
    todos = []
    for t, f, esp in ctrl:
        V.write(f"A{r}", t, f_n); F(V, f"B{r}", f, f_c); V.write(f"C{r}", esp, f_i)
        OK(V, f"D{r}", f'=IF(B{r}=C{r},"OK","ERROR")'); todos.append(f"D{r}"); r += 1
    extra = [
        ("Controles de cada tarea (sept. y completa): 26 tareas x 2", f'=COUNTIF(Tareas!V{R0}:V{R1},"OK")+COUNTIF(Tareas!AB{R0}:AB{R1},"OK")', 2 * n),
        ("Mezclas que llenan su plan (3 mezclas x 3 planes)", "=" + "+".join(f'COUNTIF({c},"OK")' for v in range(3) for c in base_mezcla[(v, "chk")]), 9),
        ("Controles del reparto por persona y por talla", "=" + "+".join(f'COUNTIF({c},"OK")' for c in chk_equipo), len(chk_equipo)),
        ("Mezclas con esfuerzo parecido al del plan (±5 %) que caben en el mes", "=" + "+".join(f'COUNTIF({c},"OK")' for v in range(3) for c in base_mezcla[(v, "horas")]), 9),
        ("Personas cuyo esfuerzo estimado cabe en su mes (42 h x 4)", "=" + "+".join(f'COUNTIF({c},"OK")' for c in chk_horas), len(chk_horas)),
    ]
    for t, f, esp in extra:
        V.write(f"A{r}", t, f_n); F(V, f"B{r}", f, f_c); V.write(f"C{r}", esp, f_i)
        OK(V, f"D{r}", f'=IF(B{r}=C{r},"OK","ERROR")'); todos.append(f"D{r}"); r += 1
    V.write(f"A{r + 1}", "RESULTADO GENERAL", f_b)
    OK(V, f"D{r + 1}", f'=IF(COUNTIF(D4:D{r - 1},"OK")={len(todos)},"OK","ERROR")')
    V.activate()
    wb.close()
    return registro


# --------------------------------------------------------------------------- evaluación con `formulas`
def evaluar(ruta, registro):
    import formulas
    xl = formulas.ExcelModel().loads(ruta).finish()
    sol = xl.calculate()
    libro = os.path.basename(ruta)
    out = {}
    for hoja_, celda in registro:
        clave = f"'[{libro}]{hoja_.upper()}'!{celda}"
        v = sol[clave].value[0, 0]
        if hasattr(v, "item"):
            v = v.item()
        out[(hoja_, celda)] = v
    return out


def main():
    m = completar(modelo())
    tmp = XLSX + ".tmp.xlsx"
    reg = construir(tmp, m)
    vals = evaluar(tmp, reg)
    os.remove(tmp)
    reg = construir(XLSX, m, vals)
    # El Excel (evaluado) debe dar lo mismo que el modelo en Python
    chk = {
        ("Septiembre", "B4"): 19, ("Septiembre", "B5"): m["horas"]["completa_terminadas"], ("Septiembre", "B6"): m["horas"]["sept_terminadas"],
        ("Septiembre", "B7"): m["horas"]["sept_otras"], ("Septiembre", "B8"): m["horas"]["sept_total"], ("Septiembre", "B9"): m["pts_completa_terminadas"],
        ("Septiembre", "B10"): m["pts_sept_terminadas"], ("Septiembre", "B11"): m["pts_sept_otras"], ("Septiembre", "B12"): m["capacidad_real"],
        ("Parametros", "B7"): m["pts_por_persona"], ("Planes", "D4"): m["planes"][0]["capacidad"], ("Planes", "D6"): m["planes"][2]["capacidad"],
    }
    for k, esperado in chk.items():
        assert abs(vals[k] - esperado) < 1e-9, (k, vals[k], esperado)
    for i, t in enumerate(m["tareas"]):
        r = 5 + i
        assert vals[("Tareas", f"K{r}")] == t["pts_completa"] and vals[("Tareas", f"P{r}")] == t["pts_sept"], t["id"]
    for t in ORDEN:
        assert vals[("Septiembre", f"C{19 + ORDEN.index(t)}")] == m["sept_por_talla"][t]
    for v, mz in enumerate(m["mezclas"]):
        for p, blk in enumerate(mz["planes"]):
            celda = ("Mezclas", f"{'CDE'[p]}{4 + v * 20 + 12}")
            assert abs(vals[celda] - blk["horas"]["medio"]) < 1e-6, (celda, vals[celda], blk["horas"]["medio"])
    errores = [k for k, v in vals.items() if v == "ERROR"]
    assert not errores, errores
    assert vals[[k for k in vals if k[0] == "Verificacion"][-1]] == "OK"
    with open(os.path.join(AQUI, "datos.json"), "w") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=1)
    print("OK · Excel evaluado = modelo Python;", len(reg), "fórmulas;", XLSX)


if __name__ == "__main__":
    main()
