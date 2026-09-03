# Stroke order — the score for the letter-formation engine

*Wroot Labs · Fable scoping session 2026-09-03 · status: PLAN, nothing built. Execution is
Sonnet work per §9, with one human step (§6) that is Wilson's own. Companion to
`SYRIAC-CALLIGRAPHY-KICKOFF.md` (the research handoff this answers — read its §4 for the five
questions), `SYRIAC-LANGUAGE-PILOT.md` §10 (where the idea was first written down) and
`SYRIAC-WEB-PLAN.md` / `SYRIAC-PDF-PLAN.md` (the two builds this plugs into). This scores
item 2 of NEXT-SESSION.md's "two new ideas".*

**Where the needle is.** Lesson 0 teaches recognition — name the shape, say the sound — and
says nothing about how a letter is *made*. For a Roman-literate adult, "where does the pen
start" is the first real wall of a non-Roman script. The ask, from `SYRIAC-LANGUAGE-PILOT.md`
§10: *a small program that generates an animation of a letter's strokes flowing in order, then a
word's letters flowing and joining — built once as an engine keyed off each script's stroke
data, so it is cheap to point at a new script later.*

**The one rule this plan exists to protect.** *Shape is derived; order is authored; both are
sourced.* The letter's geometry comes out of the font the learner is already looking at
(Noto Sans Syriac, OFL, self-hosted since the PDF build) by a program, never redrawn by hand.
The order and direction of the strokes are a small hand-authored annotation per letter — a
few points per stroke — and every stroke carries `source` and `status` the way every R1 cell
does, because **a wrong stroke order taught confidently is worse than none**
(`reference_paleography-gt-ingest`'s standing worry, verbatim). The engine renders whatever
the annotation says; it has no opinion of its own.

**What this is NOT.** Not handwriting recognition (checking the learner's own strokes —
HanziWriter's quiz mode; §11). Not a nib/pen-angle model — a round-capped centreline, not
calligraphy. Not a historical ductus study of Cod. Syr. 1 or any manuscript — that is a
hand-side consumer this plan leaves a door open for (§2) and does not build. Not a GIF
generator (§4 says why the original word choice is dropped). Not a change to any lesson's
prose beyond the one figure Lesson 0 gains (§7).

---

## 1. What was measured before scoring (2026-09-03, this Mac)

- **Nothing on disk.** `grep -ri 'stroke\|ductus' registry/ scripts/ learn/ quarry/` finds
  only unrelated hits (kickoff §3, re-checked). Greenfield data.
- **The font can give us the shape today.** `learn/fonts/NotoSansSyriac-Var.ttf` (OFL, already
  self-hosted): UPM 1000, one `wght` axis (100–900, default 400), 604 glyphs, of which the 22
  letters have **112 positional glyphs** already drawn (`uni0712.init/.medi/.fina` etc. —
  the joined forms Lesson 0 Part 2 teaches). `fontTools` 4.63 is installed for `python3.11`
  and `SVGPathPen` returns a glyph's outline as an SVG path string directly — verified on
  bēth in all four forms (`uni0712` adv 958, `.fina` 968, `.init` 730, `.medi` 740). The
  plain "Noto Sans Syriac" family is the Estrangela design (`registry/profiles/syriac.toml`
  header), so the animated shape **is** the shape the site draws — the learner never sees two
  bēths.
- **The font cannot give us the order.** An outline is the finished shape: one closed
  contour (or several) with a winding direction that means "fill inside", not "the pen went
  this way". Confirmed by inspection — bēth's outline is one contour; the pen's path is not
  recoverable from it. Kickoff §3's guess was right.
- **Prior art, two families, one architecture.** *HanziWriter* / *Make Me a Hanzi* store per
  character `strokes[]` (one SVG outline path *per stroke*) + `medians[]` (a polyline down
  the middle of each stroke, in the same coordinates) — the renderer animates the median
  clipped by the stroke outline. *strokesvg* (Japanese kana, from the OFL Klee One font) is
  the closer cousin: **font-derived "shadow" shapes + hand-drawn centrelines**, rendered with
  CSS `stroke-dasharray`/`stroke-dashoffset` keyframes, one `--i` delay variable per stroke,
  JS only to restart or scrub. Both separate the data from the renderer; §3–4 borrow exactly
  that split and nothing else (no CJK data transfers).
- **Where the order can come from, for Syriac.** One real printed authority exists:
  **George A. Kiraz, *Tūrrāṣ Mamllā*, vol. I *Syriac Orthography* (Gorgias, 2012, ISBN
  9781463201838), Part II "Graphotactics, Writing, and Ductus" — "presenting the ductus of
  each graph."** In copyright: consult, never ingest; a stroke order is a fact, our geometry
  is ours (§3). HMML School's Syriac lessons defer to Nöldeke/Muraoka for "the basic ductus"
  and are explicitly reader-side, not writer-side; Nöldeke is in the quarry (PD) but his
  alphabet plate prints finished shapes — worth one look, expect nothing. A YouTube
  "Syriac Alphabet Handwriting" video (Estrangela/Eastern/Western) exists as a weak visual
  second witness. **No open stroke-order dataset exists for Syriac.** (Nor Hebrew;
  Devanagari has Wikimedia Commons stroke-order SVG/GIFs; CJK has everything. So for every
  script on `EXPANSION-PLAN.md`'s roadmap the data will be authored here — the engine's
  reuse value is the format and the authoring tool, not shared data.)
- **The Syriacist seat and the order-source are different people.** Ephrem Ishac's CV is
  liturgy + HTR, not calligraphy; Kiraz (Beth Mardutho's founder) wrote the ductus chapter.
  Noted for `NEXT-SESSION.md`'s held-outreach item; no new email is proposed here.

## 2. Which side owns it — the question collapses

The kickoff's central question (`syriac.paleography.app` vs `paleography.app` vs a third
shared thing) assumed two homes. There is one: **this repo already holds both surfaces**
(`site/` = the hand trainer at paleography.app; `learn/` = the language course) and already
has a shared layer both read — `registry/`. So the ruling is not *which project* but *which
directory*, and the repo's own convention answers it:

- **Data → `registry/strokes/<profile>/<hand>/<glyph>.toml`** (e.g.
  `registry/strokes/syriac/estrangela/uni0712.isol.toml`). Sits beside `registry/profiles/`,
  keyed by the same profile id, and the profile gains one pointer:
  `strokes = "registry/strokes/syriac/estrangela"`. A new script adds a directory, not code.
- **Engine → `tools/strokes.py`**, a module with no opinion about lessons: *read a stroke
  TOML → emit an SVG string* (animated or static, §4) and *read a font glyph → write the
  outline stub* (§5). Lives with the other shared tools (`tools/`), imported by
  `learn/tools/make_learn.py` now and by the hand trainer's build later.
- **Consumers, in order:** Lesson 0 (this plan, §7) · the printable Lesson 0 sheet (the
  static figure, free once the SVG exists, §7) · the hand trainer (a "how this letter is
  formed" reveal on a letter — a later plan, not this one; the door is that the trainer
  already reads the profile, so it can find the strokes when it wants them).

The ductus-is-a-reading-fact argument from §10 is honoured by *where the data lives*, not by
building a hand-side feature now.

## 3. The data — one TOML per glyph

```toml
# registry/strokes/syriac/estrangela/uni0712.isol.toml
[glyph]
script  = "syriac"
hand    = "estrangela"
letter  = "ܒ"
name    = "Bēth"
form    = "isol"                      # isol | init | medi | fina
font    = "NotoSansSyriac-Var.ttf"    # the outline's provenance
upm     = 1000
advance = 958
outline = "M240 0Q157 0 110.5 22.0 …" # GENERATED by tools/strokes.py; never hand-edited

[[stroke]]                            # array order = stroke order; point order = direction
median = [[880, 620], [860, 90], [300, 60], [120, 100]]
status = "proposed"                   # proposed | confirmed, exactly as R1 cells
source = "kiraz-2012 II §… (Bēth)"    # or "pen-logic" while unsourced — say so
note   = ""
```

- **Coordinates are font units, y-up**, as `fontTools` emits them; the renderer flips once.
  Nothing is ever converted by hand.
- **`outline` is the whole glyph, not per-stroke outlines.** HanziWriter splits the outline
  per stroke; that split is the expensive hand step and Estrangela does not need it — its
  letters are 1–3 strokes that rarely overlap. The whole-glyph outline is the clip mask
  (§4); a stroke is revealed as a thick round-capped line *inside* the letter. Per-stroke
  outlines are the upgrade if a letter ever looks wrong, not the baseline.
- **A median is 3–8 points.** Not a Bézier; a polyline the renderer smooths. The point of
  the format is that a human can author one in seconds and read one back.
- **`status`/`source` per stroke, not per glyph**, because Kiraz may settle a letter's main
  stroke and say nothing about its dot or its second stroke.
- **Positional forms are separate files** with their own medians, because `.init`/`.medi`
  drop the tail and add the connector — a different pen path, not a shifted copy. The
  authoring tool (§5) seeds a positional form from the isolated one so most of the work is
  moving two points.

## 4. Rendering — inline SVG, animated by CSS, GIF dropped

The original phrasing was "an animated GIF (or equivalent)". Take "or equivalent". A GIF is
a raster of one size, one speed, no replay-on-demand, no scrub, and a bigger file than the
vector it came from; the PDF build already showed the site's consumers want *one source,
many renderings*. So:

- **One function, two modes.** `strokes.svg(glyph, mode="animate"|"static")`:
  - *animate*: `<svg viewBox>` · a faint fill of `outline` as the ghost of the letter ·
    `<clipPath>` from the same outline · one `<path>` per median (smoothed), stroke-width ≈
    the letter's stem (measured from the outline once per font, a profile number), round
    caps/joins, clipped · `stroke-dasharray = pathLength`, `stroke-dashoffset` from full
    to 0 by a CSS keyframe, delay `= var(--i) × (--time + --gap)`. **strokesvg's mechanism,
    re-implemented in ~60 lines, no dependency.** ≤ 40 lines of JS for *replay*, *speed*, and
    a scrub slider that sets `dashoffset` directly. Reduced-motion media query → static mode.
  - *static*: the same SVG, animation off, each stroke drawn in full with a **numbered start
    dot and an arrowhead at its end**. This is the print figure (`SYRIAC-PDF-PLAN.md` ruled
    that formation belongs to item 2 — this is item 2 delivering it) and the thing a GIF
    would have been for.
- **Word mode (v2, §8)** is the same function over a list of glyphs laid out by the font's
  advance widths, RTL, with `--i` continuing across letters so a word draws itself in reading
  order. Joins cost nothing extra: the positional glyphs already contain the connecting
  stroke, so a word is its positional forms placed side by side.
- **If a GIF is ever actually needed** (a social post, an email), rasterise frames of the
  same SVG with the headless Chrome `make_pdf.py` already drives. Not built until asked.

## 5. Authoring — a tool for the hand-authored part

The only hand work is the medians, and the only judgment is stroke order/direction. Both
want a tool, not a text editor:

- **`tools/strokes.py extract`** writes the stub TOML for every letter form from the font —
  `outline`, `advance`, `letter`, `name` filled, `[[stroke]]` empty. Mechanical; runs once
  per font/hand; 134 files for Estrangela (22 isolated + 112 positional).
- **`learn/tools/stroke_author.html`**, a local single page: loads a stub, draws the outline
  large, **click to lay median points, Enter = next stroke, Backspace = undo, ← → = reorder,
  R = reverse direction**, live preview of the animation beside it, "copy TOML" button.
  Authoring a letter is ~1–2 minutes; 22 isolated letters is an hour of someone's time with
  the Kiraz page open. No server, no framework — the same discipline as `drill_shell.html`.
- **Who holds the mouse.** Default: an agent proposes medians for all 22 (from the shape,
  with `source = "pen-logic"`, `status = "proposed"`), then **Wilson corrects order and
  direction against Kiraz** in the tool, changing `source` as he goes. The agent is fast at
  "where is the middle of this stroke"; only a human with the book can say "which stroke is
  first". Skeletonisation (scikit-image, not installed) was considered as the proposer and
  rejected for v1 — it still cannot order or direct, and 22 letters by eye is cheaper than the
  dependency.

## 6. Trust — how a stroke earns `confirmed`

- A stroke is `confirmed` when its order and direction match a named page of Kiraz (or a
  Syriacist's ruling, whenever that seat is filled). Until then it is `proposed`, and
  **Lesson 0 says so to the learner**, once, in one sentence: *this is one common way to form
  the letter; scribes vary, and the point is to have* a *starting place, not the only one.*
  Honest, and true of every script's stroke order.
- The build refuses to render a glyph with zero strokes and warns on any `proposed` stroke
  in a lesson (`make_learn.py --check`, the existing gate), so the count of unsourced strokes
  is visible on every build, never silently zero.
- **The gate that matters is Wilson's pencil (call it G4).** Phase 3 ends with him watching
  each of the 22 animations and copying the letter on paper. If the animation makes the
  formation obvious, it passes; if he has to think, the median is wrong even if the order is
  right. Same instinct as G2 and the PDF's paper gate.

## 7. Where it lands — Lesson 0, and the reference page

- **Lesson 0 Part 1**: each letter's entry gains the figure — static by default (so the page
  reads as a page), *play* on click/hover, with the numbered static figure as the fallback.
  The prose does not change beyond the one-sentence caveat in §6. Generated by
  `make_learn.py` from the strokes directory the profile points at; the Markdown gets one
  marker (`{stroke:ܒ}` or similar) per letter so the figure's position is authored where the
  prose is, not guessed by the renderer.
- **The printable Lesson 0 sheet** gets the static figure per letter beside the existing
  "copy this letter" rule (PDF plan ruling 3 anticipated exactly this).
- **`/letters`** on syriac.paleography.app: one page, all 22 letters, all forms, play-all —
  the reference a learner comes back to from Lesson 3. Cheap once the per-letter figure
  exists; also the public artifact that shows a Syriacist what "stroke order engine" means.

## 8. Phases, in order — each ends in something Wilson can look at

0. **Extract.** `tools/strokes.py extract` → 134 stub TOMLs under
   `registry/strokes/syriac/estrangela/`, profile pointer added, `--check` counts them.
   *Ends in:* a directory that exists and a stem-width number in the profile.
1. **Render one letter.** `strokes.svg()` both modes on bēth with a hand-typed median;
   opened in a browser; reduced-motion checked. *Ends in:* one animated bēth in a scratch
   HTML page.
2. **Authoring tool + proposed medians.** `stroke_author.html`; an agent lays proposed
   medians for the 22 isolated letters. *Ends in:* 22 TOMLs, all `proposed`, viewable in the
   tool.
3. **Wilson's pass (G4).** With Kiraz open, correct order/direction for the 22 in the tool;
   flip `source`/`status`. *Ends in:* 22 letters, each `confirmed` or knowingly `proposed`,
   and his verdict on whether the figures teach.
4. **Wire in.** Lesson 0 figures via `make_learn.py`, the `/letters` page, the static figure
   in `make_pdf.py`. `--check` passes. **Deploy is a hard stop** per the standing rule.
   *Ends in:* live pages.
5. **Positional forms (v1.5).** Medians for the 112 joined forms, seeded from the isolated
   ones; Lesson 0 Part 2 gains the joined figures.
6. **Words (v2).** Word mode; Lesson 1's first words draw themselves. Serto and East Syriac
   are the same six steps over Noto Sans Syriac Western/Eastern when a track wants them.

Phases 0–2 need no book. Phase 3 needs Kiraz on the desk (§10 ruling 2).

## 9. Execution tiers, and the burn

Sonnet throughout — extraction and rendering are pattern work with a verified library;
the authoring tool is a single page; the wiring extends `make_learn.py` the way the PDF
build did. The only judgment-dense step is Phase 3 and it is a human's. Total agent burn is
small (well under any hard-stop threshold); the real cost is Wilson's hour in Phase 3 and
the price of the book.

## 10. Rulings wanted — defaults are stated; a bare "go" takes all of them

1. **Ownership = the registry** (§2): data under `registry/strokes/`, engine in `tools/`,
   Lesson 0 the first consumer, the hand trainer a later one. *Default: yes.* Say no only if
   you want the data somewhere the trainer can never see it.
2. **Order source = Kiraz, *Tūrrāṣ Mamllā* vol. I (Gorgias 2012).** Do you have it? If not,
   buy it before Phase 3 (Phases 0–2 don't need it), or run Phase 3 with `pen-logic` orders
   left `proposed` and let a Syriacist confirm later. *Default: buy it — one book, and it is
   the only printed ductus for all three hands.*
3. **Output = inline SVG, static + animated; no GIF built** (§4). *Default: yes.*
4. **Authoring = agent proposes, Wilson corrects in the tool** (§5). *Default: yes.* Say
   "I'll do all 22 myself" if you'd rather own the medians outright.
5. **v1 scope = 22 isolated Estrangela letters**; joined forms are v1.5, words v2 (§8).
   *Default: yes.*
6. **Geometry = Noto's Estrangela**, not a manuscript hand (§1). *Default: yes*; a
   manuscript ductus is the hand trainer's future feature, not this.
7. **Lands in Lesson 0 per letter AND a `/letters` reference page** (§7). *Default: both.*

## 11. Left out on purpose

- **Handwriting quiz / stroke recognition** (draw it yourself, be scored): HanziWriter's
  second half. Real, and the natural v3 once medians exist — a learner's finger path can be
  compared to the median. Not scoped.
- **Nib and pen-angle modelling**: a calligraphy simulator is a different product.
- **Manuscript ductus** (how the Cod. Syr. 1 scribe actually moved): the hand-side consumer
  §2 leaves a door for. It would need a different order source (a paleographer, or
  Desreumaux on scribal practice, per HMML) and its own status discipline.
- **A shared stroke library for other Wroot projects**: nothing else needs one.
- **Outreach.** Kiraz is a third name for the Syriacist seat; `NEXT-SESSION.md`'s hold on
  that email stands, and `/letters` (Phase 4) is the kind of public artifact it was waiting
  for.
