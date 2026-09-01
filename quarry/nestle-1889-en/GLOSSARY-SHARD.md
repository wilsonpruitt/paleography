# Glossary shard — run it straight through

*The R4 shard of Phase 1. 51 of 63 pages done (2026-09-01), 710 records. This file is written
so the next session starts extracting inside five minutes and never re-derives anything.*

---

## Where you are, mechanically

```sh
cd ~/paleography
python3 tools/quarry_r4.py --remaining     # pages left, their leaves, and the next fetch command
python3 tools/quarry_r4.py --audit         # per-page counts, uncertainty rate, unread count
python3 tools/quarry_r4.py --unread        # the head-words that could not be read
```

**12 pages left:** pp. 184–195 (n273–n284). Everything before that is done, including p. 171,
which was in the calibration batch. `--remaining` knows. The run is now contiguous to the end.

## The loop

```sh
sh tools/quarry_fetch.sh 273 274 275 276 277 278     # six pages at a time
```

Then, per page: **read `n<leaf>_a.jpg`, read `n<leaf>_b.jpg`, emit.**

```python
import sys; sys.path.insert(0, 'tools')
from quarry_r4 import emit
emit(page=184, leaf="n273", entries=[ dict(slug=..., unvoc=..., voc=..., translit=..., pos=..., en=...), ... ])
```

`emit` validates every record as it writes it, so a TOML mistake surfaces on the spot.
Field list is in `tools/quarry_r4.py`'s docstring. Model record: `r4/g171-neshab.toml`.

⚑ **Two crops, not one whole page.** The full leaf at 1598×2604 is not reliably readable for
pointed Serto; two halves at 1.75× are. This is measured — ~6.5k vision tokens per page against
~2k for a read you cannot trust.

⚑ **A third crop, when a head-word would otherwise be lost.** `sh tools/quarry_zoom.sh <leaf>
<top> <bot>` cuts one horizontal band of the leaf at 3×, by fractions of the WHOLE page. Added
2026-09-01; used six times over pp. 150–161 and about twenty-five times over pp. 162–183, i.e.
roughly one per page. ⚑ To aim it: the `a` crop is page fractions 0.05–0.55 and `b` is 0.52–1.00,
so a line at fraction *f* of the `a` image sits at `0.05 + 0.50f` of the page (`0.52 + 0.48f` for
`b`). A 0.04–0.07 band is one to three lines. ⚑ zsh does NOT word-split an unquoted variable, so a
`for b in "0.2 0.3"; set -- $b` loop silently passes the whole string as one argument — call the
script once per band. It is what turns a ⛔ NOT READ into a record —
but it costs a third image, so spend it on head-words, not on sub-lemmas.

⚑ **Commit every 2–3 pages.** Cheap, and it keeps the diff reviewable.

## Rate, so you can tell if something is wrong

**~14 head-lemmas per page (~25.5 LEMMAS/page counting sub-lemmas), ~19–21% of records carrying
`uncertain = true`.** ⚑ Recalibrated twice. At the halfway mark the head rate held exactly
(13.6/page over 30 pages) but sub-lemmas ran well above §2's estimate. At 51 of 63 pages the head
rate is 13.9 and holding, and the SUB rate has come back down as the sections got denser in
one-line cross-references: 589 subs against 710 heads, 25.5 lemmas/page, projecting **~1,600
lemmas for the glossary entire** rather than the ~1,680 the halfway point suggested. `--audit`
prints both counts. A page coming in at 9 or at 20 is not necessarily an error — pp. 139, 142 and
172 are genuinely short (letter transitions and long entries), pp. 164 and 177 genuinely long
(runs of one-line cross-references) — but a *run* of pages off the rate means something drifted.

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
7. ⛔ **`emit` DROPPED `sub_lemmas` silently until 2026-09-01.** The ruling below converted the
   88 legacy records but never taught the writer the new shape, so p. 150 — the first page
   emitted after it — came out with 16 sub-lemmas missing and every other field intact. `emit`
   now writes them and RAISES if what it reads back does not match what it was handed. The
   lesson generalises: **a schema change has two ends**, and `--audit`'s per-page sub count is
   the thing that shows the second one.
8. ✅ **`sub_lemmas` is a STRUCTURED ARRAY on the parent** — ruled 2026-09-01. Pass a list of
   `{voc, gloss_en, gloss_de, raw}`, or a legacy `‖`-separated string, which `emit` parses on
   the way in. Convention inside the string: leading Syriac is the form, then **English first,
   German second**, split on ` | `. ⚑ Keep `raw` — the parse is a convenience, not the record.
   The 88 legacy records were converted; there are none left to convert.
9. **An entry that runs onto the next page gets FOLDED BACK when you reach that page.** Nine
   done so far (ܙܒܢ, ܚܦܛ, ܝܕ, ܝܠܕ, ܝܩܪ, ܟܪܟ, ܢܛܪ, ܥܠܐ, ܦܠܓ). This is a HAND EDIT of a written
   record, not an `emit` call — so run `--validate` after every fold. One such edit put a stray
   backslash into a TOML string; --validate caught it.
   ⛔ **But --validate does NOT catch the worse trap, and it bit once on 2026-09-01.** In TOML a
   bare key written AFTER a `[[sub_lemmas]]` table belongs to THAT TABLE, not to the record — so
   inserting `continues_from = "…"` just before `[source]` in a file that already has sub-lemmas
   silently buries it inside the last sub-lemma, and the file still parses. **Every root-level key
   you add by hand must go BEFORE the first `[[sub_lemmas]]` line.** Check with
   `python3 -c "import tomllib; print(tomllib.load(open(F,'rb')).get('continues_from'))"`, not with
   --validate. Same lesson as convention 7: a change has two ends, and the parser only sees one.
10. **The next page adjudicates the previous one.** Nestle's root order is strict, and three
   times over pp. 150–161 the following page settled a reading the current page could not:
   ܙܘܪܐ 'fist' (p. 151 cross-refers to it), ܛܡܐܘܬܐ against ܛܢܦܘܬܐ (p. 157 gives ܛܢܦ its own
   entry), and the ܚ-order anomaly on p. 152 (p. 153 shows the order holds, so the anomaly is
   ours). ⚑ Therefore: when a slot and a sense disagree, WRITE THE DOUBT DOWN and read on —
   do not zoom twice and do not guess.
11. **Capture every point faithfully.** Curriculum questions — what a learner sees first —
   leak nowhere into extraction.

## What is owed, and is NOT yours to decide

- ✅ The **`‖` ruling** — answered: structured array on the parent. Convention 7 above.
- ✅ The **`word_notes` ruling** — answered: a field on R3, not a record type R5. Done, 36
  notes read off pp. 70-72 into `r3/c070-1.toml`.
- ⬜ The **Syriacist seat**. Every Syriac string here is extractor output that nobody qualified
  has ruled on. That is the standing condition of this shard, not a reason to stop. ⚑ 710 records
  in, the cost of the empty seat is concrete and nameable: nineteen homograph pairs whose members
  are separated by a single point, and the ܦܶܣܚܳܐ/ܦܶܨܚܳܐ question (p. 180), which is not a reading
  question at all but a lexicographical one.
- ⬜ **NEW, and it is Wilson's not the Syriacist's: the duplicate glosses.** Seventeen German or
  English words are now reached from two unrelated roots with no pointer between them. Linking
  them would be a curriculum decision about what a learner should see, not an extraction one, and
  the extraction has deliberately only RECORDED them (each is flagged ⚑ in a `primer_note`).

## Patterns worth carrying forward (pp. 150-161)

None of these is a rule to apply; each is a shape to RECOGNISE, so a page is not read as though
it were the first one.

- **Gloss by cognate instead of translation.** Greek alone (ἦχος, ἅλωσις, θεοτόκος, τύραννος),
  Greek WITH ITS ARTICLE for a loan (ὁ τύπος, ἡ τάξις), Latin alone for a particle or a letter
  name (ܝܽܘܕ, ܟܺܝ), Hebrew alone (h. תולדות), and once Aramaic + Hebrew with no modern language
  at all (ܝܳܬ). Record the cognate; do not invent an English gloss and pass it off as Nestle's.
- **Preformative words filed under the root.** ܡ- (ܡܙܰܡܪܳܢܳܐ under ܙܡܪ), ܬ-/ܡܬ- (under ܚܘܝ),
  ܫ- Shaphel (ܫܰܚܠܶܦ under ܚܠܦ; ܫܰܘܙܶܒ as a HEAD-WORD in the ܝ section), ܐ- (ܐܺܝܕܳܐ, ܐܺܝܡܳܡܳܐ,
  ܐܺܝܩܳܪܳܐ all under ܝ), ܒ- (ܒܰܠܚܽܘܕ under ܝܚܕ). A head-word's first letter predicts nothing.
- **Numbered sense-splits** (ܙܩܺܝܦܳܐ, ܚܰܝܽܘܬܳܐ, ܚܶܫܽܘܟ): one word, two senses, ONE record.
- **Homographs**: eight pairs so far, every one separated by pointing alone. Two records when
  Nestle separates them; a sub-lemma when he brackets the second inside the first (ܚܶܣܕܳܐ
  'grace' inside ܚܣܳܕܳܐ 'disgrace').
- **Glosses that end in a dash** (ܛܽܘܒܰܝܗܽܘܢ 'blessed are —', ܛܥܶܢ 'see to it that —'): the word
  needs its clause, and the dash is Nestle's, not damage.
- **Nestle's own apparatus, which is never our uncertainty** (convention 6): 'deest apud PSm',
  'rarius scribitur', 'ohne Plural', 'Cum ܒ', a '?' he prints himself, back-references into his
  own grammar ('p. 32, n. 1'), and once a real bibliography (de Lagarde; Hoffmann, ZDMG 32).
- **Bracket shapes may differ.** Unattested roots come in round brackets throughout, except
  [ܝܠܠ] on p. 158, which is square. ⬜ Nobody has ruled on whether that is a distinction.

## Hand the blind control these first

Not a random sample. Two classes concentrate the damage: PARTICLE CLUSTERS, and pages where two
entries of the same skeleton stand next to each other.

- `r4/g148-ha-demonstrative.toml` — the whole demonstrative system in one entry, ten two-letter
  sub-forms. **A sixth of p. 149 is cross-references into it**, so if it is wrong, p. 149 is
  wrong with it and nothing on p. 149 would show that.
- `r4/g165-ma-interrogative.toml` and `r4/g167-man-who.toml` — the ܡܳܐ/ܡܰܢ system, the same shape
  as ܗܳܐ and the same hazard: later pages cross-refer INTO them. ܡܳܢܰܘ is entered in BOTH, with
  different senses (convention 4), and one sub-lemma of ܡܳܐ is ⛔ NOT READ.
- `r4/g183-qbal-receive.toml` — nine forms in four sub-lemmas, differing by prefix (ܠ-, ܕܠ-, ܣ-)
  and by points alone. It is also the target of the shard's longest-range cross-reference.
- `r4/g134-ahr.toml`, `g135-ayk.toml`, `g136-ela.toml`, `g137-en-if.toml` — the same shape, smaller.
- **The homograph pairs, now nineteen.** The ones that are not separable by anything a control
  could check without the plate: `g162-kap-bend` / `g162-kap-hand` (identical to the point, told
  apart only by the part of speech that follows), `g167-men-from` / `g167-men-men-particle`
  (separated by LANGUAGE — Syriac preposition against borrowed Greek μέν), `g176-al-enter` /
  the ܥܰܠ sub-lemma of `g176-ali-raise` (verb and preposition, adjacent entries, different roots).
- `g180-pesha-passover-greek` / `g180-ptsah-cheerful` — the SAME FEAST twice, ܦܶܣܚܳܐ glossed
  τὸ πάσχα and ܦܶܨܚܳܐ glossed 'Passover', in two correct alphabetical slots, never linked.

## Patterns worth carrying forward (pp. 150-183)

None of these is a rule to apply; each is a shape to RECOGNISE, so a page is not read as though
it were the first one.

- **Gloss by cognate instead of translation**, and by now in every combination: Greek alone
  (ἦχος, σκηνοποιός, μίλιον, ἅπλωμα), Greek WITH ITS ARTICLE for a loan (ὁ τύπος, ὁ νόμος,
  τὸ πάσχα, ἡ κιβωτός), a Greek INFINITIVE for a verb (ἱερατεύειν, κηρύσσειν, προσκυνεῖν), Greek
  in PARENTHESES as etymology (πεῖσαι, πάταχρα), Greek AFTER the English (πέπτω, κρόταφος), a
  Greek PHRASE for a Syriac phrase (ἀφ' ἑαυτῆς), Latin alone (palatium, piscinae, 'metropolitanus
  factus est'), Hebrew alone (כְּרוּב, עַמּוּד), Hebrew AND Greek together (מַלְאָךְ + ἄγγελος),
  and ⭐ the EQUATION — 'ܢܳܐ § 3 = h. נָא', 'ܦܘܪܛܝܢ = h. שֹׁפְטִים', the three-language chain
  'ܢܐܦܘܬ = äg. νεφώθ = gr. κροκόδειλος', and once between two LETTERS, '(ܥ = ܐ)'.
- **Glosses that are not glosses at all.** A part of speech and nothing else ('ܡܰܟܺܝܟܳܐܺܝܬ adv.',
  and twice in one line on p. 167). Arabic numerals alone ('ܡܳܐܐ 100, § 33'). A bare citation
  ('ܐܶܬܦܰܓܪܰܢ BH. Gr. 1, 48'). And the space savers: a hanging prefix ('zeugen, be-') and 'do.'
  for a repeated stem.
- **Nestle's Latin does four different jobs** and they are worth telling apart: a part-of-speech
  label ('particula negationis', 'Adj. et Subst.'), government ('cum dupp. Acc.', 'cum ܥܰܠ',
  'cum vel sine ܦܶܬܓܳܡܳܐ'), a judgment between forms ('melius', 'Rarius', 'potius pro', 'varia
  lectio'), and once a whole GRAMMATICAL RULE (ܥܬܺܝܕ: 'sequente ܠ vel ܕ futuro significando
  inservit').
- **Preformative words filed under the root**, now with every prefix: ܡ-, ܬ-/ܡܬ-, ܫ- (Shaphel,
  and at ܫܽܘܥܒܳܕܳܐ the Shaphel NOUN), ܐ-, ܒ- (ܒܶܣܬܰܪ, ܒܰܥܓܰܠ), ܠ- (ܠܦܽܘܬ). ⭐ And the shard's
  own textbook case finally appeared in the text: ܥܺܕܬܳܐ 'church' filed under ܘܥܕ, with only a
  pointer left in the ܥ section (p. 175). A head-word's first letter predicts nothing.
- **Idioms and phrases lemmatised whole**: ܢܣܰܒ ܡܶܠܟܳܐ 'take counsel', ܡܰܣܳܡ ܒܪܺܝܫܳܐ 'punishment',
  ܥܰܠ ܟܽܠ ܦܪܽܘܣ 'come what may', ܡܟܺܝܪܰܬ ܠܓܰܒܪܳܐ 'married', ܒܶܝܬ ܨܰܘܒܳܐ 'meeting-house', and an
  inflected form with its own subject, ܡܶܨܶܝܢܰܢ 'we can'.
- **Numbered sense-splits**, on the head (ܡܠܳܐ 1 fill / 2 be full) and inside a SUB-lemma
  (ܨܠܺܝܒܳܐ 1 adj. crucified / 2 subst. cross).
- **Homographs: nineteen pairs**, and the kinds are now four — by pointing alone, by part of
  speech alone, by LANGUAGE (ܡܶܢ / μέν), and by root while adjacent (ܥܰܠ verb / ܥܰܠ preposition).
  Several sit INSIDE one entry, separated by intervening sub-lemmas (ܡܰܠܟܳܐ/ܡܶܠܟܳܐ,
  ܢܽܘܗܪܳܐ/ܢܰܗܪܳܐ, ܢܶܣܝܽܘܢܳܐ/ܢܶܣܝܳܢܳܐ). Nestle never warns the reader.
- ⚑ **Duplicate glosses: SEVENTEEN and counting** — Leuchter, Haar, Schrift, dicht, Blindheit,
  Weihrauch, hemmen, weil, labour (×3), sterben, blasen, Strick, prayer, Gegner (×3), schmähen,
  Vogel. Two unrelated roots reaching the same German or English word with no pointer between
  them, sometimes one page apart. ⬜ **Whether the finished glossary should link them is a
  decision nobody has made, and it is a curriculum decision, not an extraction one.**
- **Nestle's own apparatus, which is never our uncertainty** (convention 6), and its sources:
  Payne Smith (PSm., with column numbers), Bar Hebraeus (BH. Gr., and 1, 48 cited TWICE for
  denominative verbs), Bar Ali (BA.), de Lagarde (Orientalia, Mittheilungen, Semitica), Hoffmann
  (ZDMG 32 — five times, 748/751/752/753/757, one article read end to end), an unexpanded 'K.',
  a Nestorian pointing, and 'codex meus'.
- ⭐ **Arabic appears once**, p. 177: 'ܥܶܦܺܝܦ δίπλοῦς; varia lectio ܐܰܟܺܝܦ = ضعيف de Lagarde,
  Semitica 1, 25' — four scripts on one line, and the Arabic inside an apparatus note.
- **Bracket shapes.** Round brackets hold unattested roots throughout. SQUARE brackets have now
  been seen three times and for three different kinds of content ([ܝܠܠ] a root, [ܠܒܰܪ v. ܒܰܪ] a
  cross-reference, [ܠܒܽܘܟܳܐ … confusion.?] a whole entry) — the common factor is not the content
  but Nestle's DOUBT, and the third one prints his '?' inside the bracket. ⬜ Still nobody's ruling.
- **Cross-references come in four shapes**: bare 'v. X', the bracketed '[X v. Y]', a parenthetical
  '(cf. X)', and a bare 'Cf. X' with no gloss at all.

## Do not

- ⛔ Touch `registry/`, `site/`, or anything the trainer builds from. This shard writes only
  under `quarry/nestle-1889-en/r4/`. `sh tools/acceptance.sh` must stay five-for-five PASS.
- ⛔ Deploy. Nothing here reaches the live site.
- ⛔ Push without asking.
