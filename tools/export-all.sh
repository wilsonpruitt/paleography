#!/bin/sh
# Export the whole corpus to PAGE XML and verify every witness round-trips.
set -e
cd "$(dirname "$0")/.."
mkdir -p build/page-xml
for f in corpus/normalized/*.jsonl; do
  w=$(basename "$f" .jsonl)
  case "$w" in
    cpgr23)   root=corpus/raw/cpgr23 ;;
    rescribe) root=corpus/raw/rescribe-caroline ;;
    eutyches-*) root=corpus/raw/eutyches ;;
    *)        root="" ;;                     # wien940 has no images at all
  esac
  if [ -n "$root" ] && [ -d "$root" ]; then
    python3 tools/export_page.py "$f" "build/page-xml/$w" --image-root "$root"
  else
    python3 tools/export_page.py "$f" "build/page-xml/$w"
  fi
done
echo
echo "--- round-trip verification ---"
fail=0
for f in corpus/normalized/*.jsonl; do
  python3 tools/roundtrip_check.py "$f" | grep -E "round-trip:|FAIL|characters" || fail=1
done
[ "$fail" = 0 ] && echo "ALL WITNESSES ROUND-TRIP CLEAN"
