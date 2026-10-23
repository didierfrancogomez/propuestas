#!/bin/bash
# Regenera el borrador, embebe los logos, chequea la marca y renderiza PNGs. Uso: rebuild.sh [dir_png]
cd "$(dirname "$0")/.." || exit 1
B="/Users/didierfranco/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/153d0a53-1e17-4eee-9796-36710d3f0086/4cd0ae1b-44f5-4a3c-9a79-316580a6b1cf/skills/tech-and-solve-deck"
python3 calculos/build_v5.py calculos/deck-borrador.html || exit 1
python3 "$B/scripts/embed_assets.py" calculos/deck-borrador.html tech-and-solve-propuesta-paquetes-de-actividades.html >/dev/null
python3 "$B/scripts/check_brand_compliance.py" tech-and-solve-propuesta-paquetes-de-actividades.html | sed -n 3,12p
[ -n "$1" ] && calculos/render.sh tech-and-solve-propuesta-paquetes-de-actividades.html "$1"
