#!/usr/bin/env python3
"""Audita la presentación SURA contra datos.json: cifras, orden de las láminas y términos prohibidos ante el cliente.

Uso: python3 auditar_deck.py   (sale con error si algo no cuadra)
"""
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(AQUI, "..", "tech-and-solve-propuesta-paquetes-de-actividades.html")
m = json.load(open(os.path.join(AQUI, "datos.json")))
P = {"XL": 8, "L": 5, "M": 3, "S": 2, "XS": 1}
t = open(HTML).read()
sl = re.findall(r'<section class="slide">.*?</section>', t, flags=re.S)
pts = lambda s: sum(int(n) * P[k] for n, k in re.findall(r"(\d+) (XL|L|M|S|XS)\b", s))
cuenta = lambda s: {k: int(n) for n, k in re.findall(r"(\d+) (XL|L|M|S|XS)\b", s)}
caps = [p["capacidad"] for p in m["planes"]]
ok = []


def lamina(titulo):
    r = [s for s in sl if titulo in s]
    assert len(r) == 1, titulo
    return r[0]


# 1. Orden: las internas van al final y son tres
internas = [i for i, s in enumerate(sl) if "USO INTERNO" in s]
assert internas == list(range(len(sl) - len(internas), len(sl))) and len(internas) == 3, internas
ok.append(f"{len(sl)} láminas: {len(sl) - 3} para el cliente y las 3 internas al final")

# 2. Ante el cliente: sin Viva, sin puntos, sin nombres, sin «actividad», sin archivos internos
cli = re.sub(r"<[^>]+>", " ", re.sub(r"data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+", "", "".join(sl[:internas[0]])))
for w in ("Viva", "Generic API", "punto", "pts", "Daniel", "Luis", "Gabriel", "LLMCoder", "IA ", "Ready for prod", "ctividad", "paquete", "xlsx"):
    assert w not in cli, w
ok.append("láminas del cliente sin Viva, puntos, nombres, «actividad», «paquete» ni archivos internos")

# 3. Capacidad por talla = INT(capacidad / puntos de la talla)
s4 = lamina("Cuántas características de cada talla")
nums = list(map(int, re.findall(r'font-size:1\.719cqw;font-weight:700;color:var\(--blue-accent\)">(\d+)<', s4)))
assert nums == [caps[i % 3] // [1, 2, 3, 5, 8][i // 3] for i in range(15)], nums
perfil = re.search(r'margin-top:0\.156cqw">([^<]+)</div>', s4).group(1)
assert cuenta(perfil) == {k: v for k, v in m["sept_por_talla"].items() if v} and pts(perfil) == caps[0]
ok.append("capacidad por talla (15 cifras) y perfil de septiembre = 117 pts")

# 4. Mezclas: cada una llena su plan y coincide con datos.json
s5 = lamina("Cada plan se puede llenar con")
ms = [x.strip() for x in re.findall(r'<div style="font-size:1\.250cqw;font-weight:700;line-height:1\.2">([^<]+)</div>', s5)]
assert [pts(x) for x in ms] == caps * 3
assert [cuenta(x) for x in ms] == [{k: v for k, v in p["mezcla"].items() if v} for mz in m["mezclas"] for p in mz["planes"]]
assert ms[0] == perfil
act = list(map(int, re.findall(r">(\d+) características en el mes<", s5)))
assert act == [sum(cuenta(x).values()) for x in ms]
ok.append("9 mezclas = capacidad de su plan; la primera de Inicial = perfil de la lámina 4")

# 5. Reparto: cada persona 39; la suma del equipo = la mezcla; personas = 3 + 4 + 5 por mezcla
s_eq = lamina("Cómo se reparte cada mezcla")
filas = re.findall(r"<tr>(.*?)</tr>", s_eq, flags=re.S)[1:]
n_pers = 0
for fi, f in enumerate(filas):
    for ci, c in enumerate(re.findall(r'<td style="[^"]*vertical-align:top">(.*?)</td>', f, flags=re.S)[1:]):
        tot = {}
        pers = 0
        for n, mix in re.findall(r">(\d+) personas?</span><span[^>]*>([^<]+)</span>", c):
            assert pts(mix) == m["pts_por_persona"], mix
            pers += int(n)
            for k, q in cuenta(mix).items():
                tot[k] = tot.get(k, 0) + int(n) * q
        assert pers == m["planes"][ci]["personas"] and tot == cuenta(ms[fi * 3 + ci]), (fi, ci)
        n_pers += pers
assert n_pers == 36
ok.append("reparto: 36 personas con 39 pts y cada equipo suma su mezcla")

# 6. Septiembre: tallas por tarea suman 117 y el conteo por talla
s9 = lamina("Tallas de referencia")
tot, cnt = 0, {k: 0 for k in P}
for f in re.findall(r"<tr>(.*?)</tr>", s9, flags=re.S):
    tds = re.findall(r"<td[^>]*>(.*?)</td>", f, flags=re.S)
    if len(tds) == 4 and tds[0].startswith("<b>API"):
        talla, p_ = re.findall(r"<b[^>]*>([^<]+)</b>", tds[3])[-1].split(" · ")
        ks = [x.strip() for x in talla.split("+")]
        assert sum(P[k] for k in ks) == int(p_.split()[0])
        tot += int(p_.split()[0])
        for k in ks:
            cnt[k] += 1
assert tot == m["pts_sept_terminadas"] and cnt == m["sept_por_talla"], (tot, cnt)
ok.append("septiembre: 19 tareas = 117 pts = 10 XL + 4 L + 1 M + 5 S + 4 XS")

# 7. Plan Inicial: equivalencias en M y horas
s10 = lamina("El plan Inicial es de")
eqs = re.findall(r"= (\d+) características M \(exacto\) · ≈ (\d+) h de trabajo", s10)
assert [(int(a), int(b)) for a, b in eqs] == [(c // 3, round(c * m["horas_por_punto"])) for c in caps], eqs
for s in (s9, s10):
    assert "pueden variar según el tipo de proyecto" in s
ok.append("plan Inicial: 39 / 52 / 65 M y 394 / 525 / 657 h; aviso de datos de referencia en ambas internas")

print("\n".join("OK · " + x for x in ok))
