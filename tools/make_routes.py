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
ATTEMPTS = ROOT / "site/api/attempts.js"
LANDING = ROOT / "site/index.html"
L_BEGIN = "<!-- BEGIN GENERATED TRACK CARDS (tools/make_routes.py; do not edit by hand) -->"
L_END = "<!-- END GENERATED TRACK CARDS -->"
P_BEGIN = "<!-- BEGIN GENERATED PRIMERS -->"
P_END = "<!-- END GENERATED PRIMERS -->"
BEGIN = "// --- BEGIN GENERATED TRACKS (tools/make_routes.py; do not edit by hand) ---"
END = "// --- END GENERATED TRACKS ---"


def build():
    languages, profiles, tracks = registry.load()
    cfg = json.loads(DEST.read_text(encoding="utf-8"))

    # Primer pages: /hand/<profile> -> site/hand/<profile>/index.html
    primer_routes = [{"source": f"/hand/{pid}", "destination": f"/hand/{pid}/index.html"}
                     for pid, prof in sorted(profiles.items()) if prof.get("primer")]

    track_routes = []
    for t in registry.ordered_tracks(languages, tracks):
        track_routes.append({
            "source": t["route"],
            "destination": f"/read/index.html?track={t['id']}",
        })

    # Keep every rewrite this script does not own, in its original order.
    owned = {t["route"] for t in registry.ordered_tracks(languages, tracks)}
    kept = [r for r in cfg.get("rewrites", []) if r["source"] not in owned]
    owned_primers = {r["source"] for r in primer_routes}
    kept = [r for r in kept if r["source"] not in owned_primers]
    cfg["rewrites"] = track_routes + primer_routes + kept
    return cfg


def build_tracks():
    """The track allowlist the /api/attempts validator checks against.

    That endpoint is public and treats every body as hostile, so it needs to know which
    track ids are real. It ran on a hardcoded Set -- a third copy of the track list, and
    the one whose drift is worst: a new language's attempts are silently dropped, and
    nothing logs it, because dropping unknown fields is the endpoint's whole job.
    """
    languages, profiles, tracks = registry.load()
    ids = [t["id"] for t in registry.ordered_tracks(languages, tracks)]
    src = ATTEMPTS.read_text(encoding="utf-8")
    i, j = src.index(BEGIN), src.index(END)
    listing = ", ".join(json.dumps(x) for x in ids)
    block = f"{BEGIN}\nconst TRACKS = new Set([{listing}]);\n"
    return ids, src[:i] + block + src[j:]


def build_landing():
    """The 'Choose a hand' cards on the apex, generated from the registry.

    ⛔ ONLY the cards, between the markers. Everything else on that page -- the lede, the
    stage list, the attributions, the licence note -- is hand-written prose and is left
    exactly as it is.

    The card copy lives in registry/languages/*.toml (card_chip, card_witness,
    card_blurb) and is deliberately NOT the same text as `printed`: that paragraph
    orients a reader who has already chosen a track, this one has to make them choose.
    """
    languages, profiles, tracks = registry.load()
    rows = []
    for t in registry.ordered_tracks(languages, tracks):
        name = t.get("card_name_html") or t["name"]
        rows.append(
            f'  <a class="track" href="{t["route"]}">\n'
            f'    <div class="chip">{t["card_chip"]}</div>\n'
            f'    <div class="n">{name}</div>\n'
            f'    <div class="w">{t["card_witness"]}</div>\n'
            f'    <div class="d">{t["card_blurb"]}</div>\n'
            f'    <div class="go">Begin →</div>\n'
            f'  </a>'
        )
    block = L_BEGIN + "\n" + "\n\n".join(rows) + "\n" + L_END
    src = LANDING.read_text(encoding="utf-8")
    i, j = src.index(L_BEGIN), src.index(L_END) + len(L_END)
    src = src[:i] + block + src[j:]

    # Primer links. Generated for the same reason as the cards: a hand-kept list is one a
    # new script silently misses. Ordered as the languages are, so the page reads top-down.
    seen, plinks = set(), []
    for t in registry.ordered_tracks(languages, tracks):
        pid = t["profile"]["id"]
        if pid in seen or not t["profile"].get("primer"):
            continue
        seen.add(pid)
        plinks.append(f'  <p class="navline"><a href="/hand/{pid}">'
                      f'A reader\'s primer on {t["profile"]["name"].lower()} →</a></p>')
    pblock = P_BEGIN + "\n" + "\n".join(plinks) + "\n" + P_END
    i, j = src.index(P_BEGIN), src.index(P_END) + len(P_END)
    return src[:i] + pblock + src[j:]


if __name__ == "__main__":
    cfg = build()
    new = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
    old = DEST.read_text(encoding="utf-8")
    ids, new_attempts = build_tracks()
    old_attempts = ATTEMPTS.read_text(encoding="utf-8")
    new_landing = build_landing()
    old_landing = LANDING.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        if new_landing != old_landing:
            print(f"STALE  {LANDING} track cards do not match the registry")
            sys.exit(1)
        if new_attempts != old_attempts:
            print(f"STALE  {ATTEMPTS} track allowlist does not match the registry")
            sys.exit(1)
        if new != old:
            print(f"STALE  {DEST} does not match the registry; run: python3 tools/make_routes.py")
            sys.exit(1)
        print(f"ok     {DEST} matches the registry")
    else:
        LANDING.write_text(new_landing, encoding="utf-8")
        print(f"{LANDING} — {len(ids)} track cards")
        ATTEMPTS.write_text(new_attempts, encoding="utf-8")
        print(f"{ATTEMPTS} — allowlist {', '.join(ids)}")
        DEST.write_text(new, encoding="utf-8")
        n = len(cfg["rewrites"])
        print(f"{DEST} — {n} rewrites")
        for r in cfg["rewrites"]:
            print(f"  {r['source']:12} -> {r['destination']}")
