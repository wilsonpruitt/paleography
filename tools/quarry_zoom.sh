#!/bin/sh
# Zoom one horizontal band of a Nestle leaf, for lines the 1.75x half-crop cannot carry.
#
#   sh tools/quarry_zoom.sh 239 0.62 0.78        # leaf, top frac, bottom frac (of the WHOLE page)
#
# Use sparingly: a band costs vision tokens on top of the page's two halves. It exists for
# the head-words that would otherwise become "⛔ NOT READ" records (shard convention 5).
# Writes $TMPDIR/nestle-img/n<leaf>_z.jpg and deletes the full page again.
set -e
DIR="${QUARRY_IMG:-$TMPDIR/nestle-img}"
mkdir -p "$DIR"
n="$1"; TOP="$2"; BOT="$3"
curl -sL "https://archive.org/download/syriacgrammarwit00nestiala/page/n${n}.jpg" -o "$DIR/n${n}.jpg"
DIR="$DIR" TOP="$TOP" BOT="$BOT" python3 - "$n" <<'PY'
import os, sys
from PIL import Image
n = sys.argv[1]; d = os.environ["DIR"]
top, bot = float(os.environ["TOP"]), float(os.environ["BOT"])
im = Image.open(f"{d}/n{n}.jpg"); w, h = im.size
c = im.crop((int(w*0.02), int(h*top), int(w*0.99), int(h*bot)))
c = c.resize((int(c.width*3.0), int(c.height*3.0)), Image.LANCZOS)
c.save(f"{d}/n{n}_z.jpg", quality=94)
im.close()
print(f"  n{n} [{top}-{bot}] -> {d}/n{n}_z.jpg  {c.size}")
PY
rm -f "$DIR/n${n}.jpg"
