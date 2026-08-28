#!/usr/bin/env python3
"""Generate site/vercel.json from the registry.

Routes were hand-written in two places -- registry/languages/*.toml (which the trainer
reads to resolve /greek to a track) and site/vercel.json (which makes /greek reach the
trainer at all). Two hand-maintained copies of the same fact drift, and the failure is
silent: the rewrite 404s, or worse, lands on the trainer with a track it cannot find.

⛔ Everything else in vercel.json is hand-maintained and PRESERVED here -- headers, the
keepalive cron, the /about and /read rewrites. This script only owns the per-track
rewrites, between the two marker comments. Do not turn it into a full generator: the
cron schedule and the cache headers are decisions, not derivations.

⚑ The rewrites point at /read/index.html?track=<id>. That query is only ever visible
server-side, because a Vercel REWRITE leaves the browser's URL as typed -- which is why
the trainer resolves its track from the PATH and treats ?track= as a fallback.

Usage:  python3 tools/make_routes.py [--check]
        --check exits non-zero if the file on disk is stale, for use in a build.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "site/vercel.json"


def build():
    languages, profiles, tracks = registry.load()
    cfg = json.loads(DEST.read_text(encoding="utf-8"))

    track_routes = []
    for t in registry.ordered_tracks(languages, tracks):
        track_routes.append({
            "source": t["route"],
            "destination": f"/read/index.html?track={t['id']}",
        })

    # Keep every rewrite this script does not own, in its original order.
    owned = {t["route"] for t in registry.ordered_tracks(languages, tracks)}
    kept = [r for r in cfg.get("rewrites", []) if r["source"] not in owned]
    cfg["rewrites"] = track_routes + kept
    return cfg


if __name__ == "__main__":
    cfg = build()
    new = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
    old = DEST.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        if new != old:
            print(f"STALE  {DEST} does not match the registry; run: python3 tools/make_routes.py")
            sys.exit(1)
        print(f"ok     {DEST} matches the registry")
    else:
        DEST.write_text(new, encoding="utf-8")
        n = len(cfg["rewrites"])
        print(f"{DEST} — {n} rewrites")
        for r in cfg["rewrites"]:
            print(f"  {r['source']:12} -> {r['destination']}")
