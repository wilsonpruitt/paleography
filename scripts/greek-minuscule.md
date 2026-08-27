# Greek minuscule — a reader's primer

*Track 2 of the MVP. For someone who reads Greek and has never read a manuscript.
Grounded in 3,374 lines of ground truth from Heidelberg, Codex Palatinus graecus 23
(the Palatine Anthology), s. X — see `corpus/sources.yml`.*

---

## 1. The one historical fact that organises everything

Until about **AD 800, Greek books were written in majuscule** — capitals only, no word
division, no accents: *biblical uncial*, the hand of Sinaiticus and Vaticanus. Then,
within a couple of generations, Byzantine scribes adopted **minuscule**, a small
connected book hand derived from cursive documentary writing.

The change was radical and it is the reason this track is tractable: minuscule brought
**word division, accents and breathings written as a matter of course, and punctuation**.
A 10th-century Greek page is far closer to a printed page than a 5th-century one.

⚠ So "Greek paleography" is really two disciplines. This track is **minuscule
bookhand, s. X–XII** — the hand in which nearly all of classical and patristic Greek
actually reaches us, because it is what the Byzantine scriptoria copied. Majuscule and
papyri are different problems, deferred (papyri to Phase 3 by Wilson's ruling).

## 2. Why minuscule is harder than Caroline despite being more legible

Caroline separates letters; **minuscule connects them.** The difficulty is not the
individual letter but the **ligature** — two or three letters fused into a single
compound shape that must be learned as its own sign. A scribe writing quickly runs
`ει`, `ου`, `σθ`, `ταν` together into forms that share little with their components.

Second difficulty: **the same letter has several forms in one hand**, chosen by
position and by what precedes. Beta, kappa, and above all **tau** vary a lot.

Third: **abbreviation by suspension at line-end**, plus a set of conventional
tachygraphic (shorthand) signs for the commonest words and endings.

## 3. What our witness looks like

Real lines from Pal. gr. 23 (s. X), an anthology of epigrams:

```
    εἵλετο δὲ στεφάνουσ· καὶ πηκτίδα· καὶ μετὰ κώμων·
    ⁛ ὦξυρὸν οὐράνιον· ξυρὸν ὄλβιον· ὧι πλοκαμῖδασ
    ἐξ ἁλόσ· ὧι δὲ νέμοισ· ἠέροσ ὠφελίην: ⋇ ⋇
```

⚠⚠ **Read `στεφάνουσ` and `ἁλόσ` again.** Those are not typos and not my errors.

## 4. Three conventions of this transcription you must know before you type anything

These are decisions the editors made, verified in the data. **Get them wrong and every
exercise marks you wrong for being right.**

### (a) Final sigma does not exist

**`ς` occurs 0 times in 3,374 lines. `σ` occurs 6,036 times, and 3,203 words end in
it.** The editors state why: *"Sigma is always transcribed σ and never ς. This decision
reflects the scribe's practice of using exclusively σ."*

⚑ So `κάλλοσ`, `χρόνοσ`, `πολιῆσ`. **The scribe did not distinguish final sigma, so the
transcription does not either.** The medial/final distinction is a printing convention
of the Renaissance, not a fact about this manuscript.

⚑ For the app this is load-bearing: the diff engine must normalise `ς`→`σ` for this
witness, or every learner is penalised for correct modern Greek habits.

### (b) All punctuation is one sign

**0 commas, 0 full stops, 0 semicolons; 3,437 interpuncts (`·`).** Every punctuation
mark in the manuscript has been collapsed to a single raised dot. You cannot learn
Byzantine punctuation from this witness — it has been normalised away.

### (c) Abbreviations are already expanded

⛔ **This is the most important fact about this dataset, and the HTR-United catalogue
gets it wrong.** The catalogue says abbreviations are *not* resolved. The dataset's own
README says *"All abbreviations have been transcribed in expanded form"* — e.g. `ϗ` is
written out as `καί`, `ȣ` as `ου`.

Verified in the data: **`ϗ` occurs 0 times. `ȣ` occurs 0 times.**

⚑ **Consequence: Pal. gr. 23 cannot teach Level 2 (abbreviation) at all.** It is an
excellent Level-1 and Level-3 witness (letterforms, line reading) and useless for
learning what the abbreviation signs look like, because they are not in it.

⚑ **Therefore the Greek track needs a second, diplomatic witness before Level 2 can be
built.** This is the single biggest gap Phase 1 found, and it is a genuine
Phase-1b task, not a nicety. The Stavronikita manuscripts in the queue resolve
abbreviations too — so they do not fix it either. **Finding a diplomatic Greek witness
is an open problem.**

## 5. What the marks in the margins mean

Pal. gr. 23 uses a small set of structural signs, all documented by its editors:

| sign | Unicode | count | meaning |
|---|---|---|---|
| `⁛` | U+205B | 379 | beginning of an epigram |
| `⋇` | U+22C7 | 407 | end of an epigram |
| `∻` | U+223B | 28 | a scholion begins, in the margin |
| `※` | U+203B | 61 | a scholion begins, in the main text |

The page is not a block of prose. **725 of 3,374 lines (21%) are `MarginTextZone`** —
scholia, variant readings, the epigram-ascriptions. Reading a Byzantine anthology page
means reading a main text *and* a commentary apparatus laid around it.

## 6. Accents, breathings, and what is actually there

Unlike the Latin corpus, the Greek GT uses **no private-use codepoints and no combining
marks at all** — everything is precomposed polytonic Unicode. Practically: `ἐπεὶ`,
`ὑμετέροιο`, `θῆκεν` arrive as single codepoints per letter.

⚑ Two consequences. Rendering needs no special font (unlike the Latin, which needs a
MUFI font). And a learner typing polytonic Greek needs a **polytonic input method** —
which is a real onboarding obstacle the Latin track does not have, and the app must
solve it (an on-screen accent palette; the editors themselves built an eScriptorium
virtual keyboard for exactly this reason).

## 7. Practice order for this track

1. **Script ID** — minuscule vs majuscule; s. X bookhand vs later cursive.
2. **Glyph cards** — the position-variant letters first: `τ`, `β`, `κ`, `θ`; then the
   letters that collide (`ν`/`υ`, `γ`/`τ` in ligature).
3. **Ligature cards** — `ει`, `ου`, `σθ`, `ταν`, `εν`. *This is the step Latin does not
   have, and it is the heart of the Greek track.*
4. **Line** — Pal. gr. 23 `MainZone`, with `ς`→`σ` normalisation in the diff.
5. **Level 2 (abbreviation) — BLOCKED.** Needs a diplomatic witness we do not yet have.

## 8. Wilson's queue starts here

Per PLAN.md ruling 3, Greek expert review is Wilson's. Because Greek GT is thin and
this witness is already expanded, **the Greek track needs his judgement earlier than
the Latin one** — specifically on:

- whether an expanded-only witness is acceptable for the MVP Greek track (my read: yes
  for Levels 1 and 3, and the track ships honestly saying Level 2 is not yet available);
- where to find a diplomatic Greek witness, which may mean transcribing one ourselves
  from a IIIF facsimile rather than finding a dataset.

## Sources

Ground truth CC-BY 4.0, Codex Palatinus graecus 23, ecrinum/anthologia (Huma-Num).
Manuscript digitised by Heidelberg: https://doi.org/10.11588/diglit.3449
Conventions quoted from the dataset's own README; all counts computed over
`corpus/normalized/cpgr23.jsonl`.
