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

## ⛔⛔ 9. Two calibrations that both look right when assumed and are both wrong

**2026-08-27, fetching Wien ÖNB Cod. 940's images from IIIF** (`research/onb-cod940-iiif.md`,
`corpus/sources.yml`). The GT ships with no images; the manuscript is digitised; joining the
two needs two numbers, and guessing either quietly ruins the result.

### The leaf → canvas offset

The manifest has **290 canvases and the TEI has exactly 290 surfaces**, which invites
`canvas = leaf`. Verified against stated image dimensions instead:

| offset | exact dimension matches |
|---|---|
| −2 | **125 / 125** ✅ |
| 0 | 88 / 125 |
| −1, +1 | 0 / 125 |

⚑ **Offset 0 matches 88 of 125 pages.** A spot check of two or three pages would have
passed, and 37 pages would have been silently cropped from the wrong folio. Calibrate
against every page you can, not a sample — and prefer a check the data can fail.

### The coordinate scale, which is not uniform

The TEI records **2479×3508 for 137 of the 262 GT-bearing pages**. That is a **Transkribus
placeholder, not a real size**: the canvases at those leaves run from **566 to 1320 px
wide**. Those pages were uploaded stretched to a fixed size, so `x` and `y` must be scaled
**independently** (`sx = canvas_w/tei_w`, `sy = canvas_h/tei_h`). The other 125 pages carry
real dimensions and map 1:1.

⚑ **A uniform image size repeated across 165 pages of a hand-photographed manuscript is a
placeholder.** Real photography does not produce identical dimensions.

⚑ Both classes were settled the only way that settles anything here: **fetch one line
region from each and read it against its transcription.** Both came back correct.

⭐ Worth noting for the curriculum, not just the pipeline: Cod. 940 is **continuous prose in
a clean hand**, far gentler than the Eutyches glossed grammar with its 300 lines a page. It
is the better beginner text, and it was the one we could not use.

## ⛔⛔⛔ 10. I committed the error in §1 myself, and my "evidence" was the tell

**2026-08-27.** `corpus/sources.yml` declared Wien ÖNB Cod. 940 `layer: diplomatic`, with
`layer_evidence: "line-break hyphen ¬ preserved (1790x)"`.

**The probe, run only after a plate raised a doubt:**

| sign | occurrences in 7,889 lines |
|---|---|
| `ꝑ ꝓ ꝗ ꝰ ᷑ ÷ ⁊ ł đ` | **0** |
| combining tilde, `ũ ã õ ĩ` | **0** |

**A ninth-century Latin manuscript cannot contain no abbreviations.** They were all resolved
silently. Confirmed on the plate: the ink of `0159_p159` reads `sca` (stroked) and `ē`; the
transcription writes `sancta` and `est`. **wien940 is `expanded`.**

⚑⚑ **The evidence I recorded was about lineation and said nothing whatever about
abbreviation.** It pointed the way I already believed, so I accepted it. §1 of this very file
says to verify the layer with a character probe; I wrote that sentence and then did not run the
probe. ⭐ **The rule is not "check the layer" — it is "check the layer WITH EVIDENCE OF THE RIGHT
KIND". Evidence about one property is not evidence about another, however confidently filed.**

## ⚠ 11. Ground truth from a teaching workshop is not finished ground truth

Cod. 940's GT comes from an **HTR Winter School**, and the opening pages show it. Leaf 6's
first text line is transcribed `scrminiomin puti etnetatioer inri`; **the ink plainly reads
`Nouum opus facere me cogis ex vete[ri]`** — the opening of Jerome's preface to the Gospels.
No expansion policy explains that; it is uncorrected machine output. The display-script heading
lines above it are garbled the same way (`INIET EPSOSDIA HERNM` for *INCIPIT EPISTOLA
HIERONYMI*).

**Where the damage is, measured rather than assumed:** seven body lines sampled from across the
manuscript (leaves 30, 32, 37, 58, 93, 159, 224) were **7/7 correct**. The failures cluster in
the front matter and in display capitals, exactly where an ATR model is weakest and a
workshop's correctors got least far. The bank therefore ships `leaf >= 30` and no all-caps
lines — 7,641 of 7,889 — and the shipping selection was sample-verified against the plates.

⛔ **A statistical detector did not find this and cannot.** A character-bigram model trained on
known-good Latin ranked the garbage line **1607th of 7,869** — while its ten "worst" lines were
all *correct*: `HVCVSQVE VI · NVNC V ·`, Eusebian canon references, penalised for not being
running prose. **Every one of its top findings was a false positive and the true error was
invisible.** The same shape as [[reference_plate-read-triage]]: frequency evidence is worthless
against well-formed text, and only the plate settles it.

⭐ **The correction improved the product.** An expanded text with no abbreviation signs is the
*right* first Latin track — the learner meets letterforms alone — with the diplomatic,
abbreviation-rich grammar as the second. The ramp now mirrors the layer field: **expanded
before diplomatic**, in Latin as in Greek.
