# Next session — start here

*Rewritten 2026-09-02, at the close of the Syriac R3 shard + Phase 3 lesson design. Read this
before `PLAN.md` or `EXPANSION-PLAN.md`: those are the score, this is where the needle is.*

---

## ⭐ THE IMMEDIATE NEXT TASK — build a throwaway drill prototype, not R1

Wilson's own words, ending the session that produced Lesson 0/1: *"i like the structure of
lesson 0 and 1 but i will personally need the drills before i can test its effectiveness on
myself."* Static markdown with an answer key three lines below the question is not a real
test of recall — G2 ("Wilson runs lesson 1... if it is beyond him, revise the ramp") cannot
actually be checked without something that hides the answer and grades him.

**Build a small, disposable interactive drill — recommend a private Claude Artifact (HTML),
not a repo web build.** Scope, deliberately narrow:
- Lesson 0's letter-recognition drills (`LESSON-0.md` Parts 1 and 3) — show a letter or a
  short nonsense string, ask for the name/reading, reveal and grade.
- Lesson 1's stages 2–4 (`LESSON-1.md`) — one-word cloze in the text, finish-the-line,
  whole-line — real hide/reveal, not a document he self-grades by eye.

**What this is NOT:** not the generative multiple-choice drill *engine* described in
`SYRIAC-LANGUAGE-PILOT.md` §10 (that's a bigger, separate design decision — building it over
R1–R4 records at scale, for every future language). Not R1 grammar extraction either — that
runs AFTER this, once G2 actually passes, and only pulls the paradigm cells lessons 2–10
need (§7a's ruling), not the whole grammar blind. This prototype exists purely so Wilson can
tell us whether the RAMP works, cheaply, before more content or more engineering sits on top
of an unvalidated design. Throwing it away and rebuilding properly later is fine and expected.

**Source data it needs**, all already extracted and committed:
- `LESSON-0.md`, `LESSON-1.md` — the lesson text and drill specs as currently written.
- `quarry/nestle-1889-en/r1/p004-1.toml` — the 22-letter alphabet table (names, sounds,
  non-joining letters) behind Lesson 0.
- `quarry/nestle-1889-en/r3/c067-1.toml` (Genesis 1:1–5, Lesson 1's text) and the R4 glossary
  entries it cites, if the drill wants to pull glosses live rather than copy them from the doc.
- `SYRIAC-LESSON-PLAN.md` §0/§2 — the reasoning behind what each lesson drills, if the
  prototype needs to explain itself.

**After Wilson actually runs it:** either G2 passes (→ resume R1, steered by lessons 2–10)
or it surfaces a ramp defect (→ revise `SYRIAC-LESSON-PLAN.md`/the lesson docs, not the
learner, per §7).

---

## State, briefly — detail lives in the docs named, not repeated here

- **Phase 1 (R3, the chrestomathy) is done.** 65 pages + the Lord's Prayer. 22 pages
  (Genesis 1-4, Matthew 5, Lord's Prayer) are fully keyed and independently diffed against PD
  editions — lesson-ready. 44 pages (Vitae Prophetarum, Historia inventionis) are partially or
  wholly unkeyed — a different, open problem (needs a Syriacist seat or Serto HTR), not more
  of the same extraction. Full picture: `quarry/nestle-1889-en/MAP.md` "R3 — RUN COMPLETE".
- **Phase 3 (lesson design) drafted 2026-09-02.** Ten lessons scored in `SYRIAC-LESSON-PLAN.md`
  from the 20 solid R3(a) pages; `LESSON-0.md` (alphabet, added after Wilson's own G2 feedback)
  and `LESSON-1.md` (Gen 1:1-5) are fully worked. Lessons 2-10 are scored but not yet written
  out as documents — do that only after G2 passes on 0/1.
- **Two future-idea notes recorded, both explicitly deferred, neither started:**
  1. The eventual web build = a generated multiple-choice drill engine over R1-R4 records, not
     a static single page. `SYRIAC-LANGUAGE-PILOT.md` §10.
  2. A stroke-order/letter-formation GIF-generation engine, Syriac as proof of concept,
     meant to generalize to every future non-Roman script (and possibly the paleography
     hand-reading side too). Same §10, second half.
- **R1 (grammar paradigms) is mostly unstarted** — 5 calibration records plus the new alphabet
  table (`r1/p004-1.toml`). Per §7a's ruling, extract only what lessons 2-10 actually need,
  once they're written, not the whole 40-70 record body blind.
- **Fixed this session, worth knowing about if anything references the old name:** the Lord's
  Prayer record was clobbered by a page-70 filename collision (Nestle has two printed page
  70s in two pagination sequences) and is now `r3/c070g-1.toml`, restored in full.

## Owed by Wilson, unrelated to the above, still open

1. **The licence question, touching a live track.** Both HTR Winter School Vienna
   repositories — Cod. 940 (Latin I, live) and Cod. Syr. 1 (Syriac) — ship a CC BY-SA 4.0
   `LICENSE.md` beside an `htr-united.yml` declaring CC BY 4.0. The site/README now state
   BY-SA correctly, but the underlying conflict is still unresolved with the source. One
   email to the Winter School settles it. Detail: `corpus/sources.yml` →
   `onb-syr1.license_conflict`.
2. **A Syriacist.** `registry/languages/syriac.toml` has `expert = ""`; several glosses are
   `proposed`. Same two people cover both this and item 1: **Ephrem Aboud Ishac** and
   **Christine Roughan**, who ran the Winter School Syriac group. ⏸ UT Austin LRC's earlier
   (2026-08-28) outreach is unanswered and cannot serve Syriac anyway (EIEOL is Indo-European).
3. **The word-division gloss fires on Greek** — `SPACING`'s note is Latin end to end but has
   appeared under Greek lines since that track shipped, kept only to stay byte-identical.
   Drop it there, or write a Greek one?
4. Smaller, long-standing: an Old French expert seat; the latin-caroline
   `count_marks_as_letters` ruling; 5 Greek glosses at `proposed`.

## Environment gotchas worth not re-discovering

- **Git LFS is DISABLED on the Syriac hand-trainer repo** (Cod. Syr. 1's 140 JPEGs) — clone
  with LFS filters off (`tools/fetch-seeds.sh` does), take plates from ÖNB over IIIF instead.
- **The GT repo's date for Cod. 940 is wrong** (says 1545; ÖNB says 1554 — the Vorlage for the
  first book printed in Syriac, 1555). Read the library's record, not the dataset's README.
- **Google Fonts families that don't exist fail silently** (200 + an HTML error page, then a
  fallback with no glyphs). Verified present: Noto Sans Syriac (Western/plain/Eastern).
  Verified absent: Noto Serif Syriac, Noto Sans Syriac Estrangela.
- **Canvas IIIF offset calibration: always check on ALL pages, not a plausible-looking one** —
  Cod. 940's correct offset (−1) gives scale exactly 0.500 on 140/140 pages; a wrong offset
  gives a plausible ≈0.5 that's wrong on 19-20 of them.
