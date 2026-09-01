#!/bin/sh
# Fetch Nestle glossary leaves and cut each into two readable halves.
#
#   sh tools/quarry_fetch.sh 239 240 241 242
#
# Why halves: the whole page at the scan's 1598x2604 is NOT reliably readable
# for pointed Serto. Two crops at 1.75x are, and cost ~6.5k vision tokens per
# page against ~2k for a useless whole-page read. Measured, not guessed —
# research/syriac-pilot-phase1-calibration.md.
#
# Leaf n = printed page + 89 for the whole second sequence. Glossary = n222-n284.
# Deletes the full page after cropping: this Mac runs with ~100 MB free.
set -e
DIR="${QUARRY_IMG:-$TMPDIR/nestle-img}"
mkdir -p "$DIR"
for n in "$@"; do
  [ -f "$DIR/n${n}_a.jpg" ] && continue
  curl -sL "https://archive.org/download/syriacgrammarwit00nestiala/page/n${n}.jpg" -o "$DIR/n${n}.jpg"
  DIR="$DIR" python3 - "$n" <<'PY'
import os, sys
from PIL import Image
n = sys.argv[1]; d = os.environ["DIR"]
im = Image.open(f"{d}/n{n}.jpg"); w, h = im.size
for tag, (a, b) in {"a": (0.05, 0.55), "b": (0.52, 1.00)}.items():
    c = im.crop((int(w*0.02), int(h*a), int(w*0.99), int(h*b)))
    c = c.resize((int(c.width*1.75), int(c.height*1.75)), Image.LANCZOS)
    c.save(f"{d}/n{n}_{tag}.jpg", quality=92)
im.close()
PY
  rm -f "$DIR/n${n}.jpg"
  echo "  n${n} -> ${DIR}/n${n}_a.jpg  n${n}_b.jpg"
done
