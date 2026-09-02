# Syriac web build — the score for syriac.paleography.app

*Wroot Labs · Fable scoping session 2026-09-02 · status: PLAN, nothing built. Execution is
Sonnet/Opus work per §8. Companion to `SYRIAC-LANGUAGE-PILOT.md` (the language pilot, whose §10
deliberately deferred this) and `SYRIAC-LESSON-PLAN.md` (the ten lessons). Read those first if
you don't know why there are eleven `LESSON-*.md` files at the repo root.*

**Where the needle is.** The pilot cleared its own gates: G2 passed on Lessons 0–1 (run on paper
and in the "First Light" prototype), and Lessons 2–10 are written (commit `42c6e14`). What exists
is a *course on paper* plus a *throwaway drill engine for two of its eleven lessons*. What Wilson
wants is one public address where the whole course is legible, usable, and shareable — good
enough to be the artifact the held Syriacist outreach is waiting on (NEXT-SESSION.md "Owed by
Wilson" item 2: *don't send until there's a live, public artifact demonstrating the pipeline*).

**What this is NOT.** Not the procedurally-generated drill engine over R1–R4 at scale
(pilot §10, first idea) — that remains deferred; this build must not preclude it, but does not
attempt it. Not the spaced-repetition vocab/parsing engine (`paleography.md`, 2026-09-02) — same.
Not the stroke-order animation engine. Not Hebrew. Not a redesign of the hand-trainer. **v1 is
the book and the drill, generated from one source, on one subdomain.**

---

## 1. The shape — three surfaces, one source

Three audiences arrive at the same address, and they want different things:

| audience | wants | surface |
|---|---|---|
| **learner** (Wilson is #1) | read a lesson, practise it until it sticks, move on | `/N` — the lesson page: prose + drill |
| **scholar** (a Syriacist deciding whether to answer an email) | *what is this, where did the text come from, what do you need from me* | `/about` · `/sources` · `/for-syriacists` |
| **everyone else** (a colleague, a curious reader) | one paragraph and a door | `/` |

Each surface is generated from material that already exists, so the build is a renderer plus a
thin data layer, not authoring:

```
learn/                          ← the language side (twin of site/ + registry/)
  syriac/
    LESSON-0.md … LESSON-10.md  ← moved here from the repo root (§5, one git mv)
    drill/L00.toml … L10.toml   ← per-lesson drill SIDECARS, extracted from the .md (§3)
    course.toml                 ← the course record: name, lesson list, sources, seats (§2)
  shell/
    lesson_shell.html           ← page chrome; the .md renders into it
    drill_shell.html            ← First Light's engine, de-Artifact-ed and made data-driven (§3)
  tools/make_learn.py           ← .md + .toml → learn/site/;  --check catches drift
  site/                         ← GENERATED, gitignored like site/read/; the DEPLOY ROOT
    index.html  about/  sources/  for-syriacists/  lesson/N/  drill/LNN.json  fonts/
    vercel.json
```

**Why a parallel tree and not more of `site/`:** the hand-trainer's `site/` is registry-driven
(`tools/make_routes.py --check`) and byte-identity-gated (`tools/acceptance.sh`); bolting eleven
lesson pages and a second engine onto it would put the language side inside the hand side's
acceptance gate for no benefit. The two paths *share machinery* (the md renderer, the registry's
Syriac profile, the fonts) but *deploy separately*. Cross-links do the twin-path work.

---

## 2. URL convention — ruling wanted

**Proposed standing convention, for every language track from here on:**

- **`<lang>.paleography.app`** = *learn the language* (this build).
- **`paleography.app/<lang>`** = *read the hand* (the live trainer, unchanged).

So `syriac.paleography.app` and `paleography.app/syriac` are the two doors of one language, and
Lesson 10's Stage-4 handoff (§6 of the pilot: "the same line as ink") is a link from the one to
the other. Hebrew inherits `hebrew.paleography.app` the day it exists. Wilson said "for now" —
the convention is proposed so "for now" doesn't turn into a URL nobody meant to keep.

**Mechanics:** a **separate Vercel project** (`paleography-syriac`, **Labs team**
`team_sERwO8…`, same as `paleography`), root directory `learn/site/`, no build step, no
`package.json` (research/deploy.md on what a stray one cost). DNS: **CNAME `syriac` →
`cname.vercel-dns.com`, DNS-only (grey cloud), at Cloudflare** — same recipe as the apex, per
[[reference_domains-cloudflare]]; `.app` is HSTS-preloaded so it's HTTPS or nothing. ⛔ **Deploy
from `learn/site/`, never the repo root** ([[feedback_vercel-deploy-from-subdirectory]]).

**The course record — `learn/syriac/course.toml`** is the only place the course is named:

```toml
id = "syriac"
title = ""                      # ← Wilson names it (§7). "First Light" was the prototype's name.
hand_track = "https://paleography.app/syriac"
lessons = ["L00", "L01", … , "L10"]   # order; each maps to LESSON-N.md + drill/LNN.toml
[sources]                       # rendered on /sources and in every lesson footer
nestle-1889-en   = { title = "Nestle, Syriac Grammar with Bibliography, Chrestomathy and Glossary, 1889", rights = "public domain", scan = "archive.org syriacgrammarwit00nestiala" }
payne-smith-1903 = { … }
noldeke-1904     = { … }
barnes-1914      = { … }        # the control edition
[seats]
syriacist = ""                  # empty → /for-syriacists says so, in so many words
```

---

## 3. The drill — what carries forward from First Light, what doesn't

First Light (private artifact, 2026-09-02) is **two things glued together**: a data-driven engine
and Lesson 0/1's data hard-coded into it. Split them.

**The engine carries forward whole.** Its model is already right and already G2-passed:
`TRACKS` → `phases` → items, five phase types (`study`, `translit` "sound it out", `mc`,
`fillin`, `produce`), shuffled order, per-item grading, a scorecard. It uses no
`window.claude`, no storage, no external script — it lifts out of the artifact as one HTML file.
Changes, all small: (a) read `TRACKS` and items from `/drill/LNN.json` instead of constants;
(b) fonts via `@font-face` from `/fonts/` (§4) instead of Google Fonts; (c) persist state in
`localStorage` keyed by lesson so a closed tab doesn't lose a half-done lesson (wrapped in
try/catch; empty is fine); (d) the scorecard gets a **copy-to-clipboard** button that emits the
same fields as the paper scorecard at the foot of every `LESSON-N.md` — that text is the G2 data,
and pasting it into an email is v1's entire feedback loop.

**The track list becomes per-lesson config — this is the answer to "some of the tool from
lesson 0 or 1 won't be helpful for the rest."** Lesson 0's `letters` / `pairs` / `triples` tracks
are the alphabet's and appear only on `/0`. Every lesson from 1 on declares the tracks it needs
from this menu, in the ramp's order (recognition before recall — pilot §6):

| track | phases | fed by | lessons |
|---|---|---|---|
| `letters` `pairs` `triples` | study · recognize · fill-in · produce | invented strings (LESSON-0 Part 3) | 0 only |
| `vowels` | study | the vowel-mark table | 1; again on 5 as "reading without them" |
| `vocabSound` | sound-it-out · recognize | the lesson's new-lemma table (`translit`) | 1–10 |
| `vocabMeaning` | definitions · recognize · reversed · produce | same table (`gloss`) | 1–10 |
| **`forms`** — NEW | study · recognize · produce | the lesson's "new form cells" | 2–10 |
| `halfline` | produce | Stage-1 phrases with one word blanked | 1–10 |
| `cloze` | produce | Stage 2 items, verbatim | 1–10 |
| `finish` | produce | Stage 3 items, verbatim | 1–10 |
| `drills` — NEW | recognize (mc over the 3–6 answers) | the lesson's "Drills (ours)" block | 1–10 |
| `whole` | produce | Stage 4 target line | 1–10 |

`forms` is the one genuinely new track type, and it is small: an item is `{form, cell, gloss,
lemma}` ("ܗܘܳܬ" · "3fs perfect" · "she was" · "ܗܘܐ"); *recognize* asks which cell, *produce* asks
for the gloss. It is the seed of the §10 generated engine — every item carries its `lemma` and
`cell` so a later engine can resample distractors from R1 — but v1 only ever shows the lesson's
own handful. ⭐ Pilot ruling 7 (numerals are decoding, not vocabulary) applies the day a lesson
teaches numerals: those items go in an alphabet-style track (`letters`-shaped), not `vocabMeaning`.

**The sidecar — `drill/LNN.toml` — is extracted from the lesson, and the extraction is checked.**
The `.md` stays the author's document (its prose is the product; it passed G2 as prose). The
sidecar holds only what the engine needs — vocab rows, form rows, cloze/finish/whole items with
their answers — and **`make_learn.py --check` fails if any Syriac string in a sidecar does not
occur verbatim in its lesson's `.md`.** That one rule is what keeps the drill honest to the
lesson and the lesson honest to the R3 plate reading, without restructuring eleven documents
into records today. (Structured lesson records — an "L" type beside R1–R4 — are the right
long-term home and the §10 engine will want them; they are *not* v1. The sidecar is the bridge,
and the verbatim check is the bridge's load rating.)

---

## 4. The lesson page, and what makes it credible

`/N` renders `LESSON-N.md` through the **same local Markdown renderer `make_primers.py` already
uses** (headings, tables, blockquotes, bold/italic/code — the lessons use nothing outside that set;
`--check` should say so rather than silently pass unknown syntax through). Layout: prose column,
with the drill for that lesson embedded **at the point the prose hands off to it** — Stage 1
(read along) is prose; Stages 2–4 are where the engine takes over, so the drill sits after Stage 1
and the paper Stage 2–4 sections collapse to their answer keys. Mobile-first — lessons are read
on a phone, drills are tapped on a phone.

**Fonts settle the setup note.** Every lesson currently opens by telling the learner to install
Meltho. On the web, serve it: **Meltho "Estrangelo Edessa" as the UNMODIFIED `.ttf`** via
`@font-face` — its licence permits redistribution and forbids modification, so ⛔ **no WOFF2
conversion** (research/syriac-pilot-phase0.md §fonts, read it before touching the font files) —
with **Noto Sans Syriac** (OFL, self-hosted or Google Fonts; letterforms follow Estrangela) as
the fallback. `make_learn.py` then strips or rewrites the install paragraph; the `.md` keeps it
for the paper reader.

**Every lesson footer is generated from the lesson's own metadata line** — the R3 record ids it
cites (`c067-1`, `c068-1`…), the control edition, the Nestle page — and each id **links to a
rendered view of that record at `/sources/r3/c067-1`.** This is the single cheapest credibility
move available: a Syriacist clicking through from Lesson 2 lands on the plate reading, the
Barnes 1914 diff, and the flagged v.11 conjunction, exactly as the record holds them. The TOML →
HTML renderer is a hundred lines (no deps; the records use a closed set of fields).

**`/sources`** = the shelf (`course.toml [sources]`) + an index of every rendered record, grouped
R1 / R3 / R4 with each record's `status` / `uncertain` badges visible in the list.

**`/for-syriacists`** = the ask, written once, as a page rather than an email — so the held
outreach becomes "here is what we built; this page lists what we need." Its content is already
inventoried in NEXT-SESSION.md and is *specific*, which is what makes it answerable:
- the **27 Payne Smith R4 records that need only vowel points** (`voc` empty on purpose);
- `p031-1` row I.b (a 'foot' word taking masculine plural endings — wrong lexeme, or real?);
- `p034-1`'s person-assignment of Nestle's seven worked forms (proposed, not proven);
- `p063-1`'s second bāṯar-shaped word (teth vs taw);
- the four `proposed` dot-glosses on the hand track;
- the 44 unkeyed Vitae Prophetarum / Historia inventionis pages (needs a reader or Serto HTR);
- the open seat itself (`course.toml [seats].syriacist = ""`), stated plainly.
Each item links to its record. The page ends with the licence facts a scholar will check first
(§6) and the contact address.

**`/about`** = the pilot in a page: the thesis ("learning Syriac to read Syriac"), the method
(PD primers → four record types → re-sequenced reading-first → every lesson ends in real text),
what's checked and what isn't, and the twin-path relationship to the hand trainer. ⚠ **Authored
prose → Opus** ([[feedback_opus-for-authored-prose]]); it is also the one page that should say
what the whole project is *for*, so Wilson reads it before it ships.

**`/`** = one paragraph, the lesson list with a one-line "what you'll be able to do" per lesson
(each `LESSON-N.md` already has that sentence — generate, don't rewrite), and the three doors:
start at Lesson 0 · read the hand · for Syriacists.

---

## 5. Phases, in order — each ends in something checkable

**Phase A — the tree and the renderer (Sonnet).** `git mv LESSON-*.md learn/syriac/` and fix
every pointer (`NEXT-SESSION.md`, `SYRIAC-LESSON-PLAN.md`, `SYRIAC-LANGUAGE-PILOT.md` §9,
`paleography.md` memory). Write `course.toml`. Write `make_learn.py` reusing `make_primers.py`'s
renderer (import it; don't fork it). Render eleven lesson pages with footers and `/sources/r3|r1|r4/<id>`
record views. **Gate:** every lesson renders; `--check` passes on the closed Markdown set; every
record id in every lesson footer resolves to a rendered record.

**Phase B — the engine (Sonnet).** Lift First Light's HTML into `learn/shell/drill_shell.html`;
externalise `TRACKS`/items to JSON; add `forms` and `drills` track types; localStorage; scorecard
copy. Write `drill/L00.toml` and `L01.toml` by transcribing First Light's own constants (they ARE
Lesson 0/1's data, already G2-passed — carry them over verbatim, don't re-derive). **Gate:**
`/0` and `/1` behave identically to the prototype Wilson ran; `--check` verbatim rule passes.

**Phase C — sidecars for 2–10 (Sonnet, with the verbatim check as the reviewer).** One TOML per
lesson from its `.md`: vocab table → `vocabSound`/`vocabMeaning`; "new form cells" → `forms`;
Stage 2/3/4 and the Drills block → `cloze`/`finish`/`whole`/`drills`; half-line items by
blanking one word of a Stage-1 line (the one judgment call — prefer the lesson's own cloze
anchors). **Gate:** `--check` passes for all eleven; eyeball one lesson's drill end to end.

**Phase D — the three scholar pages (Opus for `/about` and `/for-syriacists` prose; Sonnet for
`/sources` and `/`).** **Gate:** Wilson reads `/about` and `/for-syriacists` — these are what a
Syriacist judges the project by.

**Phase E — ship (Sonnet/Haiku; two hard stops).** Create the Vercel project · `npx vercel --prod`
**from `learn/site/`** (⛔ stop 1: production deploy — "deploy? y/n") · add the Cloudflare CNAME
(⛔ stop 2: outward-facing — the address becomes reachable; "make it live? y/n") · verify on the
real domain, not the `.vercel.app` URL. Then the outreach email is unblocked — **and is still
Wilson's own send, a third stop, not part of this plan.**

Order matters: A before B so the engine has pages to embed in; B before C so sidecars have a
consumer to test against; D can run in parallel with C; E last, once.

---

## 6. Rights and attribution — write the footer from this, not from memory

Per [[wroot-press-licensing]] — read it before writing the footer; the rule is by *class of
work*, not house-wide:
- **Nestle 1889, Payne Smith 1903, Nöldeke 1904, Barnes 1914: public domain.** No licence is
  claimed over their text; a transcription of a PD text creates no new copyright (*Feist*), and
  saying otherwise is copyfraud a serious reuser will notice.
- **What IS claimed, CC BY-NC 4.0 (a site — the "online" class):** the lesson prose, the drill
  data, the glosses and notes, and the encoding as a compilation (record ids, alignment diffs,
  the sequencing itself).
- **Free, never paywalled** (pilot ruling 5).
- **Fonts:** Meltho — Beth Mardutho, redistributed unmodified under its own terms; Noto — OFL.
- **Attribution** (CC BY's one condition, and the thing that was missing on the hand site once
  — `paleography.md` "Attribution was missing"): none of this build's sources is CC-licensed, so
  nothing is *owed*, but the shelf is named in full on `/sources` anyway, because a scholar
  reads a bibliography before a thesis.

---

## 7. Rulings wanted from Wilson — answerable in a word each

1. **URL convention** — `<lang>.paleography.app` = learn, `paleography.app/<lang>` = read the
   hand, as a standing rule? (Recommend **yes**.)
2. **Separate Vercel project** rooted at `learn/site/`, Labs team? (Recommend **yes**.)
3. **Move `LESSON-*.md` into `learn/syriac/`** with pointer updates? (Recommend **yes**; the
   alternative is a build that globs the repo root.)
4. **Sidecar drill TOML with the verbatim check**, not lesson records, for v1? (Recommend
   **yes**; records are the §10 engine's problem.)
5. **Publish the R1/R3/R4 records as pages** under `/sources/…` and build `/for-syriacists` on
   them? (Recommend **yes** — it is the outreach gate's actual deliverable.)
6. **A name** for `course.toml [title]`. "First Light" was the prototype's; keep it, or not.
7. **Scorecard = local + copy-to-clipboard, no Supabase in v1?** (Recommend **yes**; the hand
   site's opt-in confusion collection can extend here later, and the letter-confusion thesis
   says it eventually should — but not before a learner other than Wilson exists.)

---

## 8. Execution tiers, and one nudge

The score is written; playing it is Sonnet with Opus on the two authored pages. Nothing in
Phases A–C, or E, is a judgment call once §§1–6 are agreed — they are pattern-following against
machinery the repo already has (`make_primers.py`, `trainer_shell.html`, `make_routes.py --check`,
the deploy notes). Rough burn: Phases A–C ≈ 150–250K tokens across two or three sessions; D is
two pages of prose; E is twenty minutes and two stops. ⚠ 8 GB Mac: no agent fan-out — one
phase at a time, single-threaded, as every Syriac session so far has run.

## 9. Left out on purpose

The §10 generated drill engine (needs lesson records and the R1 cell schema settled) · SRS for
vocab/parsing (needs a learner population and the Tabella export question) · stroke-order
animation · East Syriac / Serto variant lessons (post-pilot, pilot §6) · reading-data collection
(§7 item 7) · Lessons 11+ from the bank (`SYRIAC-LESSON-PLAN.md` §3) · Hebrew · any change to
the hand trainer's `site/`.
