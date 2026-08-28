#!/usr/bin/env python3
"""Publish the script primers as pages -> site/hand/<profile>/index.html.

⚑ Why this exists. Two carefully-built reference documents sat in `scripts/` where no
learner could reach them, while `registry/` carried a `primer` field that nothing read --
a promise the product did not keep. Either publish them or drop the field; this publishes.

A primer documents a SCRIPT, so the field lives on the profile: both Latin tracks share
Caroline's, and every future vernacular track shares the Gothic one.

The renderer is deliberately small and local. This repo carries no dependencies (see
research/deploy.md on what a stray package.json cost), and the primers use a known, closed
set of Markdown: headings, paragraphs, tables, bullets, fences, bold, italic, code, links,
and horizontal rules. Anything outside that set is passed through escaped rather than
guessed at.

Usage:  python3 tools/make_primers.py
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry

ROOT = Path(__file__).resolve().parent.parent


def inline(s):
    """Escape first, then re-introduce only the inline markup we allow."""
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" rel="noopener">\1</a>', s)
    s = re.sub(r"&lt;(https?://[^&\s]+)&gt;", r'<a href="\1" rel="noopener">\1</a>', s)
    return s


def render(md):
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):                       # fenced block
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i])); i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>"); i += 1
        elif ln.startswith("|"):                       # table
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            cells = [c for c in cells if not all(set(x) <= set("-: ") for x in c)]
            head, body = cells[0], cells[1:]
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for r in body:
                t += ["<tr>"] + [f"<td>{inline(c)}</td>" for c in r] + ["</tr>"]
            out.append("".join(t + ["</tbody></table>"]))
        elif re.match(r"^[-*] ", ln):                  # bullets
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                items.append(inline(lines[i][2:])); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
        elif re.match(r"^\d+\. ", ln):                 # numbered
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(inline(re.sub(r"^\d+\. ", "", lines[i]))); i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>")
        elif ln.startswith("#"):
            n = len(ln) - len(ln.lstrip("#"))
            out.append(f"<h{min(n,4)}>{inline(ln[n:].strip())}</h{min(n,4)}>"); i += 1
        elif ln.strip() in ("---", "***"):
            out.append("<hr>"); i += 1
        elif not ln.strip():
            i += 1
        else:                                          # paragraph
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||```|[-*] |\d+\. )", lines[i]) \
                    and lines[i].strip() not in ("---", "***"):
                buf.append(lines[i].strip()); i += 1
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{title} — Paleography">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://paleography.app/hand/{pid}">
<meta property="og:image" content="https://paleography.app/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><text y='.9em' font-size='56'>%E2%9C%92%EF%B8%8F</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400&family=IBM+Plex+Sans:wght@400;500;600&family=Noto+Serif:wght@400&display=swap">
<title>{title} — Paleography</title>
<style>
:root{{--ink:#14120F;--surface:#1E1B17;--raised:#2A2621;--line:#3A342D;
 --text:#EAE4DA;--muted:#A0958A;--dim:#7B7168;--accent:#5B82BE;--accent-soft:#2F415E;
 --serif:"EB Garamond",Georgia,serif;--sans:"IBM Plex Sans",-apple-system,sans-serif;
 --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--r:3px}}
:root[data-theme="light"]{{--ink:#F2EEE7;--surface:#FBF9F5;--raised:#FFF;--line:#DED7CB;
 --text:#211E19;--muted:#5F574C;--dim:#857C70;--accent:#2E4B7A;--accent-soft:#DDE5F1}}
@media (prefers-color-scheme:light){{:root:not([data-theme="dark"]){{
 --ink:#F2EEE7;--surface:#FBF9F5;--raised:#FFF;--line:#DED7CB;
 --text:#211E19;--muted:#5F574C;--dim:#857C70;--accent:#2E4B7A;--accent-soft:#DDE5F1}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ink);color:var(--text);font-family:var(--sans);
 font-size:17px;line-height:1.66;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:760px;margin:0 auto;padding:28px 22px 80px}}
header{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;
 padding-bottom:18px;border-bottom:1px solid var(--line);margin-bottom:30px}}
h1.wm{{font-family:var(--serif);font-size:27px;font-weight:400;margin:0}}
h1.wm a{{color:var(--text);text-decoration:none}}
.spacer{{flex:1}}
header a.nav{{color:var(--muted);text-decoration:none;font-size:15px}}
header a.nav:hover{{color:var(--text)}}
h1{{font-family:var(--serif);font-weight:400;font-size:36px;line-height:1.2;margin:0 0 6px}}
h2{{font-family:var(--serif);font-weight:400;font-size:25px;margin:38px 0 10px;
 padding-top:16px;border-top:1px solid var(--line)}}
h3{{font-family:var(--serif);font-weight:400;font-size:20px;margin:26px 0 8px;color:var(--text)}}
h4{{font-size:15px;margin:20px 0 6px;color:var(--muted)}}
p{{margin:0 0 14px}}
em{{color:var(--muted)}}
strong{{font-weight:600}}
code{{font-family:var(--mono);font-size:14.5px;background:var(--surface);
 border:1px solid var(--line);border-radius:var(--r);padding:1px 5px}}
pre{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
 padding:14px;overflow-x:auto}}
pre code{{border:0;background:none;padding:0}}
a{{color:var(--accent)}}
hr{{border:0;border-top:1px solid var(--line);margin:26px 0}}
ul,ol{{margin:0 0 14px;padding-left:22px}}
li{{margin:5px 0}}
.tablewrap{{overflow-x:auto;margin:0 0 18px}}
table{{border-collapse:collapse;width:100%;font-size:15.5px}}
th,td{{text-align:left;padding:7px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{color:var(--muted);font-weight:500;font-size:13px;text-transform:uppercase;
 letter-spacing:.05em}}
tbody tr:last-child td{{border-bottom:0}}
.backline{{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);
 font-size:15px;color:var(--muted)}}
.backline a{{color:var(--accent)}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1 class="wm"><a href="/">Paleography</a></h1>
  <div class="spacer"></div>
  <a class="nav" href="/about">about</a>
</header>
{body}
<p class="backline">{back}</p>
</div>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""


def main():
    languages, profiles, tracks = registry.load()
    # which tracks each profile serves, so a primer can link to its own practice
    serves = {}
    for t in registry.ordered_tracks(languages, tracks):
        serves.setdefault(t["profile"]["id"], []).append(t)

    made = []
    for pid, prof in sorted(profiles.items()):
        rel = prof.get("primer", "")
        if not rel:
            print(f"  {pid}: no primer declared — skipped")
            continue
        src = ROOT / rel
        if not src.exists():
            raise SystemExit(f"FATAL {pid}: primer {rel} does not exist")
        md = src.read_text(encoding="utf-8")
        body = render(md)
        body = body.replace("<table>", '<div class="tablewrap"><table>').replace(
            "</table>", "</table></div>")

        links = " · ".join(f'<a href="{t["route"]}">{t["name"]}</a>' for t in serves.get(pid, []))
        back = (f"Practise this hand: {links}" if links else "No track uses this profile yet.")
        title = prof["name"]
        # first italic paragraph of the primer is its standfirst; use a plain summary instead
        desc = (f"A reader's primer on {title.lower()} — what trips you, what the page looks "
                f"like, and the abbreviation system, counted over real ground truth.")
        dest = ROOT / "site/hand" / pid / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(PAGE.format(title=html.escape(title), desc=html.escape(desc),
                                    pid=pid, body=body, back=back), encoding="utf-8")
        made.append((pid, dest.stat().st_size))
        print(f"  {pid:18} -> site/hand/{pid}/index.html  {dest.stat().st_size/1024:.0f} KB")
    if not made:
        raise SystemExit("FATAL no primers published")


if __name__ == "__main__":
    main()
