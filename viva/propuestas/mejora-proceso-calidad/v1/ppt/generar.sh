#!/usr/bin/env bash
# Regenera los PPTX editables (cliente e interno) desde generar_ppt.js.
# La primera vez instala pptxgenjs en ppt/node_modules.
set -euo pipefail
cd "$(dirname "$0")"
SKILLS="/Users/didierfranco/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/153d0a53-1e17-4eee-9796-36710d3f0086/4cd0ae1b-44f5-4a3c-9a79-316580a6b1cf/skills"
[ -d node_modules/pptxgenjs ] || npm install --no-audit --no-fund pptxgenjs@3.12.0
PPTX_SKILL="$SKILLS/pptx" BRAND_ASSETS="$SKILLS/tech-and-solve-deck/assets" node generar_ppt.js
