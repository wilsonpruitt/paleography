# Gothic bookhand — a reader's primer

*Track 3 of the MVP, and the first vernacular one. Written for someone who has read the
Caroline tracks here, or who reads printed Old French and has never read a manuscript.
Frequencies are real, counted over **2,070 lines / 54,099 characters** of ground truth from
the five 13th–14th-century witnesses of the CIHAM-HTR* Fabliaux *corpus (see
`corpus/sources.yml`). Nothing here is invented for illustration.*

---

## 1. Why this script, and what changed

Caroline minuscule was made to be legible. Over the twelfth and thirteenth centuries it was
squeezed: parchment was expensive, universities and a growing lay readership wanted more text
per leaf, and scribes obliged by narrowing every letter, breaking curves into angles, and
abbreviating relentlessly. What came out is the **Gothic bookhand** — *textualis* — and by the
fourteenth and fifteenth centuries it hardens further into the dense black *textura* of the
printed Bibles that imitated it.

The hand in this track sits comfortably before that extreme. It is compressed and angular but
still separates most letters, which is exactly why it is the right place to meet the change.

**If you have done the Latin tracks, unlearn one habit: the gaps.** Caroline gives you white
space between letters and words, and your eye uses it without being asked. Gothic takes much
of it away.

## 2. What will actually trip you

Not the alphabet. Three things, in order of how often they bite:

**(a) Minims — far and away the worst.** A *minim* is one short vertical stroke. In this hand
**i, u, n, m** are built from identical minims, and so are parts of **r**. Five minims in a row
can be *inui*, *muu*, *nui*, *unn*… The scribe will not help you: there is no dot on the *i*
by default. You resolve it by knowing the word, which is why the language matters here more
than in the Latin tracks (§6). A worked case: `ml̾t` (36×) is *mult*, and the *ul* is two
minims and a stroke that you will misread as *ul*, *nl* or *ill* until you have met the word
a few times.

**(b) Fusion, or *biting*.** When two curved letters meet, their bowls merge and share a
single stroke — *de*, *do*, *po*, *bo*, *pp*. The pair reads as one shape. Caroline never does
this; Gothic does it constantly, and it is the main reason a word looks shorter than it is.

**(c) `u` and `v` are the same letter, and so are `i` and `j`.** The scribe writes one form.
`uꝰ` is *vous*; `ura` may be *vra*. Expect to supply the distinction yourself — modern editions
add it, the manuscript does not.

A fourth, milder: **word division is unreliable.** Short words lean on their neighbours, and a
preposition may sit tight against its noun. Trust the sense, not the gaps.

## 3. What the page looks like

The *Fabliaux* witnesses are **verse**, and the layout follows: two columns, one octosyllabic
line per ruled line, the couplets rhyming in pairs. Three consequences worth having in mind:

- **The line is a unit of sense**, not an arbitrary cut. That is a real advantage over prose.
- **Metre and rhyme are evidence.** Eight syllables, and a rhyme you already know from the line
  above, will often settle a word the ink leaves ambiguous. Using them is technique, not
  cheating.
- **Line-initial capitals often sit in their own narrow column**, set off from the verse. Do not
  read them as separate words.

Ruling is usually visible as faint lines. Rubrics and initials are in red; a `·` is the
ordinary point.

## 4. The abbreviation system — the actual work

Counted over the 2,070 lines. This is where the reading time goes.

### (i) The nasal bar — a plain horizontal or wavy stroke

A bar over a vowel stands for a **missing n or m**. Roughly 1,036 instances (569 written as
precomposed vowels, 467 as a combining mark on another letter).

| sign | count | reads as | real example |
|---|---|---|---|
| `õ` | 183 | *on* / *om* | `mõ` = mon, `sõ` = son, `nõ` = non |
| `ẽ` | 158 | *en* / *em* | `biẽ` = bien, `nẽ` = nen |
| `ĩ` | 112 | *in* | `bĩe` = bien |
| `ã` | 100 | *an* / *am* | `tãt` = tant, `grãt` = grant |
| `ũ` | 16 | *un* / *um* | |

### (ii) The one you will meet most: `q̃` = *que*

**118 times** (`q̃` 100, capital `Q̃` 18) — the single most abbreviated word in the corpus, which
figures in a language this full of subordinate clauses. Its neighbour `qͥ` (**42**, plus `qͥl`
18) is *qui* / *qu'il*: a **superscript i** after `q` gives *-ui*.

### (iii) Brevigraphs — letters carrying a stroke

| sign | count | reads as | real example |
|---|---|---|---|
| `⁊` | 380 | *et* | the Tironian note; looks like a `z` with a bar |
| `ꝑ` | 139 | *par* / *per* | bare `ꝑ` (75×) is the preposition *par*; `ꝑdu` = perdu, `ꝑole` = parole |
| `ꝰ` | 78 | *-us* / *-ous* | `uꝰ` (59×) is **vous** — by itself most of this sign's work |
| `ꝯ` | 64 | *con-* / *com-* | `ꝯme` = come, `ꝯte` = conte, `ꝯter` = conter |
| `ẜ` | 8 | *ser* | |
| `ł` | 8 | *l* with stroke | |
| `ꝓ` | 1 | *pro* | rare in the vernacular; common in Latin |

`⁊` at 380 is more frequent than every brevigraph after it combined. Learn it first.

### (iv) The vertical tilde is NOT the nasal bar — and this is the distinction to hold

The corpus distinguishes two marks that look similar and mean different things:

- **plain tilde** (U+0303) — the nasal bar of §4(i): letters *n* or *m* omitted.
- **vertical tilde** (U+033E, 246×) — a **general suspension**: something else has been left
  out, and what it is depends on the word.

The vertical-tilde words are worth memorising as shapes, because they are frequent and opaque:

| form | count | reads as |
|---|---|---|
| `ml̾t` | 36 (+ `mlt̾` 6, `Ml̾t` 4) | *mult* / *molt* — "very, much" |
| `ch̾r`, `ch̾rs` | 34 together | *chevalier*, *chevaliers* |
| `ap̾s` | 5 | *après* |

### (v) Superscript letters

A small letter written above stands for itself plus what surrounds it: superscript **i** (86),
**a** (33), **e** (5), **o** (3), **m** (2), and a dedicated **ur** mark (U+1DD1, 7).

## 5. ⚠ What is NOT yet settled

This primer has **no expert reviewer** (`registry/languages/old-french.toml`, `expert = ""`).
It was written from counted evidence plus the transcribers' own conventions, by a reader of
Latin and Greek and not of Old French. Specifically:

- The readings in §4 that are **certain** are those the corpus itself demonstrates — `ꝑdu` =
  perdu, `uꝰ` = vous, `q̃` = que, `mõ` = mon — because the same words appear elsewhere in full.
- `st̾` occurs **14×** and is deliberately **not** expanded here. I could not settle it from the
  evidence, and a confident wrong expansion is worse than an admitted gap.
- The distinction in §4(iv) is drawn from the CREMMALAB transcription convention and the
  distribution of the two marks. A medievalist should confirm it means what I have said.
- Frequencies are from five witnesses of one genre. Fabliaux are not a neutral sample of
  thirteenth-century French, and a psalter or a charter would count differently.

## 6. You may need the language, and that is new here

The Latin and Greek tracks assume you read the language and teach you only the ink. **Old
French is the first track where that assumption fails for most readers.** Minims especially
cannot be resolved without knowing what word is possible, so the ink and the language are not
cleanly separable in practice.

If you need the language, the best free course is the University of Texas Linguistics Research
Center's **Old French Online** — ten lessons built on real texts (*Roland*, *Tristan*,
*Yvain*), with grammar and glossaries:
<https://lrc.la.utexas.edu/eieol/ofrol>

## 7. Practice order for this track

1. Read §2(a) again and accept that minims are the whole difficulty.
2. Learn three signs before anything else: `⁊` = et, `q̃` = que, `ꝑ` = par. That is 637
   instances, over a third of all abbreviation in the corpus.
3. Then the nasal bar, which is one rule covering ~1,000 instances.
4. Then `uꝰ` = vous and `ꝯ` = con-, which are two words and a prefix.
5. Leave the vertical-tilde forms (§4 iv) until last. They are memorised, not derived.

## Sources

- Ground truth: **CIHAM-HTR,** *Fabliaux* (Corinne Pierreville, Ariane Pinche; funded by
  Biblissima+), CC BY 4.0 — <https://github.com/CIHAM-HTR/Fabliaux>
- Transcription convention: Ariane Pinche, *Transcription Guide for 10th to 15th Century
  Manuscripts*, CREMMALAB, 2022 (hal-03697382)
- Plates for this track: **Bern, Burgerbibliothek, Cod. 354**, e-codices, Public Domain Mark
- Language: UT Austin LRC, *Old French Online* — <https://lrc.la.utexas.edu/eieol/ofrol>
