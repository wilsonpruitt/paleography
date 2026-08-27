# Wien, ÖNB, Cod. 940 — IIIF access

Manuscript: Carolingian, Saint-Amand, early 9th c. (ÖNB dates the piece 780–820).
COMMENTARIUS IN MATTHAEUM, olim Salisb. 33, 142 folios, 295×193mm.
Confirmed match via ÖNB's own object record: "Handschrift; 142 Bll.", "295 x 193 mm",
"Leder mit Blindstempeln über Holzdeckeln, Saint-Amand, 8./9. Jhdt.", signature
**"Cod. 940 HAN MAG"**.

## How it was found

manuscripta.at pointed at the ÖNB Gesamtkatalog but the catalogue id it gave
(AL00175429) is an Alma bib record, not the digitisation object — `onb.digital/result/AL00175429`
returns "Element nicht verfügbar". The `iiif.onb.ac.at` (SACHA) `/presentation/collection`
search endpoint accepts a documented JSON body (`{"query":{"localSignature":"...",...}}`)
but returned HTTP 500 for every query tried (localSignature, title, fulltext, idnr) — that
search backend appears broken/unavailable, not a body-shape problem.

The working route was ÖNB Digital's own front-end search API (found via Playwright network
capture): `POST https://onb.digital/Frontend/search_api_search` with form field `keywords`.
Searching `keywords=Cod. 940` returned a "Sammelhandschrift" result (id `10047947`, dated
0780-0820) whose detail page (`onb.digital/result/10047947`) confirms all the physical
description facts above and gives:
- Digitisate link: `https://digital.onb.ac.at/rep/access/open/10047947` (redirects to the
  viewer at `https://viewer.onb.ac.at/10047947`)
- Catalogue link: `https://data.onb.ac.at/rec/AC13958947` (AC13958947 — the real digitisation-linked
  catalogue id; different from the AL00175429 Alma id manuscripta.at surfaced)

Loading the viewer and reading its network requests (Playwright) surfaced the real IIIF
Presentation v3 manifest request directly.

## IIIF Manifest — VERIFIED

```
https://api.onb.ac.at/iiif/presentation/v3/manifest/10047947
```

Fetched directly with curl: HTTP 200, valid IIIF Presentation API v3 JSON.

- `id`: `https://api.onb.ac.at/iiif/presentation/v3/manifest/10047947`
- `type`: `Manifest`
- `label`: "Sammelhandschrift" (ÖNB gives manuscripts a fingiert/generic title, not the
  content title — confirmed elsewhere in the record as "Titel fingiert")
- **Canvas count: 290** (not exactly 284 = 142×2; ÖNB imaging apparently includes a few
  extra shots — covers, flyleaves, color bars, etc. — beyond strict recto/verso of the
  142 numbered leaves)
- Metadata block includes `Signatur: Cod. 940 HAN MAG` (linked to
  `https://data.onb.ac.at/rec/AC13958947`), `Barcode: +Z134327601`, `IDNR: AC13958947`,
  `Umfang: Handschrift; 142 Bll.`, `Format/Maße: 295 x 193 mm`.
- `seeAlso`: catalogue record (AC13958947) and a PDF-service endpoint
  (`https://pdf-service.onb.ac.at/10047947`).

## Image service — VERIFIED

Base pattern per canvas:
```
https://api.onb.ac.at/iiif/image/v3/10047947/{imageID}
```
`{imageID}` is a per-page opaque token from the manifest (e.g. canvas 1's is
`uk4nGb4kQHe3msbC`), NOT sequential — always read it out of the manifest, don't guess it.

Verified working example (canvas 1, first folio image):
- `info.json`: `https://api.onb.ac.at/iiif/image/v3/10047947/uk4nGb4kQHe3msbC/info.json`
  → HTTP 200, IIIF Image API v3, level2 profile, full size **1320×2035**.
- Full image: `https://api.onb.ac.at/iiif/image/v3/10047947/uk4nGb4kQHe3msbC/full/max/0/default.jpg`
  → HTTP 200, `image/jpeg`, confirmed via `file` as a real 1320×2035 JPEG (476 KB).
- Region crop: `https://api.onb.ac.at/iiif/image/v3/10047947/uk4nGb4kQHe3msbC/100,100,500,300/full/0/default.jpg`
  → HTTP 200, confirmed via `file` as a real 500×300 JPEG.

### How to fetch an arbitrary line/region crop

```
https://api.onb.ac.at/iiif/image/v3/10047947/{imageID}/{x},{y},{w},{h}/full/0/default.jpg
```
- `{x},{y},{w},{h}` — pixel region in the full-resolution image's coordinate space (get
  full dims from that image's `info.json`, e.g. 1320×2035 for canvas 1).
- `/full/` (size) after the region returns the crop at its native resolution; use
  `/pct:N/` there instead to downscale.
- `/0/` = no rotation; append `default.jpg` (or `.png`/`.tif` per the profile) for format.
- Level2 profile supports arbitrary region + size + rotation per the IIIF Image API 3.0 spec.

## Licence / rights

The manifest carries **no `rights` IRI** (no CC/RS/PD URI) — only a `requiredStatement`:
> label "Bereitgestellt von" / "Attribution" — value "Österreichische Nationalbibliothek" /
> "Austrian National Library"

ÖNB's site-wide usage terms (`https://www.onb.ac.at/nutzung`, fetched and read in full)
state, in the "Lesen / Nutzung von Inhalten" section: ÖNB asserts no copyright exploitation
right of its own in content/digitisations it makes available online, and explicitly
consents to re-use of that content **in the web resolution as delivered** — including on
blogs and social media. Two carve-outs:
1. Third-party rights (if any exist in the underlying content) must still be individually
   cleared by the re-user before any re-use.
2. Scans made by the Google partnership (Austrian Books Online) carry a time-limited
   non-commercial-only restriction — does not apply here (Cod. 940 is a HAN MAG manuscript
   digitisation, not an ABO/Google scan).
ÖNB asks (not requires) an image credit (title, date, description) and a source citation
back to the portal/ÖNB.

Net: web-resolution reuse is ÖNB-cleared with attribution requested, no explicit open
license (CC0/CC-BY) is declared on the manifest itself — treat as "rights-cleared with
attribution," not as a specific SPDX/CC license code, when this needs to go on a plate.

## Routes tried that did NOT pan out

- `iiif.onb.ac.at` SACHA `/presentation/collection` search: correct JSON body shape found
  in the API's own Asciidoctor docs (`{"query":{"<field>":"<value>"}}`), but every field
  tried (localSignature, title, fulltext, idnr) returned HTTP 500 "Something went wrong in
  SACHA server" — a live backend problem, not a request-shape problem.
- `onb.digital/result/AL00175429` (the Alma id manuscripta.at surfaced): HTTP 200 but
  renders "Element nicht verfügbar" — that id is a plain bib record with no attached
  digitisation object under this route.
- `search.onb.ac.at` Primo Quicksearch: reachable (redirects to `primo-explore/search?vid=ONB`)
  but not queried further once the `onb.digital` front-end search API proved faster and
  gave a direct hit.
