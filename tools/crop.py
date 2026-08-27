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


def polygon_band(poly, samples=41):
    """Robust vertical extent of a line polygon: the MEDIAN per-column extent.

    The bounding box cannot be used directly -- some source polygons are
    self-intersecting (an eScriptorium artifact), and one stray spur turned a 46 px
    line into a 189 px box. But the polygon is not worthless either: it is the only
    thing that knows a display-capital line really is 260 px tall.

    Taking the extent column by column and then the median of those extents keeps both
    truths: a spur occupies a few columns and is voted out, while a genuinely tall line
    is tall in almost every column. Returns (top_y, bottom_y) or None.
    """
    if not poly or len(poly) < 3:
        return None
    xs = [p[0] for p in poly]
    x0, x1 = min(xs), max(xs)
    if x1 <= x0:
        return None
    tops, bots = [], []
    edges = list(zip(poly, poly[1:] + poly[:1]))
    for i in range(samples):
        x = x0 + (x1 - x0) * (i + 0.5) / samples
        hits = []
        for (ax, ay), (bx, by) in edges:
            if (ax <= x < bx) or (bx <= x < ax):
                t = (x - ax) / (bx - ax)
                hits.append(ay + t * (by - ay))
        if len(hits) >= 2:
            tops.append(min(hits)); bots.append(max(hits))
    if len(tops) < 5:
        return None
    tops.sort(); bots.sort()
    return tops[len(tops) // 2], bots[len(bots) // 2]


def _ink_profile(win, thresh, step=2):
    """Per-row count of ink pixels, lightly smoothed."""
    g = win.convert("L"); W, H = g.size; px = g.load()
    raw = [sum(1 for x in range(0, W, step) if px[x, y] < thresh) for y in range(H)]
    out = []
    for i in range(H):
        lo, hi = max(0, i - 1), min(H, i + 2)
        out.append(sum(raw[lo:hi]) / (hi - lo))
    return out


def _ink_extent(win, my, lh, max_up, max_dn):
    """Distance from the baseline to the inter-line GUTTER, above and below.

    Three attempts were needed here, and the two failures are the instructive part.

    A fixed multiple of the page line height clips DISPLAY CAPITALS: on Voss. Lat. O. 41
    f02r the page median line gap is 46 px but INCIPIT LIBER EVTI stands ~260 px tall, so
    a 1.25*lh ascender lopped the tops off the N and C. Raising the multiple globally
    drags neighbours into every ordinary crop instead.

    Looking for BLANK rows fails too: this parchment is mottled and densely written, and
    the row-ink count never approaches zero -- that attempt returned an identical 195 px
    for a display line and a small one.

    What actually marks the gutter is a LOCAL MINIMUM that then rises again as the next
    line up begins. Measured on the line above: ink runs 115-145 through the x-height,
    dips to 77, then jumps to 231. So: walk out, track the running minimum, and call the
    gutter as soon as the profile climbs back above 1.6x that minimum. Absolute darkness
    is never the test; the shape of the profile is.
    """
    g = win.convert("L"); W, H = g.size; px = g.load()
    samples = sorted(px[x, y] for y in range(0, H, max(1, H // 40))
                     for x in range(0, W, max(1, W // 40)))
    if not samples:
        return int(1.25 * lh), int(0.4 * lh)
    bg = samples[int(len(samples) * 0.85)]
    prof = _ink_profile(win, bg - 30)
    if not prof:
        return int(1.25 * lh), int(0.4 * lh)
    my = int(my)

    def scan(direction, limit, min_off):
        limit = int(limit); min_off = int(max(2, min_off))
        vals = []
        for d in range(0, limit + 1):
            y = my + direction * d
            vals.append(prof[y] if 0 <= y < H else 0.0)
        peak = max(vals) if vals else 0.0
        if peak <= 0:
            return min_off
        run_min, run_at = None, min_off
        for d in range(min_off, limit + 1):
            v = vals[d]
            # blank space (edge of the written area) -- gutter reached outright
            if v <= peak * 0.12:
                return d
            if run_min is None or v < run_min:
                run_min, run_at = v, d
            elif run_min is not None and v > max(run_min * 1.6, peak * 0.28):
                return run_at            # profile climbing again: next line beginning
        return limit

    up = scan(-1, max_up, max(6, 0.62 * lh))
    dn = scan(+1, max_dn, max(4, 0.22 * lh))
    return up, dn


def crop_baseline(img, baseline, lh, poly=None, asc=1.25, desc=0.40, pad=4, deskew=True):
    """Crop a band around the baseline, sized to the ink rather than to a fixed multiple.

    Rotates FIRST, then bands. Doing it the other way adds the baseline's own tilt to the
    band height -- on a tilted line that turned a 46 px line into a 133 px crop carrying
    its neighbours with it.

    Robust to malformed polygons (self-intersecting spurs are a real eScriptorium
    artifact here): the polygon is used only as a loose ceiling, never as the box.
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
    band = polygon_band(poly) if poly else None
    poly_h = (band[1] - band[0]) if band else None
    ceil_up = max((poly_h * 1.3 + lh) if poly_h else 2.8 * lh, 1.6 * lh)
    ceil_dn = max(0.9 * lh, min(1.4 * lh, (poly_h * 0.45) if poly_h else 0.9 * lh))

    half_w = (x1 - x0) / 2.0 + pad
    half_h = ceil_up + abs(math.sin(math.radians(ang))) * half_w + lh
    wx0, wy0 = int(cx - half_w - lh), int(cy - half_h)
    wx1, wy1 = int(cx + half_w + lh), int(cy + ceil_dn + lh)
    wx0, wy0 = max(wx0, 0), max(wy0, 0)
    wx1, wy1 = min(wx1, img.width), min(wy1, img.height)
    if wx1 <= wx0 or wy1 <= wy0:
        return None
    win = img.crop((wx0, wy0, wx1, wy1))
    mx, my = cx - wx0, cy - wy0
    if ang:
        win = win.rotate(ang, resample=Image.BICUBIC, center=(mx, my),
                         expand=False, fillcolor=(255, 255, 255))
    if band:
        # trust the robust polygon extent, measured from the baseline, plus a little air
        up = int(max(cy - band[0], 0.95 * lh) + 0.16 * lh + 4)
        dn = int(max(band[1] - cy, desc * lh) + 0.10 * lh + 3)
        up = min(up, int(3.4 * lh) if poly_h is None else int(poly_h * 1.3 + lh))
    else:
        up, dn = _ink_extent(win, my, lh, int(ceil_up), int(ceil_dn))
        up = int(min(max(up + 6, 0.95 * lh), ceil_up))
        dn = int(min(max(dn + 4, desc * lh), ceil_dn))
    bx0 = max(int(mx - half_w), 0)
    bx1 = min(int(mx + half_w), win.width)
    by0 = max(int(my - up), 0)
    by1 = min(int(my + dn), win.height)
    if bx1 <= bx0 or by1 <= by0:
        return None
    return win.crop((bx0, by0, bx1, by1))


def extend_for_initial(img, poly, lh, max_reach=3.2, bg_pct=0.85):
    """How far left the crop must reach to include an enlarged opening initial.

    A section in a medieval book opens with a large decorated capital that hangs OUTSIDE
    the ruled text block, in the margin, and the scribe does not repeat the letter: the
    body of the line begins with the second letter. On Cod. 940 f. 30 the line reads
    `uaeritur quod cooperantur` beside a tall rubricated Q -- together, *Quaeritur*.

    The GT polygon covers only the ordinary script, so a crop taken from it starts at
    `uaeritur` while the printed transcription says `Quaeritur`, which is exactly as
    confusing as it sounds.

    Returns a new left edge: scans leftwards for a band of ink lying within the line's
    vertical extent, and stops at the first clear gutter beyond it.
    """
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    x0, y0, y1 = min(xs), min(ys), max(ys)
    reach = int(max_reach * lh)
    sx0 = max(int(x0 - reach), 0)
    if sx0 >= x0:
        return x0
    # an initial is TALL: look a little above and below the line band
    ty0 = max(int(y0 - 0.5 * lh), 0)
    ty1 = min(int(y1 + 0.5 * lh), img.height)
    strip = img.crop((sx0, ty0, int(x0), ty1)).convert("L")
    w, h = strip.size
    if w < 4 or h < 4:
        return x0
    px = strip.load()
    samples = sorted(px[x, y] for y in range(0, h, max(1, h // 30))
                     for x in range(0, w, max(1, w // 30)))
    if not samples:
        return x0
    thresh = samples[int(len(samples) * bg_pct)] - 30
    cols = [sum(1 for y in range(0, h, 2) if px[x, y] < thresh) for x in range(w)]
    if not any(cols):
        return x0
    peak = max(cols)
    if peak < 2:
        return x0
    # walk left from the polygon edge; remember the last inked column, stop after a gutter
    last, gap = None, 0
    for i in range(w - 1, -1, -1):
        if cols[i] > peak * 0.18:
            last = i; gap = 0
        elif last is not None:
            gap += 1
            # an initial is DELIBERATELY set apart from the text it opens, so the gutter
            # tolerance here must be generous -- 0.6*lh stopped short of a Q sitting 50px
            # clear of its line.
            if gap > lh * 1.5:
                break
    if last is None:
        return x0
    return max(sx0 + last - int(0.25 * lh), 0)


def crop_line(img, poly, pad=6, mask=True, bg=(255, 255, 255), lh=None,
              initials=True, text=None, flags=None):
    xs = [x for x, y in poly]; ys = [y for x, y in poly]
    x0, y0 = max(min(xs) - pad, 0), max(min(ys) - pad, 0)
    x1, y1 = min(max(xs) + pad, img.width), min(max(ys) + pad, img.height)
    ext = None
    # Reach for an opening initial ONLY when the transcription itself starts with a
    # capital. A tall initial hangs down beside the NEXT line too, and without this test
    # that line grabs it -- measured: `euangelii non difficile...` came back carrying the
    # Q that belongs to `Quaeritur` above it.
    if initials and lh and text and text[:1].isupper():
        ext = extend_for_initial(img, poly, lh)
        if ext is not None and ext < x0 - 2:
            x0 = ext
            mask = False          # the initial lies outside the polygon; masking erases it
            if flags is not None:
                flags["initial"] = True
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
    ap.add_argument("--no-initials", action="store_true",
                    help="do not reach left for an enlarged opening initial")
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
            box = crop_baseline(cache[p], r["baseline"], lh_cache[p],
                                poly=r.get("polygon"), deskew=not a.no_deskew)
        else:
            if p not in lh_cache:
                lh_cache[p] = page_line_height([x for x in rows if x["page"] == r["page"]])
            flags = {}
            box = crop_line(cache[p], r["polygon"], mask=not a.no_mask,
                            lh=lh_cache[p], initials=not a.no_initials,
                            text=r["text"], flags=flags)
            if flags.get("initial"):
                r = dict(r); r["initial"] = True
        if box is None: skipped_filter += 1; continue
        if box.height > a.max_height:
            box = box.resize((max(1, int(box.width * a.max_height / box.height)),
                              a.max_height), Image.LANCZOS)
        name = f"{r['witness']}__{r['page']}__{r['line_id']}".replace("/", "_") + ".jpg"
        box.save(out / name, quality=82, optimize=True)
        man.write(json.dumps(dict(image=name, text=r["text"], layer=r["layer"],
                                  witness=r["witness"], page=r["page"],
                                  region_type=r.get("region_type"),
                                  initial=bool(r.get("initial")),
                                  w=box.width, h=box.height), ensure_ascii=False) + "\n")
        kept += 1
        if a.limit and kept >= a.limit: break
    man.close()
    print(f"{kept} crops -> {out}  (skipped: {skipped_filter} filtered, {skipped_noimg} no image)")


if __name__ == "__main__":
    main()
