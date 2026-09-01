# Nestle 1889 (Kennedy tr.) — structure map

*Step 0 of `SYRIAC-PHASE1-RUNBOOK.md`, run 2026-09-01. Scan `syriacgrammarwit00nestiala`,
302 leaves. Leaf n = the `…/download/syriacgrammarwit00nestiala/page/n<LEAF>.jpg` index.*

## How this map was built

The scan ships its own **hOCR page index** (`_hocr_pageindex.json.gz` + `_hocr_searchtext.txt.gz`),
which gives per-leaf OCR text and therefore every running head and printed page number in one
cheap fetch. Section boundaries were read off the running heads, then **checked against the
volume's own Table of Contents (n14–n17)** and confirmed on the plate for the two boundaries
that OCR could not be trusted on. ⛔ The archive's `_page_numbers.json` is OCR-guessed and is
**wrong at n90–n91** (it continues the grammar sequence into the Litteratura); do not use it as
the pagination authority. The Table of Contents is.

## Sections

| Leaves | Printed pp. | Offset | Section | In extraction set |
|---|---|---|---|---|
| n0–n3 | — | — | Williams & Norgate advertisements | ❌ filler |
| n4–n5 | — | — | Title page, library stamp | ❌ |
| n6–n13 | vi–XII (roman) | leaf = p + 1 | Preface to the German edition + English preface | ❌ filler |
| n14–n17 | XIII–XVI | leaf = p + 1 | **Table of Contents** | ❌ (but it is the pagination authority) |
| **n18–n86** | **1–69** | **leaf = p + 17** | **Grammar §§1–56** | ✅ **R1 zone** |
| **n87–n89** | **70–72** | leaf = p + 17 | **Reading Exercise (Matt. 6, 10–13) + Aids to Translation** | ✅ **R2 zone** |
| n90–n155 | 1–66 | leaf = p + 89 | **Litteratura Syriaca** (bibliography, 4 parts) | ❌ **named filler** |
| **n156–n220** | **67–131** | **leaf = p + 89** | **Chrestomathia** (4 works, 6 sub-pieces) | ✅ **R3 zone** |
| n221 | 132 | leaf = p + 89 | *Menses anni syriaci* + *Dies septimanae* | ⚠ flagged — see below |
| **n222–n284** | **133–195** | **leaf = p + 89** | **Glossarium** | ✅ **R4 zone** |
| n285 | — | — | Drugulin colophon | ❌ |
| n286–n301 | 1–7 (3rd seq.) | — | Publisher's catalogue | ❌ filler |

**Extraction set = 201 leaves:** n18–n89 (72), n156–n221 (66), n222–n284 (63).

### Pagination — calibrated, not spot-checked

**Two arabic sequences, not three.** Grammar is `leaf = page + 17`. **One single second sequence
(`leaf = page + 89`) spans the Litteratura, the Chrestomathia AND the Glossarium** — the
chrestomathy does *not* restart. Six independent agreements, from the Table of Contents against
the running heads:

| ToC entry | printed p. | predicted leaf | head found there |
|---|---|---|---|
| Litteratura I | 3 | n92 | `Litteratura. 3` |
| Chrestomathia I (Genesis) | 67 | n156 | `CHRESTOMATHIA. / I. QUATTUOR PRIMA CAPITA GENESEOS` ✅ plate |
| Chrestomathia II (Matt. 5) | 79 | n168 | `II. EVANGELII MATTHAEI CAPUT QUINTUM` |
| Chrestomathia III (Vitae Prophetarum) | 86 | n175 | `III. VITAE PROPHETARUM` |
| Chrestomathia IV.3 (Vat. syr. 148) | 127 | n216 | `3) e Cod. Vat. syr. 148 (a. Chr. 1267)` |
| Menses anni syriaci | 132 | n221 | `132  Menses anni syriaci` ✅ plate |
| Glossarium (running head) | 171 | n260 | `Glossarium. 171` |

⚠ **Why the chrestomathy *looks* unpaginated.** Its pages carry their number in **Syriac
numeral letters**, centred at the head (verified on the n160 plate), so the OCR reports no page
number and the printed arabic number is absent. The sequence is unbroken underneath. Arabic
numerals resume at p. 132. **Never infer a restart from a missing number.**

## Contents of the extraction zones

**Grammar (R1 zone), by ToC:** §1 Introduction p.1 · I. Orthography & Phonology §§2–18 pp.2–22
(alphabet p.4, vowel scheme p.5, numerical signs p.18) · II. Morphology §§19–49 pp.23–64
(pronoun 23–24, noun 24–38 incl. numerals §33 36–38, verb §§34–48 39–63, **strong-verb paradigm
plates pp.44–45**, particles §49 63–64) · III. Notes on the Syntax §§50–56 pp.65–69.

**Chrestomathia (R3 zone), by ToC — 4 works, 6 sub-pieces:**

| # | Work | pp. | leaves |
|---|---|---|---|
| I | Quattuor prima capita Geneseos | 67–78 | n156–n167 |
| II | Evangelii Matthaei caput quintum (*ex editione Americana*, Litt. nr. 65 c) | 79–85 | n168–n174 |
| III | Vitae Prophetarum (e tribus codd. Mus. Brit.) | 86–107 | n175–n196 |
| IV.1 | Historia inventionis sanctae crucis — cod. Paris. 234 | 108–112 | n197–n201 |
| IV.2 | — cod. Mus. Brit. Add. 14644 | 113–126 | n202–n215 |
| IV.3 | — cod. Vat. syr. 148 | 127–131 | n216–n220 |

**Glossarium (R4 zone):** pp. 133–195, single column, alphabetical by Syriac letter. Entry =
vocalized Serto lemma · gram. abbrev. (`m.`/`f.`/`impf. a`/`Pa.`/`Ethpe.`) · optional `§ NN`
back-reference into the grammar · **German | English** gloss pair separated by a pipe · optional
Greek etymon, Hebrew cognate (`h.`), Nestorian variant (`nest.`). Sub-lemmas follow `||`.

## ⚠ Layer — Phase 0's note needs amending

Phase 0 recorded the chrestomathy as *unvocalized Estrangela* from the n180 probe. On the plates
it is **mixed, and the mix is pedagogical**: n156 (Genesis, p. 67) opens in **fully vocalized
Serto**; by n160 (p. 71) the same Genesis text is running in **unvocalized Estrangela** with
seyame and diacritic points. Nestle ramps the reader off the vowels and off Serto inside one
passage. ⛔ **Declare the layer per record from the plate — the section default is wrong for
this section.** (Good news for the Estrangela-leads ruling: Nestle supplies both faces.)

Glossary and grammar are vocalized Serto as recorded. p. 132 (Menses) is vocalized Serto.

## Flags — unsure, not extracted-to-be-safe

1. ⚑ **p. 132 (n221), *Menses anni syriaci* + *Dies septimanae*.** A bare lexical table (12 month
   names, 7 weekday names, Latin glosses), sitting inside the chrestomathy's pagination but not
   in its ToC list of works. Not a passage (R3) and not a paradigm of forms (R1) as the schema
   means it. **Taken as R1 with a `kind = "lexical-table"` qualifier**, and used as the
   calibration batch's flagged-ambiguous page so the shape gets ruled on before the run.
2. ⚑ **Glossary sub-lemmas after `||`.** One entry frequently carries derived nouns and other
   stems. Own record, or a repeated field on the parent? Decided at calibration; whichever way,
   it moves the R4 count by a factor of ~2.
3. ⚑ **Grammar pp. 1–22 (§§1–18)** are prose about script and sound with only three real tables.
   Kept in the read set (the tables are R1 and the § numbers are the glossary's cross-reference
   targets), but expect a low record yield per page — this is not a shard to judge the rate by.
4. ✅ Not flagged, decided: the Hebrew/Greek cognates *inside* glossary entries are part of the
   entry and are captured. The runbook's "comparative-philology digression" exclusion means the
   Litteratura and the prefaces, which are excluded whole.

## Expected counts — the sanity check for the run

| Record | Pilot §2 expectation | This volume's estimate | Basis |
|---|---|---|---|
| R1 paradigms | dozens | **40–70** | 3 tables in §§2–18 + the morphology paradigms §§19–49 over pp. 23–64 |
| R2 exercises | low hundreds | ⚠ **1–3** | Nestle prints **one** composed exercise (Reading Exercise, pp. 70–72) |
| R3 passages | dozens | **65** | one record per chrestomathy page, n156–n220 |
| R4 glossary | low hundreds | ⚠ **~1200–1300** | 63 pages × ~20 head-lemmas (n222 plate), before the `||` ruling |

⛔ **Two of the four expectations are off, and both matter to the plan, not just to the count.**

- **R2 is not in this volume.** Nestle 1889 is a descriptive grammar with a chrestomathy, not an
  exercise primer; the whole R2 body has to come from **Robinson** (which is why Robinson's
  keylessness was Phase 0's question). Phase 1 should not be sized as if Nestle supplies R2.
- **R4 is an order of magnitude above "low hundreds"** and is the volume's real bulk — 63 dense
  pages against 72 grammar pages that are mostly prose. The glossary, not the grammar, is what
  the burn estimate turns on.

Both fold back into `SYRIAC-LANGUAGE-PILOT.md` §2 at the G1 gate.

## Model records

Copy these shapes; do not re-derive them from the schema prose.

| Record type | Model file | What it proves |
|---|---|---|
| R1, big paradigm | `r1/p044-1.toml` | landscape-plate handling; `uncertain` on a cell, not the file |
| R1, split on category | `r1/p023-1.toml` + `r1/p023-2.toml` | one printed page → two records, because the enclitics are a different category and are not even a table |
| R1, lexical table | `r1/p132-1.toml` | the `kind = "lexical-table"` qualifier, and Nestle's own brackets |
| R3, keyed | `r3/c070-1.toml` | layer + `transliteration_primer` + the schema-gap note |
| R3, identified but not keyed | `r3/c067-1.toml`, `r3/c087-1.toml` | `[extraction] status/reason` — the honest shape when alignment is impossible |
| R4 | `r4/g171-neshab.toml` | lemma/pos/gloss pair, `sub_lemmas`, empty `frequency_rank` |

⛔ **TOML ordering trap, paid for once:** put every top-level key BEFORE the `[source]` table.
A bare key written after a table header belongs to that table, so `lexeme = …` placed under
`[source]` silently becomes `source.lexeme` and the file still parses. Every model file above
has `[source]` last.

## Measured cost and the full-run estimate

→ `research/syriac-pilot-phase1-calibration.md`. Headline: **4.7k vision + 1.5k output tokens
per page measured over 8 pages; 201 pages ⇒ ~1.43M tokens irreducible I/O.**
