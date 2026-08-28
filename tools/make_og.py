#!/usr/bin/env python3
"""Compose the Open Graph card -> site/og.png (1200x630).

Generated rather than drawn by hand for the same reason as the routes and the landing
cards: the language list is registry data, and a hand-made image goes stale the first
time a language is added and nobody remembers the file exists.

The card shows what the product actually is -- one real line of ink with its transcription
beneath, the site's own comparison view. The line is from Bern, Burgerbibliothek, Cod. 354,
chosen because e-codices places its images under the **Public Domain Mark**: an OG image is
the most widely redistributed asset a site has (every link preview, every share, every
scraper), so it is the one place to be strictest about rights. Attribution is still printed
on the card because it is right, not because the licence compels it.

⚑ The chosen line reads `Qi ait ꝑdu si ait perdu` -- the scribe writes the same word twice,
once abbreviated and once in full. That is the whole pedagogy in one line, so the card can
teach rather than merely announce.

Usage:  python3 tools/make_og.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
FONTS = Path.home() / "Library/Fonts"

# The site's own palette (site/index.html :root), dark theme.
INK, TEXT, MUTED, DIM = "#14120F", "#EAE4DA", "#A0958A", "#7B7168"
LINE, PLATE, ACCENT = "#3A342D", "#100E0C", "#5B82BE"

W, H, M = 1200, 630, 76

# The hero line and its reading. Kept here rather than picked at random from the bank:
# an OG card is a composition, and a randomly chosen line would sometimes be a dull one.
HERO_CROP = ("corpus/crops/fabliaux-bern354/"
             "fabliaux-bern354__e-codices_bbb-0354_146v_max.jpg__eSc_line_1c7fd43c.jpg")
HERO_TEXT = "Qi ait ꝑdu si ait perdu"
HERO_GLOSS = "ꝑ is per — the scribe writes the same word twice, short then long."
HERO_ATTRIB = "Bern, Burgerbibliothek, Cod. 354"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def _tofu_ref(f):
    """Raster of a codepoint no font has, i.e. what .notdef looks like in this face."""
    im = Image.new("L", (120, 120), 0)
    ImageDraw.Draw(im).text((6, 6), "\ue123", font=f, fill=255)
    return im.tobytes()


def assert_glyphs(f, s, where):
    """Fail loudly on a missing glyph instead of shipping a tofu box.

    ⚑ Worth the code. The first cut of this card set the gloss in EB Garamond Italic,
    which has no U+A751, and rendered a hollow box in the one place the card was trying to
    TEACH the sign. A naive check -- "did anything draw?" -- passes on tofu, because tofu
    draws. The only honest test is against the face's own .notdef.
    """
    ref = _tofu_ref(f)
    bad = []
    for ch in sorted(set(s)):
        if ch.isspace():
            continue
        im = Image.new("L", (120, 120), 0)
        ImageDraw.Draw(im).text((6, 6), ch, font=f, fill=255)
        if im.tobytes() == ref:
            bad.append(f"U+{ord(ch):04X} {ch!r}")
    if bad:
        raise SystemExit(f"FATAL {where}: font lacks {', '.join(bad)} -- pick another face")


def main():
    languages, _, _ = registry.load()
    names = " · ".join(l["name"] for l in
                       sorted(languages.values(), key=lambda l: (l.get("order", 999), l["id"])))

    g = lambda s: font("EBGaramond12-Regular.otf", s)
    gi = lambda s: font("EBGaramond12-Italic.otf", s)
    gsc = lambda s: font("EBGaramondSC12-Regular.otf", s)
    # ⛔ EB Garamond has ꝑ only in the roman and has neither ⁊ nor ꝯ at all. Anything
    # quoting the manuscript is set in Cardo, the medievalist's face, which carries the
    # whole repertoire in roman and italic and sits happily beside Garamond.
    c = lambda s: font("Cardo104s.ttf", s)
    ci = lambda s: font("Cardoi99.ttf", s)

    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)

    d.text((M, 54), "Paleography", font=g(76), fill=TEXT)
    d.line([M, 130, M + 96, 130], fill=ACCENT, width=3)
    d.text((M, 148), "Learn to read the manuscripts — not the language, the hand.",
           font=gi(31), fill=MUTED)

    # --- the plate. Trim the crop to its text band: the untrimmed line carries a
    # neighbour's descender above and a rubric bleeding in below, which read as dirt at
    # card size even though they are honest at exercise size.
    crop = Image.open(ROOT / HERO_CROP).convert("RGB")
    crop = crop.crop((0, int(crop.height * 0.13), crop.width, int(crop.height * 0.86)))
    panel_w = W - 2 * M
    ch = int(crop.height * panel_w / crop.width)
    crop = crop.resize((panel_w, ch), Image.LANCZOS)

    top, pad = 224, 22
    box_h = ch + pad * 2 + 108
    d.rounded_rectangle([M - pad, top - pad, M + panel_w + pad, top - pad + box_h],
                        radius=4, fill=PLATE, outline=LINE)
    im.paste(crop, (M, top))
    y = top + ch + 20
    d.line([M, y, M + panel_w, y], fill=LINE)
    f_text, f_gloss = c(38), ci(25)
    assert_glyphs(f_text, HERO_TEXT, "HERO_TEXT")
    assert_glyphs(f_gloss, HERO_GLOSS, "HERO_GLOSS")
    d.text((M, y + 12), HERO_TEXT, font=f_text, fill=TEXT)
    d.text((M, y + 60), HERO_GLOSS, font=f_gloss, fill=MUTED)

    fy = H - 62
    d.text((M, fy), "paleography.app", font=gsc(27), fill=TEXT)
    d.text((M + 236, fy + 4), names, font=g(25), fill=DIM)
    w = d.textlength(HERO_ATTRIB, font=g(22))
    d.text((W - M - w, fy + 5), HERO_ATTRIB, font=g(22), fill=DIM)

    dest = ROOT / "site/og.png"
    im.save(dest, optimize=True)
    print(f"{dest} — {im.size[0]}x{im.size[1]}, {dest.stat().st_size/1024:.0f} KB")
    print(f"  languages: {names}")


if __name__ == "__main__":
    main()
