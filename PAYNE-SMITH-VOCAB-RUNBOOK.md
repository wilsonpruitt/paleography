# Payne Smith vocab-gap runbook — locate targets set up 2026-09-02, extraction NOT run

*Written the session after the R1 grammar pull finished. Purpose: close the vocabulary gap
found by checking `SYRIAC-LESSON-PLAN.md`'s Lessons 1–10 "New lemmas" lists against the
existing 874-record R4 glossary (`quarry/nestle-1889-en/r4/`). ⛔ That glossary is COMPLETE —
`GLOSSARY-SHARD.md` says so explicitly, "do not re-run extraction" — so this is not a Nestle
re-read. Nestle's own 63-page glossary simply doesn't define every word the lessons need,
because the lessons draw on Peshitta/Gospel passages beyond what Nestle's grammar examples
used. This runbook pulls the missing ~20 words from a second PD source instead.*

## The gap, and how it was checked (not guessed)

Checked programmatically: extracted every "New lemmas" list from `SYRIAC-LESSON-PLAN.md`
(Lessons 1–10), matched each English gloss against all 874 R4 records' `gloss_en` fields
(head + sub-lemmas) with word-boundary regex, then spot-checked apparent misses by Syriac root
(catching false misses — e.g. "morning" IS in R4, just glossed "dawn"). What's left after
discounting wording mismatches:

| word | Syriac lemma | lesson(s) |
|---|---|---|
| deep | ܬܗܘܡܐ | L1 |
| hover | ܪܚܦ | L1 (gloss-only in the lesson plan, not drilled) |
| evening | ܪܡܫܐ | L1 |
| midst | ܡܨܥܬܐ | L2 |
| gather | ܟܢܫ | L2 |
| luminary | ܢܗܝܪܐ | L3 |
| multiply | ܣܓܐ | L4 |
| sanctify | ܩܕܫ (Pael) | L5, L6 (Ethpaal) |
| forgive | ܫܒܩ | L6 |
| debt / debtor | ܚܘܒܐ / ܚܝܒܐ | L6 |
| crafty | ܥܪܝܡ | L7 |
| beast | ܚܝܘܬܐ | L7 |
| mourner | ܐܒܝܠܐ | L8 |
| meek | ܡܟܝܟܐ | L8 |
| righteousness | ܟܐܢܘܬܐ | L8 |
| persecute | ܪܕܦ | L8 |
| Cain | ܩܐܝܢ | L9 — proper noun, may not warrant a dictionary-style R4 record at all, see below |
| keeper | ܢܛܘܪܐ | L9 |
| henceforth | ܡܟܝܠ | L9 |
| city | ܡܕܝܢܬܐ | L10 |
| lampstand | ܡܢܪܬܐ | L10 |
| bushel | ܣܐܬܐ | L10 |
| reward | ܐܓܪܐ | L10 |

22 targets (21 common words + 1 proper noun). Also open, smaller: L5's ordinals (ܫܬܝܬܝܐ
sixth / ܫܒܝܥܝܐ seventh) and L6's ܐܡܝܢ "amen" and ܒܝܫܐ/ܒܝܫܬܐ "evil" (m./f. of the same
root) — not individually leaf-located below, fold into Step 1 when this runs since they're the
same kind of gap.

⭐ **Cain, and proper nouns generally:** worth a ruling before extracting — Nestle's own
glossary appears to exclude proper names (Cain doesn't turn up there either), and a
comprehensive dictionary like Payne Smith may treat ܩܐܝܢ as a bare cross-reference to
Genesis rather than a real entry. If so, this is a `word_notes` item on the R3/lesson record
that uses it, not an R4 pull. Check when Step 1 runs; don't force it into the dictionary shape
if the source doesn't either.

## Source: Payne Smith's *Compendious Syriac Dictionary* (1903), confirmed usable

- **archive.org id: `compendioussyria00payn`** — "A compendious Syriac dictionary, founded
  upon the Thesaurus Syriacus of R. Payne Smith, D.D.," 1903, Oxford. Public domain (1903,
  well past any term). Same hOCR/pageindex/searchtext tooling as the Nestle and Nöldeke scans
  already in use this pilot — `_hocr_searchtext.txt.gz` + `_hocr_pageindex.json.gz`, 710
  leaves total.
- **Pagination — leaf = printed page + 15**, confirmed at TWO independent points (leaf 40 =
  page 25, leaf 100 = page 85). Not yet checked at the volume's edges (very early/late pages);
  recheck if a target lands near the front or back matter.
- **Format**: two-column page, alphabetical by Syriac root (traditional 22-letter order),
  running heads give the first/last root on the page (same convention as Nestle's glossary and
  the strong-verb table headers already handled this pilot). English definitions in italic
  type — this is what makes English-string OCR search usable here even though the headwords
  themselves are Syriac.
- ⚠ Several duplicate scans of the same 1903 edition exist on archive.org
  (`compendioussyria0000rpay`, `compendioussyria0000jpay`, etc.) — `compendioussyria00payn`
  was the one actually calibrated; don't assume the others share its leaf offset without
  re-checking.

## What's already done (cheap, text-only — no images fetched for this)

Ran an OCR-text search for all 22 target words (English gloss, word-boundary regex) across
all 710 leaves. **21 of 22 found directly; the 22nd ("lampstand") is covered under the
period-correct term "candlestick"**, which the entry almost certainly uses instead of the
modern word. This is a strong signal Payne Smith has everything needed, but ⚠ **these are
raw text hits, not confirmed headword locations** — a word appearing on a page usually means
it's cited inside SOME entry's definition (Payne Smith's definitions are long and
cross-reference heavily), not necessarily that the page's own headword is that word. Do not
skip Step 1 below because this list already has leaf numbers on it.

## Step 1 — locate the actual headword entry (cheap, do first)

For each of the 22 targets, the SYRIAC LEMMA is already known (table above, taken directly
from `SYRIAC-LESSON-PLAN.md`, not guessed) — so locate by ALPHABETICAL ROOT POSITION, the same
way Nestle's own grammar sections were bracketed in `MAP.md`, rather than trusting the noisy
English-hit leaf list above (most hits are citations inside unrelated entries). Method:
1. Fetch the hOCR searchtext leaves at the top and bottom of a reasonable bracket for the
   target's first root letter (running heads give the letter range per page cheaply, same
   trick used for Nestle's ToC calibration).
2. Narrow to the specific page by scanning running-head root-letter combinations toward the
   target root.
3. Confirm on the actual plate before transcribing — running heads can mislead the way
   Nestle's did at n90–n91.

**Partially run, 2026-09-02.** Fetched and calibrated the scan's index files
(`compendioussyria00payn_hocr_pageindex.json.gz` + `_hocr_searchtext.txt.gz`) and confirmed
pagination independently: leaf = page + 15, checked against the printed page number visible on
the n300 plate (page 285, 300−15=285 ✓) — matches the number this runbook already stated, now
confirmed by a second method.

⚑ **Offset-scheme gotcha, worth recording for future scans using this same tooling
(Nestle/Nöldeke included, if not already known there):** the pageindex's four numbers per leaf
are `[searchtext_char_start, searchtext_char_end, hocr_html_byte_start, hocr_html_byte_end]` —
**two different files, two different scales.** The first pair indexes into the small plain-text
file (`_hocr_searchtext.txt`, ~2.6 MB here); the second pair indexes into the full markup file
(`_hocr.html`, ~60 MB here) and will look like nonsense (way past EOF) if applied to the small
file, or silently return a plausible-looking WRONG page if applied by accident within the small
file's own byte range (leaves under ~50 both "worked" by coincidence when I first mixed up the
columns — a live instance of "the search was wrong, not the absence," per
[[feedback_empty-grep-is-not-absence]]'s sibling failure mode: a wrong offset that returns real
text is worse than one that errors).

**Ran the full English-hit search across all 710 leaves** (word-boundary regex, same method as
the gap-check table above, just exhaustive instead of first-5-hits). Result confirms the
runbook's own prediction that this is a fallback, not a locator: 5 of 22 words are load-bearing
enough already (**hover**→leaf 607 only, **luminary**→362 only, **bushel**→255 only,
**sanctify**→{135, 550}, **persecute**→{600, 681}, each ≤2 distinct leaves — low ambiguity, a
plate check would likely confirm directly), but the rest degrade fast: **debt**/*evening*/
*beast*/*keeper*/*gather*/*deep* each hit 15–30 leaves, and **city** hits 103 of 710 — useless
on its own, exactly the "citation inside an unrelated entry" problem this runbook already named.

⛔ **The alphabetical-root method (Step 1's actual point) has NOT run, and here's the real
obstacle, not just "not done yet":** Payne Smith's running heads are the Syriac root itself (a
printed word, not a Roman 22-letter label — confirmed on the n300 plate: `ܟܪܝܡܘܢ` /
`ܪܝܫܐ`-shaped headers, not "K" or "R"), so narrowing by them means **reading Syriac letterforms
off running heads at scale** (sampling maybe 15–20 leaves to build a coarse letter→leaf-range
map, then reading the actual candidate leaf's headword). That's a materially different risk
class than the English-hit grep above: this project has twice burned itself on exactly this
move — [[reference_paleography-gt-ingest]]'s MUFI-codepoint lesson ("never read by eye, look
for the control table") and the Eutyches bracket misread — and Payne Smith has no chocomufin-
style control table or a second independent transcription to collate against the way the R1
Nöldeke pass did. **Flagging, not deciding:** is coarse running-head letter-spotting (cheap,
lower-stakes than transcribing a full entry) an acceptable way to narrow the search, or does
alphabetical locating wait for a real reader/Syriacist seat the same way full extraction does?
The English-hit shortlist above is usable right now for the 5 low-ambiguity words regardless of
how this is resolved.

## Step 2 — extract, after Wilson's go

Same house rules as the other runbooks this pilot: split on category not typography, fetch
full-res, never read diacritic codepoints by eye, vocalisation outranks the sense, declare the
layer even when it matches the default.

⚑ **Schema question, flagging not deciding:** these 22 records don't belong under
`quarry/nestle-1889-en/r4/` — they come from a different primer. Proposed (consistent with
this project's existing multi-primer architecture — Old French, Syriac, and eventually
Hungarian each get their own `quarry/<primer>/` tree): land them under a new
`quarry/payne-smith-1903/r4/`, `record_type = "R4"`, `source.primer = "payne-smith-1903"`,
and cross-reference back with a `fills_gap_for` field naming which Nestle-primer lesson needed
it. This is the obvious extension of the existing pattern, not a new one — flagged for
Wilson's confirmation before the first record lands, per the project's habit of ruling on
schema shape before, not after, a batch commits to it.

⛔ **Hard stop before dispatch, per the house rule on big token burns**: Step 1's actual leaf
count (should be ≤22, one per word, once located precisely — down from the ~90 raw hit-leaves
above) sets the real estimate. Rough order of magnitude at the same per-page rate the other
runbooks measured: **60–100k tokens** for ~20 targeted single-page reads. Quote the actual
count after Step 1, not this guess, before asking "which model, and go?"

## Out of scope here

The ordinals/amen/evil trio noted above (fold into Step 1's target list when this runs, don't
treat as a separate pass) · the Cain proper-noun question (resolve when the actual entry, or
its absence, is seen) · writing Lessons 2–10 as documents (downstream of this, per
`NEXT-SESSION.md`) · any further R1 work (that thread is closed for this primer).

## Appendix — full English-hit leaf lists, 2026-09-02 (all 710 leaves, word-boundary regex)

Low-ambiguity (≤2 leaves) — good plate-check candidates already: hover→[607] · luminary→[362] ·
bushel→[255] · sanctify→[135, 550] · persecute→[600, 681].

Moderate (3–9 leaves): forgive→[625, 626, 652] · mourner→[18, 34, 62, 336] ·
meek→[301, 364, 454, 686] · henceforth→[122, 259, 270, 302] ·
midst→[59, 79, 328, 329, 358, 493] · debtor→[162, 163, 174, 357, 437, 688] ·
multiply→[231, 395, 507, 594, 611, 690, 709] ·
reward→[19, 136, 150, 189, 462, 486, 498, 514, 667].

High (≥12 leaves, need the alphabetical method, not this list): righteousness (12) ·
crafty (14) · candlestick (14, stands in for "lampstand" — 0 direct hits) · debt (15) ·
evening (16) · beast (17) · keeper (18) · gather (22) · deep (30) · city (103, effectively
useless on its own).

deep and debt and evening and city need the alphabetical-root method regardless — no amount of
narrowing an English-word grep fixes a word that common. Full per-leaf lists are reproducible
from the fetch already cached: `~archive.org compendioussyria00payn` hocr pageindex + searchtext
gz files (small, ~1.2 MB total, worth re-fetching rather than storing verbatim here).
