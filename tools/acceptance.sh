#!/bin/sh
# Acceptance test: adding or changing a language must not disturb any OTHER language's
# exercise bank.
#
# Originally this hashed the whole bank, which was right while the question was "did the
# Phase A refactor move anything?" It is wrong now: adding Old French changed the
# whole-bank hash and failed the test while every pre-existing track was byte-identical.
# A test that cries wolf on the project's normal event gets switched off, so it hashes
# each track SEPARATELY:
#
#   - a track listed below whose hash moved  -> FAIL, something changed that should not have
#   - a track not listed below               -> NEW, reported and not failed
#   - a listed track that has vanished       -> FAIL, it was removed or renamed
#
# When you deliberately change a track (new witness, retuned scorer, different --n or
# --quality), update its line here in the same commit and say why in the message.
#
# The build is deterministic (verified 2026-08-28: two clean runs, identical sha256).
#
# Usage:  sh tools/acceptance.sh
set -e
cd "$(dirname "$0")/.."

# track  sha256-of-t-<track>.json
KNOWN="
latin     6c6672f00b763b1e6b42e599c6d599976b35912d796c58ea03da087fd5b0d637
latin2    536d301cae8ba837a789407bb57a52b6554fd901a6143651e8524cce408f3cfa
greek     0ab1d7a1cec738774e1f6e4e54382c654a95d131956e74ee5300e1d44d50e089
fabliaux  81a99a03bf7cd267bd875c139b369f4ac6d488ed6ffcec599de51b3f9f5bb091
syriac1   6338c8dc2a6d1817d89638b6902ff5b1e74ec88b5077337d44e5728751a631ad
"

OUT=$(mktemp -d -t paleography-acceptance)
trap 'rm -rf "$OUT"' EXIT
python3 tools/build_exercises.py --out "$OUT" --n 110 --max-w 1700 --quality 80 >/dev/null

python3 - "$OUT" <<'PY'
import hashlib, subprocess, sys
from pathlib import Path

d = Path(sys.argv[1])
known = {}
for line in subprocess.run(["sh", "-c", 'sed -n "/^KNOWN=/,/^\\"$/p" tools/acceptance.sh'],
                           capture_output=True, text=True).stdout.splitlines():
    parts = line.split()
    if len(parts) == 2 and len(parts[1]) == 64:
        known[parts[0]] = parts[1]

found = {p.stem[2:]: hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest()
         for p in sorted(d.glob("t-*.json"))}

fail = False
for t, want in known.items():
    if t not in found:
        print(f"FAIL  {t}: track is GONE (removed or renamed)"); fail = True
    elif found[t] != want:
        print(f"FAIL  {t}: bank CHANGED\n        expected {want}\n        got      {found[t]}")
        fail = True
    else:
        print(f"PASS  {t}: byte-identical")
for t in found:
    if t not in known:
        print(f"NEW   {t}: {found[t]}\n        -> add this line to KNOWN in tools/acceptance.sh "
              f"once the track is settled")
sys.exit(1 if fail else 0)
PY
