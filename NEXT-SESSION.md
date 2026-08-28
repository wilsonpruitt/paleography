# Next session — start here

*Written 2026-08-28 at the close of Phases A and B. Read this before `PLAN.md` or
`EXPANSION-PLAN.md`: those are the score, this is where the needle is.*

---

## State: everything is shipped and clean

- Working tree clean, `origin/master` = `a35c7ed`, 0 ahead. Repo is **public**:
  `github.com/wilsonpruitt/paleography`.
- **Live and verified** 2026-08-28: `/` `/latin` `/latin-ii` `/greek` `/old-french`
  `/about` `/hand/*` `/og.png` `/api/keepalive` all 200.
  ⚠ **That verification is dated and expires. Never restate live state from this note —
  curl it.**
- 4 tracks × 110 lines across 3 languages. Bank hashes frozen in `tools/acceptance.sh`.

## The one command that matters

```sh
sh tools/acceptance.sh          # every pre-existing track must stay byte-identical
python3 tools/make_routes.py --check
```

`acceptance.sh` is the guard on everything below. It reports a **NEW** track rather than
failing, so adding a language is not an error; a **FAIL** means you changed a track you did
not mean to touch.

## ▶ The front is Phase C — Syriac, the RTL pilot

Chosen because it answers the hardest remaining question early, and because the data is
already there. **Opus** for the engine work, Sonnet for the second track once the first works.

**Data, both CC BY 4.0, both from HTR Winter Schools:**
- ÖNB Cod. Syr. 1 — 2,869 lines, 1545, **Serto**. ⭐ Same ÖNB IIIF route already solved for
  Cod. 940; see `research/onb-cod940-iiif.md`.
- Jerusalem, St Mark's 36 — 17,836 lines / 266 pages, s. XII–XIV, **Estrangela** with Serto
  and East Syriac features. Zenodo bundles bifolio images.

**Start with ÖNB Cod. Syr. 1**: one hand, and the IIIF path is known.

### What is genuinely new, and where it will hurt

1. **Right-to-left, end to end.** Not just `dir="rtl"` on a div. The places that will break:
   - the **input** and the **palette**;
   - the **Levenshtein diff rendering** (the alignment itself is direction-free; the display
     is not);
   - ⚠⚠ the **caret arithmetic in `wireBeta`**, which re-projects the cursor position after
     transliteration. That maths assumes LTR and must be re-derived. This is the single
     fiddliest thing in the whole expansion plan.
2. **A generic transliteration keymap.** Beta code is the Greek instance of a general thing:
   type on a Latin keyboard, see the target script. Generalise `BETA_BASE`/`BETA_DIA` into a
   keymap the profile names (`keymap = "beta-code"` already exists as a field). Syriac wants a
   SEDRA-style consonantal map, **unpointed by default**.
3. **A `syriac` profile.** ONE profile, three hands — Estrangela / Serto / East Syriac share
   letters and points, so the hand is a *variant field on the track*, not three profiles.

⭐ **Do Syriac unpointed first.** Estrangela has no final forms and light pointing, so it
isolates the DIRECTION problem from the NORMALISATION problem. Hebrew, which comes next, has
both at once — do not meet them together.

### The path is already proven

Phase B took Old French from nothing to live with **two TOML files plus crops**. Follow it:

```sh
# 1. fetch GT (XML + images), into corpus/raw/<witness>/   [gitignored]
# 2. python3 tools/ingest.py corpus/raw/<w> <w> --layer <declared> --out corpus/normalized/<w>.jsonl
# 3. ⛔ PROBE THE LAYER -- never trust the catalogue. See below.
# 4. python3 tools/crop.py corpus/normalized/<w>.jsonl corpus/raw/<w> corpus/crops/<w> --region MainZone
# 5. registry/profiles/<script>.toml + registry/languages/<lang>.toml
# 6. build, verify, deploy  (research/deploy.md has the full chain)
```

## ⛔ Rules paid for in blood. Do not relearn these.

- **Deploy from `site/`, NEVER the repo root.** A root deploy 404s the entire site for 13
  hours while reporting Ready. → [[feedback_vercel-deploy-from-subdirectory]], `research/deploy.md`.
- **Anything the trainer fetches uses an ABSOLUTE path.** `/greek` is a rewrite, so a relative
  URL resolves against `/greek` and 404s at the apex. `/read/` will look fine while every clean
  URL is broken. **Untestable locally** — `python3 -m http.server` has no rewrites.
- **PROBE the transcription layer; the catalogue lies.** It was wrong about wien940 (said
  diplomatic, was expanded). Count abbreviation signs and combining marks over the whole
  witness, and confirm on a plate. Old French: `⁊`×380, `ꝑ`×139 → diplomatic, and a crop showed
  `Qi ait ꝑdu si ait perdu`, the same word abbreviated then spelled out.
- **Read the PLATE's rights, not the dataset's.** Fabliaux GT is CC BY, but its Bern plates are
  Public Domain Mark while its other witnesses' plates come from Gallica (non-commercial).
  Rights are a property of the witness.
- **A check that can pass on a broken thing is not a check.** The OG card's first glyph test
  asked "did anything draw?" — and tofu draws. Compare against the font's own `.notdef`.
- **Never generate `site/vercel.json`, the `TRACKS` allowlist, the landing cards, or
  `site/og.png` by hand.** All come from `registry/`; `--check` catches drift.

## Owed by Wilson (none blocks Phase C)

- ⬜ **Send it to scholars, opening with the Greek Level-2 question** — no available Greek GT
  preserves abbreviations, so that track cannot teach the signs. ⭐ Better as the question you
  open with than a defect to hide; a Byzantinist settles it in a sentence. `handoff.md` is the
  pattern, one per language.
- ⬜ **An Old French expert seat** (`registry/languages/old-french.toml`, `expert = ""`). The
  primer says on its face it has no reviewer, and `st̾` (14×) is deliberately unexpanded.
- ⬜ **Ruling: Latin II's letter-ratio fix.** `count_marks_as_letters` is on for `latin-gothic`
  and off for `latin-caroline`. Eutyches has the same latent problem — 105 combining marks, 3
  lines would flip — and turning it on changes live exercise content on an existing track.
- ⬜ 5 Greek glosses still `proposed`.
- ⬜ Nav revisit past ~12 languages (two-tier bar; see EXPANSION-PLAN §7).

## Then what

Band 1, found GT: **Syriac → Hebrew/Aramaic → Coptic** (needs a licence fetch on SCAM) **→
Sanskrit** (early print, labelled type-not-a-hand).
Band 2, self-produced GT: **Hungarian → Middle English → Old English**. Hungarian's images are
settled and excellent (BSB Cod.hung. 1, Public Domain Mark, IIIF level 2 —
`https://www.digitale-sammlungen.de/en/view/bsb00087531`); its *transcription* is not reusable,
so it is a keying job with a readable-but-unshippable key. Expert seat: Alina.
DSS: a link page under Hebrew, never hosted crops.
