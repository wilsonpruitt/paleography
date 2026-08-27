# Caroline minuscule — a reader's primer

*Track 1 of the MVP. Written for someone who reads Latin and has never read a manuscript.
Frequencies are real, counted over 12,314 lines of ground truth from five 9th-century
witnesses (see `corpus/sources.yml`). Nothing here is invented for illustration.*

---

## 1. Why this script first

Caroline minuscule (c. 780 – c. 1150) is the easiest medieval Latin bookhand and the
reason your eye already half-knows it: the humanists of the 15th century mistook it for
Roman writing, copied it, and it became the model for roman type. **You are, in a real
sense, already reading a descendant of it right now.**

What that buys the beginner: **clearly separated letters, generous word spacing,
minimal ligature, one letter per sound.** Almost everything that makes Gothic and
cursive hard is absent. What remains hard is the abbreviation system — and that is
where the actual work of this track lies.

## 2. What will actually trip you

Not the letterforms. Four things, in order of how often they bite:

**(a) `a`, and the reason you will misread it.** Caroline `a` is usually a two-storey
form close to modern printed *a*, but the **open "cc"-form `a`** (looking like two c's
side by side) is common in early and Insular-influenced hands. Beside a `u`, that gives
you `au` looking like `cui`. This is the single most common misreading for beginners.

**(b) Long `ſ`.** Word-initial and medial `s` is written tall, like an `f` without the
crossbar — or with a half-bar, which makes `ſ`/`f` genuinely ambiguous. Round `s`
appears at word-end. `ſi` next to `fi` is the classic trap. *(Rescribe's GT modernizes
this to plain `s`; Eutyches' preserves it. Same script, different transcription layer —
this is why `sources.yml` declares the layer.)*

**(c) `e` caudata — `ę`.** **2,251 occurrences in our corpus.** The little tail (ogonek)
is the medieval way of writing **ae**. `ecclesię` = *ecclesiae*. It is not a spelling
error and it is not `e`.

**(d) The abbreviations.** See §4. They are the real curriculum.

## 3. What the page looks like

Real lines from Wien ÖNB Cod. 940 (Salzburg/Saint-Amand, s. VIII ex.), an Irish
commentary on Matthew:

```
    pinguitudo · HVCVSQVE ORDO NVNC ACCEDIT ID · EST ·
    infernus ‧ et sanctis fidelibus praeparatur regnum ut est illud ‧
```

Three things to notice, all of them typical:

- **Punctuation is a dot, and its height carries meaning.** The middle dot `·` (4,865x)
  and the raised point `‧` (8,340x) mark pauses of different weight — the ancestors of
  comma and full stop. Do not read them as periods.
- **Display capitals interrupt the text.** `HVCVSQVE` is in rustic capitals for
  emphasis; scribes switch script grade mid-line. `V` is `u`.
- **No `j`, no `w`; `u` and `v` are one letter.** *uerbum*, not *verbum*.

And line-ends break words without ceremony — our corpus has **1,790 line-break
hyphens** (`¬`), often mid-syllable.

## 4. The abbreviation system — the actual work

Medieval scribes abbreviated constantly, to save parchment. The system is not random;
it has four mechanisms, and once you know them most abbreviations are readable on
sight.

### (i) Suspension by a stroke — the nasal bar

**A horizontal stroke over a vowel means a following `m` or `n` is omitted.**
This is the commonest abbreviation in Latin manuscripts and our counts show it:

| sign | count | reads as | example |
|---|---|---|---|
| `ũ` | 2,747 | *un* / *um* | `uerbũ` = uerbum |
| `ẽ` | 1,338 | *en* / *em* | `artẽ` = artem |
| `ã` | 1,059 | *an* / *am* | |
| `õ` | 640 | *on* / *om* | `nõ` = non |
| `ĩ` | 245 | *in* / *im* | `enĩ` = enim |
| bare `◌̃` | 2,825 | general abbreviation mark | |

⚠ The same stroke is also a **general** "something is missing here" mark, not only a
nasal. Context decides.

### (ii) Special letterforms with a stroke through the descender

| sign | count | reads as |
|---|---|---|
| `ꝑ` | 567 | **per** (also *par*, *por*) |
| `ꝓ` | 468 | **pro** |
| `đ` | 646 | *d*- word, usually **quod** as `qđ` |
| `ł` | 1,072 | **vel** ("or") |
| `ꝗ` | 232 | **qui / quod** |
| `ꝵ` | 63 | **-rum** (genitive plural) |

### (iii) Superscript letters

A small letter written above the line supplies what is missing — usually with an `r`
understood: `qͣ` = *qua*, `qͥ` = *qui*, `IIͦIͬI` = ordinal forms. Our corpus has
combining `a` `e` `i` `o` `u` `r` `t` above the line, 700+ occurrences together.

### (iv) Conventional signs standing for whole words

| sign | count | reads as | note |
|---|---|---|---|
| `÷` | 591 | **est** | ✅ verified from the dataset's own character table |
| `⁊` | 201 | **et** | the Tironian *et*, from ancient shorthand |
| `ꝰ` | 455 | **-us** | ✅ verified |
| `᷑` | 567 | **-ur** | ✅ verified (combining UR above) |
| `` (U+F1AC) | 424 | **-que** or **-bus** | ⚠ **context-dependent**: after `q` → *que* (`cuiusq` = cuiusque); after `b` → *bus* (`dieb` = diebus) |
| `ħ` (U+E8A3) | — | **autem** | ✅ verified from `table.csv` |

⭐ **That last row is the lesson of this whole track.** Expansion is not a character
map. The same sign means different things after different letters, and only reading
Latin tells you which. **This is exactly the fusion of vision and language prior that
paleography trains** — and the reason a learner who already knows Latin can be taught
this quickly, while a model needs the language model bolted on.

### ⚠ What is NOT yet settled

Of the 64 characters occurring ≥20 times in our Latin corpus, only **4** have an
expansion verified from a source character table. **23 more carry expansions I proposed
from standard convention — they need Wilson's ratification before they teach anyone**
(`corpus/latin-abbreviations.json`, field `expansion_proposed`). 37 have no expansion
recorded at all.

⛔ This caution is not decorative. Reading four private-use codepoints from context, I
got **three of four wrong** — the contexts were suggestive and the reasoning was sound
and it made no difference. See `corpus/INGEST-NOTES.md` §7.

## 5. Nomina sacra

Contractions of holy names, inherited from Greek practice, always with a stroke over:

`DS` = *deus* · `DNS` = *dominus* · `IHS` = *Iesus* · `XPS` = *Christus* (from Greek
ΧΡΙΣΤΟΣ — the `X` and `P` are *chi* and *rho*, not Latin x and p) · `SPS` = *spiritus* ·
`SCS` = *sanctus*.

⚠ `XPS` is the one that catches people: it is a Greek word in Latin dress.

## 6. Dating a Caroline hand — rough orientation

Not an MVP exercise (Level 5), but useful to know the axis you are on:

- **s. IX** — round, wide, well-separated, few ligatures, `a` often open. Our Wien 940
  and Eutyches witnesses sit here.
- **s. X–XI** — more compact, slight lateral compression begins.
- **s. XII** — "late Caroline": letters narrowing, feet acquiring serifs, curves
  flattening. The road to Gothic.
- Then **Gothic textualis** (s. XIII), where adjacent curves fuse ("biting"), and the
  beginner's difficulty jumps a level. That is a later track.

## 7. Practice order for this track

1. **Script ID** — tell Caroline from Gothic textualis and from Insular. (One session.)
2. **Glyph cards** — `a` open vs two-storey · `ſ` vs `f` · `r` vs `n` · `ę` vs `e`.
3. **Expand** — the four mechanisms of §4, drilled in frequency order: nasal bar first
   (it is 8,800+ occurrences), then `ꝑ`/`ꝓ`, then word-signs.
4. **Line** — Wien 940 `MainZone` only. **Filter out `MarginTextZone`** or you will be
   handed a four-word scrap of gloss (INGEST-NOTES §6).
5. **Page** — then, and only then, the glossed pages of Lat7499, where main text and
   three layers of commentary share a folio.

## Sources

All ground truth CC-BY 4.0; see `corpus/sources.yml` for shelfmarks, licences and URLs.
Frequencies computed by `tools/ingest.py` over `corpus/normalized/*.jsonl`.
Character identities from the `chocomufin` control table shipped with the Eutyches
dataset (Clérice & Pinche), which is authoritative for that corpus.
