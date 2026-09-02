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

**2. "Align, don't transcribe" does not hold for this volume — but the reason is a missing
*carrier*, not a missing right.** §5 makes alignment the method and full transcription the
exception. In fact every chrestomathy page is a full plate transcription, because:

- The Digital Syriac Corpus (the one CC BY 4.0 source) is patristic and does not hold the Bible.
- ⭐ **SEDRA's verdict was too broad and is corrected** (Wilson, 2026-09-01): SEDRA carries the
  **BFBS/UBS 1905 Peshitta NT — Pusey-Gwilliam gospels (1901), Gwilliam Acts, Gwilliam-Pinkerton
  Paul, Gwynn Catholic Epp. + Rev. — all published 1905 and therefore PUBLIC DOMAIN.** A faithful
  transcription of a PD text carries no new copyright. So **the text is shippable; SEDRA's
  lemmatization and morphology are not.** Their terms remain a contract on their own files, so
  carry the text from a PD edition rather than re-exporting theirs.
- But no clean fetchable carrier of that text was found. **ETCBC/peshitta** (Text-Fabric) looked
  ideal and is not: it is the OLD Testament, OCR'd from the **in-copyright Leiden 1987 edition**,
  and the repository declares **MIT while its own `about.md` declares CC BY-NC**. ⛔ That is the
  **third** two-licences-in-one-repository trap this project has hit — Cod. 940, Cod. Syr. 1, now
  this. STEPBible-Data (CC BY 4.0) surfaced no Syriac module; syri.ac 403s to automated fetch and
  wants a human. Candidate PD scan, **not yet probed**: archive.org `newtestamentinsy00unse`
  (⚠ verify the edition at the title page, never by the ID digits). The Peshitta **OT** has no
  clean carrier at all now that Leiden is out, and wants a PD printed edition — Lee 1823, Urmia
  1852, or Mosul 1887-92.
- The *Vitae Prophetarum* and *Historia inventionis* (44 of the 66 pages) have no digital text
  anywhere under any licence, and no printed critical edition to check against either.

⭐ **The reframe this opens: we produce the digital text rather than consume one.** Nestle's
chrestomathy is itself a printed Peshitta, PD since 1889. Keying Genesis 1-4 and Matthew 5 out of
it yields PD Syriac digital text nobody has released cleanly — an asset, not a cost. And it
recovers most of what alignment was for: **key from Nestle, check against SEDRA and the 1905
scan, ship neither**, which is exactly what a compute-only source permits. Alignment was never
about saving keystrokes; it was about having something to diff against.

⛔ **The real division inside R3 is therefore not the licence line:**

| Piece | pp. | control (all PD) | strength |
|---|---|---|---|
| I Genesis 1-4 | 67-78 | Barnes, *Pentateuchus Syriace*, BFBS 1914 | Syriac ↔ Syriac, independent |
| II Matthew 5 (+ Lord's Prayer p. 70) | 79-85 | BFBS *NT in Syriac* 1905-1920; Pusey-Gwilliam 1901 | Syriac ↔ Syriac, independent |
| III *Vitae Prophetarum* | 86-107 | Schermann 1907 — **Latin of the Syriac** Sinai Syr. 10, + name index | sense only, **but in Latin** |
| IV *Historia inventionis* | 108-131 | **Nestle's own *De sancta cruce*, 1889** | Syriac ↔ Syriac, **not independent** |

⭐ **Revised 2026-09-01, twice, on Wilson's pointers.** The claim that 44 pages were "checkable
by nobody but a Syriacist" was wrong. Every page of the chrestomathy has a PD control; the two
weak spots are opposite and neither is fatal. III has an independent witness in a language we
can read but no Syriac. IV has the Syriac but no independence — Nestle lifted the piece out of
his own book the same year, so agreement proves we keyed *Nestle* right, not that Nestle keyed
the manuscript right. Details and the evidence for the *De sancta cruce* identification:
`research/syriac-peshitta-editions.md`.

⭐ **The consequence for the expert seat:** the Syriacist is no longer a precondition for R3.
Piece IV self-checks, pieces I and II diff against independent PD editions, and piece III is
checkable in Latin by Wilson.

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
  a blob and loses the keying. Proposal in `r3/c070g-1.toml`: `word_notes = [{ index, form_voc,
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
2. **Not "does R3 run" any more — "does R3 run FIRST".** The Peshitta text is PD, so the 23
   Peshitta pages are keyable now and checkable against SEDRA and a PD scan. Doing them first
   produces the diff target the rest of the pilot has been assuming it could fetch, and proves
   the keying workflow on the one text where a wrong reading is catchable. The other 44 pages
   (*Vitae Prophetarum*, *Historia inventionis*) have no check but a Syriacist and are the
   natural thing to hold. Splitting R3 that way is a different shard plan, not a smaller one.
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
- **The PD carriers were searched, not exhausted.** syri.ac is the best index and refuses
  automated fetch; `newtestamentinsy00unse` is unprobed. Both are cheap, and both are worth doing
  before the shard plan is fixed.
- The weekday list on p. 132 was read at page magnification only and is flagged `uncertain` as a
  whole (`r1/p132-2.toml`).
- Step 3 (blind control + ratio checks) is not started; it belongs after the run.
