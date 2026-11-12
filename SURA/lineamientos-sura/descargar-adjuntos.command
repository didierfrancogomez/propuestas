#!/bin/bash
# Descarga las imágenes/adjuntos de los lineamientos SURA (EDA Framework y Modelo de decisión de integración)
# a las carpetas recursos/ de cada paquete, según su manifest.json.
cd "$(dirname "$0")" || exit 1
echo "== Descarga de adjuntos de Confluence (segurosti) =="
echo "Necesitas un API token de Atlassian: https://id.atlassian.com/manage-profile/security/api-tokens"
echo
read -r -p "Correo de tu cuenta Atlassian: " EMAIL
read -r -s -p "API token (no se muestra): " TOKEN; echo
export EMAIL TOKEN
python3 - <<'PY'
import json, os, subprocess
email, tok = os.environ['EMAIL'], os.environ['TOKEN']
ok = skip = err = 0
for b in ['eda-framework', 'modelo-decision-integracion']:
    m = json.load(open(os.path.join(b, 'manifest.json')))
    for p in m['paginas']:
        for a in p['adjuntos']:
            out = os.path.join(b, a['rutaLocal'])
            if os.path.exists(out) and os.path.getsize(out) == a['bytes']:
                skip += 1; continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            url = f"https://segurosti.atlassian.net/wiki/rest/api/content/{p['id']}/child/attachment/{a['id']}/download"
            r = subprocess.run(['curl', '-sS', '-L', '--fail', '-u', f'{email}:{tok}', '-o', out, url], capture_output=True, text=True)
            if r.returncode == 0:
                ok += 1; print(f"  ok  {b}/{a['rutaLocal']}")
            else:
                err += 1; print(f"  ERROR {a['archivo']}: {r.stderr.strip()}")
                if os.path.exists(out): os.remove(out)
print(f"\nDescargados: {ok} · ya existían: {skip} · errores: {err}")
PY
echo
read -r -p "Listo. Presiona Enter para cerrar."
