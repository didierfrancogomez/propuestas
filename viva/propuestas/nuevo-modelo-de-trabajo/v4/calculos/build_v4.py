#!/usr/bin/env python3
"""Genera la propuesta v4 (paquetes de puntos de Generic API) a partir de las fuentes.

Fuentes de lectura (no se modifican):
  - Informe de seguimiento de septiembre de 2026 (xlsx), hoja «Seguimiento Mes».
  - Informe de seguimiento de agosto de 2026 (xlsx), solo para la comparación de acierto.
  - evidencia.json (junto a este script): datos de Jira y GitHub leídos el 9 oct 2026 en modo lectura.

Reglas (propuestas/viva/propuestas/nuevo-modelo-de-trabajo/CLAUDE.md):
  - El tallaje usa solo el tiempo real invertido para completar una actividad (H + I) + 30 % de desviación.
  - Solo cuentan actividades finalizadas del equipo.
  - Todo dato previo lleva su evidencia citable.
"""
import os, re, html, math, json, collections, datetime, statistics as st
import openpyxl
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
RES = "/Users/didierfranco/Documents/GitHub/techandsolve/viva/generic-api/evolucion-generic-api/evidencias/resources/"
XLSX9 = RES + "09 Viva Aerobus Seguimiento Tech and Solve - Informe Septiembre2026.xlsx"
XLSX8 = RES + "08 Viva Aerobus Seguimiento Tech and Solve - Informe Agosto2026 (1).xlsx"
EV = json.load(open(os.path.join(HERE, "evidencia.json")))
OUT = os.environ.get("V4_OUT", os.path.join(HERE, "..", "tech-and-solve-propuesta-paquetes-de-actividades.html"))
TEMPLATE = os.path.expanduser("~/.claude/skills/tech-and-solve-proposal/assets/template.html")

JIRA = "https://vivaaerobus.atlassian.net/browse/"
GH = "https://github.com/EzyWebwerkstaden/VivaAerobus.Generic.Api/pull/"
DONE = {"Finalizado", "Finalizada", "Ready for prod"}   # terminada por el equipo: Ready for prod (listo para producción) o Done; el informe escribe Done de dos formas
TEAM3 = {"Luis Galindo", "Daniel Llano", "Gabriel Herrera"}
MARGEN = D("1.3")                            # tiempo real + 30 % de desviación por defecto
LIM = [6, 11, 17, 28, 46, 74, 90]            # topes de cada rango, en horas con margen
PTS = [1, 2, 3, 5, 8, 13, 21]
NO_ENTREGA = re.compile(r"^(acompa[ñn]amiento|onboarding|daily meetings|instalaci)", re.I)


# ---------------------------------------------------------------- utilidades
def load(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)      # solo lectura
    rows = []
    for i, r in enumerate(wb["Seguimiento Mes"].iter_rows(min_col=1, max_col=13, values_only=True), 1):
        if i == 1 or not r[1]:
            continue
        rows.append(dict(row=i, dev=r[0], id=r[1], s=r[2], st=r[3], fin=r[4], ent=r[5], G=r[6],
                         H=r[7] or 0, I=r[8] or 0, J=r[9], devol=r[10], tipo=r[11], obs=r[12]))
    return rows


def size(a):
    for l, p in zip(LIM, PTS):
        if a <= l:
            return p
    return "D"


def pts_split(a):
    z = size(a)
    if z != "D":
        return z
    n = math.ceil(a / LIM[-1])
    return n * size(a / n)


def fmt(x, dec=1):
    x = float(x)
    s = f"{x:,.{dec}f}".replace(",", "_")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("_", ".")


def esc(s):
    return html.escape(str(s), quote=False)


def num_(k):
    m = re.search(r"(\d+)", k)
    return int(m.group(1)) if m else 0


def tk(k):      # enlace a un ticket de Jira
    return f'<a href="{JIRA}{k}">{k}</a>'


def pr(n):      # enlace a un PR de GitHub
    return f'<a href="{GH}{n}">#{n}</a>'


def fs(*ids):   # chips de fuente enlazados a la tabla de fuentes
    return " ".join(f'<a href="#{i.lower()}">{i}</a>' if i.startswith("F") else i for i in ids)


MES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MES3 = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def fdate(d):
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def fiso(s):    # '2026-09-03' -> '03 sep'
    y, m, d = s.split("-")
    return f"{int(d):02d}&nbsp;{MES3[int(m)]}"


# ---------------------------------------------------------------- actividades del equipo
rows9 = load(XLSX9)
rows8 = load(XLSX8)
by = collections.OrderedDict()
for r in rows9:
    if str(r["id"]).startswith("API-"):
        by.setdefault(r["id"], []).append(r)

use = collections.OrderedDict()
excluidas = {}
for k, rs in by.items():
    if not any(r["st"] in DONE for r in rs):
        continue
    names = set(r["dev"] for r in rs)
    if not names & TEAM3:
        continue                                              # no es del equipo
    if k == "API-1860":
        excluidas[k] = "la implementó un revisor"             # PR #2500 y etiqueta del ticket
        continue
    if NO_ENTREGA.match(str(rs[0]["s"])):
        excluidas[k] = "no es una entrega con PR"
        continue
    h = sum(D(str(r["H"])) + D(str(r["I"])) for r in rs)
    if h <= 0:
        excluidas[k] = "sin horas registradas"
        continue
    fe = [r["fin"] for r in rs if r["st"] in DONE and isinstance(r["fin"], datetime.datetime)]
    src = "fin"
    if not fe:
        fe = [r["ent"] for r in rs if r["st"] in DONE and isinstance(r["ent"], datetime.datetime)]
        src = "entrega"
    use[k] = dict(s=rs[0]["s"], h=h, a=(h * MARGEN).quantize(D("0.0001")),
                  f=max(fe) if fe else None, fsrc=src if fe else None,
                  team=sorted(names & TEAM3), rows=rs)

# transiciones de estado de Jira de las 26 actividades de septiembre (solo lectura, 9 oct 2026)
TRJ = json.load(open(os.path.join(HERE, "transiciones_jira.json")))


def pj(x):
    return datetime.datetime.fromisoformat(x[:-2] + ":" + x[-2:])


def tr_info(k):
    tr = [(pj(t["fecha"]), t["de"], t["a"]) for t in TRJ[k]["transiciones"]]
    rfp = next((t for t, a, b in tr if a == "UAT" and b == "Ready for prod"), None)
    done = next((t for t, a, b in tr if a == "Ready for prod" and b == "Done"), None)
    return dict(rev=sum(1 for _, a, b in tr if a == "In review" and b in ("In Progress", "Feedback")),
                uat=sum(1 for _, a, b in tr if a in ("UAT", "UAT ON HOLD") and b in ("In Progress", "Feedback", "In review")),
                rfp=rfp, done=done, tr=tr)


TI = {k: tr_info(k) for k in TRJ}
for k, v in use.items():                     # fecha de término del equipo: pase a Ready for prod en Jira, cuando se leyó
    if k in TI and TI[k]["rfp"]:
        v["f"], v["fsrc"] = TI[k]["rfp"].replace(tzinfo=None), "jira"

N = len(use)
H = sum(v["h"] for v in use.values())
A = sum(v["a"] for v in use.values())
TOTP = sum(pts_split(v["a"]) for v in use.values())
HPP = float(A) / TOTP
KEYS = PTS + ["D"]
agg = {z: [0, D(0), D(0)] for z in KEYS}
for v in use.values():
    g = agg[size(v["a"])]
    g[0] += 1
    g[1] += v["h"]
    g[2] += v["a"]
nD = agg["D"][0]

# rangos de horas
rng = {}
prev = 0
for l, p in zip(LIM, PTS):
    rng[p] = f"hasta {l}&nbsp;h" if prev == 0 else f"más de {prev} y hasta {l}&nbsp;h"
    prev = l
rng["D"] = f"más de {LIM[-1]}&nbsp;h"

# serie mensual (septiembre 2025 a septiembre 2026)
mo = collections.defaultdict(lambda: [0, 0, set()])
sin_fecha = []
for k, v in use.items():
    if not v["f"]:
        sin_fecha.append(k)
        continue
    m = v["f"].strftime("%Y-%m")
    mo[m][0] += 1
    mo[m][1] += pts_split(v["a"])
    mo[m][2].update(v["team"])
months = [m for m in sorted(mo) if "2025-09" <= m <= "2026-09"]
assert len(months) == 13
solo1 = [m for m in months if len(mo[m][2]) == 1]
prim2 = next(m for m in months if len(mo[m][2]) >= 2)
prim3 = next(m for m in months if len(mo[m][2]) == 3)
def mtxt(m): return f"{MES[int(m[5:])]} de {m[:4]}"
vals = [mo[m][1] for m in months]
lo, hi, med = min(vals), max(vals), int(st.median(vals))
srt = sorted(vals, reverse=True)
n_fecha_entrega = sum(1 for v in use.values() if v["fsrc"] == "entrega")
n_jira = sum(1 for v in use.values() if v["fsrc"] == "jira")
pts_sin_fecha = sum(pts_split(use[k]["a"]) for k in sin_fecha)
# puntos por persona: los puntos de cada actividad se reparten según las horas (H + I) de cada integrante del equipo en ella
pp = collections.defaultdict(lambda: collections.defaultdict(float))
for k, v in use.items():
    if not v["f"]:
        continue
    m = v["f"].strftime("%Y-%m")
    rs_t = [r for r in v["rows"] if r["dev"] in TEAM3]
    tot = sum(float(D(str(r["H"])) + D(str(r["I"]))) for r in rs_t)
    for r in rs_t:
        pp[m][r["dev"]] += pts_split(v["a"]) * float(D(str(r["H"])) + D(str(r["I"]))) / tot
for m in months:
    assert abs(sum(pp[m].values()) - mo[m][1]) < 1e-6
m3 = [m for m in months if m >= prim3]
v3 = [x for m in m3 for x in pp[m].values()]                  # puntos de cada persona en cada mes con las tres activas
pp_prom, pp_min, pp_max = sum(v3) / len(v3), min(v3), max(v3)
PPP = int(pp_prom)                                       # puntos por persona al mes: parte entera del promedio observado
PERS = (3, 4, 5)                                         # paquetes por personas enteras; el primero es la operación actual
PK = tuple(n * PPP for n in PERS)
tot3 = [mo[m][1] for m in m3]                            # puntos del equipo en los meses con las tres personas
cnt3 = [sum(1 for x in tot3 if x >= p) for p in PK]
antes = {m: mo[m] for m in sorted(mo) if m < "2025-09"}

# ejemplo por tamaño: la actividad cuyo tiempo queda más cerca del centro de su rango
ex = {}
for z in PTS:
    i = PTS.index(z)
    mid = ((LIM[i - 1] if i else 0) + LIM[i]) / 2
    cands = [(k, v) for k, v in use.items() if size(v["a"]) == z and len(v["s"]) <= 80
             and not re.match(r"(investig|daily)", str(v["s"]), re.I)]
    k, v = min(cands, key=lambda kv: abs(float(kv[1]["a"]) - mid))
    ex[z] = (k, v)

# mezcla de ejemplo del paquete Inicial: proporción de tamaños de las actividades finalizadas
pieces = collections.Counter()
for v in use.values():
    z = size(v["a"])
    if z != "D":
        pieces[z] += 1
    else:
        n = math.ceil(float(v["a"]) / LIM[-1])
        pieces[size(float(v["a"]) / n)] += n
tp = sum(pieces.values())
avgp = TOTP / tp
exp = {z: pieces[z] * PK[0] / avgp / tp for z in PTS}
best = None


def search(i, left, cur):
    global best
    if i == len(PTS):
        if left == 0:
            d = sum((cur[z] - exp[z]) ** 2 for z in PTS)
            if best is None or d < best[0]:
                best = (d, dict(cur))
        return
    z = PTS[i]
    for n in range(0, left // z + 1):
        if n > round(exp[z]) + 2:
            break
        cur[z] = n
        search(i + 1, left - n * z, cur)
    cur.pop(z, None)


search(0, PK[0], {})
mix = best[1]
assert sum(k * v for k, v in mix.items()) == PK[0]
mixtxt = ", ".join(f"{v} de {k} {'punto' if k == 1 else 'puntos'} ({k * v})" for k, v in mix.items() if v)

# ---------------------------------------------------------------- cifras del informe (horas, acierto)
def mes_equipo(rows):
    rs = [r for r in rows if r["dev"] in TEAM3 and str(r["id"]).startswith("API-") and (r["I"] or 0) > 0]
    con = [r for r in rs if isinstance(r["G"], (int, float)) and r["G"] > 0]
    ok = [r for r in con if ((r["H"] + r["I"]) - r["G"]) / r["G"] <= 0.30 + 1e-9]
    return dict(act=len(rs), con=len(con), ok=len(ok), ej=sum(r["H"] + r["I"] for r in con),
                es=sum(r["G"] for r in con), horas_mes=sum(r["I"] for r in rs),
                devol=sum((r["devol"] or 0) for r in rs if isinstance(r["devol"], (int, float))),
                por_persona={d: sum(r["I"] for r in rs if r["dev"] == d) for d in sorted(TEAM3)})


S = mes_equipo(rows9)
G8 = mes_equipo(rows8)
assert (S["ok"], S["con"], S["act"]) == (18, 25, 26) and (G8["ok"], G8["con"]) == (4, 18)
horas_pp = " + ".join(fmt(S["por_persona"][d], 0) for d in ("Daniel Llano", "Gabriel Herrera", "Luis Galindo"))
R = EV["resumen_prs"]
assert (R["abiertos"], R["mergeados"], R["solicitudes_de_cambio"]) == (20, 19, 25)
resen = len(EV["reestimaciones"])
sin_acierto = S["act"] - S["con"]

# ---------------------------------------------------------------- actividades de septiembre (devoluciones y desviación)
ESPERA_LARGA = {e["tarea"] for e in EV["esperas_de_revision"]}
act_sep = []
for r in rows9:
    if r["dev"] in TEAM3 and str(r["id"]).startswith("API-") and (r["I"] or 0) > 0:
        g = r["G"] if isinstance(r["G"], (int, float)) and r["G"] > 0 else None
        ej = r["H"] + r["I"]
        j = (ej - g) / g if g else None
        act_sep.append(dict(id=r["id"], tipo=r["tipo"], obs=bool(r["obs"]), fila=r["row"], dev=r["devol"] if isinstance(r["devol"], (int, float)) else None, ej=ej, g=g, j=j,
                            ok=(j is not None and j <= 0.30 + 1e-9), larga=r["id"] in ESPERA_LARGA))
con_est = [a for a in act_sep if a["g"]]
grupos = {"0": [0, 0], "1": [0, 0], "2": [0, 0], "3 o más": [0, 0]}
for a in con_est:
    d = a["dev"] or 0
    k = "0" if d == 0 else "1" if d == 1 else "2" if d == 2 else "3 o más"
    grupos[k][0 if a["ok"] else 1] += 1
con_dev = [a for a in con_est if (a["dev"] or 0) >= 1]
ok_dev = [a for a in con_dev if a["ok"]]
dev_larga = sum(a["ej"] - a["g"] for a in con_est if a["larga"])
dev_resto = sum(a["ej"] - a["g"] for a in con_est if not a["larga"])
n_resto = sum(1 for a in con_est if not a["larga"])
assert (len(con_est), len(con_dev), len(ok_dev), dev_larga, dev_resto, n_resto) == (25, 19, 12, 169, -9, 21)
larga_rows = sorted([a for a in con_est if a["larga"]], key=lambda a: -(a["ej"] - a["g"]))
ESTD = EV["estandarizacion"]
n_estd = len({q["pr"] for q in ESTD["descripcion_del_pr"] + ESTD["evidencia_de_pruebas"]})


cumplen_dev = sorted([a for a in con_est if a["ok"]], key=lambda a: (-(a["dev"] or 0), num_(a["id"])))
conj_dev_max = max((a["dev"] or 0) for a in cumplen_dev)
desv = sorted([a for a in act_sep if a["tipo"] == "Desviado"], key=lambda a: -(a["ej"] - a["g"]))
desv_h = sum(a["ej"] - a["g"] for a in desv)
desv_dev = sum((a["dev"] or 0) for a in desv)
desv_obs = sum(1 for a in desv if a["obs"])
sin_est = [a for a in act_sep if a["tipo"] == "Sin estimación"]
assert all((a["tipo"] == "Normal") == a["ok"] for a in con_est)      # «Normal» = cumple (J ≤ 30 %)
assert (len(desv), len(sin_est)) == (7, 1)


def svg_medicion():
    tarjetas = [("Horas estimadas → ejecutadas", f"{fmt(S['es'], 0)} → {fmt(S['ej'], 0)} h", f"+{fmt(S['ej'] - S['es'], 0)} h (+{fmt(100 * (S['ej'] - S['es']) / S['es'], 0)} %) · {len(con_est)} actividades con estimación"),
                ("Tiempos que se desvían (> +30 %)", f"{len(desv)} de {len(con_est)}", f"«Desviado»: +{fmt(desv_h, 0)} h sobre lo estimado"),
                ("Devoluciones", f"{S['devol']}", f"en las {S['act']} actividades; {desv_dev} en las {len(desv)} desviadas")]
    out = ['<svg viewBox="0 0 760 112" role="img" aria-label="Lo que mide hoy el informe de seguimiento">']
    for i, (t, v, d) in enumerate(tarjetas):
        x = 2 + i * 254
        out.append(f'<rect x="{x}" y="4" width="244" height="100" rx="10" fill="#FFFFFF" stroke="#DCD8EC" stroke-width="1.4"/>')
        out.append(f'<text x="{x + 16}" y="28" font-size="11.5" font-weight="600" fill="#5B5A66">{t}</text>')
        out.append(f'<text x="{x + 16}" y="68" font-size="30" font-weight="600" fill="#280265">{v}</text>')
        out.append(f'<text x="{x + 16}" y="90" font-size="9.5" fill="#5B5A66">{esc(d)}</text>')
    out.append("</svg>")
    return "".join(out)


def dias_hab(a, b):
    if b <= a:
        return 0.0
    tot, cur = 0.0, a
    while cur < b:
        nxt = min(b, (cur + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
        if cur.weekday() < 5:
            tot += (nxt - cur).total_seconds() / 86400
        cur = nxt
    return tot


ret_rev = sum(TI[a["id"]]["rev"] for a in act_sep)
ret_uat = sum(TI[a["id"]]["uat"] for a in act_sep)
n_uat_ret = sum(1 for a in act_sep if TI[a["id"]]["uat"])
n_rfp = sum(1 for a in act_sep if TI[a["id"]]["rfp"])
n_done = sum(1 for a in act_sep if TI[a["id"]]["done"])


def svg_flujo():
    cajas = [("To Do", "otro equipo", "estima en horas", 0), ("In Progress", f"3 personas", f"{fmt(S['horas_mes'], 0)} h en sept.", 0),
             ("In review", "revisión del PR", f"{R['abiertos']} PRs en sept.", 2), ("UAT", "prueba tras el", "despliegue a prueba", 0),
             ("Ready for prod", "listo para producción", "el equipo terminó", 0), ("Done", "desplegado en", "producción", 0)]
    mira = {0: "horas estimadas", 1: "horas ejecutadas"}
    out = ['<svg viewBox="0 0 760 252" role="img" aria-label="Estados de una actividad en Jira hoy, devoluciones y dónde se acumula la espera">',
           '<defs><marker id="fl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="#5300DF"/></marker></defs>',
           '<text x="2" y="14" font-size="11" font-weight="600" fill="#280265">Lo que mira Viva Aerobus hoy</text>']
    for i, (t1, t2, t3, rojo) in enumerate(cajas):
        x = 2 + i * 130
        fill, stroke, col = ("#FDECEC", "#B42318", "#B42318") if rojo else ("#EBEBFF", "#5300DF", "#280265")
        out.append(f'<rect x="{x}" y="64" width="108" height="64" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        out.append(f'<text x="{x + 54}" y="88" text-anchor="middle" font-size="11" font-weight="600" fill="{col}">{esc(t1)}</text>')
        out.append(f'<text x="{x + 54}" y="105" text-anchor="middle" font-size="9" fill="#5B5A66">{esc(t2)}</text>')
        out.append(f'<text x="{x + 54}" y="117" text-anchor="middle" font-size="9" fill="#5B5A66">{esc(t3)}</text>')
        if i in mira:
            out.append(f'<rect x="{x + 4}" y="28" width="100" height="22" rx="11" fill="#FFFFFF" stroke="#5300DF" stroke-width="1"/>')
            out.append(f'<text x="{x + 54}" y="43" text-anchor="middle" font-size="9" font-weight="600" fill="#5300DF">{mira[i]}</text>')
            out.append(f'<line x1="{x + 54}" y1="50" x2="{x + 54}" y2="64" stroke="#5300DF" stroke-width="1" stroke-dasharray="3 2"/>')
        if i < 5:
            out.append(f'<line x1="{x + 110}" y1="96" x2="{x + 128}" y2="96" stroke="#5300DF" stroke-width="1.4" marker-end="url(#fl)"/>')
    out.append('<line x1="186" y1="128" x2="186" y2="152" stroke="#5300DF" stroke-width="1.2" stroke-dasharray="3 2"/>')
    out.append('<rect x="2" y="152" width="262" height="86" rx="8" fill="#FFFFFF" stroke="#5300DF" stroke-width="1.4"/>')
    out.append('<text x="133" y="173" text-anchor="middle" font-size="11" font-weight="600" fill="#280265">Devoluciones: vuelven a In Progress</text>')
    out.append(f'<text x="133" y="191" text-anchor="middle" font-size="10" fill="#1A1E27">desde In review: {ret_rev}</text>')
    out.append(f'<text x="133" y="206" text-anchor="middle" font-size="10" fill="#1A1E27">desde UAT: {ret_uat}</text>')
    out.append(f'<text x="133" y="224" text-anchor="middle" font-size="9" fill="#5B5A66">{len(act_sep)} actividades de septiembre · Jira</text>')
    out.append('<line x1="316" y1="128" x2="316" y2="152" stroke="#B42318" stroke-width="1.2"/>')
    out.append('<rect x="282" y="152" width="360" height="86" rx="8" fill="#FFFFFF" stroke="#B42318" stroke-width="1.4"/>')
    out.append('<text x="462" y="173" text-anchor="middle" font-size="11" font-weight="600" fill="#B42318">Lo que hoy no se mide: la espera de revisión</text>')
    out.append(f'<text x="462" y="191" text-anchor="middle" font-size="10" fill="#1A1E27">{len(esp)} de 26 actividades esperaron más de 30 días hábiles</text>')
    out.append(f'<text x="462" y="206" text-anchor="middle" font-size="10" fill="#1A1E27">la primera acción del revisor (hasta {fmt(esp["API-724"]["habiles"], 0)})</text>')
    out.append(f'<text x="462" y="224" text-anchor="middle" font-size="9" fill="#5B5A66">{R["revisados"] - R["primera_revision_en_2_habiles_o_menos"]} de {R["revisados"]} PRs con más de 2 días hábiles</text>')
    out.append("</svg>")
    return "".join(out)


def svg_devoluciones():
    out = ['<svg viewBox="0 0 760 196" role="img" aria-label="Actividades que cumplen y no cumplen según su número de devoluciones">',
           '<text x="2" y="14" font-size="11" font-weight="600" fill="#280265">Actividades de septiembre por número de devoluciones</text>']
    u = 36
    for i, (k, (c, n)) in enumerate(grupos.items()):
        y = 30 + i * 32
        out.append(f'<text x="2" y="{y + 16}" font-size="10.5" fill="#1A1E27">{k} {"devolución" if k == "1" else "devoluciones"}</text>')
        if c:
            out.append(f'<rect x="150" y="{y}" width="{c * u}" height="22" rx="4" fill="#5300DF"/><text x="{150 + c * u / 2}" y="{y + 15}" text-anchor="middle" font-size="10.5" font-weight="600" fill="#FFFFFF">{c}</text>')
        if n:
            out.append(f'<rect x="{150 + c * u}" y="{y}" width="{n * u}" height="22" rx="4" fill="#B9720A"/><text x="{150 + c * u + n * u / 2}" y="{y + 15}" text-anchor="middle" font-size="10.5" font-weight="600" fill="#FFFFFF">{n}</text>')
    out.append('<rect x="150" y="166" width="12" height="12" rx="2" fill="#5300DF"/><text x="168" y="176" font-size="10" fill="#5B5A66">Cumplió lo estimado (hasta +30 %)</text>')
    out.append('<rect x="370" y="166" width="12" height="12" rx="2" fill="#B9720A"/><text x="388" y="176" font-size="10" fill="#5B5A66">No cumplió</text>')
    out.append(f'<text x="470" y="52" font-size="11" font-weight="600" fill="#280265">{len(con_dev)} de {len(con_est)} actividades tienen devoluciones</text>')
    out.append(f'<text x="470" y="70" font-size="10.5" fill="#1A1E27">{len(ok_dev)} de esas {len(con_dev)} cumplieron lo estimado</text>')
    out.append(f'<text x="470" y="92" font-size="10" fill="#5B5A66">Con 3 o más devoluciones, {grupos["3 o más"][0]} de {sum(grupos["3 o más"])}</text>')
    out.append('<text x="470" y="107" font-size="10" fill="#5B5A66">cumplieron: el número de devoluciones</text>')
    out.append('<text x="470" y="122" font-size="10" fill="#5B5A66">no separa por sí solo cumplir de no cumplir.</text>')
    out.append("</svg>")
    return "".join(out)


def svg_desvio():
    x0, k = 190, 2.0
    out = ['<svg viewBox="0 0 760 160" role="img" aria-label="Dónde se concentra la desviación de horas de septiembre">',
           f'<text x="2" y="14" font-size="11" font-weight="600" fill="#280265">Desviación de horas de septiembre: ejecutadas menos estimadas</text>',
           f'<text x="2" y="38" font-size="10.5" fill="#1A1E27">{len(larga_rows)} actividades con espera de revisión &gt; 30 días hábiles: +{fmt(dev_larga, 0)} h</text>']
    x = x0
    sombras = ["#B9720A", "#C98A2E", "#D9A24F", "#E4B873"]
    for i, a in enumerate(larga_rows):
        w = (a["ej"] - a["g"]) * k
        out.append(f'<rect x="{x:.1f}" y="46" width="{w:.1f}" height="30" fill="{sombras[i % 4]}" stroke="#FFFFFF" stroke-width="1"/>')
        out.append(f'<text x="{x + w / 2:.1f}" y="59" text-anchor="middle" font-size="8.5" font-weight="600" fill="#1A1E27">{a["id"]}</text>')
        out.append(f'<text x="{x + w / 2:.1f}" y="71" text-anchor="middle" font-size="9" fill="#1A1E27">+{fmt(a["ej"] - a["g"], 0)} h</text>')
        x += w
    out.append(f'<text x="2" y="108" font-size="10.5" fill="#1A1E27">Las otras {n_resto} actividades: {fmt(dev_resto, 0).replace("-", "−")} h</text>')
    wr = abs(dev_resto) * k
    out.append(f'<rect x="{x0 - wr:.1f}" y="116" width="{wr:.1f}" height="22" fill="#5300DF"/>')
    out.append(f'<text x="{x0 - wr - 6:.1f}" y="131" text-anchor="end" font-size="10" font-weight="600" fill="#5300DF">{fmt(dev_resto, 0).replace("-", "−")} h</text>')
    out.append(f'<line x1="{x0}" y1="42" x2="{x0}" y2="144" stroke="#1A1E27" stroke-width="1"/>')
    out.append(f'<text x="{x0 + 8}" y="136" font-size="10" fill="#5B5A66">Neto del mes: +{fmt(S["ej"] - S["es"], 0)} h (+{fmt(100 * (S["ej"] - S["es"]) / S["es"], 0)} %)</text>')
    out.append("</svg>")
    return "".join(out)


def svg_propuesta():
    cajas = [("Diseño conjunto", "Viva y Tech and Solve", "definen la actividad"), ("Tamaño en puntos", "1, 2, 3, 5, 8, 13 o 21", "en vez de horas"),
             ("Desarrollo", "pruebas unitarias", "automatizadas y Sonar"), ("PR abierto", "con descripción y", "evidencia estándar"),
             ("Revisión", "máx. 2 días hábiles", "para la primera acción"), ("PR aprobado", "sesión de entrega", "y se paga")]
    mira = {0: "tamaño acordado", 3: "estándar de PR", 4: "espera de revisión", 2: "Quality Gate de Sonar"}
    out = ['<svg viewBox="0 0 760 250" role="img" aria-label="Recorrido de una actividad con la propuesta, qué se observa y qué se paga">',
           '<defs><marker id="pf" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="#5300DF"/></marker></defs>',
           '<text x="2" y="14" font-size="11" font-weight="600" fill="#280265">Qué se observa en cada paso</text>']
    for i, (t1, t2, t3) in enumerate(cajas):
        x = 2 + i * 130
        ult = i == 5
        fill, stroke, col = ("#280265", "#280265", "#FFFFFF") if ult else ("#EBEBFF", "#5300DF", "#280265")
        sub = "#DCD8EC" if ult else "#5B5A66"
        out.append(f'<rect x="{x}" y="64" width="108" height="72" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        out.append(f'<text x="{x + 54}" y="88" text-anchor="middle" font-size="11" font-weight="600" fill="{col}">{esc(t1)}</text>')
        out.append(f'<text x="{x + 54}" y="106" text-anchor="middle" font-size="9" fill="{sub}">{esc(t2)}</text>')
        out.append(f'<text x="{x + 54}" y="119" text-anchor="middle" font-size="9" fill="{sub}">{esc(t3)}</text>')
        if i in mira:
            out.append(f'<rect x="{x + 2}" y="28" width="104" height="22" rx="11" fill="#FFFFFF" stroke="#5300DF" stroke-width="1"/>')
            out.append(f'<text x="{x + 54}" y="43" text-anchor="middle" font-size="9" font-weight="600" fill="#5300DF">{mira[i]}</text>')
            out.append(f'<line x1="{x + 54}" y1="50" x2="{x + 54}" y2="64" stroke="#5300DF" stroke-width="1" stroke-dasharray="3 2"/>')
        if i < 5:
            out.append(f'<line x1="{x + 110}" y1="100" x2="{x + 128}" y2="100" stroke="#5300DF" stroke-width="1.4" marker-end="url(#pf)"/>')
    out.append('<line x1="656" y1="136" x2="656" y2="160" stroke="#280265" stroke-width="1.2"/>')
    out.append('<rect x="372" y="160" width="386" height="80" rx="8" fill="#FFFFFF" stroke="#280265" stroke-width="1.4"/>')
    out.append('<text x="565" y="181" text-anchor="middle" font-size="11" font-weight="600" fill="#280265">Qué se paga</text>')
    out.append('<text x="565" y="199" text-anchor="middle" font-size="10" fill="#1A1E27">Los puntos de cada actividad con PR aprobado</text>')
    out.append(f'<text x="565" y="215" text-anchor="middle" font-size="10" fill="#1A1E27">dentro de un paquete mensual de {PERS[0]}, {PERS[1]} o {PERS[2]} personas</text>')
    out.append('<text x="565" y="231" text-anchor="middle" font-size="9" fill="#5B5A66">No se paga por horas, personas ni intentos de revisión</text>')
    out.append("</svg>")
    return "".join(out)


def svg_enfoque():
    hoy = [("Horas estimadas", "La estimación llega fijada en horas", "y se compara con lo ejecutado"),
           ("Tiempos que se desvían", f"{len(desv)} de {len(con_est)} actividades «Desviado»: +{fmt(desv_h, 0)} h", f"{len(larga_rows)} con espera de revisión > 30 días hábiles: +{fmt(dev_larga, 0)} h"),
           ("Número de devoluciones", f"{len(ok_dev)} de las {len(con_dev)} actividades con devoluciones", "cumplieron lo estimado")]
    des = [("Cumplimiento en la entrega", "Actividad con PR aprobado dentro de su tamaño", ""),
           ("Espera de revisión", "Máximo 2 días hábiles;", f"hoy {R['primera_revision_en_2_habiles_o_menos']} de {R['revisados']} PRs lo cumplen"),
           ("Quality Gate de Sonar", f"Hoy {R['mergeados_con_sonar_rojo']} de {R['mergeados']} PRs mergeados en rojo;", "ninguna reseña lo menciona"),
           ("Estándar de PR y evidencia", f"Pedidos distintos sobre descripción y", f"evidencia en {n_estd} PRs de septiembre")]
    out = ['<svg viewBox="0 0 760 322" role="img" aria-label="Lo que mira Viva Aerobus hoy y lo que mira después del cambio">',
           '<defs><marker id="en" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L8 4L0 8z" fill="#5300DF"/></marker></defs>',
           '<text x="2" y="16" font-size="12" font-weight="600" fill="#5B5A66">Hoy: lo que mira Viva Aerobus</text>',
           '<text x="420" y="16" font-size="12" font-weight="600" fill="#280265">Después: lo que mira Viva Aerobus</text>']
    for i, (t, a, b) in enumerate(hoy):
        y = 28 + i * 86
        out.append(f'<rect x="2" y="{y}" width="330" height="74" rx="8" fill="#FFFFFF" stroke="#DCD8EC" stroke-width="1.4"/>')
        out.append(f'<text x="14" y="{y + 24}" font-size="11.5" font-weight="600" fill="#5B5A66">{esc(t)}</text>')
        out.append(f'<text x="14" y="{y + 44}" font-size="9.5" fill="#1A1E27">{esc(a)}</text>')
        out.append(f'<text x="14" y="{y + 58}" font-size="9.5" fill="#1A1E27">{esc(b)}</text>')
    for i, (t, a, b) in enumerate(des):
        y = 28 + i * 64
        out.append(f'<rect x="420" y="{y}" width="338" height="54" rx="8" fill="#EBEBFF" stroke="#5300DF" stroke-width="1.4"/>')
        out.append(f'<text x="432" y="{y + 20}" font-size="11.5" font-weight="600" fill="#280265">{esc(t)}</text>')
        out.append(f'<text x="432" y="{y + 36}" font-size="9.5" fill="#1A1E27">{esc(a)}</text>')
        if b:
            out.append(f'<text x="432" y="{y + 48}" font-size="9.5" fill="#1A1E27">{esc(b)}</text>')
    out.append('<line x1="344" y1="150" x2="408" y2="150" stroke="#5300DF" stroke-width="2" marker-end="url(#en)"/>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- piezas de HTML
CHECK = ('<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 6.5l2.5 2.5L10 3.5" fill="none" stroke="currentColor" '
         'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def kv(rows_):
    return ('<table class="scenario-table"><tbody>'
            + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows_) + "</tbody></table>\n")


T0 = open(TEMPLATE).read()
head = (T0[:T0.index("<body>")].replace("{{TITULO_CORTO}}", "Paquetes de puntos")
        .replace("{{PROYECTO}}", "Generic API").replace("{{CLIENTE}}", "Viva Aerobus"))

# --- tabla de tamaños (sección 2)
menu = "".join(
    f'<tr><th class="col-narrow">{z}</th><td>{rng[z]}</td><td>{tk(ex[z][0])} · {fmt(ex[z][1]["h"])}&nbsp;h + 30&nbsp;% = {fmt(ex[z][1]["a"])}&nbsp;h</td></tr>' for z in PTS)
menu += (f'<tr><th class="col-narrow">Dividir</th><td>{rng["D"]}</td>'
         f'<td>Se divide en actividades menores antes de aceptarla.</td></tr>')

HRP = float(H) / TOTP                              # horas reales por punto (sin el 30 %)
NOM = ("Inicial", "Estándar", "Ampliado")
prow = "".join(
    f"<tr><th>{nom}</th><td>{n} {'persona' if n == 1 else 'personas'}{' (equipo actual)' if n == 3 else ''}</td><td>{p} puntos</td><td>{p} × valor del punto</td>"
    f"<td>{fmt(p * HRP, 0)}&nbsp;h ({fmt(100 * p * HRP / (n * 168), 0)}&nbsp;% de {n * 168}&nbsp;h)</td>"
    f"<td>{(str(c) + ' de ' + str(len(tot3))) if n == 3 else 'sin histórico: más personas que hoy'}</td></tr>"
    for nom, n, p, c in zip(NOM, PERS, PK, cnt3))

# --- anexo A: resumen por tamaño y por mes
sumrows = ""
for z in KEYS:
    g = agg[z]
    hpp = f"{fmt(g[2] / g[0] / z)}&nbsp;h" if z != "D" else "&nbsp;"
    sumrows += (f'<tr><th class="col-narrow">{z if z != "D" else "Dividir"}</th><td>{rng[z]}</td><td>{g[0]}</td>'
                f'<td>{fmt(g[1])}&nbsp;h</td><td>{fmt(g[2])}&nbsp;h</td><td>{hpp}</td></tr>')
sumrows += (f'<tr><th class="col-narrow">Total</th><td>&nbsp;</td><td><strong>{N}</strong></td>'
            f'<td><strong>{fmt(H)}&nbsp;h</strong></td><td><strong>{fmt(A)}&nbsp;h</strong></td><td>{fmt(HPP)}&nbsp;h</td></tr>')
monrows = "".join(
    f'<tr><th>{MES[int(m[5:])].capitalize()} de {m[:4]}</th><td>{mo[m][0]}</td><td>{mo[m][1]}</td><td>{len(mo[m][2])}</td></tr>'
    for m in months)
monrows += (f'<tr><th>Sin fecha de cierre</th><td>{len(sin_fecha)}</td><td>{pts_sin_fecha}</td><td>&nbsp;</td></tr>')


def num(k):
    m = re.search(r"(\d+)", k)
    return int(m.group(1)) if m else 0


def cierre(v):
    if not v["f"]:
        return "—"
    return fdate(v["f"]) + ("*" if v["fsrc"] == "entrega" else "†" if v["fsrc"] == "jira" else "")


tasks = "".join(
    f'<tr><td class="col-narrow">{tk(k)}</td><td>{esc(v["s"])}</td><td class="col-narrow">{cierre(v)}</td>'
    f'<td class="col-narrow">{fmt(v["h"])}&nbsp;h</td><td class="col-narrow">{fmt(v["a"])}&nbsp;h</td>'
    f'<td class="col-narrow">{size(v["a"]) if size(v["a"]) != "D" else "Dividir"}</td></tr>'
    for k, v in sorted(use.items(), key=lambda kv: num(kv[0])))

# --- anexo C: PRs de septiembre
def sonar_txt(s):
    n = s["issues_nuevos"]
    return f'rojo · {n}&nbsp;{"issue" if n == 1 else "issues"}' if s["estado"] == "rojo" else "verde"


prrows = ""
for p in EV["prs_septiembre"]:
    prrows += (f'<tr><td class="col-narrow">{pr(p["pr"])}</td><td class="col-narrow">{tk(p["tarea"])}</td>'
               f'<td class="col-narrow">{fiso(p["abierto"])}</td>'
               f'<td class="col-narrow">{fiso(p["primera_revision"])} · {fmt(p["espera_primera_revision_habiles"])}</td>'
               f'<td class="col-narrow">{p["solicitudes_de_cambio"]}</td>'
               f'<td class="col-narrow">{fiso(p["primera_aprobacion"]) if p["primera_aprobacion"] else "—"}'
               f'{(" · " + fmt(p["espera_hasta_aprobacion_habiles"])) if p["primera_aprobacion"] else ""}</td>'
               f'<td class="col-narrow">{fiso(p["merge"]) if p["merge"] else "abierto"}</td>'
               f'<td class="col-narrow">{sonar_txt(p["sonar"])}</td></tr>')
esp = {e["tarea"]: e for e in EV["esperas_de_revision"]}
esperas_rows = (
    f'<tr><td class="col-narrow">{tk("API-724")}</td><td class="col-narrow">{pr(2209)}</td><td>25&nbsp;nov&nbsp;2025</td>'
    f'<td>Sin ninguna reseña al 8&nbsp;oct&nbsp;2026</td><td>{fmt(esp["API-724"]["habiles"])} ({fmt(esp["API-724"]["corridos"], 0)} corridos)</td></tr>')
for k, ini, fin_ in (("API-1663", "30&nbsp;jun", "16&nbsp;sep"), ("API-1693", "7&nbsp;jul", "21&nbsp;sep"), ("API-1529", "3&nbsp;ago", "17&nbsp;sep")):
    e = esp[k]
    esperas_rows += (f'<tr><td class="col-narrow">{tk(k)}</td><td class="col-narrow">{pr(e["pr"])}</td><td>{ini}</td>'
                     f'<td>{fin_}</td><td>{fmt(e["habiles"])} ({fmt(e["corridos"])} corridos)</td></tr>')
ma = {m["tarea"]: m for m in EV["impacto_rama_base"]}
master_rows = ""
for k in ("API-1663", "API-1693"):
    m = ma[k]
    master_rows += (f'<tr><td class="col-narrow">{tk(k)}</td><td>«{esc(m["pedido"])}» · {m["donde"]}, {fiso(m["fecha"])}</td>'
                    f'<td>{m["devoluciones_siguientes"]}</td><td>{fmt(m["h_desarrollador"])}&nbsp;h</td>'
                    f'<td>{fmt(m["h_revisores"])}&nbsp;h</td><td>{m["ejecutadas"]} / {m["estimadas"]}&nbsp;h</td></tr>')
tot_dev = sum(m["devoluciones_siguientes"] for m in ma.values())
tot_hd = sum(m["h_desarrollador"] for m in ma.values())
tot_hr = sum(m["h_revisores"] for m in ma.values())
tot_ej = sum(m["ejecutadas"] for m in ma.values())
tot_es = sum(m["estimadas"] for m in ma.values())
assert (tot_dev, tot_hd, tot_hr, tot_ej - tot_es) == (4, 26.0, 21.5, 65)
master_rows += (f'<tr><td class="col-narrow"><strong>Total</strong></td><td>&nbsp;</td><td><strong>{tot_dev}</strong></td>'
                f'<td><strong>{fmt(tot_hd)}&nbsp;h</strong></td><td><strong>{fmt(tot_hr)}&nbsp;h</strong></td>'
                f'<td><strong>{tot_ej} / {tot_es}&nbsp;h</strong></td></tr>')
sep_rows = "".join(
    f'<tr><td class="col-narrow">{tk(a["id"])}</td><td class="col-narrow">{a["dev"] if a["dev"] is not None else "—"}</td>'
    f'<td>{fmt(a["ej"])}' + (f' / {fmt(a["g"])}' if a["g"] else ' / —') + '&nbsp;h</td>'
    f'<td>{("cumple" if a["ok"] else "no cumple") + " · +" + fmt(100 * a["j"], 0) + "&nbsp;%" if a["j"] is not None and a["j"] > 0 else ("cumple · acertó" if a["ok"] else "sin estimación")}</td>'
    f'<td>{"sí" if a["larga"] else "—"}</td></tr>' for a in sorted(act_sep, key=lambda a: num(a["id"])))
estd_rows = "".join(
    f'<tr><td class="col-narrow">{pr(q["pr"])}</td><td class="col-narrow">{tk(q["tarea"])}</td><td class="col-narrow">{fiso(q["fecha"])}</td>'
    f'<td>{tema}</td><td>«{esc(q["pedido"])}»</td></tr>'
    for tema, lst in (("Descripción del PR", ESTD["descripcion_del_pr"]), ("Evidencia de pruebas", ESTD["evidencia_de_pruebas"])) for q in lst)
preg_rows = "".join(f'<tr><td class="col-narrow">{pr(q["pr"])}</td><td class="col-narrow">{tk(q["tarea"])}</td>'
                    f'<td class="col-narrow">{fiso(q["fecha"])}</td><td>«{esc(q["cita"])}»</td></tr>'
                    for q in EV["preguntas_de_negocio"])
re_list = ", ".join(tk(k) for k in EV["reestimaciones"])
re_short = ", ".join(k.replace("API-", "") for k in EV["reestimaciones"])
abiertas = EV["abiertas_al_9_oct"]
abiertas_list = ", ".join(tk(k) for k in abiertas)
est_otra = ", ".join(tk(k) for k in EV["estimacion_inicial_fijada_por_otra_persona"])
n_labels = sum(1 for v in EV["etiquetas_de_prueba"].values() if any(x in ("TestCaseReady", "TestCasesReady") for x in v))

# ---------------------------------------------------------------- cuerpo
# ---------------------------------------------------------------- paneles «ver más →» (patrón del informe de septiembre)
DRAWER_CSS = """
  /* ---- «ver más →»: panel lateral sin JavaScript de apertura (input + velo + panel adyacentes) ---- */
  label.more{cursor:pointer;color:var(--accent);font-size:.95em;font-weight:600;white-space:nowrap;margin-left:4px;}
  label.more:hover{text-decoration:underline;}
  .dr-toggle{position:fixed;top:0;left:0;opacity:0;width:1px;height:1px;pointer-events:none;}
  .dr-back{position:fixed;inset:0;background:rgba(26,30,39,.35);opacity:0;pointer-events:none;transition:opacity .2s;z-index:1000;}
  .drawer{position:fixed;top:0;right:0;height:100vh;height:100dvh;width:min(680px,94vw);background:#FFFFFF;box-shadow:-8px 0 24px rgba(26,30,39,.18);transform:translateX(105%);visibility:hidden;transition:transform .25s ease,visibility 0s linear .25s;z-index:1001;display:flex;flex-direction:column;}
  .dr-toggle:checked + .dr-back{opacity:1;pointer-events:auto;}
  .dr-toggle:checked + .dr-back + .drawer{transform:none;visibility:visible;transition:transform .25s ease;}
  .dr-head{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--border);background:var(--violet-light);color:var(--violet);font-size:14px;}
  .dr-close{cursor:pointer;font-size:12px;font-weight:600;color:var(--accent);white-space:nowrap;}
  .dr-body{overflow:auto;padding:14px 18px 28px;flex:1;}
  .dr-body h4{margin-top:14px;}
  .print-only{display:none;}
  @media print{
    label.more,.dr-toggle,.dr-back,.dr-close{display:none !important;}
    .print-only{display:block;}
    .drawer{position:static;transform:none;visibility:visible;width:auto;height:auto;box-shadow:none;display:block;margin-top:14px;}
    .dr-head{background:none;padding:0 0 4px;border-bottom:2px solid var(--violet);font-size:12px;}
    .dr-body{overflow:visible;padding:6px 0 0;}
  }
"""
head = head.replace("</style>", DRAWER_CSS + "</style>", 1)
DR = []


def more(i, titulo, cuerpo, texto="ver más →"):
    """Registra un panel y devuelve el enlace «ver más →» que lo abre."""
    if not any(d[0] == i for d in DR):
        DR.append((i, titulo, cuerpo))
    return f'<label class="more" for="{i}">{texto}</label>'


def drawers_html():
    out = ['<h2 class="print-only break-before">Anexos</h2>', '<div class="dr-set">']
    for i, titulo, cuerpo in DR:
        out.append(f'<input type="checkbox" class="dr-toggle" id="{i}"><label class="dr-back" for="{i}" aria-hidden="true"></label>'
                   f'<div class="drawer" role="dialog" aria-label="{esc(titulo)}"><div class="dr-head"><strong>{esc(titulo)}</strong>'
                   f'<label class="dr-close" for="{i}">Cerrar</label></div><div class="dr-body">{cuerpo}</div></div>')
    out.append("</div>")
    return "\n".join(out)


def tabla(cab, filas_html, clase="scenario-table glossary allow-break"):
    return f'<table class="{clase}"><thead><tr>{cab}</tr></thead><tbody>{filas_html}</tbody></table>'


# --- contenido de los paneles
more("d-acierto", "Estimación en horas: acierto y reestimaciones", f"""
  <p>Septiembre: <strong>{S["ok"]} de {S["con"]}</strong> actividades con estimación cumplieron (hasta +30&nbsp;%); agosto: <strong>{G8["ok"]} de {G8["con"]}</strong>. Horas ejecutadas / estimadas: septiembre {fmt(S["ej"])} / {fmt(S["es"], 0)} (+{fmt(S["ej"] - S["es"], 0)}&nbsp;h, +{fmt(100 * (S["ej"] - S["es"]) / S["es"], 0)}&nbsp;%); agosto {fmt(G8["ej"])} / {fmt(G8["es"], 0)} (+{fmt(G8["ej"] - G8["es"])}&nbsp;h, +{fmt(100 * (G8["ej"] - G8["es"]) / G8["es"], 0)}&nbsp;%). {fs("F1", "F2")}</p>
  <p>Cambiaron su estimación durante el trabajo ({resen} de 26): {re_list}. {fs("F3")}</p>""")
more("d-esperas", "Esperas de revisión de más de 30 días hábiles", f"""
  <p>Septiembre: mediana de <strong>{fmt(R["mediana_primera_revision_habiles"])} días hábiles</strong> hasta la primera revisión; <strong>{R["primera_revision_en_2_habiles_o_menos"]} de {R["revisados"]}</strong> PRs la recibieron en 2 días hábiles o menos. {fs("F4")}</p>
  {tabla('<th class="col-narrow">Tarea</th><th class="col-narrow">PR</th><th>En revisión desde</th><th>Primera acción del revisor</th><th>Espera en días hábiles</th>', esperas_rows)}
  <p class="diagram-caption">Jira: pase a «In review» y primera transición del revisor. API-724 se mide en GitHub, porque su PR nunca recibió una reseña. {fs("F3", "F4")}</p>""")
more("d-master", "Pedido de actualizar con master tras la espera", f"""
  {tabla('<th class="col-narrow">Tarea</th><th>Pedido del revisor</th><th>Devoluciones desde el pedido</th><th>Horas de desarrolladores</th><th>Horas de revisores</th><th>Ejecutadas / estimadas</th>', master_rows)}
  <p class="diagram-caption">Horas registradas en Jira desde el día del pedido; no se separa qué parte se debió a la rama base. El PR {pr(2428)} de {tk("API-1693")} se cerró y se rehízo como {pr(2509)}. {fs("F1", "F3", "F4")}</p>""")
more("d-pr", "PRs abiertos en septiembre", f"""
  <p>{R["abiertos"]} abiertos, {R["mergeados"]} mergeados. Mediana hasta la primera revisión {fmt(R["mediana_primera_revision_habiles"])} días hábiles; {R["solicitudes_de_cambio"]} solicitudes de cambio ({fmt(R["solicitudes_por_pr"], 2)} por PR), {R["aprobados_sin_solicitudes"]} aprobados sin ninguna; apertura → primera aprobación: mediana {fmt(R["mediana_hasta_aprobacion_habiles"])} (máximo {fmt(R["max_hasta_aprobacion_habiles"])}); apertura → merge: mediana {fmt(R["mediana_hasta_merge_habiles"])}. Sonar: {R["mergeados_con_sonar_rojo"]} de {R["mergeados"]} mergeados con el Quality Gate en rojo ({R["issues_en_mergeados_con_sonar_rojo"]} issues nuevos); {R["menciones_de_sonar_por_terceros"]} menciones en {R["resenas_y_comentarios_de_terceros_revisados"]} reseñas y comentarios de revisores. {fs("F4")}</p>
  {tabla('<th class="col-narrow">PR</th><th class="col-narrow">Tarea</th><th class="col-narrow">Abierto</th><th class="col-narrow">1.ª revisión · espera</th><th class="col-narrow">Cambios pedidos</th><th class="col-narrow">1.ª aprobación · espera</th><th class="col-narrow">Merge</th><th class="col-narrow">Sonar</th>', prrows)}
  <p class="diagram-caption">Días hábiles = lunes a viernes. Sonar: último análisis publicado en el PR y número de issues nuevos.</p>""")
more("d-act", "Actividades de septiembre: devoluciones y desviación", f"""
  <p>Las {len(act_sep)} actividades con horas en septiembre; cumple = desviación de hasta +30&nbsp;% (columna J). {fs("F1")}</p>
  {tabla('<th class="col-narrow">Tarea</th><th class="col-narrow">Devoluciones (K)</th><th>Ejecutadas / estimadas (H + I / G)</th><th>Resultado</th><th>Espera de revisión &gt; 30 días hábiles</th>', sep_rows)}""")
more("d-preg", "PRs con preguntas de negocio o de alcance", f"""
  <p>Lectura de los comentarios de revisión de septiembre. En {pr(2516)}, el equipo respondió el 29 de septiembre que lo confirmó con Viva Aerobus. {fs("F4")}</p>
  {tabla('<th class="col-narrow">PR</th><th class="col-narrow">Tarea</th><th class="col-narrow">Fecha</th><th>Pregunta del revisor</th>', preg_rows, "scenario-table")}""")
more("d-estd", "Pedidos sobre descripción del PR y evidencia de pruebas", f"""
  {tabla('<th class="col-narrow">PR</th><th class="col-narrow">Tarea</th><th class="col-narrow">Fecha</th><th>Tema</th><th>Pedido del revisor</th>', estd_rows, "scenario-table")}
  <p class="diagram-caption">Lectura de las reseñas y comentarios de revisión de septiembre. {fs("F4")}</p>""")
more("d-tam", "Cómo calculamos los tamaños", f"""
  <p><strong>Universo.</strong> Actividades de Generic API (tickets API del informe de septiembre) con al menos un registro terminado por el equipo (Ready for prod, o Done: «Finalizado» o «Finalizada») y con registros de al menos una de las tres personas del equipo. {fs("F1")} No entran otros estados, {tk("API-1860")} (la implementó un revisor: PR {pr(2500)}) {fs("F3", "F4")} ni {tk("API-1621")} (acompañamiento mensual, no una entrega con PR). Resultan <strong>{N} actividades</strong>.</p>
  <p><strong>Tiempo.</strong> Suma de H + I de todos los registros de la actividad: <strong>{fmt(H)} h</strong> reales. Más <strong>30&nbsp;%</strong> de desviación por defecto, el margen con el que el informe da una actividad por cumplida (columna J): <strong>{fmt(A)} h</strong>. El tamaño no usa las estimaciones del informe. {fs("F1", "F2")}</p>
  <p><strong>Puntos.</strong> 1, 2, 3, 5, 8, 13 y 21 siguen la secuencia de Fibonacci, práctica de industria documentada por <a href="https://www.atlassian.com/agile/project-management/fibonacci-story-points">Atlassian</a>, no una norma. {fs("F5")}</p>
  {tabla('<th class="col-narrow">Puntos</th><th>Tiempo</th><th>Actividades</th><th>Horas reales</th><th>Horas con 30&nbsp;%</th><th>Horas por punto</th>', sumrows, "scenario-table")}
  <p>{nD} actividades superan las {LIM[-1]} horas y se dividen antes de aceptarlas; en la serie mensual cada una se divide en partes iguales de hasta {LIM[-1]} h. Límites: las horas del informe no incluyen pruebas unitarias nuevas ni correcciones de Sonar; el primer mes verifica los tamaños.</p>
  <p>{more("d-94", "Las " + str(N) + " actividades finalizadas y sus puntos", f'<p>Los puntos se definen con las horas reales más 30&nbsp;%. * Fecha de entrega, porque la fecha de fin está vacía. † Fecha en que pasó a Ready for prod, según el historial de Jira ({n_jira} actividades de septiembre). {fs("F1")}</p>' + tabla('<th class="col-narrow">Actividad</th><th>Resumen</th><th class="col-narrow">Cierre</th><th class="col-narrow">Horas reales</th><th class="col-narrow">Con 30&nbsp;%</th><th class="col-narrow">Puntos</th>', tasks), f"Ver las {N} actividades →")}</p>""")
more("d-meses", "Cómo salen los paquetes", f"""
  <p>Cada paquete es un número entero de personas × <strong>{PPP} puntos por persona al mes</strong> ({PERS[0]} × {PPP} = {PK[0]}; {PERS[1]} × {PPP} = {PK[1]}; {PERS[2]} × {PPP} = {PK[2]}). Los {PPP} puntos son la parte entera del promedio observado con las tres personas activas ({fmt(pp_prom, 1)}). En esos {len(tot3)} meses el equipo cerró {", ".join(str(x) for x in tot3)} puntos; el rango de todo el histórico va de {lo} a {hi} (mediana {med}). Capacidad: 42 h × 4 semanas = 168&nbsp;h al mes por persona ({fs("F6")}); horas reales = puntos × {fmt(HRP)} h por punto. El resto de la capacidad cubre la espera de revisión, las devoluciones y el trabajo que no cierra en el mes.</p>
  {tabla('<th>Mes de cierre</th><th>Actividades</th><th>Puntos</th><th>Personas del equipo</th>', monrows, "scenario-table")}
  <p class="diagram-caption">Fecha de cierre: pase a Ready for prod en Jira en {n_jira} actividades de septiembre; en las demás, «Fecha fin» (E) del informe o, si está vacía, «Fecha entrega» (F) en {n_fecha_entrega}. {len(sin_fecha)} sin ninguna fecha no entran. Entre {mtxt(solo1[0])} y {mtxt(solo1[-1])} solo una de las tres personas tuvo actividades cerradas por mes; las tres aparecen desde {mtxt(prim3)}. {fs("F1")}</p>
  <p>Ejemplo con el paquete Inicial, con la proporción de tamaños de las actividades finalizadas: {mixtxt} suman {PK[0]} puntos en {sum(mix.values())} actividades.</p>""")
desv_rows = "".join(
    f'<tr><td class="col-narrow">{tk(a["id"])}</td><td>{fmt(a["ej"])} / {fmt(a["g"])}&nbsp;h</td><td>+{fmt(100 * a["j"], 0)}&nbsp;%</td>'
    f'<td class="col-narrow">{a["dev"] if a["dev"] is not None else "—"}</td><td>{"diligenciada" if a["obs"] else "vacía"}</td>'
    f'<td>{"sí" if a["larga"] else "no"}</td></tr>' for a in desv)
more("d-mide", "Qué mide hoy el informe de seguimiento", f"""
  <p>Por actividad, la pestaña «Seguimiento Mes» registra: desarrollador, ticket, estado, fecha fin, fecha de entrega, estimación en horas (G), horas de meses previos (H) y del mes (I), desviación del 30&nbsp;% (J), devoluciones (K), tipo de ticket (L: Normal, Desviado o Sin estimación) y observaciones del desvío (M). {fs("F1")}</p>
  <p>En septiembre, de las {S["act"]} actividades del equipo con horas: <strong>{S["ok"]} «Normal»</strong>, <strong>{len(desv)} «Desviado»</strong> y {len(sin_est)} «Sin estimación» ({tk(sin_est[0]["id"])}). Las {len(desv)} desviadas suman +{fmt(desv_h, 0)}&nbsp;h sobre su estimación y {desv_dev} devoluciones; la observación del desvío (M) está diligenciada en {desv_obs} de {len(desv)}. {fs("F1")}</p>
  {tabla('<th class="col-narrow">Tarea</th><th>Ejecutadas / estimadas</th><th>Desviación (J)</th><th class="col-narrow">Devoluciones (K)</th><th>Observación (M)</th><th>Espera de revisión &gt; 30 días hábiles</th>', desv_rows)}
  <p class="diagram-caption">«Desviado» = más de +30&nbsp;% sobre la estimación; coincide con la columna J en las {len(con_est)} actividades con estimación. {fs("F1")}</p>""")
pers_rows = "".join(
    f'<tr><th>{MES[int(m[5:])].capitalize()} de {m[:4]}</th><td>{mo[m][1]}</td><td>{len(pp[m])}</td><td>{fmt(mo[m][1] / len(pp[m]), 1)}</td>'
    f'<td>{fmt(min(pp[m].values()), 1)} a {fmt(max(pp[m].values()), 1)}</td></tr>' for m in months)
more("d-persona", "Puntos por persona al mes", f"""
  <p>Los puntos de cada actividad se reparten entre las personas del equipo según las horas (H + I) que cada una registró en ella. Con las tres personas activas ({mtxt(m3[0])} a {mtxt(m3[-1])}), cada una cerró en promedio <strong>{fmt(pp_prom, 1)} puntos al mes</strong>, entre {fmt(pp_min, 1)} y {fmt(pp_max, 1)}. Un paquete es un número entero de personas × {PPP} puntos: {PK[0]}, {PK[1]} o {PK[2]} puntos para {PERS[0]}, {PERS[1]} o {PERS[2]} personas. {PPP} es la parte entera del promedio observado, no un compromiso. {fs("F1")}</p>
  {tabla('<th>Mes de cierre</th><th>Puntos del equipo</th><th>Personas con actividades cerradas</th><th>Promedio por persona</th><th>Rango entre personas</th>', pers_rows, "scenario-table")}
  <p class="diagram-caption">Antes de {mtxt(prim3)} el equipo tuvo menos de tres personas con actividades cerradas por mes, así que el promedio por persona no es comparable con el paquete. Las actividades cuyas horas son de varias personas se reparten en proporción. {fs("F1")}</p>""")
def _d(x):
    return x.strftime("%d/%m") if x else "—"


def _h(a, b):
    return fmt(dias_hab(a, b), 1) if a and b else "—"


et_rows = ""
for a in sorted(act_sep, key=lambda a: num_(a["id"])):
    t = TI[a["id"]]
    uin = [x for x, p, q in t["tr"] if q == "UAT"]
    et_rows += (f'<tr><td class="col-narrow">{tk(a["id"])}</td><td class="col-narrow">{a["dev"] if a["dev"] is not None else "—"}</td>'
                f'<td class="col-narrow">{t["rev"]}</td><td class="col-narrow">{t["uat"]}</td>'
                f'<td class="col-narrow">{_d(t["rfp"])}</td><td class="col-narrow">{_d(t["done"])}</td>'
                f'<td class="col-narrow">{_h(uin[-1], t["rfp"]) if uin else "—"}</td><td class="col-narrow">{_h(t["rfp"], t["done"])}</td></tr>')
dd = [dias_hab(TI[a["id"]]["rfp"], TI[a["id"]]["done"]) for a in act_sep if TI[a["id"]]["rfp"] and TI[a["id"]]["done"]]
more("d-etapas", "Estados en Jira y devoluciones por etapa", f"""
  <p>Flujo en Jira: To Do → In Progress → In review → UAT → Ready for prod → Done. In Progress e In review son del equipo; en In review se revisa el PR y puede devolver la actividad al equipo; en UAT se prueba tras el despliegue a prueba y también puede devolverla. Ready for prod es cuando queda lista para producción y Done, cuando se despliega en producción. {fs("F3")}</p>
  <p>De las {len(act_sep)} actividades de septiembre, {n_rfp} llegaron a Ready for prod y {n_done} a Done. Contando los retornos a In Progress o Feedback registrados en Jira: <strong>{ret_rev} desde In review</strong> y <strong>{ret_uat} desde UAT</strong> ({n_uat_ret} actividades). De Ready for prod a Done pasaron entre {fmt(min(dd), 1)} y {fmt(max(dd), 1)} días hábiles (mediana {fmt(st.median(dd), 1)}). {fs("F3")}</p>
  {tabla('<th class="col-narrow">Tarea</th><th class="col-narrow">Devoluciones (informe, K)</th><th class="col-narrow">Desde In review</th><th class="col-narrow">Desde UAT</th><th class="col-narrow">A Ready for prod</th><th class="col-narrow">A Done</th><th class="col-narrow">UAT → Ready (días háb.)</th><th class="col-narrow">Ready → Done (días háb.)</th>', et_rows)}
  <p class="diagram-caption">Fechas de septiembre u octubre de 2026 (dd/mm), historial de estados de cada actividad en Jira, leído el 9 de octubre. «Desde» cuenta los pases a In Progress o Feedback (en UAT, también a In review). El informe cuenta las devoluciones de otra forma, por eso las cifras no coinciden. {fs("F1", "F3")}</p>""")
ent_rows = "".join(
    f'<tr><td class="col-narrow">{tk(a["id"])}</td><td class="col-narrow">{a["dev"] if a["dev"] is not None else "—"}</td>'
    f'<td>{fmt(a["ej"])} / {fmt(a["g"])}&nbsp;h</td><td>{"dentro de lo estimado · +" + fmt(100 * a["j"], 0) + "&nbsp;%" if a["j"] > 0 else "dentro de lo estimado · acertó"}</td></tr>'
    for a in cumplen_dev)
more("d-entrega", "Historias entregadas dentro de lo estimado, con sus devoluciones", f"""
  <p><strong>{S["ok"]} de {S["con"]}</strong> actividades se entregaron dentro de lo estimado (hasta +30&nbsp;%); <strong>{len(ok_dev)}</strong> de ellas con devoluciones, hasta {conj_dev_max}. Las devoluciones no impidieron la entrega en el tiempo estimado. {fs("F1")}</p>
  {tabla('<th class="col-narrow">Tarea</th><th class="col-narrow">Devoluciones (K)</th><th>Ejecutadas / estimadas (H + I / G)</th><th>Resultado</th>', ent_rows)}
  <p class="diagram-caption">Las {S["con"] - S["ok"]} que no cumplieron están en el detalle de actividades de septiembre. {more("d-act", "", "ver las 26 actividades →")}</p>""")
_fe = EV["notas_de_proceso"]["formato_de_evidencia"]
more("d-n1", "Formato de evidencia de pruebas que cambia sin aviso", f"""
  <p>Del 1 al 21 de septiembre, en los comentarios de revisores de los {R["abiertos"]} PRs, solo {len(_fe["menciones_de_revisores_antes_del_21_sep"])} mencionan casos de prueba o evidencia ({pr(2484)} y {pr(2493)}) y ninguno el formato. Entre tanto, {tk("API-1738")}, {tk("API-1867")} y {tk("API-1834")} pasaron a UAT el 7, 14 y 18 de septiembre. Desde el 21 se piden formatos distintos. No consta aviso del cambio en los comentarios de los PRs; Jira y otros canales no se revisaron. {fs("F3", "F4")}</p>
  {tabla('<th class="col-narrow">PR</th><th class="col-narrow">Tarea</th><th class="col-narrow">Fecha</th><th>Pedido del revisor</th>', "".join(f'<tr><td class="col-narrow">{pr(q["pr"])}</td><td class="col-narrow">{tk(q["tarea"])}</td><td class="col-narrow">{fiso(q["fecha"])}</td><td>«{esc(q["pedido"])}»</td></tr>' for q in _fe["pedidos"]), "scenario-table")}""")
more("d-n2", "Devoluciones por estándares que una herramienta puede revisar", f"""
  <p>Pedidos de septiembre sobre nombres y código sin uso. Criterio de Tech and Solve: son comentarios mecánicos que un análisis estático como Sonar puede cubrir sin depender del revisor. Hoy {R["mergeados_con_sonar_rojo"]} de {R["mergeados"]} PRs mergeados tienen el Quality Gate en rojo y ninguna reseña lo menciona. {fs("F4")}</p>
  {tabla('<th class="col-narrow">PR</th><th class="col-narrow">Tarea</th><th class="col-narrow">Fecha</th><th>Pedido del revisor</th>', "".join(f'<tr><td class="col-narrow">{pr(q["pr"])}</td><td class="col-narrow">{tk(q["tarea"])}</td><td class="col-narrow">{fiso(q["fecha"])}</td><td>«{esc(q["pedido"])}»</td></tr>' for q in EV["notas_de_proceso"]["pedidos_mecanicos"]), "scenario-table")}""")
more("d-n3", "Alcance de las pruebas distinto en cada PR", f"""
  <p>Los pedidos sobre pruebas varían de un PR a otro: agregar casos, seguir un patrón o no tocar las pruebas existentes. Criterio de Tech and Solve: debe ser un estándar único, con todo automatizado y sin decidir en cada PR qué se automatiza. {fs("F4")}</p>
  {tabla('<th class="col-narrow">PR</th><th class="col-narrow">Tarea</th><th class="col-narrow">Fecha</th><th>Pedido del revisor</th>', "".join(f'<tr><td class="col-narrow">{pr(q["pr"])}</td><td class="col-narrow">{tk(q["tarea"])}</td><td class="col-narrow">{fiso(q["fecha"])}</td><td>«{esc(q["pedido"])}»</td></tr>' for q in EV["notas_de_proceso"]["alcance_de_pruebas"]), "scenario-table")}""")
more("d-pruebas", "Pruebas unitarias hoy", f"""<p>En la revisión del PR {pr(2488)} (11 sep) el revisor escribió: «I know we don't write them», sobre las pruebas unitarias. {fs("F3", "F4")}</p>""")
more("d-abiertas", "Actividades de septiembre que siguen abiertas", f"""<p>Al 9 de octubre de 2026: {abiertas_list}. {fs("F3")}</p>""")
more("d-terminos", "Términos", tabla("<th>Término</th><th>Qué significa</th>",
    "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td></tr>" for a, b in [
        ("Punto", "Lo que cuesta una actividad según su tamaño."),
        ("Valor del punto", "Precio que Viva Aerobus paga por cada punto de actividades con PR aprobado."),
        ("Días hábiles", "Lunes a viernes."),
        ("PR (pull request)", "Solicitud de revisión de un cambio de código antes de integrarlo."),
        ("Merge", "Integración del cambio aprobado en la rama base."),
        ("Devolución", "Solicitud de cambios del revisor sobre un PR o una tarea."),
        ("Prueba unitaria", "Prueba automática de una pieza pequeña de código."),
        ("Sonar (SonarQube)", "Herramienta que analiza el código; su Quality Gate falla si el análisis no cumple las condiciones.")])))

# ---------------------------------------------------------------- cuerpo
body = f"""<body>
<div class="page">

  <div class="cover-page">
    <div class="cover-logos"><img src="{{{{LOGO}}}}" alt="Tech and Solve" class="cover-logo-main"></div>
    <div class="eyebrow">Propuesta comercial</div>
    <h1>Pago por actividades terminadas, no por horas</h1>
    <p class="subtitle">Viva Aerobus compra puntos cada mes. Cada actividad cuesta los puntos de su tamaño y se paga cuando su PR está aprobado.</p>
    <div class="cover-meta">Viva Aerobus<br>Generic API<br><strong>Paquetes mensuales de puntos &middot; Equipo Tech and Solve &middot; Pago por actividad entregada</strong></div>
    <div class="cover-confidential">Documento confidencial. Elaborado por Tech and Solve para Viva Aerobus.</div>
  </div>

  <h2 id="dinamica" class="break-before">1. El modelo de trabajo actual y lo que se mide</h2>
  <div class="keep-together">
  <h3>Cómo se trabaja hoy</h3>
  {svg_flujo()}
  <p class="diagram-caption">Estados en Jira: In review y UAT pueden devolver la actividad al equipo; Ready for prod es cuando el equipo termina y Done, cuando se despliega. {more("d-etapas", "", "ver los estados y devoluciones por etapa →")} {more("d-pr", "", "")} {more("d-esperas", "", "ver las esperas →")}</p>
  </div>
  <div class="keep-together">
  <h3>Lo que se mide hoy, y lo que más pesa: tiempos que se desvían y devoluciones</h3>
  {svg_medicion()}
  <p class="diagram-caption">Septiembre, equipo de Generic API. El informe marca cada actividad como «Normal» o «Desviado» y registra sus devoluciones. {more("d-mide", "", "ver qué mide el informe →")}</p>
  </div>
  <div class="keep-together">
  <h3>La medición debería ser el cumplimiento en la entrega</h3>
  {svg_devoluciones()}
  <p class="diagram-caption">{len(ok_dev)} de las {len(con_dev)} actividades con devoluciones se entregaron dentro de lo estimado. {more("d-entrega", "", "ver las historias entregadas y sus devoluciones →")}</p>
  {svg_desvio()}
  <p class="diagram-caption">La desviación está en las {len(larga_rows)} actividades con espera de revisión de más de 30 días hábiles. {more("d-act", "", "ver las 26 actividades →")}</p>
  </div>
  <h3>Lo que no está bien hoy</h3>
  <blockquote><strong>Sin estándar de revisión.</strong> Cada PR puede traer pedidos distintos, y eso genera reprocesos. Por ejemplo, el formato de la evidencia de pruebas cambió sin aviso. {more("d-n1", "", "")}</blockquote>
  <blockquote><strong>Devoluciones por reglas mecánicas.</strong> Nombres y código sin uso podría revisarlos Sonar sin depender del revisor del PR. {more("d-n2", "", "")}</blockquote>
  <blockquote><strong>El alcance de las pruebas cambia.</strong> Debería ser un estándar: todo se automatiza, sin decidir caso a caso qué sí y qué no, porque eso genera reprocesos para todo el equipo. {more("d-n3", "", "")}</blockquote>

  <h2 id="funciona" class="break-before">2. Propuesta</h2>
  <div class="keep-together">
  <h3>Cómo se trabaja con la propuesta, qué se observa y qué se paga</h3>
  {svg_propuesta()}
  <p class="diagram-caption">Una actividad se paga cuando su PR está aprobado; durante el recorrido se observa el cumplimiento en la entrega, no las horas ni las devoluciones.</p>
  </div>
  <div class="keep-together">
  <h3>Lo que cambia en lo que mira Viva Aerobus</h3>
  {svg_enfoque()}
  <p class="diagram-caption">Del esfuerzo (horas y devoluciones) al cumplimiento en la entrega, y a lo que hoy genera reprocesos. {more("d-estd", "", "ver los pedidos de estandarización →")}</p>
  </div>
  <h3>Cada actividad cuesta los puntos de su tamaño</h3>
  <table class="scenario-table"><thead><tr><th class="col-narrow">Puntos</th><th>Tiempo</th><th>Ejemplo finalizado</th></tr></thead><tbody>{menu}</tbody></table>
  <p class="diagram-caption">Tiempo: horas reales + 30&nbsp;% de desviación por defecto. Una actividad de más de {LIM[-1]} h se divide antes de aceptarla. {more("d-tam", "", "cómo se calcula →")}</p>

  <h3>Se compra un paquete de puntos al mes</h3>
  <table class="scenario-table"><thead><tr><th>Paquete</th><th>Equipo</th><th>Puntos al mes</th><th>Pago máximo al mes</th><th>Horas reales (% de la capacidad)</th><th>Meses de jul-sep 2026 con estos puntos o más</th></tr></thead><tbody>{prow}</tbody></table>
  <p class="diagram-caption">Histórico: septiembre de 2025 a septiembre de 2026 (13 meses). {more("d-meses", "", "cómo salen los paquetes →")}</p>
  <p>Cada paquete es un número entero de personas por <strong>{PPP} puntos por persona al mes</strong>, la parte entera de lo que cada una cerró en promedio con las tres activas ({fmt(pp_prom, 1)}; entre {fmt(pp_min, 1)} y {fmt(pp_max, 1)}). El Inicial es el equipo que opera hoy; para más puntos se suman personas completas, de a una. {more("d-persona", "", "ver los puntos por persona →")}</p>

  <h3>Cómo se paga</h3>
  <p>Viva Aerobus paga el valor del punto por cada punto de las actividades con PR aprobado en el mes. Los puntos que Tech and Solve no entrega con PR aprobado no se pagan, y si una actividad exige más horas que el rango de su tamaño, el costo adicional es de Tech and Solve. [PENDIENTE] Definir qué pasa con los puntos que Viva Aerobus no usa por no tener tareas definidas.</p>

  <div class="keep-together">
  <h3>El recorrido de una actividad</h3>
<div class="stepper">
  <div class="step"><div class="step-dot">1</div><div class="step-title">Definición</div><p class="step-desc">Se diseña la tarea con criterios de aceptación claros, se acuerda su tamaño y se registra en Jira.</p></div>
  <div class="step"><div class="step-dot">2</div><div class="step-title">Desarrollo <span class="tag tag-fail">Bloquea</span></div><p class="step-desc">Un PR por tarea, con pruebas unitarias y análisis de Sonar. Sin pruebas, no pasa a revisión.</p></div>
  <div class="step"><div class="step-dot">3</div><div class="step-title">Revisión</div><p class="step-desc">Viva Aerobus responde en máximo dos días hábiles.</p></div>
  <div class="step"><div class="step-dot">4</div><div class="step-title">Sesión de entrega</div><p class="step-desc">Tech and Solve presenta la actividad y sus evidencias.</p></div>
  <div class="step step-edge"><div class="step-dot">{CHECK}</div><div class="step-title">PR aprobado</div><p class="step-desc">La actividad suma sus puntos al mes.</p></div>
</div>
  </div>

  <h2 id="respaldo">3. Mejoras de proceso y su respaldo en datos</h2>
  <table class="scenario-table"><thead><tr><th>Mejora propuesta</th><th>Dato real de Generic API</th></tr></thead><tbody>
  <tr><th>Tamaño en puntos, acordado antes de empezar</th><td>Septiembre: <strong>{S["ok"]} de {S["con"]}</strong> cumplieron lo estimado (agosto: {G8["ok"]} de {G8["con"]}); <strong>{resen} de 26</strong> cambiaron su estimación durante el trabajo. {more("d-acierto", "", "")}</td></tr>
  <tr><th>Revisión en máximo dos días hábiles</th><td><strong>{R["primera_revision_en_2_habiles_o_menos"]} de {R["revisados"]}</strong> PRs recibieron la primera revisión en 2 días hábiles o menos; <strong>4 de 26</strong> actividades esperaron más de 30. {more("d-esperas", "", "")}</td></tr>
  <tr><th>Revisión por cambio de la rama base = tarea nueva</th><td>Tras esperar {fmt(esp["API-1663"]["habiles"], 0)} y {fmt(esp["API-1693"]["habiles"], 0)} días hábiles, el pedido de actualizar con master trajo <strong>{tot_dev} devoluciones</strong> y +{tot_ej - tot_es}&nbsp;h. {more("d-master", "", "")}</td></tr>
  <tr><th>Cumplimiento por PR aprobado</th><td>Primera aprobación en mediana <strong>{fmt(R["mediana_hasta_aprobacion_habiles"])} días hábiles</strong>; {R["con_aprobacion"]} de {R["abiertos"]} aprobados. {more("d-pr", "", "")}</td></tr>
  <tr><th>Pruebas unitarias y Sonar como control central</th><td><strong>{R["mergeados_con_sonar_rojo"]} de {R["mergeados"]}</strong> PRs mergeados con Sonar en rojo; ninguna reseña lo menciona. {more("d-pr", "", "")}</td></tr>
  <tr><th>Diseño conjunto y rechazo si hay ambigüedad</th><td><strong>{len(EV["preguntas_de_negocio"])} PRs</strong> con preguntas de negocio dirigidas a Viva Aerobus. {more("d-preg", "", "")}</td></tr>
  <tr><th>Plantilla de PR y evidencia comunes</th><td><strong>{n_estd} PRs</strong> con pedidos distintos sobre descripción y evidencia. {more("d-estd", "", "")}</td></tr></tbody></table>

  <h2 id="compromisos">4. Compromisos de cada parte</h2>
  <h3>Tech and Solve</h3>
  <ul><li>Entregar cada actividad con las evidencias del resumen.</li><li>Elegir las pruebas unitarias que considere oportunas, si cubren los criterios de aceptación.</li></ul>
  <h3>Viva Aerobus</h3>
{kv([("Responder el PR", "Máximo dos días hábiles. Si el PR queda más tiempo sin respuesta, la actividad se cuenta como entregada en el mes."),
     ("Definir la tarea", "Criterios de aceptación claros, sin ambigüedad y con dependencias resueltas."),
     ("Cambios de alcance", "Todo cambio de alcance o control de cambios es una tarea nueva, con su propio tamaño."),
     ("Merge del PR aprobado", "Si no hace merge y luego pide revisiones porque la rama base cambió, esa revisión es una tarea nueva."),
     ("Autorizar pruebas unitarias", f"Hoy se prueba de forma manual; la propuesta agrega pruebas unitarias en cada actividad. {more('d-pruebas', '', '')}"),
     ("Acceso a Sonar", f"El resultado de SonarQube ya se publica en cada PR; Tech and Solve necesita acceso de lectura al panel. {more('d-pr', '', '')}")])}
  <p>Tech and Solve puede rechazar una actividad antes de implementarla si su tamaño no es el oportuno, no tiene criterios de aceptación claros, es ambigua o tiene dependencias sin resolver.</p>

  <h2 id="preguntas">5. Preguntas frecuentes</h2>
  <table class="scenario-table"><thead><tr><th>Pregunta</th><th>Respuesta</th></tr></thead><tbody>
  <tr><th>¿Cómo sigo el avance sin reportes de horas?</th><td>Por los puntos con PR aprobado en Jira y la sesión de entrega de cada actividad.</td></tr>
  <tr><th>¿Qué pasa si cambian las prioridades?</th><td>Una tarea sin empezar se sustituye por otra del mismo tamaño; un cambio sobre una tarea iniciada es una tarea nueva.</td></tr>
  <tr><th>¿Y si un mes necesito más puntos?</th><td>Se elige un paquete mayor. [PENDIENTE] Días de aviso para cambiar de paquete.</td></tr>
  <tr><th>¿Qué pasa con las actividades en curso?</th><td>{len(abiertas)} de las 26 actividades de septiembre siguen abiertas. {more("d-abiertas", "", "")} [PENDIENTE] Definir si se cierran con el modelo actual o entran al primer paquete.</td></tr></tbody></table>

  <h2 id="siguiente">6. Siguiente paso</h2>
  <p>Viva Aerobus elige un paquete y entrega una muestra de tareas reales del backlog; con ella se hace la primera sesión de tamaños. El valor del punto se acuerda antes de empezar. Al cierre del primer mes se comparan los tamaños con lo entregado y se ajustan si hace falta.</p>

  <h2 id="fuentes">Fuentes</h2>
  <table class="scenario-table glossary"><thead><tr><th class="col-narrow">Ref.</th><th>Fuente</th></tr></thead><tbody>
  <tr id="f1"><td class="col-narrow">F1</td><td>Informe de seguimiento de septiembre de 2026 (xlsx), hoja «Seguimiento Mes», columnas A a L</td></tr>
  <tr id="f2"><td class="col-narrow">F2</td><td>Informe de seguimiento de agosto de 2026 (xlsx), misma hoja</td></tr>
  <tr id="f3"><td class="col-narrow">F3</td><td>Jira de Viva Aerobus, proyecto API; lectura del 9 de octubre de 2026</td></tr>
  <tr id="f4"><td class="col-narrow">F4</td><td>GitHub, repositorio EzyWebwerkstaden/VivaAerobus.Generic.Api; lectura del 9 de octubre de 2026</td></tr>
  <tr id="f5"><td class="col-narrow">F5</td><td><a href="https://www.atlassian.com/agile/project-management/fibonacci-story-points">Atlassian: Fibonacci story points</a>; consultada el 9 de octubre de 2026</td></tr>
  <tr id="f6"><td class="col-narrow">F6</td><td>Jornada del equipo de Generic API: 42 horas semanales por persona (información de Tech and Solve). El informe registra 524 h en septiembre (22 días hábiles de 8 h).</td></tr></tbody></table>
  <p class="diagram-caption">Todas las cifras se calculan desde estas fuentes. {more("d-terminos", "", "términos →")}</p>

  <footer>Documento confidencial. Elaborado por Tech and Solve para Viva Aerobus. Propuesta comercial de paquetes de puntos para Generic API, octubre de 2026.</footer>
{drawers_html()}
</div>
<script>
/* Esc o seguir un enlace interno cierra los paneles «ver más» */
document.addEventListener('keydown',function(e){{ if(e.key==='Escape') document.querySelectorAll('.dr-toggle:checked').forEach(function(i){{i.checked=false;}}); }});
document.addEventListener('click',function(e){{ var a=e.target.closest&&e.target.closest('.drawer a[href^="#"]'); if(a) document.querySelectorAll('.dr-toggle:checked').forEach(function(i){{i.checked=false;}}); }});
</script>
</body>
</html>
"""

open(OUT, "w").write(head + body)
print("OK ->", os.path.abspath(OUT))
print(f"N={N} H={H} A={A} h/pt={HPP:.2f} puntos={TOTP} meses={list(zip([m[2:] for m in months], [mo[m][0] for m in months], vals))}")
print(f"min/mediana/max={lo}/{med}/{hi} paquetes={PK} meses_3_personas={cnt3} mezcla={mix} ({sum(mix.values())} act.)")
print("D:", nD, "| sin fecha:", sin_fecha, "| fecha de entrega:", n_fecha_entrega, "| excluidas:", excluidas)
print("sept:", S, "| ago:", {k: v for k, v in G8.items() if k != 'por_persona'})
