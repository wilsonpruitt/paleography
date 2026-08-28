# Syriac — a reader's primer

*The fourth track, the first written right to left, and the first that is not an alphabet.
Written for someone who reads printed Syriac — or who reads Hebrew or Arabic and can hear
the language — and has never read it from a manuscript. Frequencies are real, counted over
**2,475 lines / 21,975 words / 7,900 distinct word-forms** of the ground truth for Vienna,
ÖNB Cod. Syr. 1 (see `corpus/sources.yml`). Nothing here is invented for illustration.*

---

## 1. The book, and why it is worth your first hour

This is a small codex — **91 × 75 mm**, the size of a hand — of the four Gospels, written
at Vienna in **1554** by **Moses of Mardin**, a priest of the Syriac Orthodox Church who
had come west from Mesopotamia, and dedicated to the Emperor Ferdinand I.

The reason to read *this* manuscript rather than any other: it is the **printer's copy**.
ÖNB's own record says so — *Vorlage für den bei Caspar Kraft und Michael Zimmermann 1555 in
Wien herausgegebenen ersten Druck in syrischer Schrift und Sprache*. The book set from
these pages, Widmanstetter's Syriac New Testament of 1555, is the first book ever printed
in Syriac. So the hand you are learning to read is the hand a compositor read, and the
letterforms of every Syriac type since descend, at one remove, from these strokes.

⚠ **The ground-truth repository dates the codex 1545.** ÖNB dates it 1554, gives Vienna as
the place, and ties it to the 1555 edition. 1545 looks like two digits changed places. We
follow the library.

## 2. What is different before anything else

**(a) It runs right to left.** Everything in this trainer that shows you Syriac —
the printed line, your input box, the character-by-character comparison — runs the other
way. Nothing about *reading* changes; a habit does.

**(b) It is an abjad: the vowels are not written.** Twenty-two letters, all consonants.
Syriac has a full apparatus of vowel points, and this manuscript **does not use it**, and
neither does the transcription. You supply the vowels from the word, which means you are
reading Syriac, not decoding it. This is the ordinary condition of the manuscript tradition,
not an austerity chosen for the exercise.

**(c) Letters join.** Most letters connect to what follows, so a word is one continuous
line with a shape of its own. Eight letters — **ܐ ܕ ܗ ܘ ܙ ܨ ܪ ܬ** — never join to the
letter after them, so they break a word into pieces. A gap inside a word is normal and is
not a word boundary. This is the single commonest early misreading.

**(d) There are no capitals, and no final forms.** Hebrew has five final letters; Syriac
has none to speak of (final semkath ܤ occurs exactly **once** in 2,475 lines). One shape per
letter, in up to four joined positions.

## 3. Serto, and the two hands you are not reading

Three Syriac scripts share these letters:

- **Estrangela**, the oldest, upright, heavy, angular — the "book" script.
- **Serto** (*serṭo*, "a line"), cursive, rounded, sloping; the West Syriac hand, and
  **this one**.
- **East Syriac** (Madnḥaya), the hand of the Church of the East.

They are the *same alphabet*. If you learn Serto here, you will read the other two with a
week of adjustment, not a new alphabet. That is why this site treats Syriac as one script
profile with a hand named per manuscript, and not as three.

⚠ **The printed line under each plate is a modern typeface** (Noto Sans Syriac Western,
a Serto face). It shows you what the words *are*, never what the strokes *look like*. Read
shapes from the ink and only from the ink.

## 4. The dots, which are the whole lesson

There are no vowels here, but there are dots, and they are not decoration. **675 of the
7,035 word-forms in this bank appear in more than one pointing** — that is, the same
consonants with the dots placed differently, meaning different things. A dot is as much a
letter as a letter is.

Four jobs, in the order you will meet them:

**(a) Seyame — two dots over a word, marking the plural.** On **1,182 of 2,475 lines**.
It sits over a letter of the word rather than at a fixed place — most often over a ܪ
(455 of the 1,870 in this bank), then ܝ (286), ܡ (185), ܢ (168).
`ܟܗ̈ܢܐ` *kāhnē*, "priests" (22×) · `ܡ̈ܝܐ` *mayyā*, "waters" (15×) · `ܟܢ̈ܫܐ` *kenšē*,
"crowds" (14×). Without it the same letters are a singular. **This is the first thing to
train your eye on**, because it changes the sense of the sentence and it is easy to miss
in a small hand.

**(b) The dot that separates homographs.** The textbook case is in front of you 445 times:

| written | dots | reads | count |
|---|---|---|---|
| `ܡ̣ܢ` | dot **below** | *men*, "from" | 179 |
| `ܡ̇ܢ` | dot **above** | *man*, "who" | 49 |
| `ܡܢ` | none | the scribe left it open | 217 |

One set of consonants, two words, told apart by one dot's position and by nothing else in
the letters. And the third row is the honest part: **half the time this scribe does not
point it at all** and the sentence has to decide. Expect that. A diplomatic transcription
records what is there, so the trainer will ask you for a bare `ܡܢ` as often as a pointed
one.

**(c) The dot that gives a verb its tense.** `ܐܡ̇ܪ` with a dot **above** is *āmar*, "he
says" — the participle — and occurs **167×**. `ܐܡ̣ܪ` with a dot **below** is *emar*, "he
said" — the perfect — **79×**. Add the conjunction and `ܘܐܡ̣ܪ` "and he said" is one of the
commonest words in a Gospel, **155×**. When you misplace this dot you change the tense of
the narrative.

**(d) The dot over the feminine.** Over a final ܗ it marks the feminine suffix — *her*,
not *his*: `ܠܗ` "to him" (232×) against `ܠܗ̇` "to her" (40×).

⭐ **349 lines in the bank carry no mark at all.** The bank is ordered easiest first, and
those are where you start.

## 5. What else is on the page

**Punctuation is the scribe's, and it is text.** `.` full stop (3,307×) · `܆` (597×) ·
`:` (239×) · `܇` (114×) · `܉` (65×) · `܀` end of section (145×). Transcribe what you see;
they are not normalised in this ground truth.

**Abbreviation is nearly absent.** One sign, `܏`, on **140 lines** — a stroke over a
suspended word, most often `ܬܠܡܝ̈ܕ܏ܘܗܝ` for *talmīdaw(hy)*, "his disciples". After the
Latin tracks, where a third of the work is expanding brevigraphs, this will feel like a
holiday. It is the honest state of a 16th-century Gospel book: this scribe wrote things
out.

**Gold.** The opening of the text is written in gold block letters. Those lines are
segmented in the ground truth as a separate zone and are **not** in this bank — a different
letterform, and a reading exercise of its own.

## 6. Typing it

You do not need a Syriac keyboard. Type romanised and the box converts as you go — one key
per consonant:

```
a ܐ   b ܒ   g ܓ   d ܕ   h ܗ   w ܘ   z ܙ   H ܚ   T ܛ   y ܝ   k ܟ
l ܠ   m ܡ   n ܢ   s ܣ   e ܥ   p ܦ   c ܨ   q ܩ   r ܪ   x ܫ   t ܬ
```

Points come **after** the letter they sit on, exactly as accents do in the Greek track:
`"` seyame · `^` dot above · `_` dot below. So `mlk"a` gives `ܡܠܟ̈ܐ`, and `am^r` gives
`ܐܡ̇ܪ`.

⛔ The mark keys are `^ _ "` and deliberately **not** `. , :` — a full stop follows a
letter 3,307 times in this text, and would have been swallowed as a dot every time.

## 7. A first line, read through

An early plate, from Matthew's genealogy:

`ܪܥܘܬ. ܥܘܒܝܕ ܐܘܠܕ ܠܐܝܫܝ. ܐܝܫܝ ܐܘܠܕ ܠܕܘܝܕ`

Right to left: *Rʿūt* (Ruth), full stop · *ʿŪbīd* (Obed) *awled* (begat) *l-Īšay* (Jesse),
full stop · *Īšay awled l-Dawīd* — Jesse begat David. Note `ܐܘܠܕ` *awled*: ܐ and ܘ and ܕ
are all non-joining, so the word arrives in pieces and is still one word. Note too that you
recognise the names before you have parsed a letter, which is the technique — **let the
word tell you what the strokes are.**

---

*Corrections are welcome and wanted; the track carries a link on every line. There is no
Syriacist on this project yet, and the expert seat for this language is empty.*
