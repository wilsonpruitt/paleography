#!/bin/sh
# Phase A acceptance test: the registry refactor must not change a single byte of the
# exercise bank for the three tracks that existed before it.
#
# The refactor moves what used to be a hardcoded `specs` list in build_exercises.py into
# registry/*.toml, and then teaches the trainer to read languages, profiles and routes
# from the same place. That is a pure restructuring: same witnesses, same scorers, same
# thresholds, so the same 330 lines must come out in the same order with the same JPEGs.
#
# ⚑ What is hashed is the `tracks` OBJECT, not the whole file. The envelope around it
# grows during Phase A -- it gains `languages` and `profiles` so the trainer can stop
# hardcoding them -- and hashing the file would fail on every such addition while saying
# nothing about whether the bank moved. The bank is the invariant; the envelope is not.
#
# If this hash moves, something about SELECTION, GRADING or track METADATA changed, and
# the diff is not the refactor you thought you were making.
#
# The build is deterministic (verified 2026-08-28: two clean runs, identical sha256), so
# this is a real test and not a flaky one.
#
# Usage:  sh tools/acceptance.sh
set -e
cd "$(dirname "$0")/.."

EXPECT=b1f6db854df98d1fe9bb3a37379257977a5f0208322c360a7c4b63f619eeb016
OUT=$(mktemp -t paleography-acceptance)
trap 'rm -f "$OUT"' EXIT

python3 tools/build_exercises.py --out "$OUT" --n 110 --max-w 1700 --quality 80 >/dev/null
GOT=$(python3 -c '
import json, hashlib, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
b = json.dumps(d["tracks"], ensure_ascii=False).encode()
print(hashlib.sha256(b).hexdigest())
' "$OUT")

if [ "$GOT" = "$EXPECT" ]; then
  echo "PASS  exercise bank byte-identical  ($GOT)"
else
  echo "FAIL  exercise bank CHANGED"
  echo "  expected $EXPECT"
  echo "  got      $GOT"
  echo
  echo "If the change is deliberate (new witness, retuned scorer, different --n/--quality),"
  echo "update EXPECT above in the same commit that causes it, and say why in the message."
  exit 1
fi
