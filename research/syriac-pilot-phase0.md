# Syriac language pilot — Phase 0 record (inventory + licences)

*Run 2026-08-31. Protocol: `SYRIAC-LANGUAGE-PILOT.md` §3 (scan bar = vowel-point legibility,
3 full-res pages per scan via `archive.org/download/<id>/page/n<leaf>.jpg`, identity checked by
running head / title page, never by ID digits). Probe images kept only in session scratchpad —
re-fetch by leaf number below.*

## G0 verdict: PASS

Every primary title pinned with a legible scan; Nestle's scan chosen; §5 licence table filled.
No HathiTrust fallback was needed.

## Pinned scans

| Work | archive.org ID | Ed. verified | Probes (leaf = printed page) | Legibility |
|---|---|---|---|---|
| **Nestle, *Syriac Grammar*** ⭐ pilot primer | **`syriacgrammarwit00nestiala`** | English (Kennedy), 1889 — English preface confirmed at n7 (p. vi) | n40 = p. 23 (grammar, §19); n180 = chrestomathy (lines 100–115); n260 = Glossarium p. 171 | ✅ PASS all 3 — vocalized Serto points and unvocalized Estrangela seyame individually resolvable at 1598 px width |
| Nöldeke, *Compendious Syriac Grammar* (tr. Crichton 1904) | `CompendiousSyriacGrammar` | English w/ marginal § apparatus; §§ match 1904 ed. | n60 = p. 22 (§§28–30); n200 = p. 162 (§205) | ✅ PASS — bitonal Google scan but 3585×5429; every point resolvable. Arabic-page offset = 38 |
| Rödiger, *Chrestomathia Syriaca*, 2nd ed. 1868 | `chrestomathiasy00roed` | Latin preface (n8 = p. V) matches 2nd-ed. contents (Aesopic fables, Eusebius excerpts, tabulae emendatiores) | n30 = chrest. p. 102 (Narcissus epistle, BM Add. 17142); n150 = gram. tables p. 19 (fully vocalized suffix paradigms) | ✅ PASS — 2078×3060, tables carry every vowel sign distinctly |
| Robinson, *Paradigms and Exercises*, **1915 1st ed.** | `bwb_KU-996-498` | 1915 printing (BWB scan; Author's Note at n5) | n9 = contents p. viii; n60 = p. 49 (§14–15, Peal perfect) | ✅ PASS print — ⚠ this copy has a prior owner's pencil marginalia around paradigms (printed text unobscured on probe). If a specific paradigm is fouled in Phase 1, check HathiTrust for a cleaner 1915 |
| Payne Smith, *Compendious Syriac Dictionary*, 1903 | `compendioussyria00payn` | Two-column dictionary, Estrangela running heads | n100 = p. 85 (dalath); n400 = p. 385 (semkath); offset = 15, stable | ✅ PASS — 3412×4977, pristine |
| Brockelmann, *Syrische Grammatik*, **2nd ed. 1912** (PLO V) | `syrischegrammati00brocuoft` | Title page at n7: Porta Linguarum Orientalium V, Berlin 1912 | n240 = chrest. p. 71* (Life of Rabbula); n320 = Glossar p. 151* (vocalized, § cross-refs) | ✅ PASS — one tape repair crosses n240, text readable through it. Starred pagination = chrest./glossary section |

**Pagination trap, recorded:** Nestle, Rödiger and Brockelmann each restart pagination for the
chrestomathy/glossary back matter (Brockelmann stars it: `71*`). One arabic-page offset does NOT
cover a whole volume — calibrate per section in Phase 1.

**Reserve bench (pinned, no protocol run — spot-check before any use):**
Uhlemann tr. Hutchinson: `uhlemannssyriacg00uhleuoft` (1855) or `uhlemannssyriacg00uhlerich`
(1875) · Phillips *Elements*: `elementsofsyriac00phil` (1845) or `elementsofsyriac00philiala`
(1837, 1st ed.).

**Not selected:** the other 1889 Nestles (`syriacgrammarwi00nestgoog` Google copy;
`syriacgrammarwit00nest`) — iala copy checked out first, no need; Nöldeke DLI copy
(`in.ernet.dli.2015.102391`) and community `noldeke-compendious-syriac-grammar` — unprobed
spares; Brockelmann 1899 firsts (`syrischegramm00broc` etc.) — 1912 2nd ed. is the fuller text
and the probed scan passed.

## Robinson keys — ANSWERED (was the §3 ⚠)

The 1915 contents page (n9) lists 32 lessons, then Syriac–English and English–Syriac
vocabularies. **No key section exists in the 1915 edition** (keys are Coakley's in-copyright
addition). Every Robinson R2 record therefore carries `key = ""` and any supplied translation is
marked as ours, per schema.

## §5 licence table — verdicts

| Source | Licence found | Verdict |
|---|---|---|
| **Digital Syriac Corpus** (syriaccorpus.org; TEI on GitHub `srophe/syriac-corpus`) | Site + per-text TEI headers: **CC BY 4.0** on the TEI editions; Syriac base texts declared public domain. Verified in the header of `data/tei/5.xml` (Aphrahat, Dem. 5; encoder James E. Walters credited) | ✅ **SHIPPABLE with attribution.** Discipline: read the `availability` element of each text actually ingested and credit its encoder on the page at ingest |
| **SEDRA / Beth Mardutho** (lemmatized Peshitta NT) | Site: "© Beth Mardutho, All Rights Reserved." SEDRA III data terms (as carried in `peshitta/sedrajs`): personal + academic use; **no redistribution of altered files, no redistribution for profit**. No public data licence for SEDRA IV found | ⚠ **COMPUTE-ONLY** — the Ómagyar pattern: may *check* and be *counted over*, never *become* our shipped text. Derived frequency ranks are defensible for a free product but redistribution of lemma/text data is not. Confirm with Beth Mardutho before any deeper dependency; fallback (hand-lemmatize the pilot's own passages) stands |
| **Meltho fonts** (Beth Mardutho) | Freeware; licence permits **redistribution, prohibits modification** (so packaged by X.Org/FreeBSD as `font-misc-meltho`). Licence text ships in the font package (Meltho guide PDF) | ✅ **USABLE** — serve the *unmodified* TTF/OTF via @font-face. ⚠ Format conversion (WOFF2) is arguably modification — don't, without reading the packaged licence text first. Fallback: Noto Sans Syriac family (OFL) if a converted webfont is ever required |

## ⚠ Corrections to this record (later evidence)

*This file is the dated record of the Phase 0 run and its verdicts are left as they were written.
What later evidence changed is listed here.*

- **2026-09-01, the SEDRA verdict was too broad (Wilson).** "COMPUTE-ONLY" is right about the
  database and wrong about the text in it: SEDRA carries the **BFBS/UBS 1905 Peshitta NT**, which
  is **public domain**. The text is shippable; the lemmatization and morphology are not. Corrected
  in `SYRIAC-LANGUAGE-PILOT.md` §5; consequences in
  `research/syriac-pilot-phase1-calibration.md`.
- **2026-09-01, the chrestomathy layer note below is wrong for Nestle.** p. 67 opens in fully
  vocalized Serto and has ramped to unvocalized Estrangela by p. 71, inside one passage. The n180
  probe saw only the second half of that ramp. See `quarry/nestle-1889-en/MAP.md`.

## Layer observations (for Phase 1 planning — declared layer can still be wrong)

- Nestle grammar + glossary: **vocalized Serto** (West Syriac Greek-letter vowels). Nestle
  chrestomathy (probe page): **unvocalized Estrangela** with seyame. One volume, two scripts,
  two layers — declare per record, and good news for the Estrangela-leads ruling.
- Rödiger: chrestomathy largely unvocalized Serto; grammatical tables fully vocalized.
- Brockelmann: chrestomathy unvocalized; Glossar vocalized with Nöldeke-style § refs.
- Payne Smith: fully vocalized throughout, East-Syriac variants marked `E-Syr.`

## Next (Phase 1, Opus per §9)

Decompose Nestle into R1–R4. **Before dispatch: estimate the burn from measured per-plate
figures and put the "which model, and go?" hard stop to Wilson.** ~297 leaves in the pinned
scan; the extraction set is smaller (grammar ~96 pp + chrestomathy + glossary; bibliography
chapters and prefaces are named filler).
