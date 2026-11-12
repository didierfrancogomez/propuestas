#!/usr/bin/env bash
# Genera las dos versiones del deck desde draft.html:
#   propuesta-mejora-proceso-calidad-para-cliente-v3.html          -> para el cliente (sin slides internas)
#   propuesta-mejora-proceso-calidad-uso-interno-no-enviar-v3.html  -> uso interno de Tech and Solve (con todas)
# Las slides internas van entre <!-- INTERNO-INICIO --> y <!-- INTERNO-FIN --> en draft.html.
set -euo pipefail
cd "$(dirname "$0")"
SKILL="/Users/didierfranco/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/153d0a53-1e17-4eee-9796-36710d3f0086/4cd0ae1b-44f5-4a3c-9a79-316580a6b1cf/skills/tech-and-solve-deck/scripts"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 - draft.html "$TMP/cliente.html" <<'EOF'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
s, n = re.subn(r"<!-- INTERNO-INICIO.*?<!-- INTERNO-FIN -->\n*", "", s, flags=re.S)
open(sys.argv[2], "w", encoding="utf-8").write(s)
print(f"Slides internas quitadas de la versión cliente: {n}")
EOF

python3 "$SKILL/embed_assets.py" "$TMP/cliente.html" propuesta-mejora-proceso-calidad-para-cliente-v3.html
python3 "$SKILL/embed_assets.py" draft.html propuesta-mejora-proceso-calidad-uso-interno-no-enviar-v3.html
python3 "$SKILL/check_brand_compliance.py" propuesta-mejora-proceso-calidad-para-cliente-v3.html
python3 "$SKILL/check_brand_compliance.py" propuesta-mejora-proceso-calidad-uso-interno-no-enviar-v3.html

# PDF de la versión cliente (una página 1280x720 por slide, usando los estilos de impresión del HTML)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=5000 \
  --print-to-pdf="$PWD/propuesta-mejora-proceso-calidad-para-cliente-v3.pdf" \
  "file://$PWD/propuesta-mejora-proceso-calidad-para-cliente-v3.html" 2>/dev/null
echo "PDF: propuesta-mejora-proceso-calidad-para-cliente-v3.pdf"
