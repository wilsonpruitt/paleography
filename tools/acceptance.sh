#!/bin/sh
# Phase A acceptance test: the registry refactor must not change a single byte of the
# exercise bank for the three tracks that existed before it.
#
# The refactor moves what used to be a hardcoded `specs` list in build_exercises.py into
# registry/*.toml. That is a pure restructuring: same witnesses, same scorers, same
# thresholds, so the same 330 lines must come out in the same order with the same JPEGs.
# If this hash moves, something about SELECTION or GRADING changed and the diff is not
# the refactor you thought you were making.
#
# The build is deterministic (verified 2026-08-28: two clean runs, identical sha256), so
# this is a real test and not a flaky one.
#
# Usage:  sh tools/acceptance.sh
set -e
cd "$(dirname "$0")/.."

EXPECT=25087261c3228aa9aec27cf10a8de687998135205e0bedfd83340ab58036d8eb
OUT=$(mktemp -t paleography-acceptance)
trap 'rm -f "$OUT"' EXIT

python3 tools/build_exercises.py --out "$OUT" --n 110 --max-w 1700 --quality 80 >/dev/null
GOT=$(shasum -a 256 "$OUT" | awk '{print $1}')

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
