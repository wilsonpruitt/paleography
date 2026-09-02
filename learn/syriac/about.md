# A Syriac Chrestomathy

*What it is, how it was made, and which parts of it have been checked.*

## Reading first

A chrestomathy is a graded collection of real passages for learning a language; this one is
Syriac, read first.

That last phrase is the design. A beginner's Syriac normally opens with the alphabet, spends
some weeks on the noun and some more on the verb, and reaches continuous text somewhere near
the end — by which point the reader has learned a good deal *about* Syriac and read almost
none of it. This course inverts the order. Lesson 1 is Genesis 1:1–5, in Syriac, on the first
page you turn to. Grammar arrives when the line in front of you needs it and not before, and
every lesson ends with you reading a real sentence unaided.

The trade is deliberate and worth stating plainly. Eleven lessons will not make you a
Syriacist. They are meant to leave you able to sit down with a page of the Peshitta and a
dictionary and get through it — which is the thing most people who want Syriac actually want,
and the thing a paradigm-first course reaches last.

There are eleven documents, Lesson 0 through Lesson 10. Lesson 0 is the twenty-two letters and
nothing else — no meaning at all, on purpose, because learning shapes and learning sense at
the same time is two problems, and beginners fail at the seam between them. From Lesson 1 the
text is real throughout: the first four chapters of Genesis, the Beatitudes, the Lord's Prayer,
and *you are the light of the world*, which is where the course ends.

## The twin path

There are two doors into a language, and they are not the same skill.

[paleography.app](https://paleography.app/syriac) teaches you to read the **hand** — ink on a
manuscript page, in this case a pocket Gospel book written at Vienna in 1554 by Moses of
Mardin, which is the very copy the compositors worked from when they set the first book ever
printed in Syriac the following year. That track will not teach you a word of the language.
It teaches your eye.

This site teaches the **language**, in a modern printed face where every letter is
unambiguous. It will not teach you to read a manuscript.

They are built to meet. Lesson 10 ends by handing you the same line you have just learned, as
ink, on the other track. Learn one and the other costs you a week rather than a year; learn
neither and a manuscript is a wall.

## Where the text comes from

Four public-domain books, all read from scans at the Internet Archive:

- **Eberhard Nestle, *Syriac Grammar with Bibliography, Chrestomathy and Glossary* (1889).**
  The spine of the whole thing — its grammar supplies the paradigms, its glossary the
  vocabulary, and its chrestomathy the text. The word on this site's masthead is Nestle's own:
  *Chrestomathia* stands at the head of p. 67, which is the page Lesson 1 is cut from.
- **R. Payne Smith, *A Compendious Syriac Dictionary* (1903).** Consulted where Nestle's
  glossary leaves a lesson short.
- **Theodor Nöldeke, *Compendious Syriac Grammar* (1904, Crichton's translation).** Not a
  source but a **control**: an independent printed paradigm to check ours against, cell by cell.
- **W. E. Barnes, *Pentateuchus Syriace* (BFBS, 1914).** The comparison edition for Genesis.
  Every keyed page of Genesis in this course has been diffed against it.

One finding from that reading is worth repeating here, because a reader meets it in Lesson 5
and would otherwise think the site had broken. Nestle does not print his Genesis in one script.
Caput I and Caput III are set in **vocalized Serto** — vowel points and all — and Caput II and
Caput IV in **unvocalized Estrangela**. The alternation is by chapter, and it is deliberate on
his part. This project first recorded it as a gradual drift across the pages and had to correct
itself. So Lesson 5 is the first lesson with no vowel points on the page not as a pedagogical
stunt but because that is what the book does there — and reading unpointed text, supplying the
vowels you already know, is the skill every manuscript will eventually demand of you anyway.

## How a lesson is built

Nothing in a lesson is typed from memory. Each printed page is read off a high-resolution crop
of the plate and captured as a **record** — a small structured file that says what the page
prints, where it prints it, how confident the reading is, and what it was checked against.
There are three kinds in play here:

| kind | what it holds | how many |
|---|---|---|
| **R3** | a keyed page of continuous text, with its verse numbers, marginal line numbers and layout as printed | 66 |
| **R1** | a grammatical paradigm — a verb's cells, a noun's states, the numerals | 14 |
| **R4** | a lexicon entry — lemma, part of speech, gloss | 901 |

A lesson is then built *backwards* from the records: choose the destination passage first, see
which forms and words it actually requires, and teach only those. That is why Lesson 2 covers
eight verses and Lesson 5 covers three — the count that matters is new material, not verses.

Every record is published. The footer of each lesson names the records it was built from, and
each one links to the reading itself, so a claim in a lesson can be traced to the plate it came
off in two clicks. That is the point of [the sources shelf](/sources): not decoration, but the
ability to check us.

## What has been checked, and what has not

This is the section to read first if you know Syriac, and the reason
[the next page](/for-syriacists) exists.

- **22 of the 66 keyed pages** — the Genesis 1–4 selections, Matthew 5, and the Lord's Prayer —
  are fully keyed and independently diffed against a second printed edition. Those are the
  pages the lessons are built from. The remaining 44, the *Vitae Prophetarum* and the *Historia
  inventionis*, are partially or wholly unkeyed and no lesson touches them.
- **10 of the 14 paradigm records** have been collated cell by cell against Nöldeke's own
  printed paradigms, and the collation is recorded in the record, disagreements included. Of
  the four without: two are calendar lists, for which Nöldeke has no section at all; one is the
  alphabet table; and one — the Peal perfect with object suffixes — is simply still owed.
- **Vocalisation is a plate reading at the word level, not a certified diacritic-level
  edition.** The vowel points are legible as shapes at the resolutions used and are recorded.
  The finest layer — the rukkakha and qushshaya bars, the ܗ̇ point, the linea occultans — is
  recorded where seen and is not warranted point by point.
- **Twenty-seven dictionary records carry no vowel points at all, deliberately.** Payne Smith's
  plates are pointed and the points are visible; there is no control for that typeface's
  pointing and no second reader. So the consonantal skeleton, the part of speech and the
  English gloss went in — all of them reliable — and the vocalisation stayed out rather than
  being guessed. 161 of the 874 records taken from Nestle's own glossary carry an uncertainty
  flag on their face for similar reasons.
- **No Syriacist has ruled on any of it.** The seat is open and the registry says so in the
  file: `expert = ""`. Everything here was read off the plates by one person who reads Latin
  and Greek, working with a language model, against standard reference grammar. Where a reading
  could not be resolved it is marked unresolved rather than smoothed over, on the same rule the
  hand track runs on: a confident wrong reading is worse than none.

## What this site does, and does not

It teaches reading, and only reading. It will not teach you to compose Syriac, and it does not
try to make you fluent — eleven lessons cannot. It is not a substitute for a grammar; Nöldeke
is free and is named above. It teaches West Syriac letterforms because that is what the sources
print, so East Syriac and Estrangela will each cost you a little adjustment and not a new
alphabet.

It is free, it has no account, no login and no paywall, and it never will.

---

Nestle, Payne Smith, Nöldeke and Barnes are in the public domain and were read from scans at
the [Internet Archive](https://archive.org). No licence is claimed over their text: a
transcription of a public-domain work creates no new copyright, and saying otherwise would be
a claim we have no right to make. What *is* offered under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) is this project's own work —
the lesson prose, the drills, the glosses and notes, and the encoding as a compilation. Syriac
is set in [Noto Sans Syriac](https://fonts.google.com/noto/specimen/Noto+Sans+Syriac) (SIL
Open Font License).

Made alongside [Wroot Press](https://wrootpress.com), which publishes translations from the
manuscripts these hands were written in. Corrections, and especially corrections to the Syriac,
to [wilson.pruitt@gmail.com](mailto:wilson.pruitt@gmail.com?subject=A%20Syriac%20Chrestomathy).
