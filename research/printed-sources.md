# Printed sources — what is public domain, what is still true

*Started 2026-08-27 from Wilson's pointer to Thompson on archive.org.*

## Thompson — and there are two of him

| | *Handbook of Greek and Latin Palaeography* | *An Introduction to Greek and Latin Palaeography* |
|---|---|---|
| date | 1893, Appleton | **1912, Clarendon** |
| archive.org id | `handbookofgreeka002967mbp` (the one Wilson linked) | `introductiontogr00thomuoft` |
| leaves | 369 | **626** |
| OCR text | 0.58 MB | **1.23 MB**, and noticeably cleaner (real Greek characters survive) |

⭐ **The 1912 *Introduction* is Thompson's own expanded replacement for the 1893
*Handbook*** — same chapter architecture, roughly twice the text, far more facsimiles.
**Prefer it.** The 1893 is not wrong, it is thinner.

Both are public domain (Thompson d. 1929; both published pre-1929).

**Leaf↔page calibration for the 1893 scan: offset 20.** Leaf `n137` prints page 117
(verified by fetching the image, per `reference_archive-org-page-images`). So printed
page *P* is at `https://archive.org/download/handbookofgreeka002967mbp/page/n<P+20>.jpg`.
⚠ This scan has **no `pageNumber` data in its `scandata.xml`** — the offset had to be
established from an image, and cannot be looked up.

### What is durable in Thompson

- **The architecture of the subject.** His chapter order — materials → implements →
  book forms → abbreviation → then Greek, then Latin, each majuscule-before-minuscule —
  is still how the field is taught. Our two primers arrived at the same shape
  independently, which is mild evidence it is the right one.
- **The abbreviation chapter (VII).** Directly useful, and see below.
- **The terminology page** (1893 p. 117 = the leaf Wilson opened): majuscule vs
  minuscule, capital vs uncial, and why "uncial" is a word — Jerome's preface to Job.
  This is exactly the ground the Greek primer covers in §1.

### What is superseded

- **Dating and localisation of individual hands.** A century of work (Lowe's *Codices
  Latini Antiquiores*, Bischoff) has redrawn this.
- **The national-hands framework.** Thompson's "Lombardic / Visigothic / Merovingian"
  chapter reflects a taxonomy later scholarship complicated considerably. He half-sees
  it himself: an 1912 footnote points at Traube and W. M. Lindsay investigating "the
  systems of independent schools in Western Europe previous to the Carolingian period."
- **Papyrus chronology and the Greek cursive sequence** — rewritten by a century of finds.
- Modern replacements to reach for: **Bischoff, *Latin Palaeography*** (Cambridge 1990);
  for Greek, **Reynolds & Wilson, *Scribes and Scholars***. Neither is PD.

## ⭐⭐ Cappelli — the thing that actually unblocks Level 2

**Adriano Cappelli, *Lexicon Abbreviaturarum / Dizionario di abbreviature latine ed
italiane*.** The standard dictionary of Latin manuscript abbreviations, ~14,000 forms.
On archive.org and public domain in its early editions:

- `lexiconabbreviat00capp` — 1901, Leipzig (the German *Wörterbuch*)
- `pbc.gda.pl.Lexicon_abbreviaturarum_Cappelli_` — 1912
- `CappelliDizionarioDiAbbreviature`, `lexiconabbreviat29capp` — 1929

⚑ **This is the right source for the 23 unratified expansions in
`corpus/latin-abbreviations.json`** — far better than Thompson, who gives principles
and a few dozen examples where Cappelli gives the dictionary. ⚠ Not yet fetched or
assessed; the OCR of a sign-dictionary will be near-useless, so this will mean page
images, and probably a targeted lookup per sign rather than a bulk ingest.

## What Thompson confirmed, and one thing he added

**Confirmed, twice and independently of us:** the semicolon-shaped sign is
**context-dependent** — 1912 p. 87, *"abbreviations by suspension … such as
B-=termination bus, Q-=termination que"*; the 1893 has the same at p. 103 (`Q'=que`,
`B'=bus`). This is exactly the rule proposed in `latin-abbreviations.json` for U+F1AC
and marked as needing ratification. **It is now attested in a printed authority, though
it still wants Wilson's eye on the manuscript instances.**

Also confirmed: the nomina sacra list in the Caroline primer (`DS DNS IHS XPS SPS SCS`),
plus a distinction the primer did not have — **`DNS` for the Lord, `DMS`/`domnus` reserved
for human superiors** ("domnus abbas").

⭐⭐ **Added, and it belongs in the data model — the distinction between SUSPENSION and
CONTRACTION** (1912 ch. VII opening):

> *Abbreviation is the shortening of a word by the omission or suspension … of the end;
> contraction is the shortening of a word by omitting letters from the body and leaving
> the beginning and end. **The system of contraction is superior to that of suspension,
> in that it affords a key to the inflections.***

⚑ That last clause is a functional fact, not a taxonomy. A **contraction preserves the
ending, so the case and number survive** (`dñs` → dominus / domini is recoverable);
a **suspension destroys them**. So the `abbreviation_type` field on our Level-2 table
should carry `suspension | contraction | word-sign | superscript`, and the trainer can
tell a learner *why* one sign is decidable from the sentence and another is not.

⚠⚠ **And a warning we did not have: the same sign changes meaning across periods.**
Thompson's example — `TM` = *tamen* under the older suspension system, but *tantum*
once the contraction system takes over, the shift falling in the eighth and ninth
centuries, exactly our witnesses' date. **So an abbreviation table must be scoped by
period, not global.** Add `date_from` / `date_to` to the abbreviation rows before the
table grows.
