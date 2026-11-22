"""Generic loop check. Discovers every loop and runs its checker twice.

A loop is a skill folder that holds a `loop.json`. See docs/loop-pattern.md.
For each loop this check confirms the shape, runs the loop's checker on its
demo workspace (must pass), then on a broken copy per declared break (must fail).
"""
import json
import re
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


DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# A number standing alone in a JSON value, table cell or CSV cell. Prose and dates do not match.
NUMBER_RE = re.compile(r"(?<=[|,:\[])(\s*)-?\d+(?:\.\d+)?(\s*)(?=[|,\]}\n]|$)", re.M)
TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt"}


# Each corruption is a text -> text function, applied to a copy of the demo.
CORRUPTIONS = {
    "text where numbers go": (TEXT_SUFFIXES, lambda t: NUMBER_RE.sub(r"\1junk\2", t)),
    "garbage where dates go": (TEXT_SUFFIXES, lambda t: DATE_RE.sub("9999-99-99", t)),
    "empty JSON": ({".json"}, lambda t: ""),
    "invalid JSON": ({".json"}, lambda t: "{not json"),
}


def _corrupt(workspace, suffixes, fn, only=None):
    """Rewrite matching files (or just `only`). Return how many files changed."""
    changed = 0
    for f in sorted(workspace.rglob("*")):
        if f.is_file() and f.suffix in suffixes and (only is None or f == only):
            old = f.read_text(encoding="utf-8")
            new = fn(old)
            if new != old:
                f.write_text(new, encoding="utf-8")
                changed += 1
    return changed


def _crashed(out):
    return "Traceback (most recent call last)" in out


def check_junk_input(checker, demo, label):
    """A checker must reject junk input with a problem line, never a Python traceback.

    Whole demo: every corruption at once must exit non-zero. Then each file alone gets
    each corruption, so an early exit on one bad file cannot hide a crash on another.
    """
    problems = []
    for why, (suffixes, fn) in CORRUPTIONS.items():
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / "demo"
            shutil.copytree(demo, copy)
            if not _corrupt(copy, suffixes, fn):
                continue
            code, out = run_checker(checker, copy)
            if _crashed(out):
                problems.append(f"{label}: checker crashes on junk input ({why}): {out.splitlines()[-1]}")
            elif code == 0:
                problems.append(f"{label}: checker accepts junk input ({why})")
        for f in sorted(p for p in demo.rglob("*") if p.is_file() and p.suffix in suffixes):
            rel = f.relative_to(demo)
            with tempfile.TemporaryDirectory() as t:
                copy = Path(t) / "demo"
                shutil.copytree(demo, copy)
                if not _corrupt(copy, suffixes, fn, only=copy / rel):
                    continue
                code, out = run_checker(checker, copy)
                if _crashed(out):
                    problems.append(f"{label}: checker crashes on junk in {rel} ({why}): {out.splitlines()[-1]}")
    return problems


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
    problems += check_junk_input(checker, demo, label)
    return problems


def check_loops(root):
    root = Path(root)
    problems = []
    for manifest in discover_loops(root):
        problems += check_loop(manifest, root)
    return problems
