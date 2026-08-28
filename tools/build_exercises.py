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
import json, base64, argparse, statistics, unicodedata, re, sys
from pathlib import Path
from io import BytesIO
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent

GLOSS = {g["char"]: g for g in
         json.loads(Path(__file__).resolve().parent.parent
                    .joinpath("corpus/abbreviation-glosses.json").read_text(encoding="utf-8"))["signs"]}

def abbreviation_density(t, prof):
    """Abbreviation density dominates; length and word count trim the ordering.

    Counts non-ASCII characters as a proxy for abbreviation signs. That proxy is only
    valid for a script whose ordinary letters ARE ascii -- see diacritic_density.
    """
    n = len(t)
    if not n:
        return 999.0
    abbr = sum(1 for c in t if not c.isascii())
    return round(abbr / n * 100 + n * 0.35 + len(t.split()) * 1.2, 1)


def diacritic_density(t, prof):
    """Diacritic density dominates. 'Non-ASCII' would score every Greek line alike."""
    plain = set(prof["plain_letters"])
    letters = [c for c in t if c.isalpha()]
    if not letters:
        return 999.0
    dia = sum(1 for c in letters if c not in plain)
    return round(dia / len(letters) * 40 + len(t) * 0.55 + len(t.split()) * 1.5, 1)


# A profile names its scorer; adding a script means adding a function here and one
# line of TOML, not editing a hardcoded list of tracks.
SCORERS = {
    "abbreviation_density": abbreviation_density,
    "diacritic_density": diacritic_density,
}


def is_sentence(t, prof):
    if any(c in set(prof["structural"]) for c in t):
        return False
    # Bracketed lines are ADMITTED (see manual-review/eutyches-parentheses-plate-read.md:
    # the brackets are the editors' supply where the ink is unreadable) but flagged, so the
    # trainer can show them for reading and withhold them from every stage that asks the
    # learner to type -- you cannot type letters that are not on the page.
    if len(t.split()) < prof["min_words"]:
        return False
    # Transkribus editorial marks typed as literal text and then escaped into the TEI:
    # `di<del>f</del>ficile`, `<add>no</add>`. 59 lines in Cod. 940. They are notes ABOUT
    # the text rather than the text, and a learner cannot type them.
    if "<" in t or ">" in t:
        return False
    # A combining mark is part of a letter, not a non-letter. Counting it as junk made
    # this filter throw away the most heavily abbreviated lines -- the ones a diplomatic
    # track exists to teach. Off by default so the Caroline tracks are untouched; see
    # registry/profiles/latin-gothic.toml for the evidence.
    if prof.get("count_marks_as_letters"):
        n = sum(1 for c in t if c.isalpha() or unicodedata.combining(c))
    else:
        n = sum(1 for c in t if c.isalpha())
    return n / max(len(t), 1) > prof["letter_ratio"]


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


GLOSS_FREQ = {}          # filled per track in pack(): how many lines each gloss fires on


def pack(manifest_dir, n, max_w, quality, track, prof):
    scorer = SCORERS[prof["scorer"]]
    rows = [json.loads(l) for l in open(Path(manifest_dir) / "manifest.jsonl", encoding="utf-8")]
    rows = [r for r in rows if is_sentence(r["text"], prof)]
    for r in rows:
        r["diff"] = scorer(r["text"], prof)
    rows.sort(key=lambda r: r["diff"])
    # Sample evenly across the easiest 55% of the pool. Taking a flat top-n gives a
    # bank with no gradient at all (every line as easy as the first); taking the whole
    # pool puts dense elided verse in front of a beginner. This gives a real ramp
    # that still starts gently.
    pool = rows[: max(n, int(len(rows) * 0.55))]
    step = max(1, len(pool) // n)
    picked = pool[::step][:n]
    # count how often each gloss would fire across the selection, so the cap keeps the rare
    GLOSS_FREQ.clear()
    for r in picked:
        seen = set()
        if r.get("initial"):
            seen.add("INITIAL")
        for ch in r["text"]:
            if ch in GLOSS:
                seen.add(ch)
        for g in GLOSS.values():
            if g.get("trigger") and re.search(g["trigger"], r["text"]):
                seen.add(g["char"])
        for k in seen:
            GLOSS_FREQ[k] = GLOSS_FREQ.get(k, 0) + 1
    out = []
    for r in picked:
        p = Path(manifest_dir) / r["image"]
        im = Image.open(p).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, max(1, int(im.height * max_w / im.width))), Image.LANCZOS)
        buf = BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True)
        words = r["text"].split()
        seen, gl = set(), []
        if r.get("initial") and "INITIAL" in GLOSS:
            gl.append(GLOSS["INITIAL"])
        for ch in r["text"]:
            if ch in GLOSS and ch not in seen:
                seen.add(ch); gl.append(GLOSS[ch])
        # Regex triggers exist because an EXPANDED transcription has, by definition, edited
        # out the very signs a learner needs explained: Cod. 940 has 0 literal "&" in 7,641
        # lines, though the scribe writes it constantly. A character trigger can never fire
        # on a sign the editors resolved, so those glosses key on the expanded spelling.
        for g in GLOSS.values():
            if g.get("trigger") and g["char"] not in seen:
                if re.search(g["trigger"], r["text"]):
                    seen.add(g["char"]); gl.append(g)
        # Which characters mean "the editors supplied this, the ink does not have it".
        # CREMMA uses white square brackets where Eutyches used round ones.
        damaged = any(c in prof.get("damaged_marks", "()[]") for c in r["text"])
        # Cap the glosses per line. Greek letterform triggers are common by nature -- omega
        # fires on 23 of 44 lines, kappa on 21 -- and four explanations under one line is a
        # wall of prose, not help. Keep the rarest, which are the ones a reader has least
        # chance of having met already.
        gl.sort(key=lambda g: GLOSS_FREQ.get(g["char"], 0))
        gl = gl[:3]
        out.append(dict(id=r["image"].rsplit(".", 1)[0][-12:], track=track, damaged=damaged,
                        text=r["text"], words=words, cloze=cloze_index(words),
                        diff=r["diff"], glosses=gl, layer=r["layer"], witness=r["witness"],
                        page=r["page"], w=im.width, h=im.height,
                        img=base64.b64encode(buf.getvalue()).decode()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True,
                    help="directory for the split payload: index.json + t-<track>.json")
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--max-w", type=int, default=2200)
    ap.add_argument("--quality", type=int, default=87)
    a = ap.parse_args()

    # Tracks, their metadata and their script profiles all come from registry/.
    # Adding a language is a TOML file plus its crops -- no edit here. See
    # tools/registry.py and EXPANSION-PLAN.md §3.
    languages, profiles, tracks = registry.load()

    # The trainer used to hardcode its tab list, its /latin -> latin route map, its
    # palettes and its normalisation rules, keyed by a literal track id. All of that is
    # registry data, so it ships in the payload and the shell reads it. Only what the
    # runtime actually needs goes across -- not the whole TOML.
    envelope_langs, envelope_profs = {}, {}
    for lang in sorted(languages.values(), key=lambda l: (l.get("order", 999), l["id"])):
        envelope_langs[lang["id"]] = {
            "name": lang["name"],
            "profile": lang["profile"],
            "resources": [{"label": r["label"], "url": r["url"], "note": r.get("note", "")}
                          for r in lang.get("resources", [])],
            "tracks": [{"id": x["id"], "tab": x["tab"], "route": x["route"],
                        "orient": x.get("orient", "").strip(),
                        "orientTail": x.get("orient_tail", "").strip()}
                       for x in lang.get("tracks", [])],
        }
    for prof in profiles.values():
        envelope_profs[prof["id"]] = {
            "name": prof["name"],
            "direction": prof["direction"],
            "keymap": prof.get("keymap", ""),
            "keymapHint": prof.get("keymap_hint", "").strip(),
            "cssClass": prof.get("css_class", ""),
            "primer": f"/hand/{prof['id']}" if prof.get("primer") else "",
            "primerName": prof["name"],
            "palette": prof["palette"],
            "fold": prof.get("fold", {}),
            "strip_combining": prof.get("strip_combining_when_forgiving", False),
            "fonts": prof["fonts"],
        }

    data = {"tracks": {}, "built": "2026-08-27",
            "languages": envelope_langs, "profiles": envelope_profs}
    lang_of = {}
    for t in registry.ordered_tracks(languages, tracks):
        meta = {"name": t["name"], "witness": t["witness"], "layer": t["layer"],
                "printed": t["printed"]}
        lang_of[t["id"]] = t["language"]
        if t.get("attribution"):
            meta["attribution"] = t["attribution"]
        items = pack(ROOT / t["crops"], a.n, a.max_w, a.quality, t["id"], t["profile"])
        data["tracks"][t["id"]] = dict(meta=meta, items=items)
        kb = sum(len(i["img"]) for i in items) / 1024 / 1024
        print(f"  {t['id']:6} {len(items):3} lines  {kb:.2f} MB  "
              f"difficulty {items[0]['diff']:.0f} \u2192 {items[-1]['diff']:.0f}")

    data["trackLang"] = lang_of      # which language space a track belongs to

    # Split, one file per track plus a small index.
    #
    # The bank was a single inlined blob because the trainer was ALSO built as a
    # self-contained Artifact, which can fetch nothing. That build is retired
    # (2026-08-28), and one file does not survive the expansion: three tracks are
    # 10.9 MB, and a reader who opens /greek should not pay for Latin at all.
    #
    # The INDEX stays inline in the page -- it is ~2 KB of languages, profiles and
    # routes, and the tab strip and track resolution need it before first paint or the
    # header flashes. Only the heavy part, the images, is fetched.
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    for tid, blob in data.pop("tracks").items():
        f = outdir / f"t-{tid}.json"
        f.write_text(json.dumps(blob, ensure_ascii=False), encoding="utf-8")
        print(f"  {tid:6} -> {f.name}  {f.stat().st_size/1024/1024:.2f} MB")
    index = outdir / "index.json"
    index.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"-> {index}  {index.stat().st_size/1024:.1f} KB index")
