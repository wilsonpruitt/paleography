#!/usr/bin/env python3
"""Fetch a witness's page images from a IIIF manifest and rescale its GT to them.

Written for Wien ÖNB Cod. 940, whose ground truth ships with no images at all. Two
calibrations had to be established by measurement, and both would have been wrong if
assumed (see research/onb-cod940-iiif.md):

  * **leaf -> canvas offset.** Verified by matching stated image dimensions:
    offset -2 gives 125/125 exact matches. Offset 0 gives 88/125 -- plausible enough to
    pass a spot check and wrong for 37 pages.
  * **coordinate scale.** The TEI records a uniform 2479x3508 for 137 of the 262
    GT-bearing pages. That is a Transkribus PLACEHOLDER, not a real size: the canvases at
    those leaves run from 566 to 1320 px wide. Those pages were uploaded stretched to a
    fixed size, so x and y must be scaled INDEPENDENTLY. Verified by fetching a line
    region from each class and reading it against its transcription.

Writes images to <outdir> and a rescaled JSONL whose coordinates refer to the images we
actually have, so every downstream tool works unchanged.
"""
import json, re, argparse, sys, time, urllib.request, urllib.error
from pathlib import Path


def leaf_of(page):
    m = re.match(r"(\d+)", page)
    return int(m.group(1)) if m else None


def load_manifest(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def canvas_info(cv):
    body = cv["items"][0]["items"][0]["body"]
    svc = (body.get("service") or [{}])[0].get("id")
    return svc, cv.get("width"), cv.get("height")


def tei_dims(tei_path):
    s = Path(tei_path).read_text(encoding="utf-8")
    return {u: (int(w), int(h)) for u, w, h in
            re.findall(r"<graphic url='([^']+)' width='(\d+)px' height='(\d+)px'", s)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl"); ap.add_argument("manifest"); ap.add_argument("outdir")
    ap.add_argument("--tei", required=True, help="source TEI, for its stated image sizes")
    ap.add_argument("--offset", type=int, required=True, help="canvas_index = leaf + offset")
    ap.add_argument("--out-jsonl", required=True)
    ap.add_argument("--limit-pages", type=int, default=None)
    ap.add_argument("--sleep", type=float, default=0.4, help="be polite to the server")
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.jsonl, encoding="utf-8")]
    dims = tei_dims(a.tei)
    man = load_manifest(a.manifest)
    cv = man["items"]
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    pages = []
    seen = set()
    for r in rows:
        if r["page"] not in seen:
            seen.add(r["page"]); pages.append(r["page"])
    if a.limit_pages:
        pages = pages[:a.limit_pages]

    scale, got, failed = {}, 0, []
    for n, page in enumerate(pages, 1):
        i = leaf_of(page) + a.offset
        if not (0 <= i < len(cv)):
            failed.append((page, "canvas out of range")); continue
        svc, cw, ch = canvas_info(cv[i])
        tw, th = dims.get(page, (cw, ch))
        scale[page] = (cw / tw, ch / th, cw, ch)
        dest = out / (Path(page).stem + ".jpg")
        if not dest.exists():
            url = f"{svc}/full/max/0/default.jpg"
            try:
                with urllib.request.urlopen(url, timeout=120) as resp:
                    dest.write_bytes(resp.read())
                time.sleep(a.sleep)
            except (urllib.error.URLError, OSError) as e:
                failed.append((page, str(e)[:60])); continue
        got += 1
        if n % 25 == 0:
            print(f"  {n}/{len(pages)} pages", flush=True)

    with open(a.out_jsonl, "w", encoding="utf-8") as fh:
        kept = 0
        for r in rows:
            sc = scale.get(r["page"])
            if not sc:
                continue
            sx, sy, cw, ch = sc
            if not (out / (Path(r["page"]).stem + ".jpg")).exists():
                continue
            q = dict(r)
            q["page"] = Path(r["page"]).stem + ".jpg"
            if r.get("polygon"):
                q["polygon"] = [[int(x * sx), int(y * sy)] for x, y in r["polygon"]]
            if r.get("baseline"):
                q["baseline"] = [[int(x * sx), int(y * sy)] for x, y in r["baseline"]]
            fh.write(json.dumps(q, ensure_ascii=False) + "\n")
            kept += 1
    print(f"{got}/{len(pages)} page images -> {out}")
    print(f"{kept} lines rescaled -> {a.out_jsonl}")
    if failed:
        print(f"{len(failed)} pages failed, e.g. {failed[:3]}", file=sys.stderr)


if __name__ == "__main__":
    main()
