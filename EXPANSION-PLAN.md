# Paleography — from two languages to many

*Wroot Labs · Fable planning session 2026-08-28 · status: PLAN. Execution is Opus/Sonnet work
(see §7); nothing here is built.*

Wilson's brief: broaden the space beyond Greek and Latin — Old English, Middle English, Old
French, Sanskrit, Syriac, Aramaic, Hebrew, Dead Sea Scrolls, Coptic. The guided-image ramp
(orientation → read-along → one word → finish the line → whole line) should work in each.
The trainer today flips between three tabs; each language will need its own space.

`PLAN.md` said "adding a track is content, not code." That was true for a second Latin
witness. It is **not** true for Hebrew — and the honest version of this plan starts there.

---

## 1. The organising decision: language is the door, script is the data

A learner arrives with a **language prior** (they read Hebrew, or Old French, in print). The
corpus is organised by **script** (Hebrew square script serves Hebrew *and* Aramaic; Latin
script serves Latin, Old English, Middle English, Old French; Syriac script serves Syriac,
which *is* an Aramaic dialect). Neither axis alone works:

- By language only: Aramaic would be three unrelated things (Targum in Hebrew square, Syriac
  Estrangela, Qumran scrolls) with nothing shared.
- By script only: an Old French reader is told "go to Latin", which is wrong pedagogically —
  they don't read Latin, and the abbreviation system and letterforms of a 13th-c. Gothic
  vernacular hand are not Caroline.

So: **language = the learner-facing space** (its own URL, landing page, primer, expert
reviewer, progress). **Script profile = the shared machinery** underneath (direction, fonts,
input keymap, normalisation, difficulty scorer, palette, structural marks). A **track** is one
witness inside one language, bound to one script profile.

```
Language   /hebrew        landing + primer + expert + progress namespace
  Track    /hebrew/ashkenazi-bible    one witness, one script profile, one layer
  Script   hebrew-square              profile: rtl, fonts, keymap, norm, scorer, palette
```

Aramaic is therefore **not a space of its own at first**: Targum witnesses live under Hebrew
(same script profile), Syriac has its own space, and the scrolls are a track under Hebrew
(§4). Revisit if an Aramaic reader base shows up that wants a door of its own — it's a
landing page, not a rebuild.

## 2. What actually breaks today (the audit)

Everything below assumes "Latin-family or Greek" in code. This is the refactor list.

| Where | Hardcoded thing | What a config-driven version needs |
|---|---|---|
| `tools/build_exercises.py` `specs` | 3 tuples, per-track scorer function | read `languages/*.yml`; scorer selected by script profile |
| `latin_difficulty` / `greek_difficulty` | "non-ASCII = abbreviation" (Latin), "non-plain = diacritic" (Greek) | one scorer per profile; RTL abjads need a *vocalisation-density* scorer (pointed vs unpointed), Devanagari a *conjunct-density* scorer |
| `GREEK_PLAIN`, `STRUCT` | literal sets | per profile |
| `is_sentence` | `< 3 words`, `>72% .isalpha()` | word-count threshold per profile (scriptio continua Coptic/DSS has no spaces → use character count) |
| `cloze_index` | longest run of `.isalpha()` | fine for alphabets; combining marks (nikkud, Syriac points, Devanagari matras) must count with their base — use grapheme clusters, not code points |
| `trainer_shell.html` tabs `tab-latin/latin2/greek` | 3 tabs, `["latin","latin2","greek"].forEach` ×2 | tabs rendered from `DATA.languages[lang].tracks` |
| `PATH` map `/latin → latin` | literal | routes derived: `/<lang>/<track>` |
| `ORIENT`, `ORIENT_TAIL`, `PALETTE` keyed by track | literal per track | per-track orientation prose in the language's content file; palette per profile |
| `isGk()`, `fam()` | binary Greek/Latin | `profile()` returning the script profile object |
| `norm()` | ς→σ, ſ→s, strip combining if Greek | profile-declared: finals folding (ך→כ ם→מ ן→נ ף→פ ץ→צ; ς→σ), strip points (nikkud U+05B0–05C7, Syriac U+0730–074A, Coptic combining overline), Devanagari: *never* strip matras — they are letters |
| beta code `BETA_BASE`/`BETA_DIA`, `wireBeta` | Greek only | generic transliteration keymap per profile (§5) |
| CSS `--greek` font var, `.gk` class | one non-Latin font | per-profile font stack + `dir="rtl"` + `unicode-bidi` on the input, the compare view, the palette |
| `Levenshtein` diff render | LTR assumed | diff must be rendered in the profile's direction; alignment itself is direction-free |
| `site/vercel.json` rewrites | 3 literal routes | generated from the registry; old `/latin` `/latin-ii` `/greek` become 301s |
| `site/index.html` | 3 hand-written track cards | landing lists **languages**; each language page lists its tracks |
| single 10.9 MB payload | all tracks in one file | **per-track JSON fetched on demand** — this was already owed; it is now mandatory (nine languages in one file is 30 MB+) |
| Supabase `attempts` allowlist | confusion pairs validated against Latin/Greek charset | validator takes the profile's charset; RLS unchanged |
| `handoff.md` | one Greek expert | one handoff per language (§6) |

Not broken: the five-stage ramp, the cloze-in-text idea, the Levenshtein alignment, PAGE XML
export, the ingest normaliser (ALTO/PAGE/TEI are script-agnostic), Supabase collection.

## 3. The registry (the one new file shape)

```yaml
# languages/hebrew.yml
id: hebrew
name: Hebrew
lede: "You read pointed and unpointed Hebrew in print. …"        # landing card
primer: scripts/hebrew-square.md
expert: null                                                    # who rules on glosses
profile: hebrew-square                                          # → profiles/hebrew-square.yml
tracks:
  - id: ashkenazi-bible
    witness: biblia-ashk-01        # → corpus/sources.yml
    name: "Hebrew — Ashkenazi square script"
    layer: diplomatic
    printed: "…"                    # the orientation paragraph
```

```yaml
# profiles/hebrew-square.yml
direction: rtl
fonts: ["Noto Serif Hebrew", "SBL Hebrew", serif]     # Google Fonts has Noto Serif Hebrew
keymap: sbl-simple           # tools/keymaps/sbl-simple.json  (a→א? no: consonant-only map, see §5)
scorer: vocalisation_density
finals: {ך: כ, ם: מ, ן: נ, ף: פ, ץ: צ}
strip_marks: [U+05B0-U+05C7]      # for the tolerant compare only; the strict compare keeps them
structural: ["׃", "׀"]              # sof pasuq, paseq — apparatus, not text
min_words: 3
palette: ["א","ב","ג",…,"ְ","ָ","ַ","ֶ","ֵ","ִ","ֹ","ֻ","ּ"]
```

Profiles needed: `latin-caroline` (exists in spirit), `latin-gothic` (OE/ME/OF), `greek-minuscule`
(exists), `hebrew-square`, `syriac` (one profile, three hands: Estrangela / Serto / East
Syriac — a *variant* field on the track, not three profiles, since points and letters are
shared), `coptic-uncial`, `devanagari`. Seven profiles cover all nine requested languages.

## 4. Seed data — what exists, honestly (checked 2026-08-28)

Ranked by **how much open ground truth exists × how much new code it forces**. Licences and
counts are from HTR-United's catalogue and the publishing records; **re-verify each before
ingest** — the catalogue was wrong about wien940's format and layer, and it will be wrong again.

| Language | Best open GT | Lines | Licence | Images | Verdict |
|---|---|---|---|---|---|
| **Old French** | CIHAM *Fabliaux* (1200–1402) · CIHAM *Liber* (fro+lat, s. XIV) · TranscriboQuest 2025 vernacular (59,696 lines, mixed) | 2,070 · 3,789 · 59k | CC BY 4.0 | check each repo; TranscriboQuest bundles some | **Go first.** Latin script, zero new profile code beyond a Gothic scorer. Proves the language/track split cheaply. |
| **Hungarian** | ⭐ **FAST-TRACKED, ships 2nd** (§8.6). **No HTR GT exists** — nothing Hungarian in HTR-United, catalogue checked directly. But the **Ómagyar Korpusz** (NYTUD/ELTE) has all 47 codices transcribed in original orthography (+ normalised + morphologically analysed). | 47 codices / 3.2M tokens (text only, **not image-aligned**) | ⚠ **UNVERIFIED** — likely CC BY-NC-SA via META-SHARE. Check before ingest. | ⚠ **UNVERIFIED** — OSZK `nyelvemlekek.oszk.hu` has facsimiles; site 404'd and the corpus host has a bad cert, so neither could be read | **Latin script — rides the `latin-gothic` profile Old French builds, so zero new profile code.** The GT job is **alignment, not keying** (the answer key is already published), which is materially cheaper than OE/ME. Witnesses: Halotti beszéd (1192–95, Pray Codex, OSZK) · Ómagyar Mária-siralom (c. 1280–1310, Leuven Codex, OSZK) · Jókai-kódex (after 1370, oldest Hungarian book) · the 15th–16th c. codices (Munich, Érdy, Festetics…). |
| **Syriac** | ÖNB Cod. Syr. 1 (HTR Winter School 2024, 1545, Serto) · Jerusalem St Mark's 36 (Winter School 2025, s. XII–XIV, Estrangela w/ Serto+East features) | 2,869 · 17,836 | CC BY 4.0 | ÖNB by IIIF (same route as Cod. 940); Zenodo bundles bifolio images for St Mark's | **The RTL pilot.** Same ÖNB IIIF path we already solved; two hands from one profile. |
| **Hebrew (+Aramaic)** | BiblIA (Stökl Ben Ezra et al., 2021): 202 pages / ~100 MSS, six scripts (Ashkenazi, Byzantine, Italian, Oriental, Sephardi, Yemenite), Hebrew **and Aramaic** | ~202 pp | "SA" — read the Zenodo record: BY-SA is fine, but **the images are BnF + Vatican** — BnF non-commercial, Vatican restrictive; the *transcription* being open doesn't clear the *plate* | ⚠ Rights on the images decide whether this is a track or a deep-link | **Second RTL language.** Best script variety of any dataset; Aramaic arrives free. Also Tikkoun Sofrim / Sofer Mahir (Stökl) — rabbinic, big, SA. |
| **Coptic** | SCAM (Sahidic, 2026 arXiv 2606.15987) — line-level, dispersed leaves of one MS | unknown | paper CC BY; **dataset licence not in abstract** | dispersed institutions — per-leaf rights | Promising, unverified. Also Coptic SCRIPTORIUM (CC BY text, no line GT). Needs a fetch of the actual record before committing. |
| **Sanskrit** | ⭐ **RULED: early print.** Heidelberg Devanagari GT (Naval Kishore Press, 1880–1953) | 4,333 | CC BY 4.0 | bundled | **Ships as early print, labelled as type not a hand** (§8.3). Pracalit-script Nepalese MSS (Zenodo, PNG+XML) stay available for a later, honestly-named "Nepalese manuscripts" space — not Sanskrit's door. |
| **Old English** | **None in HTR-United.** Images exist (Parker on the Web CC BY-NC; BL Cotton MSS) but no open line-level GT found. | — | — | — | ⭐ **GREEN-LIT, self-produced** (§8.5): CC BY-NC witness → Kraken draft → expert correction, ~110 lines. Content gap, not code gap. First open GT for OE reading exercises. |
| **Middle English** | **None in HTR-United.** Same shape as OE; more digitised witnesses (Auchinleck, Ellesmere are restrictive). | — | — | — | ⭐ **GREEN-LIT, self-produced.** Do this one first of the two: later Gothic hands read easier and Kraken's medieval Latin models give a usable draft. |
| **Dead Sea Scrolls** | Leon Levy DSS Digital Library (IAA): images "contact for licensing"; DJD transcriptions © OUP. Groningen (Popović) HTR work is research, not open GT. | — | **closed** | closed | ⛔ ⭐ **RULED: link page, never crops** (§8.2). A "Qumran" page under Hebrew teaching the hand from Wilson's description + links into the IAA viewer. Hosting a plate is not legal here. |

**Ordering that follows** (⭐ ruled 2026-08-28): Old French → **Hungarian** → Syriac →
Hebrew/Aramaic → Coptic (after a rights fetch) → Sanskrit (early print) → Middle English →
Old English (both self-produced) → DSS (link page only).

⛔ **Rovásírás is NOT a track, and the primer must say why.** Székely-Hungarian runes have
genuine medieval attestation (Transylvanian inscriptions, the Nikolsburg alphabet of 1483) but
were used for *short epigraphic texts* — names, ownership marks, notations. There is
essentially **no manuscript literature in rovás**, and what circulates today is largely a
20th-c. revival carrying some nationalist freight. One honest paragraph in the Hungarian primer
explaining exactly that is worth more than a track, and corrects a thing people get wrong.
**The codices are authentic manuscripts; the runes are authentic but epigraphic only.**

## 5. The two genuinely new mechanisms

**5a. Right-to-left, end to end.** The stage that asks the learner to *type* is the one that
breaks. `dir="rtl"` on the input, the compare row, the palette; the Levenshtein diff renders
right-to-left; the caret-position arithmetic in `wireBeta` (it re-projects the cursor after
transliteration) must be re-derived for RTL. Test on Syriac first — Estrangela has no finals
and light pointing, so it isolates the direction problem from the normalisation problem.

**5b. Transliteration input as a first-class profile field.** Beta code is the Greek case of
a general thing: *type on a Latin keyboard, see the target script*. One keymap engine, one
JSON per script:

- Greek: beta code (exists, keep).
- Hebrew: consonant map (`b→ב`, `sh→ש`, `T→ט`, `t→ת`, `s→ס`, `S→שׂ`…) — **unpointed by
  default**; a tolerant compare strips points. Pointed drills are a stage-5 extension.
- Syriac: same shape (`)→ܐ` … choose SEDRA-style), unpointed.
- Coptic: near-1:1 with Greek beta code + six Demotic letters (`S→ϣ f→ϥ x→ϧ h→ϩ j→ϫ c→ϭ ti→ϯ`).
- Devanagari: Harvard-Kyoto or IAST → Devanagari **with virama/conjunct handling** — this
  is a real transliterator, not a char map. Use an existing library (e.g. `sanscript`) rather
  than writing it; it's the one keymap that justifies a dependency.
- Latin-script vernaculars: no keymap; palette gains þ ð ƿ æ ȝ (OE/ME) and the Gothic
  abbreviation signs.

## 6. People: every language gets an expert, and Wilson isn't it

Wilson runs the Greek queue and knows the Latin. For the rest he said it himself: "I don't
have many of these languages down." The Greek handoff pattern (`handoff.md` → a friend →
their own AI session → three concrete questions) **is the scaling unit**. Each language space
ships with:

- a `handoff-<lang>.md` written the same way (what it is, what exists, three questions);
- a `expert:` field in the registry (null until someone accepts);
- glosses marked `proposed` until that expert verifies them — exactly the Latin/Greek rule,
  and the primer says on its face when the expert seat is empty.

Without this, a Syriac track is a Latin reader's guess about Syriac, and the first Syriacist
who sees it says so publicly.

## 7. Phases, and who does them

- **Phase A — refactor to registry (code, no new content).** Registry + profiles for the three
  existing tracks; tabs/routes/orientation/palette/norm driven from them; per-track JSON
  payload; language landing pages; 301s for the old URLs; Supabase validator takes a charset.
  *Byte-identical behaviour for Latin I/II/Greek is the acceptance test.* **Opus.**
- **Phase B — Old French.** One CIHAM witness, `latin-gothic` profile, Gothic scorer, OE/ME
  palette additions. Proves "new language = registry + content". **Sonnet** once A exists.
- **Phase B2 — Hungarian.** ⭐ Fast-tracked to ride B's `latin-gothic` profile while it is warm.
  **Two gates first, both Wilson's:** (a) Ómagyar Korpusz licence, (b) OSZK image rights —
  neither could be read on 2026-08-28 (404 / bad cert), so this phase does not start until both
  are known. The new build step is a **text↔image aligner** (published transcription → line
  polygons on a facsimile): that tool does not exist yet and is the real cost here, but it is
  reusable for every later self-produced track, which is why it is worth building on the
  language where the answer key is already published. Start with the Jókai-kódex or the
  Ómagyar Mária-siralom. Primer carries the rovás paragraph (§4). **Opus** for the aligner,
  Sonnet for the content. ⭐ **Expert seat: Alina** — verifying a reading against an
  already-published corpus text needs a Hungarian reader, not a paleographer.
- **Phase C — Syriac (RTL pilot).** §5a + §5b keymap engine. ÖNB IIIF route reused. Two
  tracks (Serto 1545, Estrangela s. XII). **Opus** for the RTL/keymap engine, Sonnet for the
  second track.
- **Phase D — Hebrew/Aramaic.** Rights ruling on BiblIA images first (Wilson). Then content
  only, plus finals folding and point-stripping in the profile. **Sonnet.**
- **Phase E — Coptic, Sanskrit.** Coptic still gated on a licence fetch of the SCAM record.
  Sanskrit is **settled as early print** (§8.3) — content plus the Devanagari transliterator,
  which is the one Opus item here (virama/conjunct handling; use `sanscript`, don't write it).
  The Sanskrit space must state it is teaching type.
- **Phase F — Middle English, then Old English.** ⭐ Green-lit. ~110 lines each: pick a CC BY-NC
  witness, Kraken draft, expert correction. This is Phase 3 contribution mode arriving early,
  so build it as the real thing rather than a one-off script. **ME first** (easier hands, better
  Kraken priors). ⚠ Gate: an expert in the `expert:` seat before any gloss ships; until then the
  primer says the seat is empty.
- **DSS** — one page under Hebrew, no crops (§8.2), when Hebrew lands.

Estimated burn: Phase A is the only large one (the shell is 50 KB of hand-wired JS); B–D are
each a fraction. No agent fleet; one session per phase.

## 8. Rulings (Wilson, 2026-08-28 — all five settled)

1. ⭐ **Aramaic folds in — no door of its own.** Targum and BiblIA's Aramaic pages sit under
   Hebrew (same square script); Syriac is its own space and is itself Aramaic. Revisit only if
   an Aramaic readership asks; it is a landing page, not a rebuild.
2. ⭐ **DSS = link page, never crops.** A Qumran page under Hebrew: Wilson's description of the
   hand, links into the IAA viewer, zero hosted images, and it says on its face why there are
   no exercises. Same move PLAN.md made for papyri. ⛔ Do not host a DSS plate, and do not
   write to the IAA for terms without asking first.
3. ⭐ **Sanskrit ships as EARLY PRINT — Naval Kishore Press Devanagari** (4,333 lines, CC BY,
   images bundled). Devanagari is what a Sanskrit reader expects to see, and "early print" is
   a category PLAN.md already wanted for the Press. ⚠ **The space must say it is type, not a
   hand** — this track teaches typography and the Devanagari abbreviation/conjunct repertoire,
   not paleography. Pracalit is not ruled out later, under an honest "Nepalese manuscripts"
   label; it is not Sanskrit's door.
4. ⭐ **Old French goes first** after Phase A. Cheapest proof that "new language = registry +
   content". The RTL question waits for Syriac in Phase C.
5. ⭐ **Old AND Middle English green-lit** — ~110 lines each, self-produced. CC BY-NC witness →
   Kraken draft → expert correction. This is Phase 3 contribution mode arriving early, and it
   makes us the first open GT for OE/ME reading exercises, which is itself why scholars would
   look. ⚠ **Two expert seats must be filled before any gloss ships** — the primer says the
   seat is empty until then.
6. ⭐ **Hungarian is fast-tracked to second, right behind Old French** (added 2026-08-28 after
   Wilson asked; it is his wife's heritage language). It rides Old French's `latin-gothic`
   profile, and its GT job is **alignment rather than keying** because the Ómagyar Korpusz
   already publishes the transcriptions of all 47 codices.
   ⚠ **Blocked on two licence checks Wilson owes** — the corpus licence and OSZK image rights;
   neither could be read on 2026-08-28. ⛔ Rovásírás is not a track — one honest paragraph in
   the primer instead (§4). ⭐ Expert seat: **Alina**.

---

Related: `PLAN.md` §3 (tracks), `research/deploy.md` (ÖNB IIIF route to reuse for Syriac),
`handoff.md` (the per-language expert pattern), memory `paleography`, `wroot-press-licensing`
(rights discipline applies to every plate).
