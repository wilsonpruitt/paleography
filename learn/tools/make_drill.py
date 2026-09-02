#!/usr/bin/env python3
"""Phase B of the Syriac web build -- compile learn/syriac/drill/L*.toml sidecars into the
TRACKS+ITEMS JSON learn/shell/drill_shell.html fetches at runtime, and extend the sidecar
verbatim check. Score: SYRIAC-WEB-PLAN.md §5 "Phase B", §3.

Why derivation happens HERE and not in the browser. The "First Light" prototype (private
Claude Artifact, 2026-09-02, G2-passed by Wilson on Lesson 0 and Lesson 1 end to end) built
its `ITEMS` object client-side from a handful of raw constants (LETTERS, PAIRS, VOCAB, ...)
via a dozen small .map() calls. §3's own instruction is "read TRACKS and items from
/drill/LNN.json instead of constants" -- i.e. the JSON should already BE the derived
ITEMS/TRACKS shape, so drill_shell.html's render functions stay the unmodified,
already-G2-passed rendering code, unchanged from the artifact, and only the derivation
(which the artifact did in JS, once, at load) moves to build time in Python. This module is
that port -- see derive_items() below, which is a line-for-line translation of the
artifact's `const ITEMS = {...}` block (read from the artifact source at
~/.claude/projects/-Users-wilsonpruitt/fe8b45cd-5b03-4e82-994b-35efe888d975/tool-results/
artifact-3cfed8ce-1788356037-8245.html, lines 516-587).

Sidecar TOML holds the RAW constants (letters/pairs/triples/vocab/vowels/halfline/cloze/
finish/whole) plus a `tracks` manifest (phase list per track, in ramp order) -- i.e. the
same shape as the artifact's own LETTERS/PAIRS/.../TRACKS variables, transcribed verbatim.
This keeps the TOML a faithful, checkable transcription (§3's "verbatim" rule below) rather
than a hand-derived ITEMS object that would be much larger and harder to eyeball against
the artifact source.

The verbatim check (§3): "make_learn.py --check fails if any Syriac string in a sidecar
does not occur verbatim in its lesson's .md." Implemented here as substring containment
(a word transcribed bare, e.g. ḥeššōḵā's ܚܶܫܘܟܳܐ, still passes when the .md only ever shows
it with a proclitic glued on front, e.g. ܘܚܶܫܘܟܳܐ, because the bare string is a literal
substring of the prefixed one) against a stripped-of-HTML-markup copy of every Syriac field.

Usage: imported by learn/tools/make_learn.py, not run standalone.
"""
import glob
import re
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent          # learn/tools
LEARN = HERE.parent                              # learn/
DRILL_SRC = LEARN / "syriac" / "drill"
DRILL_OUT = LEARN / "site" / "drill"

_BLANK_RE = re.compile(r"<span class='blank'></span>")
_TAG_RE = re.compile(r"<[^>]+>")


# ---------------------------------------------------------------------------
# 1. Load a sidecar
# ---------------------------------------------------------------------------

def load_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


def find_sidecars():
    return sorted(glob.glob(str(DRILL_SRC / "L*.toml")))


# ---------------------------------------------------------------------------
# 2. Derivation -- line-for-line port of the artifact's `const ITEMS = {...}`
# ---------------------------------------------------------------------------

def _letter_names(letters):
    return [l["a"] for l in letters]


def derive_items(data, alphabet_letters, alphabet_sound):
    """data is one lesson's parsed TOML. alphabet_letters/alphabet_sound are the shared
    22-letter table + sound map (always sourced from L00.toml -- see build(); a lesson
    with no `letters` track of its own, like L01, still needs LETTER_NAME_BY_CHAR
    client-side for the word-breakdown panel on vocabSound/vocabMeaning/halfline)."""
    items = {}

    if "letters" in data:
        letters = data["letters"]
        names = _letter_names(letters)
        items["letters"] = {
            "study": letters,
            "recognize": [
                {"promptType": "syriac", "prompt": l["p"], "correct": l["a"],
                 "optionType": "text", "pool": names, "note": l.get("note", "")}
                for l in letters
            ],
            "produce": [
                {"promptType": "syriac", "prompt": l["p"], "answerType": "text",
                 "answer": l["a"], "note": l.get("note", "")}
                for l in letters
            ],
        }

    if "pairs" in data:
        pairs = data["pairs"]
        sound = data["letter_sound"]
        items["pairs"] = {
            "sound": [
                {"p": x["p"], "translit": "-".join(sound[n] for n in x["letters"]),
                 "note": "letters: " + ", ".join(x["letters"])}
                for x in pairs
            ],
            "recognize": [
                {"promptType": "syriac", "prompt": x["p"], "correct": ", ".join(x["letters"]),
                 "optionType": "text", "pool": [", ".join(y["letters"]) for y in pairs]}
                for x in pairs
            ],
            "fillin": [
                {"prompt": x["p"], "givenLabel": "First letter", "givenValue": x["letters"][0],
                 "correct": x["letters"][1], "optionType": "text", "pool": alphabet_letters}
                for x in pairs
            ],
            "produce": [
                {"promptType": "syriac", "prompt": x["p"], "answerType": "text",
                 "answer": ", ".join(x["letters"]),
                 "translit": "-".join(sound[n] for n in x["letters"])}
                for x in pairs
            ],
        }

    if "triples" in data:
        triples = data["triples"]
        sound = data["letter_sound"]
        items["triples"] = {
            "sound": [
                {"p": x["p"], "translit": "-".join(sound[n] for n in x["letters"]),
                 "note": "letters: " + ", ".join(x["letters"])}
                for x in triples
            ],
            "recognize": [
                {"promptType": "syriac", "prompt": x["p"], "correct": ", ".join(x["letters"]),
                 "optionType": "text", "pool": [", ".join(y["letters"]) for y in triples],
                 "note": x.get("note", "")}
                for x in triples
            ],
            "fillin": [
                {"prompt": x["p"], "givenLabel": "First letters",
                 "givenValue": ", ".join(x["letters"][:-1]), "correct": x["letters"][-1],
                 "optionType": "text", "pool": alphabet_letters, "note": x.get("note", "")}
                for x in triples
            ],
            "produce": [
                {"promptType": "syriac", "prompt": x["p"], "answerType": "text",
                 "answer": ", ".join(x["letters"]),
                 "translit": "-".join(sound[n] for n in x["letters"]), "note": x.get("note", "")}
                for x in triples
            ],
        }

    if "vocab" in data:
        vocab = data["vocab"]
        items["vocabSound"] = {
            "vowels": [
                {"p": v["mark"], "a": v["name"], "note": v["sound"],
                 "context": data.get("vowel_context", "")}
                for v in data.get("vowels", [])
            ],
            "sound": [{"p": v["p"], "translit": v["t"]} for v in vocab],
            "recognizeSound": [
                {"promptType": "syriac", "prompt": v["p"], "correct": v["t"],
                 "optionType": "text", "pool": [y["t"] for y in vocab]}
                for v in vocab
            ],
        }
        items["vocabMeaning"] = {
            "meanings": [{"p": v["p"], "a": v["a"], "note": f"({v['t']})"} for v in vocab],
            "recognize": [
                {"promptType": "syriac", "prompt": v["p"], "correct": v["a"],
                 "optionType": "text", "pool": [y["a"] for y in vocab]}
                for v in vocab
            ],
            "recognizeReverse": [
                {"promptType": "text", "prompt": f"Which word means “{v['a']}”?",
                 "correct": v["p"], "optionType": "syriac", "pool": [y["p"] for y in vocab]}
                for v in vocab
            ],
            "produce": [
                {"promptType": "syriac", "prompt": v["p"], "answerType": "text",
                 "answer": v["a"], "translit": v["t"]}
                for v in vocab
            ],
        }

    for key in ("halfline", "cloze", "finish"):
        if key in data:
            items[key] = {"produce": [
                {"promptType": e.get("prompt_type", "syriac"), "prompt": e["prompt"],
                 "answerType": "syriac", "answer": e["answer"], "translit": e.get("translit", ""),
                 "note": e.get("note", ""), "context": e.get("context", "")}
                for e in data[key]
            ]}

    # `forms` and `drills` -- the two NEW track types from §3, not used by L00/L01 but
    # supported here for Phase C. Neither needs a new client-side phase-type renderer:
    # both are shaped to reuse the existing study/mc/produce renderers (a `forms` item's
    # `form`/`cell`/`gloss` map onto the same p/a/note and prompt/correct/pool shapes the
    # engine already understands), per the plan's own steer to extend the vocabulary
    # rather than invent a parallel one.
    if "forms" in data:
        forms = data["forms"]
        items["forms"] = {
            "study": [{"p": f["form"], "a": f["cell"], "note": f.get("gloss", "")} for f in forms],
            "recognize": [
                {"promptType": "syriac", "prompt": f["form"], "correct": f["cell"],
                 "optionType": "text", "pool": [y["cell"] for y in forms]}
                for f in forms
            ],
            "produce": [
                {"promptType": "syriac", "prompt": f["form"], "answerType": "text",
                 "answer": f["gloss"], "note": f.get("lemma", "")}
                for f in forms
            ],
        }

    if "drills" in data:
        drills = data["drills"]
        items["drills"] = {
            "recognize": [
                {"promptType": "syriac", "prompt": d["prompt"], "correct": d["answer"],
                 "optionType": "text", "pool": [y["answer"] for y in drills]}
                for d in drills
            ],
        }

    if "whole" in data:
        items["whole"] = {"produce": [
            {"promptType": e.get("prompt_type", "text"), "prompt": e["prompt"],
             "answerType": "syriac", "answer": e["answer"], "translit": e.get("translit", ""),
             "note": e.get("note", ""), "context": e.get("context", "")}
            for e in data["whole"]
        ]}

    return items


def derive_tracks(data):
    tracks = []
    for t in data.get("tracks", []):
        tracks.append({
            "key": t["key"], "title": t["title"],
            "phases": [
                {"key": p["key"], "type": p["type"], "label": p["label"],
                 "randomize": p.get("randomize", False)}
                for p in t.get("phases", [])
            ],
        })
    return tracks


def compile_lesson(data, alphabet_names, alphabet_sound, alphabet_rows):
    """alphabet_rows is always the full {p,a,note} table (sourced from L00.toml, the one
    sidecar that owns `letters` -- every lesson needs LETTER_NAME_BY_CHAR client-side for
    the word-breakdown panel on vocabSound/vocabMeaning/halfline, per the artifact's
    WORD_LEVEL_TRACKS/decomposeWord logic, lines ~421-439 of the source)."""
    return {
        "lesson": data["lesson"],
        "tracks": derive_tracks(data),
        "items": derive_items(data, alphabet_names, alphabet_sound),
        "scorecard": data.get("scorecard", {}),
        "alphabet": {
            "letters": alphabet_names,          # ordered list of names, for MC pools
            "nameByChar": {l["p"]: l["a"] for l in alphabet_rows},
        },
    }


# ---------------------------------------------------------------------------
# 3. Verbatim check
# ---------------------------------------------------------------------------

_SYRIAC_RE = re.compile(r"[܀-ݏ]")


def _syriac_substrings(value):
    """Pull every literal SYRIAC fragment out of a field that may carry the
    `<span class='blank'></span>` gap marker -- split on it and keep non-empty, stripped
    pieces that actually contain Syriac-block characters, so a fill-in-the-blank prompt is
    checked around its gap rather than as one unmatchable HTML-laced string, and an
    English-language `text`-type prompt (e.g. `whole[0]`'s "say it aloud" cue) isn't held
    to a verbatim-punctuation standard the plan's own rule was never about -- §3 says "any
    Syriac string in a sidecar," not English prose."""
    if not isinstance(value, str):
        return []
    pieces = _BLANK_RE.split(value)
    out = []
    for p in pieces:
        p = _TAG_RE.sub("", p).strip()
        if len(p) >= 2 and _SYRIAC_RE.search(p):
            out.append(p)
    return out


_WRAP_RE = re.compile(r"\n>\s*")


def check_verbatim(data, lesson_text, lesson_name):
    """Returns a list of error strings. Checks every Syriac-bearing field (p, prompt,
    answer, given*, form fields) as a substring of the lesson's raw .md text.

    A long Stage-1 verse in these lessons often wraps across two markdown-blockquote
    lines (`> ...word\n> word...`), so a "whole line" answer spanning the wrap can't be
    a literal substring of the raw file no matter how faithfully it's transcribed -- the
    file itself has a "\n> " sitting where the transcription has a plain space. Also try
    the fragment against a version of the lesson text with every such wrap collapsed to
    a single space, so a faithful multi-line transcription still passes without being
    forced to reproduce the file's own line-wrapping and blockquote markers."""
    errors = []
    lesson_text_unwrapped = _WRAP_RE.sub(" ", lesson_text)

    def check_field(container_desc, value):
        for frag in _syriac_substrings(value):
            if frag not in lesson_text and frag not in lesson_text_unwrapped:
                errors.append(f"{lesson_name} [{container_desc}]: `{frag}` not found verbatim in the lesson .md")

    for l in data.get("letters", []):
        check_field(f"letters/{l['a']}", l.get("p"))
    for x in data.get("pairs", []):
        check_field(f"pairs/{x['p']}", x.get("p"))
    for x in data.get("triples", []):
        check_field(f"triples/{x['p']}", x.get("p"))
    for v in data.get("vocab", []):
        check_field(f"vocab/{v['t']}", v.get("p"))
    for v in data.get("vowels", []):
        check_field(f"vowels/{v['name']}", v.get("mark"))
    for key in ("halfline", "cloze", "finish", "whole"):
        for i, e in enumerate(data.get(key, [])):
            check_field(f"{key}[{i}]/prompt", e.get("prompt"))
            check_field(f"{key}[{i}]/answer", e.get("answer"))
    for i, f in enumerate(data.get("forms", [])):
        check_field(f"forms[{i}]/form", f.get("form"))
        check_field(f"forms[{i}]/lemma", f.get("lemma"))
    for i, d in enumerate(data.get("drills", [])):
        check_field(f"drills[{i}]/prompt", d.get("prompt"))

    return errors


# ---------------------------------------------------------------------------
# 4. Build
# ---------------------------------------------------------------------------

def build(lesson_texts, write=True):
    """lesson_texts: dict of {"L00": raw .md text, ...} for verbatim checking, keyed by
    zero-padded lesson id. Returns (errors, compiled) where compiled is {lesson_id: dict}."""
    errors = []
    compiled = {}
    raw = {}

    for path in find_sidecars():
        p = Path(path)
        lid = p.stem  # "L00"
        data = load_toml(path)
        if data.get("lesson") != lid:
            errors.append(f"{p.name}: `lesson = \"{data.get('lesson')}\"` does not match filename")
        raw[lid] = data

    if "L00" not in raw:
        errors.append("no L00.toml -- the shared 22-letter alphabet table has no source")
        return errors, compiled

    shared_letters = raw["L00"]["letters"]
    shared_sound = raw["L00"]["letter_sound"]

    alphabet_names = _letter_names(shared_letters)
    for lid, data in raw.items():
        entry = compile_lesson(data, alphabet_names, shared_sound, shared_letters)
        compiled[lid] = entry

        n = lid[1:].lstrip("0") or "0"
        md_path = LEARN / "syriac" / f"LESSON-{n}.md"
        if md_path.exists():
            md_text = lesson_texts.get(lid) or md_path.read_text(encoding="utf-8")
            errors.extend(check_verbatim(data, md_text, lid))
        else:
            errors.append(f"{lid}.toml: no matching {md_path.name}")

    if write:
        DRILL_OUT.mkdir(parents=True, exist_ok=True)
        import json
        for lid, entry in compiled.items():
            (DRILL_OUT / f"{lid}.json").write_text(
                json.dumps(entry, ensure_ascii=False, indent=1), encoding="utf-8")

    return errors, compiled
