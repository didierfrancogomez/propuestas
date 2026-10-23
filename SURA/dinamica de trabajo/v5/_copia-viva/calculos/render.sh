#!/bin/bash
# Captura la presentación (láminas apiladas, como la de referencia) y recorta una PNG por lámina.
# Uso: render.sh archivo.html salida_dir   (requiere Python con Pillow en $PY o python3)
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$2"; rm -f "$2"/s*.png
N=$(grep -o '<section class="slide' "$1" | wc -l | tr -d ' ')
H=$((24 + N * 744 + 60))
"$C" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=5000 --window-size=1334,$H --screenshot="$2/_todo.png" "file://$(cd "$(dirname "$1")" && pwd)/$(basename "$1")" >/dev/null 2>&1
"${PY:-python3}" - "$2" "$N" <<'PYEOF'
import sys
from PIL import Image
d, n = sys.argv[1], int(sys.argv[2])
im = Image.open(f"{d}/_todo.png"); x = (im.size[0] - 1280) // 2
for i in range(n):
    y = 24 + i * 744
    im.crop((x, y, x + 1280, y + 720)).save(f"{d}/s{i + 1:02d}.png")
PYEOF
ls "$2"/s*.png | wc -l
