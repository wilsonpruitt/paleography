#!/usr/bin/env python3
"""Duplicate-gloss report for the Nestle R4 shard.

Implements the 2026-09-01 ruling: a duplicate is REAL only when BOTH gloss columns agree.
See quarry/nestle-1889-en/CONVENTIONS-duplicate-glosses.md.

    python3 tools/quarry_dupes.py            # the real pairs, and what the rule rejected
    python3 tools/quarry_dupes.py --rejected # show the single-column matches in full

⚑ The single-column list is not a backlog. It is the control group: `temple` is in it because
ܗܰܝܟܠܳܐ is Tempel and ܨܶܕܥܳܐ is Schläfe, and linking those would assert a relation that does not
exist. Requiring both columns is what keeps it out.
"""
import argparse, glob, re, tomllib, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R4 = ROOT / "quarry" / "nestle-1889-en" / "r4"

LABEL = re.compile(r'^(m|f|c|pl|adj|adv|subst|coll|do|act|pass|ethpe|ethpa|aph|pa|part|impers|'
                   r'cross-reference|.*not read.*|.*no gloss.*)\.?$', re.I)


def norm(g):
    """Strip parentheticals and leading grammatical labels; drop anything that is only a label."""
    if not g:
        return None
    g = re.sub(r'\s*\([^)]*\)', '', g.strip()).strip().rstrip('.;,')
    g = re.sub(r'^(m|f|c|pl|adj|adv|subst|coll)\.\s*', '', g, flags=re.I).strip()
    return g.lower() if len(g) > 2 and not LABEL.match(g) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rejected", action="store_true")
    a = ap.parse_args()

    recs = []
    for f in sorted(glob.glob(str(R4 / "*.toml"))):
        d = tomllib.load(open(f, "rb"))
        d["_f"] = Path(f).name
        recs.append(d)

    both, one = collections.defaultdict(list), collections.defaultdict(list)
    for r in recs:
        de, en = norm(r.get("gloss_de")), norm(r.get("gloss_en"))
        lem = r["lemma"]["voc"] or r["lemma"]["unvoc"]
        item = (r["source"]["page"], lem, r["_f"], r.get("see_also"), r.get("see"))
        if de and en:
            both[(de, en)].append(item)
        for g in (de, en):                      # single-column index, for the control group
            if g:
                one[g].append(item)

    real = {k: v for k, v in both.items() if len({x[2] for x in v}) > 1}
    print(f"REAL duplicates (both columns agree): {len(real)}\n")
    for (de, en), v in sorted(real.items(), key=lambda kv: kv[1][0][0]):
        linked = "linked" if all(x[3] for x in v) else ("NESTLE'S OWN" if any(x[4] for x in v)
                                                        else "⚠ NOT LINKED")
        print(f"  {en:22} / {de:22} [{linked}]")
        for p, lem, f, _, _ in v:
            print(f"      p{p:>3}  {lem:12} {f}")

    # Count in RECORD-PAIRS, the unit the ruling is about — not in glosses, which double-count.
    def pairs(idx):
        out = set()
        for v in idx.values():
            fs = sorted({x[2] for x in v})
            for i in range(len(fs)):
                for j in range(i + 1, len(fs)):
                    out.add((fs[i], fs[j]))
        return out

    real_pairs, one_pairs = pairs(real), pairs(one)
    rejected = one_pairs - real_pairs
    print(f"\nREJECTED — matched on ONE column only, so NOT duplicates: {len(rejected)} record-pairs")
    print(f"   ({len(one_pairs)} pairs share a gloss word at all; {len(real_pairs)} survive the both-columns test)")
    if a.rejected:
        byfile = {r["_f"]: r for r in recs}
        for x, y in sorted(rejected):
            rx, ry = byfile[x], byfile[y]
            lx = rx["lemma"]["voc"] or rx["lemma"]["unvoc"]
            ly = ry["lemma"]["voc"] or ry["lemma"]["unvoc"]
            print(f"  {lx:12} p{rx['source']['page']:>3} [{rx.get('gloss_de') or '—'} | {rx.get('gloss_en') or '—'}]")
            print(f"  {ly:12} p{ry['source']['page']:>3} [{ry.get('gloss_de') or '—'} | {ry.get('gloss_en') or '—'}]\n")
    else:
        print("   (--rejected to list them; they are the control group, not a backlog)")


if __name__ == "__main__":
    main()
