# Ingest notes — traps found in the seed ground truth

*Phase 1, 2026-08-26. Every item here was hit for real while ingesting four datasets.
These are the reasons `tools/ingest.py` has the guards it has.*

## ⛔⛔ 1. The declared transcription layer can be WRONG in the catalogue

**HTR-United's `transcription-guidelines` for the Palatine Anthology (CPgr23) says
"we do not resolve the abbreviation, except when they are non ambiguous."
The dataset's own README says "All abbreviations have been transcribed in expanded
form." The README is right and the catalogue is wrong** — verified in the data:

| probe | count | meaning |
|---|---|---|
| `ϗ` (kai) | **0** | no abbreviation signs survive |
| `ȣ` (ou) | **0** | " |
| `ς` final sigma | **0** | final sigma not distinguished (README says so explicitly) |
| `,` `.` `;` | **0** | all punctuation collapsed |
| `·` interpunct | 3,437 | …to this one sign |

⚑ **Never take the layer from the catalogue. Read the dataset's own README, then verify
with a character probe.** A layer mislabel is the one error that silently corrupts both
the exercise bank (learner marked wrong for typing what is on the page) and any future
training set (model taught to expand when it was supposed to transcribe).

⚑ Corollary already applied: `corpus/sources.yml` records `layer` **and** `layer_evidence`
— never a bare assertion.

## ⛔ 2. One repository is often SEVERAL manuscripts

`Eutyches` looks like one dataset. It is four witnesses — VLO41 (Leiden Voss. Lat. O.
41), Lat7499 (BnF), BambergMsc30, Lat14087 — plus, in `kraken-YALTAi/test/`, a
**held-out test set from a fifth, foreign manuscript** (Bodl. Auct. F.4.32).

⚑ A naive `rglob("*.xml")` merges all five under one witness label **and eats the test
set**, destroying the train/test split before it exists. Always scope with `--include`.

## ⛔ 3. Concatenated aggregates duplicate the entire dataset

`Eutyches` also ships `XML-XSLT/out/allALTOS_lat7499.xml` (5,691 lines) and
`VLO41_allALTOS.xml` (2,744 lines) — every page of the witness merged into one file,
sitting beside the per-page GT.

Ingesting both **doubled the corpus silently**: first naive run reported 24,256 lines,
correct scoped run reports 12,314.

⚑ `ingest.py` now treats a **page key appearing in two files as fatal**. That single
guard catches traps 2 and 3 together.

## ⚠ 4. The declared FORMAT can be wrong

The catalogue says Wien ÖNB Cod. 940 is `Page-XML`. It is **TEI** (Transkribus TEI
export: `<l facs="#zone">` joined to `<zone>` coordinates in `<facsimile>`). Hence
`ingest.py` sniffs the root element and never trusts the metadata.

## ⚠ 5. Declared volumes are approximate — reconcile, don't assume

| dataset | declared | ingested | note |
|---|---|---|---|
| CPgr23 | 3,374 lines | **3,374** | exact ✓ |
| Wien 940 | 7,835 lines | 7,889 | +54; TEI `<l>` includes some non-GT lines |
| Rescribe Caroline | 457 lines | 440 | −17; empty-content lines skipped |
| Eutyches | "65 pages" | 135 pages / 12,314 lines | declared count badly understates it |

⚑ An exact match (CPgr23) is evidence the parser is right. A mismatch is a question,
not a defect — but it must be *asked*, and the answer recorded.

## ⚠ 6. A dense page is not necessarily a parser bug

Lat7499 averages 191 lines/page, max 313. That looked like a bug. It is **real**: the
page is a glossed grammar manuscript — on f74v, 132 `MainZone` lines and **181
`MarginTextZone`** lines of commentary in tiny script.

⚑ Two consequences: (a) `region_type` must survive ingest (it does) or main text and
marginal gloss become indistinguishable; (b) **glossed pages must not be drawn for
Level-3 line exercises without filtering by region** — a learner asked to "read this
line" would get a 4-word scrap of marginal gloss.

## ⚠ 7. MUFI private-use codepoints, and why guessing them is not allowed

The Latin GT uses Medieval Unicode Font Initiative private-use codepoints. They render
as tofu without a MUFI font (Junicode, Andron) and carry no Unicode name.

⛔ **I guessed four of them from context and got three wrong**:

| codepoint | my guess from context | actual (chocomufin `table.csv`) |
|---|---|---|
| U+F1AC | `;` = -que/-bus sign | ✓ LATIN ABBREVIATION SIGN SEMICOLON |
| U+E8A3 | *vel* or *id est* | ✗ **LATIN ABBREVIATION SIGN AUTEM** |
| U+E8B3 | *ergo* | ✗ **Q LIGATED WITH R ROTUNDA** (= "qr") |
| U+F1E6 | *est* | ✗ **THREE DOTS WITH COMMA POSITURA** (punctuation) |

The contexts were suggestive and the reasoning was decent. It made no difference —
same lesson as `reference_plate-read-triage`: **a good argument is not evidence.**

⚑ Eutyches ships `table.csv`, a **chocomufin** character-control table (169 rows)
that resolves every special character authoritatively. Look for one before reading a
single glyph by eye.

## ⚠ 8. Character control resolves IDENTITY, not EXPANSION

chocomufin's `ontographe` column gives an expansion for only **4** of the 64
characters that occur ≥20 times. It answers *what glyph is this*, not *what does it
stand for*.

⚑ **No dataset in the seed ships a complete diplomatic→expanded mapping.** The Level-2
abbreviation table is ours to author — see `corpus/latin-abbreviations.json`, where
`expansion_verified` (4, sourced) is kept strictly apart from `expansion_proposed`
(23, mine, **awaiting Wilson's ratification**) and 37 with no expansion yet.

⚑ And expansion is **context-dependent**: the `;` sign is *-que* after `q`
(`cuiusq;` = cuiusque) but *-bus* after `b` (`dieb;` = diebus). The abbreviation model
cannot be a flat character map.
