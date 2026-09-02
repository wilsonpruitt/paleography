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
seyame and diacritic points. ⛔ **Declare the layer per record from the plate — the section
default is wrong for this section.** (Good news for the Estrangela-leads ruling: Nestle
supplies both faces.)

⭐ **CORRECTED 2026-09-01 by the R3(a) Genesis run (records `r3/c067-1` … `r3/c078-1`).** The
sentence above got the *fact* right and the *shape* wrong. It is **not a one-way ramp** off
Serto: within Chrestomathia I the script **alternates with the CAPUT**, and it alternates back.

| Caput | pp. | leaves | layer |
|---|---|---|---|
| I (Gen 1) | 67–70 | n156–n159 | **vocalized Serto** |
| II (Gen 2) | 70–73 | n159–n162 | **unvocalized Estrangela** |
| III (Gen 3) | 73–76 | n162–n165 | **vocalized Serto** |
| IV (Gen 4) | 76–78 | n165–n167 | **unvocalized Estrangela** |

Consequences a later session must not rediscover:
1. **Three pages carry BOTH layers** — 70, 73 and 76 — because the seam is a chapter head, not
   a page break. `layer` on those records is a compound string and the sections are marked
   inside `text_syr_voc`. A schema that assumes one layer per page is wrong for this piece.
2. **Line numbering restarts at every Caput**, and the marginal numeral sits in the OUTER
   margin (right on rectos, left on versos). Caput I runs 1–55, II 1–52, III 1–45, IV 1–51.
   ⛔ A reader who takes the marginals as a single series across the piece will mis-locate
   every line from p. 70 on.
3. **A full chrestomathy page is 20 lines**, not 15; short pages are short because a heading
   or a chapter seam eats the space.

⭐ **Chrestomathia I, Caput IV is from a DIFFERENT WITNESS.** Nestle prints under the head:
`CAPUT IV. (Secundum codicem Ambrosianum seculi fere sexti.)` — Genesis 4 is set from the
Ambrosian codex, not from the base text of chs. 1–3. So for pp. 76–78 a diff against Barnes
compares two witnesses, and a divergence there is a fact about the manuscript tradition, never
a defect in the extraction. (Measured: they agree anyway, almost word for word.)

⚑ **Nestle's square brackets in this piece mark HIS EXEMPLAR'S gaps, not textual doubt.** Six
instances across pp. 70–78 (`[ܐܦܝ̈]`, `[ܠ]`, `[ܠܗ]`, `[ܝ]`, `[ܘ]`, `[ܡܢ ܬܡܢ]`, and once a
supplied punctuation point `[.]`). Every one of them is printed plain and unbracketed in
Barnes. Do not present them to a learner as a variant.

⭐ **CORRECTED 2026-09-01 by the R3(a) Matthew 5 run (records `r3/c079-1` … `r3/c085-1`).**
**Chrestomathia II (pp. 79–85) is unvocalized Estrangela on all seven pages — no vowel sign
anywhere.** Unlike Chrest. I it does not alternate; it sits at the Estrangela pole throughout,
with seyame, letter points, and a linea occultans over the elided letter of the enclitics
(ܗܘܐ, ܗܝ, ܗܘ, ܐܢܐ, ܐܢܬ, ܐܢܬܘܢ, ܐܬܝܬ, ܐܬܐܡܪ, ܡܕܝܢܬܐ) as the only marks. It also carries a
**continuous marginal line-numbering 1–100 across all seven pages** (not restarting per page
the way Chrest. I restarts per Caput) and **no philological footnotes at all**, unlike
Chrest. IV. ⚠ Trap: the superscript `40` at p. 84 line 82 is a *verse* number sitting near the
margin and reads as a line number on a quick glance.

⛔ **A diff between differently-vocalized witnesses is a consonantal diff only.** Chrest. II
(unvocalized) against the BFBS 1905–1920 New Testament (also unvocalized in the base text
used) checks consonants, seyame and numbering — not one vowel point. "Vocalisation outranks
the sense" in the pilot's QA rule presupposes both sides are pointed; it silently does not
apply here. Chrest. I against Barnes 1914 (§ above) is the stronger half of R3(a) for a
pointing check precisely because both are vocalized.

**BFBS *New Testament in Syriac* (`newtestamentinsy00unse`) leaf offset, calibrated 2026-09-01:
leaf = printed page + 11**, fixed on four agreeing pages (n12=p.1 Cap. i; n14=p.3 head
`ܡܬܝ ܓ`; n15=p.4 rubric `Cap. v.`; n18=p.7 head `ܡܬܝ ܘ` carrying Matt 6:9–15). ⚠ This scan's
own `_hocr_pageindex.json` does **not** map one segment to one leaf cleanly — same class of
defect as the `_page_numbers.json` trap already noted for the Nestle scan itself; don't trust
it as the pagination authority.

Glossary and grammar are vocalized Serto as recorded. p. 132 (Menses) is vocalized Serto.

## Flags — unsure, not extracted-to-be-safe

1. ⚑ **p. 132 (n221), *Menses anni syriaci* + *Dies septimanae*.** A bare lexical table (12 month
   names, 7 weekday names, Latin glosses), sitting inside the chrestomathy's pagination but not
   in its ToC list of works. Not a passage (R3) and not a paradigm of forms (R1) as the schema
   means it. **Taken as R1 with a `kind = "lexical-table"` qualifier**, and used as the
   calibration batch's flagged-ambiguous page so the shape gets ruled on before the run.
2. ✅ **Glossary sub-lemmas after `‖` — RULED 2026-09-01 (Wilson): a structured array on the
   parent**, `{voc, gloss_en, gloss_de, raw}`, not separate records. The record count is
   unchanged; the LEMMA count roughly doubles. Measured over the first 18 pages: 253 head
   + 171 sub = 424, i.e. ~1,480 lemmas for the glossary against ~880 records.
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

## Barnes 1914, the Genesis diff target — pagination calibrated 2026-09-01

`ktavadeauritaauk00lees`, 416 leaves. **printed page = leaf − 9.** Two independent agreements,
the same method this map used for Nestle: n10 = p. 1 (Gen 1:1–13, signature `B` at the foot,
Syriac title page at n10's head is actually n10's predecessor n9/n10 pair — the *text* starts
n10) and n11 = p. 2 (running head `ܣܦܪܐ ܕܒܪܝܬܐ` with `I. 14—28` in the outer corner; every
subsequent page carries the same chapter-and-verse running head, which makes the offset
self-checking). Genesis 1–4 = leaves **n10–n17**. Barnes prints unvocalized Estrangela with
seyame, verse numbers in the outer margin against the line on which a verse opens, `*` between
verses and `❖` at a paragraph close.

⛔ Consequence for the R3 method: **Barnes can check the consonantal text, the seyame and the
verse numbering, and it cannot check a single vowel.** On the Serto pages (67–70, 73–76) the
pointing rests on the plate read alone and still owes a blind control on a sample. On the
Estrangela pages the diff is like-for-like and is the strongest check anywhere in R3(a).

## Model records

Copy these shapes; do not re-derive them from the schema prose.

| Record type | Model file | What it proves |
|---|---|---|
| R1, big paradigm | `r1/p044-1.toml` | landscape-plate handling; `uncertain` on a cell, not the file |
| R1, split on category | `r1/p023-1.toml` + `r1/p023-2.toml` | one printed page → two records, because the enclitics are a different category and are not even a table |
| R1, lexical table | `r1/p132-1.toml` | the `kind = "lexical-table"` qualifier, and Nestle's own brackets |
| R3, keyed + independently diffed | `r3/c067-1.toml`, `r3/c079-1.toml` | full `text_syr_voc` + `[alignment].diff` against a PD edition the passage's CONTENT was already known from |
| R3, keyed cold, partial | `r3/c087-1.toml` | word-slot segmentation + contact-sheet tiling; confident vs. flagged readings side by side, unread lines marked, nothing invented |
| R3, structural only, text NOT READ | `r3/c108-1.toml` | the honest ceiling: full provenance/witness/layer capture with `text_syr_voc` left unkeyed rather than guessed, per `reference_arabic-control-rule` |
| R4 | `r4/g171-neshab.toml` | lemma/pos/gloss pair, `sub_lemmas`, empty `frequency_rank` |

⛔ **TOML ordering trap, paid for once:** put every top-level key BEFORE the `[source]` table.
A bare key written after a table header belongs to that table, so `lexeme = …` placed under
`[source]` silently becomes `source.lexeme` and the file still parses. Every model file above
has `[source]` last.

## R3 — RUN COMPLETE 2026-09-01, 65 pages + the Lord's Prayer, yield is NOT uniform

Full detail and the reasoning behind each finding → `SYRIAC-LANGUAGE-PILOT.md` §7a
("R3(a) part 1/2", "R3(b) part 1/2"). Census, for anyone sizing a lesson before reading that:

| Piece | pp. | pages | text yield | control strength |
|---|---|---|---|---|
| Lord's Prayer | 70–72 | 1 record | **fully keyed + diffed** | independent PD (BFBS) |
| Chrest. I, Genesis 1-4 | 67–78 | 12 | **fully keyed + diffed** | independent PD (Barnes 1914) |
| Chrest. II, Matthew 5 | 79–85 | 7 | **fully keyed + diffed** | independent PD (BFBS) |
| Chrest. III, Vitae Prophetarum | 86–107 | 22 | **~37% confidence-weighted** (250/435 lines read, 104 confident) | sense-only, Latin (Schermann) |
| Chrest. IV, Historia inventionis | 108–131 | 24 | **0% — text NOT READ, structural fields only** | self-diff only, not independent (Nestle's own De sancta cruce) |

⛔ **Read this before scoping a lesson (§6):** only the first 20 pages (Lord's Prayer + Genesis
+ Matthew) are lesson-ready real text with an independent check behind them. That alone clears
§6's "ten lessons" bar. Vitae Prophetarum and Historia inventionis are not a smaller version of
the same task — they are a different, currently-open problem (unknown text, no digital edition,
unvocalized) needing a Syriacist seat or a Serto HTR pass before their `text_syr_voc` can be
trusted at scale, not more of the same extraction effort.

## Measured cost and the full-run estimate

→ `research/syriac-pilot-phase1-calibration.md`. Headline: **4.7k vision + 1.5k output tokens
per page measured over 8 pages; 201 pages ⇒ ~1.43M tokens irreducible I/O.** ⚠ That estimate
assumed uniform full-transcription yield across the chrestomathy; R3's actual run (above) shows
the assumption held only for the 20 pages with known content behind them — the unknown-text
pages cost roughly the same tokens for a fraction of the yield.

## R1 Step 1 — plate locations for `SYRIAC-R1-RUNBOOK.md`'s nine targets, run 2026-09-02

Located from the scan's own hOCR text index (`_hocr_pageindex.json.gz` + `_hocr_searchtext.txt.gz`,
re-fetched fresh — **not kept on disk**, same disk-discipline as `corpus/raw`), text only, no
plate images pulled. Confirms `leaf = page + 17` holds through the whole Morphology zone
(pronoun records already on disk are `p023-*`, matching leaf n40 exactly) and section headers
OCR cleanly enough to place every target, even where the paradigm grid itself OCRs to noise.
**Result: nine targets collapse onto five leaves, and two guesses in the runbook were wrong —
in the direction of LESS work, not more.**

| target (runbook's list) | printed p. | leaf | plate / section head found |
|---|---|---|---|
| Noun + possessive-suffix set | 34 | n51 | §31 "NOUN WITH SUFFIXES" — single page, matches runbook's guess |
| Peal imperfect | 43 | **n60** | §38 "STRONG VERBS" — see correction below |
| Peal perfect, bare | 43 | **n60** | same plate as imperfect |
| Peal imperative | 43 | **n60** | same plate |
| Peal infinitive | 43 | **n60** | same plate — confirms runbook's "probably folded into the main table" |
| Peal participle, active + passive | 43 | **n60** | same plate |
| Noun plural emphatic + seyame rule | 31 | **n48** | §29 "EMPHATIC STATE" — full sing/plur × abs/cstr/emph grid |
| Construct state | 31 | **n48** | SAME plate as above — see correction below |
| Numerals: cardinals + ordinals | 36–37 | n53–n54 | §33 "THE NUMERALS" — cardinal table on n54, inflected/construct forms discussed on n53 |
| Preposition + pronominal suffix table | 63–64 | n80–n81 | §49 "PARTICLES" — location only; OCR too garbled here to confirm table vs. prose, needs the actual plate |

**Two corrections to the runbook's "likely location" guesses:**
1. **Peal perfect bare is NOT "the same plate as p044 minus its suffix columns" — it is a
   separate plate, one page earlier.** p.43 (leaf n60, headed "38. STRONG VERBS") is a full
   strong-verb synopsis grid — bare Peal perfect, imperfect, imperative, infinitive, and
   participle (active + passive) all in one table, immediately BEFORE p.44's "39. STRONG VERB
   WITH SUFFIXES" (`r1/p044-1.toml`, already on disk). So five of the nine targets are one
   single plate, not five separate pulls.
2. **Construct state is not a separate table from the plural-emphatic one — same grid.** §29's
   summary table (p.31, "Sing. Plur. / st. abs. and cstr. / st. emph. / st. abs. / st. cstr.
   st. emph.") already carries the construct-state column for both numbers. One plate covers
   both targets.

**One target demoted out of R1 entirely:** "Adjective agreement pattern" is not a paradigm —
p.68 (leaf n85, §55 "NOUN") is prose in **III. Notes on the Syntax (§§50–56)**, discussing
attributive-adjective word order. It belongs with the runbook's open syntax-note question
(relative ܕ, prohibition ܠܳܐ, etc.), not as an R1 lexeme+cells record. Not resolving that
routing question here — just correcting its target type.

**Net effect on Step 2's dispatch:** the nine-target list now needs plate reads on **five or
six leaves** (n48, n51, n53, n54, n60, and n80–81 pending confirmation), down from the
runbook's own "~6–10 leaf fetches" estimate for Step 1 locating — and Step 2's actual
transcription work is smaller than nine separate paradigm pulls would suggest, since two
plates (n48, n60) each answer multiple targets at once. Preliminary token estimate before
Step 2 dispatch, quoting the measured rate per `research/syriac-pilot-phase1-calibration.md`
rather than re-guessing: **6.2k tokens/page irreducible I/O measured on grammar-zone-adjacent
pages, ~2× end to end ⇒ roughly 12–15k tokens/page.** Six leaves (treating n80/n81 as one
target read across two pages) ⇒ **very roughly 75–90k tokens on Opus**, likely higher if the
two multi-column grid plates (n48, n60) need the same two-crop halving `p044-1`'s table did
rather than one read each — actual figure still wants a real crop-count check on those two
plates before Wilson's go, not a guess dressed as a number. This is still Step 1 (locate);
Step 2 (extract) has not run and will not without a "which model, and go?" per the runbook's
own hard stop.
