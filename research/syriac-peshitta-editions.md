# PD Peshitta editions — the R3 diff targets, pinned

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

## What this does and does not settle

✅ Both Peshitta pieces in Nestle's chrestomathy (23 of its 66 pages) now have a PD printed text
to diff against, so a wrong reading there is **catchable without a Syriacist**.

⛔ It changes nothing for the other 44 pages. *Vitae Prophetarum* (pp. 86-107) and *Historia
inventionis sanctae crucis* (pp. 108-131) have no digital text and no printed critical edition —
Brock's list does not carry them, because they are not Bible. Those pages remain keyed by us and
checkable by nobody but a Syriacist.

⚑ And a diff against a printed edition is **not** a diff against the same text: Nestle prints
his own chrestomathy from his own sources, so a divergence from Barnes or the BFBS is evidence
of an *edition* difference at least as often as of a misreading. The check catches gross error
and pointing slips; it does not adjudicate a variant. Cf. [[reference_junius-tremellius-bible]] —
a repeating offset is versification, not error.
