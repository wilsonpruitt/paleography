#!/usr/bin/env python3
"""Cut a full-resolution plate around one GT line, with its neighbours, for reading by eye.

Deliberately NOT the exercise cropper: no downscale, no masking, and generous context
above and below -- a plate read that cannot see the neighbouring lines cannot tell a
stain from a scribal habit (reference_plate-read-triage).
"""
import json, sys, argparse
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("witness"); ap.add_argument("page"); ap.add_argument("line_id")
    ap.add_argument("--out", required=True)
    ap.add_argument("--context-lines", type=float, default=1.6)
    ap.add_argument("--image-root", default="corpus/raw/eutyches")
    a = ap.parse_args()

    rows = [json.loads(l) for l in
            open(f"corpus/normalized/{a.witness}.jsonl", encoding="utf-8")]
    pg = [r for r in rows if r["page"] == a.page]
    tgt = [r for r in pg if r["line_id"] == a.line_id]
    if not tgt:
        sys.exit(f"no line {a.line_id} on {a.page}")
    t = tgt[0]
    import statistics
    ys = sorted(statistics.median(y for _, y in r["baseline"]) for r in pg if r.get("baseline"))
    gaps = [b - a2 for a2, b in zip(ys, ys[1:]) if 5 < b - a2 < 400]
    lh = statistics.median(gaps) if len(gaps) >= 3 else 40.0

    xs = [x for x, _ in t["polygon"]]; pys = [y for _, y in t["polygon"]]
    pad_x = int(lh * 1.2); pad_y = int(lh * a.context_lines)
    p = [q for q in Path(a.image_root).rglob(a.page)]
    if not p:
        sys.exit(f"image {a.page} not found under {a.image_root}")
    img = Image.open(p[0]).convert("RGB")
    box = (max(min(xs) - pad_x, 0), max(min(pys) - pad_y, 0),
           min(max(xs) + pad_x, img.width), min(max(pys) + pad_y, img.height))
    crop = img.crop(box)
    crop.save(a.out, quality=95)
    print(f"{a.out}  {crop.size}  lh={lh:.1f}  page={img.size}")
    print(f"  text: {t['text']}")


if __name__ == "__main__":
    main()
