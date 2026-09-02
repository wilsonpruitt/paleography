#!/usr/bin/env python3
"""Phase A of the Syriac web build -- render learn/syriac/LESSON-*.md and the R1/R3/R4
records they cite into learn/site/. Score: SYRIAC-WEB-PLAN.md §5 "Phase A".

Reuses tools/make_primers.py's Markdown renderer rather than forking it (that file's own
stated principle: no dependencies, one small local renderer for a closed set of Markdown).
This script adds only what that renderer doesn't need for its own callers: a blockquote
gets added to tools/make_primers.py itself (harmless there, needed here for the lessons'
Stage-1/2/3 quoted verses and gap-fill items).

Two things this script owns that make_primers.py's callers don't need:
  - a per-lesson FOOTER, built from the record ids cited in the lesson's own opening
    metadata line (the italic paragraph right after the H1) -- see extract_record_refs().
  - a generic TOML -> HTML record view for every quarry/*/r1|r3|r4/*.toml file, because
    Phase A's gate is "every record id in every lesson footer resolves to a rendered
    record" and Phase D's /sources index wants the full set rendered anyway (cheap now).

Usage:  python3 learn/tools/make_learn.py           # build
        python3 learn/tools/make_learn.py --check   # verify only, no writes; exit != 0 on failure
"""
import glob
import html
import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent          # learn/tools
LEARN = HERE.parent                              # learn/
ROOT = LEARN.parent                              # repo root

sys.path.insert(0, str(ROOT / "tools"))
import make_primers  # noqa: E402  (render(), inline() -- the shared closed-set Markdown renderer)
sys.path.insert(0, str(HERE))
import make_drill  # noqa: E402  (Phase B: drill/L*.toml -> site/drill/L*.json, + verbatim check)

SYRIAC_DIR = LEARN / "syriac"
SHELL = LEARN / "shell" / "lesson_shell.html"
DRILL_SHELL = LEARN / "shell" / "drill_shell.html"
SITE = LEARN / "site"
QUARRY = ROOT / "quarry"

N_LESSONS = 11  # L00..L10


# ---------------------------------------------------------------------------
# 1. Unsupported-Markdown gate
# ---------------------------------------------------------------------------

def find_unsupported(text, fname):
    """Return a list of (line_no, message) for constructs outside make_primers.render()'s
    closed set: headings, paragraphs, tables, top-level bullets/numbered lists,
    blockquotes, fences, bold/italic/code/links, hr. Anything else is drift, not a new
    feature quietly supported -- flag it rather than let it fall through render()'s own
    escape-and-pass-through paragraph branch unnoticed."""
    problems = []
    lines = text.split("\n")
    for n, ln in enumerate(lines, start=1):
        if re.search(r"!\[[^\]]*\]\(", ln):
            problems.append((n, "image syntax ![...](...) is not in the closed set"))
        if re.match(r"^[ \t]+[-*] ", ln):
            problems.append((n, "indented (nested) bullet -- render() only sees top-level bullets"))
        if re.match(r"^[ \t]+\d+\. ", ln):
            problems.append((n, "indented (nested) numbered item -- render() only sees top-level"))
        if re.search(r"<[a-zA-Z][a-zA-Z0-9]*[ >/]", ln):
            problems.append((n, "raw HTML tag -- not escaped/rendered by render()"))
        if "\t" in ln:
            problems.append((n, "literal tab character"))
    # Unmatched inline markers anywhere in the file (not line-by-line: a paragraph, table
    # cell, or blockquote item can wrap across lines).
    if text.count("`") % 2 != 0:
        problems.append((0, "odd number of backticks in the file -- an unclosed `code` span"))
    stars_no_bold = re.sub(r"\*\*", "", text)
    if stars_no_bold.count("*") % 2 != 0:
        problems.append((0, "odd number of single '*' after removing '**' pairs -- an unclosed *italic* span"))
    return problems


# ---------------------------------------------------------------------------
# 2. Record refs cited in a lesson's opening metadata line
# ---------------------------------------------------------------------------

def lesson_metadata_paragraph(text):
    """The italic paragraph right after the H1: skip the H1 line, skip blank lines, then
    collect contiguous non-blank lines up to the next blank line."""
    lines = text.split("\n")
    i = 0
    while i < len(lines) and not lines[i].startswith("#"):
        i += 1
    i += 1  # past the H1
    while i < len(lines) and not lines[i].strip():
        i += 1
    buf = []
    while i < len(lines) and lines[i].strip():
        buf.append(lines[i])
        i += 1
    return " ".join(buf)


def extract_record_refs(meta_text, lesson_name):
    """Backtick tokens ending .toml. A full path (contains '/') sets the current
    primer+rtype; a bare filename inherits the most recent full path's dir. Raises
    ValueError on a bare token with no preceding full path, or a full path that doesn't
    match quarry/<primer>/<rN>/<stem>.toml -- flag, don't guess."""
    refs = []
    current = None
    for tok in re.findall(r"`([^`]+)`", meta_text):
        if not tok.endswith(".toml"):
            continue
        if "/" in tok:
            m = re.match(r"^quarry/([^/]+)/(r\d)/([^/]+)\.toml$", tok)
            if not m:
                raise ValueError(f"{lesson_name}: unrecognized record path `{tok}`")
            primer, rtype, stem = m.groups()
            current = (primer, rtype)
        else:
            stem = tok[:-5]
            if current is None:
                raise ValueError(f"{lesson_name}: bare record ref `{tok}` with no preceding full path")
            primer, rtype = current
        refs.append((primer, rtype, stem))
    return refs


# ---------------------------------------------------------------------------
# 3. Generic TOML record -> HTML
# ---------------------------------------------------------------------------

PROMINENT = ("id", "record_type", "kind", "status", "uncertain", "uncertain_note")


def render_value(key, val):
    """One field -> a chunk of HTML. Recurses for dicts/lists; no per-schema special
    casing, since R1/R3/R4 each carry a different, evolving set of fields."""
    if isinstance(val, bool):
        return f'<div class="field"><span class="k">{html.escape(key)}</span> {"yes" if val else "no"}</div>'
    if isinstance(val, (int, float)):
        return f'<div class="field"><span class="k">{html.escape(key)}</span> {val}</div>'
    if isinstance(val, str):
        if "\n" in val.strip() or len(val) > 120:
            paras = "".join(f"<p>{make_primers.inline(p.strip())}</p>"
                            for p in val.strip().split("\n\n") if p.strip())
            return f'<div class="field block"><h4>{html.escape(key)}</h4>{paras}</div>'
        return f'<div class="field"><span class="k">{html.escape(key)}</span> {make_primers.inline(val)}</div>'
    if isinstance(val, dict):
        inner = "".join(render_value(k, v) for k, v in val.items())
        return f'<div class="field nested"><h4>{html.escape(key)}</h4>{inner}</div>'
    if isinstance(val, list):
        if not val:
            return ""
        if all(isinstance(e, str) for e in val):
            items = "".join(f"<li>{make_primers.inline(e)}</li>" for e in val)
            return f'<div class="field"><h4>{html.escape(key)}</h4><ul>{items}</ul></div>'
        if all(isinstance(e, dict) for e in val):
            cols = []
            for e in val:
                for k in e.keys():
                    if k not in cols:
                        cols.append(k)
            rows = "".join(
                "<tr>" + "".join(f"<td>{make_primers.inline(str(e[c])) if c in e else ''}</td>" for c in cols) + "</tr>"
                for e in val
            )
            head = "".join(f"<th>{html.escape(c)}</th>" for c in cols)
            return (f'<div class="field block"><h4>{html.escape(key)}</h4>'
                    f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead>'
                    f'<tbody>{rows}</tbody></table></div></div>')
        # mixed-type list: fall back to a definition list, one <li> per entry, joined
        items = "".join(f"<li>{make_primers.inline(str(e))}</li>" for e in val)
        return f'<div class="field"><h4>{html.escape(key)}</h4><ul>{items}</ul></div>'
    return f'<div class="field"><span class="k">{html.escape(key)}</span> {html.escape(str(val))}</div>'


def render_record(data, rtype, stem):
    badges = ""
    if data.get("kind"):
        badges += f'<span class="badge">{html.escape(data["kind"])}</span>'
    if data.get("status"):
        badges += f'<span class="badge">{html.escape(str(data["status"]))}</span>'
    if data.get("uncertain"):
        badges += '<span class="badge uncertain">uncertain</span>'
    head = (f'<p class="recordmeta">{html.escape(data.get("record_type",""))} '
            f'&middot; <code>{html.escape(data.get("id",""))}</code>{badges}</p>')
    rest = "".join(render_value(k, v) for k, v in data.items()
                    if k not in ("id", "record_type"))
    body = head + rest
    title = f'{rtype.upper()} record: {stem}'
    return title, body


# ---------------------------------------------------------------------------
# 4. Gather every quarry record
# ---------------------------------------------------------------------------

def gather_records():
    records = {}  # (rtype, stem) -> (primer, path, data)
    for path in sorted(glob.glob(str(QUARRY / "*/r*/*.toml"))):
        p = Path(path)
        primer, rtype = p.parent.parent.name, p.parent.name
        stem = p.stem
        with open(p, "rb") as f:
            try:
                data = tomllib.load(f)
            except Exception as e:
                raise SystemExit(f"FATAL: {path} does not parse as TOML: {e}")
        key = (rtype, stem)
        if key in records:
            raise SystemExit(f"FATAL: record id collision at {rtype}/{stem} -- {records[key][1]} vs {path}")
        records[key] = (primer, path, data)
    return records


# ---------------------------------------------------------------------------
# 5. Build
# ---------------------------------------------------------------------------

def wrap_page(title, desc, body, footer=""):
    shell = SHELL.read_text(encoding="utf-8")
    return (shell.replace("__TITLE__", html.escape(title))
                 .replace("__DESC__", html.escape(desc))
                 .replace("__BODY__", body)
                 .replace("__FOOTER__", footer))


def build_record_footer(refs, missing_out):
    items = []
    for primer, rtype, stem in refs:
        path = QUARRY / primer / rtype / f"{stem}.toml"
        if not path.exists():
            missing_out.append((primer, rtype, stem, path))
            continue
        items.append(f'<li><code>{html.escape(stem)}</code> ({html.escape(primer)}, {rtype}) '
                     f'&mdash; <a href="/sources/{rtype}/{stem}">source record</a></li>')
    if not items:
        return ""
    return f'<div class="footer"><strong>Sources cited</strong><ul>{"".join(items)}</ul></div>'


def run(write):
    errors = []
    missing = []

    lesson_files = [SYRIAC_DIR / f"LESSON-{n}.md" for n in range(N_LESSONS)]
    for lf in lesson_files:
        if not lf.exists():
            errors.append(f"missing lesson file: {lf}")

    records = gather_records()

    lesson_texts = {f"L{n:02d}": lf.read_text(encoding="utf-8")
                     for n, lf in enumerate(lesson_files) if lf.exists()}
    drill_errors, drill_compiled = make_drill.build(lesson_texts, write=write)
    errors.extend(f"[drill] {e}" for e in drill_errors)
    drill_shell_src = DRILL_SHELL.read_text(encoding="utf-8") if DRILL_SHELL.exists() else ""

    for n, lf in enumerate(lesson_files):
        if not lf.exists():
            continue
        text = lf.read_text(encoding="utf-8")
        for line_no, msg in find_unsupported(text, lf.name):
            where = f"{lf.name}:{line_no}" if line_no else lf.name
            errors.append(f"{where}: {msg}")

        meta = lesson_metadata_paragraph(text)
        try:
            refs = extract_record_refs(meta, lf.name)
        except ValueError as e:
            errors.append(str(e))
            refs = []
        if not refs:
            errors.append(f"{lf.name}: no record refs found in opening metadata line")

        lesson_missing = []
        for primer, rtype, stem in refs:
            path = QUARRY / primer / rtype / f"{stem}.toml"
            if not path.exists():
                lesson_missing.append((primer, rtype, stem, path))
        missing.extend(lesson_missing)
        for primer, rtype, stem, path in lesson_missing:
            errors.append(f"{lf.name}: record ref `{primer}/{rtype}/{stem}.toml` does not exist ({path})")

        if write:
            title_line = text.split("\n", 1)[0]
            title = title_line.lstrip("#").strip()
            desc = meta.strip()[:200]
            body = make_primers.render(text)
            body = body.replace("<table>", '<div class="tablewrap"><table>').replace(
                "</table>", "</table></div>")
            lid = f"L{n:02d}"
            if lid in drill_compiled and drill_shell_src:
                body += f'\n<div data-lesson="{lid}">{drill_shell_src}</div>\n'
            footer = build_record_footer(refs, [])
            prevn = f'<a href="/lesson/{n-1}">&larr; Lesson {n-1}</a>' if n > 0 else '<a href="/">&larr; Course</a>'
            nextn = f'<a href="/lesson/{n+1}">Lesson {n+1} &rarr;</a>' if n < N_LESSONS - 1 else '<span></span>'
            footer += f'<div class="lessonnav">{prevn}{nextn}</div>'
            page = wrap_page(title, desc, body, footer)
            dest = SITE / "lesson" / str(n) / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page, encoding="utf-8")

    if write:
        for (rtype, stem), (primer, path, data) in records.items():
            title, body = render_record(data, rtype, stem)
            page = wrap_page(title, f"{rtype.upper()} source record {stem}, from {primer}", body)
            dest = SITE / "sources" / rtype / stem / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page, encoding="utf-8")

    return errors, records, lesson_files


def main():
    check = "--check" in sys.argv
    errors, records, lesson_files = run(write=not check)
    if errors:
        print(f"FAIL -- {len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        raise SystemExit(1)
    n_written = len(lesson_files) + len(records)
    verb = "verified" if check else "wrote"
    print(f"OK -- {verb} {len(lesson_files)} lesson pages + {len(records)} record pages"
          f"{'' if check else f' under {SITE}'}")


if __name__ == "__main__":
    main()
