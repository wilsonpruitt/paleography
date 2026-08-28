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
# ⛔ Syriac needs the LFS filters DISABLED to clone at all. Its .gitattributes routes
# *.jpg through Git LFS, LFS is switched off on the repository (the batch API answers
# 403 "Git LFS is disabled for this repository"), and without git-lfs installed the
# checkout aborts and leaves an empty tree. These -c flags let the XML -- which is all we
# want, the plates come from ÖNB over IIIF -- check out, leaving the jpgs as pointers.
[ -d syr1 ] || git clone -q --depth 1 \
  -c filter.lfs.smudge=cat -c filter.lfs.process= -c filter.lfs.required=false \
  https://github.com/HTR-School-Vienna/2024--Syriac.git syr1
cd ../..
# Layers are DECLARED here to match corpus/sources.yml -- never inferred. See corpus/INGEST-NOTES.md
python3 tools/ingest.py corpus/raw/wien940           wien940               --layer diplomatic --out corpus/normalized/wien940.jsonl
python3 tools/ingest.py corpus/raw/cpgr23            cpgr23                --layer expanded   --out corpus/normalized/cpgr23.jsonl
python3 tools/ingest.py corpus/raw/rescribe-caroline rescribe-caroline     --layer normalised --out corpus/normalized/rescribe.jsonl
python3 tools/ingest.py corpus/raw/syr1                onb-syr1              --layer diplomatic --out corpus/normalized/onb-syr1.jsonl
for w in VLO41 Lat7499 BambergMsc30 Lat14087; do
  python3 tools/ingest.py corpus/raw/eutyches "eutyches-$w" --layer diplomatic \
    --include "/$w/GT/alto/" --out "corpus/normalized/eutyches-$w.jsonl"
done
# ⚑ onb-syr1 has NO usable images in its repo. Its plates and the rescaled coordinates
# that go with them come from ÖNB over IIIF; see corpus/sources.yml `build:` for the two
# commands, which are not run here because they fetch 28 MB from a library.
echo "seed corpus ready:"; wc -l corpus/normalized/*.jsonl | tail -1
