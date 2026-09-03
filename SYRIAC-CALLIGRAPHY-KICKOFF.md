# Calligraphy / stroke-order engine — kickoff brief, not a plan

*Written 2026-09-03 (Sonnet, prep work) so the actual scoping session opens with context
loaded instead of re-deriving it. **The scoping itself is Fable-shaped work, not Sonnet's**
— per `~/.claude/CLAUDE.md`'s model-prudence rubric, this is a greenfield architecture
decision that will outlive Syriac (see §2), the same shape as `SYRIAC-WEB-PLAN.md` and
`SYRIAC-PDF-PLAN.md`, both scored on Fable before a cheaper session played them. This file
is the research handoff; it makes no rulings.*

---

## 1. The problem, verbatim from where it was first raised

`SYRIAC-LANGUAGE-PILOT.md` §10 (second deferred idea) and `NEXT-SESSION.md` item 2, both
2026-09-02: Lesson 0 currently teaches shape *recognition* — name a letter, hear its sound
— and says nothing about how the letter is actually *formed*, stroke by stroke. For a
Roman-alphabet-literate adult, a non-Roman script's pen mechanics are genuinely opaque:
where does the stroke even start? The proposed shape is a generation **engine**, not a
library of hand-drawn animations — something that takes per-letter stroke data and
produces an animated sequence (a letter's strokes flowing in order, then a word's letters
flowing and joining), so a future script inherits it as configuration rather than
bespoke artwork.

## 2. Why this is cross-project, not a Syriac-only build

`EXPANSION-PLAN.md`'s band-1 roadmap already commits to Hebrew, Coptic, Sanskrit's
Devanagari, and Syriac's own Serto/East Syriac hand variants — every one hits the same
"where does the pen start" wall. `SYRIAC-LANGUAGE-PILOT.md` §10 also raises, without
deciding, whether this belongs on the **hand-reading side** (`paleography.app`) as much as
the language-learning side — ductus (stroke order and direction) is a manuscript-reading
fact a reader benefits from knowing, not only a handwriting-practice fact, even though
`PLAN.md` §3's exercise types currently teach recognition only, never formation. That is
the central open question this needs to settle (§4 below), and it's exactly the kind of
call that compounds — get the ownership wrong and every future script's stroke data lands
in the wrong repo, or gets duplicated across both.

## 3. What already exists to build on — checked in this session, not assumed

- **No stroke-order data exists anywhere in the repo.** Searched `registry/`, `scripts/`,
  `learn/`, `quarry/` for "stroke" or "ductus" — the only hits are unrelated (Cappelli
  abbreviation glyphs, crop-tool comments about page edges, a Lesson 7 gloss about a raised
  stroke marking a plural). This is a genuinely greenfield data problem, not a matter of
  surfacing something already captured.
- **The registry pattern this should probably extend.** `registry/profiles/<id>.toml`
  (e.g. `syriac.toml`) already carries per-script config — direction, exercise scoring,
  which marks count as letters, a `fold` table for positional variants — that the trainer
  reads generically rather than hardcoding per script (`paleography.md` memory: "a new
  script needs no CSS rule written for it by hand"). A stroke-order engine keyed the same
  way (`registry/profiles/<id>-strokes.toml` or a `[strokes]` table within the existing
  profile) would fit the repo's own established convention rather than invent a new one —
  worth testing that fit explicitly rather than assuming it, since letterform GEOMETRY is a
  different kind of data than the scoring/normalisation config the profile currently holds.
- **Lesson 0's decoding drills are the one existing prototype of "generate, don't
  hand-author."** `learn/syriac/LESSON-0.md` Part 3 (referenced in `SYRIAC-LANGUAGE-PILOT.md`
  §10's *first* deferred idea, the drill-generation engine) generates nonsense strings and
  asks for the reading — the same "build a generator once, not examples by hand" instinct
  this idea shares, though the two ideas are otherwise independent (one drills recognition
  at scale, this one teaches formation).
- **Meltho and Noto Sans Syriac are the two fonts already licensed and in use** (Meltho:
  redistribute-yes/modify-no per `research/syriac-pilot-phase0.md`; Noto: OFL, now
  self-hosted under `learn/fonts/` for the PDF build per `SYRIAC-PDF-PLAN.md` §4). Neither
  font file encodes stroke *order* — a font's glyph outline is the finished shape, with no
  notion of which contour was drawn first or in what direction. Whatever stroke-order data
  this needs will not come from the fonts already on hand; it has to come from somewhere
  else (see §4).

## 4. Open questions the scoping session needs to settle — not decided here

1. **Which side owns it**: `syriac.paleography.app` (language learning), `paleography.app`
   (hand-reading, where ductus is a reading fact), or shared machinery neither project
   depends on directly (a third small repo/package, the way the registry pattern is shared
   config rather than code duplicated into each track)? §2's ductus-is-a-reading-fact point
   argues for the hand side or shared; the pedagogical framing (a beginner learning to
   write) argues for the language side. Both are real, and the answer likely determines the
   repo layout more than anything else here.
2. **Where does the stroke-order DATA come from**, per letter, per script-hand variant
   (Estrangela first, but the answer needs to generalize)? Candidates, none evaluated yet:
   hand-authored control points/paths per letter (accurate, high one-time cost, doesn't
   scale to new scripts without a human who knows that script's calligraphy); derived
   *heuristically* from an existing font's glyph outline via contour segmentation (cheap
   per script, but a font's outline is the finished shape and doesn't encode direction or
   order — this may not be recoverable without a ground-truth source); or sourced from an
   existing calligraphy pedagogy reference for the script in question (a manual, a
   handwriting primer) — closer to how `PLAN.md`'s corpus work already treats primers as
   ground truth, but existence and licensing per script is unknown and would need the same
   discipline as any other source ingest (`reference_paleography-gt-ingest.md`'s standing
   worry about baked-in wrong assumptions applies here too — a wrong stroke order taught
   confidently is worse than none).
3. **Output format.** The original framing says "an animated GIF (or equivalent)" — worth
   treating "or equivalent" as a real option, not a hedge. An animated GIF is simple to
   generate and embed but is a dead end for interactivity (no scrubbing, no replay-on-hover,
   fixed speed, larger file for a looped animation than a vector path would need). An SVG
   path animation (CSS `stroke-dashoffset` or the Web Animations API) driven by the same
   underlying per-stroke path data can do everything a GIF does plus scrubbing, hover-to-
   replay, speed control, and crisp rendering at any size, at the cost of being JS-driven
   rather than a static asset — closer in spirit to how the drill engine already works than
   to a generated image. Worth deciding deliberately rather than defaulting to the original
   word choice.
4. **Prior art worth evaluating, not adopting sight unseen**: HanziWriter (open-source,
   MIT-licensed JS library for CJK stroke-order animation) solves a structurally similar
   problem — canonical per-character stroke path data plus an animation/quiz engine built
   on top — for a script family with a much larger and more standardized body of existing
   stroke-order data (CJK stroke order is heavily documented; Syriac calligraphy stroke
   order is not, as far as this session found). Its *architecture* (separate the path data
   format from the rendering/animation engine) may be worth borrowing even if none of its
   data or a data source shaped like its `.svg` corpus format transfers to Syriac. The
   scoping session should look at how it structures data before assuming a format.
5. **Scope boundary**: does v1 need to teach joins (how a letter's shape and stroke path
   change when connected to its neighbors — Estrangela's 8 non-joining letters make this a
   real complication even in Lesson 0) or is letter-in-isolation formation enough for a
   first pass, with joined-word animation deferred like `SYRIAC-WEB-PLAN.md`'s own v1/v2
   split did for the drill engine?

## 5. What this is not

Not a decision about whether to build this — Wilson has already green-lit scoping it, not
shipping it. Not an evaluation of specific stroke-order data sources for Syriac
specifically (that's the scoping session's first real research task, likely needing
`WebSearch`/`WebFetch` against calligraphy manuals or academic sources on Estrangela
paleography — Wilson's own `scripts/syriac-serto.md` primer may be a starting point since
it already treats letterform history, though it currently documents shape, not stroke
order). Not a build — no code, no data format, no repo layout chosen here.
