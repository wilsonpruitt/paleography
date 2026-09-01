# Syriac language pilot — PD primers, re-sequenced reading-first

*Wroot Labs · Fable planning session 2026-08-31 · status: PLAN. Execution is Opus/Sonnet work
(see §9); nothing here is built. Companion to `EXPANSION-PLAN.md` — that plan covers the
manuscript-hand side; this one covers the language side of the same door.*

Wilson's brief: the desire to learn languages survives machine translation, and for manuscript
languages the practice is heavily gated — for Syriac the options are scans of Nöldeke or a
graduate seminar, with nothing in between. Meanwhile the pedagogical corpus itself is public
domain: the 19th-century primers (grammar + chrestomathy + glossary in one volume) hold
expert-composed, classroom-tested material trapped in book order. **Extract it, tag it,
re-sequence it by contemporary acquisition ideas, and ship scaffolded practice.** The primers
are a quarry, not a syllabus.

---

## 1. Governing rulings (Wilson, 2026-08-31 unless noted)

1. ⭐⭐ **"Learning Syriac to read Syriac, not to pass a test."** Reading-first governs
   everything: vocabulary order comes from the target reading corpus, forms enter when the
   reading needs them, and paradigm completeness is never a gate. Paradigms stay in the bank
   as reference and spaced-repetition material, not as chapter walls.
2. ⭐ **Estrangela leads.** It is the root script, and it is what the early manuscripts — and
   the live `/syriac` hand track — use. Serto and East Syriac are introduced later as
   *variants of forms already known*, exactly how the hand-trainer treats a second hand.
3. **The twin paths feed each other.** The finish line of the language ramp is a real
   chrestomathy passage; stage 0 of the paleography ramp is that same passage as ink. The
   handoff between products is a line of text the learner already knows. Letter-confusion
   data flows both ways (PLAN.md's confusion-matrix thesis, extended).
4. **Separate from Tabella.** Decks may eventually export there; this is not a Tabella
   feature and takes no dependency on it.
5. **Free, like the trainer.** The source material is PD; the exercise bank is not paywalled.
6. ⭐ **Wilson is learner #1 — the tool must teach HIM** (standing ruling, and the
   [scaffold-the-learner rule](#8-traps) applies with full force: never let the data decide
   the curriculum).

## 2. What the pilot is — and is not

**Is:** (a) a verified inventory of the PD Syriac primer shelf with one chosen high-res scan
per title; (b) a decomposition schema proven against **one full primer**; (c) a corpus-derived
frequency spine; (d) a ten-lesson reading-first sequence **on paper**, lesson 1 tested on
Wilson. That is the whole pilot.

**Is not:** a web build, a product surface, a Duolingo competitor, an exam-prep course, a
transcription workbench (eScriptorium exists), or a decision about where this lives on the
web. Hebrew (consonantal-first) is explicitly the *second* language and inherits whatever
survives contact with Syriac — same pattern as Hungarian leading the self-produced GT band.

## 3. The primer shelf (candidates — Phase 0 verifies)

⚠ **No archive.org identifier below is asserted from memory** — the shelfmark ≠ text trap hit
three times in one Bibliotheca Arabica session, and scan IDs are exactly as treacherous.
Phase 0 finds and pins each ID. Editions and roles are the judgment; IDs are execution.

| Work | Ed. to seek | Language | Role in the quarry |
|---|---|---|---|
| **Nestle, *Syriac Grammar with Bibliography, Chrestomathy and Glossary*** | English tr. (Kennedy), Berlin 1889 | English | ⭐ **The pilot primer** — compact, purpose-built, all four record types in one volume |
| **Brockelmann, *Syrische Grammatik*** (Porta Linguarum Orientalium) | 1899 or later PD ed. | German | Second chrestomathy + glossary; cross-check Nestle's grammar-point coverage |
| **Rödiger, *Chrestomathia Syriaca*** | 2nd ed. 1868 | Latin apparatus | Deepest passage quarry — feeds lessons beyond the pilot ten |
| **Robinson, *Paradigms and Exercises in Syriac Grammar*** | 1st ed., Oxford 1915 | English | The exercise book (Coakley's revisions are in copyright — **1915 original only**). ⚠ Verify whether 1915 includes keys |
| **Nöldeke, *Compendious Syriac Grammar*** | tr. Crichton, London 1904 | English | **Reference grammar + the § taxonomy** (§4) — not a lesson source |
| **Payne Smith, *A Compendious Syriac Dictionary*** | Oxford 1903 | English | The PD lexicon; glossary entries link to it |
| Uhlemann (tr. Hutchinson, 1855) · Phillips, *Elements* (1837/1866) | as found | English | Reserve bench — mine only if the primary four leave gaps |

**Scan acceptance bar (ruled 2026-08-31, prior session): vowel-point legibility, not overall
dpi.** A scan where the West Syriac vowel letters or East Syriac dot patterns smear is
unusable regardless of how clean the consonants are. Protocol per candidate scan: pull 3
full-res pages via the archive.org download path (`research/` has the leaf-offset drill —
see [[reference_archive-org-page-images]] in memory), one from the grammar, one from the
chrestomathy, one from the glossary; pass/fail on whether every diacritic is individually
resolvable at 100%. ⛔ The digits in an archive ID are the ITEM number, not the volume —
check the running head. HathiTrust sometimes holds the better copy of the same edition;
check it when archive.org's best fails the bar.

⭐ **The primer's printed script does not constrain the product's script.** We extract *text*
and re-render it ourselves in Estrangela (Beth Mardutho's Meltho fonts — verify licence, it
is expected to be free). Whether Nestle printed Serto or Estrangela matters only for OCR
difficulty, never for what the learner sees. Only the paleography side ships images.

## 4. The four record types (the schema)

Everything extracted lands in one of four record types. Format: TOML files under a new
`registry/`-style directory (stdlib `tomllib`, no deps — house pattern), one file per record,
content-addressed by primer + location. Every record carries provenance:
`source = { primer = "nestle-1889-en", page = 43, leaf = "n55" }`.

**Shared grammar-point namespace: Nöldeke section numbers.** Every later grammar
cross-references him; the 1904 English translation is PD; his §§ are the stable coordinate
system this project would otherwise have to invent. Records tag `noldeke = ["§64"]`. Where a
primer teaches something Nöldeke splits or lacks, the tag is the nearest § plus a free-text
qualifier — never a new invented ID in the pilot.

### R1 — Paradigm table
`lexeme` (lemma, unvocalized + vocalized) · `category` (verb stem/tense, noun state, suffix
set…) · `cells` (list of `{gram_tags, form_unvoc, form_voc, translit}`) · `noldeke` ·
`source`. ⚠ One table in print is often several tables in data (strong verb ≠ its footnoted
weak-verb variants) — split on category, not on typography.

### R2 — Composed exercise
The author's own sentences — the part of the primer that exists nowhere else and the only
part that genuinely needs OCR. `direction` (syr→en | en→syr) · `text_syr` (unvoc + voc as
printed) · `text_en` · `key` (if the volume has one; else `key = ""` and the field is filled
by translation *marked as ours, never as the primer's*) · `vocab_lemmas` (list, linked to R4)
· `noldeke` (what the sentence drills) · `source`.

### R3 — Chrestomathy passage
`work` (canonical: e.g. `peshitta:matt:5:1-12`, `ephrem:carmina-nisibena:…`) · `text_syr` as
printed (layer-declared: vocalized? seyame? punctuation?) · `alignment` (§5: which digital
text it was matched to, and the diff) · `primer_notes` (the author's philological footnotes,
kept — they are gloss fodder) · `source`.

### R4 — Glossary entry
`lemma` (unvoc + voc) · `gloss_en` · `pos` · `root` · `payne_smith` (page ref) ·
`frequency_rank` (filled in Phase 2 from the corpus, **not** from the primer) · `source`.

**What is NOT extracted:** the comparative-philology digressions, the Hebrew/Arabic cognate
apparatus, the bibliography chapters, prefaces. That is the filler; naming it here is what
makes the run smooth. If an extractor is unsure whether something is filler, it flags — it
does not extract "to be safe" (bank bloat is a cost, per the fragment-filter lesson).

## 5. Extraction method — align, don't transcribe

**Chrestomathy passages (R3): identify → align → diff.** Most passages are excerpts of known
texts (Peshitta, Ephrem, chronicles). The job is to name the passage, fetch the existing
digital text, and align — OCR only *confirms the primer's variants* against the digital
text. Full transcription is reserved for R2 (the author's composed pages) and any R3 passage
that cannot be matched.

Digital text sources, each **licence-checked before a byte is stored** (HTR-United ingest
discipline; fill this table in Phase 0):

| Source | Holds | Licence | Verdict |
|---|---|---|---|
| Digital Syriac Corpus (syriaccorpus.org) | TEI texts, patristic + more | ⬜ verify per-text | ⬜ |
| SEDRA / Beth Mardutho | lexical DB; **lemmatized Peshitta NT** | ⬜ verify (API terms) | ⬜ |
| Meltho fonts (Beth Mardutho) | Estrangela/Serto/East Syriac fonts | ⬜ verify | ⬜ |

⚠ The Ómagyar precedent governs: a corpus can be *readable but unshippable* (keyed from
in-copyright editions, or licence-silent). Such a source may **check** our text, never
**become** it. If the Peshitta text we want to ship turns out encumbered, the fallback is
keying it ourselves from a PD printed Peshitta — slower, but the pilot's ten lessons need
tens of verses, not the canon.

**Composed exercises (R2): plate-read, house rules.** Vision plate reads at full resolution;
⛔ never read codepoints by eye (the MUFI rule generalizes — Syriac diacritics are worse);
**vocalisation outranks the sense** for transcription QA ([[reference_arabic-control-rule]]
transfers whole, including the blind-control protocol on a sample). Declare the layer of
every extracted text — "the declared layer can be wrong" was the expensive Phase-1 lesson,
and a primer that *says* it prints vocalized text will still have unvocalized lines.

**Curriculum QA is separate from transcription QA.** Reading-first demotes vocalization in
what the *learner* sees first; the *extractor* captures every point faithfully. Opposite
answers to different questions — do not let one leak into the other.

## 6. Re-sequencing — the actual reorder

**The frequency spine (Phase 2).** Compute lemma frequency from the target reading corpus —
the Peshitta gospels first (SEDRA's lemmatization makes this nearly free *if* the licence
clears; otherwise lemmatize the pilot's own passages by hand — ten lessons need only a few
hundred lemmas). ⚠ Not textbook word lists, not the primer's chapter order, and not raw
token counts without lemmatization. R4 records get `frequency_rank` from this spine.

**The lesson unit.** A lesson is built backwards from its destination: **every lesson ends in
real text.** Pick the chrestomathy passage first (easiest passages = highest cumulative
lemma coverage + lowest new-form count — score it, don't eyeball it, but ⚠ remember the
degenerate-metric lesson: a naive scorer will sort by length; filter fragments). Then derive
what the lesson must teach: the new lemmas (R4), the new forms *those words actually
exhibit* (R1 cells — the cells, not the whole table), and 3–6 composed sentences (R2) that
drill exactly those items. Nöldeke §§ are the audit trail proving coverage, never the
ordering principle.

**The ramp inside a lesson mirrors the trainer's** (recognition before recall):
0. *Orientation* — the new letterforms/points named, printed beside transliteration.
1. *Read along* — passage with full gloss, nothing typed.
2. *One word* — cloze in the TEXT (the gap goes in the text; no segmentation needed —
   the same unlock as the trainer's).
3. *Finish the line* — first half given.
4. *The whole line* — unaided, then the same line as ink on the `/syriac` hand track.

Stage 4's manuscript handoff is the twin-path convergence made physical, and it is why
lesson passages should prefer texts with witnesses in (or addable to) the hand track's bank.

**Script ramp:** lessons 1–10 are Estrangela only. Serto/East Syriac enter post-pilot as
letterform-variant lessons on *known* text — the trainer's compare-against-Caroline
pedagogy, applied to type.

## 7. Exit gates

- **G0 (inventory):** every shelf title has a pinned, vowel-point-legible scan or a recorded
  fail + HathiTrust fallback; the licence table in §5 has verdicts; Nestle's scan chosen.
- **G1 (schema survives):** Nestle fully decomposed into R1–R4 with counts reported
  (expect order-of-magnitude: dozens of R1, low hundreds of R2/R4, dozens of R3). Schema
  changes forced by contact are folded back into this document *before* a second primer.
- **G2 (sequence on paper):** ten lessons drafted, each ending in aligned real text.
  **Wilson runs lesson 1. If it is beyond him, that is a design defect report** — revise the
  ramp, not the learner. No web build before G2 passes.
- ⛔ **Stop rule:** if fewer than ~⅔ of Nestle's chrestomathy passages can be matched to a
  shippable digital text, the align-don't-OCR economics have failed — stop and re-plan
  (probably: key the passages ourselves and re-cost) rather than grinding OCR through the
  whole chrestomathy.

## 8. Traps

Named because each has already cost a session somewhere in this house:
- **The data must not decide the curriculum** — Nestle's chapter 1 is not lesson 1
  ([[feedback_paleography-scaffold-the-learner]]).
- **Declared layer can be wrong**; **shelfmark ≠ text**; **item number ≠ volume**.
- **Never read diacritic codepoints by eye**; **vocalisation outranks the sense** (QA only).
- **Empty grep ≠ absence** — a passage the aligner can't find is a query problem first.
- **Readable ≠ shippable** (licences); attribution goes on the page at ingest, not later.
- **A degenerate difficulty metric sorts by length** — validate the passage scorer on a
  sample before trusting its ranking.

## 9. Execution (model tiers, per the prudence rubric)

- **Phase 0 — inventory + licences (Sonnet):** find/pin scans, run the 3-page legibility
  protocol, fill the §3 and §5 tables. Mechanical, protocol-driven.
- **Phase 1 — decompose Nestle (Opus):** plate reads + R1–R4 extraction. Volume work with
  judgment at the margins; Opus per the Acta precedent for plate-heavy runs. ⚠ This is the
  token-heavy phase — estimate the burn from the runbook's own per-unit figure and put the
  "which model, and go?" stop to Wilson before dispatch.
- **Phase 2 — frequency spine (Sonnet):** licence-gated computation over the digital
  Peshitta; a script, not a judgment.
- **Phase 3 — ten lessons + lesson-1 test (Fable, short):** the sequencing is the
  judgment-dense step and ends with Wilson as learner #1.

No repo decision needed yet: pilot records live under `~/paleography` beside the registry
(the twin paths share machinery); if the language side outgrows the repo, splitting is a
G2-passed problem.

## 10. Deferred — decided later, on purpose

Product surface and URL · Hebrew track (consonantal-first; hostable unpointed corpus needs
its own inventory — DSS is link-only by standing ruling) · deck export toward Tabella ·
the Syriacist expert seat (⚠ the same Ishac/Roughan email already owed for the Vienna
licence question is the natural opener — but outreach is Wilson's send, a hard stop) ·
whether primer-author philological notes become learner-facing glosses or stay quarry.
