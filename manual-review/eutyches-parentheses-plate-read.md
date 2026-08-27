# Plate read — what round brackets mean in the Eutyches ground truth

**Question:** `factum (co)nprobamus`, `(des)inentem`, `luctif(icus l)etificus` — 66 instances
across the Eutyches witnesses. The dataset does not document the convention. Two hypotheses
mattered:

- **H1** — the editors supplied letters they could not read in the ink.
- **H2** — the brackets expand an abbreviation, i.e. they *do* correspond to a sign on the page.

H2 is the one that mattered pedagogically: under H2 a learner should be hunting for a sign
in the ink; under H1 there is nothing there to find and the lines must be kept out of any
production exercise.

**Read 2026-08-27, four plates, full resolution, `tools/plate.py`.**

## Result: H1, four times out of four — and H2 refuted every time

| plate | line | what the ink shows |
|---|---|---|
| f08v `eSc_line_ea725f5a` | `item sunt a fatio luctif(icus l)etificus.` | **Purple mould stains** (foxing) sitting exactly over the bracketed stretch. Ink underneath is unreadable. |
| f06v `eSc_line_c20b52af` | `factum (co)nprobamus ;` | **Ink worn away** in a gap between *factum* and *nprobamus*; faint traces only. |
| f02r `eSc_line_af5eda9e` | `ordinatur (et di)sponit᷑` | An **interlinear gloss in a small faint hand**; the bracketed part is the least legible of it. |
| f04v `eSc_line_7d3db967` | `(s)patiũ. spatior. spatiaris.` | **The parchment is physically torn.** A large diagonal loss takes the leaf away; the opening *s* is gone with it. |

⭐ **Four distinct physical causes — staining, wear, faintness, loss — and one meaning:
letters the editor supplied because the ink cannot be read.** In **no** instance did a
bracket correspond to an abbreviation sign, which is also what the dataset's own stated
guideline implies ("abbreviations preserved" — you cannot both preserve and expand).

## ⚠ One correction to my own prior guess, worth recording

I had written that the brackets were *"mostly at line openings, lost at the page edge"*.
Both halves were wrong. **37 of 66 are mid-line**, so position was never the pattern; and
the one line-opening case I read is not at the page's trimmed edge at all — the line starts
at x=1141 of a 3406-px page, and the loss is a **tear in the middle of the leaf**.

⚑ The first crop of that plate looked like edge loss because *my own crop box* clipped it
52 px before the line. Re-cutting with 420 px of context showed the tear. **A plate that is
cut too tight can manufacture the very evidence it was meant to test** — widen before
concluding, exactly as the plate-read rule says about reading the whole line.

## What follows

- Bracketed lines are **admitted to stage 1 (read along) with a gloss explaining the
  damage**, and **withheld from stages 2–4**: a learner cannot type letters that are not
  on the page.
- The gloss for `( )` is marked **verified**, on this evidence.
