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

✅ **Phase 0 ran 2026-08-31 — G0 PASS.** Every ID below is now pinned and probed (3-page
vowel-point protocol); full record with probe leaves, offsets and copy defects →
`research/syriac-pilot-phase0.md`. Editions and roles below were the judgment; the pinned IDs
are the execution.

| Work | Pinned scan (probed ✅) | Language | Role in the quarry |
|---|---|---|---|
| **Nestle, *Syriac Grammar with Bibliography, Chrestomathy and Glossary*** (Kennedy tr., 1889) | **`syriacgrammarwit00nestiala`** | English | ⭐ **The pilot primer** — compact, purpose-built, all four record types in one volume |
| **Brockelmann, *Syrische Grammatik*** (PLO V, 2nd ed. 1912) | `syrischegrammati00brocuoft` | German | Second chrestomathy + glossary; cross-check Nestle's grammar-point coverage |
| **Rödiger, *Chrestomathia Syriaca*** (2nd ed. 1868) | `chrestomathiasy00roed` | Latin apparatus | Deepest passage quarry — feeds lessons beyond the pilot ten |
| **Robinson, *Paradigms and Exercises in Syriac Grammar*** (1st ed. 1915) | `bwb_KU-996-498` (⚠ pencil marginalia in this copy) | English | The exercise book (Coakley's revisions are in copyright — **1915 original only**). ✅ Verified: **1915 has NO keys** → every Robinson R2 gets `key = ""` |
| **Nöldeke, *Compendious Syriac Grammar*** (tr. Crichton 1904) | `CompendiousSyriacGrammar` | English | **Reference grammar + the § taxonomy** (§4) — not a lesson source |
| **Payne Smith, *A Compendious Syriac Dictionary*** (1903) | `compendioussyria00payn` | English | The PD lexicon; glossary entries link to it |
| Uhlemann (tr. Hutchinson) · Phillips, *Elements* | `uhlemannssyriacg00uhleuoft` (1855) · `elementsofsyriac00phil` (1845) — unprobed | English | Reserve bench — mine only if the primary four leave gaps; run the 3-page protocol before use |

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
kept — they are gloss fodder) · `source`
· ⭐ **`word_notes` (ruled 2026-09-01)** — a list of `{index, form_voc, note, nestle_sections,
noldeke}`, one per word the primer comments on. Nestle's "Aids to Translation" are a
ready-made per-word gloss layer keyed to a passage, of exactly the kind the hand-trainer
already ships per line; flattening them into `primer_notes` loses the keying, which is the
part the curriculum wants. A field on R3, **not** a record type of its own — it belongs to the
passage, and promoting an array to its own type later is mechanical.
⛔ **`nestle_sections` is not `noldeke`.** The §§ in a primer's own apparatus are its own
section numbers. Nöldeke is the shared coordinate system precisely because every primer
numbers itself differently; merging the two namespaces destroys the thing that makes the
spine work.

### R4 — Glossary entry
`lemma` (unvoc + voc) · `gloss_en` · `pos` · `root` · `payne_smith` (page ref) ·
`frequency_rank` (filled in Phase 2 from the corpus, **not** from the primer) · `source`
· `gloss_de`, `nestle_section`, `greek`, `hebrew`, `arabic`, `latin`, `plural_voc`,
`variant_voc`, `construct_voc`, `dialect_variant`, `stems`, `see`, `continues_from` — all
added on contact with Nestle, who glosses German | English and carries a comparative
apparatus as a matter of course.
· ⭐ **`sub_lemmas` (ruled 2026-09-01)** — a STRUCTURED ARRAY on the parent, each item
`{voc, gloss_en, gloss_de | gloss, raw}`. Nestle's `‖` sub-lemmas are **not** separate
records: his ordering is by root, so the parent-child link is a claim he is actually making,
and keeping it costs nothing that Phase 2 needs. Measured on the first 18 pages: **253 head
+ 171 sub = 424 lemmas, ~23.6/page**, so the glossary is ~880 records carrying ~1,480 lemmas.
⚑ Every item keeps `raw`, the printed piece verbatim — the parse is a convenience, never the
record.

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

| Source | Holds | Licence (verified 2026-08-31) | Verdict |
|---|---|---|---|
| Digital Syriac Corpus (syriaccorpus.org) | TEI texts, patristic + more | **CC BY 4.0** on TEI editions, PD base texts (confirmed in per-text headers, GitHub `srophe/syriac-corpus`) | ✅ **SHIPPABLE with attribution** — still read each ingested text's `availability` header + credit its encoder at ingest |
| SEDRA / Beth Mardutho | lexical DB; **lemmatized Peshitta NT** | "All Rights Reserved"; SEDRA III terms = personal/academic, no redistribution | ⚠ **SPLIT VERDICT, corrected 2026-09-01 (Wilson).** The DB is compute-only, but **the TEXT inside it is the BFBS/UBS 1905 Peshitta NT, which is PD** — Pusey-Gwilliam gospels (1901), Gwilliam Acts, Gwilliam-Pinkerton Paul, Gwynn Catholic Epp. + Rev., all published 1905. A faithful transcription of a PD text carries no new copyright, so **the text is shippable**; SEDRA's **lemmatization and morphology are not**. Their terms remain a contract on *their files*, so carry the text from a PD edition, not from their export. Confirm w/ Beth Mardutho before deeper dependency |
| Meltho fonts (Beth Mardutho) | Estrangela/Serto/East Syriac fonts | Freeware: redistribution OK, **modification prohibited** | ✅ serve unmodified TTF/OTF; ⚠ no WOFF2 conversion without reading the packaged licence; OFL fallback = Noto Sans Syriac |

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

- ✅ **G0 (inventory): PASSED 2026-08-31.** All six primary titles pinned + probed legible, no
  HathiTrust fallback needed; §5 verdicts filled; Nestle = `syriacgrammarwit00nestiala`.
  Record: `research/syriac-pilot-phase0.md`.
- **G1 (schema survives):** Nestle fully decomposed into R1–R4 with counts reported
  (expect order-of-magnitude: dozens of R1, low hundreds of R2/R4, dozens of R3). Schema
  changes forced by contact are folded back into this document *before* a second primer.
- **G2 (sequence on paper):** ten lessons drafted, each ending in aligned real text.
  **Wilson runs lesson 1. If it is beyond him, that is a design defect report** — revise the
  ramp, not the learner. No web build before G2 passes.

## 7a. R1/R2/R3 execution scoping — ruled 2026-09-01

*Answers "what runs next, in what order" now that R4 (glossary, 874 records) is the only
record type actually executed at scale. R1/R2/R3 are still calibration-only (5/0/3 sample
records). This section is the score for whoever runs them; nothing below is new extraction.*

**R5 does not exist — correct any lingering reference to it.** §4 above already ruled
2026-09-01: Nestle's "Aids to Translation" become `word_notes`, a STRUCTURED FIELD on the R3
record they're keyed to, never a fifth record type. If an older note (`NEXT-SESSION.md`,
pre-dating this ruling) still frames it as an open "R5" question, that framing is stale —
there is nothing left to decide here, only to execute.

**R2 is confirmed ZERO for this primer, not merely low.** `MAP.md` already ruled Nestle
contributes no R2 body (it's a grammar-plus-chrestomathy, not an exercise primer) and pointed
composed-exercise extraction at **Robinson** instead. Its own estimate table still hedged
"1–3" R2 records against the p.70–72 "Reading Exercise," but that hedge is now closed: the
Reading Exercise **is** the Lord's Prayer in the Peshitta (Matt. 6:10–13) — a Peshitta
passage, i.e. R3, not an author-composed sentence. **Nestle: 0 R2 records, confirmed.** Do
not schedule an R2 pass against this primer; it happens against Robinson, in a later phase,
and nothing here blocks on it.

⚠ **Labeling trap in `MAP.md`'s own zone table:** it calls leaves n87–n89 (pp. 70–72) the
"R2 zone," inherited from the schema's original four-way naming before the ruling above. The
content there is actually **one R3 passage (the Lord's Prayer) plus its `word_notes`**,
physically separate from — and outside the leaf range of — the main Chrestomathia block
(n156–n220). A session extracting "the R3 zone" by leaf range alone will skip it. Treat
n87–n89 as a second, earlier R3 source location, not as R2 territory.

**R3 execution order: R3(a) → R3(b) → R1.** This answers `NEXT-SESSION.md`'s open "does R3
run first?" — yes, and here is the split within R3 too:

✅ **R3(a) part 1 — Chrestomathia I (Genesis 1–4, pp. 67–78, 12 records) RAN 2026-09-01.**
Records `quarry/nestle-1889-en/r3/c067-1.toml` … `c078-1.toml`. Three findings that change the
schema or the plan and are folded into `MAP.md` in full:
· ⭐ **Layer alternates by CAPUT, not by page** (I Serto / II Estrangela / III Serto / IV
  Estrangela), so **three pages carry two layers** and a one-layer-per-record assumption is
  wrong for this piece. §4's R3 shape needs `layer` to tolerate a compound value, or a
  `sections` array, before a second alternating primer is attempted.
· ⭐ **Genesis 4 is from cod. Ambrosianus**, printed so by Nestle. A chrestomathy passage can
  change WITNESS mid-piece; `work` alone does not carry that, and the R3 schema has no field
  for it (recorded in `work_note` here). Worth a `witness` field before R3(b), where Chrest. IV
  has three named codices in a row.
· ⚑ **Nestle's square brackets mark his exemplar's gaps, not textual doubt** — verified against
  Barnes at all six occurrences. A learner-facing render must not show them as variants.
Also measured: **the key-then-check pipeline works, and its weak half is pointing.** Barnes is
unvocalized, so the six Serto pages are checked only at the consonant/seyame level and the
vocalisation rests on the plate read; the six Estrangela pages are checked like-for-like and
came out clean. ⛔ A blind control on a vocalized sample ([[reference_arabic-control-rule]]) is
owed before any of this text ships.

✅ **R3(a) part 2 — Chrestomathia II (Matthew 5, pp. 79–85, 7 records) + the Lord's Prayer
alignment (p. 70) RAN 2026-09-01.** Records `r3/c079-1.toml` … `c085-1.toml`; the Lord's Prayer
record's `[alignment]` completed against the same BFBS control (leaf offset pinned: leaf = page + 11,
`research/syriac-peshitta-editions.md`). **R3(a) is now fully done — 22 of 22 pages.**
· ⭐ **Chrest. II is unvocalized Estrangela throughout, not alternating** — the opposite pole
  from Chrest. I. So Genesis and Matthew together give the layer table both poles cleanly.
· ⛔ **New trap for §8: a diff between differently-vocalized (or both-unvocalized) witnesses
  is a consonantal diff only.** "Vocalisation outranks the sense" presupposes both sides are
  pointed; against BFBS this Matthew half checks consonants, seyame and numbering, never a
  vowel. Chrest. I against Barnes is the stronger pointing check for that reason.
· The diff still earned its keep: two genuine edition-level divergences (a transposed word
  order at v.14; Nestle's closing ܐܡܝܢ absent in BFBS) plus one substantive four-limb v.44
  reading confirmed in both PD editions. A handful of plate-level ambiguities were flagged
  `uncertain` rather than resolved by peeking at the control (would be circular).
· **This closes the G1 evidence needed before R3(b):** the key-then-check pipeline has now
  found real divergences on two different pieces, in two different layer configurations.
✅ **R3(b) is authorized to proceed** on this evidence — no further fold-back blocks it, though
the `layer` (compound value) and `witness` schema gaps named in part 1 above are still owed
before the schema is called settled at G1.

✅ **R3(b) part 1 — Chrestomathia III, Vitae Prophetarum (pp. 86–107, 22 records) RAN
2026-09-01.** Records `r3/c086-1.toml` … `c107-1.toml`. ⛔ **This is the run's central
finding: R3(a)'s method does not transfer to unknown texts.** R3(a) worked by keying passages
whose CONTENT was already known (Genesis, Matthew) and checking the keying — that's what
"align, don't transcribe" degraded to once no shippable digital Peshitta existed. Vitae
Prophetarum has no known text at all behind it, only a sense-level Latin rendering of a
DIFFERENT Syriac witness (Schermann 1907). Result: **435 lines across 22 pages, only 250 with
any reading at all (57%), 185 flagged `⟨?LINE NOT READ⟩`; of the 250 read, 104 confident +
132 flagged uncertain — genuinely new text keyed cold, at roughly 37% confidence-weighted
yield.** Nothing was guessed to fill the gap — per §8 / `reference_arabic-control-rule`,
unreadable stayed flagged rather than resolved by inventing a plausible word. The Latin sense
control (Schermann + his proper-name index) caught wrong-looking names but cannot adjudicate a
letter, so it could not lift the rate.
· ⭐ **The one thing that DID lift the rate, worth keeping**: segmenting word slots
  mechanically (ink-column scan, split on gaps ≥11px), then cropping and tiling each run alone
  onto contact sheets grouped by run width — a short word renders at 6-10× instead of ~2%,
  turning e.g. ܕܝܢ vs. ܡܢ into one point-position feature. Tooling at the agent's scratchpad
  (`words.py`, `sheet.py`) — worth promoting into `tools/` before a second unknown-text pass.
· ⚠ **Incident, self-corrected, and instructive**: a scripted edit in the agent's own final
  shard matched a header-comment string instead of a table header and truncated five files;
  the agent rebuilt every structural field from text it still held, but the ORIGINAL
  `[alignment].diff` prose for c089/c090/c091 could not be recovered and is now overwritten by
  the keying pass's text — each record says so plainly rather than hiding it. `~/paleography`
  IS a git repo (the agent's own report wrongly claimed otherwise) — **commit checkpoints
  during a long unattended shard**, not just at the end, so a scripted edit gone wrong has
  something to `git diff` against, not just the agent's own memory of the pre-edit text.
· Two corrections already applied in-record: c091's line-numbering note is fixed (the
  segmenter, not page-trim, was clipping the leading digit of 100/105/110/115); p. 90 line 95
  has NO standalone ܀, so Jeremiah's life does not close as independently as Isaiah's does at
  line 39.
· ⚑ **Highest-leverage single guess in the shard, flagged for a Syriacist**: a recurring
  four-glyph ܐ-?-?-ܐ read as `⟨?ܐܪܥܐ⟩` on all five of pp. 87-91 — if wrong, it's wrong ten times.

✅ **R3(b) part 2 — Chrestomathia IV, Historia inventionis sanctae crucis (pp. 108–131, 24
records) RAN 2026-09-01.** Records `r3/c108-1.toml` … `c131-1.toml`. ⛔ **Confirms part 1's
finding harder: `text_syr_voc` is NOT READ on all 24 pages.** This piece's control (Nestle's
own *De sancta cruce*, 1889) is character-level but not independent — it only checks a keying
against itself — so it gave the agent nothing to key FROM either; the piece is unvocalized
Serto with no digital edition, the master scan tops out at 1586×2512px (verified: `?scale=`
and the `_jp2.zip` member all return the same size — there is no higher-resolution copy to
escalate to), and keying it cold past ~2.5x zoom crossed from careful transcription into
invention. The agent stopped and flagged rather than guess, correctly per §8.
· What WAS established, cleanly: the three codex transitions (Paris. 234 → Add. 14,644 mid-
  page on p. 113 → Vat. syr. 148 clean at 126/127); full folio/column-marker transcription in
  each codex's own citation style; **IV.3 is not a third recension of the legend but an excerpt
  from George of Arbela's *Expositio officiorum* I.24** — Nestle changed WORKS, not just
  witnesses, so `work` for pp. 127-131 must say so; and a **line-for-line correspondence with
  De sancta cruce with zero structural divergence** across pp. 108-126 (DSC leaf = page + 11).
· ⛔ **Corrigenda trap, defused, not hit**: Nestle's own "Korrekturen" in De sancta cruce refer
  to a DIFFERENT manuscript's line numbers (Add. 12,174, DSC's section A) that happen to
  overlap numerically with lines that DO exist in our IV.2 (216, 261 among them) — applying
  them would have silently corrupted five lines. Recorded as a ruling in every affected record.
· Layer: unvocalized Serto throughout, no alternation — the layer table's third distinct case
  (Chrest. I alternates by caput; II is unvocalized Estrangela, constant; IV is unvocalized
  Serto, constant). **Script and pointing are independent axes**, not one `layer` string.
· IV.3 is entirely uncontrolled (De sancta cruce only covers sub-pieces 1 and 2; "Vat. 148" and
  "1267" appear nowhere in it). Lead for later: R. H. Connolly's edition of George of Arbela
  (CSCO Script. Syri, 1911-15) — not yet on the Phase 0 shelf, licence unchecked — would be the
  only genuinely independent (textual, not transcription) control anywhere in Chrest. IV.

⛔ **The consequence for the plan, stated plainly.** R3(b)'s 46 pages did NOT produce 46 pages
of keyed Syriac. They produced: full structural/provenance metadata on all 46 (witnesses,
layers, folios, line ranges, work identification) + partial text on 22 (Vitae Prophetarum,
~37% confidence-weighted) + zero text on 24 (Historia inventionis). **`text_syr_voc` for
unknown-text, unvocalized, no-digital-edition pages is now a named open problem, not a task a
general session can grind through** — it needs one of: a Syriacist seat actually filled, a
Serto-specific HTR pass (Phase 4, currently frozen), or an explicit decision to defer these
24-46 pages' full transcription and build the pilot's first lessons from R3(a)'s 22 fully-keyed
pages alone, which already exceed the "ten lessons" target of §6.

1. **R3(a) — the Peshitta-controlled block, runs first.** n87–n89 (Lord's Prayer +
   word_notes, 3pp) + Chrest. I *Quattuor prima capita Geneseos* (pp. 67–78, n156–n167, 12pp)
   + Chrest. II *Evangelii Matthaei caput quintum* (pp. 79–85, n168–n174, 7pp). 22 pages
   total. Controls are pinned and independent PD editions (`research/syriac-peshitta-editions.md`):
   Barnes 1914 for Genesis, BFBS 1905–1920 (+ Pusey-Gwilliam 1901) for Matthew and the Lord's
   Prayer. **The Syriacist seat is not a precondition here** — these are transcription
   checks against another printed Syriac edition, not doctrinal judgments.
2. **R3(b) — the weaker-controlled block, runs second, only after (a) proves the
   key-then-check pipeline.** Chrest. III *Vitae Prophetarum* (pp. 86–107, n175–n196, 22pp,
   Schermann's Latin + name index — sense-level only) + Chrest. IV.1–3 *Historia inventionis
   sanctae crucis* (pp. 108–131, n197–n220, 24pp, Nestle's own *De sancta cruce* — Syriac
   diff but not an independent witness). 46 pages. Running (a) first means the pipeline is
   proven on independent, character-level controls before it is spent on the two pieces
   whose checks are each weaker in a different way (see `research/syriac-peshitta-editions.md`'s
   own strength table).
3. **R1 (grammar paradigms, pp. 1–69, 40–70 records expected) runs last, after R3.** Reason,
   not just ordering for its own sake: §6 above builds a lesson backward from its destination
   passage, and only extracts the R1 *cells* a chosen passage actually exercises — the whole
   table is bank filler otherwise. Extracting all 40–70 R1 records blind, before any R3
   passage is chosen for a lesson, risks capturing paradigm detail no lesson ends up needing
   and re-deriving priority later. Running R3 first means R1 extraction can be steered by
   which passages actually became lessons, not guessed at from the ToC.

**⛔ The G0-era stop rule in §7 above is now stale wording, not a live risk.** It reads "if
fewer than ⅔ of Nestle's chrestomathy passages can be matched to a shippable digital text,
...stop and re-plan (probably: key the passages ourselves)." That fallback is no longer a
fallback — it is now the method for the WHOLE chrestomathy, ruled 2026-09-01
(`research/syriac-peshitta-editions.md`): no shippable digital Peshitta exists, so every
passage is keyed from Nestle and checked against a PD scan, never aligned to an existing
digital text. The ⅔ threshold never fires because the method it was guarding against was
already replaced. Leave the stop rule in §7 as a historical note; do not gate R3(a)/(b) on it.
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

- ✅ **Phase 0 — inventory + licences: DONE 2026-08-31** (ran in a Fable session with the
  model nudge given). Results → `research/syriac-pilot-phase0.md`.
- **Phase 1 — decompose Nestle (Opus):** plate reads + R1–R4 extraction. Volume work with
  judgment at the margins; Opus per the Acta precedent for plate-heavy runs. ⚠ This is the
  token-heavy phase — estimate the burn from the runbook's own per-unit figure and put the
  "which model, and go?" stop to Wilson before dispatch.
- **Phase 2 — frequency spine (Sonnet):** licence-gated computation over the digital
  Peshitta; a script, not a judgment.
- ✅ **Phase 3 — ten lessons drafted 2026-09-02 (Fable).** Score → `SYRIAC-LESSON-PLAN.md`;
  worked lesson 1 (Gen 1:1–5, the scored winner) → `LESSON-1.md`. Built entirely from the 20
  checked pages; Serto-printed passages are re-rendered per §3's script ruling (flagged, not
  silent).
  ⭐ **First real G2 feedback landed the same day.** Wilson read Lesson 1 and reported a design
  gap: it asked him to decode shapes and read for meaning simultaneously, with no prior pass
  on the alphabet itself. Per §7's own G2 rule ("if it is beyond him, revise the ramp, not the
  learner"), this is a defect report against the score, and it's now fixed: **Lesson 0**
  (`LESSON-0.md`) precedes Lesson 1 — pure letter-shape recognition, the 22 names and sounds,
  the eight non-joining letters and the mid-word-gap trap, decoding drills built from
  invented/meaningless letter-strings only, no vocabulary or grammar anywhere in it. Its
  content is Nestle's own alphabet table (p.4), extracted on demand as `r1/p004-1.toml` — the
  first genuinely lesson-driven R1 pull, exactly as §7a reasoned R1 extraction should work.
  G2 now waits on one thing only: **Wilson runs Lesson 0, then Lesson 1.**
  ⛔ Found in passing, and FIXED the same session: the Lord's Prayer record had been CLOBBERED
  by a page-70 filename collision (grammar p. 70 vs chrestomathy p. 70 → both `r3/c070-1.toml`;
  the R3 shard's Genesis record silently overwrote the earlier Lord's Prayer record). ✅
  **Restored 2026-09-02 as `r3/c070g-1.toml`** ("g" = grammar pagination, collision-proof).
  Recovery was better than the Fable agent's own worry: it only had `git show 1dea774`, which
  predates the working record's later state — the FULL record, including all 36 structured
  `word_notes` and the completed BFBS `[alignment]` diff, was still in this session's own
  transcript (it had been read in full before the collision occurred) and is what got restored,
  not the bare calibration stub. Nothing about the Lord's Prayer content was actually lost.
  All stale pointers (`r2/README.md`, `GLOSSARY-SHARD.md`, `research/syriac-pilot-phase1-
  calibration.md`, `SYRIAC-LESSON-PLAN.md`) updated to `c070g-1.toml` in the same pass.

No repo decision needed yet: pilot records live under `~/paleography` beside the registry
(the twin paths share machinery); if the language side outgrows the repo, splitting is a
G2-passed problem.

## 10. Deferred — decided later, on purpose

Product surface and URL · Hebrew track (consonantal-first; hostable unpointed corpus needs
its own inventory — DSS is link-only by standing ruling) · deck export toward Tabella ·
the Syriacist expert seat (⚠ the same Ishac/Roughan email already owed for the Vienna
licence question is the natural opener — but outreach is Wilson's send, a hard stop) ·
whether primer-author philological notes become learner-facing glosses or stay quarry.

⭐ **The web build itself, ruled 2026-09-02 (Wilson), a separate future session — no code
yet, this is the score for when one starts.** After running Lessons 0–1 on paper, Wilson's
verdict on the *shape* of the eventual product, not just its content:

**Not a static single-page HTML the way UT Austin's EIEOL is.** The comparison is exact and
worth keeping: EIEOL's *Old French Online* (already linked from the site's Old French track)
is prose + a fixed exercise set on one page — read it once, the practice is exhausted.

**Instead: explanation + a procedurally-generated drill loop that builds up**, multiple-choice
as the drill mechanic, over material assembled from the primer extraction (R1–R4) rather than
hand-authored exercise-by-exercise. The governing complaint, from Wilson's own experience
learning Greek and Latin: **every primer he used gave FEWER repetitions and examples than he
personally needed**, and a fixed printed exercise set cannot fix that — you exhaust it and
you're still short. A generated drill can: **as much practice, in as many varied forms, as
the learner wants, before moving on** — the ceiling is the extracted corpus (R1 cells, R4
lemmas, R3 word occurrences), not an author's patience for writing one more example.

**Why this is a natural fit for what's already built, not a new architecture:** the pilot's
R1–R4 records are already structured data (lemma, forms, glosses, cross-references), not
prose — a multiple-choice question ("which cell is this form?" / "what does this lemma
mean?" / "which letter is this?") is a near-mechanical transform of a record, and infinite
variation comes from resampling distractors and forms rather than authoring new items by
hand. Lesson 0's decoding drills (`LESSON-0.md` Part 3) are the paper prototype of exactly
this pattern — generate a nonsense string, ask for the reading, check it — and the same
generator that wrote those by hand should eventually write them programmatically, at
whatever volume a learner asks for.

**Scope note, so this doesn't grow silently:** this is a description of what the *eventual*
web surface should feel like, not a spec — no framework, no data model, no page count decided
here. It generalizes past Syriac (Hebrew, and the self-produced-GT band) once it exists, since
the underlying move — turn structured extraction records into an unlimited drill generator —
doesn't depend on which language's primer fed it.
