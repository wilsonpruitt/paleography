# Paleography landscape survey — August 2026

*Compiled by Sonnet research session per PLAN.md §7.4. Method: WebSearch/WebFetch across
four parallel research passes (teaching tools, HTR-United datasets, HTR tooling, IIIF
rights). Every claim below carries a URL where one was found; anything not independently
confirmed is marked UNVERIFIED rather than guessed. This survey could not browse the live
HTR-United `catalog.html` (JS-rendered) but did pull the raw YAML catalogue directly
(section B) as a partial cross-check.*

---

## A. Teaching tools for Greek/Latin paleography (human learners)

Headline finding: **no tool surveyed gives automatic character-level transcription
feedback, and none uses SRS/SM-2.** Practice tools show a static answer key; citizen-science
projects use human/algorithmic post-hoc reconciliation, not per-attempt feedback.

| Tool | URL | Maintained (2026)? | Licence | What/who | Progressive? | Auto-feedback? | Greek/Latin |
|---|---|---|---|---|---|---|---|
| DigiPal | digipal.huma-num.fr | Active, hosted by AOROC/EPHE-PSL via Huma-Num; footer copyright reads 2011–14, currency of *content* UNVERIFIED | Academic, exact terms unconfirmed | Anglo-Saxon (c.1000–1100) handwriting comparison database; scholarly reference | No | No — comparison tool only | Latin (English vernacular script) |
| Archetype (DigiPal framework) | kdl.kcl.ac.uk/projects/archetype, github.com/kcl-ddh/digipal | **Explicitly legacy/unmaintained** per KDL's own page | Open source (framework) | Generic framework used by ~20 scholarly projects (Latin, Greek, Hebrew, cuneiform, Japanese, Mayan) | N/A | No | Framework-agnostic |
| Ancient Lives (Zooniverse) | ancientlives.org | **Not currently active** — site states it is "being rebuilt," no return date given | Zooniverse citizen-science terms | Crowdsourced transcription of Oxyrhynchus Greek papyri fragments | No | No — expert/community review, not per-attempt | Greek (papyri) |
| Other Zooniverse (Deciphering Secrets, Scribes of the Cairo Genizah, blicksam sandbox) | zooniverse.org | Mixed; some active 2025 | Zooniverse terms | Citizen-science transcription, some with built-in tutorials before real docs | Some ("Deciphering Secrets" teaches paleography first) | No | Mostly not Greek/Latin classical (Spanish, Hebrew) |
| Enigma | enigma.huma-num.fr | Live; built by Marjorie Burghart; recent-update evidence UNVERIFIED | Free academic | Wildcard/database lookup (400k+ Latin forms) to decode illegible words — a solver, not a course | No | No | Latin only |
| Album interactif de paléographie médiévale (IRHT/CIHAM) | paleographie.huma-num.fr | Site live; content dates to 2011 (Burghart, CIHAM), currency past that UNVERIFIED | Academic (French) | Leveled transcription exercises, word-by-word entry, answer key | **Yes**, leveled | No — answer key, not graded | Latin |
| Utrecht "Medieval Paleography" | via uu.nl MA program listing | Taught university module; no public standalone site found | N/A | Seminar module | Yes (course), implicit | No (human-graded) | Latin |
| English Handwriting 1500–1700 (EHOC), Cambridge | english.cam.ac.uk/ceres/ehoc | Live; content appears static, last-update date UNVERIFIED | Academic/free | Self-guided course: manual, alphabets, sample transcriptions | Yes, structured | No — sample transcriptions for manual comparison | English secretary/italic hands, not classical Greek/Latin |
| Vatican Greek Palaeography essay (Timothy Janz) | via BAV; exact URL UNVERIFIED | UNVERIFIED currency | Academic | Reference essay on Greek paleography practice | No | No | Greek |
| Ca' Foscari (Venice) Greek Palaeography course | unive.it (course FT0151) | Active, taught course | N/A | University course with practical transcription | Yes (course) | Human-graded | Greek |
| CEU Summer University — Latin & Greek Codicology and Palaeography | summeruniversity.ceu.edu | Active, 2025 listing confirmed | Paid course | In-person/Zoom intensive, beginner/advanced tracks | Yes, leveled | Human-graded | **Both** Greek and Latin |
| PapPal | pappal.info | Live (U. Heidelberg SFB 933); major content evidence ~2013-era, recent updates UNVERIFIED | Academic/free | 2,500+ dated Greek documentary papyri images for stylistic comparison/dating | No | No | Greek (papyri) |
| T-PEN "Italian Paleography" (Newberry/Mellon) | italian.newberry.t-pen.org | Active, Mellon-funded | Academic/free | Digitized MSS + T-PEN transcription tool + handbook, Italian vernacular hands 1100s–1700s | Some (by source difficulty) | Lets you transcribe against image but does not auto-grade (UNVERIFIED if any scoring exists) | Latin-alphabet Italian, not classical |
| Spanish Paleography Digital Teaching Tool (CUNY DSI) | spanishpaleographytool.org | Built 2011–13 (NEH grant); currency UNVERIFIED, site resolves | Academic/free | Digitized Spanish MSS, transcriptions, sample alphabets | Somewhat (by hand style) | No | Spanish, not Greek/Latin |
| **LearnLatin.io "Medieval Manuscripts" course** | learnlatin.io/courses/medieval-manuscripts | **2025–2026 newcomer** — page updated Feb 8 2026, copyright 2025 | Commercial ($34.95/mo or $349.95 lifetime) | 12-session course reading real MS pages, Roman bookhand → Carolingian → Gothic → Humanistic | **Yes, explicitly progressive** | No — provides transcriptions/abbreviation charts as aids, not graded | Latin only |
| DecipherInk | apps.apple.com (iOS/Android), decipherink.net | Active mobile app, presented RootsTech 2025 | Commercial/freemium | Genealogy-focused old-handwriting app, short lessons, markets "progress feedback" | Yes, structured lessons | **Possibly closest match** — claims "progress feedback" but mechanism/scope UNVERIFIED, and it targets genealogical English/European records, not Greek/classical Latin | Not Greek/classical Latin |

**Verdict for A:** the field is (a) static reference/comparison databases (DigiPal, PapPal,
Vatican essay), (b) answer-key practice sites (Album interactif, EHOC, T-PEN), (c)
citizen-science crowdsourcing without per-attempt feedback (Zooniverse), (d) paid
synchronous courses (CEU, Ca' Foscari, LearnLatin.io). CEU is the only program spanning
both Greek and Latin, and it is an in-person/Zoom intensive, not a self-serve app.

---

## B. Open ground-truth datasets (Latin + Greek HTR)

Two sources cross-checked: search-based survey of HTR-United ecosystem + a direct pull of
the raw HTR-United YAML catalogue (`raw.githubusercontent.com/HTR-United/htr-united/master/htr-united.yml`).

**From the raw HTR-United catalogue (Latin/Greek entries, confirmed directly):**

| Dataset | Language(s) | Licence | Size |
|---|---|---|---|
| TranscriboQuest 2024 Medieval Literary | Latin, Middle Dutch, Old French, Middle High German | CC BY 4.0 | 808 lines |
| old-ancient-greek-print-dataset | Ancient Greek, Latin | CC BY 4.0 | 2,113 lines / 69,351 chars / 37 files |
| ÖNB Cod. 3891 Ground Truth | Latin | CC BY 4.0 | 952 lines |
| AMSMB HTR | Latin, Catalan | CC BY-SA 4.0 | 3,369 lines / 100 files |
| Incunabula Reichenau | Latin, German | CC BY-SA 4.0 | 2,200 pages |
| GT4HistCommentLayout | English, German, Latin, Ancient Greek | CC BY 4.0 | 371 files / 2,386 regions |
| iForal-Dataset | Latin, Portuguese | CC BY 4.0 | 8,009 lines / 776,873 chars |
| Liber | Old French, Latin | CC BY 4.0 | 3,789 lines |
| TranscriboQuest 2025 Medieval Vernacular Religious Texts | Old French, Middle French, Old Irish, Latin, Old Castilian, Swedish, Early New High German | CC BY 4.0 | 59,696 lines |

**From search (GitHub/Zenodo/HuggingFace, not all independently confirmed via the raw
catalogue — cross-check before ingest):**

| Dataset | Script/language | Licence | Size | URL | Date |
|---|---|---|---|---|---|
| CREMMA Medii Aevi (CREMMA-Medieval-LAT) | Medieval Latin (Praegothica/Textualis/Cursiva/Humanistica), 12th–16th c. | UNVERIFIED (CREMMA generally CC BY) | 7,274 lines, 21 MSS | github.com/HTR-United/CREMMA-Medieval-LAT; zenodo.org/records/7229929 | Zenodo record 2022 |
| CATMuS Medieval | Multilingual Latin-script (mostly Old/Middle French, plus Latin, Spanish, Italian), 8th–16th c. | CC BY 4.0 | ~160,000 lines, 200+ MSS/incunabula | zenodo.org/records/12743230; huggingface.co/datasets/CATMuS/medieval | v1.6.0, Feb 2024 / Zenodo July 2024 |
| CATMuS Modern and Contemporary (McCATMuS) | Latin script, modern/contemporary | UNVERIFIED | UNVERIFIED | zenodo.org/records/18926781 | UNVERIFIED, likely 2025–26 |
| TRIDIS | Latin, Old French, Old Spanish documentary hands, 11th–16th c. | UNVERIFIED | ~4,000 pages | huggingface.co/datasets/magistermilitum/Tridis; zenodo.org/records/10788591; arXiv:2503.22714 | Preprint March 2025 |
| HTR Winter School 2025 — Late Medieval Latin | Latin, Central European charters/chronicles, 13th–15th c. | CC BY 4.0 (transcriptions) | ~207.6 MB, 5 MSS / 8 folders | zenodo.org/records/17911438 | Dec 12, 2025 |
| Codex Palatinus graecus 23 HTR ground truth (+ Paris. suppl. gr. 384) | Byzantine Greek minuscule, 10th c. | UNVERIFIED | pp. 1–614 + 615–709 | gitlab.huma-num.fr/ecrinum/anthologia/htr_cpgr23/; zenodo.org/records/10932742 | Models 2024; case study 2025 |
| Byzantine Greek case studies (Chrysostom / Planudes / Cyril of Alexandria) | Byzantine Greek | UNVERIFIED | "sample available," gradually updated | doi.org/10.5281/zenodo.8102662 | 2023 onward |
| ICDAR2023 Greek Letters on Papyri (Homer's Iliad) | Ancient Greek papyri, 3rd c. BCE–7th c. CE | **CC BY-NC 4.0** | 185 images / 136 MSS (150 train + 34 test) | zenodo.org/records/13825619 | Zenodo Sept 2024 |
| GRK-Papyri | Ancient Greek papyri (writer ID, not full transcription GT) | Free, non-commercial research | 50 images, 6th c. AD | d-scribes.philhist.unibas.ch/en/gkr-papyri/ | 2019 |
| PapyRow (extends GRK-Papyri) | Ancient Greek papyri, row-segmented | UNVERIFIED | 6,498 row images + XML GT | Springer 10.1007/978-3-030-68787-8_16 | 2021 |
| HTR-School-Vienna 2023 — Byzantine Greek | Byzantine Greek | UNVERIFIED | small workshop corpus | github.com/HTR-School-Vienna/2023--byzantine-greek | 2023 |

Not confirmed to exist: a "CREMMA Papyrus" Greek counterpart to CREMMA Medieval, or
dedicated "GRK-OCR"/"Alpheios"/"Rosetta Papyrology" GT datasets — none found under those
names; treat as not present.

**2025–2026 additions specifically:** TRIDIS (arXiv March 2025), the Vienna HTR Winter
School 2025 late-medieval Latin set (Zenodo Dec 2025), TranscriboQuest 2025 (in the raw
catalogue), and the "Harmonizing Guidelines for HTR of Ancient Greek" workshop
(dhtr25.anthologiagraeca.org, 2025), which consolidated pointers to existing Byzantine
Greek/papyri case studies rather than releasing one new unified Greek GT set.

**Implication:** Latin-script medieval GT is comparatively rich (CREMMA, CATMuS,
TRIDIS, HTR-United's own catalogue) but scattered across licences (CC BY, CC BY-SA,
some UNVERIFIED); Greek GT is thin, small, and Byzantine-minuscule/papyri-specific —
confirms PLAN.md's assumption that Greek minuscule is the harder seed to find, not just
the harder script.

---

## C. HTR tooling state (Aug 2026)

**Kraken / eScriptorium.** Kraken latest release **7.1** (Aug 5, 2026), adding a
PP-OCRv6-based recognition architecture with pretrained multilingual base models
(github.com/mittagessen/kraken/releases). eScriptorium reached **v1.0.0** (Jan 30,
2026) — its first stable release, new UI, Kraken 6 support (gitlab.com/scripta/escriptorium).
Public Greek model: **HTR Model for Palatinus graecus 23** (Byzantine minuscule, Palatine
Anthology) on Zenodo (zenodo.org/records/10932742); a related Chrysostom-text model
reportedly reaches **3.90% CER** (found via search snippet only — UNVERIFIED against
primary model card). Public Latin/multi-script model: **TRIDIS** (11th–16th c.
Latin/Old French/Old Spanish, huggingface.co/magistermilitum/tridis_HTR and v2), reported
**CER ~6–12% (v1)**, **~5–10% (v2)** on unseen external test sets (WER 13–26%). **CATMuS
Medieval** also ships as a Kraken model family (CER not independently verified).

**Transkribus.** 300+ public models claimed, including Latin (Caroline minuscule, Gothic
textura, humanist) — see transkribus.org/languages/latin and the **DiploLatina** model
(trained on 76k+ lines / 871k words GT; numeric CER UNVERIFIED). Greek public models:
**Greek_Ancient-Majuscule (spaced)**, **Greek_Medieval-and-Modern-Minuscule** (10th–19th
c., **2.4% CER** on validation), and a **19th-century Greek 8.0** model (**0.93% CER**
on validation) — note these are validation-set, not generalization, figures
(app.transkribus.org/models/public/text/…). Pricing/licensing shifted in 2026 to a
**credits-based subscription**: Free (~50 credits/mo), Scholar €8.25/mo (€99/yr), Team
€33.25/mo (€399/yr, 5 users), plus non-expiring credit packs (transkribus.org/pricing).

**Tesseract.** Latest stable **5.5.1** (May 2025). Has Greek/Latin language packs but is
explicitly **not viable for handwritten manuscript HTR** — it is a printed-OCR engine;
literature describes Latin-trained Tesseract on historical handwritten material as
"unacceptably low" accuracy (en.wikipedia.org/wiki/Tesseract_(software); discussion in
arxiv.org/pdf/2506.19208). Confirmed scholarly consensus, not a live competitor here.

**VLM-based manuscript transcription (2025–2026).** Mixed picture, not a clean win:
- **CHURRO** (EMNLP 2025, arXiv:2509.19768): open-weight 3B historical-VLM beats Gemini
  2.5 Pro by 1.4% (printed) / 6.5% (handwritten) normalized similarity across 46 language
  clusters incl. Greek/Latin, at 15.5x lower cost.
- **"Reading or Guessing?"** (arXiv:2605.27750, 2026): VLMs on ancient Greek editions
  produce fluent but visually **ungrounded** text — they hallucinate plausible Greek
  rather than faithfully reading the image; traditional OCR stays more faithful (if
  noisier) under perturbation.
- Medieval English legal-document project (arXiv:2605.00977, Dec 2025): GPT-5.1 still
  fails; Gemini Pro 3 performs well but inconsistently case-to-case.
- General (non-historical) handwriting benchmarks in 2026 show frontier VLMs at ~1.2–1.4%
  CER on *modern* handwriting — not transferable evidence for medieval/ancient hands.

**Net finding for C:** VLMs are competitive or superior on some historical-document
benchmarks (CHURRO) but show a documented **hallucination/visual-grounding failure mode
specifically on ancient Greek** — the field does not yet support "VLMs beat specialist
HTR for Greek/Latin manuscripts" as a settled claim; it is genuinely contested and
task-dependent as of Aug 2026.

**Script-specificity finding.** Evidence is mixed, no clean verdict either way:
generalist models reportedly do better out-of-box on Latin-script documents, while
specialist fine-tuned models win on non-Latin scripts (PMC12202554); fine-tuning
generalist models on ~10 GT pages can reach 6–10% CER but doesn't reliably generalize
across hands (must repeat per corpus); broader-trained models (TRIDIS-style) generalize
better to *unseen* manuscripts, while narrow fine-tunes win on manuscripts *already seen*
in training (arXiv:2201.07661). No ICDAR-competition citation was found specifically
comparing Latin/Greek script-specific vs. multi-script HTR head-to-head — **UNVERIFIED**
as a clean generalization for PLAN.md's assumption; treat "script-specific beats
generalist" as directionally plausible but not proven by a specific benchmark.

---

## D. IIIF image rights (crop-and-serve assessment, Aug 2026)

| Repository | Licence/terms (source) | Verdict |
|---|---|---|
| e-codices | Per-manuscript: some Public Domain Mark (commercial OK), most CC BY-NC; commercial reuse needs owning library's written permission (e-codices.ch/en/about/terms) | Borderline — check per item |
| Digital Bodleian | CC BY-NC 4.0 downloads; "cannot be used for commercial purposes"; some college holdings excluded entirely (digital.bodleian.ox.ac.uk/terms) | Non-commercial only |
| Beinecke (Yale) | No blanket licence; library "cannot grant or deny permission," user clears rights themselves; attribution required (beinecke.library.yale.edu/permissions-copyright) | Case-by-case, UNVERIFIED at repo level |
| Walters Art Museum / Digital Walters | **CC0 1.0** for PD-believed manuscript images, no evidence of 2024–26 rollback (thewalters.org/about/policies/rights-reproductions) | **Open** |
| BnF Gallica | Free non-commercial reuse with attribution; commercial reuse is paid/licensed (gallica.bnf.fr/…conditions-dutilisation; bnf.fr/…utilisation-commerciale) | Non-commercial only |
| DigiVatLib | "Free use only for personal use or study"; any publication/reproduction needs Vatican Library authorization (digi.vatlib.it) | **Restrictive** — prohibited without written authorization |
| BSB Munich (MDZ) | Google-partnership scans marked "No copyright – non-commercial use only"; full-rights use requires a fresh commissioned digitization (bsb-muenchen.de/handschriftenzentrum/digitales-angebot; digitale-sammlungen.de/de/faq) | Non-commercial only (standard scans) |
| British Library | Historically CC0/PDM pre-2023; **Oct 2023 Rhysida ransomware attack took Digitised Manuscripts + IIIF offline entirely**; per Nov 2025 status update, ~3,000+ manuscripts are back but **catalogue/metadata is still absent** and recovery is ongoing into 2026 (bl.uk/stories/news/restoring-our-services-november-2025-update; bl.uk/about/cyber-attack) | UNVERIFIED current licence wording; practically restricted/reduced coverage right now |
| Parker Library on the Web (Stanford/CCCC) | Manifest-level: CC BY-NC 4.0 per IIIF metadata; primary terms page not independently fetchable this session | Non-commercial only (per manifest), UNVERIFIED against primary page |
| Cambridge Digital Library (CUDL) | No blanket licence — per item, some "all rights reserved" (zoom-only), others CC BY-NC; direct terms page blocked to fetch | Case-by-case, UNVERIFIED |

**Bottom line for D:** none of the ten sources grant a repository-wide right to crop and
re-host images in a **paid** exercise bank. Only CC0/PD-marked items (Walters entirely;
some e-codices items) are clear for any use including commercial. CC BY-NC items
(Bodleian, most e-codices, Gallica non-commercial tier, Parker/CUDL manifests) work for a
**free, unmonetized** exercise bank with attribution — which matches PLAN.md's low-price/free
strategy for the learner product, but forecloses ever monetizing the exercise bank itself
around these images without renegotiating licences. DigiVatLib is flatly prohibited without
written Vatican Library permission — deep-link only, as PLAN.md already assumed. British
Library content is currently too incomplete post-attack to rely on for MVP sourcing.

---

## E. Gap verdict

**Nobody occupies the square "progressive curriculum + automatic per-attempt feedback +
Greek AND Latin together + for learners who already know the language."**

Evidence against each near-miss, cited:
- **CEU Summer University** (summeruniversity.ceu.edu) is the only program spanning both
  Greek and Latin with a progressive structure — but it is a paid in-person/Zoom
  intensive with human grading, not a self-serve tool with automatic feedback.
- **LearnLatin.io's Medieval Manuscripts course** (learnlatin.io/courses/medieval-manuscripts,
  live Feb 2026) is the clearest 2025–2026 commercial newcomer and is genuinely
  progressive (Roman bookhand → Carolingian → Gothic → Humanistic) — but it is Latin
  only, and gives no automatic grading, only reference transcriptions/abbreviation
  charts as aids.
- **Album interactif de paléographie médiévale** (paleographie.huma-num.fr) is
  progressive and Latin-only, answer-key not auto-graded, and its content dates to 2011
  with no confirmed refresh since.
- **DecipherInk** (decipherink.net, RootsTech 2025) is the one product in this whole
  survey that markets "progress feedback" in adjacent territory — but it targets
  genealogical/vernacular old-handwriting reading, not classical Greek or Latin
  manuscript paleography, and its actual feedback mechanism is unverified from the app
  store listing alone.
- No tool anywhere in section A uses SRS/SM-2, and none gives character-level diff
  feedback on a transcription attempt — this was searched for directly ("spaced
  repetition paleography," "character-level automatic feedback transcription") and
  turned up nothing closing that loop.
- The Zooniverse pattern (Ancient Lives and peers) gets closest to PLAN.md's
  "contribution mode" idea (double-keying/expert queue) but has no certification gate
  and no per-attempt feedback loop for the contributor — it is closer to PLAN.md's
  Phase 3 than to its Phase 2.

This is a genuine open square, not a modest whitespace claim: every adjacent, credible
project either covers one script only, gives no automated feedback, or is a
synchronous/human-graded course rather than a self-serve app. PLAN.md's MVP design
(Level 0–3 exercises, diff against expanded/normalised text, SM-2 glyph cards, both
Caroline and Greek minuscule tracks) would be, on this evidence, the first tool to
combine those four properties.

---

## Implications for PLAN.md

1. The gap PLAN.md is betting on (§3, "learner product") is confirmed open as of Aug
   2026 — no repositioning needed, proceed as planned.
2. Greek ground-truth is thin (section B) — Phase 1's "ingest 2–3 HTR-United Latin +
   Greek datasets" should budget more manual curation time for Greek than Latin; the
   Palatinus graecus 23 GT + models are the strongest single Greek seed found.
3. Latin ground-truth (CREMMA, CATMuS, TRIDIS) is licence-mixed (CC BY, CC BY-SA,
   several UNVERIFIED) — confirm each dataset's exact licence before ingest, per
   PLAN.md's "read the rights statement before a single image enters the bank" rule.
4. The IIIF rights survey (section D) hardens PLAN.md's free-not-paid stance: almost
   every usable repository is CC BY-NC, which is compatible with a free exercise bank
   but would break under any future paywall on the bank itself — worth stating
   explicitly as a constraint on Phase 3/4 monetization, not just Phase 2.
5. Walters (CC0) is the one repository confirmed fully open for any use — prioritize it
   for early rights-clear witnesses alongside e-codices' PD-marked items.
6. DigiVatLib remains flatly restrictive; British Library is currently degraded
   post-attack (images without metadata) — do not plan on either as a near-term image
   source, matching PLAN.md's existing caution.
7. Kraken 7.1 / eScriptorium 1.0.0 (both shipped in 2026) confirm PLAN.md's "baseline is
   Kraken/eScriptorium, not from scratch" call is still current and now has a first
   stable eScriptorium release to build against, when Phase 4 starts.
8. The "script-specific beats generalist" claim in PLAN.md §4 is directionally
   supported but not proven by any single head-to-head benchmark found — keep it as a
   working hypothesis to test with our own CER-per-script eval, not a cited fact.
9. VLM transcription is not a shortcut around building the HTR pipeline for Greek
   specifically — documented hallucination/ungrounded-text failures on ancient Greek
   (arXiv:2605.27750) mean the "VLM route" in PLAN.md §4 should stay a Phase 4 option to
   evaluate, not an assumption that it already works.
10. No competitor is dogfooding the way PLAN.md's Ruling 5 proposes (learner #1 = the
    plan's author). That is itself a small piece of evidence that the market has not
    found this loop yet — worth keeping in mind as the differentiator to protect, not
    just a nice-to-have.
