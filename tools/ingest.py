#!/usr/bin/env python3
"""Normalize HTR ground truth (ALTO v4 / PAGE XML / TEI-facsimile) to canonical JSONL.

One JSON object per line, matching PLAN.md section 2's Line table:
  {witness, page, line_id, order, polygon, baseline, text, layer, region, region_type}

`layer` is NOT inferred from the file -- it is declared per dataset in corpus/sources.yml,
because the seed datasets sit at different transcription layers and none of them say so
inside the XML. Mixing layers silently is the one error that would corrupt both the
exercise bank and any future training set.
"""
import json, re, sys, unicodedata
from pathlib import Path
import xml.etree.ElementTree as ET

ALTO = "{http://www.loc.gov/standards/alto/ns-v4#}"
PAGE_RE = re.compile(r"\{http://schema\.primaresearch\.org/PAGE/gts/pagecontent/[^}]+\}")
TEI = "{http://www.tei-c.org/ns/1.0}"


def _pts(s):
    """Parse 'x1,y1 x2,y2' or 'x1 y1 x2 y2' into [(x,y), ...]."""
    if not s:
        return []
    toks = s.replace(",", " ").split()
    it = [int(float(t)) for t in toks if t.strip()]
    return list(zip(it[0::2], it[1::2]))


def parse_alto(path):
    root = ET.parse(path).getroot()
    fn = root.find(f".//{ALTO}sourceImageInformation/{ALTO}fileName")
    image = (fn.text or "").strip() if fn is not None else path.stem
    # block-type id -> label (Tags/OtherTag), so region_type survives ingest
    tags = {t.get("ID"): t.get("LABEL") for t in root.iter(f"{ALTO}OtherTag")}
    out, order = [], 0
    for blk in root.iter(f"{ALTO}TextBlock"):
        rtype = tags.get(blk.get("TAGREFS", "").split()[0]) if blk.get("TAGREFS") else None
        for tl in blk.iter(f"{ALTO}TextLine"):
            strings = [s.get("CONTENT", "") for s in tl.iter(f"{ALTO}String")]
            text = " ".join(x for x in strings if x)
            if not text.strip():
                continue
            poly = None
            sh = tl.find(f"{ALTO}Shape/{ALTO}Polygon")
            if sh is not None:
                poly = _pts(sh.get("POINTS"))
            elif tl.get("HPOS") is not None:
                x, y = int(tl.get("HPOS")), int(tl.get("VPOS"))
                w, h = int(tl.get("WIDTH")), int(tl.get("HEIGHT"))
                poly = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            order += 1
            out.append(dict(page=image, line_id=tl.get("ID") or f"l{order}", order=order,
                            polygon=poly, baseline=_pts(tl.get("BASELINE")) or None,
                            text=text, region=blk.get("ID"), region_type=rtype))
    return image, out


def parse_page(path):
    root = ET.parse(path).getroot()
    ns = PAGE_RE.match(root.tag).group(0) if PAGE_RE.match(root.tag) else ""
    pg = root.find(f"{ns}Page")
    image = pg.get("imageFilename") if pg is not None else path.stem
    out, order = [], 0
    for reg in root.iter(f"{ns}TextRegion"):
        rtype = reg.get("type")
        for tl in reg.iter(f"{ns}TextLine"):
            # last TextEquiv/Unicode on the line is the line-level text
            te = tl.findall(f"{ns}TextEquiv/{ns}Unicode")
            text = (te[-1].text or "") if te else ""
            if not text.strip():
                continue
            coords = tl.find(f"{ns}Coords")
            base = tl.find(f"{ns}Baseline")
            order += 1
            out.append(dict(page=image, line_id=tl.get("id") or f"l{order}", order=order,
                            polygon=_pts(coords.get("points")) if coords is not None else None,
                            baseline=_pts(base.get("points")) if base is not None else None,
                            text=text, region=reg.get("id"), region_type=rtype))
    return image, out


def parse_tei_facs(path):
    """Transkribus TEI export: <l facs='#zoneid'>text</l> joined to <zone> coords."""
    root = ET.parse(path).getroot()
    zones, surf_of = {}, {}
    for surface in root.iter(f"{TEI}surface"):
        g = surface.find(f"{TEI}graphic")
        img = g.get("url") if g is not None else None
        for z in surface.iter(f"{TEI}zone"):
            zid = z.get("{http://www.w3.org/XML/1998/namespace}id")
            if not zid:
                continue
            if z.get("points"):
                zones[zid] = _pts(z.get("points"))
            elif z.get("ulx") is not None:
                ulx, uly = int(z.get("ulx")), int(z.get("uly"))
                lrx, lry = int(z.get("lrx")), int(z.get("lry"))
                zones[zid] = [(ulx, uly), (lrx, uly), (lrx, lry), (ulx, lry)]
            surf_of[zid] = img
    out, order = [], 0
    for l in root.iter(f"{TEI}l"):
        text = "".join(l.itertext()).strip()
        if not text:
            continue
        ref = (l.get("facs") or "").lstrip("#")
        order += 1
        out.append(dict(page=surf_of.get(ref) or "?", line_id=ref or f"l{order}", order=order,
                        polygon=zones.get(ref), baseline=None, text=text,
                        region=None, region_type=None))
    # also <p> prose lines that are not inside <lg>
    return None, out


def sniff(path):
    head = path.open("rb").read(2048).decode("utf-8", "replace")
    if "standards/alto" in head:
        return parse_alto
    if "PAGE/gts/pagecontent" in head:
        return parse_page
    if "tei-c.org/ns/1.0" in head:
        return parse_tei_facs
    return None


def ingest(root, witness, layer, out_fh, limit=None, include=None, exclude=()):
    """Ingest one WITNESS. include/exclude are substring filters on the relative path.

    Guards, each bought by a real trap in the seed data (see corpus/INGEST-NOTES.md):
      - a repo may hold SEVERAL manuscripts -> always scope with --include
      - a repo may hold CONCATENATED 'allALTOS' aggregates duplicating every page
      - a repo may hold a held-out TEST set from a foreign manuscript
    A page key appearing in two files is fatal: it is the signature of all three.
    """
    n_files = n_lines = 0
    seen_pages = {}
    files = sorted(p for p in Path(root).rglob("*.xml") if ".git" not in p.parts)
    if include:
        files = [p for p in files if include in str(p)]
    for ex in exclude:
        files = [p for p in files if ex not in str(p)]
    for p in files:
        fn = sniff(p)
        if fn is None:
            continue
        try:
            _, lines = fn(p)
        except ET.ParseError as e:
            print(f"  ! parse error {p.name}: {e}", file=sys.stderr)
            continue
        if not lines:
            continue
        key = lines[0]["page"]
        if key in seen_pages:
            raise SystemExit(
                f"FATAL duplicate page key {key!r}\n  in {p}\n  already from {seen_pages[key]}\n"
                f"  -> scope this witness with --include / --exclude; do not ingest aggregates.")
        seen_pages[key] = p
        n_files += 1
        for r in lines:
            r["witness"] = witness
            r["layer"] = layer
            r["text"] = unicodedata.normalize("NFC", r["text"])
            out_fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            n_lines += 1
        if limit and n_lines >= limit:
            break
    return n_files, n_lines


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("witness")
    ap.add_argument("--layer", required=True,
                    choices=["diplomatic", "expanded", "normalised", "mixed", "unknown"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--include", default=None, help="substring the path must contain")
    ap.add_argument("--exclude", action="append", default=[], help="substring to skip (repeatable)")
    a = ap.parse_args()
    with open(a.out, "w", encoding="utf-8") as fh:
        f, l = ingest(a.root, a.witness, a.layer, fh, include=a.include, exclude=a.exclude)
    print(f"{a.witness}: {f} files, {l} lines -> {a.out}")
