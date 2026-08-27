#!/usr/bin/env python3
"""Inject the exercise payload into the trainer shell -> build/scriptorium.html."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
shell = (root / "tools/trainer_shell.html").read_text(encoding="utf-8")
payload = (root / "build/exercises.json").read_text(encoding="utf-8")
if "</script" in payload.lower():
    raise SystemExit("payload contains </script and would break out of the tag")
out = root / "build/scriptorium.html"
out.write_text(shell.replace("__PAYLOAD__", payload), encoding="utf-8")
print(f"{out} — {out.stat().st_size/1024/1024:.2f} MB")
