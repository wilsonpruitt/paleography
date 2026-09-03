#!/usr/bin/env python3.11
"""Stroke-order engine, per SYRIAC-CALLIGRAPHY-PLAN.md.

`extract`: read a font, write one stub TOML per glyph form under
registry/strokes/<script>/<hand>/ -- outline + advance filled, [[stroke]] empty.
Never hand-edit `outline`; it is regenerated from the font, not authored.

`svg(glyph_dir, glyph_id, mode)`: read a stroke TOML, return an SVG string.
mode="static": every stroke drawn in full, numbered start dot + arrowhead.
mode="animate": ghost fill of the outline, strokes drawn via CSS dasharray/
dashoffset keyframes, clipped to the outline so a stroke reads as "inside the
letter" rather than a bare line.

No dependency beyond fontTools (already installed for python3.11 on this Mac).
"""
import argparse
import pathlib
import sys

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

REPO = pathlib.Path(__file__).resolve().parent.parent


def _toml_dump(d, f):
    # Minimal writer -- this repo's TOML files are hand-formatted, not
    # machine-round-tripped, so a small custom dumper keeps the stub files
    # readable rather than pulling in a TOML-writer dependency.
    def scalar(v):
        if isinstance(v, str):
            return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
        if isinstance(v, bool):
            return "true" if v else "false"
        return str(v)

    f.write("[glyph]\n")
    for k, v in d["glyph"].items():
        f.write(f"{k} = {scalar(v)}\n")
    f.write("\n# [[stroke]] entries go here -- array order = stroke order,\n")
    f.write("# point order within a median = pen direction. See\n")
    f.write("# SYRIAC-CALLIGRAPHY-PLAN.md §3 for the schema.\n")


def extract(font_path, script, hand, out_dir, forms=("isol", "init", "medi", "fina")):
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen

    font = TTFont(font_path)
    gs = font.getGlyphSet()
    names = set(font.getGlyphOrder())
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for name in sorted(names):
        if not name.startswith("uni0"):
            continue
        base = name.split(".")[0]
        try:
            cp = int(base[3:], 16)
        except ValueError:
            continue
        if not (0x0700 <= cp <= 0x074F):  # Syriac Unicode block only
            continue
        suffix = name[len(base):]  # "", ".init", ".medi", ".fina"
        form = {"": "isol", ".init": "init", ".medi": "medi", ".fina": "fina"}.get(suffix)
        if form is None or form not in forms:
            continue
        glyph = gs[name]
        pen = SVGPathPen(gs)
        glyph.draw(pen)
        outline = pen.getCommands()
        if not outline:
            continue
        bp = BoundsPen(gs)
        glyph.draw(bp)
        bounds = bp.bounds or (0, 0, 0, 0)
        stub = {
            "glyph": {
                "script": script,
                "hand": hand,
                "codepoint": name,
                "form": form,
                "font": pathlib.Path(font_path).name,
                "upm": font["head"].unitsPerEm,
                "advance": glyph.width,
                "bbox": f"{bounds[0]:.0f},{bounds[1]:.0f},{bounds[2]:.0f},{bounds[3]:.0f}",
                "outline": outline,
            }
        }
        fname = out_dir / f"{name}.toml"
        if fname.exists():
            existing = load(fname)
            if existing.get("stroke"):
                continue  # never clobber hand-authored strokes on a re-extract
        with open(fname, "w") as f:
            _toml_dump(stub, f)
        written.append(fname)
    return written


def load(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


def _smooth_path(points):
    """Catmull-Rom-to-cubic-Bezier smoothing over a polyline: passes exactly
    THROUGH every given point (unlike a quadratic-through-midpoints curve,
    which only approaches its control points and visibly cuts corners --
    caught on Alap's crotch, a genuinely sharp turn per Kiraz's own prose).
    Smooth between points, exact at them."""
    if len(points) < 3:
        return "M " + " L ".join(f"{x},{y}" for x, y in points)
    pts = [points[0]] + list(points) + [points[-1]]  # phantom endpoints
    d = f"M {points[0][0]},{points[0][1]} "
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]} "
    return d


def svg(data, mode="animate", stroke_width=46, size=220):
    g = data["glyph"]
    x0, y0, x1, y1 = [float(v) for v in g["bbox"].split(",")]
    pad = 60
    vb = f"{x0 - pad} {-(y1) - pad} {(x1 - x0) + 2 * pad} {(y1 - y0) + 2 * pad}"
    # font coords are y-up with baseline 0; SVG is y-down, so flip.
    flip = f'transform="scale(1,-1)"'
    strokes = data.get("stroke", [])
    parts = [
        f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" class="stroke-fig" data-mode="{mode}">',
        f'<g {flip}>',
        f'<clipPath id="clip-{g["codepoint"].replace(".", "-")}"><path d="{g["outline"]}"/></clipPath>',
        f'<path d="{g["outline"]}" fill="currentColor" fill-opacity="0.16" '
        f'stroke="currentColor" stroke-opacity="0.35" stroke-width="1.5"/>',
    ]
    n = len(strokes)
    for i, s in enumerate(strokes):
        pts = s["median"]
        d = _smooth_path(pts)
        clip = f'clip-path="url(#clip-{g["codepoint"].replace(".", "-")})"'
        if mode == "animate":
            parts.append(
                f'<path d="{d}" fill="none" stroke="currentColor" '
                f'stroke-width="{stroke_width}" stroke-linecap="round" '
                f'stroke-linejoin="round" {clip} class="stroke-path" '
                f'style="--i:{i}" pathLength="1"/>'
            )
        else:
            parts.append(
                f'<path d="{d}" fill="none" stroke="currentColor" '
                f'stroke-width="{stroke_width}" stroke-linecap="round" '
                f'stroke-linejoin="round" {clip}/>'
            )
            sx, sy = pts[0]
            parts.append(f'<circle cx="{sx}" cy="{sy}" r="18" fill="currentColor"/>')
            parts.append(
                f'<text x="{sx}" y="{sy}" font-size="24" fill="white" '
                f'text-anchor="middle" dy="8" transform="scale(1,-1)" '
                f'transform-origin="{sx} {sy}">{i + 1}</text>'
            )
    parts.append("</g></svg>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ex = sub.add_parser("extract")
    ex.add_argument("font")
    ex.add_argument("--script", required=True)
    ex.add_argument("--hand", required=True)
    ex.add_argument("--out", required=True)
    ex.add_argument("--forms", default="isol")

    rd = sub.add_parser("render")
    rd.add_argument("toml_path")
    rd.add_argument("--mode", default="animate", choices=["animate", "static"])

    args = ap.parse_args()
    if args.cmd == "extract":
        forms = tuple(args.forms.split(","))
        written = extract(args.font, args.script, args.hand, args.out, forms)
        print(f"wrote {len(written)} stub(s) to {args.out}")
    elif args.cmd == "render":
        data = load(args.toml_path)
        print(svg(data, mode=args.mode))


if __name__ == "__main__":
    main()
