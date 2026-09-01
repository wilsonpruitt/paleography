#!/usr/bin/env python3
"""Cross-check every GT source's licence against what its repository actually says.

Why this exists: a repository can declare TWO different licences, and it has happened
three times on this project (INGEST-NOTES §12). The catalogue field, the LICENSE file
and the host's own detection are three independent claims and they do not always agree.
This asks all three and shouts when they diverge.

    python3 tools/licence_check.py           # check every source with a URL
    python3 tools/licence_check.py --id wien940
    python3 tools/licence_check.py --check   # exit 1 if any source DISAGREES or is unresolved

stdlib only, per the house rule. Uses `gh api` when available (auth + rate limits),
falling back to anonymous HTTPS.
"""
import argparse, json, re, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "corpus" / "sources.yml"

# Enough SPDX ids to cover open-GT practice. Order matters: longest first, so that
# BY-SA / BY-NC are never swallowed by a bare BY match.
SPDX = [
    ("CC-BY-NC-SA-4.0", r"cc[-_ ]?by[-_ ]?nc[-_ ]?sa[-_ ]?4"),
    ("CC-BY-NC-4.0",    r"cc[-_ ]?by[-_ ]?nc[-_ ]?4"),
    ("CC-BY-SA-4.0",    r"cc[-_ ]?by[-_ ]?sa[-_ ]?4|attribution[-_ ]sharealike 4"),
    ("CC-BY-4.0",       r"cc[-_ ]?by[-_ ]?4|creative commons attribution 4"),
    ("CC0-1.0",         r"cc0[-_ ]?1|public domain dedication"),
    ("MIT",             r"\bmit license\b"),
    ("Apache-2.0",      r"apache license.{0,40}version 2"),
]

def spdx(text):
    """First SPDX id the text asserts, or None. Longest-first so BY-SA beats BY."""
    if not text:
        return None
    low = text.lower()
    for name, pat in SPDX:
        if re.search(pat, low):
            return name
    return None


def gh_api(path):
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=30)
        if out.returncode == 0:
            return json.loads(out.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return None


def fetch(url, limit=8000):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "paleography-licence-check"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read(limit).decode("utf-8", "replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def parse_sources(path):
    """Tiny line scanner — sources.yml is hand-written and PyYAML is not a dependency here."""
    entries, cur = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = re.match(r"^-\s+id:\s*(\S+)", line)
        if m:
            if cur:
                entries.append(cur)
            cur = {"id": m.group(1), "license": None, "url": None}
            continue
        if cur is None:
            continue
        m = re.match(r"^license:\s*(.+)$", line)
        if m and cur["license"] is None:
            cur["license"] = m.group(1).strip()
        m = re.match(r"^url:\s*(\S+)", line)
        if m and cur["url"] is None:
            cur["url"] = m.group(1)
    if cur:
        entries.append(cur)
    return entries


def claims_for(url):
    """Three independent claims about one repository: host detection, LICENSE file, self-declaration."""
    claims = {}
    m = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", url)
    if m:
        owner, repo = m.group(1), m.group(2).removesuffix(".git")
        meta = gh_api(f"repos/{owner}/{repo}")
        if meta is not None:
            lic = (meta.get("license") or {}).get("spdx_id")
            if lic and lic != "NOASSERTION":
                claims["host detection"] = lic
        branch = (meta or {}).get("default_branch") or "master"
        raws = [f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"]
    elif re.match(r"https://gitlab\.[^/]+/", url):
        # Self-hosted GitLab (huma-num) — no licence detection API worth trusting
        # anonymously, so read the files. Default branch is not knowable up front, and
        # for htr_cpgr23 it is `master` while `main` 404s, so try both.
        base = url.rstrip("/")
        raws = [f"{base}/-/raw/{b}" for b in ("main", "master")]
    else:
        return None, f"unrecognised host — check by hand ({url})"

    for raw in raws:
        for fn in ("LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md", "COPYING"):
            body = fetch(f"{raw}/{fn}")
            if body:
                got = spdx(body)
                if got:
                    claims[f"{fn}"] = got
                break
        if len(claims) > (1 if "host detection" in claims else 0):
            break

    # The dataset's own metadata — HTR-United's manifest. ⚠ Often a NESTED block.
    for raw in raws:
      for fn in ("htr-united.yml", "htr_united.yml", ".htr-united.yml"):
        body = fetch(f"{raw}/{fn}")
        if body:
            lines = body.splitlines()
            for i, line in enumerate(lines):
                if re.match(r"\s*licen[cs]e\s*:", line, re.I):
                    # ⚠ The declaration is often a nested block:
                    #     license:
                    #       name: CC-BY 4.0
                    #       url: https://creativecommons.org/licenses/by/4.0/
                    # Reading only the key's own line finds nothing and silently
                    # downgrades a DISAGREE to a STALE. Take the key plus 3 lines.
                    got = spdx(" ".join(lines[i:i + 4]))
                    if got:
                        claims[fn] = got
                        break
            break

    return claims, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", help="check one source only")
    ap.add_argument("--check", action="store_true", help="exit 1 on any disagreement")
    args = ap.parse_args()

    entries = parse_sources(SOURCES)
    if args.id:
        entries = [e for e in entries if e["id"] == args.id]
        if not entries:
            sys.exit(f"no source with id {args.id!r}")

    bad = 0
    for e in entries:
        recorded = e["license"] or "(none recorded)"
        print(f"\n{e['id']}  —  sources.yml says: {recorded}")
        if not e["url"]:
            # ⛔ Never skip silently. Three Eutyches entries carried a wrong licence for
            # months precisely because they had no url and so were never looked at.
            # An unchecked source is a finding, not an absence of one.
            print("  ⚠ UNCHECKED no url recorded — add one, or it is never checked")
            bad += 1
            continue
        claims, skip = claims_for(e["url"])
        if skip:
            print(f"  ⚠ MANUAL   {skip}")
            bad += 1
            continue
        if not claims:
            print("  ⚠ MANUAL   no licence found in the repository at all")
            bad += 1
            continue
        for where, what in claims.items():
            print(f"      {where:20s} {what}")
        distinct = set(claims.values())
        if len(distinct) > 1:
            print(f"  ⛔ DISAGREE  the repository declares {len(distinct)}: {', '.join(sorted(distinct))}")
            print("     → record BOTH in sources.yml as `license: ⚠ CONTESTED` + `license_conflict:`,")
            print("       state the CONSERVATIVE reading on the site, and ask the depositor.")
            bad += 1
        else:
            only = distinct.pop()
            if spdx(recorded) and spdx(recorded) != only:
                print(f"  ⛔ STALE    sources.yml records {spdx(recorded)}, the repository says {only}")
                bad += 1
            else:
                print(f"  ✅ agrees   {only}")

    print()
    if bad:
        print(f"{bad} source(s) need a human.")
    else:
        print("All sources agree with their repositories.")
    if args.check and bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
