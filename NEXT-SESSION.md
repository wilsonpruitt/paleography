# Next session — start here

*Rewritten 2026-08-28 at the close of Phase C (Syriac). Read this before `PLAN.md` or
`EXPANSION-PLAN.md`: those are the score, this is where the needle is.*

---

## State

- **5 tracks, 4 languages, 4 script profiles.** Syriac shipped 2026-08-28: pushed, deployed
  from `site/`, and `/syriac` verified on the real domain by a clean URL, not `?track=`.
  The landing chips were reworked the same day — the chip is the LANGUAGE on every card,
  with Latin's order moved to a second `card_step` chip — and stage 0 now opens with the
  plate instead of burying it under the orientation essay.
- `sh tools/acceptance.sh` → all five PASS, including `syriac1`, whose hash is now baselined.
- ⚠ Any statement about what is LIVE expires. Never restate it from this note — curl it.

## Second path: the Syriac LANGUAGE pilot (separate from the hand-trainer work below)

- Score: `SYRIAC-LANGUAGE-PILOT.md` · ✅ **Phase 0 done, G0 passed 2026-08-31**
  (`research/syriac-pilot-phase0.md` — scans pinned, licences verdicted, Robinson 1915 is
  keyless).
- ✅ **Phase 1 Step 0 + Step 1 done 2026-09-01.** Structure map =
  `quarry/nestle-1889-en/MAP.md`; measurement + hard stop =
  `research/syriac-pilot-phase1-calibration.md`. 34 calibration records from 8 pages.
- ▶ **RUNNING. Wilson said 'opus go' 2026-09-01; Step 2 is under way, single-threaded.**
  ▶▶ **The glossary shard is the live work — read `quarry/nestle-1889-en/GLOSSARY-SHARD.md`
  and run it straight through.** ✅ **51 of 63 pages, 710 records (2026-09-01).**
  pp. 162–170 and 172–183 done this session — 21 pages, +303 records, the ܟ ܠ ܡ ܢ ܣ ܥ ܦ ܨ
  sections entire, ܩ open at ܩܒܰܪ. The run is now CONTIGUOUS to the end: 12 pages left,
  pp. 184–195 (n273–n284). `python3 tools/quarry_r4.py --remaining` tells you exactly where to
  resume. ⚑ No fan-out: this Mac has ~100 MB free and 4.9 GB of swap in use.
- Approved estimate, for reference: **4.7k vision + 1.5k output tokens per page**; 201-page
  extraction set ⇒ **~1.43M tokens irreducible, ~2.5-3.0M end to end on Opus**. ⚑ **Recalibrated
  again at 51/63:** the head rate is stable at 13.9/page, but the SUB rate has come back DOWN as
  the later sections filled with one-line cross-references — 589 subs against 710 heads, 25.5
  lemmas/page, projecting **~1,600 lemmas for the glossary entire**, not the ~1,680 the halfway
  point suggested. Uncertainty is steady at 19–21%. Zooms now run about one per page.
- ⛔ **A defect worth remembering: `emit` silently dropped every `sub_lemmas` it was handed**,
  from the 2026-09-01 ruling until it was caught on p. 150 — the ruling converted the existing
  records and left the WRITER behind. Fixed, and `emit` now raises on a mismatch. No earlier
  page lost data. The general lesson is in the shard doc as convention 7.
- ⛔ **A second defect of the same family, and --validate does NOT catch it.** In TOML a bare key
  written after a `[[sub_lemmas]]` table belongs to THAT TABLE. A hand fold-back that inserted
  `continues_from` just before `[source]` buried it inside the last sub-lemma and the file still
  parsed. Caught by inspection, fixed, and written into convention 9: **every root-level key added
  by hand goes BEFORE the first `[[sub_lemmas]]` line**, and it is checked with `tomllib`, not
  with --validate.
- ⬜ **NEW and it is Wilson's ruling, not the Syriacist's — the DUPLICATE GLOSSES.** Seventeen
  German or English words are now reached from two unrelated roots with no pointer between them
  ('Leuchter', 'Haar', 'Schrift', 'Blindheit', 'labour' three times, 'Gegner' three times,
  'schmähen' one page apart in the same section, …). Extraction has only RECORDED them, each
  flagged ⚑ in a `primer_note`. Linking them is a curriculum decision about what a learner should
  see. ⭐ The sharpest instance is not a gloss but a WORD: p. 180 prints the Passover twice —
  ܦܶܣܚܳܐ glossed 'τὸ πάσχα' as a Greek loan, and ܦܶܨܚܳܐ glossed 'Passover' under the Syriac root
  ܦܨܚ 'be cheerful' — in two correct alphabetical slots, with no cross-reference either way.
- ⬜ **Still owed by Wilson — none of these blocks the glossary, all of them block what follows:**
  1. ⬜ **R5 / `word_notes`**: Nestle's "Aids to Translation" are per-word notes keyed to a
     passage — a ready-made gloss layer with no home in §4. Changes WHAT the run extracts.
  2. ⬜ **Does R3 run FIRST?** ⭐ Corrected 2026-09-01: the **Peshitta NT text is PUBLIC DOMAIN**
     (SEDRA carries the BFBS/UBS 1905 edition; only its lemmatization/morphology are
     compute-only). No clean digital *carrier* was found — ⛔ ETCBC/peshitta is the OT, OCR'd
     from the in-copyright Leiden 1987 and declares MIT *and* CC BY-NC (third such repo, after
     Cod. 940 and Cod. Syr. 1) — so we **produce** the text instead: key from Nestle (itself a
     PD printed Peshitta), check against SEDRA + a PD 1905 scan, ship neither. That splits R3:
     **23 Peshitta pages are keyable and checkable NOW**; the 44 pages of Vitae Prophetarum /
     Historia inventionis ⭐ ALSO have controls now (2026-09-01): **Schermann, *Prophetarum
     vitae fabulosae*, Teubner 1907** = `prophetarumvita00schegoog`, which prints a **Latin
     version of the Syriac** (Sinai Syr. 10) at p. 105 + a proper-name index — sense-level, but
     in Latin, so Wilson can run it; and ⭐ **Nestle's own *De sancta cruce*, 1889** =
     `desanctacruceein0000nest`, from which he lifted chrestomathy IV verbatim (same heads, same
     three codices, same `(b, col. 1)` folio markers) — a character-level Syriac diff, though
     NOT an independent witness. **No chrestomathy page is now without a control, and the
     Syriacist is no longer a precondition for R3.** ✅ **Diff targets PINNED 2026-09-01**
     from Brock's bibliography (`syri.ac/brock/bible` — Cloudflare-blocks curl and WebFetch,
     renders in Playwright): **Barnes, *Pentateuchus Syriace*, BFBS 1914** =
     `ktavadeauritaauk00lees` for Genesis, and **BFBS *New Testament in Syriac* 1905-1920** =
     `newtestamentinsy00unse` for Matthew and the Lord's Prayer. Both PD, both verified at the
     title page. Full note: `research/syriac-peshitta-editions.md`.
  3. ⚠ **The Syriacist seat is still empty and that is what this batch cost.** 200 more pages
     before it is filled multiplies unadjudicated Syriac by 25×. Same two people as the licence
     email: **Ephrem Aboud Ishac** + **Christine Roughan**. One message covers both.
- Two Phase-0 facts corrected by the plates: **Nestle has NO R2** (the "Reading Exercise" is the
  Lord's Prayer in the Peshitta), and the chrestomathy is **not** uniformly Estrangela — p. 67
  opens in vocalized Serto and ramps to unvocalized Estrangela by p. 71, inside one passage.
- ⚠ The glossary is the volume: ~1,150-1,300 R4 records over 63 pages, where §2 expected "low
  hundreds".

## The one command that matters

```sh
sh tools/acceptance.sh                 # every track byte-identical, syriac1 included
python3 tools/make_routes.py --check   # vercel.json + landing cards + TRACKS allowlist
```

## ⛔ Owed by Wilson, in the order they block things

1. **⚠ THE LICENCE, and it touches a live track.** Both HTR Winter School Vienna
   repositories — Cod. 940 (**Latin I, live since day one**) and Cod. Syr. 1 (Syriac) —
   ship a **CC BY-SA 4.0** `LICENSE.md` beside an `htr-united.yml` that declares **CC BY
   4.0**. GitHub's own detection says BY-SA. The site and README claimed flat CC BY 4.0
   for everything; both now state BY-SA for these two and say why.
   *What turns on it:* BY-SA requires adaptations to stay BY-SA and forbids adding a
   non-commercial term — so if the exercise banks are adaptations they cannot ship under
   Wroot Press's usual CC BY-NC. One email to the Winter School settles it for both tracks.
   Full detail: `corpus/sources.yml` → `onb-syr1.license_conflict`.
2. **Ruling: the word-division gloss fires on Greek.** `SPACING`'s note is Latin end to
   end (`quarequomodolongitudinem`, "the Latin divides the line") and has been appearing
   under Greek lines since the Greek track shipped. Glosses are now scoped by profile, and
   `greek-minuscule` was left in the scope **only to keep a live bank byte-identical** —
   the same shape as the latin-caroline letter-ratio ruling. Drop it there, or write a
   Greek one?
3. Still open from before: an **Old French expert seat**; the **latin-caroline
   `count_marks_as_letters`** ruling; **5 Greek glosses** at `proposed`; the Greek Level-2
   question to open the scholar outreach with.
4. **⬜ NEW: a Syriacist.** `registry/languages/syriac.toml` has `expert = ""`, and four
   new glosses are `proposed` — every claim about what a dot does is from counted data
   plus standard grammar, ruled on by nobody. ⏸ UT Austin LRC is still unanswered from
   2026-08-28 and **cannot serve Syriac anyway** (EIEOL is Indo-European). The people to
   ask are on the dataset itself: **Ephrem Aboud Ishac** and **Christine Roughan**, who
   ran the Winter School Syriac group. They are also the right people to ask about the
   licence in the same message.

## What Phase C actually changed in the engine

Nothing about direction turned out to be hard. What was hard was **naming**, twice.

- **RTL is a container property.** The Levenshtein alignment is direction-free; only the
  render needed `dir`. Per-character diff spans order correctly under bidi once the
  container declares direction.
- ⭐ **The caret arithmetic in `wireBeta` was NOT the problem the plan feared.**
  `selectionStart` is a LOGICAL offset, not a pixel position, so it is direction-blind.
  The keymap engine (now `wireKeymap` + a `KEYMAPS` table, profile-selected) needed no new
  maths for RTL at all. `EXPANSION-PLAN.md §5a` overestimated this; leave the note for the
  Hebrew session.
- **`.gk` is gone as the mechanism.** Direction, font stack and printed size come from the
  profile and are applied at render (`scriptify`). `fonts` was already in the payload and
  unread. A new script needs no CSS rule written by hand.
- **Webfonts are registry data** (`webfont` on the profile → one `<link>`, in both the
  trainer and the primers). ⚠ **A Google Fonts family that does not exist fails silently**
  — 200 with an HTML error page, then a fallback with no glyphs. Verified present: Noto
  Sans Syriac Western (= Serto), Noto Sans Syriac (= Estrangela), Noto Sans Syriac Eastern.
  Verified ABSENT: Noto Serif Syriac, Noto Sans Syriac Estrangela.
- **Glosses are scoped by profile.** A character gloss is self-scoping; a TRIGGER gloss is
  a regex and is not. See §3 above.
- **`stripCombining` is now `\p{M}`**, not two hand-picked ranges that happened to be
  Latin's and Greek's.
- **`ingest.py`**: reads SegmOnto types out of Transkribus's `custom="structure {type:…}"`
  (they are not in `@type`), and strips edge whitespace.
- **`fetch_iiif.py`**: takes `--page-dir` (PAGE XML image sizes) as well as `--tei`, and a
  `--page-re` for witnesses whose filename does not lead with the leaf number. It now
  reports its own scale calibration instead of computing it silently.

## Traps this phase paid for

- ⛔ **Git LFS is DISABLED on the Syriac repo.** Its 140 JPEGs are unreachable by every
  route (batch API 403s; every raw URL returns the pointer), and a plain `git clone`
  aborts checkout. Clone with the LFS filters switched off — `tools/fetch-seeds.sh` does —
  and take the plates from ÖNB over IIIF.
- ⭐ **The old RepViewer `DTL_…` id works directly as an ÖNB manifest id**
  (`…/manifest/DTL_2933415`). The bare number 404s. This skips the whole onb.digital search
  dance in `research/onb-cod940-iiif.md` — and that search API is now broken in a new way
  (500 on a missing `api_query`).
- ⛔ **The GT repo's date is wrong.** It says 1545; ÖNB says **1554**, and records the
  manuscript as the **Vorlage for the first book ever printed in Syriac** (Vienna 1555).
  `EXPANSION-PLAN.md` copied the wrong date. Always read the library's record, not the
  dataset's README — it is the same rule as the transcription layer, one field over.
- **Calibrate, don't spot-check.** Canvas offset −1 gives scale exactly 0.500 on 140/140
  pages with x=y; offsets 0 and −2 give a plausible ≈0.5 that is wrong on 19–20 pages.
  That near-miss is what made offset 0 look right for Cod. 940.
- **Double quotes in a `style=""` attribute.** The font stack was written into inline
  markup and closed the attribute early, so the first RTL build drew Syriac in EB Garamond
  while `dir="rtl"` worked perfectly — a failure that looks like success.

## Then what

Band 1, found GT: **Hebrew/Aramaic → Coptic** (needs a licence fetch on SCAM) **→
Sanskrit** (early print, labelled type-not-a-hand). Hebrew is the next RTL language and now
meets only the NORMALISATION problem — finals folding and vocalisation density — since
direction is solved. ⚠ Its images are BnF + Vatican and the rights, not the code, decide
whether it is a track or a link page.

A **second Syriac track** (Jerusalem, St Mark's 36 — Estrangela, 17,836 lines, Winter
School 2025, images bundled on Zenodo) is cheap now: one language TOML entry. It wants
`Noto Sans Syriac` rather than the Western face, which means **a per-track font override
the profile does not yet have** — the smallest real piece of new code left here.

Band 2, self-produced GT: **Hungarian → Middle English → Old English**.
DSS: a link page under Hebrew, never hosted crops.
