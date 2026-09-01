# Syriac pilot, Phase 1 — Step 0 + Step 1 record

*Run 2026-09-01, per `SYRIAC-PHASE1-RUNBOOK.md`. Step 0 (structure map) is complete and is in
`quarry/nestle-1889-en/MAP.md`. Step 1 (calibration batch) is complete for 8 pages. This file
carries the measurement and **the hard stop**. Step 2 has NOT been dispatched.*

## What was produced

`quarry/nestle-1889-en/` — 34 records from 8 pages, every file parsing under stdlib `tomllib`:

| | pages | records |
|---|---|---|
| R1 paradigms / lexical tables | pp. 23, 44, 132 | 5 |
| R2 composed exercises | — | **0** (see `r2/README.md`) |
| R3 chrestomathy passages | pp. 67, 70, 87 | 3 |
| R4 glossary entries | pp. 133, 171 | 26 |

Batch composition follows the runbook: 3 grammar (paradigm plate p. 44, small table + prose
p. 23, the "exercise" p. 70), 2 chrestomathy (pp. 67, 87), 2 glossary (pp. 133, 171), 1
flagged-ambiguous (p. 132).

## Three findings that change what Step 2 is

**1. Nestle has no R2 at all.** The runbook and the pilot both sized R2 at "low hundreds". The
volume's one apparent exercise is the Lord's Prayer in the Peshitta. R2 comes from Robinson or
from nowhere.

**2. R3 has nothing to align against, so "align, don't transcribe" does not hold for this
volume.** §5 of the pilot makes alignment the method and full transcription the exception. In
fact: the Digital Syriac Corpus (the one CC BY 4.0 source) is patristic and does not hold the
Peshitta; SEDRA is COMPUTE-ONLY by Phase 0's own verdict; and the Vitae Prophetarum (22 of the
66 chrestomathy pages) has no digital text under any licence. **Every chrestomathy page is a
full plate transcription.** Phase 0's fallback — key a PD printed Peshitta ourselves — is on
the critical path, not in reserve. This is the single biggest driver of the estimate below.

**3. The glossary, not the grammar, is the volume.** 63 dense pages at ~18-20 head-lemmas each
≈ **1,150-1,300 R4 records**, plus roughly 400 `||` sub-lemmas if those become records of their
own. The pilot expected "low hundreds". It is an order of magnitude out, and at one file per
record it is ~1,300 files in one directory.

Two smaller ones, both already folded into `MAP.md`:

- **Phase 0's layer note for the chrestomathy is wrong, and instructively so.** p. 67 opens in
  fully vocalized Serto; by p. 71 the same Genesis passage is running in unvocalized Estrangela.
  Nestle ramps the reader off the vowels *inside one passage*. Declare the layer per record; the
  section default is not a shortcut here.
- **A fifth record shape exists.** The "Aids to Translation" on pp. 70-72 are per-word notes
  keyed to a position in a passage, carrying § cross-references — a ready-made gloss layer of
  exactly the kind the hand-trainer already ships per line. R3's `primer_notes` flattens it into
  a blob and loses the keying. Proposal in `r3/c070-1.toml`: `word_notes = [{ index, form_voc,
  note, noldeke }]`, or a record type R5. **This one is owed BEFORE the run** — it changes what
  the run extracts, not just how it files it.

Also owed at G1, from contact with the schema: `gloss_de` (Nestle glosses German | English, §4
has `gloss_en` only), the primer's own `§` cross-reference, and fields for the Greek etymon,
Hebrew cognate and Nestorian variant that R4 entries carry as a matter of course.

## The measured rate

Measured on this batch, not assumed. Vision tokens are computed from the actual pixel
dimensions after the API's 1568px long-edge resize (w×h/750); output is the TOML actually
written.

| Page type | pages in batch | image reads/page | vision tokens/page |
|---|---|---|---|
| Grammar, prose + inline table | 2 | 1 | **2.0k** |
| Grammar, **landscape paradigm plate** | 1 | 6 | **9.2k** |
| Chrestomathy, vocalized Serto | 1 | 4 | **5.5k** |
| Chrestomathy, unvocalized Estrangela | 1 | 1-4 | **2.1k** read, ~5.5k to key |
| Glossary | 2 | 3-4 | **6.5k** |
| Flagged lexical table | 1 | 3 | **3.4k** |

- **Batch total: 37.3k vision tokens over 8 pages = 4.7k vision tokens per page.**
- **Output: 36.4 KB of TOML over 8 pages ≈ 12k tokens = 1.5k output tokens per page.**
- **Irreducible I/O = 6.2k tokens per page.**

⚠ **Why the landscape plates cost 4× a normal page.** pp. 44-45 are printed rotated 90°. At the
scan's 1598×2604 the pointing is unreadable as a whole page; it takes a rotate plus four
overlapping 2× tiles plus a header band to assign 70 cells to the right row and column. Only
two pages in the volume are like this, so it does not move the total — but it is the shape to
expect wherever a primer prints a fold-out paradigm.

## The full-run estimate

Extraction set = **201 leaves** (grammar 72, chrestomathy 66, glossary 63).

| Zone | pages | tokens/page | subtotal |
|---|---|---|---|
| Grammar prose + tables | 70 | ~4k | 280k |
| Landscape paradigm plates | 2 | ~12k | 24k |
| Chrestomathy (full transcription — finding 2) | 66 | ~7k | 462k |
| Glossary (~20 records/page — finding 3) | 63 | ~10.5k | 660k |
| | **201** | | **≈ 1.43M tokens irreducible I/O** |

Reasoning and carried context are not in that figure and are not measurable from this batch. On
the shape of this session — where the careful part is deciding what a mark is, not emitting it —
**assume roughly 2×**, giving **≈ 2.5-3.0M tokens end to end on Opus**. The 1.43M is measured;
the multiplier is an assumption and is stated as one.

Sharding, if it goes: by section, glossary first (it is the bulk, it is the most uniform, and it
is the one whose per-page rate this batch measured twice).

## ⛔ HARD STOP — Wilson's call

**Decomposing the rest of Nestle is ~200 pages at a measured 6.2k tokens/page of I/O — 1.43M
tokens irreducible, ~2.5-3.0M end to end. Model = Opus, per the pilot §9. Which model, and go?**

Three things ride on the same answer, and the third may be the real one:

1. **The R5 / `word_notes` ruling** (finding 5). It changes what the run extracts. Cheap to
   answer, expensive to retrofit.
2. **Whether R3 goes at all in this phase.** With no alignable digital Peshitta, 66 chrestomathy
   pages (462k tokens, a third of the run) are full keying of pointed Syriac with nothing to
   diff against. Deferring R3 to a phase that has a PD Peshitta keyed, or a Syriacist, cuts the
   run by a third and removes its least checkable third.
3. ⚠ **The Syriacist seat is still empty, and this batch is what that costs.** Every Syriac
   string in these 34 records is extractor output that nobody qualified has ruled on; the ones
   I could not resolve carry `uncertain = true`, but that flag is my judgement too. The Step-3
   blind control catches transcription slips — it does not catch a systematic convention error,
   which is exactly what [[feedback_blind-reader-fact-vs-rule]] warns about. Running 200 more
   pages before the seat is filled multiplies unchecked output by 25×.

   The people to ask are already named in `NEXT-SESSION.md` — **Ephrem Aboud Ishac** and
   **Christine Roughan** — and there is already an unsent email owed to them about the Cod. Syr.
   1 / Cod. 940 licence conflict. One message covers both.

## Not done, and why

- **pp. 67 and 87 were identified and layer-declared but not keyed.** Keying them under a method
  that had just been shown not to apply would have buried finding 2. The records say so on their
  face (`extraction.status`).
- The weekday list on p. 132 was read at page magnification only and is flagged `uncertain` as a
  whole (`r1/p132-2.toml`).
- Step 3 (blind control + ratio checks) is not started; it belongs after the run.
