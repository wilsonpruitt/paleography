# Cappelli, *Lexicon Abbreviaturarum* — page/leaf index for 16 target signs

## 1. Chosen scan

**Identifier: `lexiconabbreviat29capp`** (archive.org)
"Lexicon abbreviaturarum. Dizionario di abbreviature latine ed italiane... con l'aggiunta
di uno studio sulla brachigrafia medioevale..." (1929 edition — the full bilingual title
matching the task, i.e. the mature, definitive edition, not the 1901 German-titled
*Wörterbuch* predecessor).

Why this one over the alternatives:
- `lexiconabbreviat00capp` (1901, German title) — real and public domain (612 images) but
  an earlier/different edition (German front matter). Not preferred.
- `pbc.gda.pl.Lexicon_abbreviaturarum_Cappelli_` — metadata returned **no title, no date, no
  `_djvu.txt`, no files list** — effectively a bad/empty item on archive.org. Rejected.
- `CappelliDizionarioDiAbbreviature` (1929, 630 images) — legitimate alternate scan of the
  same 1929 edition, has `_djvu.txt` and scandata. Viable backup but slightly lower
  imagecount and its `_scandata.xml` lacks the clean, fully-consistent leaf→page offset
  found in the chosen item (not fully checked — deprioritized once the other item's offset
  was verified as clean).
- `lexiconabbreviat29capp` (1929, **634 images**) — highest imagecount, public domain
  (`access-restricted-item` absent), has `_djvu.txt` (792,793 bytes) and `_scandata.xml`
  (537 pages carry OCR'd `<pageNumber>`), and — critically — page images are reachable at
  `https://archive.org/download/lexiconabbreviat29capp/page/n<LEAF>.jpg` and the
  leaf→printed-page offset is a single constant across the entire arabic-numbered body
  (verified against 15+ page images). **Selected.**

No candidate 404'd; only the `pbc.gda.pl...` item was effectively unusable (empty metadata).

## 2. Leaf offset (calibrated against real page images, not just scandata)

`_scandata.xml` has a `<pageNumber>` field on 537 leaves, but it is **off by one** from the
actual printed page (scandata undercounts by 1). Do not trust it directly — trust the
formula below, which was checked against 15 independently fetched page images.

- **Main dictionary body (arabic pagination, pp. 1–~539):** `printed_page = leaf − 93`
  - Worked example: `leaf n137` → image shows running head "CANᵣₒ - CANRIA — **44** —" →
    137 − 93 = 44. ✓
  - Second check: `leaf n300` → page **207** → 300 − 207 = 93. ✓
  - Anchor: `leaf n94` is literally page **1** of the dictionary (signature mark
    "1 – CAPPELLI." at the foot of the page). 94 − 93 = 1. ✓
- **Front matter (roman pagination, pp. V–~LX, the brachigrafia treatise + facsimile
  plates):** `printed_page(roman) = leaf − 3`
  - Worked example: `leaf n50` → page **XLVII** (47) → 50 − 47 = 3. ✓
  - Second check: `leaf n40` → page **XXXVII** (37) → 40 − 37 = 3. ✓
  - The jump from front-matter offset (+3) to dictionary offset (+93) happens because 9
    full facsimile plates ("Tavola I–IX", each with its own transcription) sit between the
    end of the treatise (~p. LX) and dictionary p. 1 at leaf 94, without continuous
    numbering.
- Printer's signature marks ("N – CAPPELLI.") recur roughly every 16 pages inside the
  dictionary body and were used as a sanity check on the offset formula (e.g. "26 –
  CAPPELLI." near dictionary p. ~401–402) — consistent with the leaf−93 rule.

## 3. Structure map (from the book's own back-of-volume INDICE, `_djvu.txt` line ~73594)

| Part | Printed pages | Leaves |
|---|---|---|
| Prefazione | p. V | ~leaf 8 |
| Avvertenza | p. IX | ~leaf 12 |
| **Brachigrafia Medioevale** (treatise) | pp. XI–LII | leaves 14–55 |
| — I. Abbreviature per troncamento | p. XI | leaf 14 |
| — II. per contrazione | p. XVI | leaf 19 |
| — **III. Segni abbreviativi con significato proprio** | pp. XXIII–XXVIII | **leaves 27–31** |
| — **IV. Segni abbreviativi con significato relativo** | pp. XXIX–XXXIX+ | **leaves 32–42+** |
| — V. Abbreviature per lettere sovrapposte | p. XLI | leaf ~44 |
| — VI. Segni convenzionali (intro discussion) | p. L | leaf ~53 |
| Numerazione romana ed arabica (intro) | p. LII | leaf ~55 |
| Trascrizione dei 9 facsimili (Tavole I–IX) | pp. LVII–~LX + plates | leaves ~60–93 |
| **Dizionario di abbreviature** (main alphabetical body) | **pp. 1–406** | **leaves 94–499** |
| Segni convenzionali (appendix table) | p. 406 | leaf ~499 |
| Numerazione romana | p. 413 | leaf ~506 |
| Numerazione arabica | p. 422 | leaf ~515 |
| Sigle ed abbreviature epigrafiche | p. 429 | leaf ~522 |
| Bibliografia | end matter | leaf ~630+ |

Sections **III and IV are the systematic tables of general-purpose abbreviation signs** —
the most valuable pages for this project, since they explain the sign system directly
rather than through 16,000 scattered dictionary headwords.

## 4. The 16 signs — page/leaf table

All "leaf" numbers are for `page/n<LEAF>.jpg` on `lexiconabbreviat29capp`. Every row marked
✓ was confirmed by actually reading the page image (not OCR alone).

| # | Sign | Meaning | Printed page | Leaf | Evidence | Confidence |
|---|---|---|---|---|---|---|
| 1 | Macron/line over vowel | omitted m or n | **p. XXIV** | **27** | Image: "I. —, ⌢ = m, n" + examples `cōdo=conditio, cōmūe=commune, ī=in` | High ✓ |
| 2 | Tilde over c | = con | **p. XXX** | **33** | Image: "c̄ = cum, con, cen..." (also general 9-shaped con-sign, p. XXIV–XXV, leaves 27–28) | High ✓ |
| 3 | p, stroke through descender | = per | **p. XXX**; also p. 257 | **33**; also **350** | Image: "p̄ = per, par... por..." (leaf33); dictionary spread of per/pro glyphs (leaf350) | High ✓ |
| 4 | p, loop/flourish | = pro | **p. XXXVIII**; also p. 257 | **41**; also **350** | Image: "p, p̓, p' = pro. — Come: p̌cl=procul, pt=prout" (leaf41); dictionary spread (leaf350, right column "p̓p̓=pro XIf." etc.) | High ✓ |
| 5 | q, stroke through descender | = qui | **p. XXX** | **33** | Image: "q̄ = qui (3)" | High ✓ |
| 6 | q, stroke above | = quod | **p. XXXVIII** | **41** | Image: "9̗ = quod (1) — Come: q̛d=quoddam, q̛dāo=quodammodo" (footnote: same sign = qui in Visigothic script) | High ✓ |
| 7 | Superscript vowel over q | qua/qui/quo (e.g. quasi) | p. XXXI (quae/quoque/quam); **p. 304 (quasi itself)** | 34; **397** | Image p.XXXI: "q̄=quae, q̄q̄=quoque, q̃=quam"; Image p.304: "q̄i, q̄' = (qi) **quasi** XV f." | High ✓ |
| 8 | Semicolon-shaped sign | -que after q, -bus after b | **p. XXIX**; also p. XXXI | **32**; also **34** | Text: "dopo la lettera b (b·, b:, b;, b3) hanno valore di us [→bus]... dopo la lettera q hanno valore di ue [→que]"; examples on p.XXXI: `quib:=quibus, quod;=quodque, usq;=usque` | High ✓ |
| 9 | "us" modifier-letter sign (superscript 9/virgola) | = -us | **p. XXIV** (enum.); worked examples **p. XXV–XXVI** | **27**; **28–29** | Image: "III. 9 ⁹ = us, os, is, s"; image p.XXVI: `pri⁹=prius, su⁹=suus, p⁹=post, nob⁹=nobis` etc. | High ✓ |
| 10 | "ur" hook sign (arabic-2-like) | = -ur | **p. XXIV** (enum.); worked examples **p. XXVII** | **27**; **30** | Image: "V. 2 ∼ ʋ ⌣ = ur, tur, er"; image p.XXVII: `tenet²=tenetur, dic²=dicitur, currit²=currit` [c²rit] | High ✓ |
| 11 | "est" sign (division-sign-like, "3"-shaped) | = est | pp. XXX–XXXI | 33–**34** | Text: "Nel secolo XIV il segno 3 vale est... **prod3=prodest, it'3=interest**" | High ✓ |
| 12 | Tironian et | = et, e (etiam, ...ent) | **p. XXIV** (enum.); worked examples **p. XXVIII** | **27**; **31** | Image: "VII. 7, & = et, e"; image p.XXVIII: `7̄,& = etiam,...ent; ag&=agent; 7dicti=edicti` | High ✓ |
| 13 | l with stroke | = vel | **p. XXX** | **33** | Image: "ł, ł = vel, ul..., ...el" | High ✓ |
| 14 | d with stroke, esp. "qd" | = quod | **p. 307** | **400** | Image: full column of `qđ, qđ' = (qd) quod` variants (also `đ` alone = "quidem, - quondam") | High ✓ |
| 15 | e caudata (e-ogonek) | = ae | — | — | **UNLOCATED.** No mention found in Avvertenza, Brachigrafia treatise (sections I–VI), or the back-of-book Segni Convenzionali appendix (pp. 406–412). Cappelli's *Lexicon* catalogues abbreviation/suspension signs, not orthographic ligature variants, so ę may simply fall outside this book's scope. Do not guess a page. |
| 16 | Nomina sacra: DS | Deus | **p. 109** | **202** | Image: "D̄S = (Ds) Deus XIII"; "D̄S = (ds) dominus XIV" (both on same page) | High ✓ |
| 16 | Nomina sacra: DNS | Dominus | **p. 105** | **198** | Image: "D̄N̄S = (DNS) Dominus VII" | High ✓ |
| 16 | Nomina sacra: IHS | Iesus | **p. 176** | **269** | Image: "IHS = (IHS) Iesus VI"; "ihs = (Ihs) Iesus VI" | High ✓ |
| 16 | Nomina sacra: XPS | Christus | **p. 402** | **495** | Image: "XS = (XS) Christus XVI p." — Cappelli's font renders the chi-rho ligature as "X̄P̄"/"XS"; same page shows X̄P, Xpi, Xpia, Xpo, etc. | High ✓ (rendered as X̄S/X̄P̄, not literal Latin letters "XPS") |
| 16 | Nomina sacra: SPS | Spiritus (Sanctus) | **p. 360** | **453** | Image: "S̄P̄S = (SPS) spes, - spiritus VIII" | High ✓ |
| 16 | Nomina sacra: SCS | Sanctus | **p. 346** | **439** | Image: "S̄C̄S = (SCS) Sanctus (cap. rust.) IX" + multiple `sc̄s` variants | High ✓ |

## Summary

**15 of 16 signs located and image-confirmed.** Only #15 (e caudata / ae) is UNLOCATED — it
does not appear to be treated in this dictionary at all (checked Avvertenza, the full
Brachigrafia treatise sections I–VI, and the Segni Convenzionali appendix). A later session
should read leaves **27, 28, 29, 30, 31, 32, 33, 34, 41, 202, 198, 269, 495, 453, 439, 397,
350, 400** (already cached in the scratchpad as `leafNN.jpg`) to transcribe the actual glyph
forms for the manuscript-transcription project.

---

## Ratification, 2026-08-27 — read by me, not taken on report

The index above was produced by a subagent. Before promoting any gloss from *proposed* to
*verified* I read the two load-bearing plates myself (leaf 33 = p. XXX, leaf 32 = p. XXIX).
Both confirmed the agent's reading. **Nine of sixteen glosses in
`corpus/abbreviation-glosses.json` are now `verified`, up from four.**

### ⛔ Two of my own proposed expansions were WRONG, and Cappelli caught both

| sign | what I had proposed | what Cappelli p. XXX actually gives |
|---|---|---|
| `ł` | "**vel** — 'or'" | **vel, ul…, …el** — crossing an `l`'s ascender mid-word it may simply supply *ul* or *el*. My flat rule was wrong. |
| `ꝗ` | "**qui**, sometimes *quod*" | **qui** — ⚠ *with a footnote*: **"Nel sec. VIII lo stesso segno vale *que*"**, and in Anglo-Saxon hands *quam* / *quia*. |

⚠⚠ **The `ꝗ` footnote lands directly on us.** Our witnesses are ninth-century — Eutyches
c. 850–900, Wien 940 c. 800–850 — **sitting on exactly the boundary Cappelli names.** This is
Thompson's period-shift warning (`research/printed-sources.md`) turning up as a concrete
hazard in the very script we teach, not a general caution.

### ⭐ Cappelli names the category the whole design depends on

Section IV, p. XXIX: ***segni abbreviativi con significato relativo*** — abbreviative signs
whose value *"non è più proprio e costante, ma vario a seconda della lettera alla quale detto
segno è sovrapposto o legato"*. He then confirms the rule we had proposed from context alone:
the sign **after `b` gives the ending *bus*** (*quib;* = quibus), **after `q` gives *que***.

⚑ So the context-dependence is not an awkwardness of our corpus; it is a documented class in
the standard dictionary. **An abbreviation table can never be a flat character map** — the
`abbreviation_type` field and the period bounds both earn their place here.

### The one sign Cappelli does not have, and why that is right

**`ę` (e caudata) — UNLOCATED, correctly.** The agent checked the Avvertenza, the whole
brachigrafia treatise and the *Segni Convenzionali* appendix and found nothing. That is the
expected result: **e caudata is not an abbreviation at all but an orthographic variant**, a way
of writing *ae*, and Cappelli catalogues abbreviation signs. Our own gloss already says exactly
this. An absence that matches the reasoning is a confirmation, not a gap.

### Still `proposed` (7 of 16)

`ũ ã õ ĩ` (the nasal bar on individual vowels — the general rule is verified at Cappelli
p. XXIV; the per-vowel rows are mechanical from it), `ͣ` (superscript vowel — Cappelli p. XXXI
and p. 304 for *quasi* itself, indexed but not yet read by me), `ꝵ` (*-rum*), and `ę`.
