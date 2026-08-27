# Paleography — handoff for the Greek review

*Written 2026-08-27, for a friend (the Greek expert) to hand to his own ChatGPT session
for context. This is a summary of a larger project; the canonical docs are `PLAN.md`
and `scripts/greek-minuscule.md` in this repo if he wants the full detail.*

## What this project is

We're building a tool that teaches people who already read Greek (or Latin) how to
read the actual **manuscripts** — not the language, the handwriting. Someone fluent
in Koine or classical Greek can still be lost looking at a 10th-century minuscule
page: unfamiliar letterforms, ligatures where two or three letters fuse into one
shape, abbreviation marks, no obvious word breaks in places. The app drills exactly
that visual-recognition skill, the way flashcards drill vocabulary.

The long-term angle (not being built yet, just planned for) is that the same
image-crop + correct-transcription pairs this produces are also exactly the training
data an HTR (handwritten text recognition) model needs. So the learner exercises and
a future OCR-for-old-manuscripts model are built on one shared corpus, not two
separate efforts. That's background — what matters for the Greek review is the
learner side.

## What exists right now

1. **A corpus of real manuscript ground truth**, ingested from an open dataset:
   **Codex Palatinus graecus 23** (Heidelberg), the *Palatine Anthology*, 10th
   century — 3,374 lines, CC-BY 4.0, sourced from the ecrinum/anthologia project
   (Huma-Num). This is currently the *only* Greek witness in the corpus.
2. **A working static prototype** (`build/scriptorium.html`) — a self-contained page
   that drills reading through five graded stages (see it whole → read along →
   supply one word → finish the line → transcribe the whole line cold), with a
   Levenshtein-aligned diff showing exactly which letters were missed.
3. **A written primer** (`scripts/greek-minuscule.md`) explaining minuscule to a
   Greek reader who's never seen a manuscript — the historical shift from majuscule
   to minuscule around 800, why ligatures are the real difficulty (not individual
   letters), and the specific quirks of this transcription.

## What we need from him — three concrete questions

These are the open items in the plan that specifically need a Greek paleographer's
judgment, not more engineering:

### 1. Is an "expanded-only" witness acceptable for launch, or a real gap?

The Pal. gr. 23 transcription has **all abbreviations silently resolved** — the
dataset's own documentation says so, and we verified it: the tachygraphic signs
`ϗ` (for καί) and `ȣ` (for ου) occur **zero times** in 3,374 lines, which they
couldn't if the scribe's actual abbreviations were preserved. So this witness is
good for teaching letterforms and line-reading, but it **cannot teach a learner what
abbreviation marks actually look like on the page** — that lesson has nothing to
train on.

Question for him: is it honest/acceptable to ship the Greek track saying "abbreviation
recognition isn't available yet" while everything else works? Or does he think that's
too big a gap to launch without?

### 2. Where do we find (or make) a *diplomatic* Greek witness?

A "diplomatic" transcription preserves the manuscript's actual marks — abbreviation
signs as signs, not resolved. We need one to build the abbreviation-recognition
exercises. Options we haven't ruled on:
- Does he know of an existing openly-licensed dataset of diplomatically-transcribed
  Greek minuscule (any date range, s. IX–XIII bookhand)?
- If nothing suitable exists, would he be willing to transcribe a small witness
  himself from a IIIF-available manuscript image (we'd pick one with clear open
  rights, e.g. an e-codices or Walters manuscript)? Even a few hundred lines would
  unblock the exercise type.

### 3. Sanity-check our transcription conventions and script-track scope

A few things baked into the primer/prototype that a specialist should either bless
or correct:
- We normalize final sigma: this dataset transcribes **only `σ`, never `ς`** (the
  editors say the scribe didn't distinguish it), so the diff engine treats `σ`/`ς`
  as equivalent rather than penalizing modern-Greek habits. Does that hold up, or
  is there a subtlety we're missing?
- MVP scope is **Byzantine minuscule bookhand, roughly 10th–12th century** —
  deliberately excluding majuscule/uncial and papyri as a different, later problem.
  Does that periodization/scope match how he'd teach this, or would he draw the
  line differently?
- The primer identifies ligatures (`ει`, `ου`, `σθ`, `ταν`, `εν`...) and
  position-variant letters (`τ`, `β`, `κ`, `θ`) as the hardest things to drill, ahead
  of individual letter shapes. Does that match his experience of what actually
  trips people up?

## Where to look if he wants more

- `scripts/greek-minuscule.md` — the full primer, written for a Greek reader,
  includes real transcribed lines from the manuscript and the reasoning above in
  more depth.
- `build/scriptorium.html` — open it in a browser to actually try the exercises.
- `PLAN.md` — the whole project's first-principles plan, including the Latin track,
  the data model, and the model-training rationale (§1–§4 especially).
