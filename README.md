# Paleography

Teaching readers of Greek and Latin to read the manuscripts — and, later, training
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

## Getting the corpus

```sh
./tools/fetch-seeds.sh      # ~2.1 GB of clones, gitignored; writes corpus/normalized/*.jsonl
```

**Phase 1 state:** 24,017 lines of ground truth across 7 witnesses —
20,203 diplomatic, 3,374 expanded, 440 normalised. All CC-BY 4.0.

## The one rule

**Never take a dataset's transcription layer from its catalogue entry.** Read the
dataset's own documentation, then verify with a character probe. The catalogue was
wrong about this once already, in the direction that silently corrupts everything
downstream. `corpus/INGEST-NOTES.md` §1.
