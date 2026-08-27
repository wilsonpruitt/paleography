# Paleography — first principles and plan

*Wroot Labs · drafted 2026-08-26 (Fable planning session) · status: PLAN, nothing built*

Two directions, one asset:

1. **Learner-facing** — a tool that takes someone who already reads Greek and/or Latin
   and teaches them to read the *manuscripts* (and, later, papyri and early print).
2. **Machine-facing (future, funded)** — script-specific HTR/OCR models for ancient
   languages, so that manuscript transcription becomes cheap.

The thesis of this document: **these are the same project seen from two sides, because
both consume and produce exactly one thing — a corpus of aligned (image region ↔
transcription) pairs tagged by script, hand and date.** Build that corpus in the right
shape from day one and the learner product is a way of *growing and validating* it,
while the model work is a way of *exploiting* it. Everything below follows from that.

---

## 1. What the skill actually is (first principles)

A person who reads printed Latin brings a strong *language prior* — they know what
words are likely. What they lack is the *vision* half: mapping ink shapes to graphemes
in a script they have never seen. Paleography is the training of that vision half
**plus** the discipline of fusing it with the language prior without letting the prior
hallucinate.

That is also, precisely, the architecture of an HTR system: a visual encoder that
proposes characters, a sequence decoder, and a language model that biases the
decoding. **The learner's curriculum and the model's curriculum are the same
curriculum**, ordered from small units to large:

| Level | Learner task | Model analogue | Ground-truth unit |
|---|---|---|---|
| 0 Script | "What am I looking at?" (uncial / Caroline / Gothic / Greek minuscule …) | script classifier | page → script label |
| 1 Glyph | letterform → letter, incl. variant forms (tall-s, r-rotunda, Greek ligatured tau-alpha) | character recognition | glyph crop → grapheme |
| 2 Abbreviation | mark → expansion (macron = nasal; nomina sacra; Tironian *et*; *-bus*, *-rum*, *-que*; Greek tachygraphy) | expansion / normalisation model | token → diplomatic + expanded |
| 3 Line | read a whole line; word separation, ligatures, punctuation, breathings/accents | line-level CTC/seq2seq HTR | line polygon → transcription |
| 4 Page | layout: columns, glosses, rubrics, running heads, catchwords, marginal apparatus | layout analysis / segmentation | page → regions |
| 5 Judgement | date & localise a hand; identify corrections, scribes, quire structure | (research-grade; out of scope) | metadata |

Two consequences:

- **Levels 1–3 are where all the leverage is.** Level 0 is a short gate, level 4 is
  mostly presentation, level 5 is a graduate seminar. MVP is levels 0–3.
- **Every learner error is a datum.** A learner who confuses *c/t* in Caroline, or
  *β/μ* in a 12th-c. Greek minuscule, has just contributed to a confusion matrix.
  That matrix (a) orders the curriculum (teach the hard pairs) and (b) is the
  hard-example mining an HTR project pays annotators for. This is the concrete form of
  "the two tasks inform each other" — not a vague synergy, a shared table.

## 2. The asset: ground truth in the right shape

**Do not invent a format.** The HTR world has settled on **PAGE XML** (and ALTO) as the
interchange for page images + line polygons + transcription; eScriptorium/Kraken and
Transkribus both read and write it. Store our canonical data in a relational schema
(below) and *export* PAGE XML. This is what makes the future model work a
zero-migration step.

Working data model (Supabase/Postgres, Labs pattern):

```
Witness   — shelfmark, repository, IIIF manifest URL, date range, origin, licence,
            script_family (FK), language(s), catalogue refs
Page      — witness, folio, IIIF image id, dimensions, layout regions (jsonb)
Line      — page, polygon, baseline, order, diplomatic text, expanded text,
            normalised text, status (seed | learner | double-keyed | verified)
Token     — line, bbox, diplomatic, expanded, abbreviation_type (FK|null)
Glyph     — token, bbox, grapheme, variant_form (FK)   ← optional; derive lazily
Script    — taxonomy row: family, sub-type, date range, language, description,
            canonical letterform table, abbreviation inventory
Attempt   — user, target (line|token|glyph), submitted text, diff (jsonb), ms taken
```

Three transcription layers, always, because learners and models both need them:

- **diplomatic** — what is on the page, abbreviation marks as marks (`dñs`, `ꝑ`)
- **expanded** — abbreviations resolved, expansions marked (`d(omi)n(u)s`, `p(er)`)
- **normalised** — what a printed edition would show (`dominus`, `per`)

A learner's line answer is diffed against *expanded* with tolerance on *normalised*;
a Level-2 exercise asks for the expansion specifically. A model is trained on
diplomatic (what it sees) with a separate expansion step — the field's consensus and
the honest thing pedagogically too.

**Seed, don't create.** Open ground truth already exists in this shape:
**HTR-United** catalogues openly licensed datasets (CREMMA Medieval Latin, various
Greek minuscule sets, papyri). Ingest those first; that is the exercise bank on day one
and the model baseline on day 1,000. *(Verify current dataset list and licences — my
knowledge stops at Jan 2026.)*

**Images via IIIF, rights-clear only.** Each Witness carries a licence and the exercise
bank only draws on witnesses whose terms permit it. Rough tiers (verify each):
e-codices, Bodleian Digital, Beinecke, Walters, Library of Congress, many German
state libraries → open; BnF Gallica → non-commercial; DigiVatLib → restrictive
(deep-link, never re-host). Same discipline as [[wroot-press-licensing]]: read the
rights statement before a single image enters the bank. Learner-produced transcription
is licensed **CC BY** (the corpus must be reusable for training or the whole thesis
fails).

## 3. The learner product

**Audience.** Seminarians and clergy with Greek, classics/medieval grad students,
self-taught readers of Migne who want to check the manuscripts, Wroot Press's own
translators. Assumption: they know the language. We never teach Latin; we teach ink.

**Exercise types (map to the levels):**

- *Script ID* — page crop → pick the script family; unlocks a script's track.
- *Glyph cards* — crop → type the letter; spaced repetition (SM-2 is enough) over the
  script's letterform inventory, weighted by that learner's confusions.
- *Expand* — token crop → type the expansion; abbreviation inventory per script.
- *Line* — full line crop → transcribe; character-level diff shown inline, with
  "why" notes (tooltip on each miss: *this is r-rotunda after o*).
- *Locate* — "find *misericordia* on this page" → click; trains scanning.
- *Read-along* (later) — a whole page with reveal-on-hover, for pleasure reading.

**Tracks (MVP = two):**

1. **Latin: Caroline minuscule** (c. 800–1100). Most regular, best-documented, the
   traditional entry point, and the script behind much of the PL base text.
2. **Greek: minuscule, 10th–12th c.** (biblical/patristic bookhands, Perlschrift
   type). Same argument for PG.

Deferred, in order: Latin Gothic textualis → Insular / Beneventan / Visigothic →
Gothic cursive and documentary hands (hard) → Greek majuscule / papyri (different
imaging problems) → early print (types & abbreviations, which Press actually needs)
→ Arabic, when [[bibliotheca-arabica]] justifies it. The schema is script-agnostic;
adding a track is content, not code.

**Contribution mode (Phase 3).** After passing a track, the learner is offered unseen
lines. Two independent learner transcriptions that agree (after normalisation) →
`double-keyed`; disagreement → an expert queue (Wilson, or a trusted reviewer) →
`verified`. This is the Zooniverse pattern; the difference is our contributors are
*certified on this script first*, so agreement is meaningful.

**Positioning.** Wroot Labs (product, not Press). Low-price strategy applies
([[wroot-labs-pricing]]): learning is free or nearly; the durable asset is the corpus,
not subscriptions. No CTAs, no gamification beyond the SRS itself.

## 4. The model direction (funded, later)

Not to be built now. What is decided now so the corpus is ready:

- **Baseline is Kraken/eScriptorium, not a from-scratch model.** Fine-tune per script
  family from an open base; measure **CER/WER per script and per witness**, never a
  single aggregate. The field's finding (verify) is that script-specific models beat
  generalists for these hands, which is exactly why the Script taxonomy is a
  first-class table.
- **Diplomatic transcription is the training target; expansion is a second model** (or
  a rule table per script + LM). Do not train on normalised text.
- **Layout is separate**: segmentation model or manual polygons; the learner app can
  crowd-source polygon *correction* cheaply (drag a baseline) — another shared table.
- **Evaluation set is frozen and never shown to learners** — hold out ~10% of verified
  lines per script at ingest, before the exercise bank sees them.
- **VLM route** (fine-tuning a vision-language model on the same pairs) is the
  alternative; same data, so it costs nothing to keep open. Decide when funded.
- **Publish** models and GT openly (CC BY / permissive) — the credibility of the
  product is the corpus, and grant funders fund open corpora.

## 5. What informs what — the shared tables

| Shared thing | Learner side uses it for | Model side uses it for |
|---|---|---|
| Line/Token GT | exercises, answer key | training + eval |
| Confusion matrix (from Attempts) | curriculum ordering, per-learner SRS weighting | hard-example mining, error analysis |
| Script taxonomy + letterform/abbrev. inventories | lessons, tooltips | model partitioning, expansion rules |
| Layout polygons | line crops for exercises | segmentation training |
| Double-keying agreement | certification, contribution | GT growth, label confidence |

## 6. Phases

- **Phase 0 (this doc).** First principles, schema, script taxonomy skeleton. *Fable.*
- **Phase 1 — corpus seed. ✅ DONE 2026-08-26** (see `README.md`, `corpus/INGEST-NOTES.md`).
  24,017 lines / 7 witnesses ingested and layer-declared; normalizer handles ALTO v4 +
  PAGE XML + TEI-facsimile; abbreviation inventory built; both primers written.
  ⬜ Owed to Wilson: ratify 23 proposed Latin expansions; rule on the Greek Level-2 gap.
  ~~Phase 1 (original scope)~~: Script taxonomy file (`scripts/*.md`, one per family:
  letterform table, abbreviation inventory, 3 dated exemplars with IIIF refs). Ingest
  2–3 HTR-United Latin + Greek datasets into the schema; IIIF fetch of 3–5
  rights-clear witnesses; PAGE XML import/export round-trip. *Opus; no UI yet.*
- **Phase 2 — learner MVP.** Next.js + Supabase (Labs pattern). Script ID → glyph
  cards (SRS) → expand → line with diff. Caroline + Greek minuscule. No accounts
  beyond magic-link; progress + Attempts stored. *Opus for pilot screens, Sonnet for
  the rest once the pattern exists.*
- **Phase 3 — contribution mode.** Double-keying, expert queue, CC BY export,
  public GT release page. *Sonnet/Opus.*
- **Phase 4 — models (funded).** Kraken fine-tunes per script, eval harness, model
  release; feed CER hot-spots back into the curriculum. *Fable to design the eval and
  the funding pitch; Opus to run.*

Order of tracks after MVP is decided by (a) what learners fail at and (b) what Press
needs — early print and Gothic will likely jump the queue for that reason.

## 7. Rulings (Wilson, 2026-08-26)

1. **Papyri:** deferred to Phase 3. Not in MVP.
2. **Free.** Learning is free; the corpus is the asset.
3. **Greek expert queue: Wilson.** No external reviewer dependency for Phase 3.
4. **Landscape survey approved** — Sonnet session, results in `research/landscape-2026-08.md`.
5. ⭐ **Wilson is learner #1.** Part of the product's purpose is to teach *him* paleography.
   Consequence: Phase 1's script taxonomy files (`scripts/*.md`) are written as readable
   primers, not just data — and the Caroline + Greek minuscule tracks are usable by him
   from Phase 1 (static exercises over seed GT) before Phase 2's app exists. Dogfooding
   is the QA.

### Survey findings that amend the plan (`research/landscape-2026-08.md`, 2026-08-26)

- **Gap confirmed open.** No tool gives automatic per-attempt feedback or uses SRS; the
  only Greek+Latin offering is CEU's paid summer course, human-graded. Ancient Lives is
  down for a rebuild. LearnLatin.io (2025–26) is the nearest commercial entrant, Latin-only.
- ⚠ **Greek GT is thin.** Latin is rich (CREMMA, CATMuS ~160k lines, TRIDIS; licences
  mixed, verify each). For Greek the best single seed is the **Palatinus graecus 23**
  GT + models; budget manual curation for the Greek track — Wilson's queue starts in
  Phase 1, not Phase 3.
- ⚠ **IIIF rights harden "free".** Almost every usable repository is CC BY-NC; only
  **Walters is CC0** (prioritise it, plus e-codices PD items). DigiVatLib restrictive;
  BL still degraded post-2023. **Constraint: the exercise bank can never sit behind a
  paywall** — any Phase 3/4 revenue must come from something other than the images.
- Kraken 7.1 / eScriptorium 1.0.0 (2026) — baseline call stands. Transkribus has good
  Greek models (~2.4% CER) but is now paid credits. VLMs show documented hallucination on
  ancient Greek (arXiv:2605.27750) — the VLM route stays a Phase 4 *test*, not an assumption;
  same for "script-specific beats generalist" (directionally supported, no clean benchmark).

## 8. Non-goals

- Teaching Greek or Latin.
- A general-purpose transcription workbench (eScriptorium exists and is free; link to
  it, don't rebuild it).
- Re-hosting restricted images. Deep-link via IIIF, cache crops only where licence allows.
- Training anything before the corpus and eval split exist.
