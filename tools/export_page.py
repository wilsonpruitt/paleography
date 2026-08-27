#!/usr/bin/env python3
"""Export canonical JSONL back out as PAGE XML (one file per page).

This is the half of the round-trip PLAN.md section 2 actually depends on. Import alone
proves we can read the field's formats; EXPORT is what makes the corpus portable into
eScriptorium, Transkribus and Kraken when Phase 4 starts -- the "zero-migration" claim.

Writes PAGE 2019-07-15, the schema version eScriptorium and Transkribus both read.
Round-trip is verified by tools/roundtrip_check.py: export, re-import, compare.
"""
import json, argparse, re
from pathlib import Path
from collections import OrderedDict
from xml.sax.saxutils import escape

NS = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA = f"{NS} {NS}/pagecontent.xsd"
CREATED = "2026-08-27T00:00:00"          # fixed: a changing stamp makes every export a diff


def pts(poly):
    return " ".join(f"{int(x)},{int(y)}" for x, y in poly)


def safe_id(s, fallback):
    """PAGE ids are xsd:ID: must start with a letter/underscore, no spaces."""
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", str(s or ""))
    if not s or not (s[0].isalpha() or s[0] == "_"):
        s = "_" + s
    return s or fallback


def page_xml(image, width, height, regions, layer):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<PcGts xmlns="{NS}" xmlns:xsi="{XSI}" xsi:schemaLocation="{SCHEMA}">',
        "  <Metadata>",
        "    <Creator>Paleography (github.com/wroot-labs) via tools/export_page.py</Creator>",
        f"    <Created>{CREATED}</Created>",
        f"    <LastChange>{CREATED}</LastChange>",
        f"    <Comments>transcription layer: {escape(layer)}</Comments>",
        "  </Metadata>",
        f'  <Page imageFilename="{escape(image)}" imageWidth="{width}" imageHeight="{height}">',
    ]
    for ri, (rid, rtype, lines) in enumerate(regions, 1):
        t = f' type="{escape(rtype)}"' if rtype else ""
        rpoly = [p for l in lines if l.get("polygon") for p in l["polygon"]]
        if rpoly:
            xs = [p[0] for p in rpoly]; ys = [p[1] for p in rpoly]
            rc = [(min(xs), min(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (min(xs), max(ys))]
        else:
            rc = [(0, 0), (width, 0), (width, height), (0, height)]
        out.append(f'    <TextRegion id="{safe_id(rid, f"r{ri}")}"{t}>')
        out.append(f'      <Coords points="{pts(rc)}"/>')
        for li, l in enumerate(lines, 1):
            out.append(f'      <TextLine id="{safe_id(l.get("line_id"), f"l{li}")}">')
            if l.get("polygon"):
                out.append(f'        <Coords points="{pts(l["polygon"])}"/>')
            if l.get("baseline"):
                out.append(f'        <Baseline points="{pts(l["baseline"])}"/>')
            out.append("        <TextEquiv>")
            out.append(f'          <Unicode>{escape(l["text"])}</Unicode>')
            out.append("        </TextEquiv>")
            out.append("      </TextLine>")
        out.append("    </TextRegion>")
    out += ["  </Page>", "</PcGts>", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl"); ap.add_argument("outdir")
    ap.add_argument("--image-root", default=None,
                    help="if given, read each page image to record its true dimensions")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.jsonl, encoding="utf-8")]
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    dims = {}
    if a.image_root:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        for p in Path(a.image_root).rglob("*"):
            if p.suffix.lower() in (".jpg", ".jpeg", ".png"):
                dims[p.name] = p

    pages = OrderedDict()
    for r in rows:
        pages.setdefault(r["page"], []).append(r)

    n = 0
    for page, lines in pages.items():
        lines.sort(key=lambda r: r.get("order", 0))
        w = h = 0
        if page in dims:
            from PIL import Image
            w, h = Image.open(dims[page]).size
        else:
            allp = [p for l in lines if l.get("polygon") for p in l["polygon"]]
            if allp:
                w = max(p[0] for p in allp); h = max(p[1] for p in allp)
        regions = OrderedDict()
        for l in lines:
            key = (l.get("region") or "region1", l.get("region_type"))
            regions.setdefault(key, []).append(l)
        reg = [(k[0], k[1], v) for k, v in regions.items()]
        name = re.sub(r"\.(jpe?g|png)$", "", page, flags=re.I) + ".xml"
        (out / name).write_text(
            page_xml(page, w, h, reg, lines[0].get("layer", "unknown")), encoding="utf-8")
        n += 1
    print(f"{n} PAGE XML files -> {out}")


if __name__ == "__main__":
    main()
