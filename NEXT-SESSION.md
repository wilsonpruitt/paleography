# Next session — start here

*Rewritten 2026-09-02, at the close of G2 passing. Read this before `PLAN.md` or
`EXPANSION-PLAN.md`: those are the score, this is where the needle is.*

---

## ✅ DONE — R1 extraction, per `SYRIAC-R1-RUNBOOK.md` (history; the live task is further down)

✅ **G2 PASSED, 2026-09-02.** The throwaway drill prototype got built (private Claude Artifact
"First Light," iterated live with Wilson through several rounds — randomized order, a
sound-it-out phase ahead of every recognition step, a vowel-marks primer, a Half-a-Line stage
between vocabulary and full sentences, a letter-breakdown side panel at word level). Wilson ran
Lesson 0 and Lesson 1 through it end to end: *"loved it. we are on to something here.
structurally, i think we are solid... what we have here works for lesson one."* The ramp is
validated — do not re-litigate Lesson 0/1's design.

✅ **Step 1 (locate) run 2026-09-02, Opus, "go" given.** Addendum in `quarry/nestle-1889-en/MAP.md`
("R1 Step 1 — plate locations"). Nine targets collapse to 5–6 leaves (n48, n51, n53–54, n60,
n80–81); two of the runbook's "likely location" guesses corrected (both toward less work).
**⛔ Step 2 (extract) only partially attempted, and here's why it stopped:** on inspection, p.34
(leaf n51, the "Noun + possessive-suffix set" target — the runbook's HIGHEST priority) is **not
a printed table at all** — §31 is prose stating the rule (append the §23 suffix set to the
plural stem) plus a handful of scattered example words, not a systematic grid. And p.43
(leaf n60, §38 "Strong Verbs") — which bundles 5 of the 9 targets (bare Peal perfect, imperfect,
imperative, infinitive, participle act./pass.) — is real and exactly where predicted, but it's a
dense ~35-cell-for-Peal-alone grid (person × number × 3 stems, tiny diacritics) that I could not
read with confident per-glyph accuracy at vision resolution without risking baked-in wrong
vocalization — the project's own standing worry (`reference_paleography-gt-ingest.md`). I did
NOT commit a guessed transcription to `r1/*.toml`; nothing new is on disk from Step 2 yet.
**Two things for Wilson before this resumes:** (1) how should the p.34 rule+examples be
captured — `word_notes` on the §23 pronoun-suffix records, or a `kind = "rule"` R1 record
(third precedent after p132's `lexical-table`)? Same shape as the still-open syntax-note
question. (2) the p.43 grid is real transcription work, not a quick fetch like p023/p044 were —
worth deciding whether it waits for the Syriacist seat (still empty) rather than going in
uncontrolled the way the six existing calibration records did.

✅ **Both resolved by Wilson, 2026-09-02: defer the Syriacist seat, keep going uncontrolled now;
p.34 → `kind = "rule"`.** Four new R1 records landed this session, all calibration-only /
`proposed`, none blind-controlled:
- `r1/p034-1.toml` — the new `kind = "rule"` record for §31 (noun+suffix rule + worked
  examples). Cross-references `p023-1`/`p023-2`/`p031-1` as the base tables the rule composes,
  rather than synthesizing the full cross-product paradigm ourselves.
- `r1/p031-1.toml` — new `kind = "paradigm-survey"` (third `kind` value, alongside p132's
  `lexical-table`) for §29's 12-row noun-class table — covers BOTH the plural-emphatic/seyame
  and construct-state targets in one record, per Step 1's finding that they share a plate.
  Confidence is uneven by row — several rows flag `uncertain` where the plate shape didn't
  match a memorized "expected" paradigm and I recorded the shape rather than the expectation
  (Wilson's explicit steer).
- `r1/p043-1.toml` — bare Peal perfect (10 cells, sg+pl), same lexeme as `p044-1` (qṭal
  "kill"). **Only the Perfect row of p.43's grid** — Imperfect, Imperative, Infinitive, and
  Participle (active+passive) are confirmed on the SAME plate (§38) but NOT yet transcribed;
  land as `p043-2`/`-3`/`-4` in the next pass, don't fold in without their own source note.
- ⬜ **Not yet touched this session:** numerals (n53–54), preposition+suffix table (n80–81,
  still unconfirmed as a clean table vs. prose).
- **Third open `kind`-schema question, same shape as p132's:** R1 now has `lexeme+cells`
  (standard), `kind = "lexical-table"` (p132), `kind = "rule"` (p034), `kind =
  "paradigm-survey"` (p031). Worth a single ruling on all of these together before the schema
  grows a fourth ad hoc value, rather than one at a time.

✅ **Session continued, all nine original R1-runbook targets now landed (2026-09-02).** Final
tally, 8 new records, all TOML-valid (`python3 -c "import tomllib"` checked), all
calibration-only/`proposed`, none blind-controlled — no Syriacist seat, by Wilson's explicit
"defer the seat, keep going" ruling:
- `p034-1` — noun+suffix RULE (target 1)
- `p031-1` — plural-emphatic + construct-state, one plate (targets 7, 8)
- `p043-1`/`-2`/`-3`/`-4` — Peal perfect bare, imperfect, imperative, infinitive+participle,
  all off the SAME §38 grid (targets 2-6). `-4`'s participle cells are base singular forms
  only — the plate shows a second stacked sub-form per cell not broken out, flagged as a
  follow-up, not guessed.
- `p037-1` — numerals 1-19 + tens 20-90 (target 9). **Highest-confidence record of the
  session** — every cell carries a printed Arabic-numeral label, so lexeme identity was never
  in question the way it was for the verb/noun tables.
- `p063-1` — BONUS, not one of the nine: the preposition+suffix target (§49) turned out to be
  rule+examples like p034, not a table. Filed the same way; §49h's ~14-preposition list is
  individually English-glossed on the plate, so that part carries lexical-table-level
  confidence even inside a `kind = "rule"` record.
- ⭐ **Also logged this session, not extraction but a standing pedagogy ruling from Wilson:**
  `SYRIAC-LANGUAGE-PILOT.md` ruling 7 — numerals should be taught as a closed decoding system
  (alphabet-like), not vocabulary pairs, because a number has no visual referent to recall the
  way "dog" or "red" does. Bears on whichever lesson introduces numerals; doesn't change what
  `p037-1` captured.
✅ **All three open items ruled, 2026-09-02, same session:**
1. **Syriacist outreach (Ishac/Roughan): HELD**, not cancelled — see the "Owed by Wilson" item
   2 below for the exact reasoning and gate (needs a public, working artifact to point to
   first).
2. **`kind` field: formalized, four named shapes**, in `SYRIAC-LANGUAGE-PILOT.md` §4 —
   default (lexeme+cells), `lexical-table`, `rule`, `paradigm-survey`. All eight of this
   session's new records now cross-reference the formalized version instead of carrying an
   open question in their header comments.
3. **Blind control without a Syriacist: NOT a second fresh-session vision-read** (two reads of
   the same JPEG share failure modes — correlated error, not independent evidence, per
   `reference_arabic-control-rule`'s own logic). Real control = **Nöldeke's own PD grammar**,
   already the schema's shared coordinate system via `noldeke` tags — his printed forms for
   the same paradigm cell are a free, independent, zero-human-required check for standard
   paradigms. Two-tier protocol written up in `SYRIAC-LANGUAGE-PILOT.md` §5: tier 1 (Nöldeke
   also prints it) collates against him; tier 2 (primer-specific rule content, or any cell
   already flagged `uncertain` because it diverged from the expected paradigm) has no
   external "should be" and stays `proposed` regardless.

✅ **Tier-1 Nöldeke collation RUN, 2026-09-02, same session.** Found and calibrated a second
PD scan: `noldeke-compendious-syriac-grammar` on archive.org (same hOCR-pageindex tooling as
Nestle's; **leaf = printed page + 35**, verified on two plates). Collated:
- **`p043-1/-2/-3/-4`** (Peal perfect/imperfect/imperative/infinitive/participle) against
  Nöldeke's §168 "Regular Verb" table, p.109 (leaf n144) — **CONFIRMED across the board**,
  same paradigm verb (qṭal) independently chosen by both grammars. Bonus finds: (1) the 3fp
  perfect cell this session had flagged `uncertain` is exactly the one cell where Nöldeke's
  own plate ALSO prints two dialectal variants — the flag was right, not overcaution;
  (2) p043-4's coverage-gap note (an unexplained second stacked form per participle cell) is
  resolved — it's the feminine singular, confirmed against Nöldeke's plate, which prints both
  genders per cell where p.43's own plate only gave m.sg legibly.
- **`p037-1`** (numerals) against Nöldeke's §148, p.95 (leaf n130) — **CONFIRMED for 1-10**,
  including the harder call (6's alaph-prosthetic variant, 'eštā not štā). ⚠ **11-19 and
  20-90 NOT yet collated** — worth flagging that Nöldeke's own text on the same page warns the
  teens "fluctuate in their vocalisation... very doubtful or to be rejected altogether," so
  those cells may deserve MORE hedging than a clean match would imply, not less.
- **Not yet collated this session:** `p034-1`/`p063-1` (rule records — Nöldeke covers
  possessive-suffix attachment at §145 p.87/leaf122 and prepositions at §156-157
  p.101-103/leaf136+138, both located and ready for a follow-up pass), `p031-1` (noun-state
  survey — Nöldeke's simplest-forms paradigm is §70 p.48/leaf83, worth checking especially
  against the rows already flagged `uncertain`), `p023-1/-2` (pronouns — the two
  longest-owed records, Nöldeke's own pronoun section is §63-66 p.44-46/leaf79-81).

✅ **Tier-1 pass COMPLETE, 2026-09-02, same session — 10 of the 14 R1 records now carry a
`[noldeke_check]` block.** ⛔ **Correction (2026-09-02, caught while writing the web build's
`/about` page and verified against the records themselves):** this was first written as "all
fourteen," which is wrong — four records have no `[noldeke_check]` and none is missing by
oversight: `p004-1` (the alphabet table) and `p132-1`/`p132-2` (calendar lexical lists) have no
Nöldeke counterpart to collate against, and `p044-1` (Peal perfect with object suffixes) is
still genuinely owed, not yet run. Net result on the 10 that were checked: mostly confirmation,
but three real, actionable findings, not just reassurance:

1. **`p031-1` (noun-state survey), row I.b 'foot':** Nöldeke's general state-ending rule
   (§70) predicts feminine plural endings (-ān/-āth/-āthā) for a fem. noun like reglā; this
   record's plate reading used the masculine pattern (-in/-ay/-ē) instead. Tier-1 can't say
   which side is wrong — only that the `uncertain` flag already on this row was earning its
   keep, and it needs an actual second plate look, not a memorized-paradigm "fix."
2. **`p034-1` (noun+suffix rule):** Nöldeke's §145 states the identical coalescence rule with
   a full, cleanly English-labeled worked example ('judgment', all 10 persons × sg/pl) — a
   genuinely better reference than this record's own low-confidence `seq1-7` guesses at
   Nestle's 7-item example list. Follow-up: re-crop Nestle's p.34 line and match each of the 7
   printed forms against Nöldeke's named set instead of leaving them as unlabeled shapes.
3. **`p063-1` (prepositions), the `bāṯar` entries:** Nöldeke shows 'behind' and 'after' as
   TWO separate derived prepositions (different roots — 'on the track of' vs 'hiding from'),
   not one word covering both senses the way this record currently has it. A real correction
   to make on a follow-up pass, not just a confidence question.

Also two clean confirmations worth knowing: `p023-1`/`-2` (the longest-owed pair) both check
out against Nöldeke §63-64, including the existing `noldeke_qualifier` on `p023-2` turning out
to be exactly right (Nöldeke really does split this differently from Nestle, as already noted
before this check ran). `p037-1`'s numerals 1-10 also confirmed (prior turn).

✅ **All three findings RULED AND ACTED ON, 2026-09-02, same session — re-cropped the actual
plates rather than reasoning from the Nöldeke comparison alone:**
1. **`p031-1` row I.b 'foot':** re-verified on a second, tighter (3.2x) crop. The masculine
   -in/-ay/-ē plural pattern IS what's printed — confirmed, not a first-pass misread. Open
   question is now purely lexical (why a 'foot' word takes masculine endings — wrong lexeme
   ID, or a real Nestle-specific usage), explicitly left for a Syriacist, not re-guessed.
2. **`p034-1` noun+suffix examples:** re-cropped at 2.8x and mapped Nestle's 7 printed forms
   against Nöldeke's confirmed 10-item named set by shape/length correlation. Real upgrade —
   `translit_uncertain` fields went from bare unlabeled guesses to person-tagged proposals
   (`gram_tags_proposed`) — but flagged honestly as still short of glyph-level certainty.
3. **`p063-1` bāṯar split:** re-cropped at 5x and CONFIRMED Nestle's plate really does print
   two distinct Serto words before the shared gloss 'behind, after' — the original record's
   merge was a genuine transcription gap, now fixed with two separate `[[rule.prepositions]]`
   entries. The second word's exact spelling (teth vs taw) stays `uncertain` — visually very
   close to the first at this type size, needs a better crop or a real reader, not a guess.
   Also resolved the 'around' question from the same check: Nestle's own plate confirms
   sḥōr-shaped, so that was a genuine Nestle-vs-Nöldeke vocabulary difference, not an error.

**Genuinely open now:** the `p034-1` example mapping's exact person-assignment (proposed, not
proven) and `p063-1`'s second bāṯar-shaped word's precise spelling. Both need either a tighter
crop than this session managed or an actual Syriacist — not more reasoning from what's already
been read. Everything else in this primer's R1 zone (all nine original runbook targets plus
the bonus preposition record) is now extracted, tier-1 checked, AND re-verified where the
check found something.

## ✅ DONE — Payne Smith vocab gap, closed 2026-09-02 (Opus, on Wilson's "opus go for step 2")

**27 R4 records in the new `quarry/payne-smith-1903/r4/`** — all 22 original targets, plus the
four smaller items the runbook parked (ordinals ܫܬܝܬܝܐ / ܫܒܝܥܝܐ, ܐܡܝܢ "amen", ܒܝܫܐ "evil"),
minus **Cain**, which got a ruling instead of a record: Payne Smith has **no entry for ܩܐܝܢ**
at all — six text hits, every one a citation inside another word's entry, and the ܩ section's
opening page (486) read in full shows no headword. Not even a bare cross-reference. It's a
`word_notes` flag for whichever Lesson 9 record uses it; that record isn't written yet and was
deliberately not invented.

Full write-up, corrected page numbers, and the method are the **last section of
`PAYNE-SMITH-VOCAB-RUNBOOK.md`** — read that, not this summary. Three things worth carrying:

1. ⛔ **The runbook's own "real fix" retraction was itself wrong.** Its `n = api_page − 53`
   rule is not a constant offset (58 leaves are marked `Delete` in `scandata.xml` and drop out
   of the image sequence), so it degrades from ~1 at the front to ~53 at the back and produced
   at least three wrong-lemma "high confidence" locations (deep, debtor, multiply) that were
   caught only by checking the root on the plate. The method that works — pageindex+searchtext
   sliced per leaf, `scandata.xml` for leaf→image, **printed page = n − 15**, and then a
   free self-check (most pages' OCR begins with their own printed number: **431/453 agree**) —
   is written up as a reusable recipe. ⭐ Run that self-check first on any future archive.org scan.
2. ⛔ **`voc` is empty in all 27 records, on purpose.** The plates are pointed and the points are
   visible, but there is no control table for this typeface's pointing and no second
   transcription, so the consonantal skeleton + POS + English gloss went in (all plate-read,
   all reliable) and the vocalisation stayed out, flagged in each record. **This is now the
   single highest-value thing to hand a Syriacist if that seat is ever filled** — 27 records
   that need only vowel points, not re-extraction.
3. **10 of 27 carry `uncertain = true`**, none of them a doubtful lemma — they are coverage
   gaps (part of a long entry ran past the crop) or genuinely unresolvable plate details. One
   is a real hole to close: **`p491-qadesh` has the Pael but NOT the Ethpaal that Lesson 6
   wants**, and `p557-shbaq` has only senses f–h. Each is one more crop of a page already
   fetched.

⚠ The directory + schema shape used (`quarry/payne-smith-1903/r4/`, `source.primer =
"payne-smith-1903"`, `fills_gap_for`) is the runbook's **proposed** extension — unopposed but
never actually blessed by Wilson. Worth a one-word ruling before anything else lands under it.

## ✅ DONE — the web build, per `SYRIAC-WEB-PLAN.md` (history; the live task is further down)

✅ **Lessons 2–10 WRITTEN 2026-09-02** (commit `42c6e14`, Opus-tier fork, all Syriac verbatim from
the R3 records; two source flags carried forward unresolved — c068-1's v.11 conjunction in L2,
c080-1's v.14 word order in L10). The course is complete on paper: `learn/syriac/LESSON-0.md` … `learn/syriac/LESSON-10.md`.

✅ **All five phases of `SYRIAC-WEB-PLAN.md` §5 shipped, 2026-09-02–03, Sonnet (Opus on
`/about`/`/for-syriacists` prose per §8).** **syriac.paleography.app is LIVE** — Vercel project
`paleography-syriac` (Labs team), Cloudflare CNAME, TLS confirmed. Phase A (tree + renderer +
981 R1/R3/R4 record pages), B (drill engine, generalized from the G2-passed "First Light"
artifact, `learn/syriac/drill/L00.toml`/`L01.toml` transcribed verbatim), C (sidecars L02–L10),
D (`/about`, `/for-syriacists`, `/sources`, `/`), E (deploy) — all committed, `master` at
`03031a2`+ (see `git log --oneline` for the full commit chain, one per phase).

Two real content gaps this build's own verbatim check caught and Wilson ruled on rather than
silently working around: Lesson 0 was missing First Light's "Pairs" track (added, per his
"add it to the lesson" ruling); Lesson 0's opening paragraph read backwards ("Lesson 1 asked
you to...") from when Lesson 0 was retrofitted before Lesson 1 — fixed 2026-09-02 along with
three other live-site fixes from Wilson's own read-through: Lesson 1's Stage 0 was fully
re-teaching the alphabet Lesson 0 already covers (trimmed to what's actually new); the italic
metadata paragraph was rendering raw `quarry/...toml` paths as a wall of `<code>` chips on the
page (now stripped from display, kept for the record-footer machinery); the drill mount moved
from after Stage 1 to right after the headnotes; the drill's inherited `position:sticky` header
(fine for First Light as a standalone app, wrong embedded mid-page) drifted on mobile Safari —
now static, verified with Playwright at a 390×844 viewport.

**Held per NEXT-SESSION.md's own standing ruling:** the Syriacist outreach email (item 2 below)
is unblocked now that a live public artifact exists to point to — still explicitly Wilson's own
send, not part of the build.

## ⭐ THE IMMEDIATE NEXT TASK — two new ideas, scored 2026-09-03, not started

Wilson raised both live, right after the web build shipped, and explicitly asked for a
**separate session to design them** rather than have either built ad hoc off a one-line ask.
Per [[reference_model-prudence-rubric]], both are greenfield-scoping work — **run that session
on Fable**, and steer it toward ending in a written score (a plan/conventions file) the way
`SYRIAC-WEB-PLAN.md` itself was scored, not toward code. A cheaper session executes the score
afterward, same pattern as the web build's own Phases A–E.

1. ✅ **SCORED 2026-09-02 (Fable) → `SYRIAC-PDF-PLAN.md`. Phases 0+1 BUILT same day (Sonnet,
   commit `c849312`) — `learn/tools/make_pdf.py` + `learn/shell/print.css` +
   `learn/fonts/` (self-hosted OFL: EB Garamond, IBM Plex Sans, Noto Sans Syriac).**
   All 11 lessons pass `--check` and are written to `learn/site/pdf/lesson-N[.pdf|-a4.pdf]`
   plus `chrestomathy[.pdf|-a4.pdf]` (gitignored, built not committed, regenerate with
   `python3 learn/tools/make_pdf.py`). Five real bugs found by rendering-and-looking, not
   page-counting alone (full list in the commit message): a CSS comment containing a literal
   `</style>` closed the style element early and dumped the rest of the stylesheet as visible
   page text; the vocabulary sheet needed a HALVED cap since it shows both directions per
   word; the forms sheet was printing the cell answer next to its own blank (fixed to show
   neither answer, matching "closed-book"); Lesson 0's letters and pairs/triples sheets had
   no cap and silently overflowed past the fixed footer (Chrome doesn't repaginate content
   colliding with `position:fixed`, so the page-count check missed it — only spotted by
   rasterizing and looking); a fresh `--user-data-dir` never exits after `--print-to-pdf`
   (background component-updater fetches outlive the render) — fixed by polling for a
   size-stable output file instead of waiting on the process to exit. ⬜ **OWED, and only
   Wilson can do it — the actual paper G3 gate the plan calls for**: three PDFs sent via
   SendUserFile (Lesson 0, Lesson 2, Lesson 10 — start/median/capstone) for him to print
   duplex and run with a pencil. ⚠ **One known cosmetic gap, not yet fixed**: a few dense
   Stage-1 word-by-word tables (many short columns) run past the print margin on paper,
   where the web page can scroll horizontally and paper can't — needs either smaller type
   for wide tables or a wrapping strategy, best judged after Wilson's own read-through.
   Phase 2 (wire into the site + deploy) is UNSTARTED and has its own hard stop
   (production deploy) per the plan's own §7. Scoring-session details (the smoke test that
   ruled out LaTeX/weasyprint/wkhtmltopdf, the duplex-parity mechanism, the Noto-not-Meltho
   fact, §9's seven rulings) are in `SYRIAC-PDF-PLAN.md` itself, not repeated here.
   *(Original ask, kept for the record:)* grammar notes up front,
   drills at the end, **answers printed on the back** (so the sheet works closed-book,
   face-down, the way a paper worksheet would). Nothing was scoped at the time: not the
   layout, not the generation tool (LaTeX? a print
   stylesheet + browser print-to-PDF? `weasyprint`/`wkhtmltopdf` off the same rendered HTML
   Phase A already produces?), not whether it's one PDF per lesson or one for the whole course,
   not where the file lives (uploaded per lesson? generated at build time into `learn/site/`
   alongside everything else, so `make_learn.py` owns it the way it owns every other surface?).
   The lesson content itself (`learn/syriac/LESSON-N.md`, `drill/LNN.toml`) is already the
   single source everything else in this build derives from — the PDF should be a fourth
   consumer of that same source, not a fifth hand-authored thing to keep in sync.
2. **A calligraphy / stroke-order generator**, showing HOW a letter is formed (pen-path order),
   not just its finished shape — the thing Lesson 0 currently doesn't teach at all (it's
   recognition-only: name the shape, say the sound). **This is not a new idea — it is
   `SYRIAC-LANGUAGE-PILOT.md` §10's second deferred idea, already scoped in outline**: a
   generation *engine* keyed off each script's stroke-order data (not a hand-drawn animation
   per letter, so it's cheap to point at a future script), producing an animated GIF or
   equivalent of a letter's strokes flowing in order, then a word's letters flowing and
   joining. **Read that section before starting** — it already raises the one real
   architectural question this session needs to settle: whether the engine belongs on the
   *language* side (`syriac.paleography.app`, teaching formation) or the *hand* side
   (`paleography.app`, since ductus is a manuscript-reading fact too), or is shared machinery
   like the registry itself. Cross-project by design — Hebrew, Coptic, Devanagari and Syriac's
   own Serto/East Syriac variants all hit the same wall, so whatever gets built should not be
   Estrangela-specific under the hood even though it ships for Estrangela first.

Not yet decided whether these are one Fable session or two — item 2 is the harder
architectural call (it isn't only a Syriac decision) and may be worth scoring on its own.

## ✅ DONE — write Lessons 2–10 out as documents (history)

Everything upstream is now in place. `SYRIAC-LESSON-PLAN.md` has all ten lessons scored;
`learn/syriac/LESSON-0.md` and `learn/syriac/LESSON-1.md` are fully worked and G2-passed; R3 has 20 solid keyed pages;
R1's nine paradigm targets are all extracted and tier-1 collated against Nöldeke; and the R4
vocabulary gap those lessons opened is now closed by the Payne Smith pull above. Per §6 a
lesson is built backward from its R1/R3 material, so the material has to exist first — it does.

This is a **sequencing/writing pass, not extraction** — but the pattern is already Fable-set:
Lesson 0/1 (`SYRIAC-LANGUAGE-PILOT.md` §9) were themselves written in the Fable session that
scored all ten lessons, and Wilson G2-passed them. Writing 2–10 is executing that already-
designed, already-validated template against fully-extracted material — per the model-prudence
rubric that's **Opus** ("Opus executes a Fable-written plan"), not a fresh Fable pilot and not
Sonnet (each lesson still needs real synthesis of R1/R3/R4 material into the pedagogical voice
Lesson 0/1 set, not mechanical templating). Ruled 2026-09-02, correcting this file's own
earlier "Fable/Sonnet" guess, which predated Lesson 0/1 actually landing and passing G2.
Two things to fold in as you write:
- Each Payne Smith record names the lesson it serves in `fills_gap_for` — use that as the
  vocabulary checklist per lesson, and write the `word_notes` cross-links back the other way.
- **Cain (Lesson 9) needs a `word_notes` gloss written by hand**, since no dictionary record
  backs it. Same likely applies to any other proper noun a lesson introduces — check before
  assuming R4 covers it.

**What this is NOT:** not the generative multiple-choice drill *engine* (`SYRIAC-LANGUAGE-PILOT.md`
§10 — a bigger, separate design decision, building over R1–R4 records at scale for every future
language). Not the SRS/Tabella-adjacent vocab-and-parsing engine Wilson flagged the session G2
passed (`paleography.md`, 2026-09-02, not started, not scoped). Not more R1 or R4 extraction —
both zones are done for this primer, and the two genuinely open R1 items (`p034-1`'s
person-assignment, `p063-1`'s second bāṯar-shaped word) need a real reader, not another pass.

---

## State, briefly — detail lives in the docs named, not repeated here

- **Phase 1 (R3, the chrestomathy) is done.** 65 pages + the Lord's Prayer. 22 pages
  (Genesis 1-4, Matthew 5, Lord's Prayer) are fully keyed and independently diffed against PD
  editions — lesson-ready. 44 pages (Vitae Prophetarum, Historia inventionis) are partially or
  wholly unkeyed — a different, open problem (needs a Syriacist seat or Serto HTR), not more
  of the same extraction. Full picture: `quarry/nestle-1889-en/MAP.md` "R3 — RUN COMPLETE".
- **Phase 3 (lesson design) drafted 2026-09-02.** Ten lessons scored in `SYRIAC-LESSON-PLAN.md`
  from the 20 solid R3(a) pages; `learn/syriac/LESSON-0.md` (alphabet, added after Wilson's own G2 feedback)
  and `learn/syriac/LESSON-1.md` (Gen 1:1-5) are fully worked. Lessons 2-10 are scored but not yet written
  out as documents — do that only after G2 passes on 0/1.
- **Two future-idea notes recorded, both explicitly deferred, neither started:**
  1. The eventual web build = a generated multiple-choice drill engine over R1-R4 records, not
     a static single page. `SYRIAC-LANGUAGE-PILOT.md` §10.
  2. A stroke-order/letter-formation GIF-generation engine, Syriac as proof of concept,
     meant to generalize to every future non-Roman script (and possibly the paleography
     hand-reading side too). Same §10, second half.
- **R1 (grammar paradigms) is scoped, not yet extracted.** 6 calibration records exist
  (alphabet + 2 pronoun tables + Peal-perfect-with-suffixes + 2 calendar tables), all
  unadjudicated. `SYRIAC-R1-RUNBOOK.md` (written 2026-09-02) turns Lessons 2-10's own "new
  form cells" lines into a deduplicated 9-paradigm target list — see the immediate-task
  section above.
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
   ⭐ **RULED, 2026-09-02 (Wilson): hold this email until something stable and public exists
   to point to.** Reasoning in his own terms: anyone who doesn't work with LLMs a lot will
   underestimate what a one-man shop can actually do here and dismiss the pitch on priors,
   sight unseen. A cold ask that says "we're extracting Nöldeke-adjacent grammar with an LLM,
   want to help adjudicate" reads as implausible without a working page to click through.
   **Gate: don't send until there's a live, public artifact demonstrating the pipeline** —
   the G2-passed drill prototype turned into real site content is the natural candidate, not
   raw calibration TOML in a git repo. Since item 1's licence-question email goes to the same
   two people, it likely waits too unless split into its own, simpler ask — Wilson's call, not
   decided here.
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
