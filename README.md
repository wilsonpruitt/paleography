# Paleography

⛔ **Starting a session? Read [`NEXT-SESSION.md`](NEXT-SESSION.md) first** — current state, the front, and the rules this project paid for.

Teaching readers of Greek, Latin and Old French to read the manuscripts — and, later, training
script-specific HTR models on the same corpus.

**Start with [`PLAN.md`](PLAN.md).** It carries the first principles, the schema, the
phases and Wilson's rulings.

## Where things are

| path | what |
|---|---|
| `PLAN.md` | the score: first principles, data model, phases, rulings |
| `research/landscape-2026-08.md` | survey of what already exists (Aug 2026) |
| `scripts/caroline-minuscule.md` | **primer — Latin track**, readable start-to-finish |
| `scripts/greek-minuscule.md` | **primer — Greek track** |
| `corpus/sources.yml` | seed dataset registry, with declared transcription layer |
| `corpus/INGEST-NOTES.md` | ⛔ **read before touching ingest** — eight real traps |
| `corpus/latin-abbreviations.json` | abbreviation inventory, verified vs proposed |
| `tools/ingest.py` | ALTO v4 / PAGE XML / TEI-facsimile → canonical JSONL |
| `tools/fetch-seeds.sh` | re-fetch + re-ingest the whole seed corpus (idempotent) |
| `tools/export_page.py` | canonical JSONL → **PAGE XML 2019-07-15** (eScriptorium / Transkribus / Kraken) |
| `tools/roundtrip_check.py` | export → re-import → compare; proves nothing is lost |
| `tools/export-all.sh` | export every witness and verify all of them |
| `tools/crop.py` · `build_exercises.py` · `make_routes.py` · `make_site.py` | line crops → exercise bank → routes → the trainer page |
| `tools/plate.py` | full-resolution plate around one line, for reading by eye |

## Getting the corpus

```sh
./tools/fetch-seeds.sh      # ~2.1 GB of clones, gitignored; writes corpus/normalized/*.jsonl
```

**Corpus state:** 27,183 lines of ground truth across 9 witnesses —
15,480 diplomatic, 11,263 expanded, 440 normalised.

⚠ **Not all CC-BY 4.0**, as this line used to claim. Eutyches, ecrinum/anthologia and the
CIHAM *Fabliaux* are CC BY 4.0. The two HTR Winter School Vienna datasets — Cod. 940
(Latin I) and Cod. Syr. 1 (Syriac) — ship a **CC BY-SA 4.0** licence file alongside a
catalogue entry that says CC BY 4.0, and the site states the stricter reading until the
school resolves it. See `corpus/sources.yml` → `license_conflict`.

## The one rule

**Never take a dataset's transcription layer from its catalogue entry.** Read the
dataset's own documentation, then verify with a character probe. The catalogue was
wrong about this once already, in the direction that silently corrupts everything
downstream. `corpus/INGEST-NOTES.md` §1.
