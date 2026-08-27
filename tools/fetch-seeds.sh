#!/bin/sh
# Re-fetch and re-ingest the Phase 1 seed corpus. Idempotent.
# ~2.1 GB of clones; produces corpus/normalized/*.jsonl.
set -e
cd "$(dirname "$0")/.."
mkdir -p corpus/raw corpus/normalized
cd corpus/raw
[ -d wien940 ]           || git clone -q --depth 1 https://github.com/HTR-School-Vienna/-2024--carolingian-latin.git wien940
[ -d eutyches ]          || git clone -q --depth 1 https://github.com/malamatenia/Eutyches.git eutyches
[ -d rescribe-caroline ] || git clone -q --depth 1 https://github.com/rescribe/carolineminuscule-groundtruth.git rescribe-caroline
[ -d cpgr23 ]            || git clone -q --depth 1 https://gitlab.huma-num.fr/ecrinum/anthologia/htr_cpgr23.git cpgr23
cd ../..
# Layers are DECLARED here to match corpus/sources.yml -- never inferred. See corpus/INGEST-NOTES.md
python3 tools/ingest.py corpus/raw/wien940           wien940               --layer diplomatic --out corpus/normalized/wien940.jsonl
python3 tools/ingest.py corpus/raw/cpgr23            cpgr23                --layer expanded   --out corpus/normalized/cpgr23.jsonl
python3 tools/ingest.py corpus/raw/rescribe-caroline rescribe-caroline     --layer normalised --out corpus/normalized/rescribe.jsonl
for w in VLO41 Lat7499 BambergMsc30 Lat14087; do
  python3 tools/ingest.py corpus/raw/eutyches "eutyches-$w" --layer diplomatic \
    --include "/$w/GT/alto/" --out "corpus/normalized/eutyches-$w.jsonl"
done
echo "seed corpus ready:"; wc -l corpus/normalized/*.jsonl | tail -1
