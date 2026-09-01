#!/usr/bin/env python3
"""Emit R4 (glossary entry) records for the Nestle shard, one TOML file per head-lemma.

Per-page extraction produces a compact list of dicts; this turns them into files with the
schema of SYRIAC-LANGUAGE-PILOT.md §4, so a page's output is the READING, not the boilerplate.

    from quarry_r4 import emit
    emit(page=134, leaf="n223", entries=[ {...}, ... ])

    python3 tools/quarry_r4.py --validate     # every record parses; report counts
    python3 tools/quarry_r4.py --audit        # per-page counts + uncertainty rate

Entry keys — `slug`, `unvoc`, `voc`, `translit`, `pos`, `en` are required; everything else
optional: `de`, `sec` (Nestle's own § ref), `greek`, `hebrew`, `arabic`, `latin`, `plural_voc`,
`variant_voc`, `construct_voc`, `dialect_variant`, `stems`, `sub_lemmas`, `primer_note`,
`uncertain_note` (setting it sets `uncertain = true`), `see` (a bare `v. X` cross-reference),
`continues_from` (⚑ entries CROSS PAGE BOUNDARIES — file the record under the page where the
head-lemma STARTS and name the page it runs onto; a page-range shard therefore cannot begin
mid-entry, which constrains how this section can be split between agents).

⚑ `sub_lemmas` is a STRUCTURED ARRAY on the parent, not its own record — Wilson's ruling,
2026-09-01. Each item is `{voc, gloss_en, gloss_de | gloss, raw}`. It stays on the parent
because the parent-child link is a claim Nestle actually makes (his ordering is by root), and
promoting an array to separate records later is mechanical where merging them back is not.
Pass a list of dicts, or a legacy `‖`-separated string, which is parsed on the way in.
⚑ Every item keeps `raw`, the piece verbatim: the parse is a convenience, not the record.
"""
import argparse, glob, re, sys, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "quarry" / "nestle-1889-en" / "r4"

HEADER = ("# Nestle shard, R4. Schema: SYRIAC-LANGUAGE-PILOT.md §4; model record:\n"
          "# r4/g171-neshab.toml. ⚠ Readings are extractor output — the Syriacist seat is\n"
          "# empty and the Step-3 blind control has not run.\n")

EXTRA = ("greek", "latin", "hebrew", "arabic", "plural_voc", "variant_voc", "construct_voc",
         "dialect_variant", "stems", "see", "continues_from", "primer_note")

SYR = "\u0700-\u074f\u0730-\u074a"   # Syriac block incl. the vowel points and seyame


def parse_sub_lemmas(s):
    """Split a legacy `‖`-separated sub-lemma string into structured items.

    Convention, verified across all 88 legacy records before converting: the leading run of
    Syriac is the form(s); the gloss that follows is ENGLISH first, GERMAN second, separated
    by ' | '. Nestle himself prints German first; these records reverse him, consistently.
    ⚑ `raw` keeps the piece verbatim, so a mis-parse costs nothing.
    ⚠ Known and accepted: a leading grammatical abbreviation ('f.', 'pl.', 'impf. u') stays at
    the head of `gloss_en` rather than being lifted into its own field, and an inflected form
    printed mid-gloss stays inside the gloss. Both are recoverable from `raw`; neither is worth
    a fragile regex now.
    """
    import re
    out = []
    for piece in (x.strip() for x in s.split("\u2016")):
        if not piece:
            continue
        m = re.match(rf"^([{SYR}\s,;\u0323\u0307]+)(.*)$", piece, re.S)
        voc, rest = (m.group(1).strip(" ,;"), m.group(2).strip()) if m else ("", piece)
        item = {"voc": voc, "raw": piece}
        if " | " in rest:
            en, de = rest.split(" | ", 1)
            item["gloss_en"], item["gloss_de"] = en.strip(), de.strip()
        elif rest:
            item["gloss"] = rest
        out.append(item)
    return out


def _sub_items(v):
    """Normalise whatever `sub_lemmas` was passed as into a list of dicts.

    ⛔ Added 2026-09-01, after `emit` was found to DROP `sub_lemmas` silently. The ruling
    that made it a structured array converted the 88 legacy records but never taught the
    writer the new shape, so p. 150 — the first page emitted after the ruling — came out
    with 15 sub-lemmas missing and every other field intact. A schema change has two ends.
    """
    if not v:
        return []
    if isinstance(v, str):
        return parse_sub_lemmas(v)
    return [parse_sub_lemmas(x)[0] if isinstance(x, str) else x for x in v]


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit(page, leaf, entries):
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    # ⛔ THE ROOT CAUSE of three defects (sub_lemmas dropped, p. 150; continues_from
    # buried in a sub-table, p. 177; `root` silently discarded on all 874 records,
    # found 2026-09-01). In every case a key was handed to `emit` and went nowhere,
    # quietly. An unknown key is now FATAL — the writer must know every field it is
    # given, or say so. A schema change has two ends; this is the second one.
    KNOWN = {"slug", "unvoc", "voc", "translit", "pos", "en", "de", "sec", "root",
             "sub_lemmas", "uncertain_note", *EXTRA}
    for e in entries:
        for k in ("slug", "unvoc", "voc", "translit", "pos", "en"):
            if k not in e:
                raise KeyError(f"p.{page} entry {e.get('slug', '?')}: missing {k!r}")
        unknown = set(e) - KNOWN
        if unknown:
            raise KeyError(f"p.{page} entry {e['slug']}: unknown key(s) {sorted(unknown)} "
                           f"— `emit` would have dropped these silently. Add them to EXTRA "
                           f"and to the writer, or remove them.")
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
        L += [f'root = {q(e.get("root", ""))}', 'payne_smith = ""', 'frequency_rank = ""']
        if e.get("sec"):
            L.append(f'nestle_section = {q(e["sec"])}')
        L += ['noldeke = []', 'layer = "vocalized Serto"']
        for k in EXTRA:
            if e.get(k):
                L.append(f'{k} = {q(e[k])}')
        if e.get("uncertain_note"):
            L += ['uncertain = true', f'uncertain_note = {q(e["uncertain_note"])}']
        for item in _sub_items(e.get("sub_lemmas")):
            L += ['', '[[sub_lemmas]]', f'voc = {q(item.get("voc", ""))}']
            for k in ("gloss_en", "gloss_de", "gloss"):
                if item.get(k):
                    L.append(f'{k} = {q(item[k])}')
            L.append(f'raw = {q(item.get("raw", ""))}')
        L += ['', '[source]', 'primer = "nestle-1889-en"', f'page = {page}', f'leaf = {q(leaf)}']
        p = OUT / name
        p.write_text("\n".join(L) + "\n", encoding="utf-8")
        back = tomllib.load(open(p, "rb"))   # never leave an unparseable record behind
        n_in, n_out = len(_sub_items(e.get("sub_lemmas"))), len(back.get("sub_lemmas", []))
        if n_in != n_out:                    # the p.150 defect, made loud
            raise ValueError(f"{name}: {n_in} sub-lemmas passed, {n_out} written")
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
    ap.add_argument("--remaining", action="store_true", help="print the pages still to do, and their leaves")
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
        subs = sum(len(r.get("sub_lemmas", [])) for r in recs)
        unread = [r for r in recs if not r["lemma"]["unvoc"]]
        print(f"pages done: {len(pages)} of 63   records: {len(recs)}   "
              f"uncertain: {unc} ({100*unc/n:.0f}%)   unread: {len(unread)}   "
              f"mean/page: {len(recs)/len(pages):.1f}")
        print(f"lemmas: {len(recs)} head + {subs} sub = {len(recs)+subs}   "
              f"({(len(recs)+subs)/len(pages):.1f}/page  \u2192 ~{round((len(recs)+subs)/len(pages)*63/10)*10} for the glossary)")
    if a.remaining:
        done = {r["source"]["page"] for r in recs}
        todo = [p for p in range(133, 196) if p not in done]
        if not todo:
            # ✅ The shard finished 2026-09-01. Every page pp. 133-195 is extracted;
            # `--audit` is the live number from here on, and the next gate is the
            # Step-3 blind control, not more extraction.
            print("✅ 0 pages left of 63 — the R4 shard is COMPLETE (pp. 133-195).")
            print("   Next: `--audit` for the counts, `--unread` for the 16 open readings,")
            print("   and the Step-3 blind control. Do NOT re-run extraction.")
            return
        print(f"{len(todo)} pages left of 63.  leaf = page + 89")
        runs, start = [], todo[0]
        for i, p in enumerate(todo):
            if i + 1 == len(todo) or todo[i+1] != p + 1:
                runs.append((start, p)); start = todo[i+1] if i + 1 < len(todo) else None
        for lo, hi in runs:
            print(f"  pp. {lo}-{hi}   leaves n{lo+89}-n{hi+89}   ({hi-lo+1} pages)")
        nxt = todo[:6]
        print("  next batch:  sh tools/quarry_fetch.sh " + " ".join(str(p+89) for p in nxt))
    if a.unread:
        # ⛔ A head-word we could not read is a FINDING, not an absence. These placeholders
        # keep the page counts honest and name what has to be re-read at higher magnification.
        for r in (x for x in recs if not x["lemma"]["unvoc"]):
            print(f'  {r["_file"]:26s} p.{r["source"]["page"]} {r["source"]["leaf"]}')


if __name__ == "__main__":
    main()
