# What the seed ground truth can and cannot teach

*Phase 2 scoping, 2026-08-27. Determined by inspecting the data, not by assumption.*

## The constraint that decides the MVP

**The seed ALTO carries exactly one `<String>` per line** — no word-level and no
glyph-level boxes. Checked in both tracks:

```
eutyches/VLO41/GT/alto/f02r.xml   line 1 -> 1 String: "INCIPIT LIBER EVTI"
cpgr23/data/CPgr23/cpgraec23_0234 line 1 -> 1 String: "ἄρτεμι· σοὶ δὲ κυνῶν …"
```

⚑ So of PLAN.md's levels, only **Level 3 (line transcription)** can be built from the
seed as it stands:

| level | exercise | buildable now? | what it would need |
|---|---|---|---|
| 0 Script | script identification | yes, trivially | more scripts in the bank |
| 1 Glyph | glyph → letter cards | ❌ | glyph boxes: forced alignment or manual annotation |
| 2 Abbreviation | sign → expansion cards | ❌❌ | word boxes **and** the expansions (23 still unratified) |
| **3 Line** | **read the line, diff** | ✅ **built** | — |
| 4 Page | layout, regions | partly | region polygons exist; needs a page-level UI |

⚑ **Level 1 is unblocked by a tool, Level 2 by a ruling.** Glyph and word boxes can be
produced by forced alignment (Kraken can align a known transcription to a line image
and emit per-character positions) — that is a Phase 2b task with a known method. Level
2 additionally needs Wilson's ratification of the expansions in
`latin-abbreviations.json`, and for Greek it needs a diplomatic witness we do not have.

## Cropping: three things learned the hard way

**1. Crop from the BASELINE, not the polygon.** Source polygons are sometimes
self-intersecting — an eScriptorium artifact. One spur turned a 46 px line into a
189 px bounding box, and the height-normalising downscale then crushed the text to
an unreadable smear. Baselines are present on every witness that has images
(wien940 has baselines for 0 of 7,889 lines, but it has no images either).

**2. Rotate first, then band.** Cropping a band around a *tilted* baseline and rotating
afterwards adds the baseline's own vertical run to the band height — that turned a
46 px line into a 133 px crop carrying its neighbours with it. Rotate about the
baseline midpoint, then take the horizontal band: same line, 77 px, clean.

**3. Sizing the band: the polygon is unusable whole and indispensable in part.**
Wilson caught display capitals being decapitated — `INCIPIT LIBER EVTI` opens the book in
letters ~260 px tall on a page whose median line gap is 46 px, so a `1.25 × line-height`
ascender cut the tops off the N and C.

Three fixes were tried; the two failures are the useful part.

- *Raise the multiple globally* — drags neighbouring lines into every ordinary crop.
- *Find blank rows above the ink* — fails outright. This parchment is mottled and densely
  written; the row-ink count never approaches zero, so a display line and a small one both
  came back 195 px.
- ✅ *Median per-column polygon extent.* The bounding box is unusable (one spur inflates a
  46 px line to 189 px) but the polygon is the only thing that knows a display line really
  is tall. Take the vertical extent **column by column**, then the median: a spur occupies
  a few columns and is voted out, a genuinely tall line is tall in nearly every column.
  Measured — spurred line: bbox 189 → median band **77** (true); display line: bbox 263 →
  median band **177** (true).

⚑ An ink-profile fallback survives for lines with no usable polygon, and it looks for a
**local minimum that then rises**, never for darkness in absolute terms: between two lines
the count dips (77) and jumps again as the next line begins (231). The shape of the
profile is the signal, not its level.

⚠ On a page written 46 px apart with 77 px-tall letters the GT polygons themselves overlap
their neighbours, so a correct crop still shows slivers above and below. That is the page,
not the tool.

**4. Line height comes from the page, not the line.** Robust estimate = median gap
between consecutive baselines on that page (46.5 px on VLO41 f02r, over 75 lines).

## Images: one witness is unusable

| witness | GT pages | page images on disk |
|---|---|---|
| cpgr23 | 70 | **70** ✅ |
| eutyches-VLO41 | 63 | **63** ✅ |
| eutyches-Lat7499 | 39 | **39** ✅ |
| rescribe | 17 | **17** ✅ |
| **wien940** | 262 | **0** ❌ |

⛔ **wien940 is our largest Latin set (7,889 lines) and has no images at all** — it is a
Transkribus TEI export of transcriptions only. It cannot produce a single exercise
until the ÖNB page images are fetched (IIIF). That is the largest single win available
in Phase 2b: it would roughly triple the Latin bank.

Coordinates were checked against image dimensions on 6 pages per witness — no overflow,
so GT coordinates and on-disk images are at the same resolution. (This is a real trap
elsewhere; it happens not to bite here.)

## The trainer

`tools/build_exercises.py` → `build/exercises.json` → `tools/make_trainer.py` →
`build/scriptorium.html`, a self-contained page (3.0 MB, images inlined as data URIs).

Design decisions that are pedagogy, not styling:

- **The Greek diff always normalises `ς` → `σ`**, in strict mode too. The witness does
  not distinguish final sigma; penalising a learner for correct modern habit would be
  teaching them the dataset's convention as if it were the manuscript's.
- **Scoring is over the alignment length, not the truth length.** Otherwise an inserted
  character is free — `uerbXum` for *uerbum* scored 100%.
- **Alignment is a Levenshtein backtrace**, so a single dropped letter shifts nothing
  downstream. A naive index-by-index compare marks the whole rest of the line wrong.
- **A character palette is provided**, because a learner cannot type `ꝓ` or `᷑` on a
  normal keyboard. The cpgr23 team built an eScriptorium virtual keyboard for exactly
  this reason; it is a real part of transcription practice, not a convenience.
- **"Ignore accents & punctuation" defaults ON** for a first sitting; strict mode counts
  every point.

⚠ **Private-use (MUFI) codepoints do not render in any web font.** The current 45-line
Latin selection happens to contain none, but any wider selection will. Either filter
them at build time or ship a MUFI font (Junicode) as a data URI.

## Abbreviation glosses in the reading stages (2026-08-27)

Wilson: *"gonna need more context when we get to these abbreviations. during stage one, if
there is a strange abbreviation, let's have a paragraph under it explaining it."*

⭐ **This is where Level 2 actually lives, and it needs no word boxes either.** The earlier
note said abbreviation training was blocked on segmentation. It is not: a sign can be
*explained in prose beneath the line it occurs in*, which teaches it in the place a learner
meets it. Segmentation is needed only for a standalone flashcard deck, which is a much
later and much less useful thing.

`corpus/abbreviation-glosses.json` carries one entry per sign — expansion, mechanism,
a worked example from this very corpus, and a `status`. The bank attaches to each line
the glosses for the signs it contains; the trainer shows them in stages 1–3 and withholds
them at stage 4.

⚠⚠ **`status` is rendered, not just stored.** 11 of the 15 glosses are `proposed` (mine,
from standard convention) and display a red **not yet ratified** chip; only 4 are
`verified` against a source. A learner is never shown an unratified expansion as though it
were settled. This is the same discipline as `latin-abbreviations.json` and it must survive
any future edit to the table.

Mechanism follows Thompson 1912 ch. VII: **contraction** keeps the word's ending so the
inflection survives, **suspension** cuts it off and destroys it — which is why `᷑` = *-ur*
is worth flagging to a reader (it is what makes a verb passive).

## Two smaller corrections from the same sitting

**Round and square brackets: ✅ SETTLED BY PLATE READ, 2026-08-27** —
`manual-review/eutyches-parentheses-plate-read.md`. They are **the editors' supply where
the ink cannot be read**, confirmed on four plates with four different physical causes
(mould staining · worn ink · a gloss too faint to read · a tear that has taken the
parchment away). **In no instance does a bracket correspond to an abbreviation sign**, so
the hypothesis that mattered — that a learner should be hunting for a sign in the ink — is
refuted 4/4, consistent with the dataset's own "abbreviations preserved" guideline.

So the lines are **readmitted, flagged `damaged`**: shown in stage 1 with a verified gloss
explaining the damage, withheld from stages 2–4 where the learner is asked to type letters
that are not on the page.

⚠ **Two of my own claims here were wrong and are corrected in the plate-read record.** I had
written the brackets were "mostly at line openings, lost at the page edge": in fact **37 of
66 are mid-line**, and the one line-opening case I read is nowhere near the page edge — it
starts at x=1141 of a 3406-px page, and the loss is a tear in the middle of the leaf. ⛔ The
first cut of that plate *looked* like edge loss only because **my own crop box clipped it
52 px before the line**. A plate cut too tight can manufacture the evidence it was meant to
test; widen before concluding.

**Delivered image width raised 1400 → 2200 px cap** (median crop now ~1720 px, was 1400).
The crops were never the limit — the source pages are 3305 × 4186 — but a 1400 px image
shown at ~1070 CSS px on a 2× display was being upscaled 1.5×, which reads as softness.
It now upscales ~1.2×. Bank is 4.4 MB, well under the 16 MB artifact ceiling.

## The enlarged opening initial (2026-08-27)

Wilson, on the first line of the Latin I track: *"i am confused on the very first character.
is the qu merged here or cut off?"*

**Neither — and it is a real feature of the page, not a defect.** A new section opens with a
**large decorated capital set out in the margin**, clear of the ruled text block and two lines
deep. **The scribe does not write the letter twice.** So the ordinary script begins with the
second letter: the line reads *uaeritur quod cooperantur*, the tall rubricated **Q** beside it
supplies the first, and together they are *Quaeritur*.

The crop was cutting the initial off, because the GT polygon covers only the ordinary script.
`extend_for_initial()` now scans leftward for a band of ink within the line's vertical extent
and reaches out to include it. **72 of 400 Cod. 940 crops carry one.**

Two calibrations, both bought by a failure:

- **The gutter tolerance had to go up to 1.5 × line height.** At 0.6 the scan stopped short of
  a Q sitting 50 px clear of its own line — *an initial is deliberately set apart from the text
  it opens*, so the usual inter-word logic is exactly wrong here.
- **The reach is gated on the transcription starting with a capital.** Without that test the
  line *below* grabs the initial, because a two-line-deep letter hangs beside it too —
  measured: `euangelii non difficile…` came back carrying the Q belonging to `Quaeritur`.

The trainer now **explains it** rather than leaving it to be puzzled out: a `verified` gloss
fires on any line whose crop reached for an initial.

## Editorial marks typed as literal text

Cod. 940 has **59 lines carrying `<del>` / `<add>`** — Transkribus editorial marks the
transcribers typed as plain angle brackets, which were then escaped into the TEI as text:
`di<del>f</del>ficile`, `ca<add>no</add>num`. They are notes *about* the text rather than the
text, and no learner can type them. Filtered out in `is_sentence`.

⚠ **A process note worth more than the fix.** My first attempt at this filter silently did
nothing: the anchor string it patched had been removed by an earlier edit, the `assert` fired
inside a heredoc, and because the commands were newline-separated rather than `&&`-chained the
shell carried on and reported success. **It was caught only because the verification step
asserted on the output** rather than trusting the build. Assert on the artifact, not on the
step that made it.
