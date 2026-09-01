#!/usr/bin/env python3
"""Emit R4 (glossary entry) records for the Nestle shard, one TOML file per head-lemma.

Per-page extraction produces a compact list of dicts; this turns them into files with the
schema of SYRIAC-LANGUAGE-PILOT.md §4, so a page's output is the READING, not the boilerplate.

    from quarry_r4 import emit
    emit(page=134, leaf="n223", entries=[ {...}, ... ])

    python3 tools/quarry_r4.py --validate     # every record parses; report counts
    python3 tools/quarry_r4.py --audit        # per-page counts + uncertainty rate

Entry keys — `slug`, `unvoc`, `voc`, `translit`, `pos`, `en` are required; everything else
optional: `de`, `sec` (Nestle's own § ref), `greek`, `hebrew`, `latin`, `plural_voc`,
`variant_voc`, `construct_voc`, `dialect_variant`, `stems`, `sub_lemmas`, `primer_note`,
`uncertain_note` (setting it sets `uncertain = true`), `see` (a bare `v. X` cross-reference),
`continues_from` (⚑ entries CROSS PAGE BOUNDARIES — file the record under the page where the
head-lemma STARTS and name the page it runs onto; a page-range shard therefore cannot begin
mid-entry, which constrains how this section can be split between agents).

⚑ `sub_lemmas` is captured as a STRING FIELD on the parent, not as its own record. That is
deliberate and reversible: the `||` ruling (MAP.md flag 2) is unmade, and a superset that can
be split later is safe where a discarded reading is not.
"""
import argparse, glob, re, sys, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "quarry" / "nestle-1889-en" / "r4"

HEADER = ("# Nestle shard, R4. Schema: SYRIAC-LANGUAGE-PILOT.md §4; model record:\n"
          "# r4/g171-neshab.toml. ⚠ Readings are extractor output — the Syriacist seat is\n"
          "# empty and the Step-3 blind control has not run.\n")

EXTRA = ("greek", "latin", "hebrew", "plural_voc", "variant_voc", "construct_voc",
         "dialect_variant", "stems", "sub_lemmas", "see", "continues_from", "primer_note")


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit(page, leaf, entries):
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for e in entries:
        for k in ("slug", "unvoc", "voc", "translit", "pos", "en"):
            if k not in e:
                raise KeyError(f"p.{page} entry {e.get('slug', '?')}: missing {k!r}")
        name = f"g{page:03d}-{e['slug']}.toml"
        L = [HEADER,
             f'id = "nestle-1889-en/r4/g{page:03d}-{e["slug"]}"',
             'record_type = "R4"',
             '',
             f'lemma = {{ unvoc = {q(e["unvoc"])}, voc = {q(e["voc"])}, translit = {q(e["translit"])} }}',
             f'pos = {q(e["pos"])}',
             f'gloss_en = {q(e["en"])}']
        if e.get("de"):
            L.append(f'gloss_de = {q(e["de"])}')
        L += ['root = ""', 'payne_smith = ""', 'frequency_rank = ""']
        if e.get("sec"):
            L.append(f'nestle_section = {q(e["sec"])}')
        L += ['noldeke = []', 'layer = "vocalized Serto"']
        for k in EXTRA:
            if e.get(k):
                L.append(f'{k} = {q(e[k])}')
        if e.get("uncertain_note"):
            L += ['uncertain = true', f'uncertain_note = {q(e["uncertain_note"])}']
        L += ['', '[source]', 'primer = "nestle-1889-en"', f'page = {page}', f'leaf = {q(leaf)}']
        p = OUT / name
        p.write_text("\n".join(L) + "\n", encoding="utf-8")
        tomllib.load(open(p, "rb"))          # never leave an unparseable record behind
        written.append(name)
    return written


def _load_all():
    recs = []
    for f in sorted(glob.glob(str(OUT / "*.toml"))):
        d = tomllib.load(open(f, "rb"))
        d["_file"] = Path(f).name
        recs.append(d)
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--unread", action="store_true", help="list records whose head-word was NOT resolved")
    a = ap.parse_args()
    recs = _load_all()
    if a.validate or not (a.audit):
        print(f"{len(recs)} R4 records, all parse")
    if a.audit:
        pages, unc = {}, 0
        for r in recs:
            pages[r["source"]["page"]] = pages.get(r["source"]["page"], 0) + 1
            unc += bool(r.get("uncertain"))
        for p in sorted(pages):
            print(f"  p.{p}: {pages[p]}")
        n = len(recs) or 1
        unread = [r for r in recs if not r["lemma"]["unvoc"]]
        print(f"pages done: {len(pages)} of 63   records: {len(recs)}   "
              f"uncertain: {unc} ({100*unc/n:.0f}%)   unread: {len(unread)}   "
              f"mean/page: {len(recs)/len(pages):.1f}")
    if a.unread:
        # ⛔ A head-word we could not read is a FINDING, not an absence. These placeholders
        # keep the page counts honest and name what has to be re-read at higher magnification.
        for r in (x for x in recs if not x["lemma"]["unvoc"]):
            print(f'  {r["_file"]:26s} p.{r["source"]["page"]} {r["source"]["leaf"]}')


if __name__ == "__main__":
    main()
