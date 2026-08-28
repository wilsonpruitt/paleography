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
