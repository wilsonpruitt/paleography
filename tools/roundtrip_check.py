#!/usr/bin/env python3
"""Export a witness to PAGE XML, re-import it, and prove nothing was lost.

The point of choosing PAGE was portability. An exporter nobody has round-tripped is a
claim, not a guarantee -- so this asserts it: same line count, same text (NFC), same
polygons and baselines, same region types.
"""
import json, subprocess, sys, tempfile, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest import ingest


def main(jsonl, image_root=None):
    src = [json.loads(l) for l in open(jsonl, encoding="utf-8")]
    with tempfile.TemporaryDirectory() as td:
        xml_dir = Path(td) / "xml"
        cmd = [sys.executable, str(Path(__file__).parent / "export_page.py"), jsonl, str(xml_dir)]
        if image_root:
            cmd += ["--image-root", image_root]
        subprocess.run(cmd, check=True, capture_output=True)
        back_path = Path(td) / "back.jsonl"
        with open(back_path, "w", encoding="utf-8") as fh:
            ingest(str(xml_dir), src[0]["witness"], src[0]["layer"], fh)
        back = [json.loads(l) for l in open(back_path, encoding="utf-8")]

    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{'' if cond else '  ' + detail}")
        ok = ok and cond

    check("line count", len(src) == len(back), f"{len(src)} -> {len(back)}")
    si = {(r["page"], r["line_id"]): r for r in src}
    bi = {(r["page"], r["line_id"]): r for r in back}
    check("line ids preserved", set(si) == set(bi),
          f"{len(set(si) - set(bi))} lost, {len(set(bi) - set(si))} invented")

    shared = set(si) & set(bi)
    def norm(s): return unicodedata.normalize("NFC", s)
    bad_t = [k for k in shared if norm(si[k]["text"]) != norm(bi[k]["text"])]
    check("text identical", not bad_t, f"{len(bad_t)} differ e.g. {list(bad_t)[:1]}")
    bad_p = [k for k in shared if si[k].get("polygon") != bi[k].get("polygon")]
    check("polygons identical", not bad_p, f"{len(bad_p)} differ")
    bad_b = [k for k in shared if si[k].get("baseline") != bi[k].get("baseline")]
    check("baselines identical", not bad_b, f"{len(bad_b)} differ")
    bad_r = [k for k in shared if si[k].get("region_type") != bi[k].get("region_type")]
    check("region types identical", not bad_r, f"{len(bad_r)} differ")

    chars = sum(len(r["text"]) for r in src)
    print(f"  ({len(src)} lines, {chars} characters round-tripped)")
    return 0 if ok else 1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl"); ap.add_argument("--image-root", default=None)
    a = ap.parse_args()
    print(f"round-trip: {a.jsonl}")
    sys.exit(main(a.jsonl, a.image_root))
