#!/usr/bin/env python3
"""Select, grade and package line exercises into one self-contained JSON payload.

Two things this does that the first version did not, both from Wilson's feedback of
2026-08-27 ("the example you shared is already far beyond me; I will need a lot of
steps to get there"):

1. **Difficulty is scored per track and the bank is ordered easiest-first.** Latin is
   graded on abbreviation density (a line of plain glossary words is a far gentler
   start than one bristling with suspension signs); Greek on diacritic density, since
   every Greek character is non-ASCII and that measure would be meaningless there.

2. **Every item ships its word tokens**, so the trainer can blank one word, or half,
   rather than only demanding the whole line. Recognition before recall.

Fragments are filtered out: a line carrying a structural mark, or fewer than three
words, or less than ~72% letters, is a scrap of apparatus, not a sentence to read.
"""
import json, base64, argparse, statistics, unicodedata
from pathlib import Path
from io import BytesIO
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

GLOSS = {g["char"]: g for g in
         json.loads(Path(__file__).resolve().parent.parent
                    .joinpath("corpus/abbreviation-glosses.json").read_text(encoding="utf-8"))["signs"]}

GREEK_PLAIN = set("αβγδεζηθικλμνξοπρστυφχψωςΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ ")
STRUCT = set("~⁛⋇∻※")


def latin_difficulty(t):
    """Abbreviation density dominates; length and word count trim the ordering."""
    n = len(t)
    if not n:
        return 999.0
    abbr = sum(1 for c in t if not c.isascii())
    return round(abbr / n * 100 + n * 0.35 + len(t.split()) * 1.2, 1)


def greek_difficulty(t):
    """Diacritic density dominates. 'Non-ASCII' would score every Greek line alike."""
    letters = [c for c in t if c.isalpha()]
    if not letters:
        return 999.0
    dia = sum(1 for c in letters if c not in GREEK_PLAIN)
    return round(dia / len(letters) * 40 + len(t) * 0.55 + len(t.split()) * 1.5, 1)


def is_sentence(t):
    if any(c in STRUCT for c in t):
        return False
    # Bracketed lines are ADMITTED (see manual-review/eutyches-parentheses-plate-read.md:
    # the brackets are the editors' supply where the ink is unreadable) but flagged, so the
    # trainer can show them for reading and withhold them from every stage that asks the
    # learner to type -- you cannot type letters that are not on the page.
    if len(t.split()) < 3:
        return False
    return sum(1 for c in t if c.isalpha()) / max(len(t), 1) > 0.72


def cloze_index(words):
    """Which word to blank first: the longest, so it is a word and not a particle.

    Deterministic, so a learner meeting the line twice meets the same gap.
    """
    best, bi = -1, 0
    for i, w in enumerate(words):
        core = "".join(c for c in w if c.isalpha())
        if len(core) > best:
            best, bi = len(core), i
    return bi


def pack(manifest_dir, n, max_w, quality, track, scorer):
    rows = [json.loads(l) for l in open(Path(manifest_dir) / "manifest.jsonl", encoding="utf-8")]
    rows = [r for r in rows if is_sentence(r["text"])]
    for r in rows:
        r["diff"] = scorer(r["text"])
    rows.sort(key=lambda r: r["diff"])
    # Sample evenly across the easiest 55% of the pool. Taking a flat top-n gives a
    # bank with no gradient at all (every line as easy as the first); taking the whole
    # pool puts dense elided verse in front of a beginner. This gives a real ramp
    # that still starts gently.
    pool = rows[: max(n, int(len(rows) * 0.55))]
    step = max(1, len(pool) // n)
    picked = pool[::step][:n]
    out = []
    for r in picked:
        p = Path(manifest_dir) / r["image"]
        im = Image.open(p).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, max(1, int(im.height * max_w / im.width))), Image.LANCZOS)
        buf = BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True)
        words = r["text"].split()
        seen, gl = set(), []
        for ch in r["text"]:
            if ch in GLOSS and ch not in seen:
                seen.add(ch); gl.append(GLOSS[ch])
        damaged = any(c in "()[]" for c in r["text"])
        out.append(dict(id=r["image"].rsplit(".", 1)[0][-12:], track=track, damaged=damaged,
                        text=r["text"], words=words, cloze=cloze_index(words),
                        diff=r["diff"], glosses=gl, layer=r["layer"], witness=r["witness"],
                        page=r["page"], w=im.width, h=im.height,
                        img=base64.b64encode(buf.getvalue()).decode()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--max-w", type=int, default=2200)
    ap.add_argument("--quality", type=int, default=87)
    a = ap.parse_args()
    specs = [
        ("latin", "corpus/crops/eutyches-VLO41", latin_difficulty,
         dict(name="Latin — Caroline minuscule",
              witness="Leiden, Voss. Lat. O. 41 (s. IX)",
              layer="diplomatic",
              printed="This is a glossed grammar book. The transcription keeps the scribe's abbreviation signs, so what you type is what is on the page — not what it stands for.")),
        ("greek", "corpus/crops/cpgr23", greek_difficulty,
         dict(name="Greek — Byzantine minuscule",
              witness="Heidelberg, Pal. gr. 23 (s. X)",
              layer="expanded",
              printed="An anthology of epigrams. Abbreviations are already written out, so this hand asks you to recognise letters and ligatures, nothing more.")),
    ]
    data = {"tracks": {}, "built": "2026-08-27"}
    for track, d, scorer, meta in specs:
        items = pack(d, a.n, a.max_w, a.quality, track, scorer)
        data["tracks"][track] = dict(meta=meta, items=items)
        kb = sum(len(i["img"]) for i in items) / 1024 / 1024
        print(f"  {track:6} {len(items):3} lines  {kb:.2f} MB  "
              f"difficulty {items[0]['diff']:.0f} → {items[-1]['diff']:.0f}")
    Path(a.out).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"-> {a.out}  {Path(a.out).stat().st_size/1024/1024:.2f} MB")
