#!/usr/bin/env python3
"""Read registry/ -- the single source of truth for languages, profiles and tracks.

The shape, from EXPANSION-PLAN.md §1:

    Language   the learner's door   (its own URL, primer, expert seat, progress)
      Track    one witness          (bound to exactly one profile, one layer)
    Profile    the machinery        (direction, scorer, folding, keymap, palette)

A learner arrives with a LANGUAGE prior; the corpus is organised by SCRIPT. Neither
axis works alone, so both are first-class and a track is where they meet.

TOML, read with stdlib `tomllib` -- this repo deliberately carries no dependencies
(see research/deploy.md on why a stray package.json is actively harmful here).
"""
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "registry"


class RegistryError(Exception):
    """Raised for a registry that parses but does not cohere."""


def _load_dir(d):
    out = {}
    for p in sorted(d.glob("*.toml")):
        with open(p, "rb") as fh:
            data = tomllib.load(fh)
        if data.get("id") != p.stem:
            raise RegistryError(f"{p.name}: id={data.get('id')!r} must match the filename stem")
        out[data["id"]] = data
    return out


def load():
    """Return (languages, profiles, tracks) with every cross-reference resolved.

    `tracks` is a flat id -> track dict, each track carrying a resolved `profile`
    object and its owning `language` id. Track ids are unique ACROSS languages
    because they are the payload keys and the progress-store keys.
    """
    profiles = _load_dir(REG / "profiles")
    languages = _load_dir(REG / "languages")
    if not profiles or not languages:
        raise RegistryError(f"registry is empty at {REG}")

    tracks = {}
    for lang in languages.values():
        pid = lang.get("profile")
        if pid not in profiles:
            raise RegistryError(f"language {lang['id']}: unknown profile {pid!r}")
        for t in lang.get("tracks", []):
            if t["id"] in tracks:
                raise RegistryError(
                    f"duplicate track id {t['id']!r} "
                    f"({tracks[t['id']]['language']} and {lang['id']}) -- "
                    "track ids are payload and progress keys and must be globally unique"
                )
            missing = [k for k in ("id", "tab", "route", "name", "witness",
                                  "crops", "layer", "printed") if k not in t]
            if missing:
                raise RegistryError(
                    f"track {t.get('id', '?')!r} in {lang['id']}: missing {', '.join(missing)}")
            t = dict(t)
            t["language"] = lang["id"]
            t["profile"] = profiles[pid]
            crops = ROOT / t["crops"]
            if not (crops / "manifest.jsonl").exists():
                raise RegistryError(
                    f"track {t['id']}: no manifest at {crops}/manifest.jsonl -- "
                    "run tools/crop.py for this witness first"
                )
            tracks[t["id"]] = t
    return languages, profiles, tracks


def ordered_tracks(languages, tracks):
    """Tracks in registry order: languages by file, tracks within a language by list.

    Order is not cosmetic -- it fixes the order of the payload and therefore the tab
    order in the trainer, so it must be deterministic rather than dict-insertion luck.
    """
    out = []
    for lang in sorted(languages.values(), key=lambda l: (l.get("order", 999), l["id"])):
        for t in lang.get("tracks", []):
            out.append(tracks[t["id"]])
    return out


if __name__ == "__main__":
    langs, profs, trs = load()
    print(f"{len(langs)} languages, {len(profs)} profiles, {len(trs)} tracks")
    for t in ordered_tracks(langs, trs):
        print(f"  {t['language']:8} {t['id']:8} {t['profile']['id']:16} "
              f"{t['layer']:11} {t['route']}")
