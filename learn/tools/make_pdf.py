#!/usr/bin/env python3
"""Printable lesson PDFs -- SYRIAC-PDF-PLAN.md. Fourth consumer of LESSON-N.md + the
drill sidecars (after the lesson page, the drill JSON, and the index line): renders
notes-up-front / worksheet-sheets-with-answers-on-the-back / scorecard, per §2-3.

Nothing here re-authors content. Notes prose comes from make_primers.render() on the same
lesson text the web page renders (cut before the Drills/Stage-2 block, §2); sheet items
come straight out of the compiled drill sidecar's RAW tables (vocab/forms/halfline/cloze/
finish/whole/drills/letters/pairs/triples) -- not the compiled, shuffled, MC-pooled `items`
shape make_drill.py builds for the browser engine, since print wants the plain content in
sidecar order (§3 "Order").

Mechanics: each lesson's three parts (notes / sheets / scorecard) are rendered to PDF
SEPARATELY by headless Chrome, each pass checked by page count (`pdfinfo`), then merged
with `qpdf` -- because Chrome ignores `break-before:right` (measured, §1) so duplex parity
(every sheet's front on an odd page) has to be enforced by counting and padding, not by CSS.

Usage:  python3 learn/tools/make_pdf.py           # build learn/site/pdf/*.pdf
        python3 learn/tools/make_pdf.py --check   # verify only, renders but doesn't keep output
        python3 learn/tools/make_pdf.py --lesson 2  # just one lesson, both sizes (fast iteration)
"""
import glob
import html
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent          # learn/tools
LEARN = HERE.parent                              # learn/
ROOT = LEARN.parent                              # repo root
SYRIAC_DIR = LEARN / "syriac"
DRILL_SRC = SYRIAC_DIR / "drill"
SHELL = LEARN / "shell"
PRINT_CSS = SHELL / "print.css"
FONTS_DIR = LEARN / "fonts"
OUT_DIR = LEARN / "site" / "pdf"

sys.path.insert(0, str(HERE))
import make_learn      # noqa: E402  (reused: split_lesson_body, extract_record_refs, footer)
sys.path.insert(0, str(ROOT / "tools"))
import make_primers    # noqa: E402  (reused: the markdown renderer)

N_LESSONS = 11
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
PAGE_SIZES = {"letter": None, "a4": "A4"}   # None -> use print.css's default (Letter)

# Where each lesson's notes stop and the worksheet material begins. Every lesson from 1-10
# opens a "## Drills (ours...)" block right before Stage 2 except Lesson 7, which has no
# Drills block and goes straight to Stage 2; Lesson 0 has no Stages at all and its
# worksheet material starts at Part 4. Declared here, once, rather than hidden inside a
# regex fallback chain, so a twelfth lesson with a fourth shape fails loudly instead of
# silently matching the wrong heading.
NOTES_END_HEADING = {n: "## Drills" for n in range(1, N_LESSONS)}
NOTES_END_HEADING[0] = "## Part 4"
NOTES_END_HEADING[7] = "## Stage 2"


def inject_stroke_figures_print(body):
    """Print's own {stroke:X} -> figure pass. make_pdf.py renders lesson notes
    through make_primers.render() directly (see module docstring: a separate
    consumer of LESSON-N.md, not a call into make_learn.py's run()), so
    make_learn.inject_stroke_figures() -- built for the web page, wrapping each
    figure in a click/animate widget -- never runs here. Paper doesn't animate;
    this reuses stroke_print_figure()'s static-only rendering instead of
    quietly leaving the literal marker text in a printed page."""
    return re.sub(r"\{stroke:(.)\}", lambda m: stroke_print_figure(m.group(1)), body)


def stroke_print_figure(letter_char):
    """A small static (numbered) stroke figure for one letter, sized for print.
    SYRIAC-CALLIGRAPHY-PLAN.md §10 ruling 3: the letter sheet gets a plain ruled
    copy-row, no stroke arrows -- that was the PDF plan's own ruling, written
    before this project (item 2) existed to own formation. It exists now, so
    this is that beside-the-rule figure, per SYRIAC-CALLIGRAPHY-PLAN.md §7.
    Print is static-only -- no click/animate, paper doesn't do that."""
    data = make_learn._stroke_data(letter_char)
    if data is None or not data.get("stroke"):
        return ""
    svg = make_learn.strokes.svg(data, mode="static")
    return f'<span class="stroke-print">{svg}</span>'


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("chromium") or shutil.which("google-chrome")
    if found:
        return found
    raise SystemExit("FATAL: no headless-capable Chrome/Chromium found (see SYRIAC-PDF-PLAN.md §1)")


CHROME = None  # resolved lazily so --help-less imports (tests) don't require Chrome present


def render_pdf(html_str, out_pdf, page_size="letter"):
    """Shell out to headless Chrome. Two things were measured wrong on the first attempt,
    both fixed here: (1) the DEFAULT Chrome profile must never be used for this -- it is
    the user's real, logged-in browser profile, and driving it headless woke the real
    GoogleUpdater/GCM stack tied to that profile; every call therefore gets its own
    disposable --user-data-dir. (2) a brand-new profile's first launch fires background
    component-updater fetches (Crowd Deny, First-Party Sets, ...) that keep the Chrome
    process alive well after --print-to-pdf has already written the file -- so this
    disables that machinery AND polls for the finished, size-stable output file rather
    than waiting on the process to exit, with a generous wall-clock timeout as backstop."""
    global CHROME
    if CHROME is None:
        CHROME = find_chrome()
    last_err = None
    for attempt in range(2):   # this Mac runs at ~8GB/8GB used system-wide (measured while
        # testing this file, 214MB free) -- a single Chrome launch can transiently produce
        # nothing under that pressure with no useful stderr; one retry after a short pause
        # is cheaper than making the whole pipeline flaky over a passing contention spike.
        try:
            _render_pdf_once(html_str, out_pdf)
            return
        except SystemExit as e:
            last_err = e
            if attempt == 0:
                time.sleep(3)
    raise last_err


def _render_pdf_once(html_str, out_pdf):
    out_path = Path(out_pdf)
    out_path.unlink(missing_ok=True)   # Chrome writes the PDF atomically at the very end;
    # a caller re-using a path across runs (as this module's own manual tests just did)
    # would otherwise leave a stale file sitting there for the stability-poll below to
    # mistake for "already finished" before the real render has written anything.
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "page.html"
        src.write_text(html_str, encoding="utf-8")
        profile_dir = Path(td) / "profile"
        cmd = [
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={profile_dir}", "--no-first-run",
            "--disable-component-update", "--disable-background-networking",
            "--disable-domain-reliability", "--disable-client-side-phishing-detection",
            "--disable-sync", "--disable-features=OptimizationHints,MediaRouter",
            "--virtual-time-budget=8000",
            f"--print-to-pdf={out_pdf}", f"file://{src}",
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        deadline = time.monotonic() + 40
        last_size, stable_since = -1, None
        while time.monotonic() < deadline:
            if out_path.exists():
                size = out_path.stat().st_size
                if size > 0 and size == last_size:
                    if stable_since is None:
                        stable_since = time.monotonic()
                    elif time.monotonic() - stable_since > 1.0:
                        break
                else:
                    stable_since = None
                last_size = size
            if proc.poll() is not None:
                break
            time.sleep(0.25)
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        if not out_path.exists() or out_path.stat().st_size == 0:
            stderr = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
            raise SystemExit(f"FATAL: Chrome print-to-pdf produced nothing for {out_pdf}\n{stderr}")


def pdf_page_count(pdf_path):
    r = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    if not m:
        raise SystemExit(f"FATAL: pdfinfo didn't report a page count for {pdf_path}")
    return int(m.group(1))


def qpdf_merge(parts, out_pdf):
    parts = [str(p) for p in parts if p is not None]
    subprocess.run(["qpdf", "--empty", "--pages", *parts, "--", str(out_pdf)],
                    capture_output=True, text=True, check=True)


# ---------------------------------------------------------------------------
# Shared page chrome
# ---------------------------------------------------------------------------

def page_style_block(page_size):
    css = PRINT_CSS.read_text(encoding="utf-8")
    css = css.replace('url("../fonts/', f'url("file://{FONTS_DIR}/')
    override = ""
    size = PAGE_SIZES.get(page_size)
    if size:
        override = f"@page{{size:{size}}}"
    return f"<style>{css}\n{override}</style>"


def wrap_print_page(title, body, page_size, footer_text=""):
    foot = (f'<div class="runningfoot"><span>A Syriac Chrestomathy &middot; {html.escape(footer_text)}</span>'
            f'<span>syriac.paleography.app</span></div>') if footer_text else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>{html.escape(title)}</title>
{page_style_block(page_size)}
</head><body>
{body}
{foot}
</body></html>"""


def masthead(lesson_label):
    return (f'<div class="masthead"><span class="wm">A Syriac Chrestomathy</span>'
            f'<span class="meta">{html.escape(lesson_label)} &middot; public domain sources, '
            f'CC BY-NC 4.0 lesson text &middot; syriac.paleography.app</span></div>')


def blank_page_html(page_size, lesson_label):
    body = (masthead(lesson_label) +
            '<p class="blank-notice">This page is intentionally blank, '
            'so the worksheets that follow print back-to-back.</p>')
    return wrap_print_page("Blank", body, page_size, lesson_label)


# ---------------------------------------------------------------------------
# Part I -- notes, straight from the lesson .md via the same renderer the web uses
# ---------------------------------------------------------------------------

def cut_notes(text, n):
    """Head (opening headnotes, via make_learn.split_lesson_body) + the Stage 0/1 body,
    stopping before the worksheet material -- see NOTES_END_HEADING."""
    head_text, rest_text = make_learn.split_lesson_body(text)
    heading = NOTES_END_HEADING[n]
    lines = rest_text.split("\n")
    cut = None
    for i, ln in enumerate(lines):
        if ln.startswith(heading):
            cut = i
            break
    if cut is None:
        raise SystemExit(f"FATAL: LESSON-{n}.md has no '{heading}' heading to cut notes at")
    notes_rest = "\n".join(lines[:cut])
    return head_text, notes_rest


def build_notes_html(n, text, page_size):
    title_line = text.split("\n", 1)[0]
    title = title_line.lstrip("#").strip()
    head_text, notes_rest = cut_notes(text, n)
    meta = make_learn.lesson_metadata_paragraph(text)
    try:
        refs = make_learn.extract_record_refs(meta, f"LESSON-{n}.md")
    except ValueError as e:
        raise SystemExit(f"FATAL: {e}")
    footer = make_learn.build_record_footer(refs, [])

    # head_text still opens with the lesson's own "# Lesson N -- ..." line, which
    # make_primers.render() turns into its own <h1> -- the same way the web page gets its
    # title, per make_learn.py's run(). Adding a second <h1> here would duplicate it.
    body_html = make_primers.render(head_text) + make_primers.render(notes_rest)
    body_html = inject_stroke_figures_print(body_html)
    body_html = body_html.replace("<table>", '<div class="tablewrap"><table>').replace(
        "</table>", "</table></div>")
    body = body_html + footer
    return wrap_print_page(title, masthead(f"Lesson {n} — notes") + body,
                            page_size, f"Lesson {n} — notes")


# ---------------------------------------------------------------------------
# Part II -- sheets, from the RAW sidecar tables (not the compiled browser `items`)
# ---------------------------------------------------------------------------

def load_sidecar(n):
    path = DRILL_SRC / f"L{n:02d}.toml"
    with open(path, "rb") as f:
        return tomllib.load(f)


def syr(s):
    return f'<span class="syr">{s}</span>'


def vocab_sheet(vocab, lesson_label):
    a_items = "".join(
        f'<div class="item"><span class="n">{i+1}.</span> {syr(v["p"])} '
        f'<span class="blank"></span> <span class="blank"></span></div>'
        for i, v in enumerate(vocab)
    )
    b_items = "".join(
        f'<div class="item"><span class="n">{i+1}.</span> “{html.escape(v["a"])}” '
        f'<span class="blank wide"></span></div>'
        for i, v in enumerate(vocab)
    )
    front = (f'<div class="sheet-head"><h2>Vocabulary</h2><span class="sheet-tag">questions</span></div>'
              '<h3>A. Sound it out, then give the meaning</h3>' + a_items +
              '<h3>B. Write the Syriac for each meaning</h3>' + b_items)
    rows = "".join(
        f'<tr><td class="syr">{v["p"]}</td><td>{html.escape(v["t"])}</td><td>{html.escape(v["a"])}</td></tr>'
        for v in vocab
    )
    back = (f'<div class="sheet-head"><h2>Vocabulary — answers</h2>'
            f'<span class="sheet-tag">{html.escape(lesson_label)}</span></div>'
            '<table class="answer-table"><thead><tr><th>Syriac</th><th>Sound</th>'
            f'<th>Meaning</th></tr></thead><tbody>{rows}</tbody></table>')
    return front, back


def forms_sheet(forms, lesson_label):
    # Two blanks, neither answer shown -- name the cell, then give the gloss. The lesson's
    # own notes introduce each form's cell in prose; this is the closed-book recall check,
    # so printing the cell here (as an earlier draft did) would hand back the very answer
    # the sheet exists to test.
    items = "".join(
        f'<div class="item"><span class="n">{i+1}.</span> {syr(f["form"])} '
        f'<span class="blank"></span> <span class="blank"></span></div>'
        for i, f in enumerate(forms)
    )
    front = ('<div class="sheet-head"><h2>New forms</h2><span class="sheet-tag">questions</span></div>'
             '<p class="gloss">For each form: name the cell, then write the gloss.</p>' + items)
    rows = "".join(
        f'<tr><td class="syr">{f["form"]}</td><td>{html.escape(f.get("cell",""))}</td>'
        f'<td>{html.escape(f.get("gloss",""))}</td><td class="syr">{f.get("lemma","")}</td></tr>'
        for f in forms
    )
    back = ('<div class="sheet-head"><h2>New forms — answers</h2>'
            f'<span class="sheet-tag">{html.escape(lesson_label)}</span></div>'
            '<table class="answer-table"><thead><tr><th>Form</th><th>Cell</th>'
            f'<th>Gloss</th><th>Lemma</th></tr></thead><tbody>{rows}</tbody></table>')
    return front, back


def text_items_sheet(title, groups, lesson_label):
    """groups: list of (section_title, entries) where each entry has prompt/answer/
    translit/note/context -- used for the halfline+cloze sheet and the finish+whole+
    drills sheet. `drills` entries carry a full-sentence prompt with no blank and an
    English `answer` (translation, not a gap-fill) -- rendered as recognize/translate
    items rather than fill-in-the-blank, matching what they are on the web engine."""
    front_secs, back_rows, n = [], [], 0
    for sec_title, entries, is_drill in groups:
        if not entries:
            continue
        front_items = []
        for e in entries:
            n += 1
            if is_drill:
                front_items.append(
                    f'<div class="item"><span class="n">{n}.</span> {syr(e["prompt"])} '
                    f'<span class="blank wide"></span></div>')
                back_rows.append(f'<tr><td>{n}</td><td class="syr">{e["prompt"]}</td>'
                                  f'<td>{html.escape(e["answer"])}</td></tr>')
            else:
                note_html = (f' <span class="gloss">({html.escape(e["note"])})</span>'
                              if e.get("note") else "")
                front_items.append(
                    f'<div class="item"><span class="n">{n}.</span> {syr(e["prompt"])}'
                    f'{note_html}</div>')
                back_rows.append(f'<tr><td>{n}</td><td class="syr">{e.get("context","")}</td>'
                                  f'<td class="syr">{e["answer"]}</td>'
                                  f'<td>{html.escape(e.get("translit",""))}</td></tr>')
        front_secs.append(f'<h3>{html.escape(sec_title)}</h3>' + "".join(front_items))
    front = (f'<div class="sheet-head"><h2>{html.escape(title)}</h2>'
             '<span class="sheet-tag">questions</span></div>' + "".join(front_secs))
    back = (f'<div class="sheet-head"><h2>{html.escape(title)} — answers</h2>'
            f'<span class="sheet-tag">{html.escape(lesson_label)}</span></div>'
            '<table class="answer-table"><thead><tr><th>#</th><th>Item / context</th>'
            '<th>Answer</th><th>Notes</th></tr></thead><tbody>'
            + "".join(back_rows) + '</tbody></table>')
    return front, back


def letters_sheet(letters, lesson_label, title="Letters"):
    items = "".join(
        f'<div class="item"><span class="n">{i+1}.</span> {syr(l["p"])} '
        f'{stroke_print_figure(l["p"])}'
        f'<span class="blank"></span> <span class="blank"></span></div>'
        for i, l in enumerate(letters)
    )
    front = (f'<div class="sheet-head"><h2>{html.escape(title)}</h2>'
             '<span class="sheet-tag">copy each &middot; name it</span></div>' + items)
    rows = "".join(
        f'<tr><td class="syr">{l["p"]}</td><td>{html.escape(l["a"])}</td>'
        f'<td>{html.escape(l.get("note",""))}</td></tr>'
        for l in letters
    )
    back = (f'<div class="sheet-head"><h2>{html.escape(title)} — answers</h2>'
            f'<span class="sheet-tag">{html.escape(lesson_label)}</span></div>'
            '<table class="answer-table"><thead><tr><th>Letter</th><th>Name</th>'
            f'<th>Sound</th></tr></thead><tbody>{rows}</tbody></table>')
    return front, back


def pairs_triples_sheet(tagged_chunk, lesson_label, title="Pairs & triples"):
    """tagged_chunk: [(group_name, entry), ...] for ONE sheet -- see build_pairs_triples_sheets
    for the chunking that keeps this under one page."""
    items, back_rows, n, seen_group = [], [], 0, None
    for group_name, x in tagged_chunk:
        if group_name != seen_group:
            items.append(f'<h3>{group_name}</h3>')
            seen_group = group_name
        n += 1
        items.append(f'<div class="item"><span class="n">{n}.</span> {syr(x["p"])} '
                      f'<span class="blank wide"></span></div>')
        back_rows.append(f'<tr><td>{n}</td><td class="syr">{x["p"]}</td>'
                          f'<td>{html.escape(", ".join(x["letters"]))}</td></tr>')
    front = (f'<div class="sheet-head"><h2>{html.escape(title)}</h2>'
             '<span class="sheet-tag">name the letters in order</span></div>' + "".join(items))
    back = (f'<div class="sheet-head"><h2>{html.escape(title)} — answers</h2>'
            f'<span class="sheet-tag">{html.escape(lesson_label)}</span></div>'
            '<table class="answer-table"><thead><tr><th>#</th><th>Syriac</th>'
            f'<th>Letters</th></tr></thead><tbody>{"".join(back_rows)}</tbody></table>')
    return front, back


def build_pairs_triples_sheets(pairs, triples, cap, lesson_label):
    tagged = [("Pairs", x) for x in pairs] + [("Triples", x) for x in triples]
    chunks = [tagged[i:i + cap] for i in range(0, len(tagged), cap)]
    sheets = []
    for idx, ch in enumerate(chunks):
        if not ch:
            continue
        title = "Pairs & triples" if len(chunks) == 1 else f"Pairs & triples ({chr(97 + idx)})"
        sheets.append(pairs_triples_sheet(ch, lesson_label, title))
    return sheets


# Sheet cap: how many items may sit on one sheet's front before it splits into 1a/1b.
# Vocabulary rows are short (one line each) so they carry more per sheet than form/text
# items, which run two lines with their gloss -- SYRIAC-PDF-PLAN.md §3 "One side, one page".
# Measured against a rendered page, not guessed: the vocabulary sheet's front shows BOTH
# directions per word (A: sound+meaning, B: meaning->Syriac), i.e. 2N item-lines for N
# words, so its cap is half of what a single-direction sheet (forms, text items) can hold.
CAPS = {"vocab": 8, "forms": 12, "text": 10, "letters": 14, "pairs_triples": 14}


def chunk(seq, cap):
    return [seq[i:i + cap] for i in range(0, len(seq), cap)] or [[]]


def build_text_sheets(tagged_entries, cap, base_title, lesson_label):
    """tagged_entries: [(section_title, entry_dict, is_drill), ...], sidecar order.
    Chunked at `cap` total items per sheet (§3 "One side, one page"), regrouping by
    section title within each chunk so a split mid-section still gets its own heading;
    multiple sheets get lettered suffixes (a/b/...)."""
    if not tagged_entries:
        return []
    chunks = [tagged_entries[i:i + cap] for i in range(0, len(tagged_entries), cap)]
    sheets = []
    for idx, ch in enumerate(chunks):
        groups = []
        for title, entry, is_drill in ch:
            if groups and groups[-1][0] == title:
                groups[-1][1].append(entry)
            else:
                groups.append([title, [entry], is_drill])
        suffix = "" if len(chunks) == 1 else f" ({chr(97 + idx)})"
        sheets.append(text_items_sheet(base_title + suffix,
                                        [(t, es, isd) for t, es, isd in groups],
                                        lesson_label))
    return sheets


def build_sheets_for_lesson(n, data, page_size):
    label = f"Lesson {n}"
    sheets = []  # list of (front_html, back_html)

    if n == 0:
        letter_chunks = chunk(data.get("letters", []), CAPS["letters"])
        for idx, part in enumerate(letter_chunks):
            if not part:
                continue
            title = "Letters" if len(letter_chunks) == 1 else f"Letters ({chr(97 + idx)})"
            sheets.append(letters_sheet(part, label, title))
        pairs, triples = data.get("pairs", []), data.get("triples", [])
        sheets.extend(build_pairs_triples_sheets(pairs, triples, CAPS["pairs_triples"], label))
    else:
        vocab = data.get("vocab", [])
        for i, part in enumerate(chunk(vocab, CAPS["vocab"])):
            if part:
                sheets.append(vocab_sheet(part, label))

        forms = data.get("forms", [])
        for part in chunk(forms, CAPS["forms"]):
            if part:
                sheets.append(forms_sheet(part, label))

        tagged_ab = ([("Half a line", e, False) for e in data.get("halfline", [])]
                     + [("One word", e, False) for e in data.get("cloze", [])])
        sheets.extend(build_text_sheets(tagged_ab, CAPS["text"], "Half a line · One word", label))

        tagged_cd = ([("Finish the line", e, False) for e in data.get("finish", [])]
                     + [("The whole line", e, False) for e in data.get("whole", [])]
                     + [("Our drills — translate", e, True) for e in data.get("drills", [])])
        sheets.extend(build_text_sheets(tagged_cd, CAPS["text"], "Finish · whole line · drills", label))

    return sheets


def build_sheets_html(n, data, page_size):
    """One page per front/back side, in sheet order; every side after the very first
    gets an explicit page break, so N sheets always render as exactly 2N pages."""
    sheets = build_sheets_for_lesson(n, data, page_size)
    label = f"Lesson {n}"
    sides = []
    for front, back in sheets:
        sides.append(front)
        sides.append(back)
    body = "".join(
        f'<div{" " if i == 0 else " style=\"break-before:page\" "}>{masthead(label)}{side}</div>'
        for i, side in enumerate(sides)
    )
    return wrap_print_page(f"{label} worksheets", body, page_size, f"{label} — worksheets"), len(sheets)


def build_scorecard_html(n, data, page_size):
    label = f"Lesson {n}"
    sc = data.get("scorecard", {})
    lines = []
    if sc.get("stage0_question"):
        lines.append(f'<dt>Stage 0</dt><dd>{html.escape(sc["stage0_question"])} ☐ yes ☐ no</dd>')
    if sc.get("stage1_of"):
        lines.append(f'<dt>Stage 1</dt><dd>{html.escape(sc.get("stage1_label",""))} '
                      f'____ / {sc["stage1_of"]}</dd>')
    lines.append('<dt>Stage 2 &amp; 3</dt><dd>how many of each closed-book pass? ____ / ____</dd>')
    opts = sc.get("stage4_options", ["written from memory", "transcribed"])
    lines.append('<dt>Stage 4</dt><dd>' + " / ".join(f'☐ {html.escape(o)}' for o in opts) + ' / ☐ not yet</dd>')
    lines.append('<dt>Where exactly did it stop being fun?</dt><dd>' + '_' * 50 + '</dd>')
    lines.append('<dt>Total time</dt><dd>____ minutes, in ____ sittings.</dd>')
    body = (masthead(f"{label} — scorecard") +
            f'<h1>Scorecard</h1><div class="scorecard"><dl>{"".join(lines)}</dl></div>'
            '<p class="footer">Keep this page, or copy it into an email if you’d '
            'like a Syriacist to see how the lesson went.</p>')
    return wrap_print_page(f"{label} scorecard", body, page_size, f"{label} — scorecard")


# ---------------------------------------------------------------------------
# Per-lesson, per-size pipeline
# ---------------------------------------------------------------------------

def build_one(n, page_size, write, errors):
    lf = SYRIAC_DIR / f"LESSON-{n}.md"
    text = lf.read_text(encoding="utf-8")
    data = load_sidecar(n)
    label = f"Lesson {n}"

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        notes_pdf = td / "notes.pdf"
        render_pdf(build_notes_html(n, text, page_size), notes_pdf, page_size)
        notes_pages = pdf_page_count(notes_pdf)

        pad_pdf = None
        if notes_pages % 2 == 1:
            pad_pdf = td / "blank.pdf"
            render_pdf(blank_page_html(page_size, label), pad_pdf, page_size)
            if pdf_page_count(pad_pdf) != 1:
                errors.append(f"L{n:02d}/{page_size}: blank padding page did not render as exactly 1 page")

        sheets_html, n_sheets = build_sheets_html(n, data, page_size)
        sheets_pdf = td / "sheets.pdf"
        if n_sheets:
            render_pdf(sheets_html, sheets_pdf, page_size)
            got = pdf_page_count(sheets_pdf)
            want = 2 * n_sheets
            if got != want:
                errors.append(f"L{n:02d}/{page_size}: sheets rendered to {got} pages, "
                               f"expected {want} ({n_sheets} sheet(s) × 2)")
        else:
            sheets_pdf = None

        score_pdf = td / "score.pdf"
        render_pdf(build_scorecard_html(n, data, page_size), score_pdf, page_size)
        if pdf_page_count(score_pdf) != 1:
            errors.append(f"L{n:02d}/{page_size}: scorecard did not render as exactly 1 page")

        if write and not errors:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            suffix = "" if page_size == "letter" else f"-{page_size}"
            out = OUT_DIR / f"lesson-{n}{suffix}.pdf"
            parts = [notes_pdf, pad_pdf, sheets_pdf, score_pdf]
            qpdf_merge(parts, out)
            return out
    return None


def build_bundle(page_size, lesson_outs, write):
    if not write or not lesson_outs:
        return None
    suffix = "" if page_size == "letter" else f"-{page_size}"
    out = OUT_DIR / f"chrestomathy{suffix}.pdf"
    qpdf_merge(lesson_outs, out)
    return out


def main():
    argv = sys.argv[1:]
    check = "--check" in argv
    write = not check
    only = None
    if "--lesson" in argv:
        only = int(argv[argv.index("--lesson") + 1])

    lessons = [only] if only is not None else list(range(N_LESSONS))
    errors = []
    outs_by_size = {size: [] for size in PAGE_SIZES}

    for n in lessons:
        for size in PAGE_SIZES:
            lesson_errors = []
            out = build_one(n, size, write, lesson_errors)
            errors.extend(lesson_errors)
            if out:
                outs_by_size[size].append(out)
            print(f"{'FAIL' if lesson_errors else 'ok'}  L{n:02d} {size}"
                  + (f" -- {'; '.join(lesson_errors)}" if lesson_errors else ""))

    if only is None:
        for size, outs in outs_by_size.items():
            build_bundle(size, outs, write)

    if errors:
        print(f"\nFAIL -- {len(errors)} problem(s)", file=sys.stderr)
        raise SystemExit(1)
    verb = "verified" if check else "wrote"
    print(f"OK -- {verb} {len(lessons)} lesson(s) × {len(PAGE_SIZES)} size(s)")


if __name__ == "__main__":
    main()
