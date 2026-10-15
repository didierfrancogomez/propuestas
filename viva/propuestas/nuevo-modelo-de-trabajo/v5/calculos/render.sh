#!/bin/bash
# Renderiza cada diapositiva a PNG (1280x720) para revisión visual. Uso: render.sh archivo.html salida_dir
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$2"
N=$(grep -o 'class="slide"' "$1" | wc -l | tr -d ' ')
for i in $(seq 1 $N); do
  "$C" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=4000 --window-size=1280,720 --screenshot="$2/s$(printf %02d $i).png" "file://$(cd "$(dirname "$1")" && pwd)/$(basename "$1")#$i" >/dev/null 2>&1
done
ls "$2" | wc -l
