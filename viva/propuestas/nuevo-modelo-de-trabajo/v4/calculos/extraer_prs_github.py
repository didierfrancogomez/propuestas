#!/usr/bin/env python3
"""Recalcula desde GitHub (solo lectura, gh CLI) la parte de PRs de evidencia.json.

Uso:  python3 extraer_prs_github.py [salida.json]
Requiere `gh` autenticado con acceso de lectura a EzyWebwerkstaden/VivaAerobus.Generic.Api.
Calcula, para los PRs abiertos en septiembre de 2026 por el equipo (Daniel, Gabriel y Luis):
  - primera reseña de un revisor y su espera en días hábiles (lunes a viernes, UTC, fraccionarios);
  - solicitudes de cambio (reseñas CHANGES_REQUESTED) y primera aprobación;
  - merge y resultado de SonarQube (comentario del bot: Quality Gate y issues nuevos);
  - reseñas y comentarios de terceros (ni equipo ni bots) y cuántos mencionan Sonar / Quality Gate.
No escribe nada en GitHub.
"""
import json, re, subprocess, sys, datetime, statistics as st

REPO = "EzyWebwerkstaden/VivaAerobus.Generic.Api"
EQUIPO = {"gabrielherrera-tas", "DLlano-VA", "guillermoplus"}     # logins de GitHub del equipo
DESDE, HASTA = "2026-09-01", "2026-09-30"


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[:300])
    return r.stdout


def api(path):
    out = gh("api", "--paginate", path)
    return json.loads(out) if out.strip() else []


def P(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def dias_habiles(a, b):
    if b <= a:
        return 0.0
    tot, cur = 0.0, a
    while cur < b:
        nxt = min(b, (cur + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
        if cur.weekday() < 5:
            tot += (nxt - cur).total_seconds() / 86400
        cur = nxt
    return tot


lista = json.loads(gh("pr", "list", "--repo", REPO, "--state", "all", "--search", f"created:{DESDE}..{HASTA}",
                      "--limit", "300", "--json", "number,author"))
numeros = sorted(p["number"] for p in lista if p["author"]["login"] in EQUIPO)

filas, terceros, menciones = [], 0, 0
for n in numeros:
    p = json.loads(gh("pr", "view", str(n), "--repo", REPO, "--json",
                      "number,title,createdAt,mergedAt,reviews"))
    inline = api(f"repos/{REPO}/pulls/{n}/comments?per_page=100")
    conv = api(f"repos/{REPO}/issues/{n}/comments?per_page=100")
    creado = P(p["createdAt"])
    rv = sorted([r for r in p["reviews"] if r["author"]["login"] not in EQUIPO and r.get("submittedAt")],
                key=lambda r: r["submittedAt"])
    primera = P(rv[0]["submittedAt"]) if rv else None
    aprob = [P(r["submittedAt"]) for r in rv if r["state"] == "APPROVED"]
    bots = [c for c in conv if "sonarqube" in c["user"]["login"].lower()]
    cuerpo = bots[-1]["body"] if bots else ""
    m = re.search(r"\[(\d+) New issues?\]", cuerpo)
    items = ([("rv", r["author"]["login"], r.get("body") or "") for r in p["reviews"]]
             + [("in", c["user"]["login"], c.get("body") or "") for c in inline]
             + [("cv", c["user"]["login"], c.get("body") or "") for c in conv])
    for _, login, body in items:
        if login in EQUIPO or "bot" in login.lower():
            continue
        terceros += 1
        if re.search(r"sonar|quality ?gate", body, re.I):
            menciones += 1
    filas.append({
        "pr": n, "tarea": "API-" + re.search(r"API[- ](\d+)", p["title"]).group(1),
        "abierto": p["createdAt"][:10],
        "primera_revision": primera.date().isoformat() if primera else None,
        "espera_primera_revision_habiles": round(dias_habiles(creado, primera), 1) if primera else None,
        "solicitudes_de_cambio": sum(1 for r in rv if r["state"] == "CHANGES_REQUESTED"),
        "primera_aprobacion": min(aprob).date().isoformat() if aprob else None,
        "espera_hasta_aprobacion_habiles": round(dias_habiles(creado, min(aprob)), 1) if aprob else None,
        "merge": p["mergedAt"][:10] if p["mergedAt"] else None,
        "espera_hasta_merge_habiles": round(dias_habiles(creado, P(p["mergedAt"])), 1) if p["mergedAt"] else None,
        "sonar": {"estado": "rojo" if "Quality Gate failed" in cuerpo else "verde",
                  "issues_nuevos": int(m.group(1)) if m else 0},
    })

rev = [f for f in filas if f["espera_primera_revision_habiles"] is not None]
mer = [f for f in filas if f["merge"]]
apr = [f for f in filas if f["primera_aprobacion"]]
resumen = {
    "abiertos": len(filas), "mergeados": len(mer), "revisados": len(rev),
    "mediana_primera_revision_habiles": st.median(f["espera_primera_revision_habiles"] for f in rev),
    "primera_revision_en_2_habiles_o_menos": sum(1 for f in rev if f["espera_primera_revision_habiles"] <= 2),
    "solicitudes_de_cambio": sum(f["solicitudes_de_cambio"] for f in rev),
    "solicitudes_por_pr": round(sum(f["solicitudes_de_cambio"] for f in rev) / len(rev), 2),
    "aprobados_sin_solicitudes": sum(1 for f in rev if f["solicitudes_de_cambio"] == 0 and f["primera_aprobacion"]),
    "con_aprobacion": len(apr),
    "mediana_hasta_aprobacion_habiles": st.median(f["espera_hasta_aprobacion_habiles"] for f in apr),
    "max_hasta_aprobacion_habiles": max(f["espera_hasta_aprobacion_habiles"] for f in apr),
    "mediana_hasta_merge_habiles": st.median(f["espera_hasta_merge_habiles"] for f in mer),
    "mergeados_con_sonar_rojo": sum(1 for f in mer if f["sonar"]["estado"] == "rojo"),
    "issues_en_mergeados_con_sonar_rojo": sum(f["sonar"]["issues_nuevos"] for f in mer if f["sonar"]["estado"] == "rojo"),
    "resenas_y_comentarios_de_terceros_revisados": terceros, "menciones_de_sonar_por_terceros": menciones,
}
salida = {"prs_septiembre": filas, "resumen_prs": resumen}
destino = sys.argv[1] if len(sys.argv) > 1 else None
if destino:
    json.dump(salida, open(destino, "w"), ensure_ascii=False, indent=1)
print(json.dumps(resumen, ensure_ascii=False, indent=1))
