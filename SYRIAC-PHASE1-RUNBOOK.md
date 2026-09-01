# Phase 1 runbook — decompose Nestle into R1–R4

*Written 2026-09-01 (Fable), at the close of Phase 0. This is the execution score for the
next session. Model: **Opus** for every page that touches Syriac (per `SYRIAC-LANGUAGE-PILOT.md`
§9 and the Acta plate-read precedent); orchestration and bookkeeping can run cheaper.
⛔ **Step 1 ends in a hard stop to Wilson — no full run dispatches before his "which model,
and go?"** Read `SYRIAC-LANGUAGE-PILOT.md` §§4–5, 8 and `research/syriac-pilot-phase0.md`
before starting; this runbook implements them and does not repeat every rationale.*

## Source constants (from Phase 0 — do not re-derive)

- Scan: **`syriacgrammarwit00nestiala`** (Nestle 1889, Kennedy tr., 297 leaves).
  Page images: `https://archive.org/download/syriacgrammarwit00nestiala/page/n<LEAF>.jpg`
  (~1590×2550 px; this resolution passed the vowel-point bar — fetch full-res, no scaling).
- Known offsets: front matter roman (n7 = p. vi). Grammar arabic sequence: **leaf = page + 17**
  (n40 = p. 23). ⚠ **Pagination restarts for the back matter** — n180 is chrestomathy
  (line numbers, not page numbers visible), n260 = Glossarium p. 171. Step 0 calibrates the
  second sequence; never assume one offset spans the volume.
- Layers seen in Phase 0 (declare per record; the declared layer can still be wrong page to
  page): grammar = vocalized Serto · chrestomathy = **unvocalized Estrangela** with seyame ·
  glossary = vocalized Serto, German|English glosses.
- Reference works, already pinned: Nöldeke §§ = `CompendiousSyriacGrammar` (leaf = page + 38) ·
  Payne Smith = `compendioussyria00payn` (leaf = page + 15).

## Where records go

`quarry/nestle-1889-en/` — new directory, sibling of `registry/` (the trainer's registry is
NOT touched by this phase). One TOML file per record:

```
quarry/nestle-1889-en/
  MAP.md            # step-0 output: section → leaf ranges, offsets, extraction set
  r1/p023-1.toml    # paradigm tables      — pNNN = printed page, -N = ordinal on page
  r2/p043-2.toml    # composed exercises
  r3/c091-1.toml    # chrestomathy passages — cNNN = chrestomathy-sequence page
  r4/g171-nfs.toml  # glossary entries      — gNNN + lemma translit slug
```

Field sets are `SYRIAC-LANGUAGE-PILOT.md` §4, verbatim. Every record carries
`source = { primer = "nestle-1889-en", page = <printed>, leaf = "n<leaf>" }` and
`noldeke = ["§NN"]` (nearest § + free-text qualifier when Nestle splits/lacks — never a new
invented ID). Model examples of each record type belong in MAP.md after calibration so later
shards copy a proven shape, not the schema prose.

## Steps

### Step 0 — structure map (cheap, ~10 leaf fetches)
Fetch the contents pages + first leaf of each section. Produce `MAP.md`:
1. Section boundaries as leaf ranges: grammar / Litteratura (bibliography) / chrestomathy /
   glossary / appendicula, with the second pagination sequence's offset calibrated from two
   leaves (calibrate, don't spot-check — two agreeing pages, not one plausible one).
2. **The extraction set** (leaf list), excluding the named filler: bibliography chapters,
   prefaces, comparative-philology digressions, Hebrew/Arabic cognate apparatus. Unsure ≠
   extract-to-be-safe: flag in MAP.md and move on.
3. Expected counts to sanity-check the run against (§2 of the pilot: dozens R1, low hundreds
   R2/R4, dozens R3).

### Step 1 — calibration batch + THE HARD STOP
Decompose **8 pages**: 3 grammar (at least one paradigm table + one exercise block),
2 chrestomathy, 2 glossary, 1 flagged-ambiguous. Full rules from Step 2 apply. Then:
- Measure **tokens per page, per section type**, from this batch's actual usage.
- Compute the full-run estimate = per-section rate × MAP.md's extraction-set counts.
- ⛔ **Stop. Put to Wilson in one line: total estimated burn, the per-unit rate it came
  from (quote the measured rate, not a prior), model = Opus, "which model, and go?"**
  ([[feedback_quote-the-recalibrated-rate]] — the cheap number and the approval number are
  the same number.)

### Step 2 — the run (after the go)
Shard by section; per shard:
- **R1 (paradigms):** split on category, not typography — a footnoted weak-verb variant is
  its own table. Cells carry `gram_tags`, unvoc + voc forms, translit.
- **R2 (composed exercises):** full plate transcription. `key = ""` always for material
  keyed to Robinson later; for Nestle's own exercises, key only what the volume itself
  prints. Translations we supply are marked ours, never the primer's.
- **R3 (chrestomathy):** **identify → align → diff**, transcribe only what cannot be matched.
  Candidate digital texts: Digital Syriac Corpus (CC BY 4.0 — read each text's
  `availability` header, record encoder for attribution; TEI at GitHub
  `srophe/syriac-corpus`). SEDRA is compute-only — it may *check* a reading, its text never
  enters a record. Record per passage: canonical work ID, matched digital text + its licence
  + encoder, and the diff. **Track the running match rate — if it heads under ⅔, STOP the
  shard and report** (pilot §7 stop rule) rather than grinding OCR.
- **Universal:** fetch the leaf at full res; ⛔ never read diacritic codepoints by eye;
  declare the layer per record even when it matches the section default; vocalisation
  outranks the sense in transcription QA. Curriculum concerns (what the learner sees) leak
  nowhere into extraction — capture every point faithfully.
- Content filter: heavy plate runs can throw spurious `400 Output blocked` —
  clean re-dispatch of the page, not a material failure ([[reference_vision-plate-content-filter]]).

### Step 3 — QA + G1 gate
- **Blind control** on a sample per [[reference_arabic-control-rule]]: a fenced reader
  re-transcribes N plates without seeing the record; diffs adjudicated at the image. Remember
  the fence: the blind reader is right about what it sees, not about which convention
  licenses it.
- **Cheap ratio checks** alongside (counts by record type vs MAP.md expectations; vocalized
  vs unvocalized field fill rates per section) — the parity-style gate that catches what
  agreement between briefed agents cannot ([[feedback_two-agents-same-error-suspect-the-prompt]]).
- Report counts. **Any schema change forced by contact gets folded back into
  `SYRIAC-LANGUAGE-PILOT.md` §4 BEFORE a second primer is touched** — that is the G1 gate.

## Out of scope for Phase 1

Frequency ranks (`frequency_rank` stays empty — Phase 2) · lesson sequencing (Phase 3,
Fable) · any web surface · the other five primers (G1 must pass on Nestle first) · the
Syriacist outreach (Wilson's send, hard stop — see NEXT-SESSION.md).
