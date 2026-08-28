#!/usr/bin/env python3
"""Wrap the trainer as a STANDALONE page at /read/ on paleography.app.

The apex is a hand-written landing page (site/index.html, tracked in git); this generates
only the trainer. Clean per-track URLs are rewrites in site/vercel.json.

The Artifact runtime supplies <!doctype>, <head> and <body> at publish time, so the shell
deliberately has none. Served raw by a web host that is a bug, not a saving: without a
doctype the browser falls into quirks mode (a different box model), and without a viewport
meta the page renders at desktop width on a phone.
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
inner = (root / "build/scriptorium.html").read_text(encoding="utf-8")

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Learn to read Caroline minuscule and Byzantine Greek minuscule from the manuscripts themselves — staged from orientation to full transcription.">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="Paleography">
<meta property="og:description" content="A staged introduction to reading Greek and Latin manuscripts, built on open ground truth.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://paleography.app/read/">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><text y='.9em' font-size='56'>%E2%9C%92%EF%B8%8F</text></svg>">
"""
# Vercel Web Analytics (static-site install); the Artifact build never sees this footer
FOOT = '\n<script defer src="/_vercel/insights/script.js"></script>\n</body>\n</html>\n'

# the shell opens with <title> and its font links; those belong in <head>, the rest in <body>
marker = '<div class="wrap">'
i = inner.index(marker)
head_part, body_part = inner[:i], inner[i:]
out = HEAD + head_part + "</head>\n<body>\n" + body_part + FOOT
dest = root / "site/read/index.html"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(out, encoding="utf-8")
print(f"{dest} — {dest.stat().st_size/1024/1024:.2f} MB")
