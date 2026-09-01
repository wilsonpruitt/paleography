# Glossary shard — run it straight through

*The R4 shard of Phase 1. 18 of 63 pages done (2026-09-01), 253 records. This file is written
so the next session starts extracting inside five minutes and never re-derives anything.*

---

## Where you are, mechanically

```sh
cd ~/paleography
python3 tools/quarry_r4.py --remaining     # pages left, their leaves, and the next fetch command
python3 tools/quarry_r4.py --audit         # per-page counts, uncertainty rate, unread count
python3 tools/quarry_r4.py --unread        # the head-words that could not be read
```

**45 pages left:** pp. 150–170 (n239–n259) and pp. 172–195 (n261–n284). p. 171 is done — it was
in the calibration batch, so the run has a hole in the middle. `--remaining` knows.

## The loop

```sh
sh tools/quarry_fetch.sh 239 240 241 242 243 244     # six pages at a time
```

Then, per page: **read `n<leaf>_a.jpg`, read `n<leaf>_b.jpg`, emit.**

```python
import sys; sys.path.insert(0, 'tools')
from quarry_r4 import emit
emit(page=150, leaf="n239", entries=[ dict(slug=..., unvoc=..., voc=..., translit=..., pos=..., en=...), ... ])
```

`emit` validates every record as it writes it, so a TOML mistake surfaces on the spot.
Field list is in `tools/quarry_r4.py`'s docstring. Model record: `r4/g171-neshab.toml`.

⚑ **Two crops, not one whole page.** The full leaf at 1598×2604 is not reliably readable for
pointed Serto; two halves at 1.75× are. This is measured — ~6.5k vision tokens per page against
~2k for a read you cannot trust.

⚑ **Commit every 2–3 pages.** Cheap, and it keeps the diff reviewable.

## Rate, so you can tell if something is wrong

**~14 head-lemmas per page, ~19% of records carrying `uncertain = true`.** Both have been stable
since p. 136. A page coming in at 6 or at 25 is not necessarily an error — pp. 139 and 142 are
genuinely short (letter transitions), p. 138 genuinely long — but a *run* of pages off the rate
means something has drifted. Expect ~630 records for the shard, ~880 for the glossary entire.

## The conventions, all of them earned on the page

1. **The record is the ENTRY, not the page.** Entries cross page boundaries (ܐܚܪ starts on
   p. 134 and ends on p. 135). File under the page where the head-lemma STARTS and set
   `continues_from`.
2. **Nestle orders by ROOT, not by spelling.** ܐܽܘܪܚܳܐ sits under ܐܪܚ; ܥܺܕܬܳܐ 'church' sits
   under ܘܥܕ, in the ܘ section, not under ܥ. Do not "correct" the order, and do not expect a
   lemma to be where its first letter says.
3. **Homographs are separate records.** Nestle separates them and so do we — three distinct
   ܒܪܐ on p. 142; ܐܰܠܦܳܐ 'thousand' against ܐܶܠܦܳܐ 'ship'; ܕܶܡܳܐ 'blood' against ܕܡܳܐ 'be
   like'. Four pairs so far, every one distinguished by pointing alone.
4. **Bare `v. X` cross-references ARE records** — `pos = "cross-reference"`, `see = "v. ܐܡܪ"`.
   They are a third of some pages. And the same word can be cross-referenced twice on one page
   to two different targets (ܗܽܘ on p. 148, once to ܗܳܐ and once to § 19): record both, because
   the page prints both and the distinction is Nestle's.
5. ⛔ **A head-word you cannot read is a RECORD, not a silence.** Write it with empty
   `unvoc`/`voc` and an `uncertain_note` beginning `⛔ NOT READ`, so the page's count stays
   honest and `--unread` can find it later. Seven so far. Never invent a plausible lemma to
   fill the hole.
6. **`primer_note` is Nestle's voice; `uncertain_note` is ours.** He flags his own doubts
   ('ob zum vorhergehenden ܒܰܪ?'), prints textual conjectures ('Pro … leg. vid. …') and cites
   Lagarde and Payne Smith against his own text. None of that is our uncertainty and it must
   not be filed as if it were — the blind control would chase the wrong thing.
7. **`sub_lemmas` is a string field on the parent, not its own record.** Deliberate and
   reversible: the `‖` ruling (MAP.md flag 2) is unmade, and a superset can be split later
   where a discarded reading cannot be recovered.
8. **Capture every point faithfully.** Curriculum questions — what a learner sees first —
   leak nowhere into extraction.

## What is owed, and is NOT yours to decide

- ⬜ The **`‖` sub-lemma ruling** (own records, or a field?). Moves the R4 count by ~2×.
- ⬜ The **R5 / `word_notes`** ruling from `r3/c070-1.toml`.
- ⬜ The **Syriacist seat**. Every Syriac string here is extractor output that nobody qualified
  has ruled on. That is the standing condition of this shard, not a reason to stop.

## Hand the blind control these first

Not a random sample. The particle clusters are where the damage is concentrated:

- `r4/g148-ha-demonstrative.toml` — the whole demonstrative system in one entry, ten two-letter
  sub-forms. **A sixth of p. 149 is cross-references into it**, so if it is wrong, p. 149 is
  wrong with it and nothing on p. 149 would show that.
- `r4/g134-ahr.toml` — a dozen derived forms differing only in pointing.
- `r4/g135-ayk.toml`, `r4/g136-ela.toml`, `r4/g137-en-if.toml` — the same shape, smaller.
- The four homograph pairs (§3 above): the case the scan's resolution is least able to carry.

## Do not

- ⛔ Touch `registry/`, `site/`, or anything the trainer builds from. This shard writes only
  under `quarry/nestle-1889-en/r4/`. `sh tools/acceptance.sh` must stay five-for-five PASS.
- ⛔ Deploy. Nothing here reaches the live site.
- ⛔ Push without asking.
