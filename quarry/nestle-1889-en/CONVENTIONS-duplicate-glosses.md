# Duplicate glosses — the ruling

*Wilson, 2026-09-01. Settled after the R4 shard finished (874 records, 1,608 lemmas).*
*This file is the score. Applying it is mechanical; deciding it was not.*

---

## The question

Across the glossary, the same German or English word glosses two unrelated Syriac head-words with
no pointer between them. Does the finished glossary link them?

## The test, and it is mechanical

**A duplicate is real only when BOTH gloss columns agree.**

That single rule does the work. **48 record-pairs share a gloss word; 12 survive the test; 36 are
rejected** — and everything it removes deserves removing:

| | |
|---|---|
| `temple` | ܗܰܝܟܠܳܐ **Tempel** (the building) vs ܨܶܕܥܳܐ **Schläfe** (the side of the head) |

That is an **English homonym collision**, not a Syriac duplicate. Linking it would assert a
relation that does not exist. Thirty-six of the forty-eight are of this kind.

⚑ Nestle's German is the control on his English and vice versa. Neither column alone is evidence.

## The tiers

**Tier 1 — the two entries are ONE WORD. Link; it is grammar, not editorial taste.**

| pair | why |
|---|---|
| ܝܰܗܒ (p. 158) ↔ ܢܬܰܠ (p. 171) | suppletive: ܝܗܒ supplies the perfect, ܢܬܠ the imperfect. A learner cannot conjugate the commonest verb in the language without both. |
| ܝܫܢ (p. 160) ↔ ܫܶܢܬܳܐ (p. 192) | one root — p. 192 prints the radical sign `(√ ܝܫܢ.)`, the only one in the book. |

**Tier 2 — true synonyms, both columns agreeing. Link as "see also".**

ܐܰܝܢܳܐ/ܡܰܢ `who?` · ܐܶܪܰܥ/ܦܓܰܥ `meet` · ܓܰܐܝܳܐ/ܗܕܺܝܪ `splendid` · ܗܰܠܶܠ/ܫܰܒܰܚ `praise` ·
ܟܺܐܦܳܐ/ܫܽܘܥܳܐ `rock` · ܣܒܰܠ/ܫܩܰܠ `bear` · ܥܽܘܡܩܳܐ/ܬܗܽܘܡܳܐ `depth` · ܪܡܳܐ/ܫܕܳܐ `throw`

⚑ **One named exception, so that it is not an unstated one.** ܕܡܶܟ (p. 147) ↔ ܝܫܢ (p. 160) is also
linked, and it does NOT pass the both-columns test: `schlafen | to sleep` against `Schlaf | sleep`,
a verb and a noun. It is linked because the two are unrelated roots for one concept, which is what
Tier 2 exists for, and the columns disagree only in part of speech. It is the only such exception,
and `quarry_dupes.py` will therefore not list it among the 12 — if a later pass finds a link the
tool cannot account for, it is either this one or a mistake.

**Tier 3 — single-column match only. DO NOT LINK.** (36 record-pairs.) Homonyms in the gloss
language, not duplicates in Syriac.

**Tier 3b — the duplicate is the SOURCE's own defect. Do not link; annotate.** Two so far, both
found by this test and by nothing else:

- **ܚܰܨܳܐ (p. 155) `Brust | breast`.** Nestle's own Hebrew cognate, read at 3× as **חרץ**
  (ח, then ר with no ascender), is Aramaic חַרְצָא **'loins'** (Dan. 5:6). ܚܰܨܳܐ is 'back, loins'
  in the lexica. His cognate contradicts his gloss. The duplicate with ܚܰܕܝܳܐ 'breast' (p. 152)
  is an artefact of that.
- **ܙܶܪܬܳܐ (p. 151) `Faust | fist`.** ܙܶܪܬܳܐ is *a span* (thumb to little finger; Hebrew זֶרֶת).
  Nestle glosses it 'fist' **and links it to ܙܘܪܐ himself** — so the pair is his, and so is the
  error.

⭐ **Neither was an extraction error.** Both records reproduce the plate exactly. That is the point:
the both-columns test is the only gate in the pipeline that caught them — the uncertainty flag,
the root ordering and the blind-control shortlist would each have passed them.

## Where a link lives

`see_also`, a **root-level** field on the record. Never inside `[[sub_lemmas]]` — a bare key written
after a sub-table silently joins that table and still parses (see `GLOSSARY-SHARD.md`, convention 9).

⛔ **`see_also` is ours. `see` is Nestle's.** That distinction is load-bearing and must never blur:
`see` holds only pointers he printed. Anything we infer goes in `see_also`, tagged with its tier.

## What Nestle himself does — and where this ruling departs from him

I said in session that he links a duplicate "once in forty-two chances." **That was wrong.** He
does it **four times**, in four different formulas, and every one is a Tier 1 case:

| | | |
|---|---|---|
| `Cf.` | ܩܥܳܐ (p. 185) → the ܨܘܬ entry | identical glosses |
| `vid.` | ܗܘܦܘܡܢܡܛܐ (p. 149) → ܐܽܘܦ— | ὑπομνήματα, two spellings |
| `cf.` | ܙܶܪܬܳܐ (p. 151) → ܙܘܪܐ | one word, two forms |
| `v.` | ܝܺܠܶܦ (p. 159) → ܐܠܦ | ܐ/ܝ root alternation |

**So the ruling is derived from his practice, not imposed on it.** He links when two entries are
the same word and never when they are merely synonyms. **Tier 1 is Nestle's own rule.** Tier 2 is
the deliberate extension, and it is where a reader is being given something the 1889 book withheld.
If that extension is ever revisited, Tier 1 stands regardless.

## Out of scope, and deliberately so

The **two-words-one-thing** pairs — the Passover (ܦܶܣܚܳܐ τὸ πάσχα / ܦܶܨܚܳܐ under ܦܨܚ), the
**crocodile three times** (pp. 168, 184, 188), the lyre (ܟܶܢܳܪܳܐ / ܩܺܝܬܳܪܳܐ), the two words for the
Resurrection (ܣܽܘܠܳܩܳܐ / ܩܝܳܡܬܳܐ). The gloss test cannot find these, and identifying them is a
**scholarly claim, not a reading** — they are the extractor's, not Nestle's and not the Syriacist's.
⬜ They wait for the Syriacist. They are listed in `GLOSSARY-SHARD.md`.

## Reproducing the analysis

```sh
python3 tools/quarry_dupes.py             # the 12 both-column pairs; counts reconcile 48 = 12 + 36
python3 tools/quarry_dupes.py --rejected  # the 36 rejected, i.e. the control group
```
