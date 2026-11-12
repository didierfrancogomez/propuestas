#!/usr/bin/env bash
# Regenera el PPTX editable de cliente desde el HTML:
#   1. extraer_layout.js lee la geometría de las láminas 1 a 19 -> layout.json + img/
#   2. generar_ppt.js arma ../propuesta-viva-pui-aws-v5-cliente-editable.pptx con texto y formas nativas
# La primera vez instala pptxgenjs y puppeteer-core en ppt/node_modules (usa el Chrome instalado).
set -euo pipefail
cd "$(dirname "$0")"
SKILLS="/Users/didierfranco/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/153d0a53-1e17-4eee-9796-36710d3f0086/4cd0ae1b-44f5-4a3c-9a79-316580a6b1cf/skills"
[ -d node_modules/pptxgenjs ] && [ -d node_modules/puppeteer-core ] || npm install --no-audit --no-fund pptxgenjs@3.12.0 puppeteer-core@23.11.1
NODE_PATH="$PWD/node_modules" node extraer_layout.js
NODE_PATH="$PWD/node_modules" PPTX_SKILL="$SKILLS/pptx" node generar_ppt.js
