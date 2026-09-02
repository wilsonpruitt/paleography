# Syriac pilot — the ten lessons (Phase 3 score)

*Wroot Labs · Fable sequencing session 2026-09-02 · status: DRAFT toward G2.*
*Method: `SYRIAC-LANGUAGE-PILOT.md` §6 — every lesson built BACKWARD from a destination
passage; destination chosen by scored coverage, not eyeball; forms enter as cells, never as
whole paradigms. Lesson 1 is fully worked in `learn/syriac/LESSON-1.md` — Wilson runs it; if it is beyond
him, that is a design defect report against THIS file, not against him (§7 G2).*

---

## 0. What this is built from — and two findings

**Source pool = the 20 independently-checked pages only** (MAP.md "R3 — RUN COMPLETE"):
the Lord's Prayer (Matt 6:9–13), Genesis 1–4 (Chrest. I), Matthew 5 (Chrest. II). Vitae
Prophetarum and Historia inventionis are excluded — partially/wholly unkeyed, a different
open problem. The pool is more than enough: ten lessons below use roughly half of it.

✅ **Finding 1 — the Lord's Prayer record had been CLOBBERED by a filename collision, FIXED
2026-09-02.** Nestle's volume has two page-70s: the grammar's (Reading Exercise, leaf n87) and
the chrestomathy's (Genesis, leaf n159). Both content-addressed to `r3/c070-1.toml`, and the
R3 shard's Genesis record silently overwrote the earlier Lord's Prayer record. **Restored as
`r3/c070g-1.toml`** ("g" = grammar pagination) — and recovered fuller than this Phase-3 session
first found it: the restoration used the full working-tree record (36 structured `word_notes`
+ the completed BFBS `[alignment]` diff), not the bare `git show 1dea774` calibration stub this
note originally cited, so nothing about the Lord's Prayer content or its word-by-word gloss
layer was actually lost. Lesson 6's gloss layer below can cite `word_notes` directly rather
than flagging a gap.

⭐ **Finding 2 — Nestle's alternating layers ARE the vocalization ramp.** Chrest. I alternates
vocalized Serto / unvocalized Estrangela by caput; Chrest. II is unvocalized throughout. So
the corpus itself supplies the ramp reading-first wants: start on pointed text (training
wheels), and take the wheels off mid-course on vocabulary the learner already owns —
Lesson 5 is deliberately the FIRST unvocalized destination and is ~74% known words.

**Script ramp — the Serto conflict, resolved openly, not silently.** Lessons 1–10 are
Estrangela-only per §6, but the lesson-1 winner (Gen 1:1–5) — and Gen 3 and the Lord's
Prayer — are *printed* in vocalized Serto in Nestle. This is not a rule breach, per the
pilot's own ⭐ ruling (§3): "the primer's printed script does not constrain the product's
script — we extract text and re-render it in Estrangela." The extracted text is plain Syriac
Unicode; Serto vs Estrangela is a FONT decision at render time. On paper (these two files)
that means: the learner-facing documents instruct installing a free Estrangela font (Meltho
"Estrangelo Edessa"; Noto Sans Syriac, whose letterforms follow Estrangela, is the fallback
most systems already have), the orientation stage teaches Estrangela letterforms only, and
no Serto letterform is ever named in lessons 1–10. The Western vowel-points are kept as
printed (they render fine on Estrangela base glyphs and are standard teaching practice).
Flagged here rather than decided quietly; if Wilson wants lesson 1 re-anchored on a natively
Estrangela passage instead, Gen 2:1–3 is the scored runner-up (see below) and the swap is
one session's work.

## 1. The scoring run (so the choice is auditable)

Candidates for lesson 1 were scored on the whole 20-page corpus: surface-form tokenization
(diacritics stripped — vocalized and unvocalized text must compare equal), guarding the
degenerate length-metric (§8) by normalizing per TYPE, not per token:

| candidate | tokens | types | repetition (tok/typ) | corpus unlocked per new word |
|---|---|---|---|---|
| **Gen 1:1–5** | 49 | 38 | 1.29 | **0.384 %** |
| Gen 2:1–3 | 32 | 23 | 1.39 | 0.367 % |
| Matt 5:13–16 | 62 | 56 | 1.11 | 0.212 % |
| Beatitudes 5:3–10 | 50 | 34 | **1.47** | 0.164 % |
| Lord's Prayer | 41 | 38 | 1.08 | 0.161 % |

**Gen 1:1–5 wins on both §6 axes.** Highest coverage leverage: each new word learned unlocks
2.4× as much of the rest of the corpus as the Lord's Prayer's words do (its vocabulary — God,
earth, heaven, was, said, saw, called, day, one — IS the corpus's high-frequency spine). And
the lowest new-FORM count anywhere in the pool: six different verbs but essentially **one
verb cell** (3ms perfect Peal, "he X-ed") repeated, plus one 3fs perfect and the fixed phrase
ܢܶܗܘܶܐ. The Beatitudes' beautiful surface repetition (best tok/typ ratio) hides the heaviest
form load in the pool — 3mp imperfects across three stems (Peal/Ethpeel/Ethpaal) plus mp
absolute participles — and its formula words barely recur outside itself. The Lord's Prayer
is short but form-DENSE (imperatives ± suffixes, impf 3fs, Ethpaal, perfect 1cp, and the
whole 2ms/1cp suffix set at once): a mid-course destination, not an opening one.

Per-lesson new-surface-form load for the chosen sequence (surface forms overstate lemma
novelty — a known lemma with a new suffix counts as "new" — so treat as an upper bound):

| lesson | destination | tokens | new surface forms | new % |
|---|---|---|---|---|
| 1 | Gen 1:1–5 | 49 | 38 | 100 % (floor) |
| 2 | Gen 1:6–13 | 103 | 35 | 66 % |
| 3 | Gen 1:14–19 | 62 | 29 | 64 % |
| 4 | Gen 1:26–28 | 52 | 29 | 81 % |
| 5 | Gen 2:1–3 | 32 | 17 | 74 % |
| 6 | Matt 6:9–13 (LP) | 41 | 35 | 92 % |
| 7 | Gen 3:1–6 | 87 | 54 | 83 % |
| 8 | Matt 5:3–10 | 50 | 27 | 79 % |
| 9 | Gen 4:8–12 | 63 | 42 | 84 % |
| 10 | Matt 5:13–16 | 56 | 39 | 76 % |

(L6's and L9's high percentages are suffix-inflation: mostly known lemmas wearing new
pronominal suffixes — which is exactly what those lessons teach. L7 is the genuinely
heaviest lesson and says so in its own header; its stages split into two sittings.)

## 2. Lesson 0, then the ten lessons

⭐ **Lesson 0 added 2026-09-02, on Wilson's own report after running Lesson 1** — the first
G2 feedback the pilot has actually received, and it's a real design defect against this
score, not against him: Lesson 1 asked him to decode AND read-for-meaning at once, with no
prior pass on the shapes themselves. §6's ramp already has a "stage 0 orientation" *inside*
each lesson, but nothing upstream of Lesson 1 taught the alphabet as pure shape-recognition.
**Lesson 0 — `learn/syriac/LESSON-0.md` — fixes this**: all 22 letters named and sounded (Nestle's own
table, p.4, newly extracted as `r1/p004-1.toml` — see §0a below), the eight non-joining
letters and the mid-word-gap trap, and decoding drills built from **invented, meaningless
letter-strings only** — no vocabulary, no grammar, nothing to guess from context, exactly
Wilson's own spec. It is deliberately NOT part of the scored ten: it teaches no lemma, no
form, no passage, so it sits outside §6's coverage/new-form scoring entirely and simply runs
first. Stage vocabulary below (for lessons 1–10) follows §6's ramp: **0** orientation ·
**1** read-along, full gloss · **2** one-word cloze IN the text · **3** finish-the-line ·
**4** whole line unaided (then the same line as ink on the `/syriac` hand track, when the
bank has a witness).

### 0a. Where Lesson 0's content came from

`r1/p004-1.toml`, extracted on demand from the plate (leaf n21, p.4 — Nestle's "2. ALPHABET"
table) rather than assembled from memory, per this project's own rule against guessing at
Syriac fact. Worth noting: the table's 8 non-joining letters (Ålaf, Dålath, He, Vav, Zain,
Såde, Rīsh, Tau) came out identical, independently, to the set already named in the
hand-trainer's `registry/languages/syriac.toml` orientation prose — two different sources,
same fact, no coordination between them. One thing in the plate is flagged `uncertain`: which
of the table's two printed forms-per-cell is Estrangelo vs. Serto (inferred from the ordering
of p.5's prose, not a caption on the table itself) — doesn't affect Lesson 0, which renders
letters via standard Unicode Estrangela shaping rather than Nestle's own 1889 glyphs.

---

### Lesson 1 — "One day." · Gen 1:1–5 (`peshitta:gen:1:1-5`, Nestle p. 67)
**Why first:** the scored winner (above). One verb cell carries the whole passage; the nouns
are the corpus's ten most frequent words; the content is known to the learner by heart in
English, so comprehension never blocks decoding — the scaffold-the-learner rule made flesh.
**New lemmas (16 content + 6 function):** ܐܠܗܐ God · ܒܪܐ create · ܪܝܫܝܬ beginning · ܫܡܝܐ
heaven · ܐܪܥܐ earth · ܗܘܐ be/become · ܚܫܘܟܐ darkness · ܐܦ̈ܝ face-of · ܬܗܘܡܐ deep · ܪܘܚܐ
spirit · ܪܚܦ hover (gloss-only) · ܡ̈ܝܐ waters · ܐܡܪ say · ܢܘܗܪܐ light · ܚܙܐ see · ܫܦܝܪ
beautiful · ܦܪܫ separate · ܩܪܐ call · ܐܝܡܡܐ daytime · ܠܠܝܐ night · ܪܡܫܐ evening · ܨܦܪܐ
morning · ܝܘܡܐ day · ܚܕ one; particles ܘ־, ܕ־, ܒ־, ܠ־, ܥܠ, ܒܝܬ, ܝܬ (flagged as an archaism).
**New form cells:** 3ms perfect Peal (ܒܪܳܐ ܗܘܳܐ ܚܙܳܐ ܦܪܰܫ ܩܪܳܐ, ܘܶܐܡܰܪ) · 3fs perfect (ܗܘܳܬ) ·
emphatic-state ־ܳܐ as the noun's default dress · proclitics ܘ/ܕ/ܒ/ܠ · seyame (named only) ·
ܢܶܗܘܶܐ as a fixed phrase ("let there be" — the imperfect cell is L2's job).
**Stages 2–4:** cloze the five recurring anchors (ܐܠܗܐ, ܢܘܗܪܐ, ܘܗܘܐ, ܐܪܥܐ, ܝܘܡܐ) one gap per
pass · finish "ܘܶܐܡܰܪ ܐܰܠܳܗܳܐ ܢܶܗܘܶܐ ܢܘܗܪܳܐ ⟨…⟩" and "ܘܰܗܘܳܐ ܪܰܡܫܳܐ ⟨…⟩" · whole line unaided =
v. 3 (fiat lux). Fully worked in `learn/syriac/LESSON-1.md`.

### Lesson 2 — Days two and three · Gen 1:6–13 (p. 67–68)
**Why next:** the longest destination in the course, tolerable only because ~⅔ of its surface
forms are already L1's — the day-frame (ܘܐܡܪ ܐܠܗܐ… ܘܗܘܐ ܗܟܢܐ… ܘܗܘܐ ܪܡܫܐ ܘܗܘܐ ܨܦܪܐ) now
recycles verbatim, which is what makes room for the one big new cell.
**New lemmas:** ܪܩܝܥܐ firmament · ܡܨܥܬܐ midst · ܟܢܫ gather · ܝܒܝܫܬܐ dry land · ܝܡ̈ܡܐ seas ·
ܥܣܒܐ herb · ܙܪܥܐ seed · ܐܝܠܢܐ tree · ܦܐܪ̈ܐ fruits · ܓܢܣܐ kind · ܬܚܬ below · ܠܥܠ above ·
ܗܟܢܐ thus · ܡܢ from · ordinals ܬܪܝܢ ܬܠܬܐ.
**New form cells:** imperfect 3ms ܢܶܗܘܶܐ (now named as a cell, not a phrase) and 3mp ܢܶܗܘܘܢ /
ܢܶܬܟܰܢܫܘܢ (incl. first Ethpaal, glossed not drilled) · 3fs perfect with object flavor ܐܰܦܩܰܬ ·
ܕ־ as relative ("which sows seed") · ܒܶܝܬ … ܠ between-X-and-Y (already seen, now drilled).
**Stages 2–4:** cloze the frame slots (which word of the recycled formula is missing?) ·
finish the day-3 refrain line · whole line = "ܘܰܩܪܳܐ ܐܰܠܳܗܳܐ ܠܝܰܒܺܝܫܬܳܐ ܐܰܪܥܳܐ".

### Lesson 3 — The two lights · Gen 1:14–19 (p. 68)
**Why next:** same frame again, and the passage is a natural seyame/plural drill — ܢܰܗܺܝܪ̈ܶܐ,
ܐܳܬܘ̈ܳܬܳܐ, ܙܰܒ̈ܢܶܐ, ܝܰܘ̈ܡܳܬܳܐ, ܫܰܢ̈ܰܝܳܐ, ܟܰܘܟ̈ܒܶܐ in six lines.
**New lemmas:** ܢܗܝܪܐ luminary · ܐܬܐ sign · ܙܒܢܐ time · ܫܢܬܐ year · ܟܘܟܒܐ star · ܪܒܐ great ·
ܙܥܘܪܐ small · ܫܘܠܛܢܐ dominion · ܣܡ place/set.
**New form cells:** masculine-plural emphatic ־̈ܶܐ and the seyame rule (dots go ON the word,
find them before reading) · ܠܡܶ־ infinitive (ܠܡܶܦܪܰܫ; Aphel ܠܡܰܢܗܳܪܘ glossed) · adjective
agreement (ܢܰܗܺܝܪܳܐ ܪܰܒܳܐ / ܙܥܘܪܳܐ) · Aphel participle mp ܡܰܢܗܪܺܝܢ (recognition only) · object
pronoun ܐܶܢܘܢ.
**Stages 2–4:** cloze the plural nouns (seyame is the give-away — teach them to USE it) ·
finish "ܢܰܗܺܝܪܳܐ ܪܰܒܳܐ ܠ⟨…⟩" · whole line = v. 16's great-and-small-lights line.

### Lesson 4 — In our image · Gen 1:26–28 (p. 69)
**Why next:** the frame retires; the person system enters. Possessive suffixes and the plural
imperative arrive on the most quotable lines of the chapter. (1:20–25's zoological lists are
deliberately skipped — low-leverage vocabulary; they remain bank material.)
**New lemmas:** ܥܒܕ make/do · ܐܢܫܐ man/humankind · ܨܠܡܐ image · ܕܡܘܬܐ likeness · ܫܠܛ rule ·
ܢܘܢ̈ܝ fish-of · ܝܡܐ sea · ܦܪܚܬܐ fowl · ܒܥܝܪܐ cattle · ܐܕܡ Adam · ܕܟܪ male · ܢܩܒܬܐ female ·
ܒܪܟ bless (Pael) · ܦܪܐ be fruitful · ܣܓܐ multiply · ܡܠܐ fill · ܟܒܫ subdue.
**New form cells:** possessive suffixes 1cp ܒܨܰܠܡܰܢ / 3ms ܒܨܰܠܡܶܗ (the suffix idea itself) ·
imperfect 1cp ܢܶܥܒܶܕ ("let us make") · mp imperative ܦܪܰܘ ܘܰܣܓܰܘ ܘܰܡܠܰܘ · ܠ־ marking a definite
object (ܠܳܐܕܳܡ) · construct plural ܒܢܘܢ̈ܰܝ ܝܰܡܳܐ (recognition only).
**Stages 2–4:** cloze the suffix-bearing words (which image? whose?) · finish the imperative
chain "ܦܪܰܘ ܘܰܣܓܰܘ ܘ⟨…⟩" · whole line = "ܘܰܒܪܳܐ ܐܰܠܳܗܳܐ ܠܳܐܕܳܡ ܒܨܰܠܡܶܗ".

### Lesson 5 — Sabbath, and the wheels come off · Gen 2:1–3 (p. 70) ⭐ first UNVOCALIZED text
**Why next:** the pivot lesson. Nestle prints Caput II unvocalized (Estrangela), and 2:1–3
scores second-best in the whole pool per-type (0.367 %) precisely because it is almost
entirely L1–L4 vocabulary (ܐܠܗܐ ܫܡܝܐ ܐܪܥܐ ܝܘܡܐ ܥܒܕ ܒܪܟ ܒܪܐ) in new dress: only 17 new surface
forms in 32 tokens, most of them known lemmas unpointed. The explicit skill taught: reading
without vowels, supplying what you already know — which is what real manuscripts will demand.
**New lemmas:** ܫܠܡ finish · ܢܘܚ rest (Ethpe. ܐܬܬܢܝܚ) · ܩܕܫ sanctify (Pael) · ordinals
ܫܬܝܬܝܐ sixth / ܫܒܝܥܝܐ seventh · ܟܠ all.
**New form cells:** unpointed word-images of known lemmas (the cell IS the skill) · suffix
3mp ܟܠܗܘܢ · ܥܒܕܘ̈ܗܝ his-works (3ms suffix on a plural, seyame as the only clue) · Ethpeel
perfect ܐܬܬܢܝܚ (recognition) · ordinal pattern ־ܝܐ.
**Stages 2–4:** cloze known words in unpointed dress (can you still recognize ܐܠܗܐ without
its vowels? yes — prove it) · finish "ܘܒܪܟ ܐܠܗܐ ܠܝܘܡܐ ⟨…⟩" · whole line = v. 3a, then the
same line pointed from memory of L1–L4 pronunciation habits (aloud only, not written).

### Lesson 6 — ܐܒܘܢ ܕܒܫܡܝܐ · the Lord's Prayer, Matt 6:9–13 (p. 70 of the GRAMMAR, leaf n87)
**Why next:** the suffix system, on the one Syriac text worth having by heart first. Every
2ms and 1cp suffix cell appears in a line the learner will recite for the rest of his life:
ܫܡܳܟ ܡܰܠܟܽܘܬܳܟ ܨܶܒܝܳܢܳܟ ܕܺܝܠܳܟ (your-) against ܐܰܒܽܘܢ ܠܰܢ ܚܰܘܒܰܝܢ ܚܰܝܳܒܰܝܢ (our-/us). Placed
here, not first: its 92 % new-surface load is suffix-inflation the learner can now parse,
and Nestle's own Greek-letter transliteration (extracted with the record) rides along free.
**New lemmas:** ܐܒܐ father · ܩܕܫ hallow (Ethpaal — L5 met the root) · ܐܬܐ come · ܡܠܟܘܬܐ
kingdom · ܨܒܝܢܐ will · ܐܝܟܢܐ as · ܐܦ also · ܝܗܒ give (imv. ܗܒ) · ܠܚܡܐ bread · ܣܘܢܩܢܐ need ·
ܝܘܡܢܐ today · ܫܒܩ forgive/leave · ܚܘܒܐ debt · ܚܝܒܐ debtor · ܥܠܠ bring-in (Aphel) · ܢܣܝܘܢܐ
temptation · ܦܨܐ deliver · ܒܝܫܐ evil · ܡܛܠ ܕ because · ܚܝܠܐ power · ܬܫܒܘܚܬܐ glory · ܥܠܡ age ·
ܐܡܝܢ amen.
**New form cells:** suffix 2ms ־ܳܟ across nouns · suffix 1cp ־ܰܢ / plural-noun 1cp ־ܰܝܢ · ms
imperative ܗܰܒ / ܫܒܽܘܩ · imperative+suffix ܦܰܨܳܢ · imperfect 3fs ܬܺܐܬܶܐ · Ethpaal imperfect
ܢܶܬܩܰܕܰܫ · perfect 1cp ܫܒܰܩܢ · ܕܺܝܠ־ possessive base.
**Stages 2–4:** cloze the suffixes themselves (ܢܶܗܘܶܐ ܨܶܒܝܳܢ⟨…⟩) · finish each petition from
its opening word · whole line = the whole prayer, recited then read, then v. 9 written.
⛔ **Ships only after the clobbered record is restored** (Finding 1). The text itself is
recovered and safe; the record-keeping is what's owed.

### Lesson 7 — The serpent's question · Gen 3:1–6 (pp. 73–74) — the heavy lesson, two sittings
**Why next:** first connected DIALOGUE — speech verbs with different subjects, feminine forms
throughout (the story runs on ܐܢܬܬܐ), and the reported-speech ܕ. Heaviest new-lemma load in
the course (says so up front; stages 0–2 are sitting one, 3–4 sitting two).
**New lemmas:** ܚܘܝܐ serpent · ܥܪܝܡ crafty · ܚܝܘܬܐ beast · ܕܒܪܐ field · ܐܢܬܬܐ woman · ܐܟܠ
eat · ܡܘܬ die · ܝܕܥ know · ܦܬܚ open (Ethpa.) · ܥܝܢ̈ܐ eyes · ܛܒܬܐ good · ܒܝܫܬܐ evil · ܪܓܬܐ
desire · ܢܣܒ take · ܒܥܠܐ husband · ܥܡ with · ܫܪܝܪܐܝܬ truly.
**New form cells:** perfect 3fs series ܐܶܡܪܰܬ ܚܙܳܬ ܢܶܣܒܰܬ ܐܶܟܠܰܬ ܝܶܗܒܰܬ (one cell, five verbs —
the L1 trick again, feminine) · imperfect 2mp ܬܶܐܟܠܘܢ · prohibition ܠܳܐ + imperfect ·
preposition+suffix ܡܶܢܶܗ ܠܶܗ · linea occultans in ܐܰܢ̱ܬܬܳܐ (the silent-letter mark, named) ·
adverb ־ܐܝܬ.
**Stages 2–4:** cloze the speech-verb slots (who says this line?) · finish the serpent's
"ܠܳܐ ܡܡܳܬ ⟨…⟩" · whole line = 3:6a (the woman saw that the tree was good).

### Lesson 8 — ܛܘܒܝܗܘܢ · the Beatitudes, Matt 5:3–10 (p. 79) — first unvocalized NT
**Why next:** now its form load is paid down: ܢ־…ܘܢ imperfects (L2), ־ܗܘܢ (L5), unpointed
reading (L5), ܡܛܠ (L5/L6). What remains genuinely new is the formula itself, and eight
near-identical lines make the passage a self-building cloze ladder. Recitable, like L6.
**New lemmas:** ܛܘܒܐ blessedness (ܛܘܒܝܗܘܢ blessed-are-they) · ܡܣܟܢܐ poor · ܐܒܝܠܐ mourner ·
ܒܝܐ comfort (Ethpa.) · ܡܟܝܟܐ meek · ܝܪܬ inherit · ܟܦܢ hunger · ܨܗܐ thirst · ܟܐܢܘܬܐ
righteousness · ܣܒܥ be filled · ܡܪܚܡܢܐ merciful · ܪ̈ܚܡܐ mercies · ܕܟܐ pure · ܠܒܐ heart ·
ܫܠܡܐ peace · ܪܕܦ persecute · ܐܝܠܝܢ ܕ those who · ܗܢܘܢ they.
**New form cells:** imperfect 3mp across stems — Peal ܢܐܪܬܘܢ ܢܚܙܘܢ, Ethpeel ܢܬܩܪܘܢ, Ethpaal
ܢܬܒܝܐܘܢ (recognize the ܢܬ־ shape, don't conjugate it) · mp absolute participles ܟܦܢܝܢ ܨܗܝܢ
ܕܟܝܢ (predicate use) · ܕܝܠܗܘܢ theirs · construct ܥܒܕ̈ܝ ܫܠܡܐ makers-of-peace.
**Stages 2–4:** cloze the second half of each beatitude (formula gives the frame, memory
gives the word) · finish alternate beatitudes from ܛܘܒܝܗܘܢ ܠ… · whole line = one whole
beatitude of the learner's choosing, unaided, plus v. 9 (the peacemakers) assigned.

### Lesson 9 — Where is Abel? · Gen 4:8–12 (pp. 76–77, cod. Ambrosianus)
**Why next:** unvocalized NARRATIVE with no formula scaffold at all — the training wheels and
the guard rails both gone, on the most famous dialogue in Genesis. Introduces the participle-
present, the single highest-value reading structure left in the pool.
**New lemmas:** ܩܐܝܢ Cain · ܗܒܝܠ Abel · ܐܚܐ brother · ܚܩܠܐ field · ܩܛܠ kill · ܩܠܐ voice ·
ܕܡܐ blood · ܓܥܐ cry · ܦܬܚ open · ܦܘܡܐ mouth · ܢܛܘܪܐ keeper · ܠܘܬ unto · ܡܟܝܠ henceforth ·
ܠܝܛ cursed.
**New form cells:** participle + enclitic pronoun = present tense: ܝܕܥ ܐܢܐ "I know", ܢܛܘܪܗ
ܐܢܐ ܕܐܚܝ "am I my brother's keeper?" · perfect 2ms ܥܒܕܬ ܦܬܚܬ ܩܒܠܬ · interrogatives ܐܝܟܘ ܡܢܐ ·
suffix 1cs ܐܚܝ · passive participle ܠܝܛ ܐܢܬ · the ܕ-chain ܩܠܐ ܕܕܡܗ ܕܐܚܘܟ (voice of-the-blood
of-your-brother).
**Stages 2–4:** cloze the dialogue turns (God's word or Cain's?) · finish "ܠܐ ܝܕܥ ܐܢܐ ⟨…⟩" ·
whole line = v. 9's question and answer, both.

### Lesson 10 — ܢܘܗܪܗ ܕܥܠܡܐ · Matt 5:13–16 (p. 80) — capstone
**Why last:** it closes every loop the course opened. ܐܢܬܘܢ ܐܢܘܢ ܡܠܚܗ ܕܐܪܥܐ / ܢܘܗܪܗ ܕܥܠܡܐ
is the signature Syriac possession idiom (his-salt of-the-earth) met glancingly in L1's ܪܘܚܶܗ
ܕܰܐܠܳܗܳܐ and now named and drilled; ܢܘܗܪܐ is L1's word; ܐܒܘܟܘܢ ܕܒܫܡܝܐ answers L6's ܐܒܘܢ
ܕܒܫܡܝܐ; and the destination — *you are the light of the world* — is a line worth arriving at.
**New lemmas:** ܡܠܚܐ salt (ܡܠܚ be-savored) · ܦܟܗ be-insipid · ܥܠܡܐ world · ܡܕܝܢܬܐ city ·
ܛܘܪܐ mountain · ܒܢܐ build · ܫܪܓܐ lamp · ܡܢܪܬܐ lampstand · ܣܐܬܐ bushel · ܬܚܝܬ under · ܒܝܬܐ
house · ܥܒܕ̈ܐ works · ܫܒܚ glorify (Pael) · ܐܓܪܐ reward.
**New form cells:** independent pronoun as copula ܐܢܬܘܢ ܐܢܘܢ "you ARE" · anticipatory suffix
+ ܕ (ܡܠܚܗ ܕܐܪܥܐ) — named, drilled, owned · suffix 2mp ־ܟܘܢ (ܢܘܗܪܟܘܢ ܥܒܕ̈ܝܟܘܢ ܐܒܘܟܘܢ) · mp
participles as present ܡܢܗܪܝܢ ܣܝܡܝܢ · imperfect-3mp purpose clause ܕܢܚܙܘܢ … ܘܢܫܒܚܘܢ.
**Stages 2–4:** cloze the two "you are X-of-the-Y" declarations · finish "ܗܟܢܐ ܢܢܗܪ ⟨…⟩" ·
whole line = v. 14a unaided — then, per §6 stage 4, the same line as ink on the `/syriac`
hand track becomes the pilot's twin-path handoff moment.

---

## 3. Left in the bank (lessons 11+, post-pilot)

Gen 1:20–25 (species lists) · Gen 2:4–25 (Eden planted; the naming; the rib) · Gen 3:7–24
(the curses — rich but form-heavy) · Gen 4:1–7, 13–26 (offerings; the Cain genealogy) ·
Matt 5:11–12, 17–48 (the antitheses — six parallel "you have heard… but I say" units, a
formula-ladder like the Beatitudes and the natural lessons 11–14). Nothing outside the 20
checked pages enters any lesson until its extraction problem is actually solved.

## 4. Composed drill sentences — a standing constraint

§6 asks each lesson for 3–6 composed drill sentences. Nestle supplies none (R2 = 0,
confirmed), and Robinson's R2 extraction hasn't run. Until it does, drills are composed
in-house under one safety rule: **every word-form in a composed drill must be attested
somewhere in the 20 checked pages** — recombination only, no invented morphology, and each
drill block is marked *ours, not the primer's* (the R2 `key` discipline applied to
pedagogy). `learn/syriac/LESSON-1.md` §Drills shows the pattern. When Robinson's exercises are extracted,
author-composed drills replace the in-house ones wherever they cover the same cells.
