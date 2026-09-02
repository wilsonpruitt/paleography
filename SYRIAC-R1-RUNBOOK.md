# R1 runbook — lesson-driven paradigm extraction

*Written 2026-09-02 (Sonnet), the session after G2 passed on `LESSON-0.md`/`LESSON-1.md` (the
"First Light" drill prototype). This is the execution score for the next session's R1 pull.
Governing rule: `SYRIAC-LANGUAGE-PILOT.md` §7a — R1 runs last, after R3, and extracts only the
cells a chosen lesson actually exercises, not the whole 40–70-record body blind. The choosing
is done: `SYRIAC-LESSON-PLAN.md` scores Lessons 1–10 against real destination passages and
names every new form cell each one needs. This runbook turns that list into an extraction
target. ⛔ Read `SYRIAC-LANGUAGE-PILOT.md` §§4–5, 7a and `SYRIAC-LESSON-PLAN.md` first; this
does not repeat their rationale.*

## What's already banked (don't re-pull)

Six R1 records exist, all flagged calibration-only / unadjudicated (Syriacist seat still
empty, no blind control run — `SYRIAC-PHASE1-RUNBOOK.md` Step 3 has not happened for R1):

| record | covers | still needed for |
|---|---|---|
| `r1/p004-1.toml` | alphabet table (Lesson 0's whole source) | nothing more — done |
| `r1/p023-1.toml` | personal pronoun, independent (§63) | L3 object pronoun ܐܶܢܘܢ, L10 copula-use ܐܢܬܘܢ ܐܢܘܢ — **already covered, pending adjudication** |
| `r1/p023-2.toml` | personal pronoun, enclitic after participle (§64) | L9 present-tense ܝܕܥ ܐܢܐ — **already covered, pending adjudication** |
| `r1/p044-1.toml` | Peal perfect **with object suffixes** (§§184–185, 188) | adjacent to but NOT the same table as the bare Peal perfect or the noun+suffix set below |
| `r1/p132-1.toml`, `p132-2.toml` | calendar lexical tables | no lesson needs these; ⚠ still carries Wilson's open ruling (R1 vs a new lexical-list type) — unrelated to this runbook, don't resolve it here |

So two of the ten lessons' pronoun needs are **already done, only awaiting adjudication** —
run those two through Step 3's blind control before or alongside the new pull below, cheaply,
since the plates are already read.

## The deduplicated target list

Compiled by walking every "New form cells" line in `SYRIAC-LESSON-PLAN.md` §2 (Lessons 1–10)
and merging repeats. Location column is Nestle's own ToC (`MAP.md` "Contents of the extraction
zones"): pronoun §23–24 (pp.23–24), noun §§19–33 (pp.24–38, numerals §33 pp.36–38), verb
§§34–48 (pp.39–63, strong-verb paradigm plates pp.44–45), particles §49 (pp.63–64), syntax
§§50–56 (pp.65–69). Priority is which lessons stall without it, not table order in the book.

| target paradigm | lessons that need it | likely location | priority |
|---|---|---|---|
| **Noun + possessive-suffix set** (1cp, 3ms, 2ms, 1cp-on-plural, 3mp, 2mp, 1cs) | L4, L5, L6, L9, L10 — five of ten | noun section §19–33, near the verb+suffix plate's counterpart | **highest** — widest reuse, nothing pulled yet |
| **Peal imperfect**, person set (3ms, 1cp, 3mp, 3fs, 2mp) | L1(named), L2, L4, L6, L7, L8, L10 — seven of ten | verb §§34–48 | **highest** |
| **Peal perfect, bare** (no object suffix), person set (3ms, 3fs, 2ms, 1cp) | L1, L6, L7, L9 | verb §§34–48, likely the same plate as p044 minus its suffix columns — check before assuming a separate table | high |
| **Peal imperative** (ms + mp) | L4, L6 | verb §§34–48 | medium |
| **Peal infinitive** ܠܡܶ־ | L3 | verb §§34–48, probably folded into the main paradigm table already targeted above | low marginal cost |
| **Peal participle**, active + passive | L9, L10 | verb §§34–48 | medium |
| **Noun plural emphatic + seyame rule** | L3 | noun §§19–33 | medium |
| **Adjective agreement pattern** | L3 | noun §§19–33 | low |
| **Construct state** (plural construct, ܕ-chain) | L4, L8, L9, L10 | noun §§19–33, noun-states table | medium |
| **Numerals: cardinals + ordinals** | L2, L5 | numerals §33, pp.36–38 | low |
| **Preposition + pronominal suffix table** (ܡܶܢ, ܠ, etc. + suffix) | L7 | particles §49, likely a plate parallel to `p023`'s pronoun table | medium |

Nine paradigm targets, not forty. That is the point of running R3 first — most of the book's
40–70-record estimate is coverage this pilot's ten lessons never touch.

## Recognition-only forms — do NOT pull full paradigms for these

Several lessons explicitly gloss a derived-stem form without drilling it as a cell (their own
language: "recognition only," "glossed not drilled"): Ethpeel (L5 ܐܬܬܢܝܚ, L8 ܢܬܩܪܘܢ), Ethpaal
(L2 first mention, L6 ܢܶܬܩܰܕܰܫ, L8 ܢܬܒܝܐܘܢ), Aphel (L3 ܡܰܢܗܪܺܝܢ, L6 ܥܠܠ). Pulling the full Ethpeel/
Ethpaal/Aphel paradigm tables for these would repeat the exact mistake §7a warned against —
capturing paradigm detail no lesson ends up needing. **Recommendation: don't extract these as
R1 records at all yet.** Gloss the specific attested form directly in the R3 `word_notes` entry
or the R4 lemma's `stems` field (both already in schema) where it occurs. Promote a stem to a
full R1 paradigm only if a later lesson (11+, out of pilot scope) actually drills it.

## An open scoping question — flagging, not deciding

Several "new form cells" are syntax rules or orthographic marks, not paradigm tables: relative
ܕ (L2), definite-object ܠ־ (L4), prohibition ܠܳܐ + imperfect (L7), linea occultans (L7), adverb
־ܐܝܬ (L7), anticipatory suffix + ܕ (L10), purpose clause ܕ + imperfect (L10). Nestle's own §§50–56
("Notes on the Syntax," pp.65–69) covers exactly this ground, but R1's schema (`SYRIAC-LANGUAGE-
PILOT.md` §4) is built for `lexeme` + `cells` — a syntax rule has no lexeme and no inflectional
cell. Two ways to handle it, both schema-legal already:
1. **As `word_notes`** on whichever R3/R2 record first exhibits it — same field that already
   carries Nestle's own philological footnotes, same shape as the R5-doesn't-exist ruling.
2. **As a light R1 record** with `kind = "syntax-note"` (parallel to p132's `kind =
   "lexical-table"` precedent), `cells` empty or a single illustrative example.
Route (1) needs no schema change and matches how Lesson 1–10 already footnote grammar inline;
route (2) keeps every grammar fact inside R1's record type for uniform querying later. Not
resolved here — flag it to Wilson before Step 2 below runs, the same way p132's R1-vs-new-type
question was left open rather than guessed at.

## Steps

### Step 1 — locate on the plates (cheap, ~6–10 leaf fetches)
For each of the nine targets above, find its actual leaf/page inside §§19–49 (pp.23–64) and
note whether Nestle prints it as one table or several (the strong-verb paradigm plates pp.44–45
already proved to be landscape, multi-column — expect the noun+suffix table to be the same
shape). Confirms or corrects the "likely location" column above before any transcription work
starts. Output: a short addendum to `MAP.md` naming each target's leaf.

### Step 2 — extract, after Wilson's go
Same house rules as `SYRIAC-PHASE1-RUNBOOK.md` Step 2: split on category not typography (a
footnoted weak-verb variant is its own table); fetch full-res; never read diacritic codepoints
by eye; vocalisation outranks the sense; declare the layer per record even when it matches the
section default. Model: **Opus**, same rationale as Phase 1 (every page touches Syriac). Land
files as `r1/p0NN-N.toml` in `quarry/nestle-1889-en/r1/`, same naming convention as the six
existing records.
⛔ **Hard stop before dispatch, per the house rule on big token burns**: after Step 1 pins the
actual leaf count, estimate tokens from `SYRIAC-PHASE1-RUNBOOK.md` Step 1's own measured
per-page rate (quote that number, don't re-guess a fresh one — [[feedback_quote-the-recalibrated-rate]]),
put the total to Wilson in one line, and wait for "which model, and go?" before extracting.

### Step 3 — adjudicate the pronoun pair + QA everything new
Run `p023-1.toml` and `p023-2.toml` through the blind control they're still owed (cheap — the
plates are already read), alongside a blind-control sample of whatever Step 2 produces, per
[[reference_arabic-control-rule]]. Report counts against this runbook's nine-target estimate.
Fold any schema surprise back into `SYRIAC-LANGUAGE-PILOT.md` §4 before touching a second
primer — same G1 gate Phase 1 already established.

## Out of scope here

The Syriacist seat (still empty, still not chased per standing instruction) · resolving
p132's R1-vs-lexical-type question · the syntax-note routing question above · any lesson 2–10
document-writing (separate from extraction — ⚠ NOT a Fable/Sonnet pass, corrected 2026-09-02:
Fable already wrote the template in Lesson 0/1, which Wilson G2-passed, so writing 2–10 is
Opus executing an established plan, per `NEXT-SESSION.md`) · the SRS/Tabella-adjacent vocab
engine idea (`paleography.md`, noted 2026-09-02, not started).
