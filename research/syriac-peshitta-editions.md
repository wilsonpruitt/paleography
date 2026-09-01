# PD control texts for Nestle's chrestomathy — the R3 diff targets, pinned

*2026-09-01. Opened by Wilson's pointer to Sebastian Brock's bibliography at
`https://syri.ac/brock/bible`, which is the authority for what exists. ⚠ syri.ac serves a
Cloudflare challenge to `curl` and to WebFetch alike; it renders fine in Playwright. Scans then
located on archive.org and **verified at the title page**, never by the identifier
([[reference_archive-org-page-images]]).*

## The problem this closes

Phase 1 found that R3 cannot align, because no *shippable digital* Peshitta exists: the Digital
Syriac Corpus is patristic, SEDRA's analysis is compute-only, and ETCBC/peshitta is OCR of the
**in-copyright Leiden edition** — confirmed by Brock's list as Brill, 1972-1998. The method
therefore inverts: **we key from Nestle and check against a PD printed edition.** These are the
editions to check against.

## Pinned

| Need | Edition | archive.org | verified |
|---|---|---|---|
| **Genesis 1-4** — Chrest. I, Nestle pp. 67-78 | **`PENTATEUCHUS SYRIACE`, post Samuelem Lee recognovit emendavit edidit **Guilelmus Emery Barnes**, adiuv. C. W. Mitchell, J. Pinkerton. Londini, apud Societatem Bibliophilorum Britannicam et Externam, MDCCCCXIV** | `ktavadeauritaauk00lees` (416 leaves) | ✅ title page, n6 |
| **Matthew 5** — Chrest. II, pp. 79-85 · **Lord's Prayer** — p. 70 | **`THE NEW TESTAMENT IN SYRIAC`. London, British and Foreign Bible Society, 1905-1920** | `newtestamentinsy00unse` (372 leaves) | ✅ title page, n6 |
| Gospels, the critical edition behind BFBS 1905 | Pusey & Gwilliam, *Tetraeuangelium sanctum juxta simplicem Syrorum versionem*. Oxonii, Typo. Clarendonianus, 1901 | `tetraeuangeliums00puseuoft` (636 leaves) | ⬜ metadata only |
| Older OT witness, superseded by Barnes | S. Lee, *Vetus Testamentum Syriace*. London, BFBS, 1823 | `VetusTestamentumSyriace` (712 leaves) | ⬜ community upload, **no metadata at all** |

All four are pre-1929 and therefore public domain.

⛔ **The trap, and it is the ID rule again.** Barnes's Pentateuch is catalogued on archive.org
under **Lee**, with a transliterated Syriac title — `ktavadeauritaauk00lees` = *Ktava
de-aurita, aukit amsha sefre de-Musha* ("Book of the Law, that is the five books of Moses").
A search for "Barnes Pentateuchus" does not find it. The identifier names one editor, the title
page names another, and only the title page is right.

⚠ **The 1905 NT's title page says `1905-1920`** — a later printing of the 1905 edition, where
the catalogue record says bare 1905. Same text, but quote the title page when citing it.

## Other PD editions Brock lists, not needed yet

Urmia 1852 (repr. de Qelayta, Trinitarian Bible Society 1913) · Mosul 1887-92, Khayyath & David,
*Biblia sacra juxta versionem simplicem quae dicitur Peschitta*, 3 vols · Barnes, *The Peshitta
Psalter according to the West Syrian Text*, CUP 1904 (`peshittapsaltera00unse`) · de Lagarde,
*Libri Veteris Testamenti Apocryphi Syriace*, 1861 · Ceriani, *Monumenta sacra et profana*, 1868
— which Nestle's own *Litteratura* cites at p. 30, so the chrestomathy and the bibliography point
at the same shelf.

## The non-biblical pieces — and they are NOT uncontrolled

*Added 2026-09-01 on Wilson's pointer to Schermann. The earlier claim here — that 44 of the 66
chrestomathy pages are "checkable by nobody but a Syriacist" — was too pessimistic, twice over.*

### Chrest. IV, *Historia inventionis sanctae crucis* (pp. 108-131) — ⭐ SAME SETTING

**E. Nestle, *De sancta cruce: ein Beitrag zur christlichen Legendengeschichte*. Berlin:
Reuther, 1889** — archive.org **`desanctacruceein0000nest`** (148 leaves; dedication to William
Wright, † 22. 5. 89).

**Nestle lifted chrestomathy IV out of his own book, the same year.** The evidence is not
inference:

- Its section head reads `B. HISTORIA INVENTIONIS SANCTAE [CRUCIS]` and its first sub-head
  `1) e cod. paris. 234.` — **verbatim** what the grammar prints at p. 108.
- The same three recensions in the same order: cod. Paris. 234 · Mus. Brit. Add. 14644 ·
  cod. Vat. syr. 148.
- Both print **unvocalized Serto with marginal line numbers every five lines and the same
  folio/column markers** — `(b, col. 1)`, `(b, col. 2)` occur in the grammar's chrestomathy
  (leaf n201) and on p. 22 of *De sancta cruce* (leaf n33) alike.

So this is a **character-level Syriac diff target**, the only one in the whole phase — and it
comes with Nestle's own corrigenda ("Korrekturen zu meiner Abschrift von B: Z. 148 lies …").
⚑ Which also means it is **not an independent witness**: agreement proves we keyed *Nestle*
correctly, not that Nestle keyed the manuscript correctly. It is a transcription check, not a
textual one — the same distinction as [[feedback_blind-reader-fact-vs-rule]].

### Chrest. III, *Vitae Prophetarum* (pp. 86-107) — sense-level, via Latin

**Th. Schermann, ed., *Prophetarum vitae fabulosae, Indices apostolorum discipulorumque Domini,
Dorotheo, Epiphanio, Hippolyto aliisque vindicata*. Lipsiae: Teubner, 1907** — archive.org
**`prophetarumvita00schegoog`** (339 leaves).

Greek text in five recensions (A-E, pp. 1-104). What matters for us is in the *Capitula*:

- ⭐ **Appendix, p. 105: *Versio latina textus syriaci Epiphanio et Cornelio in cod. Synait.
  syro 10 (saec. IX) attributi*** — a **Latin translation of a SYRIAC witness**, not merely the
  Greek. (Repeated at p. 218 for the apostle-indices.)
- **Index nominum propriorum, p. 240** — the proper-name index, which is the single most
  valuable control here: a *Vitae Prophetarum* is wall-to-wall prophets' and place-names, and
  proper names are exactly where an extractor without the language produces plausible nonsense.

⚠ **This is a sense control, not a diff.** Sinai Syr. 10 is a different witness from Nestle's
three British Museum codices, and a Latin rendering cannot adjudicate Syriac pointing. It
catches a mis-keyed name and a sentence that means nothing; it will never tell you whether a
dot is above or below. ⭐ But it is in **Latin**, which Wilson reads — so for these 22 pages the
check does not wait on the Syriacist seat.

## What this does and does not settle

**Every one of the 66 chrestomathy pages now has some PD control.** The block that was
"checkable by nobody" is gone; what is left is a gradient of how strong each check is:

| Piece | pp. | control | strength |
|---|---|---|---|
| I Genesis 1-4 | 67-78 | Barnes, *Pentateuchus Syriace* 1914 | Syriac ↔ Syriac, **independent** edition |
| II Matthew 5 (+ Lord's Prayer, p. 70) | 79-85 | BFBS NT 1905-1920; Pusey-Gwilliam 1901 | Syriac ↔ Syriac, **independent** edition |
| III *Vitae Prophetarum* | 86-107 | Schermann 1907 — Latin of Sinai Syr. 10 + name index | **sense only**, but readable by Wilson |
| IV *Historia inventionis* | 108-131 | Nestle, *De sancta cruce* 1889 | Syriac ↔ Syriac, but **NOT independent** — same editor, same year |

⚑ Note the two weaknesses are opposite and neither is fatal: III has an independent witness in a
language we can read but no Syriac; IV has the Syriac but no independence.

⚑ And a diff against a printed edition is **not** a diff against the same text: Nestle prints
his own chrestomathy from his own sources, so a divergence from Barnes or the BFBS is evidence
of an *edition* difference at least as often as of a misreading. The check catches gross error
and pointing slips; it does not adjudicate a variant. Cf. [[reference_junius-tremellius-bible]] —
a repeating offset is versification, not error.
