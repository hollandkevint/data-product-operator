"""Generic loop check. Discovers every loop and runs its checker twice.

A loop is a skill folder that holds a `loop.json`. See docs/loop-pattern.md.
For each loop this check confirms the shape, runs the loop's checker on its
demo workspace (must pass), then on a broken copy per declared break (must fail).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REQUIRED_KEYS = ("name", "trigger", "checker", "demo", "breaks")
REQUIRED_HEADINGS = ("## Maker", "## Checker", "## State", "## Trigger", "## Demo data")


def discover_loops(root):
    return sorted(Path(root).glob("skills/*/loop.json"))


def run_checker(checker, workspace):
    """Return (exit code, output). Never raises on a checker crash."""
    try:
        p = subprocess.run([sys.executable, str(checker), str(workspace)],
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return 1, "checker timed out"
    return p.returncode, (p.stdout + p.stderr).strip()


def check_loop(manifest_path, root):
    base = manifest_path.parent
    label = f"{base.relative_to(root)}"
    try:
        m = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{label}/loop.json: not valid JSON ({e})"]
    problems = [f"{label}/loop.json: key '{k}' is missing" for k in REQUIRED_KEYS if k not in m]
    if problems:
        return problems
    if m["name"] != base.name:
        problems.append(f"{label}/loop.json: name '{m['name']}' does not match the folder")
    skill = base / "SKILL.md"
    if not skill.exists():
        problems.append(f"{label}: SKILL.md is missing")
    else:
        text = skill.read_text(encoding="utf-8")
        problems += [f"{label}/SKILL.md: heading '{h}' is missing"
                     for h in REQUIRED_HEADINGS if h not in text]
    checker, demo = base / m["checker"], base / m["demo"]
    if not checker.is_file():
        problems.append(f"{label}: checker {m['checker']} is missing")
    if not demo.is_dir():
        problems.append(f"{label}: demo folder {m['demo']} is missing")
    if not m["breaks"]:
        problems.append(f"{label}/loop.json: needs at least one break")
    if problems:
        return problems

    code, out = run_checker(checker, demo)
    if code != 0:
        problems.append(f"{label}: checker rejects its own demo data: {out.splitlines()[:3]}")
    for b in m["breaks"]:
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / "demo"
            shutil.copytree(demo, copy)
            target = copy / b["file"]
            if not target.is_file():
                problems.append(f"{label}: break '{b['why']}' names a missing file {b['file']}")
                continue
            old = target.read_text(encoding="utf-8")
            if b["find"] not in old:
                problems.append(f"{label}: break '{b['why']}' finds nothing to change in {b['file']}")
                continue
            target.write_text(old.replace(b["find"], b["replace"]), encoding="utf-8")
            code, _ = run_checker(checker, copy)
            if code == 0:
                problems.append(f"{label}: checker accepts a broken copy ({b['why']})")
    return problems


def check_loops(root):
    root = Path(root)
    problems = []
    for manifest in discover_loops(root):
        problems += check_loop(manifest, root)
    return problems
