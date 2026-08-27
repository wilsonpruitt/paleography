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
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

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


def crop_baseline(img, baseline, lh, poly=None, asc=1.25, desc=0.40, pad=4,
                  deskew=True, spot=True):
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
    out = win.crop((bx0, by0, bx1, by1))
    if spot and band:
        # The band carries bleed from its neighbours -- unavoidable on a page written 46 px
        # apart in letters 77 px tall. Put the line itself in focus and let the bleed recede,
        # rather than cutting it off mid-stroke.
        base_y = int(my) - by0                      # the baseline, in the finished crop
        top = base_y - (cy - band[0])
        bot = base_y + (band[1] - cy)
        out = spotlight(out, [(0, int(top), out.width, int(bot))], blur=2.2, fade=0.5,
                        feather=7)
    return out


def find_initial(img, poly, lh, max_reach=3.2, max_rise=2.6, bg_pct=0.85):
    """Locate an enlarged opening initial to the left of a line. Returns (x0, y0, y1) or None.

    A section in a medieval book opens with a large decorated capital that hangs OUTSIDE the
    ruled text block, and the scribe does not repeat the letter: the body of the line begins
    with the SECOND letter. On Cod. 940 f. 30 the line reads `uaeritur quod cooperantur`
    beside a tall rubricated Q -- together, *Quaeritur*.

    The vertical extent is measured, not assumed: such a letter is commonly two to four lines
    deep, and a crop sized to one line band decapitates it just as surely as the old hard mask
    erased it.
    """
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    x0, y0, y1 = min(xs), min(ys), max(ys)
    reach = int(max_reach * lh)
    sx0 = max(int(x0 - reach), 0)
    if sx0 >= x0:
        return None
    # scan TALL: the initial may run well below the line it opens
    ty0 = max(int(y0 - max_rise * lh), 0)
    ty1 = min(int(y1 + max_rise * lh), img.height)
    strip = img.crop((sx0, ty0, int(x0), ty1)).convert("L")
    w, h = strip.size
    if w < 4 or h < 4:
        return None
    px = strip.load()
    samples = sorted(px[x, y] for y in range(0, h, max(1, h // 40))
                     for x in range(0, w, max(1, w // 40)))
    if not samples:
        return None
    thresh = samples[int(len(samples) * bg_pct)] - 30

    # restrict the search to rows near the line, to find the initial's HORIZONTAL start
    band0 = max(int(y0 - 0.5 * lh) - ty0, 0)
    band1 = min(int(y1 + 0.5 * lh) - ty0, h)
    cols = [sum(1 for y in range(band0, band1, 2) if px[x, y] < thresh) for x in range(w)]
    if not cols or max(cols) < 2:
        return None
    peak = max(cols)
    # Ink is ANY column with a mark in it, not one above a fraction of the peak. The page
    # edge sits at the far left of this strip and saturates the profile: judged against it,
    # the Q's own strokes look weak and the hollow of its bowl looks like a gutter. Measured
    # on Cod. 940 f.30 -- edge columns 53-71, Q strokes 30-40, Q bowl 1-12, true gutter 0.
    # Only the gutter is actually empty, so only the gutter should stop the walk.
    ink = max(1, int(peak * 0.03))
    last, gap = None, 0
    for i in range(w - 1, -1, -1):
        if cols[i] >= ink:
            last = i; gap = 0
        elif last is not None:
            gap += 1
            if gap > lh * 0.4:
                break
    if last is None:
        return None
    ix0 = max(sx0 + last - int(0.25 * lh), 0)

    # now the VERTICAL extent, over the initial's own columns only
    c0 = max(ix0 - sx0, 0); c1 = w
    rows = [sum(1 for x in range(c0, c1, 2) if px[x, y] < thresh) for y in range(h)]
    rpeak = max(rows) if rows else 0
    if rpeak < 2:
        return None
    # Take only the run of inked rows CONTIGUOUS with the line itself. Taking every inked
    # row in the strip measured 6.3 line-heights on Cod. 940 f.30 -- it was collecting the
    # marginalia and initials of other lines that happen to share these columns.
    thr = max(1, rpeak * 0.10)
    mid = min(max((band0 + band1) // 2, 0), h - 1)
    gap_max = int(0.45 * lh)
    top = mid
    gap = 0
    for y in range(mid, -1, -1):
        if rows[y] > thr:
            top = y; gap = 0
        else:
            gap += 1
            if gap > gap_max:
                break
    bot = mid
    gap = 0
    for y in range(mid, h):
        if rows[y] > thr:
            bot = y; gap = 0
        else:
            gap += 1
            if gap > gap_max:
                break
    iy0 = ty0 + top - int(0.12 * lh)
    iy1 = ty0 + bot + int(0.12 * lh)

    # Sanity bounds. A decorated opening initial in this hand runs roughly one and a half to
    # three and a half lines deep and about one to two and a half lines wide. Measurements
    # outside that are not initials: too tall means the run has escaped into marginalia or
    # the page edge, too short means a stray mark or a neighbour's descender. Reject rather
    # than return a monster crop -- the line then crops normally, which is merely no better
    # than before, whereas a six-line crop is actively worse.
    hh = (iy1 - iy0) / float(lh)
    ww = (x0 - ix0) / float(lh)
    if not (1.2 <= hh <= 3.8 and 0.55 <= ww <= 3.0):
        return None
    return (ix0, max(iy0, 0), min(iy1, img.height))


def spotlight(box, shapes, blur=2.6, fade=0.55, feather=9, bg=(255, 255, 255)):
    """Keep `shapes` sharp; blur and fade everything else in the crop.

    A hard mask (white outside the polygon) was the first approach and it is wrong twice:
    it erases an enlarged initial that lies outside the line's polygon, and on a densely
    written page it cuts neighbours off mid-stroke, which reads as damage.

    Leaving the crop untouched is wrong too -- Wilson, on a line opening with a two-line
    decorated Q: *"that first letter dwarfs everything else and brings up other lines…
    we need a way to show the first one but keep the eyes on the top line"*.

    So: everything stays visible and in place, but only the target line is in focus. The
    neighbours remain as context -- which is honest about what a manuscript page is -- and
    the eye is told where to sit. `shapes` is a list of polygons or (x0,y0,x1,y1) boxes in
    CROP coordinates.
    """
    if not shapes:
        return box
    m = Image.new("L", box.size, 0)
    d = ImageDraw.Draw(m)
    for sh in shapes:
        if not sh:
            continue
        if isinstance(sh, tuple) and len(sh) == 4 and all(isinstance(v, (int, float)) for v in sh):
            d.rectangle([int(v) for v in sh], fill=255)
        else:
            d.polygon([(int(x), int(y)) for x, y in sh], fill=255)
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    dim = box.filter(ImageFilter.GaussianBlur(blur))
    flat = Image.new(box.mode, box.size, bg[:len(box.getbands())] if box.mode != "L" else 255)
    dim = Image.blend(dim, flat, fade)          # wash the out-of-focus material toward the page
    return Image.composite(box, dim, m)


def crop_line(img, poly, pad=6, mask=True, bg=(255, 255, 255), lh=None,
              initials=True, text=None, flags=None):
    xs = [x for x, y in poly]; ys = [y for x, y in poly]
    x0, y0 = max(min(xs) - pad, 0), max(min(ys) - pad, 0)
    x1, y1 = min(max(xs) + pad, img.width), min(max(ys) + pad, img.height)
    init = None
    # Reach for an opening initial ONLY when the transcription itself starts with a capital.
    # A tall initial hangs down beside the NEXT line too, and without this test that line
    # grabs it -- measured: `euangelii non difficile...` came back carrying the Q belonging
    # to `Quaeritur` above it.
    if initials and lh and text and text[:1].isupper():
        init = find_initial(img, poly, lh)
        if init is not None and init[0] < x0 - 2:
            x0 = init[0]
            # Grow the box to the initial's measured height: these letters run two to four
            # lines deep, and a one-line band cuts them off at the waist.
            y0 = max(min(y0, init[1]), 0)
            y1 = min(max(y1, init[2]), img.height)
            if flags is not None:
                flags["initial"] = True
        else:
            init = None
    if x1 <= x0 or y1 <= y0:
        return None
    box = img.crop((x0, y0, x1, y1))
    if mask:
        shapes = [[(x - x0, y - y0) for x, y in poly]]
        if init is not None:
            # the initial's own measured rectangle, kept in focus with the line it opens
            shapes.append((0, max(init[1] - y0, 0),
                           int(min(xs) - x0) + int(0.2 * (lh or 40)),
                           min(init[2] - y0, box.height)))
        box = spotlight(box, shapes)
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
    ap.add_argument("--no-spotlight", action="store_true",
                    help="do not blur/fade material outside the target line")
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
                                poly=r.get("polygon"), deskew=not a.no_deskew,
                                spot=not a.no_spotlight)
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
