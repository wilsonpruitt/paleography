# What the seed ground truth can and cannot teach

*Phase 2 scoping, 2026-08-27. Determined by inspecting the data, not by assumption.*

## The constraint that decides the MVP

**The seed ALTO carries exactly one `<String>` per line** — no word-level and no
glyph-level boxes. Checked in both tracks:

```
eutyches/VLO41/GT/alto/f02r.xml   line 1 -> 1 String: "INCIPIT LIBER EVTI"
cpgr23/data/CPgr23/cpgraec23_0234 line 1 -> 1 String: "ἄρτεμι· σοὶ δὲ κυνῶν …"
```

⚑ So of PLAN.md's levels, only **Level 3 (line transcription)** can be built from the
seed as it stands:

| level | exercise | buildable now? | what it would need |
|---|---|---|---|
| 0 Script | script identification | yes, trivially | more scripts in the bank |
| 1 Glyph | glyph → letter cards | ❌ | glyph boxes: forced alignment or manual annotation |
| 2 Abbreviation | sign → expansion cards | ❌❌ | word boxes **and** the expansions (23 still unratified) |
| **3 Line** | **read the line, diff** | ✅ **built** | — |
| 4 Page | layout, regions | partly | region polygons exist; needs a page-level UI |

⚑ **Level 1 is unblocked by a tool, Level 2 by a ruling.** Glyph and word boxes can be
produced by forced alignment (Kraken can align a known transcription to a line image
and emit per-character positions) — that is a Phase 2b task with a known method. Level
2 additionally needs Wilson's ratification of the expansions in
`latin-abbreviations.json`, and for Greek it needs a diplomatic witness we do not have.

## Cropping: three things learned the hard way

**1. Crop from the BASELINE, not the polygon.** Source polygons are sometimes
self-intersecting — an eScriptorium artifact. One spur turned a 46 px line into a
189 px bounding box, and the height-normalising downscale then crushed the text to
an unreadable smear. Baselines are present on every witness that has images
(wien940 has baselines for 0 of 7,889 lines, but it has no images either).

**2. Rotate first, then band.** Cropping a band around a *tilted* baseline and rotating
afterwards adds the baseline's own vertical run to the band height — that turned a
46 px line into a 133 px crop carrying its neighbours with it. Rotate about the
baseline midpoint, then take the horizontal band: same line, 77 px, clean.

**3. Line height comes from the page, not the line.** Robust estimate = median gap
between consecutive baselines on that page (46.5 px on VLO41 f02r, over 75 lines).

## Images: one witness is unusable

| witness | GT pages | page images on disk |
|---|---|---|
| cpgr23 | 70 | **70** ✅ |
| eutyches-VLO41 | 63 | **63** ✅ |
| eutyches-Lat7499 | 39 | **39** ✅ |
| rescribe | 17 | **17** ✅ |
| **wien940** | 262 | **0** ❌ |

⛔ **wien940 is our largest Latin set (7,889 lines) and has no images at all** — it is a
Transkribus TEI export of transcriptions only. It cannot produce a single exercise
until the ÖNB page images are fetched (IIIF). That is the largest single win available
in Phase 2b: it would roughly triple the Latin bank.

Coordinates were checked against image dimensions on 6 pages per witness — no overflow,
so GT coordinates and on-disk images are at the same resolution. (This is a real trap
elsewhere; it happens not to bite here.)

## The trainer

`tools/build_exercises.py` → `build/exercises.json` → `tools/make_trainer.py` →
`build/scriptorium.html`, a self-contained page (3.0 MB, images inlined as data URIs).

Design decisions that are pedagogy, not styling:

- **The Greek diff always normalises `ς` → `σ`**, in strict mode too. The witness does
  not distinguish final sigma; penalising a learner for correct modern habit would be
  teaching them the dataset's convention as if it were the manuscript's.
- **Scoring is over the alignment length, not the truth length.** Otherwise an inserted
  character is free — `uerbXum` for *uerbum* scored 100%.
- **Alignment is a Levenshtein backtrace**, so a single dropped letter shifts nothing
  downstream. A naive index-by-index compare marks the whole rest of the line wrong.
- **A character palette is provided**, because a learner cannot type `ꝓ` or `᷑` on a
  normal keyboard. The cpgr23 team built an eScriptorium virtual keyboard for exactly
  this reason; it is a real part of transcription practice, not a convenience.
- **"Ignore accents & punctuation" defaults ON** for a first sitting; strict mode counts
  every point.

⚠ **Private-use (MUFI) codepoints do not render in any web font.** The current 45-line
Latin selection happens to contain none, but any wider selection will. Either filter
them at build time or ship a MUFI font (Junicode) as a data URI.
