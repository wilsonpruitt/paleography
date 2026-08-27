#!/usr/bin/env python3
"""Cut line images out of page images, using the GT polygons.

Produces the raw material for every learner exercise: one image per line, plus a
manifest carrying the transcription and its declared layer.

Deliberate choices:
  - crop to the polygon's BOUNDING BOX, then optionally white out everything outside
    the polygon. Neighbouring lines' ascenders/descenders intrude into any bounding
    box on a tight-written page; unmasked crops teach the eye to read another line's
    tail as part of this one.
  - `--region` filter, because on a glossed page a random line is a 4-word scrap of
    marginal commentary (INGEST-NOTES section 6).
"""
import json, argparse, math, statistics
from pathlib import Path
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None


def index_images(root):
    return {p.name: p for p in Path(root).rglob("*")
            if p.suffix.lower() in (".jpg", ".jpeg", ".png")}


def page_line_height(rows):
    """Robust line height for a page: median gap between consecutive baselines.

    Preferred over the polygon bbox because source polygons are sometimes
    self-intersecting (an eScriptorium artifact) -- one such spur inflated a
    46px line to a 189px box, and the downscale then crushed it to mush.
    """
    ys = sorted(statistics.median(y for x, y in r["baseline"]) for r in rows if r.get("baseline"))
    gaps = [b - a for a, b in zip(ys, ys[1:]) if 5 < b - a < 400]
    if len(gaps) >= 3:
        return statistics.median(gaps)
    hs = [max(y for x, y in r["polygon"]) - min(y for x, y in r["polygon"])
          for r in rows if r.get("polygon")]
    return statistics.median(hs) if hs else 40.0


def crop_baseline(img, baseline, lh, asc=1.25, desc=0.40, pad=4, deskew=True):
    """Crop a band around the baseline: asc*lh above it, desc*lh below.

    Rotates FIRST, then bands. Doing it the other way adds the baseline's own tilt to
    the band height -- on a tilted line that turned a 46px line into a 133px crop
    carrying the neighbouring lines with it.

    Robust to malformed polygons (self-intersecting spurs are a real eScriptorium
    artifact here), and gives every line a consistent visual scale, which matters for
    a card deck where varying x-height reads as a difference in the hand.
    """
    xs = [x for x, y in baseline]; ys = [y for x, y in baseline]
    x0, x1 = min(xs), max(xs)
    ang = 0.0
    if deskew and len(baseline) >= 2:
        dx, dy = baseline[-1][0] - baseline[0][0], baseline[-1][1] - baseline[0][1]
        if dx:
            a_ = math.degrees(math.atan2(dy, dx))
            if abs(a_) < 20:
                ang = a_
    cx, cy = (x0 + x1) / 2.0, sum(ys) / len(ys)
    # generous window so rotation has material to work with
    half_w = (x1 - x0) / 2.0 + pad
    half_h = max(asc, desc) * lh + abs(math.sin(math.radians(ang))) * half_w + lh
    wx0, wy0 = int(cx - half_w - lh), int(cy - half_h)
    wx1, wy1 = int(cx + half_w + lh), int(cy + half_h)
    wx0, wy0 = max(wx0, 0), max(wy0, 0)
    wx1, wy1 = min(wx1, img.width), min(wy1, img.height)
    if wx1 <= wx0 or wy1 <= wy0:
        return None
    win = img.crop((wx0, wy0, wx1, wy1))
    # baseline midpoint inside the window
    mx, my = cx - wx0, cy - wy0
    if ang:
        win = win.rotate(ang, resample=Image.BICUBIC, center=(mx, my),
                         expand=False, fillcolor=(255, 255, 255))
    bx0 = max(int(mx - half_w), 0)
    bx1 = min(int(mx + half_w), win.width)
    by0 = max(int(my - asc * lh), 0)
    by1 = min(int(my + desc * lh), win.height)
    if bx1 <= bx0 or by1 <= by0:
        return None
    return win.crop((bx0, by0, bx1, by1))


def crop_line(img, poly, pad=6, mask=True, bg=(255, 255, 255)):
    xs = [x for x, y in poly]; ys = [y for x, y in poly]
    x0, y0 = max(min(xs) - pad, 0), max(min(ys) - pad, 0)
    x1, y1 = min(max(xs) + pad, img.width), min(max(ys) + pad, img.height)
    if x1 <= x0 or y1 <= y0:
        return None
    box = img.crop((x0, y0, x1, y1))
    if mask:
        m = Image.new("L", box.size, 0)
        ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in poly], fill=255)
        flat = Image.new(box.mode, box.size, bg[:len(box.getbands())]
                         if box.mode != "L" else 255)
        flat.paste(box, (0, 0), m)
        box = flat
    return box


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl"); ap.add_argument("image_root"); ap.add_argument("outdir")
    ap.add_argument("--region", action="append", default=[],
                    help="keep only these region_types (repeatable)")
    ap.add_argument("--min-chars", type=int, default=0)
    ap.add_argument("--max-chars", type=int, default=10**6)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--no-mask", action="store_true")
    ap.add_argument("--no-deskew", action="store_true")
    ap.add_argument("--mode", choices=["baseline", "polygon"], default="baseline",
                    help="baseline band (robust, default) or polygon bbox+mask")
    ap.add_argument("--max-height", type=int, default=160,
                    help="downscale crops taller than this (keeps the bank small)")
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.jsonl, encoding="utf-8")]
    # group by page so the one-page image cache actually hits (8 GB box: one page at a time)
    rows.sort(key=lambda r: (r["page"], r.get("order", 0)))
    imgs = index_images(a.image_root)
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    man = open(out / "manifest.jsonl", "w", encoding="utf-8")

    kept = skipped_noimg = skipped_filter = 0
    cache = {}; lh_cache = {}
    for r in rows:
        if a.region and r.get("region_type") not in a.region: skipped_filter += 1; continue
        if not (a.min_chars <= len(r["text"]) <= a.max_chars): skipped_filter += 1; continue
        if not (r.get("polygon") or r.get("baseline")): skipped_filter += 1; continue
        p = imgs.get(r["page"])
        if p is None: skipped_noimg += 1; continue
        if p not in cache:
            cache.clear()                       # one page in memory at a time (8 GB box)
            cache[p] = Image.open(p).convert("RGB")
        if a.mode == "baseline" and r.get("baseline"):
            if p not in lh_cache:
                lh_cache[p] = page_line_height([x for x in rows if x["page"] == r["page"]])
            box = crop_baseline(cache[p], r["baseline"], lh_cache[p], deskew=not a.no_deskew)
        else:
            box = crop_line(cache[p], r["polygon"], mask=not a.no_mask)
        if box is None: skipped_filter += 1; continue
        if box.height > a.max_height:
            box = box.resize((max(1, int(box.width * a.max_height / box.height)),
                              a.max_height), Image.LANCZOS)
        name = f"{r['witness']}__{r['page']}__{r['line_id']}".replace("/", "_") + ".jpg"
        box.save(out / name, quality=82, optimize=True)
        man.write(json.dumps(dict(image=name, text=r["text"], layer=r["layer"],
                                  witness=r["witness"], page=r["page"],
                                  region_type=r.get("region_type"),
                                  w=box.width, h=box.height), ensure_ascii=False) + "\n")
        kept += 1
        if a.limit and kept >= a.limit: break
    man.close()
    print(f"{kept} crops -> {out}  (skipped: {skipped_filter} filtered, {skipped_noimg} no image)")


if __name__ == "__main__":
    main()
