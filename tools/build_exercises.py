#!/usr/bin/env python3
"""Select and package line exercises into one self-contained JSON payload.

Level 3 (line transcription) only. Levels 1-2 (glyph cards, abbreviation cards) need
word- or glyph-level boxes, and the seed ALTO carries exactly one <String> per line --
see corpus/EXERCISE-NOTES.md.

Ordering is by length, shortest first: the nearest thing to a difficulty curve that
the data supports without a learner model to weight it.
"""
import json, base64, argparse, statistics
from pathlib import Path
from io import BytesIO
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def pack(manifest_dir, n, max_w, quality, track, witness_meta):
    rows = [json.loads(l) for l in open(Path(manifest_dir) / "manifest.jsonl", encoding="utf-8")]
    rows.sort(key=lambda r: len(r["text"]))
    step = max(1, len(rows) // n)
    picked = rows[::step][:n]
    out = []
    for r in picked:
        p = Path(manifest_dir) / r["image"]
        im = Image.open(p).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, max(1, int(im.height * max_w / im.width))), Image.LANCZOS)
        buf = BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True)
        out.append(dict(id=r["image"].rsplit(".", 1)[0][-12:], track=track,
                        text=r["text"], layer=r["layer"], witness=r["witness"],
                        page=r["page"], w=im.width, h=im.height,
                        img=base64.b64encode(buf.getvalue()).decode()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--max-w", type=int, default=900)
    ap.add_argument("--quality", type=int, default=68)
    a = ap.parse_args()
    data = {"tracks": {}, "built": "2026-08-27"}
    specs = [("latin", "corpus/crops/eutyches-VLO41",
              dict(name="Latin — Caroline minuscule",
                   witness="Leiden, Voss. Lat. O. 41 (s. IX ex.)",
                   layer="diplomatic",
                   note="Abbreviations are preserved as signs. Type what is on the page.")),
             ("greek", "corpus/crops/cpgr23",
              dict(name="Greek — Byzantine minuscule",
                   witness="Heidelberg, Pal. gr. 23 (s. X)",
                   layer="expanded",
                   note="Abbreviations are already expanded in this transcription; final sigma is never used (always σ).")),
             ]
    for track, d, meta in specs:
        items = pack(d, a.n, a.max_w, a.quality, track, meta)
        data["tracks"][track] = dict(meta=meta, items=items)
        kb = sum(len(i["img"]) for i in items) / 1024
        print(f"  {track:6} {len(items):3} lines  {kb/1024:.2f} MB b64  "
              f"median chars={statistics.median(len(i['text']) for i in items):.0f}")
    Path(a.out).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"-> {a.out}  {Path(a.out).stat().st_size/1024/1024:.2f} MB")
