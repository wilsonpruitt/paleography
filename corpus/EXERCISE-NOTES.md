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

## The spotlight — showing context without competing with it (2026-08-27)

Wilson, on the crop that now included the initial: *"that first letter dwarfs everything else
and brings up other lines. this will be a continual problem so we need a way to show the first
one but keep the eyes on the top line and not be confused. if we could blur the other lines."*

He is right that it is continual, and it was never only about initials: **on a page written
46 px apart in letters 77 px tall, every crop carries bleed from its neighbours.**

Three approaches, and the first two are both wrong:

| | |
|---|---|
| **Hard mask** (white outside the polygon) | Erases an initial that lies outside the line's polygon, and cuts neighbours off mid-stroke, which reads as damage to the page. |
| **Leave it** | The eye has nothing to tell it which line is the subject. |
| ✅ **Spotlight** | Everything stays visible and in place; only the target line is in focus. Neighbours blur and wash toward the parchment. |

`spotlight()` takes polygons or rectangles in crop coordinates, feathers the mask so nothing
looks cut out, and composites the sharp original over a blurred-and-faded copy. It runs on
**both** crop paths:

- `crop_line` — the target polygon, **plus the initial's strip** where one was found, so the
  initial stays in focus with the line it belongs to.
- `crop_baseline` — the polygon's median band, so the bleed at the top and bottom of the band
  recedes. This is the dense-page case and the one that needed it most.

⚑ **The convention is stated in the orientation** rather than left to be discovered: the soft
material is really on the parchment, it is not a bad scan and nothing is being hidden — it is
out of focus so the eye knows where to sit. Without saying so, the next report would rightly
have been "the image quality got worse".

⭐ Side effect: the payload got **smaller** (4.9 MB → 4.3 MB). Blurred regions compress well.

## Giving the initial its full height (2026-08-27)

Wilson, on the spotlit crop: *"with capitals we will have to show 2-4 lines to get the full
character. so we still spotlight, but more space."* He was right — the crop was still one line
band tall, so the Q was cut off at the waist.

`find_initial()` now measures the initial's **vertical** extent as well and the crop grows to
fit; the spotlight keeps the line *and* the whole initial in focus while the extra lines that
come into view recede. On Cod. 940 f. 30 that is a 809 × 223 crop — the full decorated Q with
its tail, the line it opens sharp along the top, three faded lines beneath.

Three measurement traps, each found by looking at the numbers rather than the picture:

**1. The page edge saturates the profile.** The strip runs from the initial out to the text, and
on this page it reached the dark binding edge. Judged against *that* peak, the Q's own strokes
looked weak and the hollow of its bowl looked like a gutter. Measured column densities: page
edge 53–71, Q strokes 30–40, **Q bowl 1–12**, true gutter **0**. ⚑ **Only the gutter is actually
empty**, so ink is now *any* column with a mark in it, not one above a fraction of the peak.

**2. The vertical run must be contiguous with the line.** Taking every inked row in the strip
measured **6.3 line-heights** — it was collecting other lines' marginalia sharing those columns.
Now it expands up and down from the line itself and stops at a gap.

**3. Bounds, because the detector will still be wrong sometimes.** Sampled across 14 pages, the
run-based measurement gave a median of **5.07** line-heights and a minimum of **0.43** — both
impossible for a decorated initial. An initial in this hand is ~1.5–3.5 lines deep and ~1–2.5
wide; outside that, **reject**. Of 25 capital-initial lines sampled, **4 survive**, at 2.6–3.8
line-heights. ⚑ A capital at the start of a line does not imply a decorated initial, and a
rejected detection merely crops the line normally — no worse than before — whereas a six-line
crop is actively worse.

## Two glosses a reader asked for, and why one of them needed a new trigger (2026-08-27)

Wilson, reading Stage 1: *"merging the e and et at the end of suplet is unique and deserves a
gloss"* — the ink reads `ſupl&` where the print says *suplet* — and *"the spacing between words
in paleography deserves a gloss as well since that is what trips up neophytes like me a lot of
the time."*

**The et-ligature.** `&` began as a ligature of *e* and *t*, and in a manuscript it has not yet
narrowed to meaning only the word *et*: the scribe uses it for **the letters e-t wherever they
fall**, including word-finally. Distinct from the Tironian `⁊`, which is shorthand for the
*word* and never supplies a syllable.

⛔⛔ **This exposed a structural hole, not a missing entry.** Glosses fired on characters
present in the text — but **Cod. 940 contains 0 literal `&` in 7,641 lines**, because it is an
*expanded* witness and the editors resolved every one. **An expanded transcription has, by
definition, edited out the very signs a learner needs explained.** A character trigger can
never fire on them.

⚑ So glosses now also accept a **regex trigger keyed on the expanded spelling**: `&` fires on a
word of four or more letters ending `-et` (2 of 44 lines — *suplet*, *habet*, *manet*). And the
orientation for any expanded track now lists, up front, **the marks that appear in the ink and
nowhere in the printed line** — `&`, the nasal stroke, contracted words like `ſca`/`ē`, `ę`,
the line-break `¬` — so the mismatch reads as a convention rather than an error.

**Word division.** *Scriptio continua* had no spaces at all, and by the ninth century the job is
only half done: short words cling to their neighbours and gaps open inside long ones. The ink of
one Stage 1 line reads `quarequomodolongitudinem` for *Quare quomodo longitudinem*.

⚑ Trigger choice mattered here. Firing on any line with a common short word gave **35 of 44** —
accurate but useless as a repeated note. Two adjacent short words gave 24. **Three** adjacent
gives **6 of 44**, which marks the genuinely hard lines. The general statement lives in the
orientation, where it is always available; the gloss flags the cases.

## Polygons under-cover the right-hand end too

Same sitting: *"the last r of the phrase is cut off."* On Cod. 940 f. 41 the polygon stops at
**x=1090** while `mensuratur` runs on to about **x=1230** — a 140 px shortfall. This is the
opening-initial failure at the other end of the line, and it takes the same remedy:
`extend_right()` measures where the ink actually stops rather than trusting the box, capped at
three line-heights and ended by a real word gap.

⚑ The extended tail is added to the **spotlight's** in-focus shapes as well. Without that, the
newly recovered letters would come back blurred — rescued from the crop and then hidden by the
very device meant to make the line clear.

## Reading all of Stage 1: one bug class, four faces (2026-08-27)

Wilson read the whole of Latin I stage 1 and then all of Greek, reporting as he went. His
summary was the useful part: *"the only issues were the first letter crops so if we fix that,
they all read fine."* Four separate reports, one cause.

**The GT polygons under-cover the line on every side.** Measured on 65 lines of Cod. 940: the
median line has **77 px of its own ink outside the polygon on the left**, p90 **120 px** —
routinely a whole letter. It cost the `d` of `dus`, the `I` of `In principio`, the `r` of
`mensuratur`, and — in the other code path — the first letter of Greek lines.

| face | remedy |
|---|---|
| left clipped | `extend_left()` — short reach, ends at a real word gap |
| right clipped | `extend_right()` |
| tall letters faded at their extremes | **dilate the spotlight mask** — the long `I` of `Iohannis` reaches past the band, so the device meant to clarify was hiding it |
| Greek clipped | the same measurement in `crop_baseline` — the baseline starts only ~3 px inside the polygon there, so the polygon was no help |

⚑ Both recovered ends are added to the **spotlight's in-focus shapes**. Twice now the fix for a
crop bug would have been undone by the blur: letters rescued from the crop and then hidden.

⚑ Mask dilation is blur-then-threshold, not `MaxFilter` — a MaxFilter that wide is ~2,200
operations per pixel.

## Glosses a reader asked for, and one that never fired

From the same sitting: **`¬`** (the line-break mark: the word continues below, and the break
falls wherever the margin arrives), **`&`**, **word division**, and for Greek **`κ` written in
two strokes** — an upright and a detached arc that commonly do not meet, which until you expect
it reads as two unrelated marks. That one was magnified and verified on the page.

⛔ **The word-division trigger never fired on Greek and nobody noticed for two builds.** Its
regex was `[A-Za-zÀ-ſ]` — a Latin-only character class. Greek letters are not in that range, so
the gloss silently matched nothing on the track where word division is just as hard. Now
`[^\W\d_]`, which is Unicode-aware. ⚑ **A trigger that fires zero times looks exactly like a
trigger for a phenomenon that is absent.**

⚠ **Two Greek letterform glosses ship as `proposed`, not `verified`** — the alpha riding high on
a rho, and omega closing into a figure-eight. Both are Wilson's observations and both are
plausible, but **Pal. gr. 23's images are not sharp enough at letter scale for me to confirm
them**, and a gloss that says *verified* must mean I read the source. They say so on their face.

## Capping the glosses

Greek letterform triggers are common by nature: omega fires on 23 of 44 lines, kappa on 21. Four
explanations under one line is a wall of prose, not help. Glosses are now capped at **three per
line, keeping the rarest** — the ones a reader has least chance of having met already. Latin
averages 0.5 per line, Greek 1.8.

## Glosses move to a sidebar once there is something to type (2026-08-27)

Wilson, on reaching stage 2: *"could we move the gloss to the side bar so i can input the word
and still see the image."*

The gloss sat between the printed line and the typing box, which is right for **stage 1** — pure
reading, full width, nothing competing — and wrong for every stage after it. With a box to type
in, a block of prose in the middle pushes the image and the input apart, so **the reader loses
sight of the ink at exactly the moment they need it.**

From stage 2 the working area becomes a two-column grid: plate and printed line and input on the
left, glosses in a **sticky** right-hand column that stays put as the page scrolls. Below 900 px
it falls back to stacked, since a 330 px sidebar beside a manuscript line is worse than nothing.

⚑ The general rule this is an instance of: **an explanation belongs beside the work when the
reader is producing, and beneath it when the reader is only looking.** The same content in the
same order can be a help or an obstruction depending on what the stage asks for.
